#!/usr/bin/env python3
"""Compare two independent blinded v2.2 model-annotation passes.

Reads only the two annotation CSVs and the sanitized blinded record packet.
It does not adjudicate disagreements or create a final v2.2 manifest.
``outside_vocabulary`` is a first-class label throughout.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import tempfile
from collections import Counter
from datetime import datetime, timezone
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
    "index", "program_id", "task_id", "contest", "problem_letter",
    "difficulty", "atcoder_url", "loc", "buggy_source",
}
TASK_METADATA_FIELDS = (
    "contest", "problem_letter", "difficulty", "atcoder_url", "loc",
)

DISAGREEMENTS_NAME = "pattern_annotation_disagreements_v2_2.jsonl"
AGREEMENTS_NAME = "pattern_annotation_agreements_v2_2.csv"
AUDIT_NAME = "PATTERN_ANNOTATION_AGREEMENT_V2_2.md"
MATRIX_NAME = "pattern_annotation_confusion_matrix_v2_2.csv"
BY_LABEL_NAME = "pattern_annotation_agreement_by_label_v2_2.csv"
BY_CONFIDENCE_NAME = "pattern_annotation_agreement_by_confidence_v2_2.csv"
DISAGREEMENTS_BY_LABEL_NAME = "pattern_annotation_disagreements_by_label_v2_2.csv"
SUMMARY_NAME = "pattern_annotation_agreement_summary_v2_2.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_annotations(path: Path, annotator: str) -> tuple[dict[tuple[str, str], dict], bool]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        fields = set(reader.fieldnames or ())
        missing = REQUIRED_ANNOTATION_FIELDS - fields
        if missing:
            raise ValueError(f"{annotator} CSV missing fields: {sorted(missing)}")
        has_confidence = "confidence" in fields
        result: dict[tuple[str, str], dict] = {}
        for line_number, row in enumerate(reader, 2):
            key = (row["program_id"].strip(), row["task_id"].strip())
            # Labels are intentionally compared byte-for-byte after CSV parsing.
            # Even surrounding whitespace is invalid rather than normalized.
            label = row["pattern_label"]
            confidence = row.get("confidence", "").strip()
            if not all(key):
                raise ValueError(f"{annotator} CSV line {line_number}: blank identifier")
            if label not in FROZEN_LABELS:
                raise ValueError(
                    f"{annotator} CSV line {line_number}: invalid label {label!r}"
                )
            if key in result:
                raise ValueError(f"{annotator} CSV has duplicate record {key}")
            result[key] = {"label": label, "confidence": confidence}
    return result, has_confidence


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


def pct(value: float | None) -> str:
    return "N/A" if value is None else f"{100 * value:.2f}%"


def markdown_matrix(matrix: dict[str, Counter], codex_counts: Counter, n: int) -> list[str]:
    lines = [
        "| Claude label \\ Codex label | " + " | ".join(FROZEN_LABELS) + " | Total |",
        "|---|" + "---:|" * (len(FROZEN_LABELS) + 1),
    ]
    for claude_label in FROZEN_LABELS:
        values = [matrix[claude_label][codex_label] for codex_label in FROZEN_LABELS]
        lines.append(
            f"| `{claude_label}` | "
            + " | ".join(str(value) for value in values)
            + f" | {sum(values)} |"
        )
    lines.append(
        "| **Total** | "
        + " | ".join(str(codex_counts[label]) for label in FROZEN_LABELS)
        + f" | {n} |"
    )
    return lines


def write_audit(
    path: Path,
    *,
    n: int,
    agreements: int,
    disagreements: int,
    observed: float,
    expected: float,
    kappa: float,
    matrix: dict[str, Counter],
    codex_counts: Counter,
    agreement_by_label: list[dict],
    confidence_pairs: list[dict],
    input_hashes: dict[str, str],
) -> None:
    lines = [
        "# Pattern Annotation Agreement Audit — v2.2",
        "",
        f"Generated at {datetime.now(timezone.utc).isoformat()} by "
        "`scripts/compare_pattern_annotations_v2_2.py`.",
        "",
        "## Independent annotation design",
        "",
        "Annotator A (Claude) and Annotator B (Codex) each completed an "
        "independent blinded model annotation pass over the same frozen "
        f"{n}-program frame. Comparison was deferred until both passes were "
        "complete. Neither original annotation CSV was modified by this comparison.",
        "",
        "Exact matches are eligible to become model-consensus labels. Conflicts "
        "remain unresolved and require model-adjudicated labels from an independent "
        "third adjudicator; this comparison does not create a final v2.2 manifest.",
        "",
        "## Blinding",
        "",
        "The comparison joins the two label files only to the sanitized blinded "
        "packet. The disagreement artifact exposes buggy source plus the permitted "
        "task metadata (`contest`, `problem_letter`, `difficulty`, `atcoder_url`, "
        "and `loc`) and the two current labels/confidences. It excludes fault "
        "locations, fixed source, prior-manifest labels, pattern priors, previous "
        "localization results, and old v2.1 AST labels.",
        "",
        "## Overall agreement",
        "",
        f"- Programs compared: **{n}**",
        f"- Exact agreements: **{agreements}**",
        f"- Disagreements: **{disagreements}**",
        f"- Raw agreement: **{observed:.6f} ({pct(observed)})**",
        f"- Chance-expected agreement: **{expected:.6f} ({pct(expected)})**",
        f"- Cohen's kappa: **{kappa:.6f}**",
        "- `outside_vocabulary` is treated as a valid, distinct category.",
        "- Distinct labels are not merged or normalized.",
        "",
        "## Agreement by pattern label",
        "",
        "The symmetric label agreement rate is exact matches for a label divided "
        "by the union of programs assigned that label by either annotator.",
        "",
        "| Pattern label | Claude count | Codex count | Exact matches | Union | Agreement |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for row in agreement_by_label:
        lines.append(
            f"| `{row['pattern_label']}` | {row['claude_count']} | "
            f"{row['codex_count']} | {row['exact_matches']} | {row['union_count']} | "
            f"{pct(row['agreement_rate'])} |"
        )
    lines.extend(["", "## Full confusion matrix", ""])
    lines.extend(markdown_matrix(matrix, codex_counts, n))
    lines.extend([
        "", "Rows are Claude labels; columns are Codex labels.", "",
        "## Agreement by confidence pair", "",
        "| Claude confidence | Codex confidence | Programs | Exact matches | Agreement |",
        "|---|---|---:|---:|---:|",
    ])
    if confidence_pairs:
        for row in confidence_pairs:
            lines.append(
                f"| `{row['claude_confidence']}` | `{row['codex_confidence']}` | "
                f"{row['programs']} | {row['exact_matches']} | "
                f"{pct(row['agreement_rate'])} |"
            )
    else:
        lines.append("| N/A | N/A | 0 | 0 | N/A |")
    lines.extend([
        "", "## Why disagreements require independent adjudication", "",
        "A disagreement has no model-consensus label. Allowing either original "
        "annotator to resolve its own conflict would make the resolution "
        "dependent on a party to the disagreement. A third independent, blinded "
        "adjudicator must review only the permitted evidence in the disagreement "
        "artifact and choose the model-adjudicated label without access to the "
        "excluded answer-bearing fields.",
        "", "## Reproducibility", "",
        f"- Claude CSV SHA-256: `{input_hashes['claude']}`",
        f"- Codex CSV SHA-256: `{input_hashes['codex']}`",
        f"- Blinded packet SHA-256: `{input_hashes['blinded_packet']}`",
        "", "**Final status: READY FOR THIRD-PARTY ADJUDICATION**", "",
    ])
    path.write_text("\n".join(lines), encoding="utf-8")


def write_comparison(
    claude_path: Path,
    codex_path: Path,
    packet_path: Path,
    output_dir: Path,
) -> dict:
    claude, claude_has_confidence = read_annotations(claude_path, "Claude")
    codex, codex_has_confidence = read_annotations(codex_path, "Codex")
    records = read_blinded_packet(packet_path)
    frame_keys = [(str(r["program_id"]), str(r["task_id"])) for r in records]
    frame_set = set(frame_keys)

    for name, annotations in (("Claude", claude), ("Codex", codex)):
        missing = frame_set - set(annotations)
        extra = set(annotations) - frame_set
        if missing or extra:
            raise ValueError(
                f"{name} identifiers do not match blinded frame: "
                f"missing={len(missing)}, extra={len(extra)}"
            )
    n = len(frame_keys)
    if n == 0:
        raise ValueError("blinded frame is empty")

    claude_counts = Counter(claude[key]["label"] for key in frame_keys)
    codex_counts = Counter(codex[key]["label"] for key in frame_keys)
    matrix = {label: Counter() for label in FROZEN_LABELS}
    disagreements: list[dict] = []
    agreements_rows: list[dict] = []
    disagreements_by_label = {"Claude": Counter(), "Codex": Counter()}
    confidence_pair_counts: Counter = Counter()
    confidence_pair_agreements: Counter = Counter()

    for record, key in zip(records, frame_keys):
        claude_row = claude[key]
        codex_row = codex[key]
        claude_label = claude_row["label"]
        codex_label = codex_row["label"]
        matrix[claude_label][codex_label] += 1
        confidence_pair = (claude_row["confidence"], codex_row["confidence"])
        if claude_has_confidence and codex_has_confidence:
            confidence_pair_counts[confidence_pair] += 1
        if claude_label == codex_label:
            agreements_rows.append({
                "program_id": key[0],
                "task_id": key[1],
                "pattern_label": claude_label,
                "consensus_source": "claude-codex-blinded-agreement",
            })
            if claude_has_confidence and codex_has_confidence:
                confidence_pair_agreements[confidence_pair] += 1
            continue
        disagreements_by_label["Claude"][claude_label] += 1
        disagreements_by_label["Codex"][codex_label] += 1
        disagreements.append({
            "program_id": key[0],
            "task_id": key[1],
            "buggy_source": record["buggy_source"],
            "allowed_task_metadata": {
                field: record[field] for field in TASK_METADATA_FIELDS if field in record
            },
            "claude_label": claude_label,
            "codex_label": codex_label,
            "claude_confidence": claude_row["confidence"],
            "codex_confidence": codex_row["confidence"],
        })

    agreements = len(agreements_rows)
    observed = agreements / n
    expected = sum(
        claude_counts[label] * codex_counts[label] for label in FROZEN_LABELS
    ) / (n * n)
    kappa = (observed - expected) / (1 - expected) if expected != 1 else 1.0

    agreement_by_label = []
    for label in FROZEN_LABELS:
        exact = matrix[label][label]
        union = claude_counts[label] + codex_counts[label] - exact
        agreement_by_label.append({
            "pattern_label": label,
            "claude_count": claude_counts[label],
            "codex_count": codex_counts[label],
            "exact_matches": exact,
            "union_count": union,
            "agreement_rate": exact / union if union else None,
        })

    confidence_pairs = []
    for pair in sorted(confidence_pair_counts):
        total = confidence_pair_counts[pair]
        exact = confidence_pair_agreements[pair]
        confidence_pairs.append({
            "claude_confidence": pair[0],
            "codex_confidence": pair[1],
            "programs": total,
            "exact_matches": exact,
            "agreement_rate": exact / total,
        })

    output_dir.mkdir(parents=True, exist_ok=True)
    with (output_dir / MATRIX_NAME).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["claude_label\\codex_label", *FROZEN_LABELS, "row_total"])
        for claude_label in FROZEN_LABELS:
            values = [matrix[claude_label][codex_label] for codex_label in FROZEN_LABELS]
            writer.writerow([claude_label, *values, sum(values)])
        writer.writerow(["column_total", *[codex_counts[label] for label in FROZEN_LABELS], n])

    with (output_dir / DISAGREEMENTS_BY_LABEL_NAME).open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.writer(handle)
        writer.writerow(["annotator", "pattern_label", "disagreements"])
        for annotator in ("Claude", "Codex"):
            for label in FROZEN_LABELS:
                writer.writerow([annotator, label, disagreements_by_label[annotator][label]])

    with (output_dir / BY_LABEL_NAME).open("w", newline="", encoding="utf-8") as handle:
        fields = (
            "pattern_label", "claude_count", "codex_count", "exact_matches",
            "union_count", "agreement_rate",
        )
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(agreement_by_label)

    with (output_dir / BY_CONFIDENCE_NAME).open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        fields = (
            "claude_confidence", "codex_confidence", "programs",
            "exact_matches", "agreement_rate",
        )
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(confidence_pairs)

    with (output_dir / DISAGREEMENTS_NAME).open("w", encoding="utf-8") as handle:
        for disagreement in disagreements:
            handle.write(json.dumps(disagreement, ensure_ascii=False) + "\n")

    with (output_dir / AGREEMENTS_NAME).open("w", newline="", encoding="utf-8") as handle:
        fields = ("program_id", "task_id", "pattern_label", "consensus_source")
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(agreements_rows)

    input_hashes = {
        "claude": sha256(claude_path),
        "codex": sha256(codex_path),
        "blinded_packet": sha256(packet_path),
    }
    summary = {
        "status": "READY_FOR_THIRD_PARTY_ADJUDICATION",
        "programs": n,
        "agreements": agreements,
        "disagreements": len(disagreements),
        "raw_agreement": observed,
        "chance_expected_agreement": expected,
        "cohens_kappa": kappa,
        "claude_distribution": dict(sorted(claude_counts.items())),
        "codex_distribution": dict(sorted(codex_counts.items())),
        "disagreements_by_pattern": {
            annotator: dict(sorted(counts.items()))
            for annotator, counts in disagreements_by_label.items()
        },
        "agreement_by_label": agreement_by_label,
        "agreement_by_confidence_pair": confidence_pairs,
        "inputs_sha256": input_hashes,
        "original_labels_modified": False,
        "final_manifest_created": False,
        "required_final_label_sources": ["model-consensus", "model-adjudicated"],
    }
    (output_dir / SUMMARY_NAME).write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    write_audit(
        output_dir / AUDIT_NAME,
        n=n,
        agreements=agreements,
        disagreements=len(disagreements),
        observed=observed,
        expected=expected,
        kappa=kappa,
        matrix=matrix,
        codex_counts=codex_counts,
        agreement_by_label=agreement_by_label,
        confidence_pairs=confidence_pairs,
        input_hashes=input_hashes,
    )
    return summary


def self_test() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        packet = root / "packet.jsonl"
        packet.write_text(
            "\n".join(
                json.dumps({
                    "index": i, "program_id": str(i), "task_id": f"task_{i}",
                    "buggy_source": "print(0)\n", "difficulty": i,
                })
                for i in range(1, 5)
            ) + "\n",
            encoding="utf-8",
        )
        cases = (
            ("claude", ["greedy", "greedy", "simulation", "outside_vocabulary"],
             ["high", "high", "medium", "low"]),
            ("codex", ["greedy", "simulation", "simulation", "outside_vocabulary"],
             ["high", "medium", "high", "medium"]),
        )
        for name, labels, confidences in cases:
            with (root / f"{name}.csv").open("w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["program_id", "task_id", "pattern_label", "confidence"])
                for i, (label, confidence) in enumerate(zip(labels, confidences), 1):
                    writer.writerow([i, f"task_{i}", label, confidence])
        out = root / "out"
        summary = write_comparison(root / "claude.csv", root / "codex.csv", packet, out)
        assert summary["programs"] == 4
        assert summary["agreements"] == 3
        assert summary["disagreements"] == 1
        assert summary["raw_agreement"] == 0.75
        assert abs(summary["cohens_kappa"] - (7 / 11)) < 1e-12
        disagreement = json.loads((out / DISAGREEMENTS_NAME).read_text())
        assert set(disagreement) == {
            "program_id", "task_id", "buggy_source", "allowed_task_metadata",
            "claude_label", "codex_label", "claude_confidence", "codex_confidence",
        }
        with (out / AGREEMENTS_NAME).open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        assert len(rows) == 3
        assert set(rows[0]) == {
            "program_id", "task_id", "pattern_label", "consensus_source",
        }
        assert all(
            row["consensus_source"] == "claude-codex-blinded-agreement" for row in rows
        )
    print("self-test: PASS")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--claude", type=Path)
    parser.add_argument("--codex", type=Path)
    parser.add_argument(
        "--blinded-records", type=Path,
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
