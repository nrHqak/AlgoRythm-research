# Changelog v1 → v2

**Date:** 2026-09-10.
**Trigger:** the BLOCK verdict in `pilot/PRE_RUN_REVIEW.md`, and the user's explicit authorization of a Pilot Protocol v2.
**Status of v1:** **preserved unmodified.** Every v1 file remains byte-identical to commit `81fd51d`; this was verified mechanically (§5, check 1) and not merely intended. No git history was rewritten, amended, or force-pushed.

---

## 1. Versioning approach

v2 is **additive**. All new material lives under `pilot/v2/`, and v1 remains readable and citable as the specification that was frozen before the adversarial review. Where a v2 document supersedes a v1 document for execution purposes, it says so in its header and names the file it supersedes. Three v1 artifacts are **reused unchanged** by v2 rather than re-versioned:

| v1 artifact | v2 status |
|---|---|
| `pilot/PATTERN_VOCABULARY.md` | reused unchanged |
| `pilot/PATTERN_PRIORS.md`, `pilot/pattern_priors.json` | reused unchanged — **Change 8**, see §3 |
| `pilot/prompts/control.txt`, `pilot/prompts/pattern_prior.txt` | reused unchanged |
| `pilot/prompts/system.txt` | **retired** — replaced by `pilot/v2/prompts/system_v2.txt` (§2, Change 1c) |
| `pilot/config/pilot.yaml` | **not used by v2** — replaced by the two session configs; left in place as the v1 record |

## 2. Files created

| File | Purpose |
|---|---|
| `pilot/v2/PILOT_PROTOCOL_V2.md` | Master v2 protocol: three arms, two-session architecture, cross-session invariants, null calibration, execution order |
| `pilot/v2/GENERIC_PLACEBO_PRIOR.md` | Placebo design rationale, frozen text, and the mechanical matching audit |
| `pilot/v2/generic_placebo_prior.json` | Runner input: 12 labels → matched generic checklist (2 variants) |
| `pilot/v2/PROMPT_DIFF_V2.md` | Exact three-arm prompt diff; why the system prompt changed; disclosed residual asymmetries |
| `pilot/v2/GROUND_TRUTH_PROTOCOL.md` | Blinded, diff-first `faulty_lines` procedure; fix-shape decision table |
| `pilot/v2/SAMPLING_PROTOCOL.md` | Sampling frame, seeded draw, one-per-task rule, class selection rule |
| `pilot/v2/STATISTICAL_ANALYSIS_PLAN.md` | Program as unit, majority-of-5 aggregation, primary/secondary tests, power floor, sizing formula |
| `pilot/v2/MODEL_FREEZE_PROTOCOL.md` | Model pinning, dry run, explicit abort criteria |
| `pilot/v2/CLAIM_BOUNDARIES_V2.md` | What a successful C-vs-B result licenses, and what stays prohibited |
| `pilot/v2/CHANGELOG_V1_TO_V2.md` | This file, including the F1–F5 resolution table |
| `pilot/v2/PRE_RUN_REVIEW_V2.md` | Second adversarial review of the v2 design |
| `pilot/v2/prompts/system_v2.txt` | Neutral system prompt used by all three arms |
| `pilot/v2/config/pilot_v2_generic.yaml` | Session G config (A vs B) |
| `pilot/v2/config/pilot_v2_pattern.yaml` | Session P config (A vs C) |

**Files modified: none.** **Files deleted: none.**

## 3. Change-by-change record

