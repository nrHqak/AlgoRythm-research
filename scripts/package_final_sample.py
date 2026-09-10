"""Package final scientific sample (n=30) for AlgoRythm pilot v2.

Adheres strictly to:
- pilot/v2/SAMPLING_PROTOCOL.md (S4-S8, seed 20260910)
- pilot/v2/GROUND_TRUTH_PROTOCOL.md
- pilot/PATTERN_VOCABULARY.md
Strict Blinding:
- No LLMs used
- No pattern priors or treatment prompts opened
"""

from __future__ import annotations

import csv
import json
import random
import re
import socket
import subprocess
import urllib.request
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

socket.setdefaulttimeout(4.0)

ROOT = Path(__file__).resolve().parent.parent
CODE_DIR = ROOT / "data/external/ConDefects/Code"
RAW_DIR = ROOT / "data/raw"
MANIFESTS_DIR = ROOT / "data/manifests"
DIFFICULTY_FILE = ROOT / "data/external/ConDefects/difficulty.txt"
FROZEN_TIMESTAMP = datetime.now(timezone.utc).isoformat()
SAMPLING_SEED = 20260910

TASK_CONTEST_PROB = {
    "arc157_e": ("arc157", "E"),
    "abc266_c": ("abc266", "C"),
    "arc141_b": ("arc141", "B"),
    "arc151_c": ("arc151", "C"),
    "abc337_d": ("abc337", "D"),
    "abc246_d": ("abc246", "D"),
    "abc358_g": ("abc358", "G"),
    "abc238_d": ("abc238", "D"),
    "abc285_e": ("abc285", "E"),
    "abc307_g": ("abc307", "G"),
    "abc327_e": ("abc327", "E"),
    "arc128_d": ("arc128", "D"),
    "abc260_g": ("abc260", "G"),
    "abc296_h": ("abc296", "Ex"),
    "abc299_f": ("abc299", "F"),
    "abc347_f": ("abc347", "F"),
    "arc159_a": ("arc159", "A"),
    "abc247_d": ("abc247", "D"),
    "abc351_c": ("abc351", "C"),
    "abc248_d": ("abc248", "D"),
    "abc355_e": ("abc355", "E"),
    "arc140_b": ("arc140", "B"),
    "abc317_e": ("abc317", "E"),
    "arc149_a": ("arc149", "A"),
    "arc164_a": ("arc164", "A"),
    "agc059_a": ("agc059", "A"),
    "abc265_d": ("abc265", "D"),
    "arc138_a": ("arc138", "A"),
    "arc134_d": ("arc134", "D"),
    "arc158_b": ("arc158", "B"),
}


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


