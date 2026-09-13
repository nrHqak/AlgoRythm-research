# Claim Boundaries v2 (FROZEN)

**Status:** frozen 2026-09-10, before any data exists.
**Supersedes:** `pilot/CLAIM_BOUNDARIES.md` (v1, preserved unmodified). Every prohibition in v1 **remains in force**; v2 adds to them and never relaxes one. Where the two differ, the stricter reading governs.
**Resolves:** `pilot/PRE_RUN_REVIEW.md` **F5** (v1 licensed an attribution the design could not support).
**Use:** apply to every sentence before it enters `RESEARCH_DOSSIER.md`, `CLAIMS.md`, an РКНП or ISEF submission, a poster, an abstract, or any external text.

**Documentation-only amendment, 2026-09-13 — label-provenance wording corrected.** When this document was frozen it assumed the pilot's `pattern_label` values would be **oracle labels assigned by a human annotator**, as `pilot/ANNOTATION_GUIDE.md` §2 and `GROUND_TRUTH_PROTOCOL.md` §6 required. That assumption did not hold. `data/PATTERN_LABEL_PROVENANCE_AUDIT.md` established that the v2.0/v2.1 labels were produced by an unreviewed regex heuristic, and the authorized remediation (`PRE_RESULTS_AMENDMENT_MODEL_ASSISTED_PATTERN_ANNOTATION_V2_2.md`) replaced the planned human pass with **two independent blinded model annotators** (Claude = Annotator A, Codex = Annotator B), of which only the **exact-consensus** labels entered the frozen v2.2 sample. That amendment states explicitly that these labels "must never be described as human labels or oracle labels."

This edit **only corrects wording that had become factually false** about where the labels came from. It does **not** relax, widen, add, or remove a single claim boundary, and it changes no result, statistical method, sample, threshold, or experiment artifact. Every prohibition below stands exactly as frozen. Where the correction touches a prohibition's *rationale* (§3, last bullet), the prohibition itself is preserved verbatim and only the reason given for it is brought in line with what actually happened.

---

## 1. The single main claim a successful primary comparison licenses

If, and only if, all of the following hold — both sessions completed, all cross-session invariants asserted clean (`PILOT_PROTOCOL_V2.md` §3.1), the null-calibration gate passed (`d_null < d_primary`, §3.3), and the C-vs-B Top-1 result is favourable — the maximal permitted claim is:

> **"On this calibration sample (n = 30 ConDefects-Python programs, single-line faults, 4 algorithmic pattern classes, exact-consensus pattern labels from two independent blinded model annotators, one named model at temperature 0), providing algorithm-pattern-specific structural priors improved fault localization relative to matched generic debugging guidance."**

Every element of that parenthesis is mandatory and may not be relegated to a footnote, a methods appendix, or a single earlier mention. The claim must also carry, in the same passage:

- that the study is **exploratory / calibration-stage**, not confirmatory;
- that the pattern labels are **exact-consensus labels from two independent blinded model annotators** — *not* human-assigned, *not* oracle, and *not* adjudicated (programs on which the two annotators disagreed were excluded from the pilot rather than resolved). No trained pattern classifier was in the loop either, so the pilot still speaks to a prior built on a *given* label rather than on a predicted one;
- the **sample size**, stated as a number;
- whether the result was **statistically decisive**, and if not, that a null or indecisive result at n=30 is **not** evidence of absence (`STATISTICAL_ANALYSIS_PLAN.md` §7: at least 6 one-directional discordant pairs are needed for p ≤ 0.05 to be reachable at all).

## 2. Claims permitted with their stated qualifiers

- **Process/engineering:** that the three-arm pipeline executed end-to-end, or aborted and why; measured parser-failure rates per arm; the determinism rate; measured prompt lengths and ranking lengths per arm.
- **Null calibration:** the observed A_G-vs-A_P difference, reported as the empirical noise floor for a re-run of an identical condition.
- **Confirmatory sizing:** the observed discordance rate and the resulting sample-size estimate, reported as a **range** (`STATISTICAL_ANALYSIS_PLAN.md` §7) and qualified as applying to the 4 sampled classes, single-line faults, and one model.
- **Secondary contrasts (A vs C, A vs B):** permitted only with the added disclosure that **arm A is not a zero-guidance baseline** — the shared system prompt contains generic reviewer framing (`PILOT_PROTOCOL_V2.md` §2).

## 3. Claims that remain prohibited under any result

Everything on `pilot/CLAIM_BOUNDARIES.md`'s prohibition list carries over verbatim. Restated and extended:

**About scope of the effect**
- ❌ Any **universal debugging improvement** claim — that pattern priors improve debugging generally, for other languages, other corpora, other fault types, or other models.
- ❌ Generalization beyond **ConDefects-Python**; beyond the **4 sampled pattern classes** to the full 12-class vocabulary; beyond **single-line faults** to the harder multi-line, multi-hunk, and refactor cases that `GROUND_TRUTH_PROTOCOL.md` §3 deliberately excluded.
- ❌ Generalization beyond the **single named model**. No claim of the form "LLMs benefit from pattern priors."
- ❌ That the hypothesis is **confirmed or refuted**. n=30 is calibration.

