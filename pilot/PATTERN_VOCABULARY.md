# Pattern Vocabulary (FROZEN v1)

**Status:** Frozen by the Claude scientific-specification handoff (`agent/claude-science`), 2026-09-10.
**Scope:** applies to the current pilot (`pilot/config/pilot.yaml`, `dataset.target: ConDefects-Python`, `target_n: 30`) and is intended to carry forward unchanged into the confirmatory corpus (dossier `dossier/99_synthesis.md` §S1, n=300–500).
**Do not edit class names or slugs without a new version number and a changelog entry** — every other frozen file (`PATTERN_PRIORS.md`, `pattern_priors.json`, `pilot/prompts/pattern_prior.txt`, `ANNOTATION_GUIDE.md`) keys off these exact slugs.

Grounding: this is exactly the 12-class vocabulary recommended in `dossier/99_synthesis.md` §S1 ("Pattern vocabulary (10–12 classes, calibrated to Block 2 feasibility evidence)"), citing Watanobe et al. 2023 (structural CNN, F1 95.7 on 6–7 categories, `dossier/02_block2_classification.md` §2f), AlDeSCo's catalog (`dossier/02_block2_classification.md` §2d), and COFO's "Infer the Technique" task (`dossier/02_block2_classification.md` §2a/2f). Feasibility evidence is at the *category* level; this document adds the finer-grained decomposition the localization task needs.

## Canonical slugs

The `pattern_label` field in every manifest record MUST be exactly one of the 12 slugs below (lowercase, `snake_case`, no synonyms, no trailing/leading whitespace). `pattern_priors.json` uses these same 12 strings as its top-level keys.

| # | Slug (`pattern_label`) | Display name (for prior text) |
|---|---|---|
| 1 | `two_pointers` | two pointers |
| 2 | `sliding_window` | sliding window |
| 3 | `binary_search` | binary search |
| 4 | `prefix_sums` | prefix sums |
| 5 | `dynamic_programming` | dynamic programming |
| 6 | `greedy` | a greedy strategy |
| 7 | `graph_traversal_dfs_bfs` | graph/grid traversal (DFS or BFS) |
| 8 | `sorting_based` | a sort-then-scan approach |
| 9 | `hash_map_counting` | hash-map / hash-set counting |
| 10 | `brute_force_implementation` | direct brute-force implementation |
| 11 | `intervals` | interval merging/scheduling |
| 12 | `simulation` | step-by-step simulation |

## Class definitions, scope, and boundary rules

