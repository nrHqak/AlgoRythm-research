#!/usr/bin/env python3
"""
Interactive, resumable CLI for blinded human pattern annotation (v2.2
remediation, Option A). See data/PATTERN_LABEL_PROVENANCE_AUDIT.md and
annotation_v2_2/README.md.

Reads annotation_v2_2/blinded_records.jsonl (232 records, built by
scripts/build_annotation_workspace_v2_2.py -- run that first).

Shows, for each program: task_id, contest/problem/difficulty, an AtCoder URL
(never auto-fetched), the buggy source, and a compact reference to the 12
pattern slugs. Computes and displays NEUTRAL structural signals (presence of
sort/bisect/heapq/deque/Counter/dp-like-table/itertools/recursion) as raw
facts only -- this script never combines them into a suggested label and
never picks a label on your behalf.

You choose the label. Every decision is written immediately (append + flush)
to data/manifests/pattern_annotations_v2_2.csv, so progress is never lost
and the script is safe to interrupt (Ctrl+C) and resume at any time by
simply re-running it.

Usage:
    .venv/bin/python scripts/annotate_patterns_v2_2.py            # resume/continue
    .venv/bin/python scripts/annotate_patterns_v2_2.py --revisit  # only UNCERTAIN/skipped
    .venv/bin/python scripts/annotate_patterns_v2_2.py --stats    # progress only, no prompts
    .venv/bin/python scripts/annotate_patterns_v2_2.py --edit 45028964   # re-annotate one program

Per record you will be asked:
  1. Label: a digit 1-12 (see the printed legend), or 'o' outside_vocabulary,
     'u' uncertain, 's' skip. You may also type a combined token like "5h"
     to give the label and confidence in one entry.
  2. Confidence: h / m / l (skipped automatically for 'u'/'s').
  3. Note: free text, or just press Enter to leave blank.

Task metadata/editorial is never shown or fetched automatically -- you only
see the buggy source, task_id, contest/problem/difficulty, and a URL you can
open by hand. Because of that, the default recorded pattern_source for every
confirmed label is "human-structural-verification". If you explicitly opened
the AtCoder URL (or otherwise consulted task metadata/editorial) for a
specific, hard case, append '+' to your confidence letter (e.g. "h+", or
inline as "5h+") to record "task-metadata+human-structural-verification"
instead, for that program only. The '+' is optional and costs nothing when
you don't use it.

Other commands at the label prompt: 'v' show full vocabulary/confusable-pair
text again, 'b' go back to the previous record, 'q' quit and save, 'h' help.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
WORKSPACE_DIR = REPO_ROOT / "annotation_v2_2"
RECORDS_FILE = WORKSPACE_DIR / "blinded_records.jsonl"
CHEATSHEET_FILE = WORKSPACE_DIR / "PATTERN_VOCABULARY_CHEATSHEET.md"
OUT_CSV = REPO_ROOT / "data" / "manifests" / "pattern_annotations_v2_2.csv"

PATTERN_SOURCE_STRUCTURAL_ONLY = "human-structural-verification"
PATTERN_SOURCE_WITH_METADATA = "task-metadata+human-structural-verification"

# Fixed vocabulary order -- identical to pilot/PATTERN_VOCABULARY.md's table.
VOCAB = [
    "two_pointers",
    "sliding_window",
    "binary_search",
    "prefix_sums",
    "dynamic_programming",
    "greedy",
    "graph_traversal_dfs_bfs",
    "sorting_based",
    "hash_map_counting",
    "brute_force_implementation",
    "intervals",
    "simulation",
]
KEY_TO_SLUG = {str(i + 1): slug for i, slug in enumerate(VOCAB)}
CONF_MAP = {"h": "high", "m": "medium", "l": "low"}

FIELDNAMES = [
    "annotation_index",
    "program_id",
    "task_id",
    "pattern_label",
    "pattern_source",
    "annotation_timestamp",
    "annotation_note",
    "confidence",
]

LEGEND = "  ".join(f"{k}={v}" for k, v in KEY_TO_SLUG.items())


def load_records() -> list[dict]:
    if not RECORDS_FILE.exists():
        sys.exit(
            f"Missing {RECORDS_FILE}. Run "
            "scripts/build_annotation_workspace_v2_2.py first."
        )
    records = []
    with open(RECORDS_FILE, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def load_latest_annotations() -> dict[str, dict]:
    """Latest row per program_id (append-log semantics: a later row for the
    same program_id supersedes an earlier one -- this is how 'revisit' and
    '--edit' work without ever rewriting history in place)."""
    latest: dict[str, dict] = {}
    if OUT_CSV.exists():
        with open(OUT_CSV, encoding="utf-8") as f:
            for row in csv.DictReader(f):
                latest[row["program_id"]] = row
    return latest


def ensure_csv_header() -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    if not OUT_CSV.exists():
        with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=FIELDNAMES).writeheader()


def append_row(row: dict) -> None:
    with open(OUT_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writerow(row)
        f.flush()


def is_confirmed(row: dict | None) -> bool:
    if row is None:
        return False
    return row["pattern_label"] in VOCAB or row["pattern_label"] == "outside_vocabulary"


NEUTRAL_SIGNAL_CHECKS = [
    ("sort/sorted", re.compile(r"\.sort\(|\bsorted\(")),
    ("bisect", re.compile(r"\bbisect(_left|_right)?\b")),
    ("heapq", re.compile(r"\bheapq\b|\bheappush\b|\bheappop\b")),
    ("deque/queue", re.compile(r"\bdeque\b|\bqueue\b", re.I)),
    ("Counter/defaultdict", re.compile(r"\bCounter\(|\bdefaultdict\(")),
    ("2D-list / dp-like table literal", re.compile(r"\[\s*\[\s*0\b|\bdp\b\s*=\s*\[|\bmemo\b\s*=")),
    ("itertools (perm/comb/product)", re.compile(r"\bpermutations\b|\bcombinations\b|\bproduct\(")),
    ("recursion (def f(...) calling f)", None),  # handled specially below
    ("while loop", re.compile(r"\bwhile\b")),
    ("accumulate/prefix-style var", re.compile(r"\baccumulate\b|\b(pref|cumsum|prefix)\b\s*=\s*\[")),
]


def _has_recursion(src: str) -> bool:
    """Heuristic only: True if some function's own name is called again
    anywhere after that function's `def` line."""
    for match in re.finditer(r"^\s*def\s+(\w+)\s*\(", src, re.M):
        fn = match.group(1)
        rest_of_file = src[match.end():]
        if re.search(rf"\b{re.escape(fn)}\s*\(", rest_of_file):
            return True
    return False