| # | Authorized change | What was done | Files |
|---|---|---|---|
| 1a | Add matched placebo arm | Three arms — A `no_prior`, B `generic_prior`, C `pattern_prior` — executed as two paired sessions over the same 30 programs. Primary comparison **C vs B**. | `PILOT_PROTOCOL_V2.md`, both configs |
| 1b | Placebo design + audit | Two variants (4- and 5-checkpoint) matched per label on checkpoint count; word deviation max 8 / mean 4.2; tolerance ≤10 words predeclared; leakage scan clean | `GENERIC_PLACEBO_PRIOR.md`, `generic_placebo_prior.json` |
| 1c | Prompt diff | v1 system prompt described the block as one that "names the program's intended algorithmic pattern" — true for C, false for B, which would have framed the two arms differently and broken the primary comparison. Replaced with a neutral description. Also removed "pointer"/"base case" from the shared reviewer framing so the system prompt stops handing vocabulary-specific hints to every arm. | `PROMPT_DIFF_V2.md`, `prompts/system_v2.txt` |
| 2 | Ground-truth circularity | Strict ordering (`faulty_lines` frozen before pattern labeling) plus a blinding rule barring the ground-truth pass from the prior files; fix-shape decision table; single-line faults only for this pilot. **Plus a second blinding added during the v2 adversarial pass** (§6 of that file): the reordering alone opened the mirror-image channel, in which a labeler who knows the frozen fault line could pick, among defensible labels, the class whose checkpoints sit on it — so the labeling pass is now blinded to `faulty_lines` and to the checkpoint lists, with a mandatory exclusion rule for inseparable cases. | `GROUND_TRUTH_PROTOCOL.md` §1, §3, §6; `SAMPLING_PROTOCOL.md` S6 |
| 3 | Sampling frame | Nine-stage pipeline; mechanical filters; one program per `task_id`; seed `20260910`; 25-line floor; `problem_context` omitted uniformly; deterministic 4-class selection rule with contingencies; full reproducibility record | `SAMPLING_PROTOCOL.md` |
| 4 | Observational unit | Program is the unit; majority-of-5 aggregation; explicit prohibition on pooling 30×5 as n=150; repetitions reinterpreted as a determinism probe at temperature 0; five per-repetition tests demoted to all-or-nothing robustness reporting | `STATISTICAL_ANALYSIS_PLAN.md` |
| 5 | Model/alias safety | Exact-identifier pinning, echoed-identity verification, smoke-only dry run, dry-run and main-run abort criteria, loud-failure principle | `MODEL_FREEZE_PROTOCOL.md` |
| 6 | Claim boundaries | Single licensed main claim with mandatory qualifiers; explicit prohibitions on universal-debugging, classifier, end-to-end-product, and human-learning claims; mandatory oracle-label / small-n / exploratory disclosures | `CLAIM_BOUNDARIES_V2.md` |
| 7 | Resolve F1–F5 | See §4 | this file |
| 8 | Preserve clean priors | `pilot/pattern_priors.json` and `pilot/PATTERN_PRIORS.md` reused **byte-identically**; verified by `git diff` returning empty (§5, check 1). No prior was reworded, and none may be after any result is seen. | — |

## 4. F1–F5 resolution table (Change 7)

| Finding | Severity | v2 resolution | File implementing resolution | Remaining limitation |
|---|---|---|---|---|
| **F1** — Two-arm design cannot attribute any effect to pattern specificity; manipulation bundles content, length, checklist format, and search-order instruction | **Fatal** | Matched generic placebo arm B added; primary comparison changed to **C vs B**, which holds block presence, format, checkpoint count, tone, and (±8 words) length constant. A vs C demoted to secondary. | `PILOT_PROTOCOL_V2.md` §2–3, `GENERIC_PLACEBO_PRIOR.md`, `generic_placebo_prior.json`, `PROMPT_DIFF_V2.md` | C vs B is **cross-session**, so temporal/provider drift is not eliminated — only measured, via the A_G-vs-A_P null calibration. The placebo is constant across programs while the pattern prior is per-program, so "per-program tailoring on any axis helps" survives as an alternative explanation. The `<ALGORITHMIC_PATTERN_PRIOR>` tag wraps generic text in arm B (matched between B and C, but semantically incongruent for B). |
| **F2** — `faulty_lines` annotation not blind to pattern priors; ground truth partly a product of the treatment text | **Fatal** | Strict five-step ordering with a hard freeze boundary before any pattern reasoning; explicit blinding list; write-once audit trail committed before labeling begins; ambiguous and refactor cases excluded rather than adjudicated; single-line faults only. | `GROUND_TRUTH_PROTOCOL.md` §1, §3, §4 | Blinding removes the prior→ground-truth channel but does not make a single annotator's judgments *correct*; no κ at pilot scale. A shallow single-line fix masking a deeper error would still be scored against the shallow line — noise for all arms, bias for none. |
| **F3** — Selection can cherry-pick; no sampling frame; no task-independence constraint; no length floor; `problem_context` unspecified; multi-line fault convention undefined | **Fatal** | Enumerated frame with recorded stage-by-stage counts; seeded draws (seed `20260910`); **one program per `task_id`**; 25-line floor and denominator ≥15; `problem_context` omitted for all 30; single-line faults only; prohibition on any LLM-informed selection. | `SAMPLING_PROTOCOL.md` §2–8, `GROUND_TRUTH_PROTOCOL.md` §3 | The single-line + clean-localization filter biases the sample toward **easy** faults, compressing the achievable between-arm spread and limiting transfer of the discordance estimate to a confirmatory corpus admitting harder faults. Class narrowing (4 of 12) means the estimate describes the sampled classes only. |
| **F4** — Model alias produces a complete, non-aborting, all-zero run that looks like finished data | **Fatal (operational)** | Exact identifier pinned; **echoed identity must equal requested string, zero tolerance**; smoke-only dry run of ≥10 calls; explicit dry-run and main-run abort criteria; all-non-`ok` runs declared void and never analyzable; loud-failure principle forbidding silent retries. | `MODEL_FREEZE_PROTOCOL.md` §2–4 | If a provider offers only a moving alias, the risk is accepted and recorded rather than eliminated. Mid-run model drift is detected only when the echoed identifier changes. |
| **F5** — `CLAIM_BOUNDARIES.md` licensed an attribution the design could not support | **Fatal** | v2 states the single maximal claim a successful C-vs-B result licenses, with mandatory qualifiers; adds explicit prohibitions on attributing specificity from A-vs-C alone, on universal-debugging / classifier / product / human-learning claims; adds mandatory disclosures (oracle labels, small n, exploratory, easy-case filtering, omitted problem context); adds a worked list of violating phrasings. | `CLAIM_BOUNDARIES_V2.md` §1–5 | Claim boundaries constrain writing, not inference; they depend on being applied. The surviving "per-program tailoring" alternative (F1) must be disclosed by the author each time, since no design element rules it out. |

