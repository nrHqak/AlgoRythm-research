# Codex v2 engineering preflight changelog

Date: 2026-09-10. Base: `agent/claude-science`,
`579c68737ca4bd762bcbd7e57e3d28577e2c40bc`. Work branch:
`agent/codex-v2-preflight`. No real pilot, candidate LLM output inspection,
scientific sampling, or live provider dry run occurred.

## V-2: neutral delimiter

`experiments/prompts.py` now uses `<DEBUGGING_PRIOR>` and
`</DEBUGGING_PRIOR>` identically for generic B and pattern C. The text inside both
prior files is unchanged. System prompt and user template are unchanged.

`tests/test_v2_preflight.py` exercises all 12 labels × both priors (24 pairs),
asserting the exact construction `shared + open + prior + close`, common system
and shared text, exactly matching numbered checkpoint counts and ≤10-word
per-label difference (observed frozen maximum remains 8). It also changes the
smoke ground-truth metadata and fixed-source path and verifies identical prompts.
The original prompt test now expects the neutral closing delimiter.

The frozen `PROMPT_DIFF_V2.md` and `GENERIC_PLACEBO_PRIOR.md` describe the old tag
as an unresolved review finding. They are retained as the historical scientific
record. **This authorized engineering changelog supersedes only those delimiter
references**; it does not revise the prior content or hypotheses.

## V-3: original smoke fixtures

Added three hand-written runnable functions (sum initialization, frequency count,
and binary-search endpoint), fixed counterparts, JSON cases, and an explicit
manifest under `data/smoke/`. The README and dataset name say
**SMOKE DATA — NEVER SCIENTIFIC DATA**. No external dataset was consulted.
Fault lines and lookup labels are smoke metadata, never scientific annotation.
Offline tests prove the buggy functions fail known cases, fixed functions pass,
and the listed fault line is the single changed line.

## V-4: frozen cross-session analysis before results

`analysis/compare_v2_sessions.py` validates both sessions before writing a new
output file. It reconstructs every available raw prompt from the frozen assets
and manifest, compares exact strings, validates raw/processed rankings by
reparsing, and checks sample hashes, input hashes, IDs, repetition/condition
balance, execution keys, settings, source/truth metadata, prompt hashes,
engineering-only status and neutral delimiter parity. Missing programs in both
sessions still fail against the manifest. Provider failures remain counted,
with no-response cases restricted to provider-failure records.

The SAP implementation uses majority-of-five binary Top-K and mean-of-five
EXAM*, exact McNemar, 10,000 program bootstrap draws with seed 20260908, Wilcoxon,
per-class descriptive deltas, all five within-session repetition tests, failure
and determinism diagnostics, ranking/prompt lengths and exploratory sizing.
It applies `d_null >= d_primary` literally, including `0 >= 0`, before primary
interpretation. Sizing returns an explicit unavailable/unbounded result when
there is no discordance or psi=0.5. Negative effects retain their direction.
No inference treats 150 calls as 150 independent programs.

## Operational failure and model-freeze protection

- `experiments/model_preflight.py`: smoke-only 12-call command, exact echoed model
  check, pinned/explicit alias-only declaration, settings and asset hashes, dated
  freeze record and one session-order coin flip after mechanical success.
- A smoke attempt rejects every malformed response (stricter than the ≥90%
  minimum, consistent with “pass cleanly”), all-zero suspicion scores, empty
  content, truncation, identity mismatch and transport failure. No smoke accuracy
  threshold or model/arm selection rule is introduced.
- `experiments/providers/http.py` records whether identity was exposed; it no
  longer silently substitutes the requested model when the echo is missing.
  Missing identity is unverifiable and blocks the freeze.
- `experiments/health.py`: immediate identity stop; >5% provider failure at any
  chronological prefix of the first 50 calls; <80% completed-session ok rate,
  including an all-non-ok session, is void. This prefix interpretation is
  conservative and documented before data exists.
- `experiments/run_pilot.py` requires a committed unchanged model-freeze record
  for real v2 runs, checks the frozen settings and sample constraints, saves VOID
  diagnostics/log entries on health failure, and refuses void resumes. Processed
  failures with no raw response now participate in duplicate detection.
- Both analyzers reject unhealthy/VOID sessions before generating scientific
  reports. `analysis/run_analysis.py --report-root` allows separate G/P native
  reports without overwriting each other. Valid zero localization accuracy alone
  never invalidates a session.

## Unchanged scientific design and cost

Both frozen configs still specify 30 programs × 5 repetitions × 2 conditions.
The runner calls the provider once per condition inside the program/repetition
loops, with no retry loop: 300 calls per session, **600 total**; 150 each in A_G,
B, A_P, C. The second A costs 150 relative to a hypothetical 450-call three-arm
runner, and supplies the frozen null calibration. It cannot be removed safely
without a scientific protocol revision, so no such optimization was made.
The provided smoke command adds 12 calls, giving **612** on a clean first
attempt. Retries after a documented failed freeze are additional; token price
cannot be quoted until the provider/model and token usage are known.

## Validation and remaining execution gates

Full suite: `.venv/bin/python -m pytest -q` — **65 passed**. All provider calls
inside tests are locally mocked; no live credential was used or request sent. Tests
cover analytically known C wins, B wins, tie, majority aggregation, censoring,
parser failures, null drift, model/settings/sample mismatch, missing programs,
duplicate keys, prompt leakage/delimiter tampering, smoke validity, HTTP identity,
health thresholds, freeze requirements and the exact 600-call loop count.

`python -m experiments.validate_manifest data/smoke/manifest.json` passes. Both new
CLI help entry points execute. `git diff --check` is clean. The frozen priors,
protocols, system prompt and user template are byte-unchanged from the base.

Live model freeze, committed actual model parameters/session-order flip, and the
blinded scientific dataset remain pending. See `CODEX_PREFLIGHT_REPORT.md` and
`CODEX_MODEL_FREEZE_RUNBOOK.md`.
