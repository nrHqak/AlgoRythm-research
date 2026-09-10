# Scientific Risks (FROZEN v1) — pilot-specific

**Status:** written 2026-09-10, before any pilot data exists. Global project risks are tracked in `dossier/99_synthesis.md` §S5 and are not repeated here except where the pilot sharpens or specializes one of them. This document is pilot-scoped: risks in how `algorythm_pattern_prior_pilot` (n=30, ConDefects-Python, oracle labels, single provider/model) could mislead, ranked roughly by how much it would distort the calibration purpose stated in `PILOT_PROTOCOL.md` §1.

## 1. Sample size is far below the power needed for any inferential claim

At n=30, exact McNemar has very little power to distinguish a real effect from noise even if `dossier/05_block5_methodology.md` §5.4's rough sketch (≈45 discordant pairs needed at n=300 for reliable detection) is in the right ballpark — 30 programs × 5 repetitions gives 30 matched pairs per repetition, an order of magnitude below that. **Mitigation:** the pilot is explicitly not used for a confirmatory claim (`PRE_EXPERIMENT_COMMIT.md` rule 4, `CLAIM_BOUNDARIES.md`); its statistics are read as calibration inputs (discordance rate → power calculation for n≈300–500), not as a hypothesis-test verdict.

## 2. Prior text length is a partial confound

The treatment prompt is strictly longer than the control prompt by construction (the delimited prior block adds text) — there is no way to test "prior present vs. absent" without also changing prompt length, which is a known general confound in prompt-ablation work (the persona/CoT ablations in arXiv:2512.03421, cited in `dossier/03_block3_fault_localization.md` §3c, face the same issue). **Mitigation:** all 12 frozen priors are held to a bounded word-count band (119–138 words, spread ~15% of the mean, `PATTERN_PRIORS.md`'s length-confound audit) so the length delta is at least *consistent* across pattern classes rather than an additional uncontrolled source of per-pattern variance; `analysis/run_analysis.py` already reports `prompt_length_by_condition`, so the actual realized gap is measured, not assumed. This mitigates but cannot eliminate the confound — any observed effect should be read as "prior content + its length," not "prior content alone."

## 3. Oracle-label optimism

This pilot only tests the `oracle_pattern_prior` condition (gold pattern label), never a classifier-predicted label. Any effect seen here is an **upper bound** on what a `predicted_pattern_prior` condition could achieve once the pattern classifier (not yet built, `dossier/99_synthesis.md` §S2.1) is in the loop — classifier error will only ever subtract from this, never add. **Mitigation:** stated explicitly in `CLAIM_BOUNDARIES.md`; the confirmatory design already plans an oracle-vs-realistic split (`dossier/99_synthesis.md` §S2.2) specifically to bound this.

## 4. Single provider/model

The pilot uses one LLM (provider/model chosen at execution time, `PILOT_PROTOCOL.md` §2). Results — including the discordance-rate estimate feeding the confirmatory study's power calculation — do not generalize across models; different models may have different sensitivity to the prior block, per the prompt-ablation finding in arXiv:2512.03421 that reasoning models (o3, DeepSeekR1) are nearly unaffected by prompt structure while GPT-4-class models are heavily prompt-dependent (`dossier/03_block3_fault_localization.md` §3c). **Mitigation:** none within this pilot's budget; flagged so the confirmatory study's model selection (`dossier/99_synthesis.md` §S2.2 Arm C/D) is not anchored uncritically to whatever one model the pilot happens to use.

## 5. Annotation reliability is not measured at pilot scale

`ANNOTATION_GUIDE.md` §4 permits single-annotator labeling for the n=30 pilot; no κ is computed. A `pattern_label` error (wrong class assigned) would put a program's data in the wrong per-pattern bucket and could, in the worst case, mean the prior text shown to the model does not actually match what the code is attempting. **Mitigation:** the annotator rationale-logging requirement in `ANNOTATION_GUIDE.md` §4 creates an audit trail; the double-annotation + κ≥0.70 requirement is mandatory before the confirmatory corpus is trusted, and this pilot's own labels should be spot-checked by a second reader if time allows, though that is a recommendation, not a structural requirement, at this scale.

## 6. Data leakage risk on ConDefects

`dossier/03_block3_fault_localization.md` §3c documents a leakage suspicion specifically for **Codeflaws**, not ConDefects — but ConDefects is also sourced from a public competitive-programming site (AtCoder, `dossier/04_block4_datasets.md` §4.3) and has not been independently checked for LLM-training-data contamination. If the chosen model has memorized a task's canonical solution, its localization accuracy in *both* conditions could be inflated in a way that has nothing to do with the pattern prior, potentially compressing the observed gap between conditions in either direction. **Mitigation:** none specific to the pilot; noted as an open item for whoever selects the provider/model, and as a reason the confirmatory study should weight BugT (leakage-resistant, `dossier/04_block4_datasets.md` §4.4) more heavily than the pilot's ConDefects-only scope.

## 7. Parser-failure asymmetry could itself be a real (or a spurious) effect

If the `oracle_pattern_prior` condition's longer, more structured prompt changes the model's tendency to emit valid JSON (in either direction) relative to `pattern_agnostic`, that is scientifically informative but easy to misread as a fault-localization effect if not reported separately. **Mitigation:** `count_as_failure` is the frozen primary parser-failure policy (`PRE_EXPERIMENT_COMMIT.md`), which folds this into Top-K/EXAM rather than hiding it, and `PILOT_PROTOCOL.md` §5 requires the per-condition parser-failure rate to be reported as its own number, not only as an input to Top-K.

## 8. Cost and rate-limit risk

30 programs × 2 conditions × 5 repetitions = 300 calls minimum, more if `--resume` is used after a partial failure or if a non-frozen retry policy is added at the provider layer. This is modest in absolute terms but is a real budget/quota item for whoever executes; not a scientific-validity risk, listed here only so it is not rediscovered mid-run as a surprise.

## 9. This pilot cannot detect confounds outside its own two-arm design

Because Arms A/B/E (SBFL, MBFL, prior-reweighted spectrum) are out of scope (`PILOT_PROTOCOL.md` §1), this pilot cannot speak to `dossier/99_synthesis.md` §S5 risk 1 ("strong LLM baselines may swamp the effect") at all — that risk is only assessable once classical baselines are run on the same programs, which is future work, not this pilot.
