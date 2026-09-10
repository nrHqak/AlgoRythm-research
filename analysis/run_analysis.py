from __future__ import annotations

import argparse
import json
import shlex
import sys
from pathlib import Path
from typing import Any

import pandas as pd
import yaml

from analysis.metrics import evaluate_record
from analysis.reporting import write_outputs
from analysis.statistics import (
    clustered_bootstrap_delta,
    exact_mcnemar,
    exam_comparison,
    leave_one_program_out_delta,
    paired_by_program,
)
from experiments.health import assert_session_health
from experiments.models import ParsedRunRecord, load_manifest
from experiments.safety import (
    SafetyViolation,
    assert_condition_balance,
    assert_paired_settings,
    assert_raw_files_exist,
    assert_raw_prompt_symmetry,
    assert_unique_execution_keys,
    safety_summary,
)
from experiments.storage import file_sha256, path_sha256


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


def load_config(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("configuration root must be an object")
    return payload


def load_session_records(path: Path) -> list[ParsedRunRecord]:
    if not path.is_dir():
        raise ValueError(f"processed session directory does not exist: {path}")
    records: list[ParsedRunRecord] = []
    for record_path in sorted(path.glob("*.json")):
        payload = json.loads(record_path.read_text(encoding="utf-8"))
        if "run_id" not in payload:
            continue
        records.append(ParsedRunRecord.model_validate(payload))
    if not records:
        raise ValueError(f"no run records found in {path}")
    return records


def transitions(frame: pd.DataFrame, metric: str, control: str, treatment: str) -> dict[str, int]:
    pivot = frame.pivot(index=["program_id", "repetition"], columns="condition", values=metric)
    pivot = pivot[[control, treatment]].dropna().astype(int)
    return {
        "both_miss": int(((pivot[control] == 0) & (pivot[treatment] == 0)).sum()),
        "treatment_only": int(((pivot[control] == 0) & (pivot[treatment] == 1)).sum()),
        "control_only": int(((pivot[control] == 1) & (pivot[treatment] == 0)).sum()),
        "both_hit": int(((pivot[control] == 1) & (pivot[treatment] == 1)).sum()),
    }


def summarize_topk(
    frame: pd.DataFrame,
    *,
    metric: str,
    control: str,
    treatment: str,
    repetitions: int,
    bootstrap_iterations: int,
    seed: int,
) -> dict[str, Any]:
    conditions: dict[str, Any] = {}
    for name in (control, treatment):
        values = frame.loc[frame.condition == name, metric]
        hits = int(values.sum())
        total = int(values.count())
        conditions[name] = {"hits": hits, "total": total, "rate": hits / total}

    per_repetition: list[dict[str, Any]] = []
    for repetition in range(1, repetitions + 1):
        subset = frame.loc[frame.repetition == repetition]
        pivot = subset.pivot(index="program_id", columns="condition", values=metric)
        pivot = pivot[[control, treatment]].dropna()
        test = exact_mcnemar(pivot[control].to_numpy(), pivot[treatment].to_numpy())
        per_repetition.append(
            {
                "repetition": repetition,
                "n_programs": int(len(pivot)),
                "control_hits": int(pivot[control].sum()),
                "treatment_hits": int(pivot[treatment].sum()),
                **test,
            }
        )
    return {
        "conditions": conditions,
        "per_repetition_exact_mcnemar": per_repetition,
        "pooled_transitions": transitions(frame, metric, control, treatment),
        "pooled_transition_warning": (
            "Counts pool program-repetition pairs for visualization only; they are not an independent-sample test."
        ),
        "bootstrap": clustered_bootstrap_delta(
            frame,
            metric=metric,
            control_name=control,
            treatment_name=treatment,
            iterations=bootstrap_iterations,
            seed=seed,
        ),
    }


def complete_case_sensitivity(
    frame: pd.DataFrame, control: str, treatment: str
) -> dict[str, Any]:
    complete = frame.loc[frame.status == "ok"]
    paired_keys = (
        complete.groupby(["program_id", "repetition"])["condition"].nunique().loc[lambda value: value == 2].index
    )
    if len(paired_keys) == 0:
        return {"paired_program_repetitions": 0, "top1_delta": None, "exam_delta": None}
    indexed = complete.set_index(["program_id", "repetition"])
    paired = indexed.loc[indexed.index.isin(paired_keys)].reset_index()
    top1 = paired_by_program(paired, "top1", control, treatment)
    exam = paired_by_program(paired, "exam", control, treatment)
    return {
        "paired_program_repetitions": int(len(paired_keys)),
        "top1_delta": float((top1[treatment] - top1[control]).mean()),
        "exam_delta": float((exam[treatment] - exam[control]).mean()),
    }


def build_metrics(
    *,
    frame: pd.DataFrame,
    records: list[ParsedRunRecord],
    manifest: Any,
    config: dict[str, Any],
    bootstrap_iterations: int,
    seed: int,
    parser_failure_policy: str,
    engineering_only: bool,
) -> dict[str, Any]:
    control = str(config["conditions"]["control"])
    treatment = str(config["conditions"]["treatment"])
    repetitions = int(config["repetitions"])

    topk = {
        metric: summarize_topk(
            frame,
            metric=metric,
            control=control,
            treatment=treatment,
            repetitions=repetitions,
            bootstrap_iterations=bootstrap_iterations,
            seed=seed + index,
        )
        for index, metric in enumerate(("top1", "top3", "top5"))
    }
    pattern_means = (
        frame.groupby(["pattern_label", "condition"])[["top1", "top3", "top5", "exam"]]
        .agg(["sum", "count", "mean"])
    )
    per_pattern: dict[str, Any] = {}
    for pattern in sorted(frame.pattern_label.unique()):
        per_pattern[pattern] = {}
        for condition in (control, treatment):
            subset = frame[(frame.pattern_label == pattern) & (frame.condition == condition)]
            per_pattern[pattern][condition] = {
                metric: {
                    "sum": float(pattern_means.loc[(pattern, condition), (metric, "sum")]),
                    "count": int(pattern_means.loc[(pattern, condition), (metric, "count")]),
                    "mean": float(pattern_means.loc[(pattern, condition), (metric, "mean")]),
                }
                for metric in ("top1", "top3", "top5", "exam")
            }

    per_pattern_delta = {
        pattern: per_pattern[pattern][treatment]["top1"]["mean"]
        - per_pattern[pattern][control]["top1"]["mean"]
        for pattern in per_pattern
    }
    per_pattern_net_hits = {
        pattern: int(
            per_pattern[pattern][treatment]["top1"]["sum"]
            - per_pattern[pattern][control]["top1"]["sum"]
        )
        for pattern in per_pattern
    }
    positive_pattern_gain = sum(max(0, value) for value in per_pattern_net_hits.values())
    dominant_pattern = (
        max(per_pattern_net_hits, key=per_pattern_net_hits.get) if per_pattern_net_hits else None
    )
    per_rep_delta = {
        str(repetition): float(
            frame.loc[(frame.repetition == repetition) & (frame.condition == treatment), "top1"].mean()
            - frame.loc[(frame.repetition == repetition) & (frame.condition == control), "top1"].mean()
        )
        for repetition in range(1, repetitions + 1)
    }
    parser_by_condition = {
        condition: {
            "failures": int(
                ((frame.condition == condition) & (frame.status == "parser_failure")).sum()
            ),
            "total": int((frame.condition == condition).sum()),
        }
        for condition in (control, treatment)
    }
    prompt_lengths = {
        condition: {
            "mean_chars": float(frame.loc[frame.condition == condition, "prompt_chars"].mean()),
            "mean_tokens_estimate": float(
                frame.loc[frame.condition == condition, "prompt_tokens_estimate"].mean()
            ),
        }
        for condition in (control, treatment)
    }
    settings_values = frame[["provider", "model", "temperature", "max_tokens"]].drop_duplicates()
    if len(settings_values) != 1:
        raise SafetyViolation("analysis session contains more than one provider/model/settings tuple")
    settings = settings_values.iloc[0].to_dict()
    settings["temperature"] = float(settings["temperature"])
    settings["max_tokens"] = int(settings["max_tokens"])

    excluded = [program for program in manifest.programs if program.inclusion_status.value == "excluded"]
    return {
        "experiment_name": str(config["experiment_name"]),
        "session_id": str(frame.session_id.iloc[0]),
        "manifest_hash": str(frame.manifest_hash.iloc[0]),
        "n_programs": len(manifest.included),
        "n_programs_in_analysis": int(frame.program_id.nunique()),
        "program_ids": sorted(program.program_id for program in manifest.included),
        "n_run_records": int(len(frame)),
        "repetitions": repetitions,
        "parser_failure_policy": parser_failure_policy,
        "engineering_only": engineering_only,
        "settings": settings,
        "topk": topk,
        "exam": {
            **exam_comparison(frame, control, treatment),
            "bootstrap": clustered_bootstrap_delta(
                frame,
                metric="exam",
                control_name=control,
                treatment_name=treatment,
                iterations=bootstrap_iterations,
                seed=seed + 3,
            ),
        },
        "per_pattern": per_pattern,
        "safety": safety_summary(records),
        "exclusions": {
            "count": len(excluded),
            "programs": [
                {
                    "program_id": program.program_id,
                    "reason": program.exclusion_reason,
                    "decided_at": program.exclusion_decided_at.isoformat()
                    if program.exclusion_decided_at
                    else None,
                }
                for program in excluded
            ],
            "selection_frozen_at": manifest.selection_frozen_at.isoformat(),
        },
        "adversarial": {
            "per_pattern_top1_delta": per_pattern_delta,
            "per_pattern_top1_net_hits": per_pattern_net_hits,
            "dominant_positive_pattern": dominant_pattern,
            "dominant_positive_pattern_share": (
                max(0, per_pattern_net_hits[dominant_pattern]) / positive_pattern_gain
                if dominant_pattern is not None and positive_pattern_gain > 0
                else None
            ),
            "leave_one_program_out_top1": leave_one_program_out_delta(
                frame, "top1", control, treatment
            ),
            "per_repetition_top1_delta": per_rep_delta,
            "parser_failures_by_condition": parser_by_condition,
            "prompt_length_by_condition": prompt_lengths,
            "complete_case_sensitivity": complete_case_sensitivity(frame, control, treatment),
        },
    }


def run(args: argparse.Namespace) -> None:
    config = load_config(args.config)
    required_metrics = {"top1", "top3", "top5", "exam"}
    if set(config.get("metrics", [])) != required_metrics:
        raise SafetyViolation(f"pilot metrics must be exactly {sorted(required_metrics)}")
    if config.get("statistics", {}).get("primary") != "exact_mcnemar":
        raise SafetyViolation("pilot primary statistic must be exact_mcnemar")
    if args.bootstrap_iterations < 1:
        raise SafetyViolation("bootstrap iterations must be positive")
    manifest = load_manifest(args.manifest)
    experiment_name = str(config["experiment_name"])
    session_dir = args.results_root / "processed" / experiment_name / args.session_id
    session_manifest_path = session_dir / "session_manifest.json"
    session_manifest = json.loads(session_manifest_path.read_text(encoding="utf-8"))
    records = load_session_records(session_dir)
    control = str(config["conditions"]["control"])
    treatment = str(config["conditions"]["treatment"])
    repetitions = int(session_manifest["repetitions"])
    config = {**config, "repetitions": repetitions}

    if (session_dir / "VOID.json").exists():
        raise SafetyViolation("VOID session cannot produce scientific reports")
    assert_session_health(records)
    assert_unique_execution_keys(records)
    assert_condition_balance(
        records,
        repetitions=repetitions,
        control_name=control,
        treatment_name=treatment,
        expected_program_ids={program.program_id for program in manifest.included},
    )
    assert_paired_settings(records, control, treatment)
    assert_raw_files_exist(records, REPOSITORY_ROOT)
    assert_raw_prompt_symmetry(records, REPOSITORY_ROOT, control, treatment)
    expected_manifest_hash = file_sha256(args.manifest)
    actual_hashes = {record.manifest_hash for record in records}
    if actual_hashes != {expected_manifest_hash}:
        raise SafetyViolation(
            f"manifest mismatch: expected {expected_manifest_hash}, records contain {sorted(actual_hashes)}"
        )
    expected_settings = {
        (
            str(session_manifest["provider"]),
            str(session_manifest["model"]),
            float(session_manifest["temperature"]),
            int(session_manifest["max_tokens"]),
        )
    }
    actual_settings = {
        (record.provider, record.model, record.temperature, record.max_tokens)
        for record in records
    }
    if actual_settings != expected_settings:
        raise SafetyViolation(
            f"session settings mismatch: expected {expected_settings}, found {actual_settings}"
        )

    frame = pd.DataFrame(evaluate_record(record) for record in records)
    if args.parser_failure_policy == "exclude":
        frame = frame.loc[frame.status == "ok"].copy()
        # Exclusion is allowed only as an explicit sensitivity analysis and cannot satisfy primary balance.
        if frame.empty:
            raise SafetyViolation("all records were excluded by parser-failure policy")
    current_hashes = {
        program.program_id: {
            "buggy_source": path_sha256(program.buggy_source_path),
            "fixed_source": path_sha256(program.fixed_source_path),
            "tests": path_sha256(program.tests_path),
            "problem_context": (
                path_sha256(program.problem_context_path)
                if program.problem_context_path is not None
                else None
            ),
        }
        for program in manifest.programs
    }
    if current_hashes != session_manifest.get("program_input_hashes"):
        raise SafetyViolation("program source, fixed source, tests, or context changed after execution")
    engineering_only = bool(session_manifest.get("engineering_only"))
    if engineering_only and not args.allow_mock_analysis:
        raise SafetyViolation(
            "mock-provider sessions are engineering-only; pass --allow-mock-analysis for tests"
        )
    metrics = build_metrics(
        frame=frame,
        records=records,
        manifest=manifest,
        config=config,
        bootstrap_iterations=args.bootstrap_iterations,
        seed=args.seed,
        parser_failure_policy=args.parser_failure_policy,
        engineering_only=engineering_only,
    )
    metrics["reproducibility"] = {
        "runner_command": session_manifest["run_command"],
        "analysis_command": " ".join(shlex.quote(part) for part in sys.argv),
        "session_manifest": str(session_manifest_path),
    }
    command = metrics["reproducibility"]["runner_command"] + "\n" + metrics["reproducibility"]["analysis_command"]
    write_outputs(
        frame=frame,
        metrics=metrics,
        results_root=args.report_root or args.results_root,
        reproduce_command=command,
        control_name=control,
        treatment_name=treatment,
    )


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description="Evaluate and audit one complete pilot session.")
    result.add_argument("--config", type=Path, default=REPOSITORY_ROOT / "pilot/config/pilot.yaml")
    result.add_argument("--manifest", type=Path, required=True)
    result.add_argument("--session-id", required=True)
    result.add_argument("--results-root", type=Path, default=REPOSITORY_ROOT / "results")
    result.add_argument(
        "--parser-failure-policy",
        choices=("count_as_failure", "exclude"),
        required=True,
        help="Must be chosen by the frozen protocol; count_as_failure sets Top-K=0 and EXAM=1.",
    )
    result.add_argument("--bootstrap-iterations", type=int, default=10000)
    result.add_argument("--report-root", type=Path, help="Separate report directory; keeps v2 native session reports from overwriting each other")
    result.add_argument("--seed", type=int, default=20260908)
    result.add_argument("--allow-mock-analysis", action="store_true")
    return result


def main() -> None:
    args = parser().parse_args()
    try:
        run(args)
    except (ValueError, OSError, KeyError, SafetyViolation) as exc:
        print(f"analysis aborted: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
