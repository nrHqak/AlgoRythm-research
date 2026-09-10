#!/usr/bin/env python3
"""Match frozen testcase bytes to pinned third-party files or AtCoder samples.

Never modifies data/raw, the manifest, or the acquisition cache. Downloads only
public testcase data into memory; writes hashes and source URLs as audit evidence.
"""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import argparse
import hashlib
import html
import json
from pathlib import Path
import re
import subprocess
import sys
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
MIRROR = "https://github.com/conlacda/atcoder-testcases.git"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "AlgoRythm-Gate7-provenance-audit"})
    with urllib.request.urlopen(req, timeout=30) as response:
        return response.read()


def task_audit(record, refs):
    task = record["task_id"]
    contest, problem = task.split("_", 1)
    test_path = ROOT / "data/manifests" / record["tests_path"]
    local_bytes = test_path.read_bytes()
    local = json.loads(local_bytes)
    result = {"task_id": task, "program_id": record["program_id"],
              "packaged_tests_sha256": sha(local_bytes), "case_count": len(local),
              "classification": "unknown", "cases": [], "errors": []}
    commit = refs.get(contest)
    result["mirror_commit"] = commit
    matches = {}
    if commit:
        candidates = (["Ex"] if problem.lower() == "h" else []) + list(dict.fromkeys((problem.upper(), problem.capitalize(), problem)))
        for folder in candidates:
            base = f"https://raw.githubusercontent.com/conlacda/atcoder-testcases/{commit}/{contest}/{folder}"
            try:
                listing_bytes = fetch(base + "/list.txt")
            except urllib.error.HTTPError as error:
                if error.code == 404:
                    continue
                raise
            entries = []
            for line in listing_bytes.decode("utf-8", errors="ignore").splitlines():
                parts = line.strip().split(",")
                if len(parts) >= 2:
                    try:
                        entries.append((parts[0], int(parts[1])))
                    except ValueError:
                        pass
            if not entries:
                continue
            # Same predeclared selection order as acquisition; stable ties retain
            # list.txt order. No choosing cases based on program outcomes.
            entries.sort(key=lambda pair: (0 if any(k in pair[0].lower() for k in ("example", "sample", "hand", "000")) else 1, pair[1]))
            selected = [pair for pair in entries if pair[1] <= 30000][:8]
            result["list_url"] = base + "/list.txt"
            result["list_sha256"] = sha(listing_bytes)
            result["archive_list_case_count"] = len(entries)
            result["archive_selected_names"] = [name for name, _ in selected]
            for name, size in selected:
                in_url, out_url = base + "/in/" + name, base + "/out/" + name
                raw_input, raw_output = fetch(in_url), fetch(out_url)
                pair = (raw_input.decode("utf-8", errors="ignore"), raw_output.decode("utf-8", errors="ignore"))
                matches.setdefault(pair, []).append({"name": name, "listed_input_size": size,
                    "input_url": in_url, "output_url": out_url,
                    "upstream_input_sha256": sha(raw_input), "upstream_output_sha256": sha(raw_output)})
            break
    if all((c["input"], c["expected_output"]) in matches for c in local):
        result["classification"] = "reproducible third-party archive/mirror"
        for index, case in enumerate(local, 1):
            result["cases"].append({"index": index,
                "input_utf8_sha256": sha(case["input"].encode()),
                "expected_output_utf8_sha256": sha(case["expected_output"].encode()),
                "matching_sources": matches[(case["input"], case["expected_output"])], "exact_text_match": True})
        result["matches_complete_selected_sequence"] = [
            next((s["name"] for s in matches[(c["input"], c["expected_output"])]), None) for c in local
        ] == result["archive_selected_names"]
    else:
        url = f"https://atcoder.jp/contests/{contest}/tasks/{task}"
        page = fetch(url)
        text = page.decode("utf-8", errors="ignore")
        inputs = re.findall(r"<h3>Sample Input \d+</h3><pre>(.*?)</pre>", text, re.S)
        outputs = re.findall(r"<h3>Sample Output \d+</h3><pre>(.*?)</pre>", text, re.S)
        pairs = [(html.unescape(i).replace("\r\n", "\n"), html.unescape(o).replace("\r\n", "\n")) for i, o in zip(inputs, outputs)]
        result["official_page_url"] = url
        result["official_page_sha256"] = sha(page)
        if [(c["input"], c["expected_output"]) for c in local] == pairs:
            result["classification"] = "official AtCoder source"
            result["cases"] = [{"index": index, "sample_number": index, "source_url": url,
                "input_utf8_sha256": sha(c["input"].encode()),
                "expected_output_utf8_sha256": sha(c["expected_output"].encode()), "exact_text_match": True}
                for index, c in enumerate(local, 1)]
        else:
            result["errors"].append("packaged sequence not reproduced from either acquisition source")
    result["packaged_bytes_unchanged"] = sha(test_path.read_bytes()) == sha(local_bytes)
    print(f"{task}: {result['classification']} ({len(result['cases'])}/{len(local)} cases)", flush=True)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pins", type=Path, help="Use commits from an existing audit instead of moving branch tips")
    parser.add_argument("--output", type=Path, default=ROOT / "data/manifests/GATE7_TESTCASE_PROVENANCE.json")
    args = parser.parse_args()
    manifest_path = ROOT / "data/manifests/pilot_manifest_v2_1.json"
    before = sha(manifest_path.read_bytes())
    records = json.loads(manifest_path.read_bytes())["programs"]
    if args.pins:
        previous = json.loads(args.pins.read_text())
        if previous["manifest_sha256"] != before:
            raise ValueError("manifest differs from pinned provenance record")
        refs = {t["task_id"].split("_", 1)[0]: t["mirror_commit"] for t in previous["tasks"]}
    else:
        raw_refs = subprocess.check_output(["git", "ls-remote", MIRROR, "refs/heads/*"], text=True)
        refs = {line.split()[1].removeprefix("refs/heads/"): line.split()[0] for line in raw_refs.splitlines()}
    report = {"audited_at": datetime.now(timezone.utc).isoformat(),
              "mirror_repository": MIRROR, "manifest_sha256": before,
              "pin_scope": "resolved at Gate 7; original download did not record commits",
              "tasks": []}
    def safe(record):
        try:
            return task_audit(record, refs)
        except Exception as error:
            return {"task_id": record["task_id"], "classification": "unknown", "errors": [str(error)]}
    with ThreadPoolExecutor(max_workers=6) as pool:
        report["tasks"] = list(pool.map(safe, records))
    report["manifest_unchanged"] = sha(manifest_path.read_bytes()) == before
    report["status"] = "PASS" if report["manifest_unchanged"] and all(
        t["classification"] != "unknown" and t["packaged_bytes_unchanged"] and not t["errors"] for t in report["tasks"]) else "BLOCK"
    output = args.output
    output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"status": report["status"], "report": str(output)}))
    return report["status"] != "PASS"


if __name__ == "__main__":
    sys.exit(main())
