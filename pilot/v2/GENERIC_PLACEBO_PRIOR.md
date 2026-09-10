# Generic / Placebo Prior (FROZEN v2) — design, text, and matching audit

**Status:** frozen 2026-09-10, designed **before** dataset selection and before any experimental result exists.
**Machine-readable form:** `pilot/v2/generic_placebo_prior.json` (must be byte-identical to the text quoted in §2).
**Role:** arm **B** of the v2 design (`PILOT_PROTOCOL_V2.md` §2). The primary comparison C vs B rests entirely on this text being a *fair* counterpart to the pattern-specific priors.

## 1. Design requirements

The placebo must satisfy two requirements that pull against each other, and the tension is the whole point:

- **It must contain no algorithm-pattern-specific information.** No mention of pointers, windows, midpoints, prefixes, recurrences, memos/tables, base cases, graph or grid traversal, visited-marking, sorting keys, hashing, intervals, or step-wise simulation. Verified mechanically (§4).
- **It must be a genuinely competent generic debugging checklist — a strong control, not a straw man.** If the placebo were deliberately vacuous, a positive C-vs-B result would measure placebo weakness rather than pattern value, and the design would fail at exactly the thing it was built to do. The four generic checkpoints below are the failure classes that recur across the novice-error literature independent of algorithm family (off-by-one and loop bounds; comparison-operator direction; accumulator initialization and update order; boundary/edge cases) — see Ettles, Luxton-Reilly & Denny 2018 and Alzahrani & Vahid 2021 in `dossier/01_block1_theory.md` §1d (items D7, D8), whose catalogs are explicitly pattern-agnostic. That pattern-agnostic catalog is precisely what a fair placebo should deliver.

**Consequence, stated in advance:** because a competent generic checklist necessarily overlaps with the generic *parts* of each pattern checklist, the measured C − B effect is a **conservative lower bound** on the value of pattern-specific information. This biases against the project's hypothesis. That is the correct direction for a control to bias.

## 2. Frozen text

Two variants exist for one reason only: to match the checkpoint count of the pattern prior the same program would receive in arm C (10 of the 12 pattern priors have 4 checkpoints; `two_pointers` and `dynamic_programming` have 5, per `pilot/PATTERN_PRIORS.md`). The variants are otherwise the same checklist, and checkpoints 1–4 are byte-identical between them. The number of checkpoints carries no pattern information to the model, which sees exactly one program in one call and cannot compare across programs.

**4-checkpoint variant** (127 words, 805 characters) — used for `binary_search`, `brute_force_implementation`, `graph_traversal_dfs_bfs`, `greedy`, `hash_map_counting`, `intervals`, `prefix_sums`, `simulation`, `sliding_window`, `sorting_based`:

```
This program contains a logical fault. Before ranking the full source, check these standard failure points for buggy programs first, in order:
1. check whether every loop's start and end bounds are correct, including whether an endpoint should be inclusive or exclusive
2. check whether each comparison or conditional test uses the right operator and the right direction, including strict versus non-strict comparisons
3. check whether variables that accumulate or track state are initialized correctly and updated in the right order relative to their use
4. check whether the boundary cases are handled, such as the first item, the last item, or an empty or single-element input
These are hypotheses, not conclusions -- after checking them, still weigh every line of the source by the instructions above.
```

**5-checkpoint variant** (144 words, 896 characters) — used for `two_pointers` and `dynamic_programming`; identical to the above plus checkpoint 5:

```
5. check whether the final value printed or returned is the one the task actually asks for
```

## 3. Structural parity with the pattern priors

| Dimension | Pattern prior (arm C) | Generic prior (arm B) | Matched? |
|---|---|---|---|
| Opening sentence shape | "This program is intended to solve the task using X. Before ranking the full source, check these standard failure points for this pattern first, in order:" | "This program contains a logical fault. Before ranking the full source, check these standard failure points for buggy programs first, in order:" | Yes — same clause structure, same instruction to check listed points first, in order |
| Body format | numbered list, each item beginning "check whether…" | numbered list, each item beginning "check whether…" | Yes, byte-level format identical |
| Checkpoint count | 4, or 5 for `two_pointers` / `dynamic_programming` | 4, or 5 for the same two labels | Yes, per label |
| Closing sentence | "These are hypotheses, not conclusions -- after checking them, still weigh every line of the source by the instructions above." | identical string | Yes, byte-identical (verified in §4) |
| Level of specificity | names concrete code constructs, never program-specific facts | names concrete code constructs, never program-specific facts | Yes |
| Instructional tone | hedged ("check whether", "hypotheses, not conclusions") | hedged, same phrases | Yes |
| Delimiter block | `<ALGORITHMIC_PATTERN_PRIOR>` | `<ALGORITHMIC_PATTERN_PRIOR>` | Yes — same tag; see the disclosed residual asymmetry in `PROMPT_DIFF_V2.md` §4 |
| Word count | 119–138 | 127 or 144 | Within declared tolerance (§4) |

