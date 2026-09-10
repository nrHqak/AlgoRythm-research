# Pilot Protocol (FROZEN v1)

**Status:** Frozen by the Claude scientific-specification handoff (`agent/claude-science`), 2026-09-10, before any pilot data exists.
**Governs:** the single pilot run defined by `pilot/config/pilot.yaml` (`experiment_name: algorythm_pattern_prior_pilot`). Does **not** govern the confirmatory study (n=300–500, realistic-label pipeline, 5 arms) sketched in `dossier/99_synthesis.md` §S2–S3 — that requires its own protocol freeze after this pilot's calibration numbers are in, per `PRE_EXPERIMENT_COMMIT.md`.
**Companion documents:** `PATTERN_VOCABULARY.md`, `PATTERN_PRIORS.md`, `pilot/pattern_priors.json`, `pilot/prompts/{system.txt,control.txt,pattern_prior.txt}`, `PROMPT_DIFF.md`, `ANNOTATION_GUIDE.md`, `PRE_EXPERIMENT_COMMIT.md`, `SCIENTIFIC_RISKS.md`, `CLAIM_BOUNDARIES.md`.

## 1. What this pilot is and is not

This is the **calibration pilot** anticipated by `dossier/99_synthesis.md` §S3 point 4 and §S5.4 ("Confirm with a 30-program pilot before locking [n≈300]"). `pilot/config/pilot.yaml` was already set up by Codex with `dataset.target_n: 30` in anticipation of exactly this. It corresponds to a restricted slice of the 5-arm design in `dossier/99_synthesis.md` §S2.2: only **Arm C (LLM zero-shot, pattern-agnostic)** vs. **Arm D under the oracle label condition** (LLM + pattern prior, gold label) — i.e. `conditions.control: pattern_agnostic` vs. `conditions.treatment: oracle_pattern_prior` in `pilot/config/pilot.yaml`. SBFL/MBFL baselines (Arms A/B), the reweighted-spectrum arm (Arm E), and the realistic (predicted-label) condition are **out of scope** for this pilot; see `CLAIM_BOUNDARIES.md` for what may not be claimed as a result.

Purpose, in order of priority:
1. Verify the frozen prompt/prior pipeline executes end-to-end on real data without a `SafetyViolation` abort.
2. Measure the parser-failure rate per condition (a large or asymmetric rate would mean the prompt/schema needs revision before any larger run — see §5).
3. Measure the discordant-pair rate (McNemar `b`, `c`) to plug into the power sketch in `dossier/05_block5_methodology.md` §5.4 and set the confirmatory study's target n.
4. Record a directional, non-confirmatory read of the effect for planning purposes only.

## 2. Frozen technical parameters

Parameters already frozen by Codex in `pilot/config/pilot.yaml` (restated here for a single reference point, not re-decided):

| Parameter | Value | Source |
|---|---|---|
| `experiment_name` | `algorythm_pattern_prior_pilot` | `pilot/config/pilot.yaml` |
| `dataset.target` | `ConDefects-Python` | `pilot/config/pilot.yaml` |
| `dataset.target_n` | `30` | `pilot/config/pilot.yaml` |
| `conditions.control` | `pattern_agnostic` | `pilot/config/pilot.yaml` |
| `conditions.treatment` | `oracle_pattern_prior` | `pilot/config/pilot.yaml` |
| `metrics` | `top1, top3, top5, exam` | `pilot/config/pilot.yaml` |
| `repetitions` | `5` | `pilot/config/pilot.yaml`; matches the 5-run LLM-stochasticity averaging protocol in `dossier/03_block3_fault_localization.md` §3c / `dossier/05_block5_methodology.md` §5.1 (arXiv:2512.03421) |
| `statistics.primary` | `exact_mcnemar` | `pilot/config/pilot.yaml`; matches `dossier/05_block5_methodology.md` §5.2 |
| `statistics.bootstrap_iterations` | `10000` | `pilot/config/pilot.yaml` |

Parameters frozen **by this document** (were previously open, per `pilot/config/pilot.yaml`'s own comment "Pattern vocabulary and prior text remain intentionally unfrozen..." and `PROJECT_STATE.md`'s "Frozen Decisions" list):

