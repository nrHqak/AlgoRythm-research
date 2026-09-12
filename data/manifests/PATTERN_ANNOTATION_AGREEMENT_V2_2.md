# Pattern Annotation Agreement Audit — v2.2

Generated at 2026-09-12T15:16:06.262844+00:00 by `scripts/compare_pattern_annotations_v2_2.py`.

## Independent annotation design

Annotator A (Claude) and Annotator B (Codex) each completed an independent blinded model annotation pass over the same frozen 232-program frame. Comparison was deferred until both passes were complete. Neither original annotation CSV was modified by this comparison.

Exact matches are eligible to become model-consensus labels. Conflicts remain unresolved and require model-adjudicated labels from an independent third adjudicator; this comparison does not create a final v2.2 manifest.

## Blinding

The comparison joins the two label files only to the sanitized blinded packet. The disagreement artifact exposes buggy source plus the permitted task metadata (`contest`, `problem_letter`, `difficulty`, `atcoder_url`, and `loc`) and the two current labels/confidences. It excludes fault locations, fixed source, prior-manifest labels, pattern priors, previous localization results, and old v2.1 AST labels.

## Overall agreement

- Programs compared: **232**
- Exact agreements: **182**
- Disagreements: **50**
- Raw agreement: **0.784483 (78.45%)**
- Chance-expected agreement: **0.130035 (13.00%)**
- Cohen's kappa: **0.752269**
- `outside_vocabulary` is treated as a valid, distinct category.
- Distinct labels are not merged or normalized.

## Agreement by pattern label

The symmetric label agreement rate is exact matches for a label divided by the union of programs assigned that label by either annotator.

| Pattern label | Claude count | Codex count | Exact matches | Union | Agreement |
|---|---:|---:|---:|---:|---:|
| `two_pointers` | 3 | 6 | 2 | 7 | 28.57% |
| `sliding_window` | 6 | 5 | 5 | 6 | 83.33% |
| `binary_search` | 23 | 14 | 14 | 23 | 60.87% |
| `prefix_sums` | 7 | 9 | 6 | 10 | 60.00% |
| `dynamic_programming` | 53 | 45 | 45 | 53 | 84.91% |
| `greedy` | 15 | 14 | 11 | 18 | 61.11% |
| `graph_traversal_dfs_bfs` | 15 | 13 | 13 | 15 | 86.67% |
| `sorting_based` | 6 | 8 | 6 | 8 | 75.00% |
| `hash_map_counting` | 10 | 4 | 4 | 10 | 40.00% |
| `brute_force_implementation` | 50 | 42 | 37 | 55 | 67.27% |
| `intervals` | 5 | 5 | 4 | 6 | 66.67% |
| `simulation` | 10 | 20 | 10 | 20 | 50.00% |
| `outside_vocabulary` | 29 | 47 | 25 | 51 | 49.02% |
| `uncertain` | 0 | 0 | 0 | 0 | N/A |

## Full confusion matrix

| Claude label \ Codex label | two_pointers | sliding_window | binary_search | prefix_sums | dynamic_programming | greedy | graph_traversal_dfs_bfs | sorting_based | hash_map_counting | brute_force_implementation | intervals | simulation | outside_vocabulary | uncertain | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `two_pointers` | 2 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 |
| `sliding_window` | 0 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 6 |
| `binary_search` | 1 | 0 | 14 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 8 | 0 | 23 |
| `prefix_sums` | 0 | 0 | 0 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 7 |
| `dynamic_programming` | 1 | 0 | 0 | 0 | 45 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 6 | 0 | 53 |
| `greedy` | 2 | 0 | 0 | 1 | 0 | 11 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 15 |
| `graph_traversal_dfs_bfs` | 0 | 0 | 0 | 0 | 0 | 0 | 13 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 15 |
| `sorting_based` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 6 |
| `hash_map_counting` | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 4 | 2 | 0 | 2 | 1 | 0 | 10 |
| `brute_force_implementation` | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 1 | 0 | 37 | 0 | 4 | 6 | 0 | 50 |
| `intervals` | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 4 | 0 | 0 | 0 | 5 |
| `simulation` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 10 | 0 | 0 | 10 |
| `outside_vocabulary` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 2 | 0 | 1 | 25 | 0 | 29 |
| `uncertain` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **Total** | 6 | 5 | 14 | 9 | 45 | 14 | 13 | 8 | 4 | 42 | 5 | 20 | 47 | 0 | 232 |

Rows are Claude labels; columns are Codex labels.

## Agreement by confidence pair

| Claude confidence | Codex confidence | Programs | Exact matches | Agreement |
|---|---|---:|---:|---:|
| `high` | `high` | 106 | 103 | 97.17% |
| `high` | `medium` | 4 | 3 | 75.00% |
| `low` | `high` | 23 | 11 | 47.83% |
| `low` | `medium` | 18 | 8 | 44.44% |
| `medium` | `high` | 72 | 52 | 72.22% |
| `medium` | `medium` | 9 | 5 | 55.56% |

## Why disagreements require independent adjudication

A disagreement has no model-consensus label. Allowing either original annotator to resolve its own conflict would make the resolution dependent on a party to the disagreement. A third independent, blinded adjudicator must review only the permitted evidence in the disagreement artifact and choose the model-adjudicated label without access to the excluded answer-bearing fields.

## Reproducibility

- Claude CSV SHA-256: `5550f59f7e869deecdf6427f90b092576a81c6df9125870b0fe34e8c7b4ef773`
- Codex CSV SHA-256: `dc89712a1cfd056652f05899d816605fdce757ace3ba8d181974fd48879a5c40`
- Blinded packet SHA-256: `8a1924066287ec9b9110018e5e301736dd4d1921be9b4dc0d06396264bdf0b99`

**Final status: READY FOR THIRD-PARTY ADJUDICATION**
