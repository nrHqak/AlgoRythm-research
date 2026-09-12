"""Twenty-call synthetic gate for the frozen four-worker v2.2 execution."""
from __future__ import annotations

import argparse
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from dotenv import load_dotenv

from experiments.model_preflight import check_smoke_record, validate_identity_choice
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
STRESS_MANIFEST = ROOT / "data/smoke-stress/manifest_32768.json"
SCIENTIFIC_MANIFEST = ROOT / "data/manifests/pilot_manifest_v2_2.json"
SYSTEM = ROOT / "pilot/v2/prompts/system_v2.txt"
TEMPLATE = ROOT / "pilot/prompts/control.txt"
GENERIC_PRIORS = ROOT / "pilot/v2/generic_placebo_prior.json"
PATTERN_PRIORS = ROOT / "pilot/pattern_priors.json"
EXPECTED_CALLS = 20
WORKERS = 4


def asset_paths() -> list[Path]:
    manifest = load_manifest(STRESS_MANIFEST)
    paths = [STRESS_MANIFEST, SCIENTIFIC_MANIFEST, SYSTEM, TEMPLATE, GENERIC_PRIORS, PATTERN_PRIORS]
    for program in manifest.included[:2]:
        paths.extend([program.buggy_source_path, program.fixed_source_path, program.tests_path])
    return list(dict.fromkeys(paths))


def validate_args(args: argparse.Namespace) -> None:
    validate_identity_choice(args.model, args.model_kind, args.model_reference, args.accepted_alias_risk)
    if args.provider_label != "openrouter" or args.base_url.rstrip("/") != "https://openrouter.ai/api/v1":
        raise SafetyViolation("concurrency preflight requires frozen OpenRouter routing")
    if args.model != "z-ai/glm-5.3-flash":
        raise SafetyViolation("concurrency preflight requires the exact frozen model")
    if args.temperature != 0 or args.max_tokens != 32768 or args.timeout != 120:
        raise SafetyViolation("temperature, max_tokens, or timeout differs from the freeze")
    if args.workers != WORKERS:
        raise SafetyViolation("concurrency preflight requires exactly four workers")
    if args.openrouter_provider != "z-ai/fp8" or args.openrouter_provider_name != "Z.AI":
        raise SafetyViolation("concurrency preflight requires the frozen Z.AI endpoint pin")


def build_plan() -> list[dict]:
    stress = load_manifest(STRESS_MANIFEST)
    science = load_manifest(SCIENTIFIC_MANIFEST)
    if len(stress.included) < 2:
        raise SafetyViolation("concurrency preflight requires two registered large synthetic fixtures")
    science_ids = {program.program_id for program in science.included}
    fixtures = stress.included[:2]
    if any(program.program_id in science_ids for program in fixtures):
        raise SafetyViolation("synthetic/scientific program-ID overlap")
    if any(not program.program_id.startswith("synthetic-stress-") for program in fixtures):
        raise SafetyViolation("concurrency preflight input is not explicitly synthetic")

    system = SYSTEM.read_text(encoding="utf-8")
    template = TEMPLATE.read_text(encoding="utf-8")
    plan: list[dict] = []
    for session, program, prior_path, arms in (
        ("G", fixtures[0], GENERIC_PRIORS, ("A_G", "B")),
        ("P", fixtures[1], PATTERN_PRIORS, ("A_P", "C")),
    ):
        priors = load_prior_map(prior_path)
        pair = build_prompt_pair(system, template, program, priors[program.pattern_label])
        for repetition in range(1, 6):
            for arm in arms:
                treatment = arm in {"B", "C"}
                plan.append({
                    "session": session,
                    "program": program,
                    "arm": arm,
                    "repetition": repetition,
                    "user_prompt": pair.treatment_user_prompt if treatment else pair.control_user_prompt,
                    "shared_prompt_hash": pair.shared_prompt_hash,
                    "prior_hash": pair.prior_hash if treatment else None,
                    "run_id": deterministic_run_id_for(
                        program_id=program.program_id,
                        condition=arm,
                        repetition=repetition,
                    ),
                })
    if len(plan) != EXPECTED_CALLS or [item["session"] for item in plan] != ["G"] * 10 + ["P"] * 10:
        raise SafetyViolation("preflight plan must be exactly ten G calls then ten P calls")
    if len({item["run_id"] for item in plan}) != EXPECTED_CALLS:
        raise SafetyViolation("deterministic run-ID collision")
    return plan