def compute_neutral_signals(src: str) -> list[str]:
    """Raw structural facts only -- never combined into a recommended label."""
    hits = []
    for name, pattern in NEUTRAL_SIGNAL_CHECKS:
        if name.startswith("recursion"):
            if _has_recursion(src):
                hits.append(name)
            continue
        if pattern.search(src):
            hits.append(name)
    return hits


def print_vocab_legend() -> None:
    print("\nLabel keys:")
    for k, v in KEY_TO_SLUG.items():
        print(f"  {k:>2} = {v}")
    print("   o = outside_vocabulary    u = uncertain (revisit)    s = skip")


def print_full_cheatsheet() -> None:
    if CHEATSHEET_FILE.exists():
        print("\n" + CHEATSHEET_FILE.read_text(encoding="utf-8"))
    else:
        print("Cheat-sheet file not found; see pilot/PATTERN_VOCABULARY.md directly.")


def print_record(record: dict, position: int, total: int, pending_left: int) -> None:
    print("\n" + "=" * 78)
    print(
        f"[{position}/{total} in frame | {pending_left} pending] "
        f"index={record['index']}  program_id={record['program_id']}  "
        f"task_id={record['task_id']}"
    )
    print(
        f"contest={record['contest']}  problem={record['problem_letter']}  "
        f"difficulty={record['difficulty']}  loc={record['loc']}"
    )
    print(f"AtCoder URL (open manually if you want problem context): {record['atcoder_url']}")
    signals = compute_neutral_signals(record["buggy_source"])
    print(f"Structural signals (informational only, NOT a recommendation): {', '.join(signals) or 'none detected'}")
    print("-" * 78)
    for i, line in enumerate(record["buggy_source"].splitlines(), start=1):
        print(f"{i:4d}| {line}")
    print("-" * 78)
    print_vocab_legend()


