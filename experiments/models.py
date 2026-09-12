from __future__ import annotations

import json
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class InclusionStatus(str, Enum):
    INCLUDED = "included"
    EXCLUDED = "excluded"


class ProgramRecord(BaseModel):
    """One immutable pilot candidate and its pre-treatment selection metadata."""

    model_config = ConfigDict(extra="forbid")

    program_id: str
    task_id: str
    buggy_source_path: Path
    fixed_source_path: Path
    tests_path: Path
    faulty_lines: list[int]
    pattern_label: str
    pattern_source: str
    loc: int = Field(gt=0)
    difficulty: str
    inclusion_status: InclusionStatus
    exclusion_reason: str | None = None
    exclusion_decided_at: datetime | None = None
    problem_context_path: Path | None = None
    evaluation_denominator: int | None = Field(default=None, gt=0)

    @field_validator("program_id", "task_id", "pattern_label", "pattern_source", "difficulty")
    @classmethod
    def non_empty_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("must not be blank")
        return value

    @field_validator("faulty_lines")
    @classmethod
    def ground_truth_is_present_and_unique(cls, value: list[int]) -> list[int]:
        if not value:
            raise ValueError("missing ground-truth faulty lines")
        if any(line < 1 for line in value):
            raise ValueError("faulty line numbers must be positive")
        if len(value) != len(set(value)):
            raise ValueError("faulty line numbers must be unique")
        return sorted(value)

    @field_validator("exclusion_decided_at")
    @classmethod
    def exclusion_timestamp_is_timezone_aware(
        cls, value: datetime | None
    ) -> datetime | None:
        if value is not None and (value.tzinfo is None or value.utcoffset() is None):
            raise ValueError("exclusion_decided_at must include a timezone")
        return value

    @model_validator(mode="after")
    def validate_files_and_selection(self) -> "ProgramRecord":
        for field_name in ("buggy_source_path", "fixed_source_path", "tests_path"):
            path = getattr(self, field_name)
            if not path.exists():
                raise ValueError(f"{field_name} does not exist: {path}")
        if not self.buggy_source_path.is_file() or not self.fixed_source_path.is_file():
            raise ValueError("buggy_source_path and fixed_source_path must be files")
        if self.problem_context_path is not None and not self.problem_context_path.is_file():
            raise ValueError(f"problem_context_path is not a file: {self.problem_context_path}")

        source_line_count = len(self.buggy_source_path.read_text(encoding="utf-8").splitlines())
        if source_line_count < 1:
            raise ValueError("buggy source is empty")
        impossible = [line for line in self.faulty_lines if line > source_line_count]
        if impossible:
            raise ValueError(
                f"faulty line numbers exceed source length {source_line_count}: {impossible}"
            )
        if self.loc > source_line_count:
            raise ValueError(f"loc {self.loc} exceeds physical source length {source_line_count}")
        denominator = self.evaluation_denominator or self.loc
        if denominator > source_line_count:
            raise ValueError(
                f"evaluation_denominator {denominator} exceeds source length {source_line_count}"
            )

        if self.inclusion_status is InclusionStatus.EXCLUDED:
            if not self.exclusion_reason or not self.exclusion_reason.strip():
                raise ValueError("excluded records require exclusion_reason")
            if self.exclusion_decided_at is None:
                raise ValueError("excluded records require exclusion_decided_at")
        elif self.exclusion_reason is not None or self.exclusion_decided_at is not None:
            raise ValueError("included records cannot carry exclusion metadata")
        return self

    @property
    def source_line_count(self) -> int:
        return len(self.buggy_source_path.read_text(encoding="utf-8").splitlines())

    @property
    def exam_denominator(self) -> int:
        return self.evaluation_denominator or self.loc


