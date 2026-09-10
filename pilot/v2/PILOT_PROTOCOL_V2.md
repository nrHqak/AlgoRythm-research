# Pilot Protocol v2 (FROZEN)

**Status:** frozen 2026-09-10, before any manifest exists, before any dataset sample is selected, and before any experimental result exists.
**Supersedes:** `pilot/PILOT_PROTOCOL.md` (v1) for execution purposes. **v1 is preserved unmodified** — see `pilot/v2/CHANGELOG_V1_TO_V2.md` for the complete v1→v2 diff and rationale.
**Authorized by:** the user's v2 authorization following the BLOCK verdict in `pilot/PRE_RUN_REVIEW.md`.
**Companion v2 documents:** `GENERIC_PLACEBO_PRIOR.md`, `generic_placebo_prior.json`, `PROMPT_DIFF_V2.md`, `GROUND_TRUTH_PROTOCOL.md`, `SAMPLING_PROTOCOL.md`, `STATISTICAL_ANALYSIS_PLAN.md`, `MODEL_FREEZE_PROTOCOL.md`, `CLAIM_BOUNDARIES_V2.md`, `CHANGELOG_V1_TO_V2.md`, `PRE_RUN_REVIEW_V2.md`.
**Carried forward from v1, unchanged:** `pilot/PATTERN_VOCABULARY.md`, `pilot/PATTERN_PRIORS.md`, `pilot/pattern_priors.json`, `pilot/prompts/control.txt`, `pilot/prompts/pattern_prior.txt`.

---

## 1. What changed and why

v1 compared two conditions: no prior vs. pattern-specific prior. `PRE_RUN_REVIEW.md` F1 established that this design cannot attribute any observed effect to *pattern specificity*, because the manipulation simultaneously changes the amount of text, the presence of an ordered checklist, and the search-order instruction. A positive v1 result would have been fully explained by "any structured debugging guidance helps."

v2's central change is a **matched generic (placebo) prior** and a three-arm design whose **primary comparison is pattern vs. generic**, which is the comparison that identifies the causal contribution of pattern-specific structural information.

## 2. Conditions

| Arm | Name (as recorded in run records) | Prompt content |
|---|---|---|
| **A** | `no_prior` | Shared system prompt + shared user template. No prior block. |
| **B** | `generic_prior` | A + a delimited block containing the matched generic debugging checklist (`generic_placebo_prior.json`). |
| **C** | `pattern_prior` | A + a delimited block containing the frozen v1 pattern-specific checklist for that program's `pattern_label` (`pilot/pattern_priors.json`, unchanged). |

**Primary comparison: C vs B.** This holds constant the presence of a delimited block, its format, its instructional tone, its checkpoint count, and (within a declared tolerance) its length — isolating pattern-specific content as the only systematic difference.

**Secondary comparisons: A vs C and A vs B.** These measure the total effect of receiving a prior at all, and decompose it, but neither identifies pattern specificity on its own.

**Arm A is not a zero-guidance baseline.** The shared system prompt already contains generic reviewer framing ("loop bounds, comparison directions, index updates, initialization, and the order in which state is updated"). Arm A means "no prior *block*," not "no guidance." This dilutes A vs B and must be disclosed whenever A vs B is reported. It does not affect C vs B, where the framing is identical on both sides.

## 3. Execution architecture — two sessions, and why

Codex's runner implements exactly two conditions per session (`experiments/run_pilot.py` reads `conditions["control"]` and `conditions["treatment"]`; `condition_order()` returns a two-element list; `analysis/run_analysis.py` pivots on exactly two condition names). **This protocol does not modify Codex's code.** The three arms are therefore obtained from two sessions over the same 30 programs:

| Session | Config | Control arm | Treatment arm | Priors file |
|---|---|---|---|---|
| **G** (generic) | `pilot/v2/config/pilot_v2_generic.yaml` | `no_prior` (A_G) | `generic_prior` (B) | `pilot/v2/generic_placebo_prior.json` |
| **P** (pattern) | `pilot/v2/config/pilot_v2_pattern.yaml` | `no_prior` (A_P) | `pattern_prior` (C) | `pilot/pattern_priors.json` |

