# Ground-Truth Protocol (FROZEN v2)

**Status:** frozen 2026-09-10, before any candidate program has been examined.
**Resolves:** `pilot/PRE_RUN_REVIEW.md` **F2** (ground-truth annotation was not blind to the pattern priors) and **F3.3** (multi-line fault convention undefined).
**Relationship to v1:** replaces `pilot/ANNOTATION_GUIDE.md` §3 ("Determining `faulty_lines`") and adds blinding requirements. All other sections of `ANNOTATION_GUIDE.md` remain in force, subject to the ordering rule in §1 below.

---

## 1. The ordering rule (the core of this document)

`faulty_lines` **must be determined before, and independently of, any pattern reasoning.** The pipeline is strictly ordered, and the order may not be varied:

```
1. identify the buggy/fixed pair and its tests
2. derive candidate faulty line(s) from the fix diff and the failing tests
3. adjudicate whether the change represents the actual logical fault
4. FREEZE faulty_lines            <-- hard boundary
5. only then: assign pattern_label (ANNOTATION_GUIDE.md sections 1, 2, 4-6)
```

**Blinding requirement.** The person (or pass) performing steps 1–4 must not consult, and must not have open, any of:

- `pilot/PATTERN_PRIORS.md`
- `pilot/pattern_priors.json`
- `pilot/v2/generic_placebo_prior.json`
- any rendered treatment prompt
- `pilot/PATTERN_VOCABULARY.md`'s per-class *checkpoint* reasoning (the class definitions themselves are needed only at step 5)

If one person performs both phases — which is expected at pilot scale — they must complete steps 1–4 for **all** candidates and record the results in a write-once file before opening any of the files listed above. **`faulty_lines` may not be revised after step 5 begins, for any reason.** If a labeling pass reveals that a `faulty_lines` decision was wrong, the correct remedy is to exclude the program, not to amend the line numbers.

**Why.** The v1 guide asked the annotator to use judgment to select "the minimal buggy-file line range that a developer would need to change." An annotator primed with "for DP, check the base case, the transition, the fill order…" will, in ambiguous cases, gravitate toward marking exactly those lines — making the ground truth partly a product of the treatment text, and the arm-C score partly self-fulfilling. Ordering plus blinding removes the channel entirely rather than trying to bound it.

## 2. Deriving candidate faulty lines (step 2)

Inputs: `buggy_source_path`, `fixed_source_path`, `tests_path`, and the observed failing/passing test split. Nothing else.

1. Compute a line-level diff, buggy → fixed.
2. Record every changed hunk with its buggy-file line range.
3. Where the tests localize behavior (e.g. a failing test exercises only one branch), record that as supporting evidence.
4. Do not consult problem statements, editorials, or algorithm tags at this step. They are permitted at step 5.

## 3. Adjudication by fix shape (step 3)

The pilot **strongly prefers unambiguous single-line logical faults** (`SAMPLING_PROTOCOL.md` §3 makes this a hard filter). The rules below define the decision for each fix shape, including the shapes that are excluded rather than adjudicated.

| Fix shape | Decision | `faulty_lines` |
|---|---|---|
| **Single-line fix** — one line changed, same statement, altered operator/operand/bound/index | **Include** | that one buggy-file line number |
| **Single-line fix plus cosmetic-only changes** (whitespace, renamed local used consistently, comment text) | **Include** — cosmetic changes are ignored, and the ignored lines must be listed in the annotator's notes | the one substantive line |
| **Multi-line fix, contiguous, one logical fault** (e.g. a two-line expression rewritten) | **Exclude for this pilot** (`exclusion_reason: "multi-line fault — excluded by v2 single-line filter"`) | n/a |
| **Multi-hunk fix, same logical error repeated** (e.g. the same wrong comparison at three call sites) | **Exclude for this pilot**, even though v1 permitted it | n/a |
| **Multi-hunk fix, independent errors** | **Exclude** (`exclusion_reason: "multiple independent faults"`) | n/a |
| **Refactor around the bug** (statement split, moved, extracted) | **Exclude** (`exclusion_reason: "fix refactors — fault line not determinable from diff without judgment"`) | n/a |
| **Ambiguous** — two or more defensible single-line answers, or the diff does not clearly localize the logical error | **Exclude** (`exclusion_reason: "ambiguous fault location"`) | n/a |
| **Fix changes only I/O formatting or parsing**, not the algorithm | **Exclude** (`exclusion_reason: "non-algorithmic fault"`) | n/a |

**Rationale for the aggressive single-line filter.** Three reasons, all pre-registered:

