from __future__ import annotations

import argparse
import json
import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

import yaml
from dotenv import load_dotenv

from experiments.models import ParsedRunRecord, ProgramRecord, load_manifest
from experiments.parsing import ResponseParseError, parse_ranking
from experiments.prompts import build_prompt_pair, sha256_text
from experiments.providers import (
    CompletionRequest,
    LLMProvider,
    MockProvider,
    OpenAICompatibleProvider,
)
from experiments.safety import SafetyViolation, validate_manifest_for_run
from experiments.storage import (
    canonical_hash,
    existing_execution_keys,
    file_sha256,
    path_sha256,
    write_json_new,
)


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def load_yaml_object(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"expected an object in {path}")
    return payload


def load_prior_map(path: Path) -> dict[str, str]:
    payload = load_yaml_object(path)
    priors = payload.get("priors", payload)
    if not isinstance(priors, dict):
        raise ValueError("prior file must map pattern labels to frozen prior text")
    result = {str(label): str(text).strip() for label, text in priors.items()}
    empty = sorted(label for label, text in result.items() if not text)
    if empty:
        raise ValueError(f"empty frozen priors: {empty}")
    return result


def make_provider(args: argparse.Namespace) -> LLMProvider:
    if args.provider == "mock":
        if not args.allow_mock:
            raise SafetyViolation("mock provider requires --allow-mock and is never scientific evidence")
        return MockProvider()
    if args.provider == "openai_compatible":
        parsed_url = urlsplit(args.base_url)
        if parsed_url.scheme not in {"http", "https"} or not parsed_url.netloc:
            raise SafetyViolation("base URL must be an absolute HTTP(S) URL")
        if parsed_url.username or parsed_url.password or parsed_url.query or parsed_url.fragment:
            raise SafetyViolation(
                "base URL must not contain credentials, query parameters, or fragments"
            )
        return OpenAICompatibleProvider(
            base_url=args.base_url,
            api_key=os.environ.get("LLM_API_KEY", ""),
            provider_name=args.provider_label or args.provider,
            timeout_seconds=args.timeout,
        )
    raise ValueError(f"unsupported provider: {args.provider}")


def relative_to_root(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(REPOSITORY_ROOT))
    except ValueError:
        return str(path.resolve())


def shell_command(args: argparse.Namespace, session_id: str) -> str:
    import shlex

    parts = [
        ".venv/bin/python",
        "-m",
        "experiments.run_pilot",
        "--config",
        str(args.config),
        "--manifest",
        str(args.manifest),
        "--system-prompt",
        str(args.system_prompt),
        "--user-template",
        str(args.user_template),
        "--priors",
        str(args.priors),
        "--provider",
        args.provider,
        "--model",
        args.model,
        "--temperature",
        str(args.temperature),
        "--max-tokens",
        str(args.max_tokens),
        "--condition-order",
        args.condition_order,
        "--timeout",
        str(args.timeout),
        "--output-root",
        str(args.output_root),
        "--experiment-log",
        str(args.experiment_log),
    ]
    if args.provider_label:
        parts.extend(["--provider-label", args.provider_label])
    if args.base_url:
        parts.extend(["--base-url", args.base_url])
    if args.repetitions is not None:
        parts.extend(["--repetitions", str(args.repetitions)])
    parts.extend(["--session-id", session_id])
    if args.allow_mock:
        parts.append("--allow-mock")
    return " ".join(shlex.quote(part) for part in parts)


def execution_key_for(
    *,
    experiment_name: str,
    manifest_hash: str,
    program: ProgramRecord,
    condition: str,
    repetition: int,
    provider: str,
    model: str,
    temperature: float,
    max_tokens: int,
    system_prompt_hash: str,
    shared_prompt_hash: str,
    prior_hash: str | None,
) -> str:
    return canonical_hash(
        {
            "experiment_name": experiment_name,
            "manifest_hash": manifest_hash,
            "program_id": program.program_id,
            "condition": condition,
            "repetition": repetition,
            "provider": provider,
            "model": model,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "system_prompt_hash": system_prompt_hash,
            "shared_prompt_hash": shared_prompt_hash,
            "prior_hash": prior_hash,
        }
    )