def metric(record, raw: dict, order: int) -> dict:
    usage = raw.get("token_usage", {})
    completion = usage.get("completion_tokens_details", {})
    return {
        "order": order,
        "run_id": record.run_id,
        "program_id": record.program_id,
        "session": record.experiment_name.rsplit("_", 1)[-1],
        "condition": record.condition,
        "repetition": record.repetition,
        "status": record.status,
        "error_type": record.error_type,
        "error_message": record.error_message,
        "input_tokens": usage.get("prompt_tokens"),
        "output_tokens": usage.get("completion_tokens"),
        "reasoning_tokens": completion.get("reasoning_tokens"),
        "finish_reason": raw.get("response_metadata", {}).get("finish_reason"),
        "latency_seconds": raw.get("latency"),
        "cost_usd": usage.get("cost"),
        "model": raw.get("actual_model"),
        "underlying_provider": raw.get("response_metadata", {}).get("actual_underlying_provider"),
        "content_is_null": raw.get("raw_response") is None if raw else record.raw_response is None,
    }


def validate_record(record, raw: dict, settings: dict) -> None:
    check_smoke_record(record, raw)
    metadata = raw.get("response_metadata", {})
    if raw.get("actual_model") != settings["model"]:
        raise SafetyViolation("exact model identity mismatch")
    if metadata.get("actual_underlying_provider") != "Z.AI":
        raise SafetyViolation("pinned underlying provider identity mismatch")
    if metadata.get("provider_preferences") != settings["openrouter_routing"]["provider_preferences"]:
        raise SafetyViolation("provider pin or fallback policy mismatch")
    output_tokens = raw.get("token_usage", {}).get("completion_tokens")
    if metadata.get("finish_reason") != "stop" or output_tokens == 32768:
        raise SafetyViolation("completion reached the token ceiling or did not finish with stop")
    if any(value is None for value in (
        raw.get("token_usage", {}).get("prompt_tokens"),
        output_tokens,
        raw.get("token_usage", {}).get("completion_tokens_details", {}).get("reasoning_tokens"),
        raw.get("latency"),
        raw.get("token_usage", {}).get("cost"),
    )):
        raise SafetyViolation("provider omitted required usage, latency, or cost evidence")


