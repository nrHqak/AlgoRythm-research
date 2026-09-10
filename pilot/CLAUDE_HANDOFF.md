# Claude Scientific-Specification Handoff

**From:** Claude (agent/claude-science), 2026-09-10.
**Built on:** `agent/codex-experiment` at the two commits named in the project brief ("Set up reproducible pilot research environment", "Build reproducible pilot experiment infrastructure"), branched as `agent/claude-science`.
**Per the task brief: no experiment was run, no experimental results were inspected, and no file under `experiments/`, `analysis/`, or `tests/` was modified.** Everything below is scientific specification only.

## Files created (exactly as scoped, plus one necessary addition)

| File | Purpose |
|---|---|
| `pilot/PILOT_PROTOCOL.md` | Master frozen protocol: scope, frozen parameters (including the two this handoff had to freeze that `pilot/config/pilot.yaml` left open — condition order, parser-failure policy), dataset scope, freeze discipline, pilot-specific success criteria. Start here. |
| `pilot/PATTERN_VOCABULARY.md` | The 12 frozen pattern classes/slugs, definitions, confusable-pair rules, inclusion rule. |
| `pilot/PATTERN_PRIORS.md` | The 12 frozen prior strings with per-pattern dossier citations and a length-confound audit. |
| `pilot/pattern_priors.json` | Machine-readable `{pattern_label: prior_text}` map — byte-identical to the strings quoted in `PATTERN_PRIORS.md`; directly usable as `--priors` (see verification below). |
| `pilot/prompts/control.txt` | The frozen, shared user-prompt template (`--user-template`). Contains `{numbered_buggy_source}` plus the three other allowed fields; contains no forbidden fields. |
| `pilot/prompts/pattern_prior.txt` | The authoring template that produced every string in `pattern_priors.json` (not a runtime input). |
| `pilot/PROMPT_DIFF.md` | Documents the mechanical control→treatment diff and the file→CLI-flag mapping; records that the diff was verified against, not reimplemented from, `experiments/prompts.py`/`experiments/safety.py`. |
| `pilot/ANNOTATION_GUIDE.md` | Procedure for whoever assembles the manifest (currently Antigravity, per `PROJECT_STATE.md`) to assign `pattern_label`/`faulty_lines`/inclusion status consistently with everything above. |
| `pilot/PRE_EXPERIMENT_COMMIT.md` | Pre-registration-style commitment: what is frozen, what is deliberately deferred, the stopping/no-peeking rules, the pre-committed primary/secondary analyses. |
| `pilot/SCIENTIFIC_RISKS.md` | Pilot-specific risks (sample size, prior-length confound, oracle-label optimism, single-model generalization, annotation reliability, leakage, parser-failure asymmetry, cost, out-of-scope arms), each with its mitigation or explicit non-mitigation. |
| `pilot/CLAIM_BOUNDARIES.md` | What may and may not be claimed from this pilot once it runs, including the ISEF generative-AI-authorship disclosure boundary. |
| `pilot/CLAUDE_HANDOFF.md` | This file. |

**One file was added beyond the exact scoped list: `pilot/prompts/system.txt`.** Reason: `docs/PILOT_RUNBOOK.md` and `experiments/run_pilot.py` require a system-prompt file as a *separate* required input from the user template (`--system-prompt`, distinct from `--user-template`) — confirmed by reading `experiments/run_pilot.py::parser()` and the smoke test `tests/test_end_to_end.py`, which passes `system.txt` and `user.txt` as two distinct files. The scoped file list had two prompt files (`control.txt`, `pattern_prior.txt`) neither of which is a system prompt by the engineering contract's own definition (`pattern_prior.txt` is documented above as the non-runtime authoring template). Without a system prompt, `control.txt` cannot actually be run through `experiments.run_pilot`. This was the minimal addition needed to make the assigned deliverables executable rather than only documentary; it does not touch or rewrite any Codex-owned file. If this addition is unwanted, everything in `pilot/prompts/system.txt` is also reproducible from `PILOT_PROTOCOL.md`'s description of it.

## Consistency checks actually run before committing

All of the following were run against the **live** engineering code (`experiments.models`, `experiments.prompts`) in a local `.venv` built from `requirements.txt` — nothing below was reimplemented or hand-verified only by reading:

