# Pattern Priors (FROZEN v1) — rationale and full text

**Status:** Frozen by the Claude scientific-specification handoff (`agent/claude-science`), 2026-09-10.
**Machine-readable form:** `pilot/pattern_priors.json` (must be byte-identical to the "Frozen prior string" blocks quoted below — this is checked by the consistency script referenced in `CLAUDE_HANDOFF.md`).
**Template these follow:** `pilot/prompts/pattern_prior.txt`.
**How this gets into a prompt:** `PROMPT_DIFF.md`.

This is the "pattern-specific failure checklist" that `dossier/99_synthesis.md` §S2.2 calls "the scientific object" of the project — the operationalization of Spohrer & Soloway's finding that novice bugs concentrate at **plan boundaries** rather than uniformly across code (`dossier/01_block1_theory.md` §1d, item D3), and of Brooks' beacon theory (`dossier/01_block1_theory.md` §1b, item B1): an algorithmic pattern is a beacon set at a higher level of abstraction, and this checklist is that beacon set made explicit and machine-usable.

Every entry below cites the dossier section that motivates its specific checkpoints. Checkpoints not directly evidenced by a located source are marked "(reasoned extrapolation)" and justified in one clause, per `pilot/prompts/pattern_prior.txt` rule 5.

---

## 1. `two_pointers` (5 checkpoints — two-pointer patterns get a dossier-cited 5th checkpoint for the dedup/write-pointer variant, per `dossier/99_synthesis.md` §S2.2)

**Citations:** pointer-shift/termination/boundary checkpoints are taken directly from `dossier/99_synthesis.md` §S2.2's two-pointer row; the write/read-pointer distinction (checkpoint 5) is the in-place-compaction failure mode named in the same row ("merge/dedup step").

**Frozen prior string** (word count: 138):
```
This program is intended to solve the task using two pointers. Before ranking the full source, check these standard failure points for this pattern first, in order:
1. check whether both pointers start at the correct positions, without an off-by-one at either end of the range
2. check whether the condition choosing which pointer moves next compares the right values in the right direction
3. check whether the loop's stopping condition is correct, rather than causing an infinite loop or an early exit
4. check whether the case where one side of the structure runs out first is handled
5. check whether a write-pointer and a read-pointer stay distinct when the pattern compacts or deduplicates values in place
These are hypotheses, not conclusions -- after checking them, still weigh every line of the source by the instructions above.
```

## 2. `sliding_window` (4 checkpoints)

**Citations:** `dossier/99_synthesis.md` §S2.2 sliding-window row ("window-invariant update on expand; shrink condition; answer capture point") supplies checkpoints 1, 2, 4 directly; checkpoint 3 (shrink must reverse expand) is a reasoned extrapolation from the same row's "window-invariant update" language, made explicit because it is the concrete bug pattern that row implies but does not spell out.

**Frozen prior string** (word count: 128):
```
This program is intended to solve the task using sliding window. Before ranking the full source, check these standard failure points for this pattern first, in order:
1. check whether the running invariant, such as a sum, count, or distinct count, is updated correctly when the window's right edge expands
2. check whether the condition that triggers shrinking the window from the left is correct and not off by one
3. check whether shrinking the window correctly reverses the update that expanding it applied
4. check whether the best-answer is captured at the right moment relative to the expand and shrink steps, not too early or too late
These are hypotheses, not conclusions -- after checking them, still weigh every line of the source by the instructions above.
```

## 3. `binary_search` (4 checkpoints)

**Citations:** `dossier/99_synthesis.md` §S2.2 binary-search row ("mid computation (+1/−1 overflow); left/right update (infinite-loop); boundary return") supplies checkpoints 1, 3, and part of 4 directly; checkpoint 2 (predicate/comparison direction) is a reasoned extrapolation — the dossier's own row already implies it ("infinite-loop" boundary bugs are usually downstream of a wrong-direction comparison), made an explicit, separate checkpoint here because it is the more upstream cause.

**Frozen prior string** (word count: 127):
```
This program is intended to solve the task using binary search. Before ranking the full source, check these standard failure points for this pattern first, in order:
1. check whether the midpoint is computed correctly, without an off-by-one or overflow-style error
2. check whether the comparison against the search predicate moves the boundaries in the correct direction
3. check whether updating the low or high boundary after a comparison is correct, since a wrong update is the most common cause of an infinite loop or a skipped value
4. check whether the loop's stopping condition and the final returned index or value are consistent with each other
These are hypotheses, not conclusions -- after checking them, still weigh every line of the source by the instructions above.
```

## 4. `prefix_sums` (4 checkpoints)

**Citations:** not covered by name in `dossier/99_synthesis.md` §S2.2 (only 5 example patterns are spelled out there); this pattern's checkpoints are a reasoned extrapolation from the general plan-boundary framing of Spohrer & Soloway (`dossier/01_block1_theory.md` §1d, D3) applied to the textbook prefix-sum idiom (indexing convention, build recurrence, query formula, edge queries) — the four steps a prefix-sum implementation always contains, mirroring how the two_pointers/sliding_window rows decompose their idioms into standard steps.

