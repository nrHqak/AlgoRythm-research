# Result Insertion Map

Every location in `paper/APA7_PAPER_DRAFT.md` that must be revisited once a valid
pilot run completes. "Valid" means: both sessions (G and P) complete under the
frozen model-freeze abort criteria, all `PILOT_PROTOCOL_V2.md` §3.1 cross-session
invariants assert clean, and the null-calibration gate (`d_null` vs. `d_primary`)
has been evaluated — per `pilot/v2/STATISTICAL_ANALYSIS_PLAN.md` §8's fixed
reporting order.

Columns: **Section** (in the paper draft) · **Required metric/result** · **Source
artifact expected from Codex's analysis pipeline** (the additive cross-session
script called for in `STATISTICAL_ANALYSIS_PLAN.md` §6.1, plus
`analysis/run_analysis.py`'s native per-session output).

---

## 1. Front matter

| Section | Required metric/result | Source artifact |
|---|---|---|
| Author Note | Remove or update the "pre-results draft" / VOID disclosure once a valid run exists; state the run's completion date and session IDs. | `EXPERIMENT_LOG.md`; both sessions' `session_manifest.json` |
| Abstract, results sentence | One-sentence summary of the primary C-vs-B Top-1 result, with sample size, oracle-label caveat (pending §11 below), and statistical-decisiveness qualifier, per `CLAIM_BOUNDARIES_V2.md` §1. | Cross-session primary-analysis script output |

## 2. Introduction

| Section | Required metric/result | Source artifact |
|---|---|---|
| "Research Question and Hypotheses" | No change required unless the null-calibration gate fails and the comparison must be reported as uninterpretable — in that case, add one sentence stating this before any other discussion. | Null-calibration gate verdict |

## 3. Method

| Section | Required metric/result | Source artifact |
|---|---|---|
| "Oracle Pattern Labels" | Resolve the `pattern_source: "AST rule"` vs. blinded-human-annotation discrepancy **before** any Results content is added. This is a blocking item, not a results-dependent one — it must be closed even if the experiment is still VOID. | Corrected manifest or corrected annotation-provenance documentation |
| "Large Language Model Implementation," Table M2 | Update `max_tokens` row from "Not final" to the value that actually produced a valid run; update "Total planned scientific calls" row from "0 of 600 have been validly completed" to the actual completed count; add the actual dry-run/stress-smoke evidence reference for the final configuration. | Final `MODEL_FREEZE_RECORD*.json`; session manifests |

## 4. Measures / Statistical Analysis Plan

No results-dependent content; these sections describe planned procedure only and
require no numeric insertion. Verify after the fact that the actually-executed
analysis matches every rule as written (aggregation rule, primary test, null-gate
threshold, bootstrap seed) — any deviation must be disclosed as a protocol
deviation, not silently reflected back into these sections.

## 5. Reproducibility

| Section | Required metric/result | Source artifact |
|---|---|---|
| Final paragraph | Add the completed sessions' commit hashes, checksums of the final raw-response archive, and a pointer to the analysis script's own recorded reproduction command. | `results/CODEX_HANDOFF.md` (per `REPRODUCIBILITY.md`); `results/pilot_metrics.json` |

## 6. Results — run integrity paragraph

| Required metric/result | Source artifact |
|---|---|
| Completion status of Session G and Session P (both must show `ok`). | Both sessions' `session_manifest.json` |
| Assertion result for every `PILOT_PROTOCOL_V2.md` §3.1 invariant (manifest hash, system-prompt hash, user-template hash, per-program shared-prompt hash, provider/model/temperature/`max_tokens`, repetitions, condition-order policy, `engineering_only: false` on both). | Cross-session primary-analysis script's invariant-assertion log |
| Determinism rate: fraction of (program, condition) cells with byte-identical raw responses across 5 repetitions; fraction with identical Top-1 outcomes. | `analysis/run_analysis.py` native output, both sessions |
| Parser-failure rate per condition (A_G, B, A_P, C). | `analysis/run_analysis.py` native output |
| Overall `ok` rate per session (must be ≥ 80% per the frozen abort rule, and this must be stated even though it is the criterion that qualified the run as valid). | Both sessions' `session_manifest.json` |

## 7. Results — Table 1 (Overall Fault-Localization Performance)

| Cell | Required metric/result | Source artifact |
|---|---|---|
| Row A, columns Top-1/Top-3/Top-5 | Majority-of-5 aggregated hit counts (out of 30) and proportions for A_G and A_P, reported separately unless the null-calibration gate confirms poolability. | `analysis/run_analysis.py` native per-session output; cross-session script |
| Row A, column EXAM\* | Mean EXAM\* across programs for A_G and A_P. | Same |
| Row B, all columns | Majority-of-5 aggregated Top-1/3/5 hit counts/proportions and mean EXAM\*, Session G. | `analysis/run_analysis.py`, Session G |
| Row C, all columns | Majority-of-5 aggregated Top-1/3/5 hit counts/proportions and mean EXAM\*, Session P. | `analysis/run_analysis.py`, Session P |

## 8. Results — Table 2 (Primary Comparison of B and C)

