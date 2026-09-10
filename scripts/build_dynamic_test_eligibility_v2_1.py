#!/usr/bin/env python3
"""
Step 2: Build dynamic test eligibility for all 1,008 single-line ground-truth candidates.
Evaluates:
- buggy_pass_count >= 1
- buggy_fail_count >= 1
- fixed_fail_count == 0
- fixed_pass_count >= 1
"""
from __future__ import annotations

import html
import json
import os
import re
import subprocess
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent
CODE_DIR = REPO_ROOT / "data" / "external" / "ConDefects" / "Code"
GT_FREEZE_FILE = REPO_ROOT / "data" / "manifests" / "ground_truth_freeze_v2.csv"
OUTPUT_CSV = REPO_ROOT / "data" / "manifests" / "dynamic_test_eligibility_v2_1.csv"
CACHE_DIR = REPO_ROOT / "data" / "cache" / "testcases"

CACHE_DIR.mkdir(parents=True, exist_ok=True)


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


def run_code_on_input(code_path: Path, test_input: str, timeout_sec: float = 3.0) -> tuple[bool, str]:
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


def fetch_atcoder_html_samples(task_id: str) -> list[dict[str, str]]:
    contest = task_id.split("_")[0]
    url = f"https://atcoder.jp/contests/{contest}/tasks/{task_id}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            content = resp.read().decode("utf-8", errors="ignore")
    except Exception:
        return []

    in_blocks = re.findall(r"<h3>Sample Input \d+</h3><pre>(.*?)</pre>", content, re.DOTALL)
    out_blocks = re.findall(r"<h3>Sample Output \d+</h3><pre>(.*?)</pre>", content, re.DOTALL)

    samples = []
    for inp, out in zip(in_blocks, out_blocks):
        inp_clean = html.unescape(inp).replace("\r\n", "\n")
        out_clean = html.unescape(out).replace("\r\n", "\n")
        samples.append({"input": inp_clean, "expected_output": out_clean})
    return samples


def get_task_testcases(task_id: str) -> list[dict[str, str]]:
    cache_file = CACHE_DIR / f"{task_id}.json"
    if cache_file.exists():
        try:
            return json.loads(cache_file.read_text(encoding="utf-8"))
        except Exception:
            pass

    parts = task_id.split("_", 1)
    contest = parts[0]
    prob = parts[1]
    probs = [prob.upper(), prob.capitalize(), prob]
    if prob.lower() == "h":
        probs.insert(0, "Ex")

    entries = []
    resolved_prob = None

    # Try list.txt on atcoder-testcases
    for p in probs:
        url = f"https://raw.githubusercontent.com/conlacda/atcoder-testcases/refs/heads/{contest}/{contest}/{p}/list.txt"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=4) as resp:
                lines = resp.read().decode("utf-8", errors="ignore").splitlines()
            for line in lines:
                parts_l = line.strip().split(",")
                if len(parts_l) >= 2:
                    try:
                        entries.append((parts_l[0], int(parts_l[1])))
                    except ValueError:
                        pass
            if entries:
                resolved_prob = p
                break
        except Exception:
            pass

    testcases: list[dict[str, str]] = []

    if entries and resolved_prob:
        # Sort so samples/examples come first, then small system tests
        def sort_key(item: tuple[str, int]) -> tuple[int, int]:
            name, sz = item
            nl = name.lower()
            is_sample = 0 if any(k in nl for k in ("example", "sample", "hand", "000")) else 1
            return (is_sample, sz)

        sorted_entries = sorted(entries, key=sort_key)
        # Select up to 8 small cases (sz <= 30000)
        selected = []
        for name, sz in sorted_entries:
            if sz <= 30000:
                selected.append((name, sz))
            if len(selected) >= 8:
                break

        for name, _ in selected:
            in_u = f"https://raw.githubusercontent.com/conlacda/atcoder-testcases/refs/heads/{contest}/{contest}/{resolved_prob}/in/{name}"
            out_u = f"https://raw.githubusercontent.com/conlacda/atcoder-testcases/refs/heads/{contest}/{contest}/{resolved_prob}/out/{name}"
            try:
                req_in = urllib.request.Request(in_u, headers={"User-Agent": "Mozilla/5.0"})
                req_out = urllib.request.Request(out_u, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req_in, timeout=4) as rin, urllib.request.urlopen(req_out, timeout=4) as rout:
                    inp = rin.read().decode("utf-8", errors="ignore")
                    outp = rout.read().decode("utf-8", errors="ignore")
                    testcases.append({"input": inp, "expected_output": outp})
            except Exception:
                continue

    if not testcases:
        # Fallback to AtCoder HTML sample cases
        testcases = fetch_atcoder_html_samples(task_id)

    # Save to cache
    try:
        cache_file.write_text(json.dumps(testcases, indent=2), encoding="utf-8")
    except Exception:
        pass

    return testcases