class ProgramManifest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    manifest_version: int = Field(default=1, ge=1)
    dataset_name: str
    created_at: datetime
    selection_frozen_at: datetime
    programs: list[ProgramRecord]

    @field_validator("dataset_name")
    @classmethod
    def dataset_name_not_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("dataset_name must not be blank")
        return value

    @field_validator("created_at", "selection_frozen_at")
    @classmethod
    def timestamps_are_timezone_aware(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("manifest timestamps must include a timezone")
        return value

    @model_validator(mode="after")
    def validate_manifest(self) -> "ProgramManifest":
        ids = [program.program_id for program in self.programs]
        duplicate_ids = sorted({item for item in ids if ids.count(item) > 1})
        if duplicate_ids:
            raise ValueError(f"duplicate program IDs: {duplicate_ids}")
        if self.selection_frozen_at < self.created_at:
            raise ValueError("selection_frozen_at cannot precede created_at")
        for program in self.programs:
            decided = program.exclusion_decided_at
            if decided is not None and decided > self.selection_frozen_at:
                raise ValueError(
                    f"{program.program_id}: exclusion was introduced after selection freeze"
                )
        return self

    @property
    def included(self) -> list[ProgramRecord]:
        return [p for p in self.programs if p.inclusion_status is InclusionStatus.INCLUDED]


class RankingItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    line: int = Field(gt=0)
    score: float = Field(ge=0.0, le=1.0)
    reason: str = ""


class RankingResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ranking: list[RankingItem] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_ordered_unique_ranking(self) -> "RankingResponse":
        lines = [item.line for item in self.ranking]
        if len(lines) != len(set(lines)):
            raise ValueError("ranking contains duplicate line numbers")
        scores = [item.score for item in self.ranking]
        if scores != sorted(scores, reverse=True):
            raise ValueError("ranking scores must be in non-increasing order")
        return self


class ParsedRunRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    run_id: str
    session_id: str
    execution_key: str
    experiment_name: str
    program_id: str
    task_id: str
    condition: str
    repetition: int
    provider: str
    model: str
    temperature: float
    max_tokens: int
    timestamp: datetime
    latency: float | None
    token_usage: dict[str, Any]
    raw_response: str | None = None
    raw_response_path: str | None
    parsed_response: RankingResponse | None
    status: str
    error_type: str | None = None
    error_message: str | None = None
    source_line_count: int
    loc: int
    evaluation_denominator: int
    faulty_lines: list[int]
    pattern_label: str
    difficulty: str
    system_prompt_hash: str
    shared_prompt_hash: str
    prior_hash: str | None
    prompt_chars: int
    prompt_tokens_estimate: int
    manifest_hash: str
    reasoning_effort: str | None = None


def _aware(value: datetime, field_name: str) -> None:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{field_name} must include a timezone")


def _resolve_program_paths(payload: dict[str, Any], base_dir: Path) -> dict[str, Any]:
    result = dict(payload)
    for name in (
        "buggy_source_path",
        "fixed_source_path",
        "tests_path",
        "problem_context_path",
    ):
        raw = result.get(name)
        if raw is not None:
            path = Path(raw)
            result[name] = path if path.is_absolute() else (base_dir / path).resolve()
    return result


def load_manifest(path: Path) -> ProgramManifest:
    path = path.resolve()
    raw_text = path.read_text(encoding="utf-8")
    payload = yaml.safe_load(raw_text) if path.suffix.lower() in {".yaml", ".yml"} else json.loads(raw_text)
    if not isinstance(payload, dict):
        raise ValueError("manifest root must be an object")
    payload = dict(payload)
    payload["programs"] = [
        _resolve_program_paths(program, path.parent) for program in payload.get("programs", [])
    ]
    manifest = ProgramManifest.model_validate(payload)
    _aware(manifest.created_at, "created_at")
    _aware(manifest.selection_frozen_at, "selection_frozen_at")
    for program in manifest.programs:
        if program.exclusion_decided_at is not None:
            _aware(program.exclusion_decided_at, "exclusion_decided_at")
    if manifest.selection_frozen_at > datetime.now(timezone.utc):
        raise ValueError("selection_frozen_at cannot be in the future")
    return manifest
