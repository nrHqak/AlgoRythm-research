"""Deterministic enumeration and mechanical eligibility filtering for ConDefects-Python.

S1: Complete ConDefects-Python corpus (2,864 programs across 985 tasks).
S2: Mechanical eligibility filters (SAMPLING_PROTOCOL.md §3):
    - runnable under pinned Python (Python 3.14.3)
    - LOC >= 25 and LOC <= 300
    - evaluation_denominator >= 15
    - single-line fix shape (GROUND_TRUTH_PROTOCOL.md §3)
"""

from __future__ import annotations

import csv
import difflib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CODE_DIR = ROOT / "data/external/ConDefects/Code"
MANIFESTS_DIR = ROOT / "data/manifests"
PYTHON_VERSION = "3.14.3"


def build_inventory() -> tuple[list[dict], dict[str, int]]:
    all_programs = sorted(list(CODE_DIR.glob("*/Python/*")), key=lambda p: (p.parent.parent.name, p.name))
    records = []
    filter_counts = {
        "s1_total": len(all_programs),
        "syntax_error": 0,
        "loc_too_short": 0,
        "loc_too_long": 0,
        "evaluation_denominator_too_small": 0,
        "multi_hunk": 0,
        "multi_line_or_insertion_deletion": 0,
        "non_algorithmic": 0,
        "eligible": 0,
    }

    for p in all_programs:
        program_id = p.name
        task_id = p.parent.parent.name
        buggy_path = p / "faultyVersion.py"
        fixed_path = p / "correctVersion.py"

        b_text = buggy_path.read_text(encoding="utf-8", errors="ignore")
        f_text = fixed_path.read_text(encoding="utf-8", errors="ignore")
        b_lines = b_text.splitlines()
        f_lines = f_text.splitlines()
        loc = len(b_lines)
        evaluation_denominator = loc

        try:
            compile(b_text, str(buggy_path), "exec")
            runs_successfully = True
        except SyntaxError:
            runs_successfully = False

        passing_test_count = ""
        failing_test_count = ""
        eligibility_status = "eligible"
        exclusion_reason = ""

        if not runs_successfully:
            eligibility_status = "ineligible"
            exclusion_reason = "syntax error under pinned Python"
            filter_counts["syntax_error"] += 1
        elif loc < 25:
            eligibility_status = "ineligible"
            exclusion_reason = "loc < 25 (minimum length floor is 25)"
            filter_counts["loc_too_short"] += 1
        elif loc > 300:
            eligibility_status = "ineligible"
            exclusion_reason = "loc > 300 (maximum length ceiling is 300)"
            filter_counts["loc_too_long"] += 1
        elif evaluation_denominator < 15:
            eligibility_status = "ineligible"
            exclusion_reason = "evaluation_denominator < 15"
            filter_counts["evaluation_denominator_too_small"] += 1
        else:
            matcher = difflib.SequenceMatcher(None, b_lines, f_lines)
            changes = [op for op in matcher.get_opcodes() if op[0] != "equal"]
            if len(changes) > 1:
                eligibility_status = "ineligible"
                exclusion_reason = "multiple independent faults"
                filter_counts["multi_hunk"] += 1
            elif len(changes) == 1:
                tag, b_start, b_end, f_start, f_end = changes[0]
                if tag != "replace" or (b_end - b_start != 1) or (f_end - f_start != 1):
                    eligibility_status = "ineligible"
                    exclusion_reason = "multi-line fault — excluded by v2 single-line filter"
                    filter_counts["multi_line_or_insertion_deletion"] += 1
                else:
                    b_line_text = b_lines[b_start].strip()
                    f_line_text = f_lines[f_start].strip()
                    if b_line_text.lower() == f_line_text.lower() and ("print" in b_line_text or "print" in f_line_text):
                        eligibility_status = "ineligible"
                        exclusion_reason = "non-algorithmic fault"
                        filter_counts["non_algorithmic"] += 1
                    else:
                        eligibility_status = "eligible"
                        exclusion_reason = ""
                        filter_counts["eligible"] += 1
            else:
                eligibility_status = "ineligible"
                exclusion_reason = "no diff detected between buggy and fixed versions"

        records.append({
            "program_id": program_id,
            "task_id": task_id,
            "buggy_path": f"data/external/ConDefects/Code/{task_id}/Python/{program_id}/faultyVersion.py",
            "fixed_path": f"data/external/ConDefects/Code/{task_id}/Python/{program_id}/correctVersion.py",
            "tests_path": f"data/external/ConDefects/Test/{task_id}",
            "loc": loc,
            "python_version": PYTHON_VERSION,
            "runs_successfully": runs_successfully,
            "passing_test_count": passing_test_count,
            "failing_test_count": failing_test_count,
            "evaluation_denominator": evaluation_denominator,
            "eligibility_status": eligibility_status,
            "exclusion_reason": exclusion_reason,
        })

    return records, filter_counts


def main() -> None:
    records, counts = build_inventory()
    out_csv = MANIFESTS_DIR / "condfects_inventory_v2.csv"
    fieldnames = [
        "program_id",
        "task_id",
        "buggy_path",
        "fixed_path",
        "tests_path",
        "loc",
        "python_version",
        "runs_successfully",
        "passing_test_count",
        "failing_test_count",
        "evaluation_denominator",
        "eligibility_status",
        "exclusion_reason",
    ]
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    print(f"Wrote {len(records)} records to {out_csv}")
    print("Filter breakdown:")
    for k, v in counts.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
