from __future__ import annotations

import hashlib
import string
from dataclasses import dataclass

from experiments.models import ProgramRecord


PRIOR_OPEN = "<ALGORITHMIC_PATTERN_PRIOR>"
PRIOR_CLOSE = "</ALGORITHMIC_PATTERN_PRIOR>"
ALLOWED_TEMPLATE_FIELDS = {
    "program_id",
    "task_id",
    "problem_context",
    "numbered_buggy_source",
}
FORBIDDEN_TEMPLATE_FIELDS = {
    "faulty_lines",
    "fixed_source",
    "fixed_source_path",
    "ground_truth",
    "pattern_label",
}


@dataclass(frozen=True)
class PromptPair:
    system_prompt: str
    control_user_prompt: str
    treatment_user_prompt: str
    shared_prompt_hash: str
    prior_hash: str


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def numbered_source(source: str) -> str:
    return "\n".join(f"{index}: {line}" for index, line in enumerate(source.splitlines(), 1))


def validate_user_template(template: str) -> None:
    fields = {
        field_name
        for _, field_name, _, _ in string.Formatter().parse(template)
        if field_name is not None
    }
    forbidden = sorted(fields & FORBIDDEN_TEMPLATE_FIELDS)
    if forbidden:
        raise ValueError(f"ground-truth or treatment-only placeholders are forbidden: {forbidden}")
    unknown = sorted(fields - ALLOWED_TEMPLATE_FIELDS)
    if unknown:
        raise ValueError(f"unknown prompt placeholders: {unknown}")
    if "numbered_buggy_source" not in fields:
        raise ValueError("user prompt must contain {numbered_buggy_source}")
    if PRIOR_OPEN in template or PRIOR_CLOSE in template:
        raise ValueError("the shared user template cannot contain a treatment-prior block")


def build_prompt_pair(
    system_prompt: str,
    user_template: str,
    program: ProgramRecord,
    prior_text: str,
) -> PromptPair:
    validate_user_template(user_template)
    if not prior_text.strip():
        raise ValueError(f"missing frozen prior text for pattern {program.pattern_label!r}")
    source = program.buggy_source_path.read_text(encoding="utf-8")
    problem_context = (
        program.problem_context_path.read_text(encoding="utf-8")
        if program.problem_context_path is not None
        else ""
    )
    shared = user_template.format(
        program_id=program.program_id,
        task_id=program.task_id,
        problem_context=problem_context,
        numbered_buggy_source=numbered_source(source),
    ).rstrip()
    treatment = f"{shared}\n\n{PRIOR_OPEN}\n{prior_text.strip()}\n{PRIOR_CLOSE}"
    assert_only_prior_differs(shared, treatment, prior_text)
    return PromptPair(
        system_prompt=system_prompt,
        control_user_prompt=shared,
        treatment_user_prompt=treatment,
        shared_prompt_hash=sha256_text(shared),
        prior_hash=sha256_text(prior_text.strip()),
    )


def assert_only_prior_differs(control: str, treatment: str, prior_text: str) -> None:
    suffix = f"\n\n{PRIOR_OPEN}\n{prior_text.strip()}\n{PRIOR_CLOSE}"
    if treatment != control.rstrip() + suffix:
        raise ValueError("control/treatment prompt asymmetry exceeds the frozen prior block")