def aggregate(metrics: list[dict], wall_seconds: float) -> dict:
    valid = [item for item in metrics if item["status"] == "ok"]
    failures = [item for item in metrics if item["status"] != "ok"]
    rate_limits = [
        item for item in failures
        if "429" in str(item.get("error_message")) or "rate limit" in str(item.get("error_message")).lower()
    ]
    throughput = len(metrics) / wall_seconds if wall_seconds > 0 else None
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
        "wall_clock_seconds": wall_seconds,
        "observed_throughput_calls_per_second": throughput,
        "observed_throughput_calls_per_minute": throughput * 60 if throughput is not None else None,
        "projected_600_call_runtime_seconds": 600 / throughput if throughput else None,
        "projected_600_call_runtime_hours": 600 / throughput / 3600 if throughput else None,
        "actual_cost_usd": sum(item["cost_usd"] or 0 for item in metrics),
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
            "timeout": args.timeout,
            "workers": args.workers,
        }
        add_routing_settings(settings, args)
        write_json_new(args.output_root / "session_manifest.json", {
            "status": "RUNNING",
            "engineering_only": True,
            "purpose": "CONCURRENCY PREFLIGHT — NEVER SCIENTIFIC DATA",
            "scientific_candidates_sent": 0,
            "selective_retries": False,
            "settings": settings,
            "session_order": ["G", "P"],
            "call_plan": [{
                "order": index,
                "run_id": item["run_id"],
                "program_id": item["program"].program_id,
                "session": item["session"],
                "condition": item["arm"],
                "repetition": item["repetition"],
            } for index, item in enumerate(plan, 1)],
            "asset_hashes": {str(path.relative_to(ROOT)): file_sha256(path) for path in asset_paths()},
        })
        for session in ("G", "P"):
            session_plan = [item for item in plan if item["session"] == session]
            session_metrics: list[dict] = []
            with ThreadPoolExecutor(max_workers=WORKERS, thread_name_prefix=f"preflight-{session}") as executor:
                for offset in range(0, len(session_plan), WORKERS):
                    batch = session_plan[offset:offset + WORKERS]
                    futures = [executor.submit(
                        run_one,
                        provider=provider,
                        program=item["program"],
                        condition=item["arm"],
                        repetition=item["repetition"],
                        experiment_name=f"concurrency_preflight_{session}",
                        session_id=args.output_root.name,
                        system_prompt=system,
                        user_prompt=item["user_prompt"],
                        shared_prompt_hash=item["shared_prompt_hash"],
                        prior_hash=item["prior_hash"],
                        manifest_hash=file_sha256(STRESS_MANIFEST),
                        model=args.model,
                        temperature=args.temperature,
                        max_tokens=args.max_tokens,
                        raw_session_dir=args.output_root / "raw" / session,
                        processed_session_dir=args.output_root / "processed" / session,
                        run_id=item["run_id"],
                    ) for item in batch]
                    records = [future.result() for future in futures]
                    for item, record in zip(batch, records, strict=True):
                        raw = json.loads((ROOT / record.raw_response_path).read_text()) if record.raw_response_path else {}
                        call_metric = metric(record, raw, len(metrics) + 1)
                        metrics.append(call_metric)
                        session_metrics.append(call_metric)
                        append_experiment_log(args.experiment_log, record)
                        write_json_new(args.output_root / "ordered" / f"call-{len(metrics):02d}.json", call_metric)
                        validate_record(record, raw, settings)
            if len(session_metrics) != 10 or any(item["status"] != "ok" for item in session_metrics):
                raise SafetyViolation(f"Session {session} concurrency preflight incomplete or invalid")
            write_json_new(args.output_root / f"SESSION_{session}_PASS.json", {
                "status": "PASS", "session": session, "calls": 10,
                "run_ids_in_registered_order": [item["run_id"] for item in session_metrics],
            })
        summary = aggregate(metrics, time.perf_counter() - started)
        if summary["calls_valid"] != EXPECTED_CALLS or any(summary[key] for key in (
            "failures", "parser_failures", "content_null_failures", "length_truncations",
            "provider_model_mismatches", "rate_limit_failures",
        )):
            raise SafetyViolation("concurrency preflight failure threshold exceeded")
        result = {
            "status": "PASS",
            "engineering_only": True,
            "purpose": "CONCURRENCY PREFLIGHT — NEVER SCIENTIFIC DATA",
            "scientific_candidates_sent": 0,
            "settings": settings,
            "session_order": ["G", "P"],
            "aggregate": summary,
            "metrics": metrics,
            "asset_hashes": {str(path.relative_to(ROOT)): file_sha256(path) for path in asset_paths()},
        }
        write_json_new(args.output_root / "PASS.json", result)
        return result
    except Exception as exc:
        summary = aggregate(metrics, time.perf_counter() - started)
        write_json_new(args.output_root / "BLOCKED.json", {
            "status": "BLOCK",
            "engineering_only": True,
            "scientific_candidates_sent": 0,
            "reason": f"{type(exc).__name__}: {exc}",
            "aggregate": summary,
            "metrics": metrics,
        })
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
    result.add_argument("--timeout", type=float, required=True)
    result.add_argument("--workers", type=int, required=True)
    result.add_argument("--output-root", type=Path, required=True)
    result.add_argument("--experiment-log", type=Path, default=ROOT / "EXPERIMENT_LOG.md")
    return result


def main() -> None:
    try:
        result = run(parser().parse_args())
        print(json.dumps(result["aggregate"], indent=2))
    except Exception as exc:
        print(f"concurrency preflight blocked: {type(exc).__name__}: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
