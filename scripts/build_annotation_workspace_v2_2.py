#!/usr/bin/env python3
"""
Build the blinded pattern-annotation workspace for v2.2 remediation
(Option A, authorized by the user; see data/PATTERN_LABEL_PROVENANCE_AUDIT.md).

Reconstructs the exact corrected task-independent frame F_v2.1 (232 programs)
using the SAME source file, seed, and dedup logic as
scripts/package_final_sample_v2_1.py steps 1-3 -- byte-for-byte identical
procedure, so the frame is guaranteed to be the same 232 (task_id,
program_id) pairs that produced the disputed v2.1 sample. This script does
NOT change dynamic test eligibility, ground truth, task deduplication, or the
sampling seed (20260910), and does NOT inspect any LLM result.

For each of the 232 programs it writes ONE blinded record to
annotation_v2_2/blinded_records.jsonl containing ONLY:
  - annotation index (1..232, fixed order = sorted(task_id))
  - program_id, task_id
  - contest, problem_letter (parsed from task_id -- reproducible, no network)
  - difficulty (from the local ConDefects difficulty.txt, if present)
  - a reference AtCoder URL (for optional human lookup; never auto-fetched)
  - loc (physical line count of the buggy source)
  - buggy_source (full text of faultyVersion.py)

It deliberately never reads or writes: faulty_lines, fixed.py, any diff,
pilot/pattern_priors.json, pilot/v2/generic_placebo_prior.json, the old
pattern_label/pattern_source/pattern_confidence/pattern_note from v2.0/v2.1,
selection_rank, or any LLM/localization artifact. This is what "blinded"
means in this script: those inputs are never loaded into memory here, so
they structurally cannot leak into a record.

Run: .venv/bin/python scripts/build_annotation_workspace_v2_2.py
"""
from __future__ import annotations

import hashlib
import json
import random
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CODE_DIR = REPO_ROOT / "data" / "external" / "ConDefects" / "Code"
DIFFICULTY_FILE = REPO_ROOT / "data" / "external" / "ConDefects" / "difficulty.txt"
DYNAMIC_ELIG_FILE = REPO_ROOT / "data" / "manifests" / "dynamic_test_eligibility_v2_1.csv"
V2_1_MANIFEST = REPO_ROOT / "data" / "manifests" / "pilot_manifest_v2_1.json"
WORKSPACE_DIR = REPO_ROOT / "annotation_v2_2"
OUT_JSONL = WORKSPACE_DIR / "blinded_records.jsonl"
OUT_MANIFEST = WORKSPACE_DIR / "frame_manifest.json"

