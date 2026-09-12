"""Twenty-call realistic synthetic gate for the low-reasoning amendment."""
from __future__ import annotations

import argparse
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from dotenv import load_dotenv

from experiments.model_preflight import validate_identity_choice
from experiments.models import load_manifest
from experiments.prompts import build_prompt_pair
from experiments.providers.routing import add_routing_arguments, add_routing_settings
from experiments.run_pilot import (
    append_experiment_log,
    deterministic_run_id_for,
    load_prior_map,
    make_provider,
    run_one,
)
from experiments.safety import SafetyViolation
from experiments.storage import file_sha256, write_json_new


ROOT = Path(__file__).resolve().parents[1]
STRESS_MANIFEST = ROOT / "data/smoke-reasoning-low/manifest.json"
SCIENTIFIC_MANIFEST = ROOT / "data/manifests/pilot_manifest_v2_2.json"
METADATA = ROOT / (
    "pilot/v2/model-freeze-attempts/"
    "20260912T205114Z-openrouter-reasoning-metadata/reasoning_metadata.json"
)
SYSTEM = ROOT / "pilot/v2/prompts/system_v2.txt"
TEMPLATE = ROOT / "pilot/prompts/control.txt"
GENERIC_PRIORS = ROOT / "pilot/v2/generic_placebo_prior.json"
PATTERN_PRIORS = ROOT / "pilot/pattern_priors.json"
EXPECTED_PATTERNS = {
    "binary_search",
    "brute_force_implementation",
    "dynamic_programming",
    "graph_traversal_dfs_bfs",
}
EXPECTED_CALLS = 20
WORKERS = 4
REASONING_EFFORT = "low"
COST_GATE_USD = 4.50


def scientific_candidate_ids() -> set[str]:
    """Read IDs from the frozen manifest without loading any candidate source."""
    payload = json.loads(SCIENTIFIC_MANIFEST.read_text(encoding="utf-8"))
    return {
        str(program["program_id"])
        for program in payload["programs"]
        if program.get("inclusion_status") == "included"
    }


def asset_paths() -> list[Path]:
    manifest = load_manifest(STRESS_MANIFEST)
    paths = [
        STRESS_MANIFEST,
        SCIENTIFIC_MANIFEST,
        METADATA,
        SYSTEM,
        TEMPLATE,
        GENERIC_PRIORS,
        PATTERN_PRIORS,
    ]
    for program in manifest.included:
        paths.extend([program.buggy_source_path, program.fixed_source_path, program.tests_path])
    return list(dict.fromkeys(paths))


def validate_args(args: argparse.Namespace) -> None:
    validate_identity_choice(
        args.model,
        args.model_kind,
        args.model_reference,
        args.accepted_alias_risk,
    )
    if args.provider_label != "openrouter":
        raise SafetyViolation("reasoning preflight requires OpenRouter")
    if args.base_url.rstrip("/") != "https://openrouter.ai/api/v1":
        raise SafetyViolation("reasoning preflight requires the frozen OpenRouter endpoint")
    if args.model != "z-ai/glm-5.3-flash":
        raise SafetyViolation("reasoning preflight requires the exact frozen model")
    if args.temperature != 0 or args.max_tokens != 32768 or args.timeout != 120:
        raise SafetyViolation("temperature, max_tokens, or timeout differs from the freeze")
    if args.workers != WORKERS:
        raise SafetyViolation("reasoning preflight requires exactly four workers")
    if args.reasoning_effort != REASONING_EFFORT:
        raise SafetyViolation("reasoning preflight requires explicit low effort")
    if args.openrouter_provider != "z-ai/fp8" or args.openrouter_provider_name != "Z.AI":
        raise SafetyViolation("reasoning preflight requires the frozen Z.AI endpoint pin")

    metadata = json.loads(METADATA.read_text(encoding="utf-8"))
    reasoning = metadata.get("model_metadata", {})
    if REASONING_EFFORT not in reasoning.get("supported_efforts", []):
        raise SafetyViolation("live metadata record does not explicitly support low effort")
    if not reasoning.get("supports_max_tokens"):
        raise SafetyViolation("live metadata record does not support max_tokens")


