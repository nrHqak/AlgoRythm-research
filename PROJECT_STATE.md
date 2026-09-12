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

**Pre-results, v2.2 consensus sample frozen, technical configuration frozen, ready for the FINAL scientific pilot.** Protocol, dataset (v2.2), priors, prompts, and model configuration (including the `reasoning_effort = low` amendment) are frozen. **No valid scientific performance result exists anywhere in this repository's history.** Every execution attempt to date — under `max_tokens` 4096, 16384, and 32768 (the last with the model's default reasoning effort) — has been declared VOID by the frozen health rule. The `reasoning_effort = low` amendment that is expected to fix the reasoning-token-exhaustion cause of every VOID attempt has passed only a 20-call synthetic preflight; it has **not yet been exercised by a real scientific session**. The next required action is to run the full 600-call two-session pilot under this exact frozen configuration.

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

No scientific experiment is running.

# Blocked

Nothing currently blocks starting the final scientific pilot. The two historical blockers are both resolved:

- Pattern-label provenance (v2.1's unreviewed heuristic) — resolved by the v2.2 model-consensus-annotation remediation above.
- `max_tokens` insufficiency at 16384 — resolved by raising to 32768; the follow-on VOID at 32768 with default reasoning effort is addressed by the frozen `reasoning_effort = low` amendment, which is technically validated (synthetic preflight) but **not yet exercised by a real scientific run** — this is the one remaining unknown before a valid result can exist, not a blocker to attempting the run.

# Next Actions

1. **Run the FINAL scientific pilot** under the exact frozen configuration in `pilot/v2/MODEL_FREEZE_RECORD.json`: manifest `data/manifests/pilot_manifest_v2_2.json`, model `z-ai/glm-5.3-flash` via OpenRouter/Z.AI pinned, `temperature = 0`, `max_tokens = 32768`, `reasoning_effort = "low"`, `repetitions = 5`, 4 concurrent workers within a session, Session G then Session P with a hard barrier between them.
2. Analyze each session natively, then run the cross-session C-vs-B primary comparison (`pilot/v2/STATISTICAL_ANALYSIS_PLAN.md` §6).
3. Apply the null-calibration gate (A_G vs A_P) **before** interpreting the primary result.
4. Update `pilot/v2/CLAIM_BOUNDARIES_V2.md` to describe v2.2 labels accurately (consensus of two blinded model annotators, not oracle/human) before writing any Results text.
5. Apply the (updated) `pilot/v2/CLAIM_BOUNDARIES_V2.md` to every sentence written about the outcome.
6. Insert the result into `paper/APA7_PAPER_RU.md` per `paper/RESULT_INSERTION_MAP_RU.md`.

# Latest Experimental Results

**None.** No valid scientific performance result exists. All pilot attempts to date (4096-token, 16384-token, and 32768-token-with-default-reasoning-effort configurations) are VOID and are retained only as audit history. The `reasoning_effort = low` configuration expected to produce a valid run has passed only a synthetic, non-scientific preflight (20/20 calls, 0 failures) — **this preflight is an engineering/technical validation, not a scientific result, and must never be reported as one.**

**No Results or Discussion claim may be written yet.** Writing any performance number, effect direction, or comparative statement at this stage would violate `pilot/v2/CLAIM_BOUNDARIES_V2.md`.

# Known Risks

- `dossier/99_synthesis.md` §S5 (project-level), `pilot/SCIENTIFIC_RISKS.md` (pilot-level).
- **Two model annotators, not human experts.** v2.2 pattern labels are the exact consensus of two independent blinded LLMs (Claude, Codex), not human-assigned oracle labels. Agreement (κ ≈ 0.75) is "substantial" by the conventional scale, not perfect; the two models may share correlated training-data biases in a way two independent human experts would not.
- **Consensus-only selection bias.** The v2.2 sample is drawn only from the 78.4483% of the frame where both annotators agreed; the 50 disagreements (21.6% of the frame) were excluded, not adjudicated. This biases the pilot toward programs with comparatively unambiguous pattern assignments.
- **`reasoning_effort = low` is technically validated but scientifically unexercised.** Every real scientific attempt to date has failed on reasoning-token exhaustion; the amendment addressing this has only 20 synthetic calls of evidence behind it. The next real run is the first test of whether it actually resolves the VOID pattern at scientific scale (300+ calls).
- Open items from `pilot/v2/PRE_RUN_REVIEW_V2.md`: **V-1** single-annotator residual in the blinded fault-location pass; **V-2** the `<ALGORITHMIC_PATTERN_PRIOR>` delimiter tag wraps generic text in arm B — the only asymmetry in the design that biases *toward* the hypothesis; **V-5** a statistically null primary result is the expected outcome at n = 30 and must not be read as evidence of absence.
- **`pilot/v2/CLAIM_BOUNDARIES_V2.md` is stale** relative to the v2.2 model-consensus-annotation amendment (still describes "oracle human-assigned" labels). Must be corrected before any Results are written — see Frozen Decisions and Next Actions.
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
| `main` | authoritative, contains all work | `2533da0` (merge commit) |
| `agent/codex-gate7` | v2.2 remediation: consensus sample, model/token/concurrency/reasoning-effort freezes, final VOID diagnostics | `f8c00ff` — merged into `main` |
| `agent/claude-v2-2-annotation` | Claude's (Annotator A) independent blinded v2.2 annotation | `a1d1b16` — content (the annotation CSV) is byte-identical to what `agent/codex-gate7` already carries via its own commit `019d75f`; **not** a git ancestor of `codex-gate7`, and not separately merged. One file unique to this branch, `data/CLAUDE_ANNOTATION_V2_2_AUDIT.md` (Claude's own annotation-run audit note), is **not yet on `main`** — it duplicates no scientific data, only documentation, and can be added later without touching any frozen artifact. |
| `agent/antigravity-data-v2` | dataset v2.1 | `9c83767` |
| `agent/codex-v2-preflight` | v2 engineering gates | `96de08d` |
| `agent/claude-science` | scientific specification v1 + v2 | `579c687` |
| `agent/codex-experiment` | original pilot infrastructure | `c5265d0` |
