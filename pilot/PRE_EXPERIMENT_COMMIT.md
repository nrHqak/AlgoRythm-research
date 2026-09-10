# Pre-Experiment Commitment (FROZEN v1)

**Status:** written and frozen 2026-09-10, **before any manifest exists and before any pilot data exists.** This is the pre-registration-style commitment for `algorythm_pattern_prior_pilot`. Its purpose is to make deviations visible, not to forbid them — a deviation that turns out to be necessary is allowed, but must be logged here (or in a dated addendum) with a reason, before results are analyzed, not after.

## What is frozen as of this commitment

By the git commit recorded in `CLAUDE_HANDOFF.md` (branch `agent/claude-science`), the following are fixed and will not be altered based on pilot outcomes:

1. **Pattern vocabulary** — the 12 classes and their exact slugs in `PATTERN_VOCABULARY.md`.
2. **Pattern priors** — the exact text of all 12 strings in `pilot/pattern_priors.json`, produced by the template in `pilot/prompts/pattern_prior.txt` and justified in `PATTERN_PRIORS.md`.
3. **Prompt content** — `pilot/prompts/system.txt` and `pilot/prompts/control.txt`, and the mechanical control→treatment diff documented in `PROMPT_DIFF.md`.
4. **Condition order policy** — `counterbalanced` (`PILOT_PROTOCOL.md` §2).
5. **Parser-failure policy** — `count_as_failure` as primary, `exclude` only as a labeled secondary sensitivity analysis (`PILOT_PROTOCOL.md` §2).
6. **Metrics and primary statistic** — `top1, top3, top5, exam`; primary test `exact_mcnemar`; already frozen in `pilot/config/pilot.yaml` by Codex and restated, not re-decided, here.
7. **Repetitions** — 5, per `pilot/config/pilot.yaml`.
8. **Sample scope** — ConDefects-Python, n=30, oracle pattern labels only.
9. **Inclusion/exclusion filters and the annotation procedure** — `ANNOTATION_GUIDE.md`.
10. **Analysis bootstrap seed** — `20260908` (the `analysis/run_analysis.py` default), unless a documented deviation.

## What is explicitly NOT frozen yet (deferred to whoever executes)

- Exact LLM provider/model, temperature beyond the recommended `0`, and max_tokens beyond the recommended floor of `1024` — selection criteria are frozen (`PILOT_PROTOCOL.md` §2), the specific choice is not, because credentials/provider access were not supplied to this handoff (`PROJECT_STATE.md`).
- The manifest itself (which 30 specific programs) — owned by the dataset-assembly step (`ANNOTATION_GUIDE.md`), not by this document.

Whoever fixes these must record them in the immutable `session_manifest.json` (already guaranteed by `experiments/run_pilot.py`) and treat that moment — not this document — as when those specific parameters became frozen for that run.

## Stopping / non-negotiation rules

1. **No peeking.** Items 1–9 above must not be changed after a candidate manifest's `selection_frozen_at` timestamp has passed for a given run. `experiments/models.py` and `experiments/run_pilot.py` enforce parts of this structurally (frozen-in-the-future rejected, duplicate execution keys aborted); the rest (prompt/prior wording) has no code-level lock and relies on this document plus git history as the record.
2. **No outcome-driven prior tuning.** Pilot results must never be used to retroactively edit the wording of `pilot/pattern_priors.json` in a way intended to make the treatment condition look better. If, after seeing pilot results, there is a genuine methodological reason to revise a prior (e.g. a checkpoint is discovered to reference something ambiguous), that revision must: (a) be written up as a dated addendum explaining the reason, independent of which condition it would favor; (b) bump the vocabulary/prior version to v2; (c) be applied **before** the confirmatory (n=300+) run, never retroactively to pilot data already collected. Pilot data collected under v1 priors is reported as v1 data, permanently.
3. **No silent exclusion.** Any program excluded after being included in a frozen manifest requires a logged `exclusion_reason` and `exclusion_decided_at` before the *next* freeze point, per `ANNOTATION_GUIDE.md` §6 — never a quiet removal.
4. **The pilot is calibration, not confirmation.** Regardless of what the pilot's exact McNemar p-value or Top-K deltas turn out to be, no submission, abstract, or claim may cite this pilot's n=30 result as evidence that the pattern-prior hypothesis is confirmed or refuted. See `CLAIM_BOUNDARIES.md` for the exhaustive list of permitted vs. forbidden claims — that document is itself frozen by this same commitment and for the same reason.

## Primary and secondary analyses committed in advance

- **Primary:** per-repetition exact McNemar on `top1` (already the config default, `statistics.primary: exact_mcnemar`), reported alongside pooled transition counts and the discordance-rate estimate that feeds the confirmatory study's power calculation (`PILOT_PROTOCOL.md` §5.3).
- **Secondary, pre-committed, not exploratory:** clustered bootstrap 95% CI on the Top-1/3/5/EXAM deltas (`analysis/statistics.py::clustered_bootstrap_delta`, 10,000 iterations, seed 20260908); Wilcoxon signed-rank on EXAM (`analysis/statistics.py::exam_comparison`); per-pattern Top-1 delta breakdown, conditional on at least 2 programs per pattern per `PILOT_PROTOCOL.md` §3; parser-failure-rate comparison by condition; prompt-length-by-condition comparison against the length-confound audit in `PATTERN_PRIORS.md`.
- **Explicitly exploratory, must be labeled as such if reported:** anything not listed above, including any leave-one-program-out sensitivity beyond the `adversarial.leave_one_program_out_top1` diagnostic Codex's pipeline already produces automatically.