def build_plan() -> list[dict]:
    stress = load_manifest(STRESS_MANIFEST)
    fixtures = stress.included
    if len(fixtures) != 4 or {item.pattern_label for item in fixtures} != EXPECTED_PATTERNS:
        raise SafetyViolation("stress frame must contain exactly the four frozen pattern families")
    science_ids = scientific_candidate_ids()
    if any(item.program_id in science_ids for item in fixtures):
        raise SafetyViolation("synthetic/scientific program-ID overlap")
    if any(not item.program_id.startswith("synthetic-reasoning-") for item in fixtures):
        raise SafetyViolation("preflight input is not explicitly synthetic")

    system = SYSTEM.read_text(encoding="utf-8")
    template = TEMPLATE.read_text(encoding="utf-8")
    plan: list[dict] = []
    for session, prior_path, arms in (
        ("G", GENERIC_PRIORS, ("A_G", "B")),
        ("P", PATTERN_PRIORS, ("A_P", "C")),
    ):
        priors = load_prior_map(prior_path)
        # Every prompt form sees every family once. The largest DP fixture receives
        # the fifth call in each arm so each of A_G/B/A_P/C has exactly five calls.
        scheduled = [(program, 1) for program in fixtures]
        scheduled.append((next(p for p in fixtures if p.pattern_label == "dynamic_programming"), 2))
        for program, repetition in scheduled:
            pair = build_prompt_pair(system, template, program, priors[program.pattern_label])
            for arm in arms:
                treatment = arm in {"B", "C"}
                plan.append(
                    {
                        "session": session,
                        "program": program,
                        "arm": arm,
                        "repetition": repetition,
                        "user_prompt": (
                            pair.treatment_user_prompt if treatment else pair.control_user_prompt
                        ),
                        "shared_prompt_hash": pair.shared_prompt_hash,
                        "prior_hash": pair.prior_hash if treatment else None,
                        "run_id": deterministic_run_id_for(
                            program_id=program.program_id,
                            condition=arm,
                            repetition=repetition,
                        ),
                    }
                )
    if len(plan) != EXPECTED_CALLS:
        raise SafetyViolation("preflight plan must contain exactly 20 calls")
    if [item["session"] for item in plan] != ["G"] * 10 + ["P"] * 10:
        raise SafetyViolation("preflight plan must be exactly ten G calls then ten P calls")
    if len({item["run_id"] for item in plan}) != EXPECTED_CALLS:
        raise SafetyViolation("deterministic run-ID collision")
    for arm in ("A_G", "B", "A_P", "C"):
        arm_items = [item for item in plan if item["arm"] == arm]
        if len(arm_items) != 5 or {item["program"].pattern_label for item in arm_items} != EXPECTED_PATTERNS:
            raise SafetyViolation(f"{arm} does not cover all four pattern families in five calls")
    return plan


def call_metric(record, raw: dict, order: int) -> dict:
    usage = raw.get("token_usage", {})
    details = usage.get("completion_tokens_details", {}) or {}
    output_tokens = usage.get("completion_tokens")
    reasoning_tokens = details.get("reasoning_tokens")
    final_content_tokens = (
        output_tokens - reasoning_tokens
        if isinstance(output_tokens, int) and isinstance(reasoning_tokens, int)
        else None
    )
    return {
        "order": order,
        "run_id": record.run_id,
        "program_id": record.program_id,
        "pattern_label": record.pattern_label,
        "session": record.experiment_name.rsplit("_", 1)[-1],
        "condition": record.condition,
        "repetition": record.repetition,
        "status": record.status,
        "error_type": record.error_type,
        "error_message": record.error_message,
        "input_tokens": usage.get("prompt_tokens"),
        "output_tokens": output_tokens,
        "reasoning_tokens": reasoning_tokens,
        "final_content_tokens": final_content_tokens,
        "finish_reason": raw.get("response_metadata", {}).get("finish_reason"),
        "latency_seconds": raw.get("latency"),
        "cost_usd": usage.get("cost"),
        "model": raw.get("actual_model"),
        "underlying_provider": raw.get("response_metadata", {}).get(
            "actual_underlying_provider"
        ),
        "reasoning_effort_requested": raw.get("response_metadata", {}).get(
            "reasoning_effort_requested"
        ),
        "content_is_null": raw.get("raw_response") is None if raw else True,
    }


