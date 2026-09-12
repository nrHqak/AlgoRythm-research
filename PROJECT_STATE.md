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
- **Dataset v2.1** — corrected sample frozen at `selection_frozen_at 2026-09-10T17:51:43Z`; **n = 30**, 30 unique programs, 30 unique `task_id`s; manifest SHA-256 `d53bcdc232f7…`; mechanical sanity `PASS` (`data/manifests/GATE7_DATASET_SANITY.json`).
- **Model freeze** — `z-ai/glm-5.3-flash` via OpenRouter (`https://openrouter.ai/api/v1`), underlying provider pinned to **Z.AI**, `temperature = 0`, `max_tokens = 16384` (`pilot/v2/MODEL_FREEZE_RECORD_16384.json`).
- **Claim boundaries** — `pilot/v2/CLAIM_BOUNDARIES_V2.md`.

# Current Stage

**Pre-results.** Protocol, dataset, priors, prompts, and model are frozen; the pilot has been attempted and every attempt is VOID. **No valid scientific performance result exists.**

# Completed

- Research dossier (`RESEARCH_DOSSIER.md`, `dossier/`).
- Pilot engineering infrastructure, safety gates, analysis pipeline, figures (Codex).
- Scientific specification v1, frozen (`pilot/`), then adversarially reviewed → **BLOCK** (`pilot/PRE_RUN_REVIEW.md`): the two-arm design could not attribute any effect to pattern specificity.
- Scientific specification v2, frozen (`pilot/v2/`), adding the matched placebo arm and resolving F1–F5; re-reviewed → **RUN PILOT** subject to setup gates (`pilot/v2/PRE_RUN_REVIEW_V2.md`). v1 preserved byte-identically; see `pilot/v2/CHANGELOG_V1_TO_V2.md`.
- Dataset: ConDefects provenance, mechanical inventory, blinded fault-location ground truth frozen **before** pattern labeling, sampling audits, and the corrected v2.1 sample (Antigravity).
- **Test-case provenance audit completed** — `data/TESTCASE_PROVENANCE_AUDIT.md`, `data/manifests/GATE7_TESTCASE_PROVENANCE.json`.
- Gate 7 readiness, freeze-integrity and roster-discrepancy audits (`pilot/v2/GATE7_READINESS.md`, `data/manifests/GATE7_*.json`).
- Engineering gates: smoke fixtures, OpenRouter routing pin with drift guards, cross-session comparison script (`analysis/compare_v2_sessions.py`), stress-smoke harness.
- Model freeze after several recorded aborts (Gemini credential/HTTP 503 attempts, OpenRouter truncation aborts) — all preserved as audit history under `pilot/v2/model-freeze-attempts/`.
- Pre-results amendments to `max_tokens` (4096 → 16384), recorded before any result existed.
- Fresh 16384-token stress smoke passed (`pilot/v2/STRESS_SMOKE_16384_STATUS.md`).
- **Pre-results APA 7 paper draft** written from the frozen protocol, dataset audits, and literature dossier only — `paper/APA7_PAPER_DRAFT.md`, with `paper/RESULT_INSERTION_MAP.md`, `paper/APA7_COMPLIANCE_CHECKLIST.md`, and `paper/PAPER_SOURCE_AUDIT.md`. No result, effect direction, or comparative claim is asserted anywhere in it; every Results table cell is an explicit `[RESULT PENDING]` placeholder. The source audit surfaces one open data-integrity item that blocks any future Results section independent of experiment completion: the frozen manifest records `pattern_source: "AST rule"` for all 30 programs, which is inconsistent with the blinded human-annotation provenance `pilot/ANNOTATION_GUIDE.md` §2 and `pilot/v2/CLAIM_BOUNDARIES_V2.md` §4.1 require — see `paper/PAPER_SOURCE_AUDIT.md` and `paper/RESULT_INSERTION_MAP.md` §11.

# In Progress

No scientific experiment is running.

# Blocked

- **The latest clean scientific rerun is VOID.** Session `20260912T105822Z-G-clean` (Session G) stopped after call 18. Calls 1–17 completed; call 18 returned HTTP 200 with exact model/provider identity but `content=null`, `finish_reason=length`, 16,384 output tokens of which 16,383 were reasoning tokens. The first-50 provider-failure rate was 1/18 = 5.56%, which tripped the frozen >5% health rule and invalidated the session. Session P and all analyses were not run. Cause is **output-token exhaustion only** — not a scientific, protocol, dataset, or prompt defect. Evidence: `pilot/v2/CLEAN_SCIENTIFIC_RERUN_STATUS.md`, `pilot/v2/VOID_TECHNICAL_DIAGNOSIS.md`, `results/scientific-rerun-16384/`.
- `max_tokens = 16384` is therefore **demonstrably insufficient** for this model on at least one real pilot program, because the model spends nearly the entire budget on reasoning tokens before emitting any content.
- No valid pilot session has completed, so **no Top-K, EXAM\*, discordance, or effect estimate exists.**