def append_experiment_log(path: Path, record: ParsedRunRecord) -> None:
    status_note = record.error_type or "-"
    output = record.raw_response_path or "-"
    line = (
        f"| {record.timestamp.isoformat()} | {record.run_id} | "
        f"{record.experiment_name}/{record.condition}/rep-{record.repetition} | "
        f"{record.manifest_hash[:12]} | {record.status} | {output} | {status_note} |\n"
    )
    with path.open("a", encoding="utf-8") as handle:
        handle.write(line)


def run_one(
    *,
    provider: LLMProvider,
    program: ProgramRecord,
    condition: str,
    repetition: int,
    experiment_name: str,
    session_id: str,
    system_prompt: str,
    user_prompt: str,
    shared_prompt_hash: str,
    prior_hash: str | None,
    manifest_hash: str,
    model: str,
    temperature: float,
    max_tokens: int,
    raw_session_dir: Path,
    processed_session_dir: Path,
) -> ParsedRunRecord:
    run_id = str(uuid.uuid4())
    timestamp = utc_now()
    execution_key = execution_key_for(
        experiment_name=experiment_name,
        manifest_hash=manifest_hash,
        program=program,
        condition=condition,
        repetition=repetition,
        provider=provider.name,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        system_prompt_hash=sha256_text(system_prompt),
        shared_prompt_hash=shared_prompt_hash,
        prior_hash=prior_hash,
    )
    common = {
        "run_id": run_id,
        "session_id": session_id,
        "execution_key": execution_key,
        "experiment_name": experiment_name,
        "program_id": program.program_id,
        "task_id": program.task_id,
        "condition": condition,
        "repetition": repetition,
        "provider": provider.name,
        "model": model,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "timestamp": timestamp,
        "source_line_count": program.source_line_count,
        "loc": program.loc,
        "evaluation_denominator": program.exam_denominator,
        "faulty_lines": program.faulty_lines,
        "pattern_label": program.pattern_label,
        "difficulty": program.difficulty,
        "system_prompt_hash": sha256_text(system_prompt),
        "shared_prompt_hash": shared_prompt_hash,
        "prior_hash": prior_hash,
        "prompt_chars": len(system_prompt) + len(user_prompt),
        "prompt_tokens_estimate": (len(system_prompt) + len(user_prompt) + 3) // 4,
        "manifest_hash": manifest_hash,
    }
    try:
        reply = provider.complete(
            CompletionRequest(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
            )
        )
    except Exception as exc:
        record = ParsedRunRecord.model_validate(
            {
                **common,
                "latency": None,
                "token_usage": {},
                "raw_response_path": None,
                "parsed_response": None,
                "status": "provider_failure",
                "error_type": type(exc).__name__,
                "error_message": str(exc),
            }
        )
        write_json_new(
            processed_session_dir / f"{run_id}.json",
            record.model_dump(mode="json"),
        )
        return record

    raw_path = raw_session_dir / f"{run_id}.json"
    raw_payload = {
        **common,
        "timestamp": (reply.timestamp or timestamp).isoformat(),
        "system_prompt": system_prompt,
        "user_prompt": user_prompt,
        "raw_response": reply.raw_response,
        "latency": reply.latency,
        "token_usage": reply.token_usage,
        "response_metadata": reply.response_metadata,
        "actual_provider": reply.provider,
        "actual_model": reply.model,
        "prompt_input_fields": [
            "program_id",
            "task_id",
            "problem_context",
            "numbered_buggy_source",
        ],
        "raw_saved_before_parsing": True,
    }
    write_json_new(raw_path, raw_payload)

    if reply.provider != provider.name or reply.model != model:
        parsed = None
        status = "provider_failure"
        error_type = "ModelIdentityMismatch"
        error_message = (
            f"requested {provider.name}/{model}, received {reply.provider}/{reply.model}"
        )
    else:
        try:
            parsed = parse_ranking(
                reply.raw_response,
                source_line_count=program.source_line_count,
                loc=program.exam_denominator,
            )
            status = "ok"
            error_type = None
            error_message = None
        except ResponseParseError as exc:
            parsed = None
            status = "parser_failure"
            error_type = type(exc).__name__
            error_message = str(exc)

    record = ParsedRunRecord.model_validate(
        {
            **common,
            "timestamp": reply.timestamp or timestamp,
            "latency": reply.latency,
            "token_usage": reply.token_usage,
            "raw_response": reply.raw_response,
            "raw_response_path": relative_to_root(raw_path),
            "parsed_response": parsed,
            "status": status,
            "error_type": error_type,
            "error_message": error_message,
        }
    )
    write_json_new(
        processed_session_dir / f"{run_id}.json",
        record.model_dump(mode="json"),
    )
    return record


