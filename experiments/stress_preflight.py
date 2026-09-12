"""Twenty-call non-candidate stress smoke for the 16,384-token amendment."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from urllib.parse import urlsplit

from experiments.model_preflight import check_smoke_record, validate_identity_choice
from experiments.models import load_manifest
from experiments.prompts import build_prompt_pair
from experiments.providers.routing import add_routing_arguments, add_routing_settings
from experiments.run_pilot import append_experiment_log, load_prior_map, make_provider, run_one, utc_now
from experiments.safety import SafetyViolation
from experiments.storage import file_sha256, write_json_new

ROOT = Path(__file__).resolve().parents[1]
STRESS_MANIFEST = ROOT / "data/smoke-stress/manifest.json"
SCIENTIFIC_MANIFEST = ROOT / "data/manifests/pilot_manifest_v2_1.json"
SYSTEM = ROOT / "pilot/v2/prompts/system_v2.txt"
TEMPLATE = ROOT / "pilot/prompts/control.txt"
GENERIC_PRIORS = ROOT / "pilot/v2/generic_placebo_prior.json"
PATTERN_PRIORS = ROOT / "pilot/pattern_priors.json"
EXPECTED_CALLS = 20
MAX_PROJECTED_COST = 4.50


def stress_asset_paths():
    manifest = load_manifest(STRESS_MANIFEST)
    return [
        STRESS_MANIFEST,
        SYSTEM,
        TEMPLATE,
        GENERIC_PRIORS,
        PATTERN_PRIORS,
        *(path for program in manifest.included for path in (
            program.buggy_source_path,
            program.fixed_source_path,
            program.tests_path,
        )),
    ]


def call_plan(program, system, template):
    generic = load_prior_map(GENERIC_PRIORS)[program.pattern_label]
    pattern = load_prior_map(PATTERN_PRIORS)[program.pattern_label]
    pair_g = build_prompt_pair(system, template, program, generic)
    pair_p = build_prompt_pair(system, template, program, pattern)
    plan = []
    for repetition in range(1, 6):
        plan.extend([
            ("G", "A_G", repetition, pair_g.control_user_prompt, pair_g.shared_prompt_hash, None),
            ("G", "B", repetition, pair_g.treatment_user_prompt, pair_g.shared_prompt_hash, pair_g.prior_hash),
        ])
    for repetition in range(1, 6):
        plan.extend([
            ("P", "A_P", repetition, pair_p.control_user_prompt, pair_p.shared_prompt_hash, None),
            ("P", "C", repetition, pair_p.treatment_user_prompt, pair_p.shared_prompt_hash, pair_p.prior_hash),
        ])
    return plan


def _number(value):
    return value if isinstance(value, (int, float)) and not isinstance(value, bool) else None


def call_metric(record, raw):
    usage = raw.get("token_usage", {})
    details = usage.get("completion_tokens_details", {})
    return {
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


def aggregate(metrics):
    def average(field):
        values = [item[field] for item in metrics if item[field] is not None]
        return sum(values) / len(values) if len(values) == len(metrics) and values else None

    average_cost = average("cost_usd")
    return {
        "calls_attempted": len(metrics),
        "calls_successful": sum(item["parser_status"] == "ok" for item in metrics),
        "parser_failures": sum(item["parser_status"] == "parser_failure" for item in metrics),
        "content_null_failures": sum(item["content_is_null"] for item in metrics),
        "transport_failures": sum(item["transport_failure"] for item in metrics),
        "length_truncations": sum(item["finish_reason"] == "length" for item in metrics),
        "average_input_tokens": average("input_tokens"),
        "average_output_tokens": average("output_tokens"),
        "average_reasoning_tokens": average("reasoning_tokens"),
        "maximum_output_tokens": max((item["output_tokens"] for item in metrics if item["output_tokens"] is not None), default=None),
        "average_cost_per_call_usd": average_cost,
        "projected_600_call_cost_usd": average_cost * 600 if average_cost is not None else None,
    }


def validate_fixture(manifest):
    if STRESS_MANIFEST.resolve() == SCIENTIFIC_MANIFEST.resolve():
        raise SafetyViolation("stress and scientific manifests must differ")
    if manifest.dataset_name != "STRESS SMOKE DATA — NEVER SCIENTIFIC DATA":
        raise SafetyViolation("stress manifest lacks the permanent non-scientific marker")
    if len(manifest.included) != 1:
        raise SafetyViolation("stress smoke requires exactly one synthetic program")
    program = manifest.included[0]
    if not program.program_id.startswith("synthetic-stress-") or program.difficulty != "synthetic-stress-only":
        raise SafetyViolation("stress fixture is not explicitly synthetic")
    if not 150 <= program.source_line_count <= 160:
        raise SafetyViolation("stress fixture must have 150-160 physical lines")
    if len(program.faulty_lines) != 1:
        raise SafetyViolation("stress fixture must contain one planted faulty line")
    return program


def validate_args(args):
    validate_identity_choice(args.model, args.model_kind, args.model_reference, args.accepted_alias_risk)
    if args.provider_label != "openrouter":
        raise SafetyViolation("stress smoke requires frozen provider label openrouter")
    if args.base_url.rstrip("/") != "https://openrouter.ai/api/v1":
        raise SafetyViolation("stress smoke requires the frozen OpenRouter API base")
    if args.model != "z-ai/glm-5.3-flash":
        raise SafetyViolation("stress smoke requires the exact frozen model")
    if args.temperature != 0 or args.max_tokens != 16384 or args.timeout != 120:
        raise SafetyViolation("stress smoke requires temperature=0, max_tokens=16384, timeout=120")
    if args.openrouter_provider != "z-ai/fp8" or args.openrouter_provider_name != "Z.AI":
        raise SafetyViolation("stress smoke requires the frozen Z.AI endpoint pin")
    url = urlsplit(args.base_url)
    if url.scheme != "https" or url.netloc != "openrouter.ai":
        raise SafetyViolation("invalid frozen OpenRouter URL")


def run(args):
    validate_args(args)
    if args.output_root.exists():
        raise SafetyViolation("stress output root already exists; never overwrite evidence")
    manifest = load_manifest(STRESS_MANIFEST)
    program = validate_fixture(manifest)
    provider = make_provider(args)
    system, template = SYSTEM.read_text(), TEMPLATE.read_text()
    plan = call_plan(program, system, template)
    if len(plan) != EXPECTED_CALLS:
        raise SafetyViolation("registered stress plan must contain exactly 20 calls")
    args.output_root.mkdir(parents=True, exist_ok=False)
    raw_dir = args.output_root / "raw"
    processed_dir = args.output_root / "processed"
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
    session_id = args.output_root.name
    manifest_hash = file_sha256(STRESS_MANIFEST)
    write_json_new(args.output_root / "session_manifest.json", {
        "status": "RUNNING",
        "engineering_only": True,
        "purpose": "STRESS SMOKE DATA — NEVER SCIENTIFIC DATA",
        "scientific_candidates_sent": 0,
        "settings": settings,
        "call_plan": [{"session": x[0], "arm": x[1], "repetition": x[2]} for x in plan],
        "asset_hashes": {str(path.relative_to(ROOT)): file_sha256(path) for path in stress_asset_paths()},
    })
    metrics = []
    try:
        for session, arm, repetition, prompt, shared_hash, prior_hash in plan:
            record = run_one(
                provider=provider,
                program=program,
                condition=arm,
                repetition=repetition,
                experiment_name=f"stress_smoke_{session}",
                session_id=session_id,
                system_prompt=system,
                user_prompt=prompt,
                shared_prompt_hash=shared_hash,
                prior_hash=prior_hash,
                manifest_hash=manifest_hash,
                model=args.model,
                temperature=args.temperature,
                max_tokens=args.max_tokens,
                raw_session_dir=raw_dir,
                processed_session_dir=processed_dir,
            )
            append_experiment_log(args.experiment_log, record)
            raw = json.loads((ROOT / record.raw_response_path).read_text()) if record.raw_response_path else {}
            metric = call_metric(record, raw)
            metrics.append(metric)
            write_json_new(args.output_root / f"progress-{len(metrics):02d}.json", metric)
            check_smoke_record(record, raw)
            if raw.get("actual_model") != args.model:
                raise SafetyViolation("exact model identity mismatch")
            metadata = raw.get("response_metadata", {})
            if metadata.get("actual_underlying_provider") != "Z.AI":
                raise SafetyViolation("pinned underlying provider identity mismatch")
            if metadata.get("provider_preferences") != settings["openrouter_routing"]["provider_preferences"]:
                raise SafetyViolation("provider pin or fallback policy mismatch")
            if metric["finish_reason"] != "stop":
                raise SafetyViolation("stress completion did not finish with stop")
            if metric["input_tokens"] is None or metric["output_tokens"] is None or metric["cost_usd"] is None:
                raise SafetyViolation("provider did not expose required usage/cost evidence")
    except Exception as exc:
        summary = aggregate(metrics)
        write_json_new(args.output_root / "BLOCKED.json", {
            "status": "BLOCK",
            "engineering_only": True,
            "scientific_candidates_sent": 0,
            "reason": f"{type(exc).__name__}: {exc}",
            "metrics": metrics,
            "aggregate": summary,
        })
        raise
    summary = aggregate(metrics)
    if summary["calls_successful"] != EXPECTED_CALLS:
        raise SafetyViolation("fewer than 20 stress calls succeeded")
    if summary["parser_failures"] or summary["content_null_failures"] or summary["length_truncations"]:
        raise SafetyViolation("stress failure threshold exceeded")
    if summary["projected_600_call_cost_usd"] is None:
        raise SafetyViolation("scientific cost cannot be projected")
    status = "PASS" if summary["projected_600_call_cost_usd"] <= MAX_PROJECTED_COST else "BLOCK"
    result = {
        "status": status,
        "engineering_only": True,
        "purpose": "STRESS SMOKE DATA — NEVER SCIENTIFIC DATA",
        "scientific_candidates_sent": 0,
        "settings": settings,
        "metrics": metrics,
        "aggregate": summary,
        "cost_gate_usd": MAX_PROJECTED_COST,
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