def evaluate_single_program(row_tuple: tuple) -> dict:
    _, row = row_tuple
    prog_id = str(row["program_id"])
    task_id = str(row["task_id"])
    buggy_path = CODE_DIR / task_id / "Python" / prog_id / "faultyVersion.py"
    fixed_path = CODE_DIR / task_id / "Python" / prog_id / "correctVersion.py"
    now_iso = datetime.now(timezone.utc).isoformat()

    tests = get_task_testcases(task_id)
    if not tests:
        return {
            "program_id": prog_id,
            "task_id": task_id,
            "buggy_pass_count": 0,
            "buggy_fail_count": 0,
            "fixed_pass_count": 0,
            "fixed_fail_count": 0,
            "eligible": False,
            "exclusion_reason": "fails frozen pass/fail precondition",
            "timestamp": now_iso,
        }

    b_pass = 0
    b_fail = 0
    f_pass = 0
    f_fail = 0

    for tc in tests:
        inp = tc["input"]
        exp = tc["expected_output"]

        # Run fixed
        ok_f, act_f = run_code_on_input(fixed_path, inp, timeout_sec=2.5)
        if ok_f and check_output_match(act_f, exp):
            f_pass += 1
        else:
            f_fail += 1

        # Run buggy
        ok_b, act_b = run_code_on_input(buggy_path, inp, timeout_sec=2.5)
        if ok_b and check_output_match(act_b, exp):
            b_pass += 1
        else:
            b_fail += 1

    eligible = bool(b_pass >= 1 and b_fail >= 1 and f_fail == 0 and f_pass >= 1)
    reason = "" if eligible else "fails frozen pass/fail precondition"

    return {
        "program_id": prog_id,
        "task_id": task_id,
        "buggy_pass_count": b_pass,
        "buggy_fail_count": b_fail,
        "fixed_pass_count": f_pass,
        "fixed_fail_count": f_fail,
        "eligible": eligible,
        "exclusion_reason": reason,
        "timestamp": now_iso,
    }


def main():
    print("Loading frozen ground truth v2...")
    df = pd.read_csv(GT_FREEZE_FILE)
    inc = df[df["decision"] == "include"].copy()
    print(f"Total candidate programs to evaluate: {len(inc)}")

    # Pre-cache testcases concurrently
    unique_tasks = inc["task_id"].unique()
    print(f"Pre-caching testcases for {len(unique_tasks)} unique tasks with 25 threads...")
    with ThreadPoolExecutor(max_workers=25) as ex:
        list(ex.map(get_task_testcases, unique_tasks))
    print("Testcase caching complete.")

    print(f"Evaluating dynamic eligibility for all {len(inc)} programs...")
    rows_list = list(inc.iterrows())
    with ThreadPoolExecutor(max_workers=16) as ex:
        results = list(ex.map(evaluate_single_program, rows_list))

    res_df = pd.DataFrame(results)
    res_df.to_csv(OUTPUT_CSV, index=False)
    print(f"Wrote dynamic test eligibility to {OUTPUT_CSV}")

    eligible_count = res_df["eligible"].sum()
    excluded_count = len(res_df) - eligible_count
    eligible_tasks = res_df[res_df["eligible"]]["task_id"].nunique()
    print(f"=== Dynamic Test Eligibility Summary ===")
    print(f"Total evaluated: {len(res_df)}")
    print(f"Eligible programs: {eligible_count} ({eligible_count / len(res_df) * 100:.1f}%)")
    print(f"Excluded programs: {excluded_count} ({excluded_count / len(res_df) * 100:.1f}%)")
    print(f"Unique tasks among eligible programs: {eligible_tasks}")


if __name__ == "__main__":
    main()