## 4. Matching audit (mechanically measured, not estimated)

Measured by script against the two frozen JSON files; every number below is script output, not a hand count.

| `pattern_label` | C words | B words | \|Δ\| | C items | B items |
|---|---|---|---|---|---|
| `two_pointers` | 138 | 144 | 6 | 5 | 5 |
| `sliding_window` | 128 | 127 | 1 | 4 | 4 |
| `binary_search` | 127 | 127 | 0 | 4 | 4 |
| `prefix_sums` | 122 | 127 | 5 | 4 | 4 |
| `dynamic_programming` | 136 | 144 | 8 | 5 | 5 |
| `greedy` | 131 | 127 | 4 | 4 | 4 |
| `graph_traversal_dfs_bfs` | 134 | 127 | 7 | 4 | 4 |
| `sorting_based` | 121 | 127 | 6 | 4 | 4 |
| `hash_map_counting` | 128 | 127 | 1 | 4 | 4 |
| `brute_force_implementation` | 131 | 127 | 4 | 4 | 4 |
| `intervals` | 119 | 127 | 8 | 4 | 4 |
| `simulation` | 127 | 127 | 0 | 4 | 4 |

- **Word-count deviation: max 8, mean 4.2.**
- **Character-count deviation: max 62 (7.5%), mean 38.1 (4.8%).**
- **Checkpoint count: matched exactly for all 12 labels.**
- **Closing sentence: identical across all 24 strings.**
- **Pattern-vocabulary leakage scan of the placebo text: clean** — none of `pointer, window, binary search, midpoint, prefix, recurrence, memo, base case, greedy, graph, grid, DFS, BFS, visited, enqueue, dequeue, sort, hash, interval, simulation, brute, table, neighbor, traversal, predecessor, sentinel, dedup, shrink, expand` appears in either variant.

### Pre-declared tolerance

Exact per-label word matching is impossible: the placebo is one text (two variants) while the pattern priors are twelve different texts spanning 119–138 words. **Declared acceptable tolerance: |Δwords| ≤ 10 per label, and checkpoint count matched exactly.** Both hold (max observed 8). Character deviation is reported for transparency but is not the matching criterion, since token count tracks words more closely than characters and the character gap is driven by pattern-specific terms being longer words.

**How this is verified against the real prompts at analysis time:** `analysis/run_analysis.py` already emits `adversarial.prompt_length_by_condition` (mean chars and estimated tokens per condition) for each session. The predicted realized gap between arm B and arm C is small and of unknown sign (B is longer for 5 labels, shorter for 6, equal for 1). If the measured B-vs-C prompt-length gap materially exceeds what these 24 strings imply, that indicates a prompt-construction bug, not a finding.

## 5. What this placebo does and does not license

- It **does** let C vs B distinguish "pattern-specific structural information helps" from "additional structured debugging guidance helps."
- It **does not** control for the *semantic relevance* of the guidance to the specific program — a pattern prior is, by construction, selected per program, while the placebo is constant. A residual interpretation therefore survives: "guidance tailored to the program in any way helps, whether or not the tailoring is pattern-based." Distinguishing *that* would require a third kind of prior (e.g. a per-program checklist tailored on some non-pattern axis), which is out of scope for an n=30 pilot and is recorded as a known limitation in `PRE_RUN_REVIEW_V2.md` and `CLAIM_BOUNDARIES_V2.md`.
- It **does not** make the pilot confirmatory. n=30 remains a calibration sample.

## 6. Freeze

This text may not be reworded after any result is seen, in either direction — not to strengthen it (making C look worse) and not to weaken it (making C look better). `pilot/PRE_EXPERIMENT_COMMIT.md` rule 2 extends to this file. Any future revision requires a v3 with a dated changelog entry, applied before the next data collection, never retroactively.
