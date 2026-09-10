from __future__ import annotations

from pathlib import Path

import pytest

from experiments.models import ProgramRecord
from experiments.parsing import ResponseParseError, parse_ranking
from experiments.prompts import PRIOR_OPEN, build_prompt_pair, validate_user_template


def program(tmp_path: Path) -> ProgramRecord:
    tmp_path.mkdir(parents=True, exist_ok=True)
    buggy = tmp_path / "buggy.py"
    fixed = tmp_path / "fixed.py"
    tests = tmp_path / "tests"
    buggy.write_text("x = 1\nprint(x)\n", encoding="utf-8")
    fixed.write_text("x = 2\nprint(x)\n", encoding="utf-8")
    tests.mkdir()
    return ProgramRecord(
        program_id="p1",
        task_id="t1",
        buggy_source_path=buggy,
        fixed_source_path=fixed,
        tests_path=tests,
        faulty_lines=[1],
        pattern_label="oracle-label",
        pattern_source="handoff",
        loc=2,
        difficulty="level",
        inclusion_status="included",
    )


def test_prompt_pair_differs_only_by_prior(tmp_path: Path) -> None:
    pair = build_prompt_pair(
        "system",
        "Program {program_id}\n{numbered_buggy_source}",
        program(tmp_path),
        "frozen prior",
    )
    assert pair.treatment_user_prompt.startswith(pair.control_user_prompt)
    assert pair.treatment_user_prompt[len(pair.control_user_prompt):] == (
        f"\n\n{PRIOR_OPEN}\nfrozen prior\n</DEBUGGING_PRIOR>"
    )
    assert "oracle-label" not in pair.control_user_prompt


def test_prompt_template_rejects_ground_truth() -> None:
    with pytest.raises(ValueError, match="forbidden"):
        validate_user_template("{numbered_buggy_source}\n{faulty_lines}")


def test_parser_accepts_fenced_json_and_preserves_order() -> None:
    parsed = parse_ranking(
        '```json\n{"ranking":[{"line":2,"score":0.9,"reason":"a"},{"line":1,"score":0.4,"reason":"b"}]}\n```',
        source_line_count=2,
        loc=2,
    )
    assert [item.line for item in parsed.ranking] == [2, 1]


@pytest.mark.parametrize(
    "response",
    [
        '{"ranking":[{"line":3,"score":0.9,"reason":"outside"}]}',
        '{"ranking":[{"line":1,"score":0.1,"reason":"low"},{"line":2,"score":0.9,"reason":"high"}]}',
        '{"ranking":[{"line":1,"score":0.9,"reason":"a"},{"line":1,"score":0.8,"reason":"b"}]}',
        "not json",
    ],
)
def test_parser_rejects_invalid_rankings(response: str) -> None:
    with pytest.raises(ResponseParseError):
        parse_ranking(response, source_line_count=2, loc=2)
