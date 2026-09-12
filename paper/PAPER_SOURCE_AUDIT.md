# Paper Source Audit — `APA7_PAPER_DRAFT.md`

Purpose: for every material factual statement in the paper draft, record its
source and source category, so that unsupported claims can be caught by
inspection rather than trust. Source categories, per the task brief:

- **[SPEC]** — repository scientific specification (frozen protocol documents:
  `pilot/v2/*`, `pilot/*`)
- **[DATA]** — dataset/provenance audit (`data/*`, `data/manifests/*`)
- **[LIT]** — prior published literature, as verified in `dossier/*` /
  `RESEARCH_DOSSIER.md`
- **[PLACEHOLDER]** — explicit experiment-result placeholder, no claim made
- **[LOG]** — project execution log / git history (`EXPERIMENT_LOG.md`,
  `pilot/v2/*STATUS*.md`, `pilot/v2/*DIAGNOSIS*.md`, git commits)
- **[FLAG]** — an inconsistency this review discovered between two repository
  sources, disclosed rather than silently resolved

This file does not re-derive every sentence of the paper; it covers every
claim that carries factual weight (a number, a named finding, a protocol
rule, or a bibliographic fact).

---

## Abstract

| Claim | Category | Source |
|---|---|---|
| "no published method conditions localization on the algorithmic pattern" | [LIT] | `dossier/07_block7_novelty.md` (8 query families, no matching work found) |
| n = 30, ConDefects-Python, four classes, three conditions, one model, temp 0, 5 reps | [SPEC] + [DATA] | `pilot/v2/PILOT_PROTOCOL_V2.md` §2, §4; `data/manifests/pilot_manifest_v2_1.json` |
| "every execution attempt... terminated in a technical VOID" | [LOG] | `pilot/v2/CLEAN_SCIENTIFIC_RERUN_STATUS.md`; `EXPERIMENT_LOG.md` |
| Results sentence | [PLACEHOLDER] | Explicit `[RESULT PENDING]` |

## Introduction

| Claim | Category | Source |
|---|---|---|
| Du Boulay's five-area difficulty account; "pragmatics" as distinct/undertaught | [LIT] | `dossier/01_block1_theory.md` item A2 (du Boulay, 1986), verification tag [V] |
| Fitzgerald et al. (2008), novice debugging = "flailing" | [LIT] | `dossier/01_block1_theory.md` item B13, [V] |
| McCauley et al. (2008) review conclusions | [LIT] | `dossier/01_block1_theory.md` item B12, [V] |
| Spohrer & Soloway (1986), plan bugs vs. symbolic bugs finding | [LIT] | `dossier/01_block1_theory.md` item D3, [V] |
| Araujo et al. (2016), ~40% of novice programs violate SBFL precondition | [LIT] | `dossier/03_block3_fault_localization.md` §3a; verification tag [V-cited] (seen only via citation inside another fetched source — **flagged**, see Reference Verification Flags below) |
| Yang et al. (2025), MBFL Top-5 ≈ 61% Python, ~87 machine-hours / 150 programs | [LIT] | `dossier/03_block3_fault_localization.md` §3b, full text fetched, [V] |
| Xu et al. (2025), 13 LLMs beat SBFL/MBFL, accuracy degrades with difficulty | [LIT] | `dossier/03_block3_fault_localization.md` §3c, full text fetched, [V] |
| MacNeil et al. (2024), GPT-4 beats 964 students at logic-error detection | [LIT] | `dossier/01_block1_theory.md` item D11, [V] (arXiv abstract) |
| Brooks (1983) beacons; Pennington (1987) situation model; von Mayrhauser & Vans (1995) | [LIT] | `dossier/01_block1_theory.md` items B1, B2, B4, all [V] |
| Baron & Feitelson (2024), recursion difficulty concentrates on base cases | [LIT] | `dossier/01_block1_theory.md` item B16, [V] |
| Notional-machine literature (du Boulay et al. 1981; Sorva 2013; Fincher et al. 2020) | [LIT] | `dossier/01_block1_theory.md` §1a, items A1, A3, A5, all [V] |
| Johnson (1990) PROUST description | [LIT] | `dossier/01_block1_theory.md` §1c synthesis; `dossier/07_block7_novelty.md` B7.1 #1 |
| "This study originates from and is intended to inform AlgoRythm" | [SPEC] | Task brief instruction + `PROJECT_STATE.md` framing; no effectiveness claim made, per `pilot/v2/CLAIM_BOUNDARIES_V2.md` §3 |
| Watanobe et al. (2023), F1 ≈ 95.7 on 6–7 categories | [LIT] | `dossier/02_block2_classification.md` §2f, full text fetched, [V] |
| Neumüller et al. (2024) AlDeSCo, F1 0.74 vs. 0.35 for CodeLlama baseline | [LIT] | `dossier/02_block2_classification.md` §2d, [V] |
| "no published method... measures Top-k gains" (the gap statement) | [LIT] | `dossier/07_block7_novelty.md`, full section — the project's own novelty-check pass |
| Hypotheses framed as directional/exploratory, not confirmatory; power arithmetic reference | [SPEC] | `pilot/v2/STATISTICAL_ANALYSIS_PLAN.md` §7 |
| A_G vs. A_P calibration expectation | [SPEC] | `pilot/v2/PILOT_PROTOCOL_V2.md` §3.3 |
| Contributions list, including "v1 design was found unable to make [the pattern-specificity attribution]" | [SPEC] | `pilot/PRE_RUN_REVIEW.md` finding F1 (BLOCK verdict) |