1. **Metric comparability.** `analysis/metrics.py::conservative_fault_rank` scores a multi-line fault by the **best (minimum) rank across all faulty lines**, so a k-line fault gets k independent chances to land in Top-K. Programs with wider faults are systematically easier, and fault width plausibly correlates with pattern class — which would confound the per-pattern breakdown and, worse, the C-vs-B comparison if width correlates with the classes sampled.
2. **Literature comparability.** Both baselines the project positions against use single-line ground truth: IJSEKE 2025 and arXiv:2512.03421 (`dossier/03_block3_fault_localization.md` §3b–3c).
3. **Circularity.** Ambiguous and refactor cases are exactly the ones where step-3 judgment could import pattern reasoning. Excluding them removes the residual risk that blinding alone does not.

**Cost, disclosed:** this filter shrinks the eligible pool and biases the sample toward *simple, cleanly-localized* faults. Simple faults are the easiest case for a strong LLM in every arm, which compresses the achievable spread between arms and biases the pilot **against** detecting a C-vs-B difference. That is the conservative direction, but it also means the pilot's discordance estimate will not transfer to a confirmatory corpus that admits harder faults. Recorded in `CLAIM_BOUNDARIES_V2.md` and `PRE_RUN_REVIEW_V2.md`.

## 4. Recording requirements

For each candidate examined in steps 1–4, the annotator records, in a write-once file created before step 5:

- `program_id`, `task_id`
- diff summary: number of hunks, changed buggy-file line ranges
- decision: include / exclude, with the exclusion reason string from §3 where applicable
- `faulty_lines` (for includes)
- a one-line justification referencing which row of §3 applied
- timestamp

This file is the audit trail for the blinding claim. It must be committed **before** any pattern labeling begins, so that git history establishes the ordering independently of anyone's recollection.

## 5. Interaction with the manifest schema

- `faulty_lines` must be 1-indexed buggy-file line numbers, unique, and within the file's physical line count (`experiments/models.py::ProgramRecord.ground_truth_is_present_and_unique`). Under §3 the list will always have exactly one element for included programs.
- `evaluation_denominator` is set per `SAMPLING_PROTOCOL.md` §5 and is a separate decision from `faulty_lines`; it is not adjusted per program to affect any metric.
- `pattern_source` (assigned at step 5) must record the provenance of the *label*, never of the fault location.

## 6. Second blinding — the labeling pass (added during the v2 adversarial pass)

§1 stops the pattern priors from shaping the ground truth. On its own it opens the **mirror-image channel**: because labeling now happens *after* `faulty_lines` is frozen, the labeler knows where the fault is, and — if they also consult the checkpoint lists — could choose, among defensible labels, the class whose checklist best covers the known fault line. That would point arm C's prior at the answer by construction, inflating arm C for a reason that has nothing to do with pattern information being useful.

The reordering in §1 is still correct; it just needs a second blind on the other side.

**Rules for step 5 (pattern labeling):**

1. The labeler works from **the buggy source plus task metadata plus `pilot/PATTERN_VOCABULARY.md` only**. That document contains class definitions and confusable-pair tie-break rules and deliberately contains **no checkpoint lists** — the checkpoints live in `pilot/PATTERN_PRIORS.md`, which must stay closed during labeling.
2. **`faulty_lines` must not be in view during labeling.** Keep the §4 write-once ground-truth record in a separate file that is not open, and do not annotate the source with the fault location.
3. If one person performs both phases — expected at pilot scale — perfect blinding is impossible, because they cannot unsee what they recorded at step 3. Two mitigations, both required:
   - label from the unannotated buggy source, applying the `PATTERN_VOCABULARY.md` rules in their stated order, and record which rule decided each case;
   - **exclude any program whose label choice was, or could plausibly have been, influenced by knowledge of the fault line** — for example, a genuinely confusable case where two labels are defensible and one of them happens to have a checkpoint sitting on the known faulty line. `exclusion_reason: "label choice not separable from known fault location"`. When in doubt, exclude; the frame is large enough to absorb it.
4. Where a second person is available, they should perform step 5 instead. This is a recommendation, not a requirement, at pilot scale — but it is the only way to close the channel completely, and it becomes **mandatory for the confirmatory corpus**, where double annotation is already required (`pilot/ANNOTATION_GUIDE.md` §4).

**Residual risk, disclosed:** with a single annotator, this is a discipline-and-exclusion control, not a structural guarantee. Its strength rests on the fact that the pilot admits only clean single-line faults in structurally unambiguous programs (§3), so the label is usually determined by code shape rather than by fault position, and on the confusable-case exclusion rule above. `PRE_RUN_REVIEW_V2.md` records this as the most significant unresolved-by-construction risk in the v2 design.

## 7. What this protocol does not fix

Blinding removes the prior→ground-truth channel. It does not make a single annotator's fault-location judgments *correct*; no κ is computed at pilot scale (`ANNOTATION_GUIDE.md` §4 relaxation stands). The single-line filter substantially reduces the space in which a judgment error is possible, but a program whose "obvious" single-line fix masks a deeper logical error would still be scored against the shallow line. This is a known, disclosed limitation of the pilot's ground truth, and it applies identically to all three arms — so it adds noise to every comparison rather than bias to any one of them.