**Frozen prior string** (word count: 122):
```
This program is intended to solve the task using prefix sums. Before ranking the full source, check these standard failure points for this pattern first, in order:
1. check whether the prefix array's indexing convention, such as 0-indexed versus 1-indexed with a leading zero sentinel, is applied consistently
2. check whether the loop that builds the prefix array uses the correct recurrence and correct loop bounds
3. check whether a range query correctly combines two prefix values for the query's inclusive or exclusive boundaries
4. check whether queries touching the very first or very last element are handled without an out-of-range access
These are hypotheses, not conclusions -- after checking them, still weigh every line of the source by the instructions above.
```

## 5. `dynamic_programming` (5 checkpoints — dossier-cited 5th checkpoint)

**Citations:** `dossier/99_synthesis.md` §S2.2 DP row ("base case; transition completeness (all predecessors); iteration order; memo initialization; index offsets") supplies all 5 checkpoints directly, in the same order. Independent empirical support for base-case/stopping-condition difficulty specifically: Baron & Feitelson 2024, ITiCSE (`dossier/01_block1_theory.md` §1b, item B16) — difficulties in recursive structures concentrate on base-case recognition and stopping conditions even for experienced programmers.

**Frozen prior string** (word count: 136):
```
This program is intended to solve the task using dynamic programming. Before ranking the full source, check these standard failure points for this pattern first, in order:
1. check whether the base case's value and its index are correct
2. check whether the recurrence considers every predecessor state, not just some of them
3. check whether the table is filled in an order consistent with the direction the recurrence depends on
4. check whether the table or memo is initialized with a value consistent with how the recurrence combines results, such as the correct sentinel for a minimum or maximum
5. check whether indices are offset consistently between the problem statement and the table's own indexing
These are hypotheses, not conclusions -- after checking them, still weigh every line of the source by the instructions above.
```

## 6. `greedy` (4 checkpoints)

**Citations:** reasoned extrapolation from the general "exchange-argument correctness" structure of greedy algorithms combined with Spohrer & Soloway's plan-composition failure mode (`dossier/01_block1_theory.md` §1d, D3): a greedy solution's plan decomposes into (a) selection criterion, (b) application order, (c) state update after each choice, (d) tie-breaking — each is a documented place novice greedy implementations diverge from the intended exchange argument. Not separately spelled out in `dossier/99_synthesis.md` §S2.2's example row list, which only illustrates 5 of the 12 patterns.

**Frozen prior string** (word count: 131):
```
This program is intended to solve the task using a greedy strategy. Before ranking the full source, check these standard failure points for this pattern first, in order:
1. check whether the sort or selection criterion uses the correct key and the correct direction, ascending versus descending
2. check whether choices are applied in the intended order rather than the input's original order
3. check whether the state used to decide feasibility of the next choice, such as remaining capacity or the last selection made, is updated correctly after each choice
4. check whether ties in the selection criterion are broken in a way consistent with the strategy's intended correctness argument
These are hypotheses, not conclusions -- after checking them, still weigh every line of the source by the instructions above.
```

## 7. `graph_traversal_dfs_bfs` (4 checkpoints)

**Citations:** `dossier/99_synthesis.md` §S2.2 DFS/BFS row ("visited marking placement; queue/stack discipline; neighbor pruning; termination") supplies all 4 checkpoints directly, in the same order.

**Frozen prior string** (word count: 134):
```
This program is intended to solve the task using graph or grid traversal, DFS or BFS. Before ranking the full source, check these standard failure points for this pattern first, in order:
1. check whether nodes are marked visited at the correct moment, on push/enqueue versus on pop/dequeue, since the wrong moment causes duplicate work or missed nodes
2. check whether the traversal follows the right discipline: first-in-first-out for BFS, last-in-first-out for DFS, with recursive calls unwinding properly
3. check whether every valid neighbor is enumerated exactly once, including boundary checks for grid traversals
4. check whether the goal or termination check happens at the correct point relative to enqueueing or dequeueing a node
These are hypotheses, not conclusions -- after checking them, still weigh every line of the source by the instructions above.
```

## 8. `sorting_based` (4 checkpoints)

