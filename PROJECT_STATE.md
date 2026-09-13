# Current Research Question

Does supplying a classified algorithmic pattern as a structural prior improve automatic logical-fault localization in novice code, compared with pattern-agnostic localization? See `AGENTS.md` and `dossier/99_synthesis.md`.

The pilot's **primary causal comparison is pattern-specific prior vs. matched generic prior** (arm C vs arm B), not prior vs. no prior — see `pilot/v2/PILOT_PROTOCOL_V2.md` §2.

# Frozen Decisions

All of the following are frozen and must not be altered before the pilot runs:

- **Scientific protocol v2** — `pilot/v2/PILOT_PROTOCOL_V2.md` (three arms `no_prior` / `generic_prior` / `pattern_prior`, two paired sessions, primary comparison C vs B).
- **Pattern vocabulary** — `pilot/PATTERN_VOCABULARY.md`, 12 classes (v1, carried into v2 unchanged).
- **Pattern priors** — `pilot/pattern_priors.json` (v1, byte-identical, deliberately not re-tuned).
- **Generic/placebo prior** — `pilot/v2/generic_placebo_prior.json` (word-count deviation vs. pattern priors: max 8, mean 4.2; checkpoint counts matched per label).
- **Prompts** — `pilot/prompts/control.txt` (v1, unchanged) + `pilot/v2/prompts/system_v2.txt`.
- **Statistical analysis plan** — `pilot/v2/STATISTICAL_ANALYSIS_PLAN.md` (program-level unit, majority-of-5 aggregation, exact McNemar primary, `count_as_failure` parser policy, `counterbalanced` condition order).
- **Dataset v2.2 (current, supersedes v2.1 for execution)** — consensus-only sample frozen at `selection_frozen_at 2026-09-12T18:18:44Z`; **n = 30**, 30 unique programs, 30 unique `task_id`s; manifest SHA-256 `9f2db14bd38647e611bed87c72c87f7c934a2c824388751e2969ad4cab9ef8fc` (`data/manifests/pilot_manifest_v2_2.json`). Classes and allocation: `dynamic_programming` (8), `brute_force_implementation` (8), `binary_search` (7), `graph_traversal_dfs_bfs` (7). Every record carries `pattern_source: "model-consensus"`. **v2.1's manifest (`pilot_manifest_v2_1.json`) is preserved unmodified as permanent audit history and is no longer the execution target** — see "Completed" and `data/PATTERN_LABEL_PROVENANCE_AUDIT.md` for why it was superseded.
- **Pattern-label provenance for v2.2** — exact-consensus labels from two independent blinded **model** annotators (Claude = Annotator A, Codex = Annotator B), not human or oracle labels. Agreement over the shared 232-program frame: 182/232 exact matches, raw agreement 78.4483%, Cohen's κ ≈ 0.752269 (`data/manifests/PATTERN_ANNOTATION_AGREEMENT_V2_2.md`). The 50 disagreements were excluded from the pilot without adjudication (`excluded from pilot: independent pattern annotators disagreed`), per the user-authorized pilot-only consensus filter (`pilot/v2/PRE_RESULTS_AMENDMENT_MODEL_ASSISTED_PATTERN_ANNOTATION_V2_2.md`).
- **Model freeze (current)** — `z-ai/glm-5.3-flash` via OpenRouter (`https://openrouter.ai/api/v1`), underlying provider pinned to **Z.AI** (`z-ai/fp8`, fallbacks disabled, `require_parameters` enabled), `temperature = 0`, **`max_tokens = 32768`** (raised from 16384 after a demonstrated VOID; validated by a 50/50 synthetic stress pass), **`reasoning_effort = "low"`** (lowered from the model's default `max`; validated only by a 20/20 synthetic preflight, see `pilot/v2/PRE_RESULTS_AMENDMENT_REASONING_EFFORT_LOW.md` — **not yet validated by any real scientific session**), `repetitions = 5`, bounded concurrency of **4 workers** within a session with a hard G-before-P barrier (`pilot/v2/PRE_RESULTS_AMENDMENT_CONCURRENCY_4.md`). Active record: `pilot/v2/MODEL_FREEZE_RECORD.json`.
- **Claim boundaries** — `pilot/v2/CLAIM_BOUNDARIES_V2.md`. **Known open item:** this document's text still describes pilot labels as "oracle (human-assigned)" (§1, §4.1), which is stale relative to the v2.2 model-consensus-annotation amendment above. It must be updated to describe v2.2 labels as consensus labels from two independent blinded model annotators before any Results are written. Not yet applied.

# Current Stage

**Post-results. The final scientific pilot is COMPLETE and VALID, and the Russian APA 7 paper is finalized against it.** The frozen v2.2 protocol was executed end-to-end under `max_tokens = 32768`, `reasoning_effort = low`, 4 workers, Session G then Session P: **600/600 registered calls completed**, zero provider failures, one parser failure (arm B, handled under the preregistered `count_as_failure` policy), all cross-session invariants `PASS`, no VOID marker on either session. The `reasoning_effort = low` amendment resolved the reasoning-token exhaustion that had voided every prior attempt — zero length truncations across all 600 calls.

**The preregistered primary hypothesis was NOT supported.** Program-level Top-1, C vs B: 12/30 (40.00%) vs 12/30 (40.00%), delta 0.00 pp, exact McNemar *p* = 1.0, *b* = 3, *c* = 3, *d* = 6, bootstrap 95% CI [−16.67, +16.67] pp. The null-control gate passed (*d*_null = 5 < *d*_primary = 6), with a minimal margin. This is a **null/mixed calibration result, not evidence of equivalence and not evidence of absence.**

# Completed

- Research dossier (`RESEARCH_DOSSIER.md`, `dossier/`).
- Pilot engineering infrastructure, safety gates, analysis pipeline, figures (Codex).
- Scientific specification v1, frozen (`pilot/`), then adversarially reviewed → **BLOCK** (`pilot/PRE_RUN_REVIEW.md`): the two-arm design could not attribute any effect to pattern specificity.
- Scientific specification v2, frozen (`pilot/v2/`), adding the matched placebo arm and resolving F1–F5; re-reviewed → **RUN PILOT** subject to setup gates (`pilot/v2/PRE_RUN_REVIEW_V2.md`). v1 preserved byte-identically; see `pilot/v2/CHANGELOG_V1_TO_V2.md`.
- Dataset: ConDefects provenance, mechanical inventory, blinded fault-location ground truth frozen **before** pattern labeling, sampling audits, and the corrected v2.1 sample (Antigravity).
- **Pattern-label provenance investigation** (`data/PATTERN_LABEL_PROVENANCE_AUDIT.md`): found that v2.0/v2.1 `pattern_label` values were produced entirely by an unreviewed regex/keyword heuristic (`classify_program()`) falsely recorded as `pattern_source: "AST rule"`, never by a human annotator as the frozen protocol required, with a demonstrated real misclassification rate (2 of 3 spot-checked `binary_search` programs). This finding is retained as permanent audit history, not hidden.
- **v2.2 remediation, completed and frozen:**
  - Independent blinded pattern annotation of the same 232-program frame by two model annotators — Claude (Annotator A, `data/manifests/pattern_annotations_claude_v2_2.csv`) and Codex (Annotator B, `data/manifests/pattern_annotations_codex_v2_2.csv`).
  - Agreement analysis: 182/232 exact agreement (78.4483% raw agreement, Cohen's κ ≈ 0.752269) — `data/manifests/PATTERN_ANNOTATION_AGREEMENT_V2_2.md`.
  - Consensus-only pilot sample frozen (n = 30; classes `dynamic_programming`/`brute_force_implementation`/`binary_search`/`graph_traversal_dfs_bfs` at 8/8/7/7) — `data/manifests/pilot_manifest_v2_2.json`, `data/manifests/SAMPLING_AUDIT_V2_2.md`. Sampling seed `20260910` reused unchanged (no reroll).
  - Technical amendments, each validated by a synthetic preflight before being frozen: `max_tokens` 16384 → 32768 (50/50 pass), bounded concurrency of 4 workers (20/20 pass), `reasoning_effort` default (`max`) → `low` (20/20 pass, 0 parser failures / 0 content-null / 0 length truncations).
  - **Final v2.2 scientific pilot attempt** under `max_tokens = 32768` with the model's *default* reasoning effort: VOID after the first concurrent batch of 4 calls (1 success, 3 provider failures from reasoning-token exhaustion) — `results/scientific-v2_2-32768-w4/final_pilot_void.json`, `pilot/v2/FINAL_SCIENTIFIC_PILOT_V2_2_STATUS.md`. This is the failure that motivated the `reasoning_effort = low` amendment above.
- **Test-case provenance audit completed** — `data/TESTCASE_PROVENANCE_AUDIT.md`, `data/manifests/GATE7_TESTCASE_PROVENANCE.json`.
- Gate 7 readiness, freeze-integrity and roster-discrepancy audits (`pilot/v2/GATE7_READINESS.md`, `data/manifests/GATE7_*.json`).
- Engineering gates: smoke fixtures, OpenRouter routing pin with drift guards, cross-session comparison script (`analysis/compare_v2_sessions.py`), stress-smoke harness.
- **Pre-results APA 7 paper draft (English, historical)** — `paper/APA7_PAPER_DRAFT.md`, with `paper/RESULT_INSERTION_MAP.md`, `paper/APA7_COMPLIANCE_CHECKLIST.md`, `paper/PAPER_SOURCE_AUDIT.md`. Written against the v2.1 state and preserved unmodified as historical/source material; it predates the v2.2 remediation and should not be read as reflecting current dataset facts.
- **Russian APA 7 paper draft (current)** — `paper/APA7_PAPER_RU.md`, with `paper/APA7_PAPER_RU_STATUS.md` and `paper/RESULT_INSERTION_MAP_RU.md`. Written against the current v2.2 state (consensus-only sample, model-consensus labels, current technical freeze). No result, effect direction, or comparative claim is asserted anywhere in it; every Results table cell is an explicit `[РЕЗУЛЬТАТ ОЖИДАЕТСЯ]` placeholder.
- Full regression test suite passing (80/80, `.venv/bin/python -m pytest`) after merging the v2.2 branch into `main`.

# In Progress

No scientific experiment is running. The final pilot is complete and its results are written up in `paper/APA7_PAPER_RU.md`.

# Blocked

Nothing is blocked. Both historical blockers were resolved and the final pilot has run:

- Pattern-label provenance (v2.1's unreviewed heuristic) — resolved by the v2.2 model-consensus-annotation remediation.
- Reasoning-token exhaustion — resolved by the `reasoning_effort = low` amendment, now confirmed at scientific scale (zero length truncations across 600 calls).

# Next Actions

1. Update `pilot/v2/CLAIM_BOUNDARIES_V2.md` to describe v2.2 labels accurately (consensus of two blinded model annotators, not oracle/human). This is the one remaining internal-consistency item; the Russian paper already follows the correct characterization and discloses the discrepancy.
2. Verify the 10 flagged, incompletely-sourced reference entries against primary bibliographic sources (`paper/APA7_PAPER_RU_STATUS.md` §6).
3. Student action: supply author name/spelling, affiliation, graduation year, and correspondence address on the title page (competition AI-authorship rule).
4. Optional: add `data/CLAUDE_ANNOTATION_V2_2_AUDIT.md` (Annotator A's run audit, the only file unique to `agent/claude-v2-2-annotation`) to `main`.
5. Optional follow-on science, per the paper's Future Work: adjudicate the 50 excluded disagreement programs; run a confirmatory study sized from an externally-specified minimum meaningful difference (this pilot could not size it); test the two hypotheses this pilot generated (ranking-quality effect; pattern-dependent effect).

# Latest Experimental Results

**The final v2.2 scientific pilot is COMPLETE and VALID** (`results/final-pilot-v2-2-low/`). Run integrity: 600/600 calls, 0 provider failures, 1 parser failure (arm B, `count_as_failure`), invariants `PASS`, no VOID marker.

- **Primary (preregistered), Top-1, C vs B, program level:** 12/30 (40.00%) vs 12/30 (40.00%); delta 0.00 pp; exact McNemar *p* = 1.0; *b* = 3, *c* = 3, *d* = 6; bootstrap 95% CI [−16.67, +16.67] pp. **H1 not supported.**
- **Null-control gate:** A_G 13/30 (43.33%) vs A_P 12/30 (40.00%); drift −3.33 pp; *d*_null = 5; *p* = 1.0; gate **PASS** (5 < 6), minimal margin.
- **Secondary/descriptive (no alpha adjustment, none significant):** Top-3 50.00% vs 60.00% (*p* = .453); Top-5 53.33% vs 63.33% (*p* = .375); EXAM\* 0.510798 vs 0.445055 (Wilcoxon *p* = .124). All CIs include zero.
- **Per-pattern Top-1 (descriptive only):** brute force +25.00 pp, dynamic programming −25.00 pp, binary search 0.00 pp, graph traversal 0.00 pp — the two non-zero shifts cancel in the pooled result.
- **Determinism finding:** 0.00% of (program, condition) cells produced five byte-identical responses in any arm; Top-1 agreement across five repetitions was only 56.67–73.33%. Temperature 0 did not yield reproducible output.
- **Confirmatory sizing:** NOT POSSIBLE from this pilot. π_d = 0.200 [0.067, 0.367] but ψ = 0.500 exactly, so the McNemar approximation is undefined; registered status "PILOT COULD NOT SIZE THE STUDY".
- **Operational:** US$0.29696674; 3,385.523 s (56 min 25.5 s); 1,227,795 total tokens.

**Interpretation discipline:** the result is a null/mixed calibration outcome. It is **not** evidence of equivalence and **not** evidence of absence of an effect; the CI is compatible with a substantial effect in either direction. The secondary ranking-quality signal and the pattern-dependent heterogeneity are hypothesis-generating only.

# Known Risks

- `dossier/99_synthesis.md` §S5 (project-level), `pilot/SCIENTIFIC_RISKS.md` (pilot-level).
- **Two model annotators, not human experts.** v2.2 pattern labels are the exact consensus of two independent blinded LLMs (Claude, Codex), not human-assigned oracle labels. Agreement (κ ≈ 0.75) is "substantial" by the conventional scale, not perfect; the two models may share correlated training-data biases in a way two independent human experts would not.
- **Consensus-only selection bias.** The v2.2 sample is drawn only from the 78.4483% of the frame where both annotators agreed; the 50 disagreements (21.6% of the frame) were excluded, not adjudicated. This biases the pilot toward programs with comparatively unambiguous pattern assignments.
- **No determinism at temperature 0 (measured).** Zero percent of (program, condition) cells produced five byte-identical responses; Top-1 agreement across repetitions was 56.67–73.33%. Single-shot evaluation of this model is not reproducible, and any future protocol must keep repetitions plus an explicit aggregation rule.
- **The empirical noise floor nearly equals the primary signal.** *d*_null = 5 vs *d*_primary = 6. The interpretability gate passed, but barely; at n = 30 a Top-1 difference is hard to separate from re-run variability.
- **The pilot could not size the confirmatory study.** ψ = 0.500 exactly makes the McNemar sizing approximation undefined. Future planning must start from an externally-specified minimum meaningful difference.
- **`reasoning_effort = low` is a forced configuration constraint.** It was required to get any completion at all; the model's behavior under higher reasoning effort is untested here, so the null result is conditional on this setting.
- Open items from `pilot/v2/PRE_RUN_REVIEW_V2.md`: **V-1** single-annotator residual in the blinded fault-location pass; **V-2** the `<ALGORITHMIC_PATTERN_PRIOR>` delimiter tag wraps generic text in arm B — the only asymmetry in the design that biases *toward* the hypothesis; **V-5** a statistically null primary result is the expected outcome at n = 30 and must not be read as evidence of absence.
- **`pilot/v2/CLAIM_BOUNDARIES_V2.md` is stale** relative to the v2.2 model-consensus-annotation amendment (still describes "oracle human-assigned" labels). The Russian paper already uses the correct characterization and discloses the discrepancy, but the document itself still needs correcting — see Next Actions.
- ⚠️ **ISEF rule:** generative AI may not be used to author the research plan, the ≤250-word abstract, the poster, or the citations (`AGENTS.md` §3.2 item 7, `dossier/08_block8_competition.md`). AI-assisted engineering and specification work is permissible but must be disclosed accurately.

# Agent Handoffs

- **Claude (science):** delivered. v1 `81fd51d`, v2 `579c687`; reviews in `pilot/PRE_RUN_REVIEW.md` and `pilot/v2/PRE_RUN_REVIEW_V2.md`.
- **Antigravity (data):** delivered. Corrected v2.1 sample frozen at `9c83767`; audits under `data/manifests/`. Superseded for execution by the v2.2 consensus sample above; v2.1 manifest preserved as audit history.
- **Claude (v2.2 annotation, Annotator A):** delivered independent blinded pattern annotation of the 232-program frame (`agent/claude-v2-2-annotation`, `a1d1b16`); content merged into `main` via `agent/codex-gate7`.
- **Codex (engineering + v2.2 annotation, Annotator B):** delivered through the v2.2 consensus-sample freeze, the `max_tokens`/concurrency/`reasoning_effort` amendments, and the final VOID pilot attempt diagnosis (`agent/codex-gate7`, `f8c00ff`). No valid scientific result handoff exists, because no valid result exists.
- **Claude (Russian paper):** delivered `paper/APA7_PAPER_RU.md` and its companions, built from the v2.2 state.

# Branch Map

`main` is now the authoritative branch and contains everything below (merged from `agent/codex-gate7` via an explicit merge commit, preserving both the Russian-paper commit on `main` and the full scientific/audit history from `codex-gate7`; no squash, no rewrite):

| Branch | Role | Tip |
|---|---|---|
| `main` | authoritative, contains all work including the final valid results | this commit |
| `agent/codex-gate7` | v2.2 remediation, execution freezes, VOID diagnostics, and the final VALID pilot results | `bc34ccd` — merged into `main` |
| `agent/claude-v2-2-annotation` | Claude's (Annotator A) independent blinded v2.2 annotation | `a1d1b16` — content (the annotation CSV) is byte-identical to what `agent/codex-gate7` already carries via its own commit `019d75f`; **not** a git ancestor of `codex-gate7`, and not separately merged. One file unique to this branch, `data/CLAUDE_ANNOTATION_V2_2_AUDIT.md` (Claude's own annotation-run audit note), is **not yet on `main`** — it duplicates no scientific data, only documentation, and can be added later without touching any frozen artifact. |
| `agent/antigravity-data-v2` | dataset v2.1 | `9c83767` |
| `agent/codex-v2-preflight` | v2 engineering gates | `96de08d` |
| `agent/claude-science` | scientific specification v1 + v2 | `579c687` |
| `agent/codex-experiment` | original pilot infrastructure | `c5265d0` |