SAMPLING_SEED = 20260910


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_eligible_pairs() -> list[tuple[str, str]]:
    """(task_id, program_id) pairs with eligible == 'True', via the stdlib csv
    module -- no third-party dependency."""
    import csv

    pairs: list[tuple[str, str]] = []
    with open(DYNAMIC_ELIG_FILE, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["eligible"] == "True":
                pairs.append((row["task_id"], row["program_id"]))
    return pairs


def build_frame() -> list[tuple[str, str]]:
    """Reproduces scripts/package_final_sample_v2_1.py steps 1-3 exactly:
    group eligible candidates by task_id, then seeded-dedup one program per
    task, iterating sorted(task_id) so the RNG consumption order is
    identical and therefore the result is bit-for-bit identical."""
    eligible = load_eligible_pairs()
    by_task: dict[str, list[str]] = defaultdict(list)
    for task_id, program_id in eligible:
        by_task[task_id].append(program_id)

    rng_s4 = random.Random(SAMPLING_SEED)
    frame: list[tuple[str, str]] = []
    for task_id in sorted(by_task.keys()):
        progs = sorted(by_task[task_id])
        chosen = progs[0] if len(progs) == 1 else rng_s4.choice(progs)
        frame.append((task_id, chosen))
    return frame


def load_difficulty_map() -> dict[str, str]:
    diff_map: dict[str, str] = {}
    if DIFFICULTY_FILE.exists():
        for line in DIFFICULTY_FILE.read_text(encoding="utf-8").splitlines():
            parts = line.strip().split()
            if len(parts) == 2:
                diff_map[parts[0]] = parts[1]
    return diff_map


def main() -> None:
    WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)

    frame = build_frame()
    print(f"Reconstructed frame size: {len(frame)} (expected 232)")
    assert len(frame) == 232, (
        f"Frame reconstruction mismatch: got {len(frame)}, expected 232. "
        "Do not proceed -- this must match F_v2.1 exactly."
    )

    # Integrity check: every program_id in the frozen v2.1 final-30 manifest
    # must appear in this reconstructed frame (it is a subset of F_v2.1).
    v2_1_data = json.loads(V2_1_MANIFEST.read_text(encoding="utf-8"))
    v2_1_program_ids = {p["program_id"] for p in v2_1_data["programs"]}
    frame_program_ids = {pid for _, pid in frame}
    missing = v2_1_program_ids - frame_program_ids
    if missing:
        raise SystemExit(
            f"FATAL: {len(missing)} v2.1 final-sample program_id(s) are NOT "
            f"in the reconstructed frame: {sorted(missing)}. Frame "
            "reconstruction does not match v2.1 -- aborting without writing "
            "anything."
        )
    print(
        f"Integrity check PASSED: all {len(v2_1_program_ids)} v2.1 final-sample "
        "program_ids are present in the reconstructed 232-program frame."
    )

    diff_map = load_difficulty_map()

    records = []
    for idx, (task_id, program_id) in enumerate(frame, start=1):
        buggy_path = CODE_DIR / task_id / "Python" / program_id / "faultyVersion.py"
        src = buggy_path.read_text(encoding="utf-8", errors="ignore")
        contest, _, problem_letter = task_id.rpartition("_")
        record = {
            "index": idx,
            "program_id": program_id,
            "task_id": task_id,
            "contest": contest,
            "problem_letter": problem_letter,
            "difficulty": diff_map.get(task_id, "unknown"),
            "atcoder_url": f"https://atcoder.jp/contests/{contest}/tasks/{task_id}",
            "loc": len(src.splitlines()),
            "buggy_source": src,
        }
        records.append(record)

    with open(OUT_JSONL, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"Wrote {len(records)} blinded records to {OUT_JSONL}")

    frame_manifest = {
        "frame_size": len(frame),
        "sampling_seed": SAMPLING_SEED,
        "built_at": datetime.now(timezone.utc).isoformat(),
        "reconstruction_procedure": (
            "Identical to scripts/package_final_sample_v2_1.py steps 1-3: "
            "load dynamic_test_eligibility_v2_1.csv, filter eligible=True, "
            "group by task_id, then random.Random(20260910) with progs[0] "
            "for singleton tasks or rng.choice(progs) for multi-candidate "
            "tasks, iterating sorted(task_id) order."
        ),
        "source_file_sha256": {
            "data/manifests/dynamic_test_eligibility_v2_1.csv": sha256_of(DYNAMIC_ELIG_FILE),
        },
        "v2_1_final_sample_subset_check": "PASS -- all 30 v2.1 program_ids present in frame",
        "fields_deliberately_excluded_from_every_record": [
            "faulty_lines",
            "fixed.py / fixed source text",
            "buggy-to-fixed diff",
            "pilot/pattern_priors.json content",
            "pilot/v2/generic_placebo_prior.json content",
            "previous (v2.0/v2.1) pattern_label",
            "previous pattern_source (\"AST rule\")",
            "previous pattern_confidence / pattern_note",
            "previous selection_rank / class allocation",
            "whether this program was in the old final 30",
            "any LLM localization output",
        ],
    }
    OUT_MANIFEST.write_text(json.dumps(frame_manifest, indent=2), encoding="utf-8")
    print(f"Wrote frame manifest to {OUT_MANIFEST}")


if __name__ == "__main__":
    main()
