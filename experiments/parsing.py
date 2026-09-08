from __future__ import annotations

import json
from typing import Any

from experiments.models import RankingResponse


class ResponseParseError(ValueError):
    pass


def _candidate_json_values(raw_response: str) -> list[Any]:
    stripped = raw_response.strip()
    candidates: list[str] = [stripped]
    if stripped.startswith("```") and stripped.endswith("```"):
        inner = stripped[3:-3].strip()
        if inner.lower().startswith("json"):
            inner = inner[4:].lstrip()
        candidates.append(inner)

    decoder = json.JSONDecoder()
    values: list[Any] = []
    seen: set[str] = set()
    for candidate in candidates:
        if candidate in seen:
            continue
        seen.add(candidate)
        try:
            values.append(json.loads(candidate))
            continue
        except json.JSONDecodeError:
            pass
        for index, character in enumerate(candidate):
            if character != "{":
                continue
            try:
                value, _ = decoder.raw_decode(candidate[index:])
            except json.JSONDecodeError:
                continue
            values.append(value)
            break
    return values


def parse_ranking(raw_response: str, *, source_line_count: int, loc: int) -> RankingResponse:
    errors: list[str] = []
    for value in _candidate_json_values(raw_response):
        try:
            parsed = RankingResponse.model_validate(value)
            invalid = [item.line for item in parsed.ranking if item.line > source_line_count]
            if invalid:
                raise ValueError(
                    f"ranking line numbers exceed source length {source_line_count}: {invalid}"
                )
            if len(parsed.ranking) > loc:
                raise ValueError(f"ranking has {len(parsed.ranking)} entries but loc is {loc}")
            return parsed
        except ValueError as exc:
            errors.append(str(exc))
    detail = errors[-1] if errors else "no JSON object found"
    raise ResponseParseError(f"could not parse a valid ordered ranking: {detail}")
