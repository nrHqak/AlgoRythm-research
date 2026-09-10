# Sampling Protocol (FROZEN v2)

**Status:** frozen 2026-09-10, before the sampling frame has been built and before any candidate program has been examined.
**Resolves:** `pilot/PRE_RUN_REVIEW.md` **F3** (no sampling frame; unblinded judgment gates; no task-independence constraint; no length floor; `problem_context` unspecified) and **N1** (12 classes at n≈2.5 each).
**Relationship to v1:** replaces `pilot/PILOT_PROTOCOL.md` §3 and `pilot/ANNOTATION_GUIDE.md` §1 sampling behavior. The `pattern_label` assignment rules in `ANNOTATION_GUIDE.md` §2 and §5 remain in force, executed at stage S6 below.

---

## 1. Principle

The sample is **not** "30 convenient programs." It is a seeded draw from an explicitly enumerated frame, produced by a pipeline in which every human judgment happens before, and independently of, any knowledge of how a model performs. **No stage of this pipeline may use LLM output, and no candidate may be run through any LLM before the manifest is frozen** (the only permitted LLM calls before the main run are the dry-run calls in `MODEL_FREEZE_PROTOCOL.md`, which use smoke data only and never touch candidates).

## 2. Pipeline

```
S1  ConDefects-Python, complete corpus
S2  -> mechanical eligibility filters          (no judgment)
S3  -> ground-truth determination, BLINDED     (GROUND_TRUTH_PROTOCOL.md steps 1-4)
S4  -> one program per task_id                 (seeded)
S5  -> frame F is now fixed and recorded
S6  -> pattern annotation, BLINDED to faulty_lines and to the checkpoint
       lists (GROUND_TRUTH_PROTOCOL.md section 6; ANNOTATION_GUIDE.md sections 2, 5)
S7  -> class selection rule                    (deterministic)
S8  -> seeded within-class draw
S9  -> final n = 30, manifest frozen
```

Each stage's input and output counts must be recorded (§7). A stage may never be re-run with a different seed or a different rule after seeing a later stage's contents.

## 3. S2 — mechanical eligibility filters (no judgment permitted)

Applied by script. A candidate is eligible only if **all** hold:

1. **Runs without syntax error** under the pinned Python version.
2. **At least one passing and at least one failing test** in `tests_path` (Araujo et al. 2016 precondition, `dossier/03_block3_fault_localization.md` §3a). Checked by executing the suite, never by inspection.
3. **Physical source length ≥ 25 lines and ≤ 300 lines.**
   *The 25-line floor is new in v2.* v1's floor of 10 was too low: `evaluation_denominator` defaults to `loc`, so on a very short program Top-5 covers a large fraction of the file and is near-trivially attainable once any block directs attention to a construct — the treatment arms would saturate Top-5 for structural reasons unrelated to localization quality. The floor also guarantees enough inspectable lines for Top-1/3/5 to discriminate.
4. **`evaluation_denominator` ≥ 15** after the §5 rule is applied (a corollary of 3, checked explicitly because the denominator, not the physical length, is what the metrics divide by).
5. **Single-line fix shape** per `GROUND_TRUTH_PROTOCOL.md` §3 — determined at S3, but recorded as an eligibility outcome.

Filters 1, 2, 3, 4 are pure script decisions. Filter 5 involves the blinded adjudication of `GROUND_TRUTH_PROTOCOL.md` §3, whose decision table is written to make the outcome as close to mechanical as the material allows.

## 4. S4 — one program per `task_id`

**At most one program from any `task_id` may enter the frame.** ConDefects-Python holds 1,625 faulty programs across 985 tasks (`dossier/04_block4_datasets.md` §4.3), so an unconstrained draw of 30 would very likely include same-task siblings, which share a problem statement, an intended technique, and often a fault mode. Both the primary McNemar test and `analysis/statistics.py::clustered_bootstrap_delta` treat the **program** as the independent unit; the bootstrap clusters on `program_id` and **nothing in Codex's pipeline clusters on `task_id`**. Enforcing uniqueness at selection is what makes the existing program-level clustering correct.

Where several eligible programs share a `task_id`, keep one **by seeded random draw** — never by length, readability, familiarity, or any quality criterion.

**This constraint is load-bearing.** If it is ever relaxed, the statistics become wrong and no code in the repository will detect it.

