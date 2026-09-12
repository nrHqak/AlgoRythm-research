"""Fifty-call non-candidate stress smoke for the 32,768-token amendment."""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

from experiments.model_preflight import check_smoke_record, validate_identity_choice
from experiments.models import load_manifest
from experiments.prompts import build_prompt_pair
from experiments.providers.routing import add_routing_arguments, add_routing_settings
from experiments.run_pilot import append_experiment_log, load_prior_map, make_provider, run_one
from experiments.safety import SafetyViolation
from experiments.storage import file_sha256, write_json_new

ROOT = Path(__file__).resolve().parents[1]
STRESS_MANIFEST = ROOT / "data/smoke-stress/manifest_32768.json"
SCIENTIFIC_MANIFEST = ROOT / "data/manifests/pilot_manifest_v2_1.json"
SYSTEM = ROOT / "pilot/v2/prompts/system_v2.txt"
TEMPLATE = ROOT / "pilot/prompts/control.txt"
GENERIC_PRIORS = ROOT / "pilot/v2/generic_placebo_prior.json"
PATTERN_PRIORS = ROOT / "pilot/pattern_priors.json"
EXPECTED_CALLS = 50
COST_GATE_USD = 4.50


def stress_asset_paths():
    manifest = load_manifest(STRESS_MANIFEST)
    paths = [STRESS_MANIFEST, SYSTEM, TEMPLATE, GENERIC_PRIORS, PATTERN_PRIORS]
    for program in manifest.included:
        paths.extend([program.buggy_source_path, program.fixed_source_path, program.tests_path])
    return list(dict.fromkeys(paths))


def call_plan(manifest, system, template):
    generic = load_prior_map(GENERIC_PRIORS)
    pattern = load_prior_map(PATTERN_PRIORS)
    plan = []
    for program in manifest.included:
        pair = build_prompt_pair(system, template, program, generic[program.pattern_label])
        for repetition in range(1, 6):
            plan.extend([
                (program, "G", "A_G", repetition, pair.control_user_prompt, pair.shared_prompt_hash, None),
                (program, "G", "B", repetition, pair.treatment_user_prompt, pair.shared_prompt_hash, pair.prior_hash),
            ])
    for program in manifest.included[:2]:
        pair = build_prompt_pair(system, template, program, pattern[program.pattern_label])
        for repetition in range(1, 6):
            plan.extend([
                (program, "P", "A_P", repetition, pair.control_user_prompt, pair.shared_prompt_hash, None),
                (program, "P", "C", repetition, pair.treatment_user_prompt, pair.shared_prompt_hash, pair.prior_hash),
            ])
    return plan


def _number(value):
    return value if isinstance(value, (int, float)) and not isinstance(value, bool) else None


def call_metric(record, raw):
    usage = raw.get("token_usage", {})
    details = usage.get("completion_tokens_details", {})
    return {
        "program_id": record.program_id,
        "session": record.experiment_name.rsplit("_", 1)[-1],
        "arm": record.condition,
        "repetition": record.repetition,
        "input_tokens": _number(usage.get("prompt_tokens")),
        "output_tokens": _number(usage.get("completion_tokens")),
        "reasoning_tokens": _number(details.get("reasoning_tokens")),
        "finish_reason": raw.get("response_metadata", {}).get("finish_reason"),
        "latency_seconds": _number(raw.get("latency")),
        "cost_usd": _number(usage.get("cost")),
        "model": raw.get("actual_model"),
        "provider": raw.get("response_metadata", {}).get("actual_underlying_provider"),
        "content_is_null": bool(record.raw_response_path) and raw.get("raw_response") is None,
        "transport_failure": record.status == "provider_failure" and not record.raw_response_path,
        "parser_status": record.status,
    }


def _mean(values):
    return sum(values) / len(values) if values else None


def _complete_values(metrics, field):
    values = [item[field] for item in metrics if item[field] is not None]
    return values if len(values) == len(metrics) else []