Each definition below states what belongs in the class and the most common confusion to rule out. Annotators (see `ANNOTATION_GUIDE.md`) apply these definitions to (a) the AtCoder/Codeforces task's *reference/intended* solution technique and (b) a read of the candidate's *buggy* submission to confirm it is attempting the same technique (a submission using a structurally different technique than the task's canonical one is not automatically excluded, but its `pattern_label` follows the submission's attempted technique, not the task's; if these ever disagree, see the adjudication rule in `ANNOTATION_GUIDE.md`).

1. **`two_pointers`** — two (or more) index variables advance through one or more linear structures under a monotonic or converging rule, replacing an O(n²) nested scan. *Confuse with:* `sliding_window` (window pointers move together to maintain an invariant over a contiguous range — if the code maintains a running aggregate over `[left, right)`, prefer `sliding_window`) and `sorting_based` (if the two pointers only exist to consume an already-sorted array from both ends after a sort, both labels are defensible; prefer `two_pointers` if the two-ended scan is the *algorithmic idea*, `sorting_based` if the sort is the hard part and the scan is trivial single-direction cleanup).

2. **`sliding_window`** — maintains a contiguous subrange with an incrementally updated invariant (sum, count, distinct-count) via expand/shrink steps. *Confuse with:* `two_pointers` (see above) and `prefix_sums` (if the window's aggregate is recomputed from scratch via prefix differences rather than incremental expand/shrink, label `prefix_sums`).

3. **`binary_search`** — repeatedly halves a monotonic search space (an array or an answer domain, i.e. "binary search on the answer") via a midpoint and a predicate. *Confuse with:* `sorting_based` (binary search over an array assumes it is sorted; if sorting is the only nontrivial step and lookup is a single `bisect`-style call with no custom predicate, this is still `binary_search` if the intended technique is binary search — annotate by which part the submission actually implements by hand).

4. **`prefix_sums`** — precomputes a cumulative aggregate array so that any range query is O(1) via two prefix lookups. *Confuse with:* `sliding_window` (see above); *does not include* general dynamic-programming tables even though a DP table is also "precomputed" — `prefix_sums` is specifically a 1D (or per-dimension) running-total structure used for range queries, not a recurrence with branching transitions.

5. **`dynamic_programming`** — defines a recurrence over overlapping subproblems, stored in a table or memo, built from explicit base case(s) via a defined fill/recursion order. *Confuse with:* `greedy` (if the submission's comment/structure suggests the author *intended* a greedy exchange-argument solution but the task actually requires DP, label by the submission's own structure: does it build a table/memo? If yes, `dynamic_programming` regardless of whether the recurrence is buggy); `brute_force_implementation` (unmemoized exhaustive recursion without a table is `brute_force_implementation`, not `dynamic_programming` — the memo/table is the defining feature).

6. **`greedy`** — builds a solution by repeatedly taking the locally-best choice under a fixed selection/sort criterion, never reconsidering past choices. *Confuse with:* `sorting_based` (nearly all greedy solutions sort first; label `greedy` when the *post-sort* iterative choice-and-commit loop is the algorithmic core, `sorting_based` when sorting is the core and the scan after it is a simple linear pass with no "choice" semantics, e.g. finding max gap between sorted elements).

7. **`graph_traversal_dfs_bfs`** — explores a graph or grid from one or more sources with DFS (recursion/explicit stack) or BFS (queue), tracking visited state. DFS and BFS share one slug in this vocabulary (dossier `dossier/99_synthesis.md` §S1: "Confusable pairs (BFS vs DFS) stay as separate classes only if annotator agreement supports it" — no annotator-agreement data exists yet at pilot scale, so they are merged; revisit only after the confirmatory corpus has enough double-annotated examples to measure κ separately for the split). *Confuse with:* `brute_force_implementation` (a traversal implemented as an explicit worklist without proper visited-tracking is still `graph_traversal_dfs_bfs` if a graph/grid is being explored — the missing visited-check is exactly the kind of bug this pattern's prior targets, not a reason to relabel).

8. **`sorting_based`** — correctness depends on processing values in sorted order (via a comparator or library sort) followed by a linear or two-pointer pass. *Confuse with:* `two_pointers`, `greedy`, `binary_search` (see above notes in each entry — `sorting_based` is the residual category when the post-sort logic is not itself doing pointer-convergence, greedy choice-commitment, or search).

9. **`hash_map_counting`** — uses a hash map/set to count occurrences or record "seen" state in one pass. *Confuse with:* `brute_force_implementation` (an O(n²) nested-loop counting solution that does *not* use a hash map/set is `brute_force_implementation`, even if it computes the same thing a hash map would).

10. **`brute_force_implementation`** — directly simulates/enumerates the specification with nested loops or a direct formula; no algorithmic shortcut. *Confuse with:* `simulation` (see below — `brute_force_implementation` enumerates a *search space* looking for an answer, e.g. try every pair/subset; `simulation` steps through a *described process over time/turns* regardless of search).

11. **`intervals`** — represents data as (start, end) ranges and reasons about overlap, merging, or scheduling, typically via sorting endpoints and a sweep. *Confuse with:* `sorting_based`/`greedy` (interval scheduling problems are often also greedy; label `intervals` when the interval representation and overlap/merge logic is the defining structure of the code, even if the selection rule is greedy).

12. **`simulation`** — directly steps through a described process (turns, time steps, physical moves), applying the stated rules at each step. *Confuse with:* `brute_force_implementation` (see above).

## Inclusion rule for the pilot manifest

A program may only carry a `pattern_label` from this table. If a candidate program's intended technique does not fit any of the 12 classes (e.g., pure math/number-theory formula derivation with no iterative structure, or a technique outside this list such as union-find, segment trees, or bit-DP), it must be marked `inclusion_status: excluded` with `exclusion_reason: "pattern outside frozen vocabulary v1"` rather than force-fit into the nearest class. This preserves the meaning of the McNemar test's population (dossier `dossier/05_block5_methodology.md` §5.5) and keeps the prior's coverage well-defined. Expanding the vocabulary is possible for the confirmatory corpus but requires a new frozen version of this document and of every file that keys off it.