**Citations:** reasoned extrapolation. `dossier/02_block2_classification.md` §2f documents sort-then-scan as a common structural family (Watanobe et al.'s sorting-algorithm dataset B); the checkpoints below decompose the family into its standard failure surface (key/direction, identity preservation, scan boundary, duplicate handling), mirroring the decomposition style the dossier uses for the 5 example patterns.

**Frozen prior string** (word count: 121):
```
This program is intended to solve the task using a sort-then-scan approach. Before ranking the full source, check these standard failure points for this pattern first, in order:
1. check whether the sort key and sort direction match what the algorithm actually needs
2. check whether original positions or identities are preserved after sorting, if the answer depends on them
3. check whether the scan after sorting starts at the correct index and treats the first or last element correctly
4. check whether adjacent equal values are handled the way the intended logic requires, such as when counting or deduplicating runs
These are hypotheses, not conclusions -- after checking them, still weigh every line of the source by the instructions above.
```

## 9. `hash_map_counting` (4 checkpoints)

**Citations:** reasoned extrapolation from the classic "check-before-or-after-insert" off-by-one that recurs across hash-map counting solutions (e.g. counting pairs summing to a target); grounded generally in Ettles, Luxton-Reilly & Denny 2018's persistent-logic-error catalog (`dossier/01_block1_theory.md` §1d, D7), which documents off-by-one and comparison-direction errors as cross-decade recurring classes.

**Frozen prior string** (word count: 128):
```
This program is intended to solve the task using hash-map or hash-set counting. Before ranking the full source, check these standard failure points for this pattern first, in order:
1. check whether the code looks up the current element in the map or set before or after inserting it, matching the order the intended logic requires
2. check whether a missing key is handled correctly rather than raising an error or silently defaulting to the wrong value
3. check whether the logic needs a count and uses a boolean seen-flag instead, or the reverse
4. check whether keys are normalized consistently, for example order-independent pairs or matching types
These are hypotheses, not conclusions -- after checking them, still weigh every line of the source by the instructions above.
```

## 10. `brute_force_implementation` (4 checkpoints)

**Citations:** reasoned extrapolation targeted at the class's own definition in `PATTERN_VOCABULARY.md` ("correctness depends on faithfully translating the specification"); checkpoints follow directly from that definition (loop bounds vs. stated range, faithfulness to stated formula/operator precedence, index shadowing, single-vs-repeated finalization) rather than from an algorithmic idiom, since brute force by definition has no idiom beyond the specification itself.

**Frozen prior string** (word count: 131):
```
This program is intended to solve the task using a direct brute-force implementation. Before ranking the full source, check these standard failure points for this pattern first, in order:
1. check whether every loop's bounds match the range stated by the problem, including whether an endpoint should be inclusive or exclusive
2. check whether the code follows the problem statement's formula and order of operations faithfully, including integer versus floating-point division
3. check whether a nested loop's index variable is accidentally reused or shadowed by an inner loop
4. check whether the final accumulation or output step runs exactly once at the correct point, not inside a loop that repeats it
These are hypotheses, not conclusions -- after checking them, still weigh every line of the source by the instructions above.
```

## 11. `intervals` (4 checkpoints)

**Citations:** reasoned extrapolation, structurally parallel to the `sorting_based`/`greedy` entries (interval problems are a specialization of both); checkpoints follow the standard interval-sweep idiom (sort key, overlap condition, merge-extend step, tie handling at coincident endpoints).

**Frozen prior string** (word count: 119):
```
This program is intended to solve the task using interval merging or scheduling. Before ranking the full source, check these standard failure points for this pattern first, in order:
1. check whether intervals are sorted by the correct key, start versus end, for the intended algorithm
2. check whether the overlap or merge condition uses the correct comparison and the correct inclusive or exclusive boundary
3. check whether merging two overlapping intervals correctly extends the endpoint rather than simply overwriting it
4. check whether intervals whose start and end coincide are processed in the order the intended logic requires
These are hypotheses, not conclusions -- after checking them, still weigh every line of the source by the instructions above.
```

## 12. `simulation` (4 checkpoints)

**Citations:** reasoned extrapolation from Pea 1986's "parallelism" bug class (`dossier/01_block1_theory.md` §1d, D2: novices wrongly assume the machine does several things at once / merges next-steps) — checkpoint 1 operationalizes exactly this failure for stepwise simulation; checkpoints 2–4 follow from the class definition in `PATTERN_VOCABULARY.md`.

**Frozen prior string** (word count: 127):
```
This program is intended to solve the task using step-by-step simulation. Before ranking the full source, check these standard failure points for this pattern first, in order:
1. check whether all state updates within a single step are computed from the state before that step, rather than mixing pre-step and already-updated values
2. check whether the number of steps or turns simulated matches what the problem statement requires
3. check whether boundary conditions, such as wrap-around or collisions, are handled the same way every time they occur
4. check whether the simulation stops exactly when the stated end condition is met, not one step early or late
These are hypotheses, not conclusions -- after checking them, still weigh every line of the source by the instructions above.
```

---

## Length-confound audit

Word counts across the 12 frozen strings, as measured by the consistency script referenced in `CLAUDE_HANDOFF.md` (not hand-counted): min 119 (`intervals`), max 138 (`two_pointers`), spread 19 words (~15% of the mean prior length, ~128 words). This is a real, measured property of the frozen v1 priors, not a design target hit exactly — an earlier draft targeted a tighter 70–110 word band and three outliers (`two_pointers`, `dynamic_programming`, `graph_traversal_dfs_bfs`) were trimmed once toward that target, but the band was not forced further at the cost of cutting a dossier-cited checkpoint. `pilot/prompts/pattern_prior.txt` rule 3 records the same achieved band. This is reported here, and is cross-checked again empirically by `analysis/run_analysis.py`'s built-in `prompt_length_by_condition` metric at analysis time against the *actual* per-program prompt character/token counts, per `SCIENTIFIC_RISKS.md` ("prior length as a confound") — this section is a pre-registered prediction of that later measurement, not a substitute for it.
