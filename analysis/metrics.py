from __future__ import annotations

from typing import Any

from experiments.models import ParsedRunRecord, RankingResponse


def conservative_fault_rank(
    ranking: RankingResponse | None,
    faulty_lines: list[int],
    denominator: int,
) -> int:
    """Return the best faulty-line rank, assigning every score tie its worst rank."""

    if ranking is None:
        return denominator
    faulty = set(faulty_lines)
    candidate_ranks: list[int] = []
    items = ranking.ranking
    for index, item in enumerate(items):
        if item.line not in faulty:
            continue
        worst_tied_index = index
        while worst_tied_index + 1 < len(items):
            if items[worst_tied_index + 1].score != item.score:
                break
            worst_tied_index += 1
        candidate_ranks.append(worst_tied_index + 1)
    if not candidate_ranks:
        return denominator
    return min(min(candidate_ranks), denominator)


def evaluate_record(record: ParsedRunRecord) -> dict[str, Any]:
    rank = conservative_fault_rank(
        record.parsed_response,
        record.faulty_lines,
        record.evaluation_denominator,
    )
    failed_run = record.status != "ok"
    return {
        "run_id": record.run_id,
        "session_id": record.session_id,
        "execution_key": record.execution_key,
        "experiment_name": record.experiment_name,
        "program_id": record.program_id,
        "task_id": record.task_id,
        "pattern_label": record.pattern_label,
        "difficulty": record.difficulty,
        "condition": record.condition,
        "repetition": record.repetition,
        "provider": record.provider,
        "model": record.model,
        "temperature": record.temperature,
        "max_tokens": record.max_tokens,
        "status": record.status,
        "error_type": record.error_type,
        "error_message": record.error_message,
        "faulty_lines": json_list(record.faulty_lines),
        "ranking": (
            record.parsed_response.model_dump_json() if record.parsed_response is not None else None
        ),
        "first_fault_rank": rank,
        "top1": 0 if failed_run else int(rank <= 1),
        "top3": 0 if failed_run else int(rank <= 3),
        "top5": 0 if failed_run else int(rank <= 5),
        "exam": 1.0 if failed_run else rank / record.evaluation_denominator,
        "source_line_count": record.source_line_count,
        "loc": record.loc,
        "evaluation_denominator": record.evaluation_denominator,
        "latency": record.latency,
        "token_usage": json_dict(record.token_usage),
        "prompt_chars": record.prompt_chars,
        "prompt_tokens_estimate": record.prompt_tokens_estimate,
        "raw_response_path": record.raw_response_path,
        "manifest_hash": record.manifest_hash,
    }


def json_list(value: list[Any]) -> str:
    import json

    return json.dumps(value, separators=(",", ":"))


def json_dict(value: dict[str, Any]) -> str:
    import json

    return json.dumps(value, sort_keys=True, separators=(",", ":"))
