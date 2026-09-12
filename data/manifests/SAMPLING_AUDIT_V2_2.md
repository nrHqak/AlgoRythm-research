# Sampling Audit — Pilot v2.2 Consensus-Only Freeze

**Amendment timing:** authorized before any valid scientific result existed.
**Sampling seed:** `20260910` (frozen; no rerolls).
**Scientific execution:** not run.
**Validation:** PASS.

## 1. Pre-results methodological amendment

The pilot uses **exact-consensus labels from two independent blinded model annotators**. Claude and Codex independently annotated the same 232-program task-independent frame before their outputs were compared.

- Independently annotated programs: **232**
- Exact agreements: **182**
- Disagreements: **50**
- Raw agreement: **78.4483%**
- Cohen's kappa: **0.752269**

The 50 disagreements were not adjudicated, and neither annotator was preferred over the other. Every disagreement was excluded uniformly with the reason: **"excluded from pilot: independent pattern annotators disagreed"**. The original disagreement artifact is preserved unchanged as audit evidence for future work.

This is a pilot-specific reliability filter intended to avoid introducing adjudicator-dependent labels.

**Limitation:** the resulting pilot represents programs with comparatively unambiguous algorithmic-pattern assignments and may not generalize to ambiguous programs.

No prior automated pattern labels, old sample membership, pattern priors, or scientific localization outputs were inputs to this rebuild. The v2.0 and v2.1 manifests and their raw packages were not modified.

## 2. Consensus eligibility funnel

| Stage | Retained | Excluded | Rule |
|---|---:|---:|---|
| Independent blinded annotations | 232 | 0 | Frozen task-independent frame |
| Exact consensus | 182 | 50 | `excluded from pilot: independent pattern annotators disagreed` |
| In-vocabulary consensus | 157 | 25 | Consensus `outside_vocabulary` excluded |
| Classes meeting threshold | 130 | 27 | Frozen class count >= 7 |
| Top-four class pools | 109 | 21 | Count descending; vocabulary-order tie break |
| Final sample | 30 | 79 not drawn | Seeded 8/8/7/7 draw without replacement |

## 3. Consensus class counts

Counts below exclude the 25 exact-consensus `outside_vocabulary` records.

| Frozen pattern class | Count | >= 7 | Selected rank | Allocation |
|---|---:|:---:|---:|---:|
| `two_pointers` | 2 | No | — | 0 |
| `sliding_window` | 5 | No | — | 0 |
| `binary_search` | 14 | Yes | 3 | 7 |
| `prefix_sums` | 6 | No | — | 0 |
| `dynamic_programming` | 45 | Yes | 1 | 8 |
| `greedy` | 11 | Yes | — | 0 |
| `graph_traversal_dfs_bfs` | 13 | Yes | 4 | 7 |
| `sorting_based` | 6 | No | — | 0 |
| `hash_map_counting` | 4 | No | — | 0 |
| `brute_force_implementation` | 37 | Yes | 2 | 8 |
| `intervals` | 4 | No | — | 0 |
| `simulation` | 10 | Yes | — | 0 |

## 4. Deterministic class selection and draw

Eligible classes were ranked by count descending, with ties broken by the frozen vocabulary order. The top four received allocations 8/8/7/7. Within each class, records were sorted by `program_id` and sampled without replacement using one `random.Random(20260910)` stream in class-rank order. No prior sample member was preserved by rule, no seed was changed, and no draw was rerolled.

