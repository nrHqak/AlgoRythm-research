#!/usr/bin/env python3
"""
Package and freeze the corrected Pilot v2.1 sample (n=30)
under original SAMPLING_PROTOCOL.md v2 rules:
- Pre-dedup dynamic pass/fail filter applied
- Task deduplication on eligible pool using seed 20260910 -> Frame F_v2_1 (size 232)
- Class ranking per §6:
    1. brute_force_implementation (count=94, quota=8)
    2. dynamic_programming (count=45, quota=8)
    3. binary_search (count=22, quota=7)
    4. sorting_based (count=21, quota=7)
- Seeded draw using seed 20260910
- Packaging into data/raw/<program_id>/
- Writing pilot_manifest_v2_1.json and pilot_manifest_v2_1.csv
"""
from __future__ import annotations

import csv
import json
import random
import re
import subprocess
import sys
from collections import defaultdict, Counter
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CODE_DIR = REPO_ROOT / "data" / "external" / "ConDefects" / "Code"
DIFFICULTY_FILE = REPO_ROOT / "data" / "external" / "ConDefects" / "difficulty.txt"
GT_FREEZE_FILE = REPO_ROOT / "data" / "manifests" / "ground_truth_freeze_v2.csv"
DYNAMIC_ELIG_FILE = REPO_ROOT / "data" / "manifests" / "dynamic_test_eligibility_v2_1.csv"
CACHE_TESTS_DIR = REPO_ROOT / "data" / "cache" / "testcases"
RAW_DIR = REPO_ROOT / "data" / "raw"
MANIFESTS_DIR = REPO_ROOT / "data" / "manifests"

SAMPLING_SEED = 20260910


def check_output_match(actual: str, expected: str) -> bool:
    act_lines = [l.strip() for l in actual.strip().splitlines() if l.strip()]
    exp_lines = [l.strip() for l in expected.strip().splitlines() if l.strip()]
    if len(act_lines) != len(exp_lines):
        return False
    for a_line, e_line in zip(act_lines, exp_lines):
        a_tokens = a_line.split()
        e_tokens = e_line.split()
        if len(a_tokens) != len(e_tokens):
            return False
        for a, e in zip(a_tokens, e_tokens):
            if a == e:
                continue
            try:
                fa = float(a)
                fe = float(e)
                if abs(fa - fe) < 1e-6 or (fe != 0 and abs(fa - fe) / abs(fe) < 1e-6):
                    continue
            except ValueError:
                pass
            return False
    return True


def run_code_on_input(code_path: Path, test_input: str, timeout_sec: float = 4.0) -> tuple[bool, str]:
    try:
        res = subprocess.run(
            [sys.executable, str(code_path)],
            input=test_input,
            capture_output=True,
            text=True,
            timeout=timeout_sec,
        )
        if res.returncode != 0:
            return False, f"Non-zero exit {res.returncode}"
        return True, res.stdout
    except subprocess.TimeoutExpired:
        return False, "TimeoutExpired"
    except Exception as exc:
        return False, f"Error: {exc}"