## Related Work

| Claim | Category | Source |
|---|---|---|
| SBFL formulas (Tarantula, Ochiai, DStar) and definitions | [LIT] | `dossier/03_block3_fault_localization.md` §3a |
| Wong et al. (2016) survey, "over 150 SBFL papers" | [LIT] | `dossier/03_block3_fault_localization.md` §3a — **[FLAG]**: the dossier's own author-list transcription for this survey ("C. Song Wong, Wei Gao, Zhenyu Li, Ruitao Feng, Yueqi Lyu, Yong Wang, Lin Chen") contains an internally implausible name ("C. Song Wong") and was not independently re-verified against IEEE Xplore in this pass. The paper's reference entry is flagged accordingly rather than silently corrected from the reviewer's own background knowledge, per the task's "no fabricated citations" instruction. **Action: verify directly against IEEE Xplore before submission.** |
| Yang et al. (2025) MBFL protocol and numbers | [LIT] | `dossier/03_block3_fault_localization.md` §3b, [V] |
| VsusFL (422 programs, bipartite-graph variable matching) | [LIT] | `dossier/03_block3_fault_localization.md` §3d, [V] (ScienceDirect intro fetched) — full author list not independently verified; **flagged** in References |
| CLARA (ITiCSE 2018, clustering + trace alignment) | [LIT] | `dossier/03_block3_fault_localization.md` §3e, [V] |
| Fitzgerald et al. (2008); Lister et al. (2004) | [LIT] | `dossier/01_block1_theory.md` items B13, B9, both [V] |
| Xu et al. (2025) full method description (13 models, 3 datasets, ablation design) | [LIT] | `dossier/03_block3_fault_localization.md` §3c, full text fetched, [V] |
| Watanobe et al. (2023) method and numbers | [LIT] | `dossier/02_block2_classification.md` §2f, full text fetched, [V] |
| Neumüller et al. (2024) AlDeSCo method and numbers | [LIT] | `dossier/02_block2_classification.md` §2d, [V] |
| COFO "Infer the Technique" task | [LIT] | `dossier/02_block2_classification.md` §2a, [S] (search snippets only, not independently fetched — disclosed here) |
| FaR-Loc (2025 arXiv, functional-intent retrieval FL on Defects4J) | [LIT] | `dossier/07_block7_novelty.md` B7.1 #3, [S] — not independently fetched; presented without a References entry because it is cited only descriptively and its exact bibliographic completeness was not verified. **If retained in a future version, add a References entry and verify.** |
| Multi-correct-program spectrum boosting (IEICE 2024) | [LIT] | `dossier/03_block3_fault_localization.md` §3d, [S] — same treatment as FaR-Loc above |
| Johnson (1990) PROUST description and differentiation | [LIT] | `dossier/07_block7_novelty.md` B7.1 #1 |
| Ko & Myers (2008) Whyline, "twice as successful in half the time" | [LIT] | `dossier/01_block1_theory.md` item B15, [V] for existence/DOI; the specific effect-size quote is marked [S] (quoted via a search snippet of the source PDF, not independently re-fetched) in the dossier — **this qualifier is not currently repeated in the paper body; consider softening the claim or adding the [S] qualifier explicitly in a future revision.** |
| Synthesis paragraph (three converging literatures) | [SPEC]/[LIT] | Author synthesis, directly following `dossier/99_synthesis.md` §S6 and `dossier/07_block7_novelty.md` B7.3 |