**About the causal attribution**
- ❌ Attribution of the effect to pattern specificity **without** the matched-generic comparison — i.e. no claim of pattern specificity may rest on A vs C alone. A vs C measures "a prior versus no prior" and remains fully length- and guidance-confounded; only C vs B speaks to specificity.
- ❌ That the effect is due to pattern-specific content **as opposed to per-program tailoring in general**. The placebo is constant across programs while the pattern prior is selected per program, so the surviving alternative — "guidance tailored to the program on any axis helps" — is **not** excluded by this design (`GENERIC_PLACEBO_PRIOR.md` §5).
- ❌ Any interpretation of the primary result if the null-calibration gate failed (`d_null >= d_primary`). In that case the only permitted statement is that the comparison was uninterpretable at this sample size.

**About things this pilot did not study**
- ❌ **Classifier effectiveness.** No trained pattern classifier exists or was run. The labels used were the exact consensus of two independent blinded model annotators, which is a labelling procedure, not a deployable classifier, and its agreement statistic bounds neither classifier accuracy nor error propagation in a realistic pipeline.
- ❌ **End-to-end AlgoRythm effectiveness.** The platform was not evaluated. No claim about the product, its sandbox, its curriculum, or its tutor follows from this pilot.
- ❌ **Human-learning improvement.** No human subjects participated. No claim about student learning, comprehension, debugging skill, time-to-fix, or educational outcome is supported — and any future study that would support one requires IRB/SRC pre-approval **before** data collection (`dossier/08_block8_competition.md` via `AGENTS.md` §3.2 item 7).
- ❌ Comparison against **SBFL, MBFL, or the prior-reweighted-spectrum arm** — not implemented, not run.
- ❌ **Cost-effectiveness or latency** advantage of the prior; the design does not isolate cost as an outcome, though per-program latency and token counts may be reported descriptively with the same qualifiers.
- ❌ That **pattern labeling is reliable at scale.** *(Prohibition unchanged; rationale corrected 2026-09-13.)* A κ **was** computed for v2.2 — Cohen's κ ≈ 0.752269 between the two blinded model annotators over the 232-program frame (raw agreement 78.4483%, `data/manifests/PATTERN_ANNOTATION_AGREEMENT_V2_2.md`) — but it does not license this claim, for three reasons: it measures agreement between **two models**, which may share correlated training-data biases, and not agreement among independent human experts; agreement is a reliability statistic and never evidence that either annotator was **correct**; and the pilot sample was then filtered to the agreeing subset, so no reliability figure at all is available for the ambiguous programs that were excluded.

## 4. Mandatory disclosures whenever any pilot number is reported

1. **Model-consensus labels were used, not oracle or human labels** — each program's `pattern_label` is the exact-consensus label of two independent blinded model annotators (Claude and Codex) working from the buggy source, permitted task metadata, and the frozen 12-class vocabulary only. Inter-annotator agreement **was** measured (Cohen's κ ≈ 0.752269; raw agreement 78.4483% over 232 programs), and the 50 disagreeing programs were **excluded from the pilot rather than adjudicated**, so the sample is biased toward programs whose algorithmic pattern is comparatively unambiguous. The phrases "oracle labels," "human-assigned labels," "expert annotation," and "ground-truth algorithm labels" are all inaccurate for this pilot and may not be used.
2. **The sample is small** — n = 30 programs, and the effective information content is 30 paired observations per comparison, not 150, whenever the determinism rate is high (`STATISTICAL_ANALYSIS_PLAN.md` §4).
3. **The study is exploratory / calibration-stage.**
4. **The sample is filtered toward easy cases** — single-line, cleanly-localized faults only, which compresses the achievable spread between arms and biases against detecting a difference (`GROUND_TRUTH_PROTOCOL.md` §3).
5. **`problem_context` was omitted** — the model saw code without the problem statement (`SAMPLING_PROTOCOL.md` §5), which is not the realistic deployment setting.

## 5. Wording that violates these boundaries even when the numbers are real

For calibration, these are violations regardless of the underlying result:

- "Pattern priors improve fault localization." — unqualified scope.
- "Our method beats generic debugging advice." — "method" overstates a prompt block; "beats" overstates an n=30 calibration contrast.
- "Pattern-conditioned localization achieves X% Top-1." — reports an arm's absolute level as if it were a benchmark result.
- "The pattern prior helped in 4 of 4 pattern classes." — per-class results are descriptive only, at 7–8 programs each.
- "Results suggest AlgoRythm's classifier will improve debugging." — a claim about a component that was not in the loop.
- "Students would find bugs faster." — a human-outcome claim from a study with no humans.
- "Using oracle / human-assigned / expert pattern labels…" — factually false for this pilot; the labels are the exact consensus of two blinded **model** annotators (§4.1).
- "Inter-annotator agreement confirms the labels are correct." — κ measures agreement, never correctness, and here it is agreement between two models rather than two independent human experts.

## 6. Escalation

The path from a permitted pilot claim to a confirmatory claim is never "the pilot's effect looked strong." It is: run the confirmatory study at the sample size derived in `STATISTICAL_ANALYSIS_PLAN.md` §7, spanning the full pattern vocabulary, including the realistic (classifier-predicted) label condition and the classical baselines, with double annotation at κ ≥ 0.70 — and only then revise this document, as a new version with a changelog entry, to reflect what the larger study licenses.

*Clarification, 2026-09-13 (no change to the bar itself):* the "double annotation at κ ≥ 0.70" requirement was written when this document assumed human annotation throughout, and it means **independent human-expert double annotation**. The v2.2 pilot's model-to-model κ ≈ 0.752269 therefore does **not** satisfy this escalation criterion, and may not be presented as satisfying it.