## 5. `problem_context` and `evaluation_denominator` — declared uniformly, in advance

- **`problem_context`: OMITTED for all 30 programs.** `problem_context_path` is left null throughout. Rationale: AtCoder problem statements frequently make the intended technique obvious, which would leak pattern information into arms A and B and shrink the very contrast the pilot exists to measure. Omitting it also removes an uncontrolled per-program variable. The cost — a less realistic task setting — is accepted for the pilot and revisited for the confirmatory study, where realism matters more. The decision is all-or-none by construction: no program carries a problem statement.
- **`evaluation_denominator`: physical line count of the buggy file**, i.e. the `loc` default, applied identically to all 30 programs. No per-program convention switching. Note this makes the resulting EXAM a *censored, line-based* statistic that is **not** the statement-based EXAM of IJSEKE 2025; it is reported as EXAM\* and treated as secondary (`STATISTICAL_ANALYSIS_PLAN.md` §5).

## 6. S7 — class selection rule (deterministic, outcome-independent)

v1 spread 30 programs over 12 classes (~2.5 each), which made the "treatment" twelve different interventions pooled, and made the per-pattern breakdown uninterpretable. v2 concentrates the sample:

1. After S6, compute the eligible count per `pattern_label` in frame F.
2. **Eligible classes** are those with ≥ 7 programs in F.
3. Rank eligible classes by count, descending. **Ties are broken by the row order of the table in `pilot/PATTERN_VOCABULARY.md`** (deterministic, fixed before any counting).
4. Take the **top 4** classes. Allocate **8, 8, 7, 7** programs in rank order.
5. Within each selected class, draw the allocated number **by seeded random sample without replacement**.

**Contingency rules** (fixed now, so that a disappointing frame cannot become an excuse for improvisation):

- If exactly 3 classes have ≥ 7: use those 3, allocate 10/10/10.
- If fewer than 3 classes have ≥ 7: lower the per-class floor to 5 and take the top 6 classes, allocating 5 each. If that also fails, **stop and record a protocol deviation** — do not proceed by relaxing filters ad hoc.
- If a selected class turns out to have fewer eligible programs than allocated (should be impossible given step 2, but recorded for completeness), promote the next-ranked eligible class and re-allocate by the same rule.

The rule uses only frame counts — available before any model is run — so it cannot be steered toward classes expected to perform well.

**Disclosed consequence:** the pilot's discordance estimate describes the 4 sampled classes, not the 12-class vocabulary. Transfer to a confirmatory corpus spanning all 12 requires a homogeneity assumption that this pilot cannot test. This is recorded in `CLAIM_BOUNDARIES_V2.md` and is the price of having enough programs per class for the per-class numbers to mean anything at all.

## 7. Seeds and reproducibility record

- **Sampling seed: `20260910`**, used for both the S4 task-deduplication draw and the S8 within-class draw, via a documented deterministic procedure (sort candidates by `program_id` for a stable order, then draw with `random.Random(20260910)`). Frozen here; a different seed may not be substituted after any draw is observed.
- The following must be recorded and committed **with** the manifest:
  - corpus size at S1;
  - count removed by each S2 filter, separately;
  - count removed at S3 by each `GROUND_TRUTH_PROTOCOL.md` §3 exclusion reason;
  - count removed at S4 by task deduplication;
  - **frame size |F| and the per-class eligible counts** (the input to §6);
  - the 4 selected classes, their ranks, and their allocations;
  - the drawn `program_id` list, in draw order;
  - the seed, and the exact script or command used.

A reader must be able to re-run the pipeline from the recorded seed and reproduce the identical 30 `program_id`s.

## 8. Prohibited

- Selecting, dropping, or swapping any program for any reason connected to how a model performed on it.
- Running any candidate through any LLM before the manifest is frozen.
- Adjusting a filter threshold after seeing which programs it removes.
- Re-drawing with a different seed because the first draw "looks unbalanced" — the draw is the draw.
- Adding a 31st program, or substituting a replacement for one later found flawed. A flawed program is marked `excluded` with a reason and timestamp before `selection_frozen_at`; after that point the sample stands and `target_n` must be reconciled per `experiments/safety.py::validate_manifest_for_run` before running, or the freeze is re-done from scratch with a new manifest and a documented deviation.
