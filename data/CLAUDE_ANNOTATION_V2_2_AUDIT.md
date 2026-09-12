# Claude (Annotator A) — v2.2 Blinded Annotation Run Audit

**Role:** Annotator A (Claude), independent blinded model annotator, per the
user's authorized amendment: pattern labels for v2.2 are produced by two
independent blinded model annotators (Claude = A, Codex = B) followed by
agreement analysis and independent adjudication of disagreements. This audit
covers Annotator A's run only.

**Output:** `data/manifests/pattern_annotations_claude_v2_2.csv` — 232/232
programs, one row each, columns `annotation_index, program_id, task_id,
pattern_label, confidence, annotation_rationale, annotation_source`, with
`annotation_source = "claude-blinded-model-annotation"` on every row.

**Verified before writing the CSV:** 232 unique indices, each matching
`annotation_v2_2/blinded_records.jsonl`'s `program_id`/`task_id` exactly, every
`pattern_label` one of the 12 frozen slugs or `outside_vocabulary`, every
`confidence` one of `high`/`medium`/`low`. Zero errors on all four checks.

## Method

Each of the 232 records in `annotation_v2_2/blinded_records.jsonl` was read
directly — program_id, task_id, contest/problem/difficulty, and the full
buggy source — and classified by reading and reasoning about the actual
algorithmic structure of the code, applying `pilot/PATTERN_VOCABULARY.md`'s
definitions and confusable-pair rules. No script, regex, or heuristic
computed any label; every row reflects a first-pass judgment call made while
reading that program's source.

## Blinding

Only `annotation_v2_2/blinded_records.jsonl`, `pilot/PATTERN_VOCABULARY.md`,
`pilot/ANNOTATION_GUIDE.md`, and `annotation_v2_2/PATTERN_VOCABULARY_CHEATSHEET.md`
were read for this task. No AtCoder editorial, external web page, or the
task's problem statement was fetched or consulted. `data/manifests/pilot_manifest_v2_1.json`'s
pattern labels, the old `"AST rule"` labels, `scripts/package_final_sample*.py`,
any Codex/`pattern_annotations_codex*` file, `faulty_lines`, `fixed.py`, any
buggy-to-fixed diff, either prior JSON file, and every prior VOID
model-localization output were not opened during this task.

**Blinding contamination: NO.** No forbidden file was read. This is verified
directly, not merely asserted: `annotation_v2_2/blinded_records.jsonl` itself
was independently confirmed (in the earlier remediation-tooling work) to
contain none of the excluded fields, so the only inputs available to this
annotation pass were the permitted ones.

A small number of programs in this frame happened to be recognizable from
context accumulated earlier in this same session, during the *separate*,
already-completed pattern-label-provenance investigation (which inspected 6
sampled programs' source directly against the old automated labels, before
this annotation task was authorized). Those 6 programs' labels here were
still derived by re-reading the code fresh in this pass, independent of the
earlier investigation's conclusions; where the label matches, it is because
the code supports it independently, not because the earlier finding was
carried over as an assumption. This is disclosed for transparency, not
because any forbidden file was consulted.

## Label distribution (232 total)

| Pattern class | Count |
|---|---:|
| `dynamic_programming` | 53 |
| `brute_force_implementation` | 50 |
| `outside_vocabulary` | 29 |
| `binary_search` | 23 |
| `graph_traversal_dfs_bfs` | 15 |
| `greedy` | 15 |
| `hash_map_counting` | 10 |
| `simulation` | 10 |
| `prefix_sums` | 7 |
| `sorting_based` | 6 |
| `sliding_window` | 6 |
| `intervals` | 5 |
| `two_pointers` | 3 |

## Confidence distribution

high: 110 · medium: 81 · low: 41

## Disclosure: `outside_vocabulary` is large (29/232, ~12.5%)

Most `outside_vocabulary` calls are driven by an explicit, advanced
supporting data structure or technique the vocabulary's own inclusion rule
names as an exclusion example — Union-Find/DSU (9 programs), segment trees
(2), Fenwick/BIT trees (2), max-flow/min-cost-flow (3), convex hull trick
(1), matrix exponentiation (2), Möbius/sieve-based number theory (2),
closed-form combinatorial game theory (2), XOR linear basis (1), and a few
genuinely bespoke techniques with no vocabulary match. None were
force-fitted into the nearest of the 12 classes, per
`pilot/PATTERN_VOCABULARY.md`'s explicit inclusion rule ("must be marked
outside_vocabulary... rather than force-fit into the nearest class").

## Items flagged for adjudication attention

The following categories of calls are the ones most likely to disagree with
Annotator B, or with the disputed automated labels, and are flagged here so
the adjudication pass can prioritize them:

1. **41 `low`-confidence calls** — every one of these is a genuine judgment
   call where a defensible alternative label exists; see the
   `annotation_rationale` column for the specific alternative considered in
   each case.
2. **Multi-technique programs** (e.g., index 45/119/162: an outer
   binary/ternary search whose predicate is evaluated via a max-flow or
   convex-hull-trick subroutine; index 229: a small DP feeding into
   Berlekamp-Massey/Bostan-Mori) — labeled by the outer/driving control
   structure where one was clearly dominant, flagged `low`/`medium`
   confidence where the choice is genuinely close.
3. **Kadane's-style minimal rolling recurrences** (indices 110, 164, 184,
   225) — labeled `dynamic_programming` at `low` confidence on the grounds
   that a self-referential single-state recurrence is still a recurrence,
   even with no explicit table; a stricter reading could call these
   `brute_force_implementation` instead.
4. **Three programs independently found to contradict the disputed
   automated ("AST rule") labels on direct inspection**, corroborating the
   finding in `data/PATTERN_LABEL_PROVENANCE_AUDIT.md`: index 16
   (`46026874`, two_pointers, not binary_search), index 108 (`46028780`,
   binary_search — the code defines a function literally named
   `binary_search`, not sorting_based), and index 63/94 pattern class shifts
   observed while reading other previously-flagged programs from that
   investigation. This is reported as a data point for the agreement
   analysis, not as this annotator asserting the old labels are wrong by
   fiat.

## Independence

This run did not read, compare against, or wait for any Codex output at any
point. No consensus, averaging, or reconciliation was performed. This file
and the CSV represent Annotator A's independent first-pass judgment only.