### Non-fatal findings (N1–N12) disposition

| Finding | Disposition |
|---|---|
| N1 — 12 classes at n≈2.5 | **Resolved** — 4 classes × 7–8, by a deterministic frequency rule (`SAMPLING_PROTOCOL.md` §6). Limitation: estimate describes sampled classes only. |
| N2 — temperature 0 vs 5 reps incoherent | **Resolved** — temperature 0 retained; repetitions reinterpreted as a determinism probe; determinism rate is now a mandatory reported quantity (`STATISTICAL_ANALYSIS_PLAN.md` §4). |
| N3 — no rule for combining 5 McNemar tests | **Resolved** — program-level aggregation is primary; the five per-repetition tests are all-or-nothing robustness reporting (§6.4). |
| N4 — power floor undisclosed | **Resolved** — the d≥6 arithmetic is stated in the plan (§7) and the pilot's job is redefined as discordance estimation. |
| N5 — EXAM censoring and ranking-length mediation | **Partly resolved** — EXAM renamed EXAM\* and demoted to descriptive; ranking length is a mandatory diagnostic. Ranking length is deliberately **not** fixed (see `PROMPT_DIFF_V2.md` §4.3 for the reasoning); the mediation is measured, not eliminated. |
| N6 — "oracle" misnomer | **Resolved in description** — condition names in the v2 configs no longer use "oracle" (`no_prior` / `generic_prior` / `pattern_prior`); the label's single-rater nature is a mandatory disclosure (`CLAIM_BOUNDARIES_V2.md` §4). |
| N7 — counterbalancing near-no-op | **Resolved** — retained (it balances temporal drift and prefix-cache effects), with the overstated v1 rationale corrected in `PILOT_PROTOCOL_V2.md` §4. |
| N8 — system prompt primes for an absent block | **Resolved** — neutral wording in `system_v2.txt`; this became mandatory in v2, since the v1 phrasing would have differentially framed arms B and C. |
| N9 — stale "~22-word" cross-reference | **Superseded** — the v1 file is preserved with its error intact (correcting it would modify v1); v2 states the correct figures. Noted here so the discrepancy is not mistaken for a new one. |
| N10 — dry-run data source unspecified | **Resolved** — smoke data only, never candidates (`MODEL_FREEZE_PROTOCOL.md` §3). |
| N11 — ConDefects leakage unprobed | **Not resolved** — remains an open risk, disclosed. A leakage probe on non-manifest programs is recommended before ConDefects carries confirmatory weight. |
| N12 — no task-level clustering in code | **Resolved by design** — one program per `task_id` makes the existing program-level clustering correct (`SAMPLING_PROTOCOL.md` §4). Load-bearing: relaxing it silently invalidates the statistics. |

## 5. Verification performed before committing

Run against the **live** Codex code in a local `.venv` built from `requirements.txt`; nothing below was reimplemented or checked by reading alone.

1. **v1 immutability** — `git diff HEAD` over all 13 v1 pilot files returned empty. v1 is byte-identical to commit `81fd51d`.
2. **Both priors files load through the runner's own loader** — `experiments.run_pilot.load_prior_map` returns 12 keys for each, and the key sets are identical, so `run_pilot.py`'s `missing_priors` guard will pass for either session.
3. **System prompt neutrality** — the v1 pattern-naming sentence is absent, the neutral block description is present, and the terms `pointer` / `base case` no longer appear.
4. **`control.txt` still validates** unchanged via `experiments.prompts.validate_user_template`.
5. **24 prompt pairs built** (12 labels × 2 priors files) through `experiments.prompts.build_prompt_pair`, whose internal `assert_only_prior_differs` raised nothing. Verified additionally that, for every label: the arm-A prompt and its `shared_prompt_hash` are identical across the two sessions; arm B and arm C are byte-identical outside the delimited block; and the placebo and pattern `prior_hash` values never collide.
6. **Both v2 configs satisfy the runner's own validation rules** — exact metric set, `exact_mcnemar` primary, `target_n` 30, `repetitions` 5, distinct condition names, agreeing `dataset.target`, arm A named `no_prior` in both — and, critically, **the two `experiment_name` values are distinct**, without which the second session would abort on duplicate arm-A execution keys.
7. **Placebo matching audit** — word deviation max 8 / mean 4.2 against the corresponding pattern prior; checkpoint counts matched for all 12 labels; closing sentence byte-identical across all 24 strings; zero hits in a 28-term pattern-vocabulary leakage scan.
8. **Full repository test suite** — `pytest -q`: 17 passed. `compileall` on `experiments analysis tests`: clean. No Codex code was modified.
