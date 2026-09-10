"""Generate write-once blinded ground truth artifact.

Phase 4 of pilot v2 protocol (SAMPLING_PROTOCOL.md §2, GROUND_TRUTH_PROTOCOL.md §§1-4).
DO NOT OPEN:
- pilot/PATTERN_PRIORS.md
- pilot/pattern_priors.json
- pilot/v2/GENERIC_PLACEBO_PRIOR.md
- pilot/v2/generic_placebo_prior.json
- rendered treatment prompts
"""

from __future__ import annotations

import csv
import difflib
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CODE_DIR = ROOT / "data/external/ConDefects/Code"
MANIFESTS_DIR = ROOT / "data/manifests"
FROZEN_TIMESTAMP = "2026-09-10T18:05:00+00:00"


def generate_ground_truth_freeze() -> tuple[list[dict], dict[str, int]]:
    all_programs = sorted(list(CODE_DIR.glob("*/Python/*")), key=lambda p: (p.parent.parent.name, p.name))
    records = []
    stats = {
        "total_evaluated": 0,
        "included_single_line": 0,
        "excluded_multi_hunk": 0,
        "excluded_multi_line": 0,
        "excluded_non_algorithmic": 0,
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

        # Only candidates surviving mechanical LOC and syntax filters are adjudicated
        try:
            compile(b_text, str(buggy_path), "exec")
        except SyntaxError:
            continue

        if loc < 25 or loc > 300:
            continue

        stats["total_evaluated"] += 1

        matcher = difflib.SequenceMatcher(None, b_lines, f_lines)
        changes = [op for op in matcher.get_opcodes() if op[0] != "equal"]
        diff_hunks = len(changes)

        changed_buggy_lines = []
        for op in changes:
            tag, b_start, b_end, f_start, f_end = op
            # 1-indexed buggy line numbers
            changed_buggy_lines.extend(list(range(b_start + 1, b_end + 1)))

        if diff_hunks > 1:
            decision = "exclude"
            faulty_lines = "[]"
            exclusion_reason = "multiple independent faults"
            justification = "Multi-hunk fix per GROUND_TRUTH_PROTOCOL.md §3"
            stats["excluded_multi_hunk"] += 1
        elif diff_hunks == 1:
            tag, b_start, b_end, f_start, f_end = changes[0]
            if tag != "replace" or (b_end - b_start != 1) or (f_end - f_start != 1):
                decision = "exclude"
                faulty_lines = "[]"
                exclusion_reason = "multi-line fault — excluded by v2 single-line filter"
                justification = "Multi-line fix or insertion/deletion per GROUND_TRUTH_PROTOCOL.md §3"
                stats["excluded_multi_line"] += 1
            else:
                b_line_text = b_lines[b_start].strip()
                f_line_text = f_lines[f_start].strip()
                faulty_line_num = b_start + 1
                if b_line_text.lower() == f_line_text.lower() and ("print" in b_line_text or "print" in f_line_text):
                    decision = "exclude"
                    faulty_lines = "[]"
                    exclusion_reason = "non-algorithmic fault"
                    justification = "Fix changes only I/O formatting or parsing per GROUND_TRUTH_PROTOCOL.md §3"
                    stats["excluded_non_algorithmic"] += 1
                else:
                    decision = "include"
                    faulty_lines = f"[{faulty_line_num}]"
                    exclusion_reason = ""
                    justification = "Single-line fix: altered operator/operand/bound/index per GROUND_TRUTH_PROTOCOL.md §3"
                    stats["included_single_line"] += 1
        else:
            decision = "exclude"
            faulty_lines = "[]"
            exclusion_reason = "no diff detected between buggy and fixed versions"
            justification = "Identical files per GROUND_TRUTH_PROTOCOL.md §3"

        records.append({
            "program_id": program_id,
            "task_id": task_id,
            "diff_hunks": diff_hunks,
            "changed_buggy_lines": str(changed_buggy_lines),
            "decision": decision,
            "faulty_lines": faulty_lines,
            "exclusion_reason": exclusion_reason,
            "justification": justification,
            "timestamp": FROZEN_TIMESTAMP,
        })

    return records, stats


def main() -> None:
    records, stats = generate_ground_truth_freeze()
    out_csv = MANIFESTS_DIR / "ground_truth_freeze_v2.csv"
    fieldnames = [
        "program_id",
        "task_id",
        "diff_hunks",
        "changed_buggy_lines",
        "decision",
        "faulty_lines",
        "exclusion_reason",
        "justification",
        "timestamp",
    ]
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    print(f"Wrote {len(records)} records to {out_csv}")
    print("Ground truth statistics:")
    for k, v in stats.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
