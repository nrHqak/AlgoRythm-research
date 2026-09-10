#!/usr/bin/env python3
"""Read-only Gate 7 verification; executes local test suites, never calls an LLM.

Run with the frozen Python 3.14.3 environment from the repository root.
Candidate source and execution output are not printed or written to the report.
"""
import csv
import difflib
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data/manifests/pilot_manifest_v2_1.json"
EXPECTED_HASH = "d53bcdc232f7e4daebca3248e53e060143a32e2638bb99959fda4c0db38e6ca3"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def matches(actual, expected):
    # Independently implement the acquisition/packaging comparator, including
    # its generic numeric tolerance. This is not an AtCoder judge emulator.
    a = [line.split() for line in actual.splitlines() if line.strip()]
    b = [line.split() for line in expected.splitlines() if line.strip()]
    if len(a) != len(b):
        return False
    for left, right in zip(a, b):
        if len(left) != len(right):
            return False
        for x, y in zip(left, right):
            if x == y:
                continue
            try:
                delta = abs(float(x) - float(y))
                if delta < 1e-6 or (float(y) != 0 and delta / abs(float(y)) < 1e-6):
                    continue
            except ValueError:
                pass
            return False
    return True


def execute(path, case, cwd):
    try:
        completed = subprocess.run(
            [sys.executable, str(path)], input=case["input"],
            capture_output=True, text=True, timeout=2.5, cwd=cwd,
            env={"PATH": os.defpath, "LANG": "en_US.UTF-8"},
        )
        if completed.returncode:
            return "nonzero_exit"
        return "pass" if matches(completed.stdout, case["expected_output"]) else "wrong_output"
    except subprocess.TimeoutExpired:
        return "timeout"