def classify_program(src: str, task_id: str) -> tuple[str, str, str, str]:
    has_dp_table = bool(re.search(r"\bdp\b\s*=\s*\[", src) or re.search(r"\bmemo\b\s*=", src) or re.search(r"\[\s*\[\s*0\b", src))
    has_bfs_queue = bool(re.search(r"\b(deque|queue)\b", src) and re.search(r"\b(popleft|append|get)\b", src))
    has_graph_adj = bool(re.search(r"\b(adj|edges|graph|tree|G)\b\s*=\s*(\[|defaultdict)", src))
    has_visited = bool(re.search(r"\b(visited|seen|dist)\b\s*=\s*(\[|set|\{)", src))
    has_bisect = bool(re.search(r"\b(bisect|bisect_left|bisect_right)\b", src))
    has_manual_bs = bool(re.search(r"while\s+([a-zA-Z0-9_]+)\s*(<=|<)\s*([a-zA-Z0-9_]+)", src) and re.search(r"//\s*2", src))
    has_accumulate = bool(re.search(r"\baccumulate\b", src) or re.search(r"\b(pref|cumsum|acc|prefix)\b\s*=\s*\[", src))
    has_counter = bool(re.search(r"\bCounter\(", src) or re.search(r"\bdefaultdict\(int\)", src))
    has_heap = bool(re.search(r"\bheapq\b", src) or re.search(r"\bheappop\b", src) or re.search(r"\bheappush\b", src))
    has_dsu = bool(re.search(r"\b(union|find|dsu|UnionFind)\b", src, re.I) and "parent" in src)
    has_segtree = bool(re.search(r"\b(segtree|fenwick|bit)\b", src, re.I))
    has_itertools = bool(re.search(r"\b(permutations|combinations|product)\b", src))
    has_two_pointers = bool(re.search(r"while\s+[a-zA-Z0-9_]+\s*<\s*[a-zA-Z0-9_]+", src) and ("l +=" in src or "left +=" in src or "i +=" in src) and ("r -=" in src or "right -=" in src or "j -=" in src))
    has_simulation = bool(re.search(r"\b(turn|step|move|dir|grid|board)\b", src, re.I) and ("dx" in src or "dy" in src or "for _ in range" in src))

    if has_dsu or has_segtree:
        return "outside_vocabulary", "AST rule", "low", "pattern outside frozen vocabulary v1 (DSU/SegTree)"
    if has_dp_table:
        return "dynamic_programming", "AST rule", "high", "DP table and recurrence structure"
    if has_bfs_queue or (has_graph_adj and has_visited):
        return "graph_traversal_dfs_bfs", "AST rule", "high", "Graph/grid traversal with visited tracking"
    if has_bisect or has_manual_bs:
        return "binary_search", "AST rule", "high", "Monotonic search space halving"
    if has_accumulate:
        return "prefix_sums", "AST rule", "medium", "Cumulative prefix sum precomputation"
    if has_heap:
        return "greedy", "AST rule", "medium", "Priority queue greedy selection"
    if has_counter:
        return "hash_map_counting", "AST rule", "medium", "Hash map / Counter frequency tracking"
    if has_two_pointers:
        return "two_pointers", "AST rule", "medium", "Two converging/monotonic pointer scan"
    if ".sort(" in src or "sorted(" in src:
        return "sorting_based", "AST rule", "medium", "Sort-then-scan approach"
    if has_itertools:
        return "brute_force_implementation", "AST rule", "high", "Direct search space enumeration"
    if has_simulation:
        return "simulation", "AST rule", "medium", "Step-by-step process simulation"
    return "brute_force_implementation", "AST rule", "high", "Direct implementation / exhaustive loops"