The two configs carry **different `experiment_name` values**. This is mandatory, not cosmetic: `experiments/run_pilot.py` computes `raw_root = output_root/"raw"/experiment_name` and `existing_execution_keys()` scans that whole tree across all sessions; an arm-A execution key excludes `prior_hash` (it is `None` for a control run) and is otherwise identical between the two sessions, so reusing one `experiment_name` would abort session two as a duplicate run. Using `--resume` instead would silently skip arm A and then fail `assert_condition_balance` at analysis time.

### 3.1 Invariants that MUST hold across the two sessions

Because the primary comparison is cross-session, these are the conditions under which C and B remain comparable. All are mechanically checkable from the two `session_manifest.json` files and the run records, and the cross-session analysis **must assert them before computing anything** (see `STATISTICAL_ANALYSIS_PLAN.md` §6):

1. identical `manifest_hash` (the same 30 programs, byte-identical inputs);
2. identical `system_prompt_hash`;
3. identical `user_template_hash`, and identical per-program `shared_prompt_hash`;
4. identical `provider`, `model`, `temperature`, `max_tokens`;
5. identical `repetitions` (5) and `condition_order` policy (`counterbalanced`);
6. both sessions non-mock (`engineering_only: false`).

Any violation invalidates the primary comparison; do not "adjust for" it.

### 3.2 Temporal separation

The two sessions cannot run simultaneously, so C and B observations are separated in time and any provider-side drift between them is confounded with the manipulation. Two controls:

- **Run the two sessions back-to-back**, same day, no configuration change between them, order recorded. Randomize which session runs first by a single coin flip recorded in `PRE_EXPERIMENT_COMMIT` before starting; do not choose it.
- **The A_G vs A_P null calibration** (below) measures exactly this drift, because arm A is identical in both sessions.

### 3.3 The null calibration (a designed benefit of the duplicated arm A)

Arm A is executed in both sessions, so the pilot yields two independent replicates of the *same* condition on the *same* programs. The A_G vs A_P difference is an empirical noise floor: whatever difference arises there is attributable to nothing but re-running.

**Pre-declared interpretation rule.** Let `d_null` = discordant pairs in A_G vs A_P at Top-1 (program-level aggregation, `STATISTICAL_ANALYSIS_PLAN.md` §3), and `d_primary` = discordant pairs in C vs B at Top-1. **If `d_null >= d_primary`, the primary comparison is declared uninterpretable at this sample size**, and is reported as such regardless of its p-value. This rule is fixed now and may not be revised after seeing either quantity.

Cost of the duplication: 150 additional calls (see §6).

## 4. Frozen parameters

Unchanged from v1 (restated for a single reference point, not re-decided):