def prompt_label(record: dict) -> tuple[str, str | None, bool] | None:
    """Returns (pattern_label_or_control, inline_confidence_or_None,
    inline_used_metadata), or None if the user wants to go back.
    inline_used_metadata is True only if a trailing '+' was typed with the
    label (e.g. "5h+" or "5+"), meaning task metadata/editorial was
    explicitly consulted for this program."""
    while True:
        raw = input(
            "\nLabel [1-12 / o / u / s / v=full vocab / b=back / q=quit] "
            "(append + if you consulted task metadata, e.g. '5h+'): "
        ).strip().lower()
        if raw == "":
            continue
        if raw == "q":
            return ("__QUIT__", None, False)
        if raw == "b":
            return None
        if raw == "v":
            print_full_cheatsheet()
            continue
        if raw in ("h", "help", "?"):
            print(__doc__)
            continue
        if raw == "u":
            return ("UNCERTAIN", None, False)
        if raw == "s":
            return ("SKIP", None, False)
        if raw in ("o", "o+"):
            return ("outside_vocabulary", None, raw.endswith("+"))
        # combined token, e.g. "5h", "5h+", "5+", "5 h", "oh+"
        m = re.match(r"^(o|[1-9]|1[0-2])\s*([hml])?(\+)?$", raw)
        if m:
            key, conf, meta = m.group(1), m.group(2), m.group(3)
            label = "outside_vocabulary" if key == "o" else KEY_TO_SLUG[key]
            return (label, CONF_MAP[conf] if conf else None, bool(meta))
        print("Not understood. Enter a number 1-12, 'o', 'u', 's', 'v', 'b', or 'q'.")


def prompt_confidence() -> tuple[str, bool]:
    """Returns (confidence, used_metadata). Append '+' (e.g. 'h+') to flag
    that task metadata/editorial was explicitly consulted for this case."""
    while True:
        raw = input(
            "Confidence [h/m/l] (append + if you consulted task metadata, e.g. 'h+'): "
        ).strip().lower()
        m = re.match(r"^([hml])(\+)?$", raw)
        if m:
            return CONF_MAP[m.group(1)], bool(m.group(2))
        print("Enter h, m, or l (optionally with a trailing + for metadata consulted).")


def prompt_note(default_prompt: str = "Note (optional, Enter to skip): ") -> str:
    return input(default_prompt).strip()


def record_decision(
    record: dict, label: str, confidence: str, note: str, used_metadata: bool = False
) -> None:
    if is_confirmed({"pattern_label": label}):
        source = PATTERN_SOURCE_WITH_METADATA if used_metadata else PATTERN_SOURCE_STRUCTURAL_ONLY
    else:
        source = "pending-revisit"
    row = {
        "annotation_index": record["index"],
        "program_id": record["program_id"],
        "task_id": record["task_id"],
        "pattern_label": label,
        "pattern_source": source,
        "annotation_timestamp": datetime.now(timezone.utc).isoformat(),
        "annotation_note": note,
        "confidence": confidence,
    }
    append_row(row)