| Rank | Program ID | Task ID | Consensus pattern | LOC | Faulty line | Dynamic B pass/fail; F pass/fail | Test package |
|---:|---|---|---|---:|---:|---|---|
| 1 | `39201856` | `arc157_e` | `dynamic_programming` | 93 | 34 | 2/4; 6/0 | `regenerated-cache-matches-frozen-counts` |
| 2 | `44805380` | `abc232_d` | `dynamic_programming` | 27 | 22 | 5/3; 8/0 | `regenerated-cache-matches-frozen-counts` |
| 3 | `35962547` | `abc237_f` | `dynamic_programming` | 141 | 136 | 5/3; 8/0 | `regenerated-cache-matches-frozen-counts` |
| 4 | `43438224` | `arc164_e` | `dynamic_programming` | 49 | 16 | 7/1; 8/0 | `regenerated-cache-matches-frozen-counts` |
| 5 | `45808089` | `abc314_e` | `dynamic_programming` | 26 | 22 | 5/3; 8/0 | `regenerated-cache-matches-frozen-counts` |
| 6 | `45759088` | `abc283_e` | `dynamic_programming` | 43 | 36 | 5/1; 6/0 | `regenerated-cache-matches-frozen-counts` |
| 7 | `52899692` | `abc345_e` | `dynamic_programming` | 49 | 2 | 7/1; 8/0 | `regenerated-cache-matches-frozen-counts` |
| 8 | `55029036` | `abc335_e` | `dynamic_programming` | 150 | 148 | 7/1; 8/0 | `regenerated-cache-matches-frozen-counts` |
| 9 | `31456138` | `arc139_c` | `brute_force_implementation` | 43 | 28 | 7/1; 8/0 | `regenerated-cache-matches-frozen-counts` |
| 10 | `43234248` | `arc148_b` | `brute_force_implementation` | 40 | 32 | 6/2; 8/0 | `regenerated-cache-matches-frozen-counts` |
| 11 | `45289055` | `abc257_a` | `brute_force_implementation` | 44 | 40 | 4/4; 8/0 | `regenerated-cache-matches-frozen-counts` |
| 12 | `55003503` | `abc327_c` | `brute_force_implementation` | 35 | 22 | 6/2; 8/0 | `regenerated-cache-matches-frozen-counts` |
| 13 | `44917428` | `abc275_c` | `brute_force_implementation` | 58 | 13 | 7/1; 8/0 | `regenerated-cache-matches-frozen-counts` |
| 14 | `52796362` | `abc326_d` | `brute_force_implementation` | 139 | 139 | 7/1; 8/0 | `official-archive-recovery-matches-frozen-counts` |
| 15 | `46196763` | `abc322_b` | `brute_force_implementation` | 26 | 14 | 7/1; 8/0 | `regenerated-cache-matches-frozen-counts` |
| 16 | `46169156` | `abc305_b` | `brute_force_implementation` | 35 | 21 | 6/2; 8/0 | `regenerated-cache-matches-frozen-counts` |
| 17 | `53927639` | `abc341_d` | `binary_search` | 27 | 14 | 7/1; 8/0 | `regenerated-cache-matches-frozen-counts` |
| 18 | `45923968` | `abc300_f` | `binary_search` | 26 | 14 | 4/1; 5/0 | `regenerated-cache-matches-frozen-counts` |
| 19 | `43171788` | `arc138_a` | `binary_search` | 25 | 25 | 2/2; 4/0 | `regenerated-cache-matches-frozen-counts` |
| 20 | `54010856` | `arc173_a` | `binary_search` | 34 | 4 | 7/1; 8/0 | `regenerated-cache-matches-frozen-counts` |
| 21 | `37067201` | `arc152_b` | `binary_search` | 27 | 4 | 7/1; 8/0 | `regenerated-cache-matches-frozen-counts` |
| 22 | `45895898` | `abc309_c` | `binary_search` | 51 | 36 | 7/1; 8/0 | `regenerated-cache-matches-frozen-counts` |
| 23 | `41991921` | `abc304_g` | `binary_search` | 48 | 43 | 5/1; 6/0 | `regenerated-cache-matches-frozen-counts` |
| 24 | `45971969` | `abc309_e` | `graph_traversal_dfs_bfs` | 37 | 36 | 3/5; 8/0 | `regenerated-cache-matches-frozen-counts` |
| 25 | `45325123` | `abc291_e` | `graph_traversal_dfs_bfs` | 35 | 15 | 7/1; 8/0 | `regenerated-cache-matches-frozen-counts` |
| 26 | `52795863` | `abc238_e` | `graph_traversal_dfs_bfs` | 25 | 22 | 6/1; 7/0 | `regenerated-cache-matches-frozen-counts` |
| 27 | `45545460` | `abc267_f` | `graph_traversal_dfs_bfs` | 80 | 49 | 2/1; 3/0 | `regenerated-cache-matches-frozen-counts` |
| 28 | `41991860` | `arc159_a` | `graph_traversal_dfs_bfs` | 29 | 23 | 7/1; 8/0 | `regenerated-cache-matches-frozen-counts` |
| 29 | `45463729` | `abc289_e` | `graph_traversal_dfs_bfs` | 32 | 20 | 5/3; 8/0 | `regenerated-cache-matches-frozen-counts` |
| 30 | `54718266` | `abc308_d` | `graph_traversal_dfs_bfs` | 30 | 27 | 6/1; 7/0 | `regenerated-cache-matches-frozen-counts` |

## 5. Disagreement exclusion record

All 50 records in `pattern_annotation_disagreements_v2_2.jsonl` are excluded from this pilot with the exact reason "excluded from pilot: independent pattern annotators disagreed". Their program IDs are:

`27132818`, `53188054`, `44313828`, `52524531`, `45003873`, `45104462`, `52975596`, `34500524`, `45028964`, `34423081`, `49178986`, `45303110`, `37231890`, `45472060`, `45479724`, `38346885`, `54495703`, `45457264`, `46165545`, `45077270`, `45766127`, `45654657`, `52742757`, `52726801`, `54659671`, `52762677`, `54267102`, `53505050`, `54869003`, `54232515`, `55000126`, `55104573`, `29987786`, `38752586`, `28174907`, `41861434`, `34093512`, `45004334`, `32337261`, `34662508`, `37666166`, `38915061`, `43795529`, `38471956`, `40932797`, `45995987`, `51141760`, `51178140`, `51792735`, `52671232`.

The disagreement artifact SHA-256 remains:

`bd21d66615a9a8fdd81ea303b19641c295e2ebc65ef22cd8f265450020a10ebf`

## 6. Validation

- Final manifest contains exactly 30 included programs: **PASS**
- All 30 `task_id` values are unique: **PASS**
- Every selected record has exact Claude-Codex consensus: **PASS**
- Zero disagreement records are selected: **PASS**
- All selected records match frozen single-line ground truth: **PASS**
- All selected records match frozen dynamic eligibility and packaged tests reproduce its counts: **PASS**
- Class quotas are exactly 8/8/7/7 in ranked-class order: **PASS**
- Every CSV row carries frozen seed `20260910`: **PASS**
- No scientific LLM experiment was run: **PASS**

## 7. Freeze hashes

- Consensus annotations CSV: `5a4a431715dfd8d5e793a986b020da6910cbd061e6de8689e753d4ec4eda29d9`
- Pilot manifest JSON: `9f2db14bd38647e611bed87c72c87f7c934a2c824388751e2969ad4cab9ef8fc`
- Pilot manifest CSV: `79d154c0bbabfb4beba8fc6bc50998efc0c017a07518d54a0344d02cd0cef075`

**Final status: V2.2 CONSENSUS SAMPLE FROZEN**
