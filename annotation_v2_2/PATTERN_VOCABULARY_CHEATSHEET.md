# Pattern Vocabulary Cheat-Sheet (for v2.2 blinded annotation)

Condensed, faithful copy of `pilot/PATTERN_VOCABULARY.md` (FROZEN v1) for
quick reference during annotation. **The source of truth is
`pilot/PATTERN_VOCABULARY.md`** — if anything here ever looks inconsistent
with it, trust the original file. Definitions and confusable-pair notes are
reproduced verbatim from there; nothing has been added, removed, or
reworded.

Apply these definitions to **the candidate's own buggy submission's
structure** (per `pilot/ANNOTATION_GUIDE.md` §2): does the code attempt this
technique, regardless of whether it correctly or buggily implements it?
Task metadata (contest/problem, difficulty) may help you guess the
*intended* technique, but the label should reflect what the **submission
itself attempts**, per the vocabulary's own inclusion rule.

| Key | Slug | Display name | Definition | Confuse with |
|---|---|---|---|---|
| **1** | `two_pointers` | two pointers | Two (or more) index variables advance through one or more linear structures under a monotonic or converging rule, replacing an O(n²) nested scan. | `sliding_window` (window pointers move together over a contiguous range with a running aggregate → prefer sliding_window). `sorting_based` (if the two-ended scan only exists to consume an already-sorted array and the sort is the hard part, prefer sorting_based; if the two-ended scan itself is the algorithmic idea, prefer two_pointers). |
| **2** | `sliding_window` | sliding window | Maintains a contiguous subrange with an incrementally updated invariant (sum, count, distinct-count) via expand/shrink steps. | `two_pointers` (see above). `prefix_sums` (if the window aggregate is recomputed from scratch via prefix differences rather than incremental expand/shrink, label prefix_sums). |
| **3** | `binary_search` | binary search | Repeatedly halves a monotonic search space (an array, or "binary search on the answer") via a midpoint and a predicate. | `sorting_based` (binary search over an array assumes it's sorted; still label binary_search if the intended/attempted technique is the search itself, by hand or via `bisect`). |
| **4** | `prefix_sums` | prefix sums | Precomputes a cumulative aggregate array so any range query is O(1) via two prefix lookups. | `sliding_window` (see above). Does NOT include general DP tables — prefix_sums is specifically a running-total structure for range queries, not a recurrence with branching transitions. |
| **5** | `dynamic_programming` | dynamic programming | Defines a recurrence over overlapping subproblems, stored in a table or memo, built from explicit base case(s) via a defined fill/recursion order. | `greedy` (label by the submission's own structure: does it build a table/memo? If yes, dynamic_programming even if the recurrence is buggy). `brute_force_implementation` (unmemoized exhaustive recursion with NO table/memo is brute_force_implementation — the memo/table's presence is the defining feature, not correctness). |
| **6** | `greedy` | a greedy strategy | Builds a solution by repeatedly taking the locally-best choice under a fixed selection/sort criterion, never reconsidering past choices. | `sorting_based` (label greedy when the post-sort iterative choice-and-commit loop is the algorithmic core; sorting_based when sorting is the core and the scan after is a simple pass with no "choice" semantics). |
| **7** | `graph_traversal_dfs_bfs` | graph/grid traversal (DFS or BFS) | Explores a graph or grid from one or more sources with DFS (recursion/explicit stack) or BFS (queue), tracking visited state. DFS and BFS share this one slug. | `brute_force_implementation` (an explicit worklist without proper visited-tracking is STILL graph_traversal_dfs_bfs if a graph/grid is being explored — the missing visited-check is the bug this pattern's prior targets, not a reason to relabel). |
| **8** | `sorting_based` | a sort-then-scan approach | Correctness depends on processing values in sorted order (comparator or library sort) followed by a linear or two-pointer pass. | `two_pointers`, `greedy`, `binary_search` (see their notes — sorting_based is the residual category when the post-sort logic is not itself pointer-convergence, greedy choice-commitment, or search). |
| **9** | `hash_map_counting` | hash-map / hash-set counting | Uses a hash map/set to count occurrences or record "seen" state in one pass. | `brute_force_implementation` (an O(n²) nested-loop counting solution that does NOT use a hash map/set is brute_force_implementation, even if it computes the same thing). |
| **10** | `brute_force_implementation` | direct brute-force implementation | Directly simulates/enumerates the specification with nested loops or a direct formula; no algorithmic shortcut. | `simulation` (brute_force_implementation enumerates a *search space* looking for an answer, e.g. try every pair/subset; simulation steps through a *described process over time/turns* regardless of search). |
| **11** | `intervals` | interval merging/scheduling | Represents data as (start, end) ranges and reasons about overlap, merging, or scheduling, typically via sorting endpoints and a sweep. | `sorting_based`/`greedy` (label intervals when the interval representation and overlap/merge logic is the defining structure, even if the selection rule is greedy). |
| **12** | `simulation` | step-by-step simulation | Directly steps through a described process (turns, time steps, physical moves), applying the stated rules at each step. | `brute_force_implementation` (see above). |

## Other keys in the annotation CLI

| Key | Meaning |
|---|---|
| `o` | **outside_vocabulary** — the candidate's intended technique does not fit any of the 12 classes above (e.g., pure math/number-theory formula derivation with no iterative structure, union-find, segment trees, Fenwick trees, bit-DP as its own idiom beyond a plain table). Per `pilot/PATTERN_VOCABULARY.md`'s inclusion rule, do not force-fit — mark outside_vocabulary and give a one-word reason (e.g., "DSU", "SegTree", "pure math"). |
| `u` | **uncertain** — you are not ready to commit; the program is queued for a later revisit pass. Not a final label; does not count toward completion. |
| `s` | **skip** — same as uncertain but no note is requested (fastest way to defer a hard case). |

## Confidence levels (required for every confirmed label)

- **high** — the code's structure unambiguously matches one class, or task
  context (contest/problem, difficulty) strongly corroborates it.
- **medium** — a reasonable, defensible call, but a plausible alternative
  label exists (see the "confuse with" column above).
- **low** — a forced choice among multiple weakly-defensible options; flag
  these mentally as candidates for a second look before the final freeze.

## Reminder: label what the submission attempts, not what it should have done

Per `pilot/ANNOTATION_GUIDE.md` §2 step 2: read the **buggy submission's own
structure** to confirm it is attempting a technique — do not assume the
"intended" technique from difficulty/contest alone if the code visibly
attempts something else. If the task admits multiple valid techniques and
the submission is ambiguous, prefer the technique whose structural signature
is actually present in the code (a table/memo present → `dynamic_programming`;
a sort followed by sequential choice-commitment → `greedy`).