| Cell | Required metric/result | Source artifact |
|---|---|---|
| Top-1 row | `b`, `c`, `d = b+c`, exact McNemar two-sided *p*, Top-1 proportions for B and C, their difference, and the program-clustered bootstrap 95% CI on mean(H_C − H_B). | Cross-session primary-analysis script (`STATISTICAL_ANALYSIS_PLAN.md` §6.1) |
| Text immediately above the table | Null-calibration verdict: `d_null` (A_G vs. A_P discordant pairs, Top-1), `d_primary` (the `d` above), and the PASS/FAIL gate outcome, stated **before** the Top-1 row is interpreted, per the fixed reporting order in `STATISTICAL_ANALYSIS_PLAN.md` §8. | Cross-session primary-analysis script |
| Top-3 / Top-5 rows | Descriptive B and C proportions, difference, bootstrap CI (no formal test; label as secondary). | Cross-session script |
| EXAM\* row | Mean EXAM\* for B and C, difference, bootstrap 95% CI on mean(E_C − E_B), paired Wilcoxon signed-rank *p*. | Cross-session script (`analysis/statistics.py::exam_comparison`) |

## 9. Results — Table 3 (Performance by Algorithmic Pattern)

| Cell | Required metric/result | Source artifact |
|---|---|---|
| Each of the 4 rows | Top-1 (B), Top-1 (C), Δ Top-1, EXAM\* (B), EXAM\* (C) computed only over that pattern class's 7–8 programs; descriptive only, explicitly no per-class test. | Cross-session script, filtered by `pattern_label` |

## 10. Results — diagnostics paragraph

| Required metric/result | Source artifact |
|---|---|
| Mean ranking length per condition (A_G, B, A_P, C). | `analysis/run_analysis.py` native `adversarial.ranking_length` output |
| Measured prompt length (chars/tokens) per condition, checked against the ±10-word tolerance declared in `GENERIC_PLACEBO_PRIOR.md` §4. | `analysis/run_analysis.py` native `adversarial.prompt_length_by_condition` output |
| Confirmatory-study sample-size estimate, reported as a bootstrap-derived range (not a point value), per `STATISTICAL_ANALYSIS_PLAN.md` §7's worked formula. | Derived manually from `π_d` and `ψ` plus their bootstrap interval |
| Robustness check: all five per-repetition exact McNemar tests, reported together (never a single repetition quoted alone). | `analysis/run_analysis.py` native per-session output |

## 11. Results / Method — the oracle-label discrepancy

| Required action | Source artifact |
|---|---|
| Either (a) correct `pilot_manifest_v2_1.json`'s `pattern_source` field to accurately reflect the blinded human-annotation process actually followed and re-freeze/re-checksum the manifest with a dated changelog entry, or (b) revise Method ("Oracle Pattern Labels"), the mandatory-disclosures paragraph in Discussion, and every "oracle label" claim throughout the paper to accurately describe an AST-rule contribution to labeling. **This must be resolved before Results are written**, independent of when a valid experimental run completes — it is a data-integrity blocker, not a results-dependent item. | Dataset engineering agent (Antigravity's role per `PROJECT_STATE.md`); a corrected/re-audited manifest |

## 12. Discussion

| Section | Required action | Source artifact |
|---|---|---|
| The four interpretation-scenario subsections | Retain and substantially expand exactly one scenario (A, B, C, or D) matching the actual outcome; the other three should be either deleted or condensed to a one-paragraph "why this did not apply" note, per the paper's own instruction not to decide the outcome in advance. | Cross-session primary-analysis result |
| Opening "framing points hold unconditionally" paragraph | Update the oracle-label disclosure sentence once item 11 above is resolved. | — |

## 13. Threats to Validity and Limitations

| Item | Required action |
|---|---|
| "Oracle pattern-label provenance discrepancy" bullet | Remove or rewrite once item 11 above is resolved; do not leave as an open flag in a version of the paper that reports results. |
| "Model-, provider-, and configuration-specificity" bullet | Update to state the final, validated `max_tokens` value and confirm no further technical amendment is pending. |
| All other bullets | No change expected; re-verify each still applies to the completed run (e.g., confirm the determinism rate, once measured, is consistent with the "30 vs. 150 effective observations" caveat as written, and adjust the wording if the measured determinism rate is *low* rather than high). |

## 14. Conclusion

| Required action | Source artifact |
|---|---|
| Replace `[FINAL EMPIRICAL CONCLUSION TO BE INSERTED AFTER VALID PILOT]` with a 2–4 sentence, fully qualified empirical conclusion consistent with whichever Discussion scenario (A–D) applied, and consistent with every mandatory disclosure in `CLAIM_BOUNDARIES_V2.md` §1 and §4. | Discussion section, once finalized |

## 15. References

| Required action |
|---|
| Resolve every `[flag: verify before submission]` note in the reference list (Araujo et al.; du Boulay, O'Shea & Monk DOI; Johnson 1990 DOI; Jones, Harrold & Stasko venue; Gupta et al. author list; Hoq et al. author list; Li et al. VsusFL author list; Wong et al. DStar journal/volume; Wong et al. 2016 survey author list; Xu et al. 2025 author list; Yang, Mei & Yang given names) against a primary bibliographic source (publisher page, DBLP, or the arXiv/DOI record itself) before this paper is submitted anywhere, independent of whether the experimental result is ready. These are citation-accuracy blockers, not results-dependent items. |

---

## Summary: blocking items independent of experimental completion

Two items in this map (§11 oracle-label provenance; §15 reference verification)
must be resolved **regardless of when, or whether, a valid pilot run completes**.
Everything else in this map is strictly gated on a valid two-session run with a
clean cross-session invariant check.
