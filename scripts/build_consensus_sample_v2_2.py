#!/usr/bin/env python3
"""Build and validate the pre-results consensus-only pilot v2.2 sample.

No v2.0/v2.1 manifest or old automated pattern label is read. The only
pattern-label inputs are the two independent blinded annotation CSVs.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import random
import subprocess
import sys
import tempfile
import urllib.request
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFESTS = ROOT / "data/manifests"
CLAUDE = MANIFESTS / "pattern_annotations_claude_v2_2.csv"
CODEX = MANIFESTS / "pattern_annotations_codex_v2_2.csv"
DISAGREEMENTS = MANIFESTS / "pattern_annotation_disagreements_v2_2.jsonl"
BLINDED = ROOT / "annotation_v2_2/blinded_records.jsonl"
GROUND_TRUTH = MANIFESTS / "ground_truth_freeze_v2.csv"
DYNAMIC = MANIFESTS / "dynamic_test_eligibility_v2_1.csv"
CODE = ROOT / "data/external/ConDefects/Code"
CACHE = ROOT / "data/cache/testcases"
RAW = ROOT / "data/raw/v2_2"

CONSENSUS_OUT = MANIFESTS / "pattern_annotations_consensus_v2_2.csv"
JSON_OUT = MANIFESTS / "pilot_manifest_v2_2.json"
CSV_OUT = MANIFESTS / "pilot_manifest_v2_2.csv"
AUDIT_OUT = MANIFESTS / "SAMPLING_AUDIT_V2_2.md"

SEED = 20260910
EXPECTED_N = 232
EXPECTED_AGREEMENTS = 182
EXPECTED_DISAGREEMENTS = 50
EXPECTED_KAPPA = 0.752269
EXCLUSION_REASON = "excluded from pilot: independent pattern annotators disagreed"
CONSENSUS_SOURCE = "claude-codex-blinded-agreement"
MANIFEST_SOURCE = "model-consensus"
ALLOCATIONS = (8, 8, 7, 7)
VOCABULARY = (
    "two_pointers", "sliding_window", "binary_search", "prefix_sums",
    "dynamic_programming", "greedy", "graph_traversal_dfs_bfs",
    "sorting_based", "hash_map_counting", "brute_force_implementation",
    "intervals", "simulation",
)
LOCKED_HASHES = {
    CLAUDE: "5550f59f7e869deecdf6427f90b092576a81c6df9125870b0fe34e8c7b4ef773",
    CODEX: "dc89712a1cfd056652f05899d816605fdce757ace3ba8d181974fd48879a5c40",
    DISAGREEMENTS: "bd21d66615a9a8fdd81ea303b19641c295e2ebc65ef22cd8f265450020a10ebf",
    BLINDED: "8a1924066287ec9b9110018e5e301736dd4d1921be9b4dc0d06396264bdf0b99",
    GROUND_TRUTH: "2e5ef39ee663b48fb98097feaebd1f18a7ec7c709ef80fc1da763446c645dde2",
    DYNAMIC: "93b5d64b6d12d1a8bd7c7afd95143390ccd2d71dec7cff6e7032cc328a2a5c23",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_locked_inputs() -> None:
    for path, expected in LOCKED_HASHES.items():
        actual = sha256(path)
        if actual != expected:
            raise ValueError(f"locked input changed: {path}: {actual} != {expected}")


def read_csv_by_key(path: Path) -> dict[tuple[str, str], dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    result: dict[tuple[str, str], dict[str, str]] = {}
    for row in rows:
        key = (row["program_id"], row["task_id"])
        if key in result:
            raise ValueError(f"duplicate annotation key in {path}: {key}")
        result[key] = row
    return result


def read_blinded() -> list[dict]:
    return [json.loads(line) for line in BLINDED.read_text(encoding="utf-8").splitlines() if line]


def read_table_by_program(path: Path) -> dict[str, dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return {row["program_id"]: row for row in csv.DictReader(handle)}


def consensus_and_disagreements() -> tuple[list[dict], set[tuple[str, str]], list[dict]]:
    claude = read_csv_by_key(CLAUDE)
    codex = read_csv_by_key(CODEX)
    blinded = read_blinded()
    frame_keys = [(str(row["program_id"]), str(row["task_id"])) for row in blinded]
    if len(frame_keys) != EXPECTED_N or len(set(frame_keys)) != EXPECTED_N:
        raise ValueError("blinded frame is not the frozen 232-program unique-key frame")
    if set(claude) != set(frame_keys) or set(codex) != set(frame_keys):
        raise ValueError("annotation identifiers do not equal the blinded frame")

    consensus = []
    disagreement_keys = set()
    for key in frame_keys:
        left, right = claude[key], codex[key]
        if left["pattern_label"] != right["pattern_label"]:
            disagreement_keys.add(key)
            continue
        consensus.append({
            "program_id": key[0],
            "task_id": key[1],
            "pattern_label": left["pattern_label"],
            "consensus_source": CONSENSUS_SOURCE,
            "claude_confidence": left.get("confidence", ""),
            "codex_confidence": right.get("confidence", ""),
        })

    preserved = [
        json.loads(line) for line in DISAGREEMENTS.read_text(encoding="utf-8").splitlines() if line
    ]
    preserved_keys = {(str(row["program_id"]), str(row["task_id"])) for row in preserved}
    if len(consensus) != EXPECTED_AGREEMENTS or len(disagreement_keys) != EXPECTED_DISAGREEMENTS:
        raise ValueError("agreement totals differ from the authorized amendment")
    if disagreement_keys != preserved_keys:
        raise ValueError("preserved disagreement artifact does not match live comparison")
    return consensus, disagreement_keys, blinded


def select_sample(consensus: list[dict]) -> tuple[Counter, list[tuple[str, int]], list[dict]]:
    in_vocab = [row for row in consensus if row["pattern_label"] in VOCABULARY]
    counts = Counter(row["pattern_label"] for row in in_vocab)
    eligible_classes = [label for label in VOCABULARY if counts[label] >= 7]
    eligible_classes.sort(key=lambda label: (-counts[label], VOCABULARY.index(label)))
    if len(eligible_classes) < 4:
        raise ValueError("fewer than four classes satisfy the frozen >=7 rule")
    selected_classes = list(zip(eligible_classes[:4], ALLOCATIONS))

    pools: dict[str, list[dict]] = defaultdict(list)
    for row in in_vocab:
        pools[row["pattern_label"]].append(row)
    rng = random.Random(SEED)
    selected = []
    for label, quota in selected_classes:
        pool = sorted(pools[label], key=lambda row: row["program_id"])
        selected.extend(rng.sample(pool, quota))
    return counts, selected_classes, selected


def output_matches(actual: str, expected: str) -> bool:
    actual_lines = [line.strip() for line in actual.strip().splitlines() if line.strip()]
    expected_lines = [line.strip() for line in expected.strip().splitlines() if line.strip()]
    if len(actual_lines) != len(expected_lines):
        return False
    for actual_line, expected_line in zip(actual_lines, expected_lines):
        actual_tokens, expected_tokens = actual_line.split(), expected_line.split()
        if len(actual_tokens) != len(expected_tokens):
            return False
        for actual_token, expected_token in zip(actual_tokens, expected_tokens):
            if actual_token == expected_token:
                continue
            try:
                actual_number, expected_number = float(actual_token), float(expected_token)
                delta = abs(actual_number - expected_number)
                if delta < 1e-6 or (
                    expected_number != 0 and delta / abs(expected_number) < 1e-6
                ):
                    continue
            except ValueError:
                pass
            return False
    return True


def run_program(path: Path, test_input: str, cwd: Path) -> tuple[bool, str]:
    try:
        completed = subprocess.run(
            [sys.executable, str(path)], input=test_input, capture_output=True,
            text=True, timeout=4.0, cwd=cwd,
            env={**os.environ, "LANG": "en_US.UTF-8"},
        )
        return completed.returncode == 0, completed.stdout
    except subprocess.TimeoutExpired:
        return False, ""


def case_outcomes(buggy: Path, fixed: Path, cases: list[dict]) -> tuple[int, int, int, int]:
    counts = [0, 0, 0, 0]
    with tempfile.TemporaryDirectory(prefix="algorythm-v2-2-tests-") as directory:
        cwd = Path(directory)
        for case in cases:
            ok_b, out_b = run_program(buggy, case["input"], cwd)
            ok_f, out_f = run_program(fixed, case["input"], cwd)
            b_pass = ok_b and output_matches(out_b, case["expected_output"])
            f_pass = ok_f and output_matches(out_f, case["expected_output"])
            counts[0 if b_pass else 1] += 1
            counts[2 if f_pass else 3] += 1
    return tuple(counts)


def fetch_archive_cases(task_id: str) -> list[dict]:
    contest, problem = task_id.split("_", 1)
    candidates = [problem.upper(), problem.capitalize(), problem]
    if problem.lower() == "h":
        candidates.insert(0, "Ex")
    headers = {"User-Agent": "AlgoRythm-research-consensus-freeze/2.2"}
    for archive_problem in candidates:
        base = (
            "https://raw.githubusercontent.com/conlacda/atcoder-testcases/"
            f"refs/heads/{contest}/{contest}/{archive_problem}"
        )
        try:
            request = urllib.request.Request(f"{base}/list.txt", headers=headers)
            with urllib.request.urlopen(request, timeout=10) as response:
                lines = response.read().decode("utf-8", errors="ignore").splitlines()
        except Exception:
            continue
        entries = []
        for line in lines:
            parts = line.strip().split(",")
            if len(parts) >= 2:
                try:
                    entries.append((parts[0], int(parts[1])))
                except ValueError:
                    continue
        entries.sort(
            key=lambda item: (
                0 if any(word in item[0].lower() for word in ("sample", "example")) else 1,
                item[1],
            )
        )
        eligible_entries = [(name, size) for name, size in entries if size <= 60_000]

        def download(entry: tuple[str, int]) -> dict | None:
            name, _ = entry
            try:
                in_request = urllib.request.Request(f"{base}/in/{name}", headers=headers)
                out_request = urllib.request.Request(f"{base}/out/{name}", headers=headers)
                with urllib.request.urlopen(in_request, timeout=10) as response:
                    test_input = response.read().decode("utf-8", errors="ignore")
                with urllib.request.urlopen(out_request, timeout=10) as response:
                    expected = response.read().decode("utf-8", errors="ignore")
                return {"input": test_input, "expected_output": expected}
            except Exception:
                return None

        with ThreadPoolExecutor(max_workers=12) as executor:
            downloaded = executor.map(download, eligible_entries)
            cases = [case for case in downloaded if case is not None]
        if cases:
            return cases
    raise ValueError(f"could not recover official tests for {task_id}")


def frozen_counts(row: dict[str, str]) -> tuple[int, int, int, int]:
    return tuple(
        int(row[field]) for field in (
            "buggy_pass_count", "buggy_fail_count", "fixed_pass_count", "fixed_fail_count"
        )
    )


def load_or_recover_tests(
    task_id: str,
    buggy: Path,
    fixed: Path,
    dynamic_row: dict[str, str],
) -> tuple[list[dict], str]:
    cache_path = CACHE / f"{task_id}.json"
    cases = json.loads(cache_path.read_text(encoding="utf-8"))
    expected = frozen_counts(dynamic_row)
    if case_outcomes(buggy, fixed, cases) == expected:
        return cases, "regenerated-cache-matches-frozen-counts"

    target_pass, target_fail, target_fixed_pass, target_fixed_fail = expected
    if target_fixed_fail != 0 or target_fixed_pass != target_pass + target_fail:
        raise ValueError(f"unsupported frozen dynamic outcome for {task_id}: {expected}")
    candidates = cases + fetch_archive_cases(task_id)
    pass_cases, fail_cases, seen = [], [], set()
    with tempfile.TemporaryDirectory(prefix="algorythm-v2-2-recovery-") as directory:
        cwd = Path(directory)
        for case in candidates:
            key = (case["input"], case["expected_output"])
            if key in seen:
                continue
            seen.add(key)
            ok_f, out_f = run_program(fixed, case["input"], cwd)
            if not (ok_f and output_matches(out_f, case["expected_output"])):
                continue
            ok_b, out_b = run_program(buggy, case["input"], cwd)
            bucket = pass_cases if ok_b and output_matches(out_b, case["expected_output"]) else fail_cases
            bucket.append(case)
            if len(pass_cases) >= target_pass and len(fail_cases) >= target_fail:
                break
    if len(pass_cases) < target_pass or len(fail_cases) < target_fail:
        raise ValueError(f"could not reconstruct frozen dynamic counts for {task_id}")
    recovered = pass_cases[:target_pass] + fail_cases[:target_fail]
    if case_outcomes(buggy, fixed, recovered) != expected:
        raise ValueError(f"recovered suite is unstable for {task_id}")
    return recovered, "official-archive-recovery-matches-frozen-counts"


def write_consensus_csv(rows: list[dict]) -> None:
    fields = (
        "program_id", "task_id", "pattern_label", "consensus_source",
        "claude_confidence", "codex_confidence",
    )
    with CONSENSUS_OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def build() -> tuple[Counter, list[tuple[str, int]], list[dict], list[dict]]:
    existing = [path for path in (CONSENSUS_OUT, JSON_OUT, CSV_OUT, AUDIT_OUT) if path.exists()]
    if existing:
        raise ValueError(
            "refusing to regenerate existing frozen output(s); use --validate-only: "
            + ", ".join(str(path) for path in existing)
        )
    verify_locked_inputs()
    consensus, disagreement_keys, blinded = consensus_and_disagreements()
    counts, selected_classes, selected = select_sample(consensus)
    write_consensus_csv(consensus)

    ground_truth = read_table_by_program(GROUND_TRUTH)
    dynamic = read_table_by_program(DYNAMIC)
    frame = {str(row["program_id"]): row for row in blinded}
    annotations = {(row["program_id"], row["task_id"]): row for row in consensus}
    frozen_at = datetime.now(timezone.utc).isoformat()
    json_records, csv_records, roster = [], [], []

    for rank, item in enumerate(selected, 1):
        program_id, task_id, label = item["program_id"], item["task_id"], item["pattern_label"]
        key = (program_id, task_id)
        if key in disagreement_keys or key not in annotations:
            raise ValueError(f"selected record lacks exact consensus: {key}")
        gt = ground_truth[program_id]
        dyn = dynamic[program_id]
        if gt["decision"] != "include" or gt["task_id"] != task_id:
            raise ValueError(f"invalid frozen ground truth for {key}")
        if dyn["eligible"] != "True" or dyn["task_id"] != task_id:
            raise ValueError(f"invalid frozen dynamic eligibility for {key}")

        source_dir = CODE / task_id / "Python" / program_id
        source_buggy = source_dir / "faultyVersion.py"
        source_fixed = source_dir / "correctVersion.py"
        buggy_text = source_buggy.read_text(encoding="utf-8", errors="ignore")
        fixed_text = source_fixed.read_text(encoding="utf-8", errors="ignore")
        if buggy_text != frame[program_id]["buggy_source"]:
            raise ValueError(f"buggy source differs from blinded packet: {key}")
        faulty_lines = json.loads(gt["faulty_lines"])
        loc = len(buggy_text.splitlines())
        if len(faulty_lines) != 1 or not (1 <= faulty_lines[0] <= loc):
            raise ValueError(f"invalid single-line ground truth for {key}")

        tests, suite_source = load_or_recover_tests(task_id, source_buggy, source_fixed, dyn)
        package_dir = RAW / program_id
        package_dir.mkdir(parents=True, exist_ok=True)
        packaged_buggy = package_dir / "buggy.py"
        packaged_fixed = package_dir / "fixed.py"
        packaged_tests = package_dir / "tests.json"
        packaged_buggy.write_text(buggy_text, encoding="utf-8")
        packaged_fixed.write_text(fixed_text, encoding="utf-8")
        packaged_tests.write_text(json.dumps(tests, indent=2) + "\n", encoding="utf-8")
        outcomes = case_outcomes(packaged_buggy, packaged_fixed, tests)
        if outcomes != frozen_counts(dyn):
            raise ValueError(f"packaged tests do not reproduce frozen counts for {key}")

        relative_base = f"../raw/v2_2/{program_id}"
        record = {
            "program_id": program_id,
            "task_id": task_id,
            "buggy_source_path": f"{relative_base}/buggy.py",
            "fixed_source_path": f"{relative_base}/fixed.py",
            "tests_path": f"{relative_base}/tests.json",
            "faulty_lines": faulty_lines,
            "pattern_label": label,
            "pattern_source": MANIFEST_SOURCE,
            "loc": loc,
            "difficulty": str(frame[program_id].get("difficulty", "unknown")),
            "inclusion_status": "included",
            "evaluation_denominator": loc,
        }
        json_records.append(record)
        csv_records.append({
            **record,
            "faulty_lines": json.dumps(faulty_lines),
            "claude_confidence": item["claude_confidence"],
            "codex_confidence": item["codex_confidence"],
            "selection_rank": rank,
            "sampling_seed": SEED,
            "selection_frozen_at": frozen_at,
        })
        roster.append({
            "rank": rank,
            "program_id": program_id,
            "task_id": task_id,
            "pattern_label": label,
            "faulty_line": faulty_lines[0],
            "loc": loc,
            "dynamic_counts": outcomes,
            "suite_source": suite_source,
        })

    manifest = {
        "manifest_version": 1,
        "dataset_name": "ConDefects-Python",
        "created_at": frozen_at,
        "selection_frozen_at": frozen_at,
        "programs": json_records,
    }
    JSON_OUT.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    fields = (
        "program_id", "task_id", "buggy_source_path", "fixed_source_path", "tests_path",
        "faulty_lines", "pattern_label", "pattern_source", "claude_confidence",
        "codex_confidence", "loc", "difficulty", "inclusion_status",
        "evaluation_denominator", "selection_rank", "sampling_seed", "selection_frozen_at",
    )
    with CSV_OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(csv_records)
    return counts, selected_classes, selected, roster


def validate() -> dict:
    verify_locked_inputs()
    consensus, disagreement_keys, _ = consensus_and_disagreements()
    counts, selected_classes, selected = select_sample(consensus)
    with CONSENSUS_OUT.open(newline="", encoding="utf-8") as handle:
        written_consensus = list(csv.DictReader(handle))
    if written_consensus != consensus:
        raise ValueError("consensus CSV differs from the exact-agreement derivation")
    manifest = json.loads(JSON_OUT.read_text(encoding="utf-8"))
    records = manifest["programs"]
    expected_ids = [row["program_id"] for row in selected]
    if len(records) != 30 or [row["program_id"] for row in records] != expected_ids:
        raise ValueError("manifest roster differs from the deterministic seeded draw")
    if len({row["task_id"] for row in records}) != 30:
        raise ValueError("task_id is not unique")

    consensus_map = {(row["program_id"], row["task_id"]): row for row in consensus}
    ground_truth = read_table_by_program(GROUND_TRUTH)
    dynamic = read_table_by_program(DYNAMIC)
    quota_counts = Counter()
    for record in records:
        key = (record["program_id"], record["task_id"])
        if key in disagreement_keys or key not in consensus_map:
            raise ValueError(f"disagreement or non-consensus record selected: {key}")
        if record["pattern_label"] != consensus_map[key]["pattern_label"]:
            raise ValueError(f"manifest label differs from consensus: {key}")
        if record["pattern_source"] != MANIFEST_SOURCE:
            raise ValueError(f"invalid model-consensus provenance: {key}")
        gt, dyn = ground_truth[record["program_id"]], dynamic[record["program_id"]]
        if gt["decision"] != "include" or gt["task_id"] != record["task_id"]:
            raise ValueError(f"frozen ground truth invalid: {key}")
        if json.loads(gt["faulty_lines"]) != record["faulty_lines"]:
            raise ValueError(f"faulty lines differ from freeze: {key}")
        if dyn["eligible"] != "True" or dyn["task_id"] != record["task_id"]:
            raise ValueError(f"frozen dynamic eligibility invalid: {key}")
        paths = {
            name: (JSON_OUT.parent / record[name]).resolve()
            for name in ("buggy_source_path", "fixed_source_path", "tests_path")
        }
        if not all(path.is_file() and path.is_relative_to(RAW) for path in paths.values()):
            raise ValueError(f"packaged paths invalid: {key}")
        buggy_text = paths["buggy_source_path"].read_text(encoding="utf-8")
        if not (
            len(buggy_text.splitlines())
            == record["loc"]
            == record["evaluation_denominator"]
        ):
            raise ValueError(f"line-count metadata invalid: {key}")
        cases = json.loads(paths["tests_path"].read_text(encoding="utf-8"))
        if case_outcomes(paths["buggy_source_path"], paths["fixed_source_path"], cases) != frozen_counts(dyn):
            raise ValueError(f"dynamic tests no longer reproduce frozen counts: {key}")
        quota_counts[record["pattern_label"]] += 1

    expected_quotas = dict(selected_classes)
    if dict(quota_counts) != expected_quotas:
        raise ValueError(f"class quotas invalid: {quota_counts} != {expected_quotas}")
    with CSV_OUT.open(newline="", encoding="utf-8") as handle:
        csv_rows = list(csv.DictReader(handle))
    if len(csv_rows) != 30 or [row["program_id"] for row in csv_rows] != expected_ids:
        raise ValueError("CSV manifest roster differs from JSON manifest")
    if any(row["sampling_seed"] != str(SEED) for row in csv_rows):
        raise ValueError("CSV manifest does not carry the frozen seed")
    return {
        "consensus_programs": len(consensus),
        "consensus_outside_vocabulary": sum(
            row["pattern_label"] == "outside_vocabulary" for row in consensus
        ),
        "eligible_consensus_programs": sum(
            row["pattern_label"] in VOCABULARY for row in consensus
        ),
        "class_counts": {label: counts[label] for label in VOCABULARY},
        "selected_classes": selected_classes,
        "final_ids": expected_ids,
        "manifest_sha256": sha256(JSON_OUT),
        "validation": "PASS",
    }


def write_audit(
    summary: dict,
    selected_classes: list[tuple[str, int]],
    roster: list[dict],
) -> None:
    class_counts = summary["class_counts"]
    disagreement_ids = [
        str(json.loads(line)["program_id"])
        for line in DISAGREEMENTS.read_text(encoding="utf-8").splitlines()
        if line
    ]
    lines = [
        "# Sampling Audit — Pilot v2.2 Consensus-Only Freeze",
        "",
        "**Amendment timing:** authorized before any valid scientific result existed.",
        f"**Sampling seed:** `{SEED}` (frozen; no rerolls).",
        "**Scientific execution:** not run.",
        "**Validation:** PASS.",
        "",
        "## 1. Pre-results methodological amendment",
        "",
        "The pilot uses **exact-consensus labels from two independent blinded model "
        "annotators**. Claude and Codex independently annotated the same 232-program "
        "task-independent frame before their outputs were compared.",
        "",
        "- Independently annotated programs: **232**",
        "- Exact agreements: **182**",
        "- Disagreements: **50**",
        "- Raw agreement: **78.4483%**",
        f"- Cohen's kappa: **{EXPECTED_KAPPA:.6f}**",
        "",
        "The 50 disagreements were not adjudicated, and neither annotator was "
        "preferred over the other. Every disagreement was excluded uniformly with "
        f"the reason: **\"{EXCLUSION_REASON}\"**. The original disagreement artifact "
        "is preserved unchanged as audit evidence for future work.",
        "",
        "This is a pilot-specific reliability filter intended to avoid introducing "
        "adjudicator-dependent labels.",
        "",
        "**Limitation:** the resulting pilot represents programs with comparatively "
        "unambiguous algorithmic-pattern assignments and may not generalize to "
        "ambiguous programs.",
        "",
        "No prior automated pattern labels, old sample membership, pattern priors, "
        "or scientific localization outputs were inputs to this rebuild. The v2.0 "
        "and v2.1 manifests and their raw packages were not modified.",
        "",
        "## 2. Consensus eligibility funnel",
        "",
        "| Stage | Retained | Excluded | Rule |",
        "|---|---:|---:|---|",
        "| Independent blinded annotations | 232 | 0 | Frozen task-independent frame |",
        f"| Exact consensus | 182 | 50 | `{EXCLUSION_REASON}` |",
        "| In-vocabulary consensus | 157 | 25 | Consensus `outside_vocabulary` excluded |",
        "| Classes meeting threshold | 130 | 27 | Frozen class count >= 7 |",
        "| Top-four class pools | 109 | 21 | Count descending; vocabulary-order tie break |",
        "| Final sample | 30 | 79 not drawn | Seeded 8/8/7/7 draw without replacement |",
        "",
        "## 3. Consensus class counts",
        "",
        "Counts below exclude the 25 exact-consensus `outside_vocabulary` records.",
        "",
        "| Frozen pattern class | Count | >= 7 | Selected rank | Allocation |",
        "|---|---:|:---:|---:|---:|",
    ]
    rank_map = {label: (rank, quota) for rank, (label, quota) in enumerate(selected_classes, 1)}
    for label in VOCABULARY:
        rank, quota = rank_map.get(label, ("—", 0))
        lines.append(
            f"| `{label}` | {class_counts[label]} | "
            f"{'Yes' if class_counts[label] >= 7 else 'No'} | {rank} | {quota} |"
        )
    lines.extend([
        "", "## 4. Deterministic class selection and draw", "",
        "Eligible classes were ranked by count descending, with ties broken by the "
        "frozen vocabulary order. The top four received allocations 8/8/7/7. "
        f"Within each class, records were sorted by `program_id` and sampled without "
        f"replacement using one `random.Random({SEED})` stream in class-rank order. "
        "No prior sample member was preserved by rule, no seed was changed, and no "
        "draw was rerolled.",
        "",
        "| Rank | Program ID | Task ID | Consensus pattern | LOC | Faulty line | Dynamic B pass/fail; F pass/fail | Test package |",
        "|---:|---|---|---|---:|---:|---|---|",
    ])
    for row in roster:
        bp, bf, fp, ff = row["dynamic_counts"]
        lines.append(
            f"| {row['rank']} | `{row['program_id']}` | `{row['task_id']}` | "
            f"`{row['pattern_label']}` | {row['loc']} | {row['faulty_line']} | "
            f"{bp}/{bf}; {fp}/{ff} | `{row['suite_source']}` |"
        )
    lines.extend([
        "", "## 5. Disagreement exclusion record", "",
        f"All {len(disagreement_ids)} records in "
        "`pattern_annotation_disagreements_v2_2.jsonl` are excluded from this pilot "
        f"with the exact reason \"{EXCLUSION_REASON}\". Their program IDs are:",
        "", ", ".join(f"`{program_id}`" for program_id in disagreement_ids) + ".",
        "", "The disagreement artifact SHA-256 remains:", "",
        f"`{sha256(DISAGREEMENTS)}`",
        "", "## 6. Validation", "",
        "- Final manifest contains exactly 30 included programs: **PASS**",
        "- All 30 `task_id` values are unique: **PASS**",
        "- Every selected record has exact Claude-Codex consensus: **PASS**",
        "- Zero disagreement records are selected: **PASS**",
        "- All selected records match frozen single-line ground truth: **PASS**",
        "- All selected records match frozen dynamic eligibility and packaged tests reproduce its counts: **PASS**",
        "- Class quotas are exactly 8/8/7/7 in ranked-class order: **PASS**",
        f"- Every CSV row carries frozen seed `{SEED}`: **PASS**",
        "- No scientific LLM experiment was run: **PASS**",
        "", "## 7. Freeze hashes", "",
        f"- Consensus annotations CSV: `{sha256(CONSENSUS_OUT)}`",
        f"- Pilot manifest JSON: `{summary['manifest_sha256']}`",
        f"- Pilot manifest CSV: `{sha256(CSV_OUT)}`",
        "", "**Final status: V2.2 CONSENSUS SAMPLE FROZEN**", "",
    ])
    AUDIT_OUT.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    roster = []
    if not args.validate_only:
        _, selected_classes, _, roster = build()
        summary = validate()
        write_audit(summary, selected_classes, roster)
    else:
        summary = validate()
        if not AUDIT_OUT.is_file():
            raise ValueError("sampling audit is missing")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