def validate_record(record, raw: dict, settings: dict) -> None:
    if record.status != "ok":
        raise SafetyViolation(f"preflight call failed: {record.status}/{record.error_type}")
    if not record.raw_response or not record.raw_response.strip():
        raise SafetyViolation("completion content is null or empty")
    if all(item.score == 0 for item in record.parsed_response.ranking):
        raise SafetyViolation("all-zero suspicion scores: mechanical validity failed")
    metadata = raw.get("response_metadata", {})
    if raw.get("actual_model") != settings["model"]:
        raise SafetyViolation("exact model identity mismatch")
    if metadata.get("actual_underlying_provider") != "Z.AI":
        raise SafetyViolation("pinned underlying provider identity mismatch")
    if metadata.get("provider_preferences") != settings["openrouter_routing"]["provider_preferences"]:
        raise SafetyViolation("provider pin or fallback policy mismatch")
    if metadata.get("reasoning_effort_requested") != REASONING_EFFORT:
        raise SafetyViolation("request did not preserve explicit low reasoning effort")
    usage = raw.get("token_usage", {})
    output_tokens = usage.get("completion_tokens")
    reasoning_tokens = (usage.get("completion_tokens_details", {}) or {}).get("reasoning_tokens")
    final_tokens = (
        output_tokens - reasoning_tokens
        if isinstance(output_tokens, int) and isinstance(reasoning_tokens, int)
        else None
    )
    if metadata.get("finish_reason") != "stop" or output_tokens == 32768:
        raise SafetyViolation("completion reached the token ceiling or did not finish with stop")
    if any(
        value is None
        for value in (
            usage.get("prompt_tokens"),
            output_tokens,
            reasoning_tokens,
            final_tokens,
            raw.get("latency"),
            usage.get("cost"),
        )
    ):
        raise SafetyViolation("provider omitted required token, latency, or cost evidence")
    if final_tokens < 1:
        raise SafetyViolation("completion contains no final-content tokens")


def aggregate(metrics: list[dict], wall_seconds: float) -> dict:
    valid = [item for item in metrics if item["status"] == "ok"]
    failures = [item for item in metrics if item["status"] != "ok"]
    rate_limits = [
        item
        for item in failures
        if "429" in str(item.get("error_message"))
        or "rate limit" in str(item.get("error_message")).lower()
    ]
    throughput = len(metrics) / wall_seconds if wall_seconds > 0 else None
    costs = [float(item["cost_usd"]) for item in metrics if item["cost_usd"] is not None]
    reasoning = [item["reasoning_tokens"] for item in metrics if item["reasoning_tokens"] is not None]
    outputs = [item["output_tokens"] for item in metrics if item["output_tokens"] is not None]
    final_contents = [
        item["final_content_tokens"]
        for item in metrics
        if item["final_content_tokens"] is not None
    ]
    average_cost = sum(costs) / len(costs) if costs else None
    return {
        "calls_attempted": len(metrics),
        "calls_valid": len(valid),
        "failures": len(failures),
        "parser_failures": sum(item["status"] == "parser_failure" for item in metrics),
        "content_null_failures": sum(item["content_is_null"] for item in metrics),
        "length_truncations": sum(item["finish_reason"] == "length" for item in metrics),
        "provider_model_mismatches": sum(
            item["model"] not in (None, "z-ai/glm-5.3-flash")
            or item["underlying_provider"] not in (None, "Z.AI")
            for item in metrics
        ),
        "rate_limit_failures": len(rate_limits),
        "average_reasoning_tokens": sum(reasoning) / len(reasoning) if reasoning else None,
        "maximum_reasoning_tokens": max(reasoning) if reasoning else None,
        "average_output_tokens": sum(outputs) / len(outputs) if outputs else None,
        "maximum_output_tokens": max(outputs) if outputs else None,
        "average_final_content_tokens": (
            sum(final_contents) / len(final_contents) if final_contents else None
        ),
        "maximum_final_content_tokens": max(final_contents) if final_contents else None,
        "average_cost_usd": average_cost,
        "actual_cost_usd": sum(costs),
        "projected_600_call_cost_usd": average_cost * 600 if average_cost is not None else None,
        "wall_clock_seconds": wall_seconds,
        "observed_throughput_calls_per_minute": throughput * 60 if throughput else None,
        "projected_600_call_runtime_seconds": 600 / throughput if throughput else None,
        "projected_600_call_runtime_hours": 600 / throughput / 3600 if throughput else None,
    }