def main():
    report = {"audited_at": datetime.now(timezone.utc).isoformat(),
              "base_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
              "python": platform.python_version(), "timeout_seconds": 2.5,
              "manifest_sha256_before": digest(MANIFEST), "programs": [], "failures": []}
    failures = report["failures"]
    manifest = json.loads(MANIFEST.read_text())
    records = manifest["programs"]
    report["selection_frozen_at"] = manifest["selection_frozen_at"]
    report["record_count"] = len(records)
    report["unique_program_count"] = len({r["program_id"] for r in records})
    report["unique_task_count"] = len({r["task_id"] for r in records})
    for key in ("record_count", "unique_program_count", "unique_task_count"):
        if report[key] != 30:
            failures.append(key)
    if report["python"] != "3.14.3":
        failures.append("frozen Python version mismatch")
    if digest(MANIFEST) != EXPECTED_HASH:
        failures.append("manifest hash differs from handoff")
    vocabulary = set(re.findall(r"^\| \d+ \| `([^`]+)`", (ROOT / "pilot/PATTERN_VOCABULARY.md").read_text(), re.M))
    with (ROOT / "data/manifests/ground_truth_freeze_v2.csv").open() as handle:
        ground_truth = {r["program_id"]: r for r in csv.DictReader(handle)}
    with (ROOT / "data/manifests/dynamic_test_eligibility_v2_1.csv").open() as handle:
        eligibility = {r["program_id"]: r for r in csv.DictReader(handle)}
    paths_before = {}
    for record in records:
        pid = record["program_id"]
        paths = {key: (MANIFEST.parent / record[key]).resolve()
                 for key in ("buggy_source_path", "fixed_source_path", "tests_path")}
        item = {"program_id": pid, "task_id": record["task_id"],
                "faulty_lines": record["faulty_lines"], "pattern_label": record["pattern_label"],
                "checks": {}, "sha256": {}}
        report["programs"].append(item)
        checks = item["checks"]
        checks["paths_valid"] = all(p.is_file() and p.is_relative_to(ROOT / "data/raw") for p in paths.values())
        if not checks["paths_valid"]:
            failures.append(f"{pid}: paths invalid")
            continue
        for key, path in paths.items():
            paths_before[path] = digest(path)
            item["sha256"][key] = digest(path)
        buggy = paths["buggy_source_path"].read_text()
        fixed = paths["fixed_source_path"].read_text()
        loc = len(buggy.splitlines())
        item["loc"] = loc
        checks["loc_frozen_limits"] = 25 <= loc <= 300 and loc == record["loc"] == record["evaluation_denominator"]
        lines = record["faulty_lines"]
        checks["single_frozen_fault"] = (len(lines) == 1 and type(lines[0]) is int and 1 <= lines[0] <= loc
            and ground_truth[pid]["decision"] == "include"
            and json.loads(ground_truth[pid]["faulty_lines"]) == lines
            and ground_truth[pid]["task_id"] == record["task_id"])
        changes = [op for op in difflib.SequenceMatcher(None, buggy.splitlines(), fixed.splitlines()).get_opcodes() if op[0] != "equal"]
        checks["single_line_fix_matches_ground_truth"] = (len(changes) == 1 and changes[0][0] == "replace"
            and changes[0][2] - changes[0][1] == changes[0][4] - changes[0][3] == 1
            and [changes[0][1] + 1] == lines)
        checks["frozen_vocabulary"] = record["pattern_label"] in vocabulary
        checks["included_no_context"] = record["inclusion_status"] == "included" and not record.get("problem_context_path")
        try:
            compile(buggy, "buggy.py", "exec")
            compile(fixed, "fixed.py", "exec")
            checks["syntax_valid"] = True
        except SyntaxError:
            checks["syntax_valid"] = False
        cases = json.loads(paths["tests_path"].read_text())
        checks["tests_valid"] = bool(cases) and all(isinstance(c.get("input"), str) and isinstance(c.get("expected_output"), str) for c in cases)
        item["test_count"] = len(cases)
        failures.extend(f"{pid}: {name}" for name, ok in checks.items() if not ok)
    # Stop before execution if any structural prerequisite fails.
    if not failures:
        with tempfile.TemporaryDirectory(prefix="algorythm-gate7-") as scratch:
            for record, item in zip(records, report["programs"]):
                cases = json.loads((MANIFEST.parent / record["tests_path"]).read_text())
                for version in ("buggy", "fixed"):
                    path = (MANIFEST.parent / record[f"{version}_source_path"]).resolve()
                    item[f"{version}_outcomes"] = [execute(path, c, scratch) for c in cases]
                    item[f"{version}_pass_count"] = item[f"{version}_outcomes"].count("pass")
                    item[f"{version}_fail_count"] = len(cases) - item[f"{version}_pass_count"]
                item["checks"]["buggy_has_pass_and_fail"] = item["buggy_pass_count"] >= 1 and item["buggy_fail_count"] >= 1
                item["checks"]["fixed_passes_all_packaged_tests"] = item["fixed_fail_count"] == 0
                item["matches_prior_dynamic_counts"] = all(item[k] == int(eligibility[record["program_id"]][k]) for k in (
                    "buggy_pass_count", "buggy_fail_count", "fixed_pass_count", "fixed_fail_count"))
                failures.extend(f"{item['program_id']}: {name}" for name in ("buggy_has_pass_and_fail", "fixed_passes_all_packaged_tests") if not item["checks"][name])
                print(f"{item['task_id']} {item['program_id']}: buggy {item['buggy_pass_count']}P/{item['buggy_fail_count']}F; fixed {item['fixed_pass_count']}P/{item['fixed_fail_count']}F", flush=True)
    report["manifest_sha256_after"] = digest(MANIFEST)
    report["all_input_bytes_unchanged"] = all(digest(p) == h for p, h in paths_before.items()) and digest(MANIFEST) == report["manifest_sha256_before"]
    if not report["all_input_bytes_unchanged"]:
        failures.append("input bytes changed")
    report["mechanical_status"] = "BLOCK" if failures else "PASS"
    output = ROOT / "data/manifests/GATE7_DATASET_SANITY.json"
    output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"mechanical_status": report["mechanical_status"], "failures": failures, "report": str(output)}))
    return bool(failures)


if __name__ == "__main__":
    sys.exit(main())