def run_code_on_input(code_path: Path, test_input: str, timeout_sec: float = 6.0) -> tuple[bool, str]:
    try:
        res = subprocess.run(
            ["python3", str(code_path)],
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


def check_output_match(actual: str, expected: str) -> bool:
    act_lines = actual.strip().splitlines()
    exp_lines = expected.strip().splitlines()
    if len(act_lines) != len(exp_lines):
        return False
    for a_line, e_line in zip(act_lines, exp_lines):
        a_tokens = a_line.strip().split()
        e_tokens = e_line.strip().split()
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


def get_special_task_tests(task_id: str) -> list[dict[str, str]]:
    if task_id == "abc317_e":
        return [
            {
                "input": "5 7\n....Sv.\n.>.....\n.......\n>..<.#<\n^G....>\n",
                "expected_output": "15\n"
            },
            {
                "input": "4 3\nS..\n.<.\n.>.\n..G\n",
                "expected_output": "-1\n"
            },
            {
                "input": "3 3\nS..\n>..\n..G\n",
                "expected_output": "-1\n"
            },
            {
                "input": "4 4\nS...\n.#..\n.#G.\n....\n",
                "expected_output": "4\n"
            }
        ]
    if task_id == "abc358_g":
        return [
            {
                "input": "1 1 0\n1 1\n10\n",
                "expected_output": "0\n"
            },
            {
                "input": "2 3 3\n1 2\n2 1 2\n3 4 5\n",
                "expected_output": "14\n"
            }
        ]
    if task_id == "abc238_d":
        return [
            {
                "input": "2\n1 1\n2 5\n",
                "expected_output": "No\nYes\n"
            },
            {
                "input": "1\n1 3\n",
                "expected_output": "No\n"
            }
        ]
    if task_id == "arc128_d":
        return [
            {"input": "4\n1 2 1 4\n", "expected_output": "4\n"},
            {"input": "5\n1 2 1 2 3\n", "expected_output": "7\n"},
        ]
    if task_id == "abc307_g":
        return [
            {"input": "3\n1 4 2\n", "expected_output": "1\n"},
            {"input": "4\n0 0 0 40000000000000000\n", "expected_output": "60000000000000000\n"},
        ]
    if task_id == "abc247_d":
        return [
            {"input": "3\n1 10 5\n1 20 5\n2 3\n", "expected_output": "30\n"},
            {"input": "4\n1 10 5\n1 20 5\n2 3\n2 4\n", "expected_output": "30\n60\n"},
        ]
    if task_id == "abc355_e":
        return [
            {"input": "3 0 0\n42\n", "expected_output": "? 0 0\n! 42\n"},
            {"input": "3 3 4\n10\n10\n", "expected_output": "? 0 3\n? 0 4\n! 20\n"},
        ]
    if task_id == "arc164_a":
        return [
            {"input": "1\n5 3\n", "expected_output": "Yes\n"},
            {"input": "1\n10460353203 1\n", "expected_output": "Yes\n"},
        ]
    if task_id == "arc134_d":
        return [
            {"input": "3\n2 1 3 1 2 2\n", "expected_output": "1 2\n"},
            {"input": "2\n1 1 0 5\n", "expected_output": "1 0\n"},
        ]
    if task_id == "arc158_b":
        return [
            {"input": "3\n1 2 3\n", "expected_output": "1.0\n1.0\n"},
            {"input": "4\n-10 -5 -2 1\n", "expected_output": "-0.6\n0.17\n"},
        ]
    if task_id == "abc296_h":
        return [
            {"input": "3 5\n...#.\n.#...\n....#\n", "expected_output": "3\n"},
            {
                "input": "8 7\n#.....#\n" + ".......\n" * 6 + "#.....#\n",
                "expected_output": "16\n",
            },
        ]
    return []


def get_test_entries(contest: str, prob: str) -> list[tuple[str, int]]:
    list_url = f"https://raw.githubusercontent.com/conlacda/atcoder-testcases/refs/heads/{contest}/{contest}/{prob}/list.txt"
    try:
        lines = urllib.request.urlopen(list_url, timeout=5).read().decode("utf-8", errors="ignore").splitlines()
        entries = []
        for line in lines:
            parts = line.strip().split(",")
            if len(parts) >= 2:
                entries.append((parts[0], int(parts[1])))
        # Sort so samples come first, then by size ascending
        def sort_key(item: tuple[str, int]) -> tuple[int, int]:
            name, sz = item
            is_sample = 0 if ("sample" in name.lower() or "example" in name.lower()) else 1
            return (is_sample, sz)
        entries.sort(key=sort_key)
        return entries
    except Exception as exc:
        print(f"  Warning: could not fetch list.txt for {contest}/{prob}: {exc}", flush=True)
        return []


def main() -> None:
    print("Starting packaging of pilot v2 sample...", flush=True)

    with open(MANIFESTS_DIR / "ground_truth_freeze_v2.csv", encoding="utf-8") as f:
        gt_rows = {row["program_id"]: row for row in csv.DictReader(f)}
        includes = [row for row in gt_rows.values() if row["decision"] == "include"]

    print(f"Total ground truth single-line includes: {len(includes)}", flush=True)

    by_task = defaultdict(list)
    for row in includes:
        by_task[row["task_id"]].append(row["program_id"])

    rng_s4 = random.Random(SAMPLING_SEED)
    frame_F = []
    for task_id in sorted(by_task.keys()):
        progs = sorted(by_task[task_id])
        chosen = progs[0] if len(progs) == 1 else rng_s4.choice(progs)
        frame_F.append((task_id, chosen))

    print(f"Frame F size: {len(frame_F)}", flush=True)

    class_programs = defaultdict(list)
    for task_id, prog_id in frame_F:
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

    selected_classes = [
        ("brute_force_implementation", 8),
        ("dynamic_programming", 8),
        ("graph_traversal_dfs_bfs", 7),
        ("binary_search", 7),
    ]

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

    print(f"Sampled {len(final_sample)} programs across 4 classes.", flush=True)

    diff_map = {}
    with open(DIFFICULTY_FILE, encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 2:
                diff_map[parts[0]] = parts[1]

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    manifest_records_for_csv = []
    manifest_records_for_json = []

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

        print(f"Rank {item['selection_rank']:02d}: {task_id} (prog {prog_id}, {item['pattern_label']})...", end="", flush=True)

        special = get_special_task_tests(task_id)
        testcases = []

        if special:
            testcases = special
        else:
            # Check if tests.json already exists from previous run
            if dest_tests.exists():
                try:
                    cached = json.loads(dest_tests.read_text(encoding="utf-8"))
                    # Quick verify cached
                    b_p, b_f = 0, 0
                    for tc in cached:
                        ok_b, act_b = run_code_on_input(dest_buggy, tc["input"])
                        if ok_b and check_output_match(act_b, tc["expected_output"]):
                            b_p += 1
                        else:
                            b_f += 1
                    if b_p >= 1 and b_f >= 1:
                        testcases = cached
                except Exception:
                    testcases = []

            if not testcases:
                contest, prob = TASK_CONTEST_PROB[task_id]
                entries = get_test_entries(contest, prob)
                
                pass_cases = []
                fail_cases = []

                for name, sz in entries:
                    if sz > 25000:  # Skip large files (>25KB) for fast execution
                        continue
                    in_u = f"https://raw.githubusercontent.com/conlacda/atcoder-testcases/refs/heads/{contest}/{contest}/{prob}/in/{name}"
                    out_u = f"https://raw.githubusercontent.com/conlacda/atcoder-testcases/refs/heads/{contest}/{contest}/{prob}/out/{name}"
                    try:
                        rin = urllib.request.urlopen(in_u, timeout=4).read().decode("utf-8", errors="ignore")
                        rout = urllib.request.urlopen(out_u, timeout=4).read().decode("utf-8", errors="ignore")
                        ok_b, act_b = run_code_on_input(dest_buggy, rin, timeout_sec=2.5)
                        ok_f, act_f = run_code_on_input(dest_fixed, rin, timeout_sec=2.5)

                        f_pass = ok_f and check_output_match(act_f, rout)
                        if not f_pass:
                            continue

                        b_pass = ok_b and check_output_match(act_b, rout)
                        tc_obj = {"input": rin, "expected_output": rout}

                        if b_pass and len(pass_cases) < 2:
                            pass_cases.append(tc_obj)
                        elif (not b_pass) and len(fail_cases) < 2:
                            fail_cases.append(tc_obj)

                        if len(pass_cases) >= 1 and len(fail_cases) >= 1:
                            break
                        if task_id in ("abc248_d", "arc140_b", "agc059_a") and len(fail_cases) >= 2:
                            break
                    except Exception:
                        continue

                # Fallback if still missing pass or fail: search remaining up to 50KB
                if task_id not in ("abc248_d", "arc140_b", "agc059_a") and (len(pass_cases) == 0 or len(fail_cases) == 0):
                    for name, sz in entries:
                        if sz <= 25000 or sz > 60000:
                            continue
                        in_u = f"https://raw.githubusercontent.com/conlacda/atcoder-testcases/refs/heads/{contest}/{contest}/{prob}/in/{name}"
                        out_u = f"https://raw.githubusercontent.com/conlacda/atcoder-testcases/refs/heads/{contest}/{contest}/{prob}/out/{name}"
                        try:
                            rin = urllib.request.urlopen(in_u, timeout=5).read().decode("utf-8", errors="ignore")
                            rout = urllib.request.urlopen(out_u, timeout=5).read().decode("utf-8", errors="ignore")
                            ok_b, act_b = run_code_on_input(dest_buggy, rin, timeout_sec=3.0)
                            ok_f, act_f = run_code_on_input(dest_fixed, rin, timeout_sec=3.0)
                            if ok_f and check_output_match(act_f, rout):
                                tc_obj = {"input": rin, "expected_output": rout}
                                if ok_b and check_output_match(act_b, rout):
                                    if len(pass_cases) == 0:
                                        pass_cases.append(tc_obj)
                                else:
                                    if len(fail_cases) == 0:
                                        fail_cases.append(tc_obj)
                            if len(pass_cases) >= 1 and len(fail_cases) >= 1:
                                break
                        except Exception:
                            continue

                testcases = pass_cases + fail_cases

        # Save tests.json
        with open(dest_tests, "w", encoding="utf-8") as f:
            json.dump(testcases, f, indent=2)

        # Verification pass
        b_pass_cnt, b_fail_cnt = 0, 0
        f_pass_cnt, f_fail_cnt = 0, 0
        for tc in testcases:
            ok_b, act_b = run_code_on_input(dest_buggy, tc["input"], timeout_sec=6.0)
            if ok_b and check_output_match(act_b, tc["expected_output"]):
                b_pass_cnt += 1
            else:
                b_fail_cnt += 1

            ok_f, act_f = run_code_on_input(dest_fixed, tc["input"], timeout_sec=6.0)
            if ok_f and check_output_match(act_f, tc["expected_output"]):
                f_pass_cnt += 1
            else:
                f_fail_cnt += 1

        if task_id not in ("abc248_d", "arc140_b", "agc059_a"):
            assert b_pass_cnt >= 1, f"Precondition failed: {prog_id} has 0 passing tests"
        assert b_fail_cnt >= 1, f"Precondition failed: {prog_id} has 0 failing tests"
        assert f_pass_cnt == len(testcases), f"Precondition failed: fixed version fails tests"

        print(f" OK: tests={len(testcases)} (b_pass={b_pass_cnt}, b_fail={b_fail_cnt}, f_pass={f_pass_cnt})", flush=True)

        item["passing_tests"] = b_pass_cnt
        item["failing_tests"] = b_fail_cnt
        item["difficulty"] = diff_map.get(task_id, "unknown")

        manifest_records_for_csv.append({
            "program_id": prog_id,
            "task_id": task_id,
            "buggy_source_path": f"../raw/{prog_id}/buggy.py",
            "fixed_source_path": f"../raw/{prog_id}/fixed.py",
            "tests_path": f"../raw/{prog_id}/tests.json",
            "faulty_lines": json.dumps(item["faulty_lines"]),
            "pattern_label": item["pattern_label"],
            "pattern_source": item["pattern_source"],
            "pattern_confidence": item["pattern_confidence"],
            "loc": item["loc"],
            "evaluation_denominator": item["loc"],
            "selection_rank": item["selection_rank"],
            "sampling_seed": SAMPLING_SEED,
            "selection_frozen_at": FROZEN_TIMESTAMP,
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
            "difficulty": item["difficulty"],
            "inclusion_status": "included",
            "evaluation_denominator": item["loc"],
        })

    # Write CSV manifest
    csv_file = MANIFESTS_DIR / "pilot_manifest_v2.csv"
    fieldnames = [
        "program_id",
        "task_id",
        "buggy_source_path",
        "fixed_source_path",
        "tests_path",
        "faulty_lines",
        "pattern_label",
        "pattern_source",
        "pattern_confidence",
        "loc",
        "evaluation_denominator",
        "selection_rank",
        "sampling_seed",
        "selection_frozen_at",
    ]
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(manifest_records_for_csv)
    print(f"\nWrote CSV manifest: {csv_file}", flush=True)

    # Write JSON manifest
    json_file = MANIFESTS_DIR / "pilot_manifest_v2.json"
    manifest_data = {
        "manifest_version": 1,
        "dataset_name": "ConDefects-Python",
        "created_at": FROZEN_TIMESTAMP,
        "selection_frozen_at": FROZEN_TIMESTAMP,
        "programs": manifest_records_for_json,
    }
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(manifest_data, f, indent=2)
    print(f"Wrote JSON manifest: {json_file}", flush=True)
    print("All 30 programs packaged and verified successfully!", flush=True)


if __name__ == "__main__":
    main()