| Parameter | Value |
|---|---|
| `dataset.target` / source | `ConDefects-Python` (must equal the manifest's `dataset_name`) |
| `dataset.target_n` | 30 |
| `metrics` | `top1, top3, top5, exam` |
| `repetitions` | 5 |
| `statistics.primary` (config-level) | `exact_mcnemar` |
| `statistics.bootstrap_iterations` | 10000 |
| `--condition-order` | `counterbalanced` |
| `--parser-failure-policy` | `count_as_failure` primary; `exclude` only as a labeled sensitivity pass |
| Analysis bootstrap seed | `20260908` |
| Pattern vocabulary | `pilot/PATTERN_VOCABULARY.md`, 12 classes, unchanged |
| Pattern prior text | `pilot/pattern_priors.json`, unchanged (Change 8) |
| User template | `pilot/prompts/control.txt`, unchanged |

New or changed in v2:

| Parameter | v2 value | Rationale |
|---|---|---|
| Conditions | three arms across two sessions (§2–3) | F1 |
| Generic prior | `pilot/v2/generic_placebo_prior.json` | F1 |
| System prompt | `pilot/v2/prompts/system_v2.txt` | the v1 system prompt described the block as one that "names the program's intended algorithmic pattern" — true for C, false for B, which would have framed the two arms differently and confounded the primary comparison. v2 describes it neutrally as "a delimited block of debugging guidance." The v1 phrase "pointer or index updates, base cases" was also narrowed to "index updates, initialization" to stop the shared system prompt from handing out vocabulary-specific hints for free. |
| Primary experimental unit | one **program** (not one LLM call) | Change 4; `STATISTICAL_ANALYSIS_PLAN.md` |
| Primary statistical comparison | program-level exact McNemar, C vs B, Top-1 | `STATISTICAL_ANALYSIS_PLAN.md` |
| Sampling frame | fully specified, seeded, one-program-per-task | F3; `SAMPLING_PROTOCOL.md` |
| Ground-truth procedure | blinded, diff-first, single-line-preferred | F2; `GROUND_TRUTH_PROTOCOL.md` |
| Model freeze | exact pinned identifier + dry run + abort criteria | F4; `MODEL_FREEZE_PROTOCOL.md` |
| Pattern coverage | 4 classes × 7–8 programs (not 12 × 2–3) | N1; `SAMPLING_PROTOCOL.md` §4 |
| Temperature / repetitions | temperature 0 **retained**, repetitions reinterpreted as a determinism probe | N2; `STATISTICAL_ANALYSIS_PLAN.md` §4 |

## 5. Purpose and success criteria

This remains a **calibration pilot**, not a confirmatory study. Purpose, in priority order:

1. Verify the three-arm pipeline executes end-to-end on real data with all cross-session invariants (§3.1) holding.
2. Establish the empirical noise floor via A_G vs A_P (§3.3).
3. Estimate the C-vs-B discordant-pair rate to size the confirmatory study (`STATISTICAL_ANALYSIS_PLAN.md` §7).
4. Record a directional, non-confirmatory read of the pattern-specificity effect.
5. Measure parser-failure rate, ranking length, and prompt length by arm as confound diagnostics.

Success criteria to evaluate once — and only once — a real run exists:

1. Both sessions complete; all §3.1 invariants assert clean.
2. Parser-failure rate is reported per arm; a large or arm-asymmetric rate is a finding, not something to normalize away.
3. Ranking length per arm is reported (`PRE_RUN_REVIEW.md` N5: ranking length is a mediator between prompt content and Top-K; it is expected to be similar for B and C, and confirming that is part of validating the primary comparison).
4. `prompt_length_by_condition` is checked against the declared tolerance in `GENERIC_PLACEBO_PRIOR.md` §4.
5. The null-calibration rule (§3.3) is applied *before* interpreting the primary result.
6. A manual spot-check of 3–5 raw transcripts per arm confirms no fault-location leakage beyond the block contents.

## 6. Budget

| Session | Programs | Arms | Reps | Calls |
|---|---|---|---|---|
| G | 30 | 2 (A_G, B) | 5 | 300 |
| P | 30 | 2 (A_P, C) | 5 | 300 |
| **Total** | | | | **600** |

Of these, 300 are arm A (150 per session). The duplication is the price of the null calibration in §3.3 and is deliberate.

Plus up to ~20 dry-run calls on smoke data (`MODEL_FREEZE_PROTOCOL.md`), which are never analyzed as scientific data.

## 7. Execution order (all steps gated; do not start a later step before an earlier one is closed)

1. **Freeze the model** (`MODEL_FREEZE_PROTOCOL.md`): pin provider + exact model identifier, run the dry run on smoke data, verify abort criteria are not triggered, record everything.
2. **Build the sampling frame and select the sample** (`SAMPLING_PROTOCOL.md`), with ground truth determined under `GROUND_TRUTH_PROTOCOL.md`'s blinding rules. Produce the manifest; validate with `python -m experiments.validate_manifest`.
3. **Record the coin flip** for session order, and the frozen model parameters, in a dated pre-experiment record.
4. **Run session G and session P** back-to-back with the invariants in §3.1.
5. **Analyze each session natively** with `analysis/run_analysis.py` (gives A vs B and A vs C, plus all built-in adversarial diagnostics).
6. **Run the cross-session primary analysis** (C vs B) per `STATISTICAL_ANALYSIS_PLAN.md` §6. This requires one small additive analysis script that reads both sessions' processed records; it does not modify Codex's pipeline and is an engineering handoff item.
7. **Apply `CLAIM_BOUNDARIES_V2.md`** before any result is written anywhere.

## 8. Freeze discipline

Everything in this document and its companions is frozen as of the commit recorded in `CHANGELOG_V1_TO_V2.md`. The v1 no-outcome-driven-tuning rule (`pilot/PRE_EXPERIMENT_COMMIT.md` rule 2) carries over verbatim and now also covers `generic_placebo_prior.json`: **the placebo may not be weakened, strengthened, or reworded after any result is seen.** A placebo tuned post hoc is worse than no placebo, because it manufactures the contrast it was built to test.