| Parameter | Frozen value | Rationale |
|---|---|---|
| `--condition-order` | `counterbalanced` | Cancels position/order effects at the individual-call level (`experiments/run_pilot.py::condition_order`: alternates which condition runs first based on `(program_index + repetition) % 2`). Preferred over `control_first`/`treatment_first`, which would confound condition with serial position for every single pair. |
| `--parser-failure-policy` (primary) | `count_as_failure` | Pre-registers the conservative handling: an unparseable response scores `top1=top3=top5=0`, `exam=1.0` rather than being dropped. Avoids the failure-prone version of post-hoc exclusion that `dossier/05_block5_methodology.md` §5.5 and `analysis/run_analysis.py`'s own help text flag as a hazard ("Exclusion is allowed only as an explicit sensitivity analysis and cannot satisfy primary balance"). |
| `--parser-failure-policy` (secondary) | `exclude`, run only as a labeled sensitivity re-analysis after the primary `count_as_failure` pass, never as the headline number | Same source. |
| Pattern vocabulary | 12 classes, see `PATTERN_VOCABULARY.md` | See that document. |
| Pattern priors | see `pilot/pattern_priors.json` / `PATTERN_PRIORS.md` | See those documents. |
| Prompt content | `pilot/prompts/{system.txt,control.txt}` | See `PROMPT_DIFF.md`. |
| `--temperature` | `0` | Matches `pilot/config/pilot.yaml`'s implicit default (`run_pilot.py` defaults `--temperature` to `LLM_TEMPERATURE` or `"0"`) and removes one source of run-to-run noise on top of the already-frozen 5-repetition averaging. |
| `--max-tokens` | `1024` (recommended floor; may be raised, never lowered, if truncation is observed in a dry run) | Enough for a JSON ranking with up to ~`loc` entries and short reasons on ConDefects-Python programs (avg 49.03 LOC per `dossier/04_block4_datasets.md` §4.3), consistent with the sub-2048-token prompt budget in arXiv:2512.03421 (`dossier/03_block3_fault_localization.md` §3c). |
| `--seed` (analysis bootstrap) | `20260908` (the `analysis/run_analysis.py` default) unless a documented deviation is logged | Freezing the default rather than silently relying on "whatever the default happens to be" makes the choice auditable. |

**Provider/model:** deliberately **not** frozen to one proprietary choice here — `PROJECT_STATE.md` records that "No provider/model credentials or exact model selection were supplied," and model/provider access is a resourcing decision outside scientific-specification ownership. What **is** frozen: selection criteria and the freeze discipline.
- Criteria: must support a `--provider openai_compatible` HTTP(S) endpoint per `experiments/providers`; must reliably follow a JSON-only output instruction (a very high parser-failure rate on a dry run is grounds to pick a different model, logged as a deviation, before spending the full 300-call budget); ideally from the model family already benchmarked in `dossier/03_block3_fault_localization.md` §3c (arXiv:2512.03421) so pilot numbers are comparable to a published baseline.
- Whoever executes the run **must** fix provider, model, temperature, and max_tokens **before** `selection_frozen_at` on the manifest and record them — this is already enforced structurally: `experiments/run_pilot.py` writes them into the immutable `session_manifest.json`, and `experiments/safety.py::assert_paired_settings` rejects a session where they differ between the two conditions of any pair.

## 3. Dataset scope for this pilot