1. `PATTERN_VOCABULARY.md`'s 12 slugs and `pattern_priors.json`'s 12 keys are the same set (script-extracted and diffed, not eyeballed).
2. `pattern_priors.json` parses identically under `json.loads` and `yaml.safe_load` — confirming the claim in `PROMPT_DIFF.md` that it is directly usable as `--priors` without a format conversion.
3. Checkpoint counts: 4 for 10 patterns, 5 for `two_pointers` and `dynamic_programming` (the two dossier-cited exceptions) — matches `PATTERN_PRIORS.md`'s stated citations.
4. Word counts per prior, extracted from the actual JSON strings, cross-checked against every "(word count: N)" annotation in `PATTERN_PRIORS.md` for an exact match. (First pass caught a real discrepancy — hand-estimated counts in the initial draft were 20–40 words low across all 12 entries; three of the longest priors were trimmed and every claimed number in `PATTERN_PRIORS.md`, `pilot/prompts/pattern_prior.txt`, and `SCIENTIFIC_RISKS.md` was corrected to the script-measured value, not the original estimate. Final band: 119–138 words, spread 19.)
5. `experiments.prompts.validate_user_template(control.txt)` passes (no forbidden fields, no `PRIOR_OPEN`/`PRIOR_CLOSE` leakage, contains `{numbered_buggy_source}`).
6. `control.txt.format(...)` succeeds with a synthetic set of field values, confirming the doubled `{{`/`}}` braces around the JSON example render correctly rather than raising `KeyError`.
7. `experiments.prompts.build_prompt_pair` was called for all 12 pattern labels against a synthetic `ProgramRecord`, confirming for every one of them that: the treatment prompt starts with the control prompt, the suffix is exactly the delimited `<ALGORITHMIC_PATTERN_PRIOR>...</ALGORITHMIC_PATTERN_PRIOR>` block, and `build_prompt_pair`'s own internal `assert_only_prior_differs` check (real code, not reimplemented) raised nothing.
8. `pilot/config/pilot.yaml` still parses and its `conditions`/`target_n` values match what every new document above assumes (`pattern_agnostic`/`oracle_pattern_prior`/30) — this file was read, never edited.
9. Full repository test suite: `.venv/bin/python -m pytest -q` → **17 passed**, 0 failed. `.venv/bin/python -m compileall -q experiments analysis tests` → clean. Neither check exercises the new `pilot/` files directly (no test imports them yet), but both confirm the engineering layer this handoff builds on top of is untouched and still green.

The check script itself was scratch tooling (`/private/tmp/.../scratchpad/consistency_check.py`, outside the repository) and is not part of this commit.

## What is still needed from other agents (unchanged from `PROJECT_STATE.md`, restated for this handoff's context)

- **From Antigravity:** the actual candidate manifest — 30 ConDefects-Python programs meeting `PILOT_PROTOCOL.md` §3's filters, labeled per `ANNOTATION_GUIDE.md`, with `pattern_label` values drawn **exactly** from the 12 slugs in `PATTERN_VOCABULARY.md` (the run aborts via `SafetyViolation` in `experiments/run_pilot.py` if any included program's label has no matching key in `pattern_priors.json`). Once it exists, validate it with `python -m experiments.validate_manifest <path>` before anything else.
- **From whoever executes the pilot (Codex or otherwise):** pick provider/model/max_tokens within the criteria frozen in `PILOT_PROTOCOL.md` §2, record them in the immutable session manifest as `experiments/run_pilot.py` already does automatically, and follow `docs/PILOT_RUNBOOK.md`'s execution steps with `--user-template pilot/prompts/control.txt --system-prompt pilot/prompts/system.txt --priors pilot/pattern_priors.json --condition-order counterbalanced`, then analyze with `--parser-failure-policy count_as_failure` as primary.
- **Not produced by this handoff, and deliberately not attempted:** the dataset manifest itself, the pattern classifier (`dossier/99_synthesis.md` §S2.1), and any part of the confirmatory (n=300–500) design beyond what `PILOT_PROTOCOL.md` §1 explicitly carries forward unchanged.

## Commit

See the branch's HEAD commit on `agent/claude-science` for the exact SHA and full file list (reported to the user alongside this handoff, per the task brief's closing instructions).
