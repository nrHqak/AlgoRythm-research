# Full frozen scientific pilot status

**Experiment: VOID**

**Final status: NOT READY**

The authorized full run started from committed freeze
`ba57dbebf1e03d5e09b9f2c3a6b3255f7633ae64` on branch
`agent/codex-gate7`. The v2.1 manifest and all model, provider, routing,
generation, prompt, prior, sampling, ground-truth, and statistical settings
matched the freeze. Session order was G followed by P.

Session G used `20260911T181032Z-G`. Its first counterbalanced call was arm B
(`generic_prior`) for program `38752586`, repetition 1. The provider request
returned no string completion, and the frozen adapter recorded
`provider_failure` / `ValueError` with message
`provider completion content must be a string`.

The frozen first-50 health rule immediately evaluated one provider failure in
one call, above 5%. It wrote `VOID.json` with reason
`provider_failure rate >5% within first 50 calls; session is void` and aborted.
There was no retry. Session P did not start. The registered native and
cross-session analyses did not run because analysis of a VOID session is
prohibited.

The processed failure record and session manifest were saved. No raw provider
response exists: the frozen HTTP adapter raised on null completion content
before it returned a response object to `run_one`, so the runner could not
persist the body before parsing. This prevents exact token-usage recovery and
is an additional evidence limitation. The scientific attempt remains VOID.

OpenRouter key usage after the attempt was US$0.00917012. The two earlier
committed OpenRouter smoke attempts account for US$0.00365405 and US$0.00331207,
leaving **US$0.002204** attributable to this single scientific request, assuming
the key had no concurrent unrecorded use. The token count is unavailable from
the retained evidence.

Evidence:

- `results/processed/algorythm_pattern_prior_pilot_v2_generic/20260911T181032Z-G/session_manifest.json`
- `results/processed/algorythm_pattern_prior_pilot_v2_generic/20260911T181032Z-G/177cea9f-c6b3-48a4-b957-b60336875f25.json`
- `results/processed/algorythm_pattern_prior_pilot_v2_generic/20260911T181032Z-G/VOID.json`
- `results/scientific-run/20260911T181032Z/full_pilot_void.json`
- `results/scientific-run/20260911T181032Z/cost_reconciliation.json`

No scientific metric is reported because there is no valid completed paired
dataset. B Top-1, C Top-1, delta, Top-3, Top-5, EXAM*, McNemar p-value,
bootstrap interval, per-pattern results, and null-control drift are unavailable.

Post-VOID technical diagnosis is recorded in
`pilot/v2/VOID_TECHNICAL_DIAGNOSIS.md`. It finds that 4,096-token exhaustion is
the likely cause, recommends 16,384 subject to a new explicit amendment and
stress smoke, and records the adapter persistence fix. No scientific rerun was
performed.