- Source: ConDefects-Python only (`dossier/04_block4_datasets.md` §4.3) — Java, Codeflaws, BugT, and the AlgoRythm-sandbox slice are out of scope for the pilot (they remain in scope for the confirmatory corpus per `dossier/99_synthesis.md` §S1).
- n = 30 included programs, oracle pattern labels only (i.e. `pattern_source` records human/task-derived ground truth, not a classifier prediction — the `oracle_pattern_prior` condition name in `pilot/config/pilot.yaml` already encodes this).
- Inclusion filters (from `dossier/99_synthesis.md` §S1, restated as the pilot's operative filter — see `ANNOTATION_GUIDE.md` for the exact procedure): compiles; at least one passing and at least one failing test (excludes the ~40% of novice programs that fail all tests and leave fault localization undefined, per Araujo et al. 2016, `dossier/03_block3_fault_localization.md` §3a); a single identifiable fault (fix diff of one hunk, or manually verified as one logical fault); source length 10–300 physical lines.
- Pattern coverage target: aim for the 30 included programs to span as many of the 12 classes in `PATTERN_VOCABULARY.md` as ConDefects-Python realistically offers, with **at least 2 programs per included class** so a per-pattern breakdown (`analysis/run_analysis.py::build_metrics`'s `per_pattern` block) is not computed on n=1. A class absent from the pilot sample is not a protocol violation; it simply has no pilot-stage signal and must be flagged as such when the pilot report is written. This is a target for whoever assembles the manifest, not itself a manifest — see `ANNOTATION_GUIDE.md` and `CLAUDE_HANDOFF.md` for what is still needed from Antigravity.
- `evaluation_denominator`: left at its default (`loc`) per `ProgramRecord.exam_denominator` unless `ANNOTATION_GUIDE.md`'s annotator computes a more precise inspectable-statement count; either way it must be set consistently across all 30 programs, not mixed conventions.

## 4. Freeze discipline

- This document, `PATTERN_VOCABULARY.md`, `PATTERN_PRIORS.md`, `pilot/pattern_priors.json`, `pilot/prompts/{system.txt,control.txt,pattern_prior.txt}`, and `PROMPT_DIFF.md` are frozen as of the git commit recorded in `CLAUDE_HANDOFF.md`. No wording in any of these files may be edited after a candidate manifest exists and `selection_frozen_at` has passed, without opening a new version (v2) and a changelog entry — this mirrors the engineering-level immutability already enforced by `experiments/models.py` (`selection_frozen_at` cannot be in the future; exclusions cannot be added after freeze) and `experiments/run_pilot.py` (duplicate execution keys abort the run).
- The dataset manifest itself is **not** produced by this handoff (see `PROJECT_STATE.md`: "Antigravity's candidate manifest and validate it with `python -m experiments.validate_manifest`" remains a listed next action) — this protocol constrains what that manifest must look like (§3, `ANNOTATION_GUIDE.md`) so that when it arrives it can be validated and run without a second scientific freeze cycle.
- Per the task that produced this handoff: **no experiment was run and no results were inspected while producing these files.** `EXPERIMENT_LOG.md` and `CLAIMS.md` remain untouched placeholders, as they should until a real session runs.

## 5. Pilot-specific success criteria (to evaluate once — and only once — a real run exists)

1. The run completes with exit code reflecting `all(record.status == "ok")`, or every non-`ok` record is accounted for and its rate reported (§5.2).
2. Parser-failure rate per condition (`analysis` output's `adversarial.parser_failures_by_condition`) is reported for both conditions; a rate that differs sharply between `pattern_agnostic` and `oracle_pattern_prior` is itself a finding to report (it could mean the prior block helps or hurts the model's ability to follow the JSON schema) rather than something to silently normalize away.
3. Discordant-pair counts (`topk.top1.per_repetition_exact_mcnemar[*].control_hit_treatment_miss` / `.control_miss_treatment_hit`) are recorded per repetition and pooled, and fed into the `dossier/05_block5_methodology.md` §5.4 power sketch to produce a concrete target n for the confirmatory study (replacing that section's ⚠️-flagged own-derivation estimate of n≈300 with pilot-informed numbers).
4. `adversarial.prompt_length_by_condition` (mean chars/tokens per condition) is checked against the length-confound audit in `PATTERN_PRIORS.md` — if the observed gap is far larger than the ~22-word spread across pattern priors predicts, that points to a bug in prompt construction, not a real finding.
5. A small manual spot-check (recommended: 3–5 raw response files per condition, read by a human) confirms no qualitative sign of the treatment condition leaking fault-location information beyond what the delimited prior block contains — a belt-and-suspenders check on top of the structural guarantees in `PROMPT_DIFF.md`.

None of the above constitutes a confirmatory scientific claim; see `CLAIM_BOUNDARIES.md`.