def aggregate(metrics):
    output = _complete_values(metrics, "output_tokens")
    reasoning = _complete_values(metrics, "reasoning_tokens")
    costs = _complete_values(metrics, "cost_usd")
    latencies = _complete_values(metrics, "latency_seconds")
    per_arm = {}
    for arm in ("A_G", "B", "A_P", "C"):
        rows = [item for item in metrics if item["arm"] == arm]
        per_arm[arm] = {
            "calls": len(rows),
            "average_cost_usd": _mean([item["cost_usd"] for item in rows if item["cost_usd"] is not None]),
            "average_latency_seconds": _mean([item["latency_seconds"] for item in rows if item["latency_seconds"] is not None]),
            "average_output_tokens": _mean([item["output_tokens"] for item in rows if item["output_tokens"] is not None]),
        }
    equal_arm_cost = sum(item["average_cost_usd"] for item in per_arm.values()) if all(item["average_cost_usd"] is not None for item in per_arm.values()) else None
    equal_arm_latency = sum(item["average_latency_seconds"] for item in per_arm.values()) if all(item["average_latency_seconds"] is not None for item in per_arm.values()) else None
    p95_output = sorted(output)[math.ceil(0.95 * len(output)) - 1] if output else None
    projected_seconds = 150 * equal_arm_latency if equal_arm_latency is not None else None
    return {
        "calls_attempted": len(metrics),
        "calls_successful": sum(item["parser_status"] == "ok" for item in metrics),
        "parser_failures": sum(item["parser_status"] == "parser_failure" for item in metrics),
        "content_null_failures": sum(item["content_is_null"] for item in metrics),
        "transport_failures": sum(item["transport_failure"] for item in metrics),
        "length_truncations": sum(item["finish_reason"] == "length" for item in metrics),
        "average_input_tokens": _mean(_complete_values(metrics, "input_tokens")),
        "average_output_tokens": _mean(output),
        "p95_output_tokens_nearest_rank": p95_output,
        "maximum_output_tokens": max(output) if output else None,
        "average_reasoning_tokens": _mean(reasoning),
        "maximum_reasoning_tokens": max(reasoning) if reasoning else None,
        "average_cost_per_call_usd": _mean(costs),
        "average_latency_seconds": _mean(latencies),
        "per_arm": per_arm,
        "projected_600_call_cost_usd_equal_arm_weighted": 150 * equal_arm_cost if equal_arm_cost is not None else None,
        "projected_600_call_runtime_seconds_equal_arm_weighted": projected_seconds,
        "projected_600_call_runtime_hours_equal_arm_weighted": projected_seconds / 3600 if projected_seconds is not None else None,
    }


def validate_fixture_manifest(manifest):
    if STRESS_MANIFEST.resolve() == SCIENTIFIC_MANIFEST.resolve():
        raise SafetyViolation("stress and scientific manifests must differ")
    if manifest.dataset_name != "32768 STRESS SMOKE DATA — NEVER SCIENTIFIC DATA":
        raise SafetyViolation("stress manifest lacks its permanent non-scientific marker")
    if len(manifest.included) != 3:
        raise SafetyViolation("registered 50-call stress manifest requires three records")
    for program in manifest.included:
        if not program.program_id.startswith("synthetic-stress-") or program.difficulty != "synthetic-stress-only":
            raise SafetyViolation("stress input is not explicitly synthetic")
        if not 140 <= program.source_line_count <= 160:
            raise SafetyViolation("stress input must be representative of the largest 140-160-line programs")
        if len(program.faulty_lines) != 1:
            raise SafetyViolation("each synthetic stress input must contain one planted fault")


def validate_args(args):
    validate_identity_choice(args.model, args.model_kind, args.model_reference, args.accepted_alias_risk)
    if args.provider_label != "openrouter" or args.base_url.rstrip("/") != "https://openrouter.ai/api/v1":
        raise SafetyViolation("stress smoke requires the frozen OpenRouter provider and API base")
    if args.model != "z-ai/glm-5.3-flash":
        raise SafetyViolation("stress smoke requires the exact frozen model")
    if args.temperature != 0 or args.max_tokens != 32768 or args.timeout != 120:
        raise SafetyViolation("stress smoke requires temperature=0, max_tokens=32768, timeout=120")
    if args.openrouter_provider != "z-ai/fp8" or args.openrouter_provider_name != "Z.AI":
        raise SafetyViolation("stress smoke requires the frozen Z.AI endpoint pin")


