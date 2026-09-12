#!/usr/bin/env python3
"""Compare two independent v2.2 pattern annotations without adjudicating them.

The program reads only the two annotation CSVs and the sanitized blinded record
packet.  It never reads a pilot manifest, fault location, fixed source, diff,
prior, prior sample, or localization output.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import tempfile
from collections import Counter, defaultdict
from pathlib import Path


FROZEN_LABELS = (
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
    "outside_vocabulary",
    "uncertain",
)
REQUIRED_ANNOTATION_FIELDS = {"program_id", "task_id", "pattern_label"}
ALLOWED_PACKET_FIELDS = {
    "index",
    "program_id",
    "task_id",
    "contest",
    "problem_letter",
    "difficulty",
    "atcoder_url",
    "loc",
    "buggy_source",
}
TASK_METADATA_FIELDS = (
    "contest",
    "problem_letter",
    "difficulty",
    "atcoder_url",
    "loc",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_annotations(path: Path, annotator: str) -> dict[tuple[str, str], str]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        fields = set(reader.fieldnames or ())
        missing = REQUIRED_ANNOTATION_FIELDS - fields
        if missing:
            raise ValueError(f"{annotator} CSV missing fields: {sorted(missing)}")
        result: dict[tuple[str, str], str] = {}
        for line_number, row in enumerate(reader, 2):
            key = (row["program_id"].strip(), row["task_id"].strip())
            label = row["pattern_label"].strip()
            if not all(key):
                raise ValueError(f"{annotator} CSV line {line_number}: blank identifier")
            if label not in FROZEN_LABELS:
                raise ValueError(
                    f"{annotator} CSV line {line_number}: invalid label {label!r}"
                )
            if key in result:
                raise ValueError(f"{annotator} CSV has duplicate record {key}")
            result[key] = label
    return result


def read_blinded_packet(path: Path) -> list[dict]:
    records = []
    seen = set()
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            record = json.loads(line)
            unexpected = set(record) - ALLOWED_PACKET_FIELDS
            missing = {"program_id", "task_id", "buggy_source"} - set(record)
            if unexpected or missing:
                raise ValueError(
                    f"blinded packet line {line_number}: unexpected={sorted(unexpected)}, "
                    f"missing={sorted(missing)}"
                )
            key = (str(record["program_id"]), str(record["task_id"]))
            if key in seen:
                raise ValueError(f"blinded packet has duplicate record {key}")
            seen.add(key)
            records.append(record)
    return records


def write_comparison(
    claude_path: Path,
    codex_path: Path,
    packet_path: Path,
    output_dir: Path,
) -> dict:
    claude = read_annotations(claude_path, "Claude")
    codex = read_annotations(codex_path, "Codex")
    records = read_blinded_packet(packet_path)
    frame_keys = [(str(r["program_id"]), str(r["task_id"])) for r in records]
    frame_set = set(frame_keys)

    for name, labels in (("Claude", claude), ("Codex", codex)):
        missing = frame_set - set(labels)
        extra = set(labels) - frame_set
        if missing or extra:
            raise ValueError(
                f"{name} identifiers do not match blinded frame: "
                f"missing={len(missing)}, extra={len(extra)}"
            )

    n = len(frame_keys)
    if n == 0:
        raise ValueError("blinded frame is empty")

    claude_counts = Counter(claude[key] for key in frame_keys)
    codex_counts = Counter(codex[key] for key in frame_keys)
    matrix = {label: Counter() for label in FROZEN_LABELS}
    disagreements = []
    disagreements_by_label = {
        "Claude": Counter(),
        "Codex": Counter(),
    }
    agreements = 0

    for record, key in zip(records, frame_keys):
        claude_label = claude[key]
        codex_label = codex[key]
        matrix[claude_label][codex_label] += 1
        if claude_label == codex_label:
            agreements += 1
            continue
        disagreements_by_label["Claude"][claude_label] += 1
        disagreements_by_label["Codex"][codex_label] += 1
        disagreements.append(
            {
                "program_id": key[0],
                "task_id": key[1],
                "buggy_source": record["buggy_source"],
                "allowed_task_metadata": {
                    field: record[field]
                    for field in TASK_METADATA_FIELDS
                    if field in record
                },
                "claude_label": claude_label,
                "codex_label": codex_label,
            }
        )

    observed = agreements / n
    expected = sum(
        claude_counts[label] * codex_counts[label] for label in FROZEN_LABELS
    ) / (n * n)
    kappa = (observed - expected) / (1 - expected) if expected != 1 else 1.0

    output_dir.mkdir(parents=True, exist_ok=False)
    with (output_dir / "confusion_matrix.csv").open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.writer(handle)
        writer.writerow(["claude_label\\codex_label", *FROZEN_LABELS, "row_total"])
        for claude_label in FROZEN_LABELS:
            row = [matrix[claude_label][codex_label] for codex_label in FROZEN_LABELS]
            writer.writerow([claude_label, *row, sum(row)])
        writer.writerow(
            ["column_total", *[codex_counts[label] for label in FROZEN_LABELS], n]
        )

    with (output_dir / "disagreements_by_pattern.csv").open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.writer(handle)
        writer.writerow(["annotator", "pattern_label", "disagreements"])
        for annotator in ("Claude", "Codex"):
            for label in FROZEN_LABELS:
                writer.writerow(
                    [annotator, label, disagreements_by_label[annotator][label]]
                )

    with (output_dir / "blinded_disagreements.jsonl").open(
        "w", encoding="utf-8"
    ) as handle:
        for disagreement in disagreements:
            handle.write(json.dumps(disagreement, ensure_ascii=False) + "\n")

    summary = {
        "status": "COMPARISON_ONLY_NO_ADJUDICATION",
        "programs": n,
        "agreements": agreements,
        "disagreements": len(disagreements),
        "raw_agreement": observed,
        "cohens_kappa": kappa,
        "claude_distribution": dict(sorted(claude_counts.items())),
        "codex_distribution": dict(sorted(codex_counts.items())),
        "disagreements_by_pattern": {
            annotator: dict(sorted(counts.items()))
            for annotator, counts in disagreements_by_label.items()
        },
        "inputs_sha256": {
            "claude": sha256(claude_path),
            "codex": sha256(codex_path),
            "blinded_packet": sha256(packet_path),
        },
        "final_label_created": False,
        "required_final_label_sources": ["model-consensus", "model-adjudicated"],
    }
    (output_dir / "agreement_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return summary


def self_test() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        packet = root / "packet.jsonl"
        packet.write_text(
            "\n".join(
                json.dumps(
                    {
                        "index": i,
                        "program_id": str(i),
                        "task_id": f"task_{i}",
                        "buggy_source": "print(0)\n",
                        "difficulty": i,
                    }
                )
                for i in range(1, 5)
            )
            + "\n",
            encoding="utf-8",
        )
        for name, labels in (
            ("claude", ["greedy", "greedy", "simulation", "simulation"]),
            ("codex", ["greedy", "simulation", "simulation", "simulation"]),
        ):
            with (root / f"{name}.csv").open("w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["program_id", "task_id", "pattern_label"])
                for i, label in enumerate(labels, 1):
                    writer.writerow([i, f"task_{i}", label])
        summary = write_comparison(
            root / "claude.csv", root / "codex.csv", packet, root / "out"
        )
        assert summary["programs"] == 4
        assert summary["agreements"] == 3
        assert summary["disagreements"] == 1
        assert summary["raw_agreement"] == 0.75
        assert abs(summary["cohens_kappa"] - 0.5) < 1e-12
        disagreement = json.loads(
            (root / "out" / "blinded_disagreements.jsonl").read_text()
        )
        assert set(disagreement) == {
            "program_id",
            "task_id",
            "buggy_source",
            "allowed_task_metadata",
            "claude_label",
            "codex_label",
        }
    print("self-test: PASS")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--claude", type=Path)
    parser.add_argument("--codex", type=Path)
    parser.add_argument(
        "--blinded-records",
        type=Path,
        default=Path("annotation_v2_2/blinded_records.jsonl"),
    )
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--self-test", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.self_test:
        self_test()
        return
    if args.claude is None or args.codex is None or args.output_dir is None:
        raise SystemExit("--claude, --codex, and --output-dir are required")
    summary = write_comparison(
        args.claude, args.codex, args.blinded_records, args.output_dir
    )
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