## Method

| Claim | Category | Source |
|---|---|---|
| Overall three-arm/two-session design | [SPEC] | `pilot/v2/PILOT_PROTOCOL_V2.md` §2–3 |
| ConDefects license (CC BY-SA 4.0), toolkit MIT, repo `appmlk/ConDefects` | [DATA] | `data/CONDEFECTS_SOURCE.md` §3 |
| `problem_context` omission rationale | [SPEC] | `pilot/v2/SAMPLING_PROTOCOL.md` §5 |
| Table M1 sampling funnel — all row counts | [DATA] | `data/manifests/SAMPLING_AUDIT_V2_1.md` §2, cross-checked against `pilot/v2/SAMPLING_PROTOCOL.md` §3–6 |
| S2c decomposition (140/392/274) | [DATA] | `data/manifests/SAMPLING_AUDIT_V2_1.md` §2 |
| S6–S7 decomposition (16 outside vocab; 5/3/2 below threshold; 7 greedy; 17 graph) | [DATA] | `data/manifests/SAMPLING_AUDIT_V2_1.md` §3 |
| Corpus-size provenance note (2,864/985 vs. dossier's 1,625/985) | [FLAG] | `data/CONDEFECTS_SOURCE.md` §2 (two distinct commits, 2,864/985 at HEAD `43f0834`, 1,625/526 at prior release `f92adc1`) vs. `dossier/04_block4_datasets.md` §4.3 ("Python: 1,625 faulty programs / 985 tasks" — an apparent conflation of the two commits' figures). This review used the figure actually consumed by the sampling pipeline (2,864/985, per `data/manifests/SAMPLING_AUDIT_V2_1.md` §2) and flags the dossier's figure as needing correction, rather than silently adopting either uncritically. |
| Ground-truth blinding procedure (steps 1–4, freeze before pattern reasoning) | [SPEC] | `pilot/v2/GROUND_TRUTH_PROTOCOL.md` §1 |
| Fix-shape adjudication table | [SPEC] | `pilot/v2/GROUND_TRUTH_PROTOCOL.md` §3 |
| Second blinding requirement (labeling blind to fault line) | [SPEC] | `pilot/v2/GROUND_TRUTH_PROTOCOL.md` §6 |
| One-program-per-task policy and rationale | [SPEC] | `pilot/v2/SAMPLING_PROTOCOL.md` §4 |
| v2.0 → v2.1 correction narrative, 28/30 programs changed, 2 preserved | [DATA] | `data/manifests/SAMPLING_AUDIT_V2_1.md` §1, §6 |
| `graph_traversal_dfs_bfs` 75→17 eligible, "~77% fail dynamic precondition" | [DATA] | `data/manifests/SAMPLING_AUDIT_V2_1.md` §3, "Class Composition Shift Rationale" |
| Final manifest: SHA-256, `selection_frozen_at`, 8/8/7/7 allocation | [DATA] | `data/manifests/pilot_manifest_v2_1.json`; `data/manifests/SAMPLING_AUDIT_V2_1.md` §7 |
| Physical length range 25–155 lines; test suites 3–8 cases | [DATA] | `data/manifests/SAMPLING_AUDIT_V2_1.md` §5, §4 |
| 12-class pattern vocabulary, definitions, confusable-pair rules | [SPEC] | `pilot/PATTERN_VOCABULARY.md` |
| Class-selection rule (rank by eligible count, ties by vocabulary row order, top 4, 8/8/7/7) | [SPEC] | `pilot/v2/SAMPLING_PROTOCOL.md` §6 |
| Ranked eligible counts per class in frame F_v2.1 | [DATA] | `data/manifests/SAMPLING_AUDIT_V2_1.md` §3 |
| "two_pointers and intervals: 0 eligible" | [DATA] | Inferred by this review: not listed among the 10 rows of `data/manifests/SAMPLING_AUDIT_V2_1.md` §3's class-count table, out of the 12-class vocabulary; treated as 0 and stated as an inference, not a directly quoted number |
| Oracle-label assignment protocol (as specified) | [SPEC] | `pilot/ANNOTATION_GUIDE.md` §2; `pilot/v2/GROUND_TRUTH_PROTOCOL.md` §6 |
| **`pattern_source: "AST rule"` discrepancy** | **[FLAG]** | Directly observed: `grep pattern_source data/manifests/pilot_manifest_v2_1.json` returns `"AST rule"` for all 30 records, checked against `pilot/ANNOTATION_GUIDE.md` §2.5's expected provenance-string format (e.g., `"atcoder-task-tag+manual-verification"`) and `pilot/v2/CLAIM_BOUNDARIES_V2.md` §4.1's mandatory disclosure that labels were human-assigned. **This is the single highest-priority open item from this review.** Not resolved by this paper; flagged prominently in Method, Discussion, Threats to Validity, and `RESULT_INSERTION_MAP.md` §11. |
| Roster-table vs. manifest discrepancy (faulty_line, difficulty) | [FLAG] | `data/manifests/GATE7_ROSTER_DISCREPANCIES.json` (27 of 30 faulty-line values and 28 of 30 difficulty values differ between `SAMPLING_AUDIT_V2_1.md`'s prose table and the JSON manifest); resolution ("use the manifest") per `data/TESTCASE_PROVENANCE_AUDIT.md` §"Corrections to earlier prose" |
| Three conditions A/B/C, exact prompt content and structure | [SPEC] | `pilot/v2/PILOT_PROTOCOL_V2.md` §2; `pilot/v2/prompts/system_v2.txt`; `pilot/prompts/control.txt`; `pilot/v2/generic_placebo_prior.json`; `pilot/pattern_priors.json` |
| DP pattern-prior checkpoint example | [SPEC] | `pilot/PATTERN_PRIORS.md` §5 |
| Structural-parity audit numbers (max Δ8 words, mean 4.2; checkpoint counts matched) | [SPEC] | `pilot/v2/GENERIC_PLACEBO_PRIOR.md` §4 |
| Delimiter-tag asymmetry (V-2) | [SPEC] | `pilot/v2/PRE_RUN_REVIEW_V2.md` §2, finding V-2 |
| "surviving alternative explanation... tailoring on any axis" | [SPEC] | `pilot/v2/GENERIC_PLACEBO_PRIOR.md` §5 |
| Why C vs. B is primary (v1 F1 finding) | [SPEC] | `pilot/PRE_RUN_REVIEW.md`, finding F1, BLOCK verdict |
| Role of condition A / null calibration | [SPEC] | `pilot/v2/PILOT_PROTOCOL_V2.md` §3.3; `pilot/v2/PRE_RUN_REVIEW_V2.md` finding V-6 (duplication is "forced," not "designed" — this paper's phrasing follows V-6's correction, describing the duplication as a byproduct put to genuine use, not as an intentional design feature) |
| Model identifier, provider, routing configuration | [SPEC]/[LOG] | `pilot/v2/MODEL_FREEZE_RECORD_16384.json`; `pilot/v2/MODEL_FREEZE_PROTOCOL.md` |
| Determinism-probe reinterpretation of 5 repetitions | [SPEC] | `pilot/v2/STATISTICAL_ANALYSIS_PLAN.md` §4 |
| max_tokens history (1024 → 4096 → 16384; each VOID event and diagnosis) | [LOG] | `pilot/v2/PRE_RESULTS_AMENDMENT_MAX_TOKENS_4096.md`; `pilot/v2/PRE_RESULTS_AMENDMENT_MAX_TOKENS_16384.md`; `pilot/v2/VOID_TECHNICAL_DIAGNOSIS.md`; `pilot/v2/CLEAN_SCIENTIFIC_RERUN_STATUS.md`; `EXPERIMENT_LOG.md` |
| 16,384-token stress smoke passed (20/20) | [LOG] | `pilot/v2/STRESS_SMOKE_16384_STATUS.md`; `pilot/v2/MODEL_FREEZE_RECORD_16384.json` |
| Clean rerun VOID at call 18, 16,383/16,384 reasoning tokens | [LOG] | `pilot/v2/CLEAN_SCIENTIFIC_RERUN_STATUS.md` |
| Session-order coin flip (`secrets.randbits(1)` = 0 → G first) | [LOG] | `pilot/v2/GATE4_GATE5_STATUS.md` §"Gate 5 execution" |
| Total planned calls (600) and current completion (0 of 600 validly completed) | [LOG] | `pilot/v2/PILOT_PROTOCOL_V2.md` §6; `EXPERIMENT_LOG.md` (both Session G attempts VOID; Session P never started) |

## Measures

| Claim | Category | Source |
|---|---|---|
| Top-K definition and conservative worst-rank tie convention | [SPEC]/[LIT] | `pilot/v2/STATISTICAL_ANALYSIS_PLAN.md` §1; tie-convention rationale attributed to Yang et al. (2025), `dossier/05_block5_methodology.md` §5.1 |
| Multi-line "best rank" convention inactive for this pilot | [SPEC] | `pilot/v2/GROUND_TRUTH_PROTOCOL.md` §3 (single-line filter); `pilot/PRE_RUN_REVIEW.md` F3 item 3 (describes the underlying code convention) |
| EXAM formula and censoring convention | [SPEC] | `pilot/v2/STATISTICAL_ANALYSIS_PLAN.md` §1 (`e_X(i,r)`, "failures score 1.0") |
| EXAM* denominator = physical LOC, not comparable to published EXAM | [SPEC] | `pilot/v2/STATISTICAL_ANALYSIS_PLAN.md` §5; `pilot/v2/SAMPLING_PROTOCOL.md` §5 |

## Statistical Analysis Plan

| Claim | Category | Source |
|---|---|---|
| Experimental unit = one program, pooling 150 prohibited | [SPEC] | `pilot/v2/STATISTICAL_ANALYSIS_PLAN.md` §2 |
| Majority-of-5 aggregation rule | [SPEC] | `pilot/v2/STATISTICAL_ANALYSIS_PLAN.md` §3 |
| Primary test definition (exact McNemar, b/c/d) | [SPEC] | `pilot/v2/STATISTICAL_ANALYSIS_PLAN.md` §6.1 |
| Cross-session invariants required before computing the primary comparison | [SPEC] | `pilot/v2/PILOT_PROTOCOL_V2.md` §3.1; `pilot/v2/STATISTICAL_ANALYSIS_PLAN.md` §6.1 |
| Null-calibration gate rule (`d_null ≥ d_primary` ⇒ uninterpretable) | [SPEC] | `pilot/v2/PILOT_PROTOCOL_V2.md` §3.3; `pilot/v2/STATISTICAL_ANALYSIS_PLAN.md` §6.2 |
| Secondary analyses (A vs B/C, bootstrap, Wilcoxon, per-class descriptive) | [SPEC] | `pilot/v2/STATISTICAL_ANALYSIS_PLAN.md` §6.3 |
| Robustness check (5 per-repetition McNemar tests reported together) | [SPEC] | `pilot/v2/STATISTICAL_ANALYSIS_PLAN.md` §6.4 |
| Multiplicity policy (1 primary endpoint, no formal correction) | [SPEC] | `pilot/v2/STATISTICAL_ANALYSIS_PLAN.md` §6.5 |
| Power table (min *p* by discordant count *d*) | [SPEC] | `pilot/v2/STATISTICAL_ANALYSIS_PLAN.md` §7 (reproduced verbatim) |
| Confirmatory sizing formula and worked example | [SPEC] | `pilot/v2/STATISTICAL_ANALYSIS_PLAN.md` §7 |

## Reproducibility

| Claim | Category | Source |
|---|---|---|
| Linear, unsquashed git history claim | [LOG] | `git log --oneline` output inspected directly during this review; `PROJECT_STATE.md` "Branch Map" section |
| Manifest checksum, pattern-prior/placebo checksums | [DATA]/[SPEC] | `data/manifests/pilot_manifest_v2_1.json`; `pilot/v2/MODEL_FREEZE_RECORD_16384.json` `asset_hashes` |
| Sampling seed 20260910, bootstrap seed 20260908 | [SPEC] | `pilot/v2/SAMPLING_PROTOCOL.md` §7; `pilot/v2/STATISTICAL_ANALYSIS_PLAN.md` §6.3 |
| Exclusive-create raw-response storage | [SPEC]/[LOG] | `DECISIONS.md` row 2 (2026-09-08 decision, attributed to Codex) |
| "Loud-failure principle" | [SPEC] | `pilot/v2/MODEL_FREEZE_PROTOCOL.md` §4.3 |

## Results

| Claim | Category | Source |
|---|---|---|
| All performance values | [PLACEHOLDER] | Explicit `[RESULT PENDING]` in every table cell |
| Run-integrity paragraph (Session G attempted twice, VOID both times; Session P never started) | [LOG] | `pilot/v2/CLEAN_SCIENTIFIC_RERUN_STATUS.md`; `EXPERIMENT_LOG.md` |
| Abort-rule thresholds (5% first-50, 80% overall) | [SPEC] | `pilot/v2/MODEL_FREEZE_PROTOCOL.md` §4.2 |

## Discussion

| Claim | Category | Source |
|---|---|---|
| Maximal permitted claim under a positive result | [SPEC] | `pilot/v2/CLAIM_BOUNDARIES_V2.md` §1, quoted near-verbatim |
| "most likely outcome" framing for a null result | [SPEC] | `pilot/v2/PRE_RUN_REVIEW_V2.md` finding V-5 |
| Delimiter-tag asymmetry as a pro-hypothesis bias, relevant to a negative-result scenario | [SPEC] | `pilot/v2/PRE_RUN_REVIEW_V2.md` finding V-2 |
| Manual spot-check requirement | [SPEC] | `pilot/v2/PILOT_PROTOCOL_V2.md` §5 item 6 |
| DP/base-case example tied to Baron & Feitelson (2024) | [LIT] | `dossier/01_block1_theory.md` item B16 |

## Threats to Validity and Limitations

Every bullet in this section maps directly to a claim already sourced above
(sample size/power → Statistical Analysis Plan sources; per-pattern *n* →
Method sources; single language and ConDefects representativeness → [DATA]
sources; oracle-label discrepancy → [FLAG] above; single-annotator/κ →
`pilot/ANNOTATION_GUIDE.md` §4; single-line-fault bias direction →
`pilot/v2/GROUND_TRUTH_PROTOCOL.md` §3 "Cost, disclosed"; `problem_context`
omission → `pilot/v2/SAMPLING_PROTOCOL.md` §5; model-specificity →
Method/[LOG] sources above; no classical baseline in this pilot → explicit
scope statement, `pilot/v2/PILOT_PROTOCOL_V2.md` §5 purpose list (baselines
are absent from the pilot's stated purposes); no human-subject validation →
`pilot/v2/CLAIM_BOUNDARIES_V2.md` §3 prohibition list; contamination unprobed
→ `dossier/01_block1_theory.md` §1d N11 (v1 pre-run-review finding, carried
forward unresolved per `pilot/v2/PRE_RUN_REVIEW_V2.md` V-10); pattern-taxonomy
limitations → `pilot/PATTERN_VOCABULARY.md` "Inclusion rule" and the
BFS/DFS-merge rationale in the same document.

The **third-party testcase archive provenance** claim is sourced specifically
from `data/TESTCASE_PROVENANCE_AUDIT.md` (verdict: "reproducible third-party
archive/mirror," not "official"), which itself explicitly supersedes and
corrects overstated "official mirror" language found elsewhere in
`data/CONDEFECTS_SOURCE.md` and `data/manifests/SAMPLING_AUDIT_V2_1.md` — this
paper follows the corrected, more conservative characterization rather than
the superseded one, and that choice is itself recorded here as a deliberate
editorial decision, not an oversight.

## Future Work

All items are prescriptive (recommendations for subsequent studies), sourced
from `pilot/v2/CLAIM_BOUNDARIES_V2.md` §6 ("Escalation" — the confirmatory
path) and `dossier/99_synthesis.md` §S3–S4 (original architecture synthesis,
for the SBFL/MBFL-baseline and multi-model recommendations); no [LIT] or
[DATA] factual claims are made in this section beyond what is already sourced
in Method.

## References — Reference Verification Flags

The following 10 of 34 reference entries carry an explicit incompleteness or
uncertainty flag inline in `APA7_PAPER_DRAFT.md` and are listed here for
convenience, each with the reason:

1. **Araujo et al. (2016)** — full author list and exact title/venue not
   independently fetched in the project's literature review (marked
   [V-cited] in `dossier/03_block3_fault_localization.md`, meaning verified
   only via a citation inside another fetched source).
2. **du Boulay, O'Shea & Monk (1981)** — DOI not independently verified in
   the project's literature review (`dossier/01_block1_theory.md` records
   only "ScienceDirect / Sussex author page" as the verification source, no
   DOI string).
3. **Johnson (1990)** — DOI not recorded anywhere in the project's
   literature review.
4. **Jones, Harrold & Stasko (2002)** — venue recorded inconsistently: the
   dossier's Block 3 lists "ISSTA 2002," which this reviewer's background
   knowledge suggests may actually be ICSE 2002; not resolved by silent
   correction, flagged for direct verification instead.
5. **Gupta et al. (2019)** — full author list not recorded in the project's
   literature review beyond "Gupta et al."
6. **Hoq et al. (2025)** — full author list not recorded beyond "M. Hoq et
   al."
7. **Li et al. (2023), VsusFL** — full author list not recorded beyond a
   partial surname list ("Li, Wu, Liu, Shen, Wu, Zhang, Chen") with no given
   names/initials.
8. **Wong, Debroy, Gao & Li (2013), DStar** — the project's literature
   review records this as "IEEE TSE 39(4), 2013, DOI 10.1109/TSE.2012.53" in
   one place; this reviewer's background knowledge associates the DStar
   paper with *IEEE Transactions on Reliability*, not *TSE* — the two
   records disagree and neither was independently re-fetched in this pass,
   so both journal name and DOI are flagged rather than either being
   asserted with confidence.
9. **Wong et al. (2016) survey** — see the [FLAG] entry under Related Work
   above; the dossier's author-list transcription appears corrupted.
10. **Xu et al. (2025)** and **Yang, Mei & Yang (2025)** — given
    names/initials for the authors are not recorded anywhere in the
    project's literature review; only surnames and, for Xu et al., partial
    author-surname lists with institutional affiliations, are available.

None of these 10 entries were "completed" with values invented by the
drafting process. Each is presented with exactly the information the
repository's own verified literature review contains, and no more.

## Summary of [FLAG] Items (Cross-Reference)

1. `pattern_source: "AST rule"` vs. mandated blinded human-annotation
   provenance — **highest priority**, blocks any Results section.
2. Corpus-size conflation in `dossier/04_block4_datasets.md` §4.3 (1,625 vs.
   2,864 programs) — does not block this paper (the correct, pipeline-used
   figure was identified and used), but should be corrected in the dossier
   itself.
3. Roster-table vs. manifest discrepancies for `faulty_line`/`difficulty` —
   resolved by using the manifest, per the project's own Gate 7 audit; not a
   blocker for this paper, disclosed for completeness.
4. Wong et al. (2016) survey author-list transcription — reference-accuracy
   blocker, does not affect any scientific claim in the paper body.
5. Ten reference entries with incomplete bibliographic data — reference-
   accuracy blockers, listed exhaustively above.