# Next Actions

1. **Pre-results technical amendment / stress test** — diagnose and bound the reasoning-token exhaustion (raise `max_tokens`, and/or constrain reasoning effort if the provider exposes it), validated by stress smoke on non-manifest fixtures only. This is a technical amendment recorded **before** any result exists; it must not touch the frozen protocol, dataset, priors, prompts, or statistical plan.
2. Re-run the clean scientific pilot: Session G and Session P back-to-back under the frozen invariants (`pilot/v2/PILOT_PROTOCOL_V2.md` §3.1).
3. Analyze each session natively, then run the cross-session C-vs-B primary comparison (`analysis/compare_v2_sessions.py`) per `pilot/v2/STATISTICAL_ANALYSIS_PLAN.md` §6.
4. Apply the null-calibration gate (A_G vs A_P) **before** interpreting the primary result.
5. Apply `pilot/v2/CLAIM_BOUNDARIES_V2.md` to every sentence written about the outcome.

**In parallel and permitted now:** a **pre-results APA 7 paper draft** — Title, Abstract (structure only), Introduction, Related Work, Method, Materials, planned Analysis, Threats to Validity, Ethics. The Method section can be written in full, because the protocol is frozen and public.

# Latest Experimental Results

**None.** No valid scientific performance result exists. All pilot attempts to date are VOID and are retained only as audit history. Mock-provider integration checks are engineering artifacts and are not research evidence.

**No Results or Discussion claim may be written yet.** Writing any performance number, effect direction, or comparative statement at this stage would violate `pilot/v2/CLAIM_BOUNDARIES_V2.md`.

# Known Risks

- `dossier/99_synthesis.md` §S5 (project-level), `pilot/SCIENTIFIC_RISKS.md` (pilot-level).
- Open items from `pilot/v2/PRE_RUN_REVIEW_V2.md`: **V-1** single-annotator residual in the blinded labeling pass; **V-2** the `<ALGORITHMIC_PATTERN_PRIOR>` delimiter tag wraps generic text in arm B — the only asymmetry in the design that biases *toward* the hypothesis, and the one to fix before any confirmatory run; **V-5** a statistically null primary result is the expected outcome at n = 30 and must not be read as evidence of absence.
- Reasoning-token exhaustion is now a demonstrated operational risk for this model, not a hypothetical one.
- ⚠️ **ISEF rule:** generative AI may not be used to author the research plan, the ≤250-word abstract, the poster, or the citations (`AGENTS.md` §3.2 item 7, `dossier/08_block8_competition.md`). AI-assisted engineering and specification work is permissible but must be disclosed accurately. This constrains how the paper draft may be produced.

# Agent Handoffs

- **Claude (science):** delivered. v1 `81fd51d`, v2 `579c687`; reviews in `pilot/PRE_RUN_REVIEW.md` and `pilot/v2/PRE_RUN_REVIEW_V2.md`.
- **Antigravity (data):** delivered. Corrected v2.1 sample frozen at `9c83767`; audits under `data/manifests/`.
- **Codex (engineering):** delivered through Gate 7 and the VOID rerun diagnosis at `583c8bf`; runbooks in `docs/PILOT_RUNBOOK.md` and `pilot/v2/OPENROUTER_MODEL_FREEZE_RUNBOOK.md`. No result handoff exists, because no valid result exists.

# Branch Map

`main` is now the authoritative branch and contains everything below (fast-forwarded from `agent/codex-gate7`, linear history, no squash or rewrite):

| Branch | Role | Tip |
|---|---|---|
| `main` | authoritative, contains all work | this commit |
| `agent/codex-gate7` | engineering through Gate 7 + VOID diagnostics | `583c8bf` |
| `agent/antigravity-data-v2` | dataset v2.1 | `9c83767` |
| `agent/codex-v2-preflight` | v2 engineering gates | `96de08d` |
| `agent/claude-science` | scientific specification v1 + v2 | `579c687` |
| `agent/codex-experiment` | original pilot infrastructure | `c5265d0` |