def condition_order(mode: str, program_index: int, repetition: int, names: tuple[str, str]) -> list[str]:
    control, treatment = names
    if mode == "control_first":
        return [control, treatment]
    if mode == "treatment_first":
        return [treatment, control]
    if mode == "counterbalanced":
        return [control, treatment] if (program_index + repetition) % 2 == 0 else [treatment, control]
    raise ValueError(f"unknown condition order: {mode}")


def run(args: argparse.Namespace) -> int:
    load_dotenv(REPOSITORY_ROOT / ".env")
    config = load_yaml_object(args.config)
    experiment_name = str(config["experiment_name"])
    dataset_config = config["dataset"]
    conditions = config["conditions"]
    repetitions = int(args.repetitions or config["repetitions"])
    target_n = int(dataset_config["target_n"])
    control_name = str(conditions["control"])
    treatment_name = str(conditions["treatment"])
    required_metrics = {"top1", "top3", "top5", "exam"}
    if set(config.get("metrics", [])) != required_metrics:
        raise SafetyViolation(f"pilot metrics must be exactly {sorted(required_metrics)}")
    if config.get("statistics", {}).get("primary") != "exact_mcnemar":
        raise SafetyViolation("pilot primary statistic must be exact_mcnemar")
    if repetitions < 1 or args.max_tokens < 1:
        raise SafetyViolation("repetitions and max_tokens must be positive")

    manifest = load_manifest(args.manifest)
    run_started_at = utc_now()
    validate_manifest_for_run(
        manifest,
        target_n=target_n,
        run_started_at=run_started_at,
        expected_dataset_name=str(dataset_config["target"]),
    )
    if control_name == treatment_name:
        raise SafetyViolation("control and treatment condition names must differ")
    manifest_hash = file_sha256(args.manifest)
    system_prompt = args.system_prompt.read_text(encoding="utf-8")
    user_template = args.user_template.read_text(encoding="utf-8")
    priors = load_prior_map(args.priors)
    missing_priors = sorted({p.pattern_label for p in manifest.included} - set(priors))
    if missing_priors:
        raise SafetyViolation(f"included programs lack frozen priors: {missing_priors}")

    provider = make_provider(args)
    session_id = args.session_id or f"{run_started_at.strftime('%Y%m%dT%H%M%SZ')}-{uuid.uuid4().hex[:8]}"
    raw_root = args.output_root / "raw" / experiment_name
    processed_root = args.output_root / "processed" / experiment_name
    raw_session_dir = raw_root / session_id
    processed_session_dir = processed_root / session_id
    session_manifest_path = processed_session_dir / "session_manifest.json"
    session_manifest = {
        "session_id": session_id,
        "experiment_name": experiment_name,
        "manifest_path": relative_to_root(args.manifest),
        "manifest_hash": manifest_hash,
        "system_prompt_path": relative_to_root(args.system_prompt),
        "system_prompt_hash": sha256_text(system_prompt),
        "user_template_path": relative_to_root(args.user_template),
        "user_template_hash": sha256_text(user_template),
        "priors_path": relative_to_root(args.priors),
        "priors_hash": sha256_text(args.priors.read_text(encoding="utf-8")),
        "provider": provider.name,
        "model": args.model,
        "temperature": args.temperature,
        "max_tokens": args.max_tokens,
        "repetitions": repetitions,
        "condition_order": args.condition_order,
        "program_input_hashes": {
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
        },
        "run_command": shell_command(args, session_id),
        "engineering_only": provider.name == "mock",
    }
    if session_manifest_path.exists():
        existing_session = json.loads(session_manifest_path.read_text(encoding="utf-8"))
        if existing_session != session_manifest:
            raise SafetyViolation("resume settings do not match the immutable session manifest")
    else:
        write_json_new(session_manifest_path, session_manifest)
    known_keys = existing_execution_keys(raw_root)
    created: list[ParsedRunRecord] = []

    for program_index, program in enumerate(manifest.included):
        pair = build_prompt_pair(system_prompt, user_template, program, priors[program.pattern_label])
        for repetition in range(1, repetitions + 1):
            order = condition_order(
                args.condition_order,
                program_index,
                repetition,
                (control_name, treatment_name),
            )
            for condition in order:
                is_treatment = condition == treatment_name
                user_prompt = pair.treatment_user_prompt if is_treatment else pair.control_user_prompt
                prior_hash = pair.prior_hash if is_treatment else None
                key = execution_key_for(
                    experiment_name=experiment_name,
                    manifest_hash=manifest_hash,
                    program=program,
                    condition=condition,
                    repetition=repetition,
                    provider=provider.name,
                    model=args.model,
                    temperature=args.temperature,
                    max_tokens=args.max_tokens,
                    system_prompt_hash=sha256_text(system_prompt),
                    shared_prompt_hash=pair.shared_prompt_hash,
                    prior_hash=prior_hash,
                )
                if key in known_keys:
                    if args.resume:
                        continue
                    raise SafetyViolation(
                        f"duplicate run detected for {program.program_id}/{condition}/rep-{repetition}; "
                        f"existing raw record: {known_keys[key]}"
                    )
                record = run_one(
                    provider=provider,
                    program=program,
                    condition=condition,
                    repetition=repetition,
                    experiment_name=experiment_name,
                    session_id=session_id,
                    system_prompt=pair.system_prompt,
                    user_prompt=user_prompt,
                    shared_prompt_hash=pair.shared_prompt_hash,
                    prior_hash=prior_hash,
                    manifest_hash=manifest_hash,
                    model=args.model,
                    temperature=args.temperature,
                    max_tokens=args.max_tokens,
                    raw_session_dir=raw_session_dir,
                    processed_session_dir=processed_session_dir,
                )
                created.append(record)
                known_keys[key] = raw_session_dir / f"{record.run_id}.json"
                append_experiment_log(args.experiment_log, record)

    summary = {
        "session_id": session_id,
        "experiment_name": experiment_name,
        "started_at": run_started_at.isoformat(),
        "completed_at": utc_now().isoformat(),
        "created_runs": len(created),
        "successful_runs": sum(record.status == "ok" for record in created),
        "parser_failures": sum(record.status == "parser_failure" for record in created),
        "provider_failures": sum(record.status == "provider_failure" for record in created),
        "engineering_only": provider.name == "mock",
    }
    summary_name = f"session_summary-{utc_now().strftime('%Y%m%dT%H%M%S%fZ')}.json"
    write_json_new(processed_session_dir / summary_name, summary)
    print(json.dumps(summary, indent=2))
    return 0 if all(record.status == "ok" for record in created) else 2


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description="Run paired pattern-prior pilot experiments.")
    result.add_argument("--config", type=Path, default=REPOSITORY_ROOT / "pilot/config/pilot.yaml")
    result.add_argument("--manifest", type=Path, required=True)
    result.add_argument("--system-prompt", type=Path, required=True)
    result.add_argument("--user-template", type=Path, required=True)
    result.add_argument("--priors", type=Path, required=True)
    result.add_argument("--provider", default=os.environ.get("LLM_PROVIDER") or "")
    result.add_argument("--provider-label")
    result.add_argument("--base-url", default="")
    result.add_argument("--model", default=os.environ.get("LLM_MODEL") or "")
    result.add_argument(
        "--temperature", type=float, default=float(os.environ.get("LLM_TEMPERATURE") or "0")
    )
    result.add_argument(
        "--max-tokens", type=int, default=int(os.environ.get("LLM_MAX_TOKENS") or "1024")
    )
    result.add_argument("--repetitions", type=int)
    result.add_argument(
        "--condition-order",
        choices=("control_first", "treatment_first", "counterbalanced"),
        required=True,
        help="Must match the frozen scientific protocol; the runner does not choose it implicitly.",
    )
    result.add_argument("--timeout", type=float, default=120.0)
    result.add_argument("--session-id")
    result.add_argument("--output-root", type=Path, default=REPOSITORY_ROOT / "results")
    result.add_argument(
        "--experiment-log", type=Path, default=REPOSITORY_ROOT / "EXPERIMENT_LOG.md"
    )
    result.add_argument("--resume", action="store_true")
    result.add_argument("--allow-mock", action="store_true")
    return result


def main() -> None:
    args = parser().parse_args()
    if not args.provider:
        raise SystemExit("LLM provider is required via --provider or LLM_PROVIDER")
    if not args.model:
        raise SystemExit("LLM model is required via --model or LLM_MODEL")
    if args.repetitions is not None and args.repetitions < 1:
        raise SystemExit("--repetitions must be positive")
    try:
        raise SystemExit(run(args))
    except (SafetyViolation, ValueError, OSError, KeyError) as exc:
        print(f"pilot aborted: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