def run(args):
    validate_args(args)
    if args.output_root.exists():
        raise SafetyViolation("stress output root already exists; never overwrite evidence")
    manifest = load_manifest(STRESS_MANIFEST)
    validate_fixture_manifest(manifest)
    provider = make_provider(args)
    system, template = SYSTEM.read_text(), TEMPLATE.read_text()
    plan = call_plan(manifest, system, template)
    if len(plan) != EXPECTED_CALLS or [item[1] for item in plan] != ["G"] * 30 + ["P"] * 20:
        raise SafetyViolation("registered stress plan must be exactly 30 G calls then 20 P calls")
    args.output_root.mkdir(parents=True, exist_ok=False)
    settings = {
        "provider": provider.name,
        "provider_type": args.provider,
        "base_url": args.base_url.rstrip("/"),
        "model": args.model,
        "temperature": args.temperature,
        "max_tokens": args.max_tokens,
        "timeout": args.timeout,
    }
    add_routing_settings(settings, args)
    manifest_hash = file_sha256(STRESS_MANIFEST)
    write_json_new(args.output_root / "session_manifest.json", {
        "status": "RUNNING",
        "engineering_only": True,
        "purpose": "32768 STRESS SMOKE DATA — NEVER SCIENTIFIC DATA",
        "scientific_candidates_sent": 0,
        "reasoning_effort_parameter_sent": False,
        "settings": settings,
        "p95_definition": "nearest-rank: sorted output token count at ceil(0.95*n)",
        "runtime_projection": "equal-arm weighted mean observed latency multiplied by 150 calls per arm",
        "cost_projection": "equal-arm weighted mean observed cost multiplied by 150 calls per arm",
        "call_plan": [{"program_id": x[0].program_id, "session": x[1], "arm": x[2], "repetition": x[3]} for x in plan],
        "asset_hashes": {str(path.relative_to(ROOT)): file_sha256(path) for path in stress_asset_paths()},
    })
    metrics = []
    try:
        for program, session, arm, repetition, prompt, shared_hash, prior_hash in plan:
            record = run_one(
                provider=provider,
                program=program,
                condition=arm,
                repetition=repetition,
                experiment_name=f"stress_smoke_32768_{session}",
                session_id=args.output_root.name,
                system_prompt=system,
                user_prompt=prompt,
                shared_prompt_hash=shared_hash,
                prior_hash=prior_hash,
                manifest_hash=manifest_hash,
                model=args.model,
                temperature=args.temperature,
                max_tokens=args.max_tokens,
                raw_session_dir=args.output_root / "raw",
                processed_session_dir=args.output_root / "processed",
            )
            append_experiment_log(args.experiment_log, record)
            raw = json.loads((ROOT / record.raw_response_path).read_text()) if record.raw_response_path else {}
            metric = call_metric(record, raw)
            metrics.append(metric)
            write_json_new(args.output_root / f"progress-{len(metrics):02d}.json", metric)
            check_smoke_record(record, raw)
            metadata = raw.get("response_metadata", {})
            if raw.get("actual_model") != args.model:
                raise SafetyViolation("exact model identity mismatch")
            if metadata.get("actual_underlying_provider") != "Z.AI":
                raise SafetyViolation("pinned underlying provider identity mismatch")
            if metadata.get("provider_preferences") != settings["openrouter_routing"]["provider_preferences"]:
                raise SafetyViolation("provider pin or fallback policy mismatch")
            if metric["finish_reason"] != "stop" or metric["output_tokens"] == 32768:
                raise SafetyViolation("stress completion reached its output limit or did not finish with stop")
            required = (metric["input_tokens"], metric["output_tokens"], metric["reasoning_tokens"], metric["latency_seconds"], metric["cost_usd"])
            if any(value is None for value in required):
                raise SafetyViolation("provider did not expose all required usage, latency, and cost evidence")
    except Exception as exc:
        write_json_new(args.output_root / "BLOCKED.json", {
            "status": "BLOCK",
            "engineering_only": True,
            "scientific_candidates_sent": 0,
            "reason": f"{type(exc).__name__}: {exc}",
            "metrics": metrics,
            "aggregate": aggregate(metrics),
        })
        raise
    summary = aggregate(metrics)
    if summary["calls_successful"] != EXPECTED_CALLS:
        raise SafetyViolation("fewer than 50 stress calls succeeded")
    if summary["parser_failures"] or summary["content_null_failures"] or summary["length_truncations"] or summary["transport_failures"]:
        raise SafetyViolation("stress failure threshold exceeded")
    projection = summary["projected_600_call_cost_usd_equal_arm_weighted"]
    status = "PASS" if projection is not None and projection <= COST_GATE_USD else "BLOCK"
    result = {
        "status": status,
        "engineering_only": True,
        "purpose": "32768 STRESS SMOKE DATA — NEVER SCIENTIFIC DATA",
        "scientific_candidates_sent": 0,
        "reasoning_effort_parameter_sent": False,
        "settings": settings,
        "metrics": metrics,
        "aggregate": summary,
        "cost_gate_usd": COST_GATE_USD,
        "session_order": ["G", "P"],
        "calls_expected": EXPECTED_CALLS,
        "asset_hashes": {str(path.relative_to(ROOT)): file_sha256(path) for path in stress_asset_paths()},
    }
    write_json_new(args.output_root / ("PASS.json" if status == "PASS" else "BLOCKED.json"), result)
    if status != "PASS":
        raise SafetyViolation("projected 600-call cost exceeds US$4.50")
    return result


def parser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--provider", choices=["openai_compatible"], required=True)
    parser.add_argument("--provider-label", required=True)
    add_routing_arguments(parser)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--model-kind", choices=["pinned", "alias_only"], required=True)
    parser.add_argument("--model-reference", required=True)
    parser.add_argument("--accepted-alias-risk", default="")
    parser.add_argument("--temperature", type=float, required=True)
    parser.add_argument("--max-tokens", type=int, required=True)
    parser.add_argument("--timeout", type=float, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--experiment-log", type=Path, default=ROOT / "EXPERIMENT_LOG.md")
    return parser


def main():
    try:
        result = run(parser().parse_args())
        print(json.dumps(result["aggregate"], indent=2))
    except Exception as exc:
        print(f"stress smoke blocked: {type(exc).__name__}: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
