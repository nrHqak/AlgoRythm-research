# Codex v2 preflight report

2026-09-10. **Engineering verdict: READY FOR DATASET.** This means the pre-results
engineering work is complete; it does **not** authorize or declare readiness for
the real pilot. Execution gates 4–6 remain BLOCKED. Follow the frozen execution
order: the live model check precedes scientific sampling.

Base branch `agent/claude-science` is at
`579c68737ca4bd762bcbd7e57e3d28577e2c40bc`, verified as an ancestor of this work.
Delivery branch: `agent/codex-v2-preflight`. The commit carrying this report is the
engineering freeze; identify it with `git log -1 --format=%H -- pilot/v2/CODEX_PREFLIGHT_REPORT.md`.

No scientific candidate was selected, sent to an LLM, or inspected for model
output. No live provider call was made. All run artifacts exercised in tests were
created from original synthetic code under pytest temporary directories. The
scientific priors, hypotheses, system/user templates and frozen protocols were
left unchanged; only the common wrapper tag was replaced as explicitly requested.

## All six execution gates (PRE_RUN_REVIEW_V2 §3)

| Gate | Status PASS/BLOCKED | Evidence | Command/test | Remaining requirement |
|---|---|---|---|---|
| 1. Create noncandidate smoke fixtures | PASS | Three original buggy/fixed Python functions, known-case JSON tests, explicit smoke manifest and README | `python -m experiments.validate_manifest data/smoke/manifest.json`; `test_handwritten_smoke_fixtures_are_runnable` | None for engineering |
| 2. Neutral delimiter in B and C | PASS | Shared `<DEBUGGING_PRIOR>` constants; original prior text untouched; 24 prompt-pair checks and raw-prompt tamper detection | `test_all_labels_only_prior_content_differs_and_truth_invariant`; `test_integrity_tampering` | None |
| 3. Write, validate and commit cross-session analysis before real data | PASS | `analysis/compare_v2_sessions.py`; program-level SAP implementation; synthetic analytical expectations; delivered in this branch's engineering commit | `.venv/bin/python -m pytest -q` (**65 passed**) | None for engineering; scientific inputs intentionally absent |
| 4. Execute model freeze: exact ID, echo and smoke dry run | BLOCKED | Executable smoke-only command and model/health guards are implemented and mocked tests pass; runbook prepared | `python -m experiments.model_preflight --help`; `test_smoke_12_calls_both_shapes_both_priors`; provider-failure/identity tests | Explicit provider endpoint, credentials, exact model/version reference, then successful live smoke check and committed freeze evidence |
| 5. Record session-order coin flip and frozen parameters | BLOCKED | Successful freeze command records one coin flip plus all settings; runner checks unchanged committed record | `test_freeze_required_committed_and_settings_immutable` | Actual parameters and the single operational flip after successful live smoke check, committed before real execution; no operational coin flipped here |
| 6. Execute blinded sampling and ground-truth protocol | BLOCKED | No frame/manifest created or reviewed; source/task/truth/smoke exclusion guards implemented; frozen procedural instructions preserved | Later: `python -m experiments.validate_manifest "$PILOT_MANIFEST"`; then review committed stage/blinding audit trail | Blinded diff-first ground truth committed before labeling; second blind; eligibility/tests, one-task rule, frame counts/class allocation, seed/draw and final n=30 manifest |

Gates 1–3 close the engineering review findings V-3, V-2 and V-4. Gates 4–5 have
implemented, offline-tested tooling, but a mock test cannot close a live-provider
execution gate. Gate 6 needs the dataset/annotation process; schema validation
cannot prove human blinding. No scientific experiment readiness claim is made.

## Analysis delivered and validated

- Primary C vs B: majority-of-five per program, Top-1 exact McNemar, b/c/d and
  discordance rate, 10,000-draw percentile bootstrap (seed 20260908).
- Null A_G vs A_P evaluated before interpretation; `d_null >= d_primary` makes
  the primary uninterpretable, even when both counts are zero or p is small.
- Secondary Top-3/Top-5, mean-of-five EXAM* with bootstrap/Wilcoxon, both native
  A comparisons, all five per-repetition checks together, descriptive per-class
  deltas. EXAM* is explicitly censored and physical-line based.
- Parser/provider failures remain counted; no program silently drops. Reports
  include raw-response and Top-1 determinism, ranking length, prompt length and
  parity, program aggregates, and exploratory sizing with undefined/unbounded
  cases represented explicitly.
- Cross-session hard checks include manifest and source/test hashes, exact
  program IDs, model/provider/token/temperature/timeout/endpoint/freeze settings,
  five repetitions, condition balance, unique execution keys, shared prompts,
  neutral delimiter, raw/processed consistency, and ground-truth input exclusion.
- Analytically known n=8 synthetic extremes produce b=8/c=0 or b=0/c=8,
  p=1/128 and delta ±1; ties give p=1 and an uninterpretable null gate. A 3/5 vs
  2/5 success pattern produces program delta 1, not invocation delta 0.2.

A provider failure is retained as diagnostic evidence. Identity mismatch or an
unhealthy session stops loudly, writes VOID/log diagnostics, and cannot generate
scientific analysis files. A legitimate all-miss localization result remains
valid data if the responses are mechanically valid. Empty/malformed/all-zero
suspicion outputs reject a smoke freeze. Priors are never tuned in response.

## Exact model-call count and cost boundary

| Work | Calculation | Calls |
|---|---|---:|
| G: A_G + B | 30 × 5 × 2 | 300 |
| P: A_P + C | 30 × 5 × 2 | 300 |
| Scientific total | Four measured arms, 150 calls each | **600** |
| Prepared successful smoke attempt | 3 fixtures × 2 shapes × 2 prior maps | **12** |
| Clean first-attempt total | Scientific + smoke | **612** |

`test_exact_v2_call_budget_from_frozen_configs_and_runner_order` enumerates the
actual `condition_order` output for both frozen configs. Each resulting iteration
calls `run_one`, which calls `provider.complete` once; the HTTP adapter posts once
without automatic retries. Early aborts reduce actual calls; documented new smoke
attempts add calls. Dollars cannot be fixed without the selected model's tariff
and token usage; no price or token estimate is fabricated.

There are 300 no-prior calls, but the incremental duplicate relative to a 450-call
three-arm design is **150**. Eliminating A_P or reusing A_G would remove the
empirical null calibration and invalidate the frozen drift rule. It therefore
cannot be safely eliminated within the authorized frozen design; both sessions
and five repetitions are preserved.

## Files changed

- `experiments/prompts.py`, `experiments/providers/http.py`,
  `experiments/run_pilot.py`: neutral wrapper and operational enforcement.
- `experiments/health.py`, `experiments/model_preflight.py`: health checks and
  smoke-only freeze tooling.
- `analysis/compare_v2_sessions.py`, `analysis/run_analysis.py`: program-level
  comparison, void guards and separate native report destinations.
- `data/smoke/README.md`, `data/smoke/manifest.json`, and `buggy.py`, `fixed.py`,
  `tests.json` under each of `smoke-sum`, `smoke-count`, `smoke-search`.
- `tests/test_prompts_and_parsing.py`, `tests/test_v2_preflight.py`.
- This report, `CODEX_PREFLIGHT_CHANGELOG.md`, `CODEX_MODEL_FREEZE_RUNBOOK.md`.

Validation: full pytest suite **65 passed**; smoke manifest valid; new CLI help
entry points load; `git diff --check` clean; frozen scientific files unchanged
against `579c687`. No new dependencies were introduced. See the runbook for exact
future commands and the distinction between runner exit codes 1 and 2.
