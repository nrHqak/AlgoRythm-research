from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

from experiments.models import ParsedRunRecord, ProgramManifest
from experiments.prompts import PRIOR_CLOSE, PRIOR_OPEN, sha256_text


class SafetyViolation(ValueError):
    pass


def validate_manifest_for_run(
    manifest: ProgramManifest,
    *,
    target_n: int,
    run_started_at: datetime,
    expected_dataset_name: str | None = None,
) -> None:
    if manifest.selection_frozen_at > run_started_at:
        raise SafetyViolation("dataset selection must be frozen before experiment execution")
    if len(manifest.included) != target_n:
        raise SafetyViolation(
            f"included sample count {len(manifest.included)} does not equal target_n {target_n}"
        )
    if expected_dataset_name is not None and manifest.dataset_name != expected_dataset_name:
        raise SafetyViolation(
            f"manifest dataset {manifest.dataset_name!r} does not match configured target "
            f"{expected_dataset_name!r}"
        )


def assert_condition_balance(
    records: Iterable[ParsedRunRecord],
    *,
    repetitions: int,
    control_name: str,
    treatment_name: str,
    expected_program_ids: set[str] | None = None,
) -> None:
    grouped: dict[str, Counter[tuple[str, int]]] = defaultdict(Counter)
    for record in records:
        grouped[record.program_id][(record.condition, record.repetition)] += 1
    expected = {
        (condition, repetition)
        for condition in (control_name, treatment_name)
        for repetition in range(1, repetitions + 1)
    }
    failures: list[str] = []
    if expected_program_ids is not None:
        absent = sorted(expected_program_ids - set(grouped))
        unexpected = sorted(set(grouped) - expected_program_ids)
        if absent or unexpected:
            failures.append(f"program-set mismatch: absent={absent}, unexpected={unexpected}")
    for program_id, counts in grouped.items():
        actual = set(counts)
        missing = sorted(expected - actual)
        duplicates = sorted(key for key, count in counts.items() if count != 1)
        extras = sorted(actual - expected)
        if missing or duplicates or extras:
            failures.append(
                f"{program_id}: missing={missing}, duplicate={duplicates}, extra={extras}"
            )
    if failures:
        raise SafetyViolation("control/treatment sample mismatch: " + "; ".join(failures))


def assert_paired_settings(
    records: Iterable[ParsedRunRecord], control_name: str, treatment_name: str
) -> None:
    pairs: dict[tuple[str, int], dict[str, ParsedRunRecord]] = defaultdict(dict)
    for record in records:
        pairs[(record.program_id, record.repetition)][record.condition] = record
    failures: list[str] = []
    for key, conditions in pairs.items():
        if control_name not in conditions or treatment_name not in conditions:
            continue
        control = conditions[control_name]
        treatment = conditions[treatment_name]
        comparisons = {
            "provider": (control.provider, treatment.provider),
            "model": (control.model, treatment.model),
            "temperature": (control.temperature, treatment.temperature),
            "max_tokens": (control.max_tokens, treatment.max_tokens),
            "system_prompt_hash": (control.system_prompt_hash, treatment.system_prompt_hash),
            "shared_prompt_hash": (control.shared_prompt_hash, treatment.shared_prompt_hash),
            "manifest_hash": (control.manifest_hash, treatment.manifest_hash),
        }
        unequal = {name: value for name, value in comparisons.items() if value[0] != value[1]}
        if unequal:
            failures.append(f"{key}: {unequal}")
    if failures:
        raise SafetyViolation("paired model/prompt setting mismatch: " + "; ".join(failures))


def assert_unique_execution_keys(records: Iterable[ParsedRunRecord]) -> None:
    keys = [record.execution_key for record in records]
    duplicates = sorted({key for key in keys if keys.count(key) > 1})
    if duplicates:
        raise SafetyViolation(f"accidental duplicate runs detected: {duplicates}")


def assert_raw_files_exist(records: Iterable[ParsedRunRecord], repository_root: Path) -> None:
    missing: list[str] = []
    for record in records:
        if record.status == "provider_failure":
            continue
        if not record.raw_response_path:
            missing.append(record.run_id)
            continue
        path = Path(record.raw_response_path)
        if not path.is_absolute():
            path = repository_root / path
        if not path.is_file():
            missing.append(record.run_id)
    if missing:
        raise SafetyViolation(f"raw responses are missing for runs: {missing}")


def assert_raw_prompt_symmetry(
    records: Iterable[ParsedRunRecord],
    repository_root: Path,
    control_name: str,
    treatment_name: str,
) -> None:
    import json

    pairs: dict[tuple[str, int], dict[str, dict[str, Any]]] = defaultdict(dict)
    for record in records:
        if not record.raw_response_path:
            continue
        path = Path(record.raw_response_path)
        if not path.is_absolute():
            path = repository_root / path
        payload = json.loads(path.read_text(encoding="utf-8"))
        if payload.get("prompt_input_fields") != [
            "program_id",
            "task_id",
            "problem_context",
            "numbered_buggy_source",
        ]:
            raise SafetyViolation(f"unverifiable prompt input provenance in {path}")
        pairs[(record.program_id, record.repetition)][record.condition] = payload

    failures: list[str] = []
    for key, conditions in pairs.items():
        if control_name not in conditions or treatment_name not in conditions:
            continue
        control = conditions[control_name]
        treatment = conditions[treatment_name]
        control_prompt = str(control["user_prompt"])
        treatment_prompt = str(treatment["user_prompt"])
        expected_prefix = control_prompt.rstrip() + f"\n\n{PRIOR_OPEN}\n"
        prior_text = (
            treatment_prompt[len(expected_prefix) : -len(f"\n{PRIOR_CLOSE}")]
            if treatment_prompt.startswith(expected_prefix)
            and treatment_prompt.endswith(f"\n{PRIOR_CLOSE}")
            else ""
        )
        if (
            PRIOR_OPEN in control_prompt
            or PRIOR_CLOSE in control_prompt
            or not treatment_prompt.startswith(expected_prefix)
            or not treatment_prompt.endswith(f"\n{PRIOR_CLOSE}")
            or control.get("system_prompt") != treatment.get("system_prompt")
            or sha256_text(str(control.get("system_prompt", "")))
            != conditions[control_name].get("system_prompt_hash")
            or sha256_text(control_prompt)
            != conditions[control_name].get("shared_prompt_hash")
            or sha256_text(control_prompt)
            != conditions[treatment_name].get("shared_prompt_hash")
            or sha256_text(prior_text) != conditions[treatment_name].get("prior_hash")
        ):
            failures.append(str(key))
    if failures:
        raise SafetyViolation(
            "prompt asymmetry other than the delimited prior was detected for pairs: "
            + ", ".join(failures)
        )


def safety_summary(records: Iterable[ParsedRunRecord]) -> dict[str, Any]:
    records = list(records)
    return {
        "run_count": len(records),
        "parser_failures": sum(record.status == "parser_failure" for record in records),
        "provider_failures": sum(record.status == "provider_failure" for record in records),
        "invalid_ranking_failures": sum(
            record.status == "parser_failure" and record.error_type == "ResponseParseError"
            for record in records
        ),
    }