def print_stats(records: list[dict], latest: dict[str, dict]) -> None:
    total = len(records)
    confirmed = sum(1 for r in records if is_confirmed(latest.get(r["program_id"])))
    outside = sum(1 for r in records if latest.get(r["program_id"], {}).get("pattern_label") == "outside_vocabulary")
    uncertain = sum(1 for r in records if latest.get(r["program_id"], {}).get("pattern_label") in ("UNCERTAIN", "SKIP"))
    untouched = total - confirmed - uncertain
    print(f"Frame size: {total}")
    print(f"Confirmed (valid label or outside_vocabulary): {confirmed}  ({outside} of which outside_vocabulary)")
    print(f"Pending (uncertain/skipped): {uncertain}")
    print(f"Never touched: {untouched}")
    print(f"Complete: {'YES' if confirmed == total else 'NO'} ({confirmed}/{total})")
    if confirmed:
        from collections import Counter

        dist = Counter(
            latest[r["program_id"]]["pattern_label"]
            for r in records
            if is_confirmed(latest.get(r["program_id"]))
        )
        print("\nCurrent class distribution among confirmed labels:")
        for slug, count in dist.most_common():
            print(f"  {slug:30s} {count}")


def main() -> None:
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("--revisit", action="store_true", help="only show UNCERTAIN/skipped records")
    ap.add_argument("--stats", action="store_true", help="print progress and exit")
    ap.add_argument("--edit", metavar="PROGRAM_ID", help="re-annotate one specific program_id and exit")
    args = ap.parse_args()

    records = load_records()
    ensure_csv_header()
    latest = load_latest_annotations()

    if args.stats:
        print_stats(records, latest)
        return

    if args.edit:
        target = next((r for r in records if r["program_id"] == args.edit), None)
        if target is None:
            sys.exit(f"program_id {args.edit} not found in the 232-program frame.")
        queue = [target]
    elif args.revisit:
        queue = [
            r for r in records
            if latest.get(r["program_id"], {}).get("pattern_label") in ("UNCERTAIN", "SKIP")
        ]
        if not queue:
            print("No uncertain/skipped records to revisit. Run with --stats for full status.")
            return
    else:
        queue = [r for r in records if not is_confirmed(latest.get(r["program_id"]))]
        if not queue:
            print("All 232 programs are confirmed. Run --stats for the final distribution,")
            print("then scripts/validate_pattern_annotations_v2_2.py to produce the audit report.")
            return

    print(f"Starting session: {len(queue)} record(s) queued.")
    print("Progress is saved after every decision. Ctrl+C or 'q' to stop safely at any time.")

    pos = 0
    try:
        while 0 <= pos < len(queue):
            record = queue[pos]
            pending_left = len(queue) - pos
            print_record(record, pos + 1, len(queue), pending_left)

            choice = prompt_label(record)
            if choice is None:  # 'b' back
                pos = max(0, pos - 1)
                continue
            label, inline_conf, inline_meta = choice
            if label == "__QUIT__":
                print("Stopped. Progress saved. Re-run the same command to resume.")
                return

            if label in ("UNCERTAIN", "SKIP"):
                note = "" if label == "SKIP" else prompt_note("Why uncertain? (optional, Enter to skip): ")
                record_decision(record, label, "", note)
                pos += 1
                continue

            if inline_conf:
                confidence, used_metadata = inline_conf, inline_meta
            else:
                confidence, used_metadata = prompt_confidence()
                used_metadata = used_metadata or inline_meta
            note_prompt = "Reason (short, e.g. 'DSU'): " if label == "outside_vocabulary" else None
            note = prompt_note(note_prompt) if note_prompt else prompt_note()
            record_decision(record, label, confidence, note, used_metadata)
            pos += 1
    except KeyboardInterrupt:
        print("\nInterrupted. Progress saved. Re-run the same command to resume.")
        return

    print("\nQueue complete for this session.")
    latest = load_latest_annotations()
    print_stats(records, latest)


if __name__ == "__main__":
    main()
