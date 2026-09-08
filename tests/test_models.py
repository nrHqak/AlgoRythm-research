from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pytest
from pydantic import ValidationError

from experiments.models import ProgramManifest, ProgramRecord


def source_fixture(tmp_path: Path) -> dict[str, Path]:
    tmp_path.mkdir(parents=True, exist_ok=True)
    buggy = tmp_path / "buggy.py"
    fixed = tmp_path / "fixed.py"
    tests = tmp_path / "tests"
    buggy.write_text("x = 1\nprint(x)\n", encoding="utf-8")
    fixed.write_text("x = 2\nprint(x)\n", encoding="utf-8")
    tests.mkdir()
    return {"buggy": buggy, "fixed": fixed, "tests": tests}


def valid_program(tmp_path: Path, program_id: str = "p1") -> ProgramRecord:
    paths = source_fixture(tmp_path)
    return ProgramRecord(
        program_id=program_id,
        task_id="t1",
        buggy_source_path=paths["buggy"],
        fixed_source_path=paths["fixed"],
        tests_path=paths["tests"],
        faulty_lines=[1],
        pattern_label="external-label",
        pattern_source="handoff-row-1",
        loc=2,
        difficulty="external-level",
        inclusion_status="included",
    )


def test_rejects_missing_source(tmp_path: Path) -> None:
    paths = source_fixture(tmp_path)
    paths["buggy"].unlink()
    with pytest.raises(ValidationError, match="does not exist"):
        ProgramRecord(
            program_id="p1",
            task_id="t1",
            buggy_source_path=paths["buggy"],
            fixed_source_path=paths["fixed"],
            tests_path=paths["tests"],
            faulty_lines=[1],
            pattern_label="label",
            pattern_source="source",
            loc=1,
            difficulty="level",
            inclusion_status="included",
        )


def test_rejects_missing_ground_truth_and_impossible_lines(tmp_path: Path) -> None:
    program = valid_program(tmp_path)
    with pytest.raises(ValidationError, match="missing ground-truth"):
        ProgramRecord(**{**program.model_dump(), "faulty_lines": []})
    with pytest.raises(ValidationError, match="exceed source length"):
        ProgramRecord(**{**program.model_dump(), "faulty_lines": [99]})


def test_rejects_missing_final_oracle_label(tmp_path: Path) -> None:
    program = valid_program(tmp_path)
    with pytest.raises(ValidationError, match="must not be blank"):
        ProgramRecord(**{**program.model_dump(), "pattern_label": " "})


def test_manifest_rejects_duplicate_ids(tmp_path: Path) -> None:
    first = valid_program(tmp_path / "one")
    second = valid_program(tmp_path / "two")
    with pytest.raises(ValidationError, match="duplicate program IDs"):
        ProgramManifest(
            dataset_name="dataset",
            created_at=datetime(2026, 9, 1, tzinfo=timezone.utc),
            selection_frozen_at=datetime(2026, 9, 2, tzinfo=timezone.utc),
            programs=[first, second],
        )


def test_rejects_post_freeze_exclusion(tmp_path: Path) -> None:
    program = valid_program(tmp_path)
    excluded = ProgramRecord(
        **{
            **program.model_dump(),
            "inclusion_status": "excluded",
            "exclusion_reason": "predefined rule",
            "exclusion_decided_at": datetime(2026, 9, 3, tzinfo=timezone.utc),
        }
    )
    with pytest.raises(ValidationError, match="after selection freeze"):
        ProgramManifest(
            dataset_name="dataset",
            created_at=datetime(2026, 9, 1, tzinfo=timezone.utc),
            selection_frozen_at=datetime(2026, 9, 2, tzinfo=timezone.utc),
            programs=[excluded],
        )
