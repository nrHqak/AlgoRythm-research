# Claim Boundaries v2 (FROZEN)

**Status:** frozen 2026-09-10, before any data exists.
**Supersedes:** `pilot/CLAIM_BOUNDARIES.md` (v1, preserved unmodified). Every prohibition in v1 **remains in force**; v2 adds to them and never relaxes one. Where the two differ, the stricter reading governs.
**Resolves:** `pilot/PRE_RUN_REVIEW.md` **F5** (v1 licensed an attribution the design could not support).
**Use:** apply to every sentence before it enters `RESEARCH_DOSSIER.md`, `CLAIMS.md`, an РКНП or ISEF submission, a poster, an abstract, or any external text.

---

## 1. The single main claim a successful primary comparison licenses

If, and only if, all of the following hold — both sessions completed, all cross-session invariants asserted clean (`PILOT_PROTOCOL_V2.md` §3.1), the null-calibration gate passed (`d_null < d_primary`, §3.3), and the C-vs-B Top-1 result is favourable — the maximal permitted claim is:

> **"On this calibration sample (n = 30 ConDefects-Python programs, single-line faults, 4 algorithmic pattern classes, oracle pattern labels, one named model at temperature 0), providing algorithm-pattern-specific structural priors improved fault localization relative to matched generic debugging guidance."**

Every element of that parenthesis is mandatory and may not be relegated to a footnote, a methods appendix, or a single earlier mention. The claim must also carry, in the same passage:

- that the study is **exploratory / calibration-stage**, not confirmatory;
- that **oracle (human-assigned) pattern labels** were used — no classifier was in the loop;
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
- ❌ **Classifier effectiveness.** No pattern classifier exists or was run; oracle labels were human-assigned. Nothing here bounds classifier accuracy or error propagation.
- ❌ **End-to-end AlgoRythm effectiveness.** The platform was not evaluated. No claim about the product, its sandbox, its curriculum, or its tutor follows from this pilot.
- ❌ **Human-learning improvement.** No human subjects participated. No claim about student learning, comprehension, debugging skill, time-to-fix, or educational outcome is supported — and any future study that would support one requires IRB/SRC pre-approval **before** data collection (`dossier/08_block8_competition.md` via `AGENTS.md` §3.2 item 7).
- ❌ Comparison against **SBFL, MBFL, or the prior-reweighted-spectrum arm** — not implemented, not run.
- ❌ **Cost-effectiveness or latency** advantage of the prior; the design does not isolate cost as an outcome, though per-program latency and token counts may be reported descriptively with the same qualifiers.
- ❌ That **pattern labeling is reliable at scale** — no κ was computed (`ANNOTATION_GUIDE.md` §4).

## 4. Mandatory disclosures whenever any pilot number is reported

1. **Oracle labels were used** — pattern labels were assigned by a human annotator from task metadata plus code reading, not predicted by a model, and no inter-annotator agreement was measured at this scale.
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

## 6. Escalation

The path from a permitted pilot claim to a confirmatory claim is never "the pilot's effect looked strong." It is: run the confirmatory study at the sample size derived in `STATISTICAL_ANALYSIS_PLAN.md` §7, spanning the full pattern vocabulary, including the realistic (classifier-predicted) label condition and the classical baselines, with double annotation at κ ≥ 0.70 — and only then revise this document, as a new version with a changelog entry, to reflect what the larger study licenses.