def run(args: argparse.Namespace) -> dict:
    validate_args(args)
    if args.output_root.exists():
        raise SafetyViolation("preflight output root already exists; evidence is immutable")
    plan = build_plan()
    args.output_root.mkdir(parents=True, exist_ok=False)
    load_dotenv(ROOT / ".env")
    metrics: list[dict] = []
    started = time.perf_counter()
    try:
        provider = make_provider(args)
        system = SYSTEM.read_text(encoding="utf-8")
        settings = {
            "provider": provider.name,
            "provider_type": args.provider,
            "base_url": args.base_url.rstrip("/"),
            "model": args.model,
            "temperature": args.temperature,
            "max_tokens": args.max_tokens,
            "reasoning": {"effort": args.reasoning_effort},
            "timeout": args.timeout,
            "workers": args.workers,
        }
        add_routing_settings(settings, args)
        write_json_new(
            args.output_root / "session_manifest.json",
            {
                "status": "RUNNING",
                "engineering_only": True,
                "purpose": "LOW-REASONING PREFLIGHT — NEVER SCIENTIFIC DATA",
                "scientific_candidates_sent": 0,
                "scientific_candidate_sources_loaded": 0,
                "selective_retries": False,
                "settings": settings,
                "session_order": ["G", "P"],
                "call_plan": [
                    {
                        "order": index,
                        "run_id": item["run_id"],
                        "program_id": item["program"].program_id,
                        "pattern_label": item["program"].pattern_label,
                        "loc": item["program"].loc,
                        "source_line_count": item["program"].source_line_count,
                        "session": item["session"],
                        "condition": item["arm"],
                        "repetition": item["repetition"],
                    }
                    for index, item in enumerate(plan, 1)
                ],
                "asset_hashes": {
                    str(path.relative_to(ROOT)): file_sha256(path) for path in asset_paths()
                },
            },
        )
        for session in ("G", "P"):
            session_plan = [item for item in plan if item["session"] == session]
            session_metrics: list[dict] = []
            with ThreadPoolExecutor(
                max_workers=WORKERS,
                thread_name_prefix=f"reasoning-preflight-{session}",
            ) as executor:
                for offset in range(0, len(session_plan), WORKERS):
                    batch = session_plan[offset : offset + WORKERS]
                    futures = [
                        executor.submit(
                            run_one,
                            provider=provider,
                            program=item["program"],
                            condition=item["arm"],
                            repetition=item["repetition"],
                            experiment_name=f"reasoning_preflight_{session}",
                            session_id=args.output_root.name,
                            system_prompt=system,
                            user_prompt=item["user_prompt"],
                            shared_prompt_hash=item["shared_prompt_hash"],
                            prior_hash=item["prior_hash"],
                            manifest_hash=file_sha256(STRESS_MANIFEST),
                            model=args.model,
                            temperature=args.temperature,
                            max_tokens=args.max_tokens,
                            reasoning_effort=args.reasoning_effort,
                            raw_session_dir=args.output_root / "raw" / session,
                            processed_session_dir=args.output_root / "processed" / session,
                            run_id=item["run_id"],
                        )
                        for item in batch
                    ]
                    records = [future.result() for future in futures]
                    for item, record in zip(batch, records, strict=True):
                        raw = (
                            json.loads((ROOT / record.raw_response_path).read_text())
                            if record.raw_response_path
                            else {}
                        )
                        metric = call_metric(record, raw, len(metrics) + 1)
                        metrics.append(metric)
                        session_metrics.append(metric)
                        append_experiment_log(args.experiment_log, record)
                        write_json_new(
                            args.output_root / "ordered" / f"call-{len(metrics):02d}.json",
                            metric,
                        )
                        validate_record(record, raw, settings)
            if len(session_metrics) != 10 or any(item["status"] != "ok" for item in session_metrics):
                raise SafetyViolation(f"Session {session} preflight incomplete or invalid")
            write_json_new(
                args.output_root / f"SESSION_{session}_PASS.json",
                {
                    "status": "PASS",
                    "session": session,
                    "calls": 10,
                    "run_ids_in_registered_order": [
                        item["run_id"] for item in session_metrics
                    ],
                },
            )

        summary = aggregate(metrics, time.perf_counter() - started)
        failure_keys = (
            "failures",
            "parser_failures",
            "content_null_failures",
            "length_truncations",
            "provider_model_mismatches",
            "rate_limit_failures",
        )
        if summary["calls_valid"] != EXPECTED_CALLS or any(summary[key] for key in failure_keys):
            raise SafetyViolation("low-reasoning preflight failure threshold exceeded")
        if summary["projected_600_call_cost_usd"] > COST_GATE_USD:
            raise SafetyViolation("projected 600-call cost exceeds US$4.50")
        result = {
            "status": "PASS",
            "engineering_only": True,
            "purpose": "LOW-REASONING PREFLIGHT — NEVER SCIENTIFIC DATA",
            "scientific_candidates_sent": 0,
            "scientific_candidate_sources_loaded": 0,
            "settings": settings,
            "session_order": ["G", "P"],
            "cost_gate_usd": COST_GATE_USD,
            "aggregate": summary,
            "metrics": metrics,
            "asset_hashes": {
                str(path.relative_to(ROOT)): file_sha256(path) for path in asset_paths()
            },
        }
        write_json_new(args.output_root / "PASS.json", result)
        return result
    except Exception as exc:
        summary = aggregate(metrics, time.perf_counter() - started)
        write_json_new(
            args.output_root / "BLOCKED.json",
            {
                "status": "BLOCK",
                "engineering_only": True,
                "scientific_candidates_sent": 0,
                "scientific_candidate_sources_loaded": 0,
                "reason": f"{type(exc).__name__}: {exc}",
                "aggregate": summary,
                "metrics": metrics,
            },
        )
        raise


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--provider", choices=["openai_compatible"], required=True)
    result.add_argument("--provider-label", required=True)
    add_routing_arguments(result)
    result.add_argument("--base-url", required=True)
    result.add_argument("--model", required=True)
    result.add_argument("--model-kind", choices=["pinned", "alias_only"], required=True)
    result.add_argument("--model-reference", required=True)
    result.add_argument("--accepted-alias-risk", default="")
    result.add_argument("--temperature", type=float, required=True)
    result.add_argument("--max-tokens", type=int, required=True)
    result.add_argument("--reasoning-effort", choices=["low"], required=True)
    result.add_argument("--timeout", type=float, required=True)
    result.add_argument("--workers", type=int, required=True)
    result.add_argument("--output-root", type=Path, required=True)
    result.add_argument(
        "--experiment-log",
        type=Path,
        default=ROOT / "EXPERIMENT_LOG.md",
    )
    return result


def main() -> None:
    try:
        result = run(parser().parse_args())
        print(json.dumps(result["aggregate"], indent=2))
    except Exception as exc:
        print(f"reasoning preflight blocked: {type(exc).__name__}: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