def main() -> None:
    print("=== Starting Packaging and Freezing for Pilot v2.1 ===", flush=True)

    # 1. Load frozen ground truth v2
    with open(GT_FREEZE_FILE, encoding="utf-8") as f:
        gt_rows = {row["program_id"]: row for row in csv.DictReader(f)}

    # 2. Load dynamic test eligibility v2.1
    with open(DYNAMIC_ELIG_FILE, encoding="utf-8") as f:
        dyn_rows = list(csv.DictReader(f))
    eligible_progs = [r for r in dyn_rows if r["eligible"] == "True"]
    print(f"Eligible single-line candidates: {len(eligible_progs)}", flush=True)

    # 3. Rebuild Task-Independent Frame F_v2_1
    by_task = defaultdict(list)
    for r in eligible_progs:
        by_task[r["task_id"]].append(r["program_id"])

    rng_s4 = random.Random(SAMPLING_SEED)
    frame_F_v2_1 = []
    for task_id in sorted(by_task.keys()):
        progs = sorted(by_task[task_id])
        chosen = progs[0] if len(progs) == 1 else rng_s4.choice(progs)
        frame_F_v2_1.append((task_id, chosen))

    print(f"Corrected Frame F_v2_1 size: {len(frame_F_v2_1)}", flush=True)

    # 4. Pattern classification
    class_programs = defaultdict(list)
    for task_id, prog_id in frame_F_v2_1:
        buggy_file = CODE_DIR / task_id / "Python" / prog_id / "faultyVersion.py"
        src = buggy_file.read_text(encoding="utf-8", errors="ignore")
        label, source, conf, note = classify_program(src, task_id)
        class_programs[label].append({
            "task_id": task_id,
            "program_id": prog_id,
            "pattern_label": label,
            "pattern_source": source,
            "pattern_confidence": conf,
            "pattern_note": note,
            "loc": len(src.splitlines()),
            "faulty_lines": json.loads(gt_rows[prog_id]["faulty_lines"]),
        })

    class_counts = {k: len(v) for k, v in class_programs.items()}
    print("Class counts in F_v2_1:", json.dumps(class_counts, indent=2), flush=True)

    # Rank classes with >= 7 programs, descending count, tie-break by PATTERN_VOCABULARY.md
    vocab_order = [
        "two_pointers", "sliding_window", "binary_search", "prefix_sums",
        "dynamic_programming", "greedy", "graph_traversal_dfs_bfs", "sorting_based",
        "hash_map_counting", "brute_force_implementation", "intervals", "simulation"
    ]
    eligible_classes = [c for c in class_counts.keys() if class_counts[c] >= 7 and c != "outside_vocabulary"]
    eligible_classes.sort(key=lambda c: (-class_counts[c], vocab_order.index(c) if c in vocab_order else 999))
    print(f"Ranked eligible classes (>= 7): {eligible_classes}", flush=True)

    selected_classes = [
        (eligible_classes[0], 8),
        (eligible_classes[1], 8),
        (eligible_classes[2], 7),
        (eligible_classes[3], 7),
    ]
    print(f"Selected top 4 classes & allocations: {selected_classes}", flush=True)

    # 5. Seeded final draw (seed=20260910)
    rng_s8 = random.Random(SAMPLING_SEED)
    final_sample = []
    rank = 1
    for cls_name, count in selected_classes:
        pool = sorted(class_programs[cls_name], key=lambda x: x["program_id"])
        drawn = rng_s8.sample(pool, count)
        for item in drawn:
            item["selection_rank"] = rank
            rank += 1
            final_sample.append(item)

    print(f"Drawn final sample of {len(final_sample)} programs.", flush=True)

    # 6. Difficulty lookup
    diff_map = {}
    with open(DIFFICULTY_FILE, encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 2:
                diff_map[parts[0]] = parts[1]

    # 7. Package each program into data/raw/<program_id>/
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    manifest_records_for_csv = []
    manifest_records_for_json = []

    frozen_timestamp = datetime.now(timezone.utc).isoformat()

    for item in final_sample:
        prog_id = item["program_id"]
        task_id = item["task_id"]
        prog_dir = RAW_DIR / prog_id
        prog_dir.mkdir(parents=True, exist_ok=True)

        orig_buggy = CODE_DIR / task_id / "Python" / prog_id / "faultyVersion.py"
        orig_fixed = CODE_DIR / task_id / "Python" / prog_id / "correctVersion.py"

        dest_buggy = prog_dir / "buggy.py"
        dest_fixed = prog_dir / "fixed.py"
        dest_tests = prog_dir / "tests.json"

        dest_buggy.write_text(orig_buggy.read_text(encoding="utf-8", errors="ignore"), encoding="utf-8")
        dest_fixed.write_text(orig_fixed.read_text(encoding="utf-8", errors="ignore"), encoding="utf-8")

        # Load verified testcases from cache
        cache_tests_file = CACHE_TESTS_DIR / f"{task_id}.json"
        testcases = json.loads(cache_tests_file.read_text(encoding="utf-8"))
        dest_tests.write_text(json.dumps(testcases, indent=2), encoding="utf-8")

        # Verification execution pass
        b_pass_cnt, b_fail_cnt = 0, 0
        f_pass_cnt, f_fail_cnt = 0, 0
        for tc in testcases:
            ok_b, act_b = run_code_on_input(dest_buggy, tc["input"])
            if ok_b and check_output_match(act_b, tc["expected_output"]):
                b_pass_cnt += 1
            else:
                b_fail_cnt += 1

            ok_f, act_f = run_code_on_input(dest_fixed, tc["input"])
            if ok_f and check_output_match(act_f, tc["expected_output"]):
                f_pass_cnt += 1
            else:
                f_fail_cnt += 1

        assert b_pass_cnt >= 1, f"Program {prog_id} violates buggy_pass_count >= 1 (got {b_pass_cnt})"
        assert b_fail_cnt >= 1, f"Program {prog_id} violates buggy_fail_count >= 1 (got {b_fail_cnt})"
        assert f_fail_cnt == 0, f"Program {prog_id} violates fixed_fail_count == 0 (got {f_fail_cnt})"

        print(
            f"Rank {item['selection_rank']:02d}: {task_id} (prog {prog_id}, {item['pattern_label']}) "
            f"OK: tests={len(testcases)} (b_pass={b_pass_cnt}, b_fail={b_fail_cnt}, f_pass={f_pass_cnt})",
            flush=True,
        )

        manifest_records_for_csv.append({
            "program_id": prog_id,
            "task_id": task_id,
            "buggy_source_path": f"../raw/{prog_id}/buggy.py",
            "fixed_source_path": f"../raw/{prog_id}/fixed.py",
            "tests_path": f"../raw/{prog_id}/tests.json",
            "faulty_lines": str(item["faulty_lines"]),
            "pattern_label": item["pattern_label"],
            "pattern_source": item["pattern_source"],
            "pattern_confidence": item["pattern_confidence"],
            "loc": item["loc"],
            "evaluation_denominator": item["loc"],
            "selection_rank": item["selection_rank"],
            "sampling_seed": SAMPLING_SEED,
            "selection_frozen_at": frozen_timestamp,
        })

        manifest_records_for_json.append({
            "program_id": prog_id,
            "task_id": task_id,
            "buggy_source_path": f"../raw/{prog_id}/buggy.py",
            "fixed_source_path": f"../raw/{prog_id}/fixed.py",
            "tests_path": f"../raw/{prog_id}/tests.json",
            "faulty_lines": item["faulty_lines"],
            "pattern_label": item["pattern_label"],
            "pattern_source": item["pattern_source"],
            "loc": item["loc"],
            "difficulty": diff_map.get(task_id, "unknown"),
            "inclusion_status": "included",
            "evaluation_denominator": item["loc"],
        })

    # Write CSV manifest
    csv_path = MANIFESTS_DIR / "pilot_manifest_v2_1.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "program_id", "task_id", "buggy_source_path", "fixed_source_path", "tests_path",
            "faulty_lines", "pattern_label", "pattern_source", "pattern_confidence", "loc",
            "evaluation_denominator", "selection_rank", "sampling_seed", "selection_frozen_at",
        ])
        writer.writeheader()
        writer.writerows(manifest_records_for_csv)
    print(f"Wrote CSV manifest: {csv_path}", flush=True)

    # Write JSON manifest
    json_path = MANIFESTS_DIR / "pilot_manifest_v2_1.json"
    manifest_data = {
        "manifest_version": 1,
        "dataset_name": "ConDefects-Python",
        "created_at": frozen_timestamp,
        "selection_frozen_at": frozen_timestamp,
        "programs": manifest_records_for_json,
    }
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(manifest_data, f, indent=2)
    print(f"Wrote JSON manifest: {json_path}", flush=True)

    print("All 30 v2.1 programs packaged, verified, and frozen successfully!", flush=True)


if __name__ == "__main__":
    main()
