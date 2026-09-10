# Experiment Log

Record every attempted run, including failed and excluded runs. Follow `AGENTS.md` and `dossier/99_synthesis.md`; do not reconstruct entries after the fact.

| timestamp | run ID | configuration | data manifest | status | outputs | notes |
|---|---|---|---|---|---|---|
| _pending_ | _placeholder_ | _placeholder_ | _placeholder_ | _placeholder_ | _placeholder_ | _placeholder_ |

| 2026-09-10T18:33:15.244741+00:00 | 20260910T183315Z-gemini-credential-precheck | Gemini OpenAI-compatible; gemini-3.8-flash; intended temperature=0, max_tokens=1024, timeout=120 | data/smoke/manifest.json (planned only; not executed) | BLOCKED BEFORE API LOOKUP | pilot/v2/model-freeze-attempts/20260910T183315Z-gemini-credential-precheck/precheck.json | Credential unavailable to login and non-login execution processes; 0 metadata requests, 0 smoke calls, 0 candidate calls, 0 coin flips. No generation parameters changed or accepted. |
| 2026-09-10T18:46:12.429499+00:00 | 5f20f4bd-ae02-4f7f-a9c2-a82fdb5f8edc | smoke_freeze_G/no_prior/rep-1 | 79b0b96e5e51 | ok | results/smoke-freeze/20260910T184609524153Z/raw/5f20f4bd-ae02-4f7f-a9c2-a82fdb5f8edc.json | - |
| 2026-09-10T18:46:12.435527+00:00 | ff7badfd-4141-4729-ae87-a320ae291a90 | smoke_freeze_G/generic_prior/rep-1 | 79b0b96e5e51 | provider_failure | - | HTTPError |

Smoke freeze VOID 20260910T184609524153Z: smoke call failed: provider_failure/HTTPError. Do not proceed; record correction before a new attempt.

Gate 4/5 audit finalization 2026-09-10T18:48:33.298695+00:00: Gemini metadata retrieval verified before smoke (2 HTTP 200 GETs). Smoke session 20260910T184609524153Z stopped on call 2 HTTP 503 UNAVAILABLE/high demand; 1 valid completion, 0 parser failures, no retry, no parameter changes, no model freeze, no coin flip, no candidate calls. Evidence: pilot/v2/model-freeze-attempts/20260910T184351Z-gemini-model-lookup/gate4_gate5_result.json.
| 2026-09-10T18:58:43.915293+00:00 | 5d60b8c6-a259-4b10-b249-1e3f7ea3dd7b | smoke_freeze_G/no_prior/rep-1 | 79b0b96e5e51 | ok | results/smoke-freeze/20260910T185841547998Z/raw/5d60b8c6-a259-4b10-b249-1e3f7ea3dd7b.json | - |
| 2026-09-10T18:58:46.567346+00:00 | a492c954-1f8c-4780-a42d-3a4e1999fa02 | smoke_freeze_G/generic_prior/rep-1 | 79b0b96e5e51 | ok | results/smoke-freeze/20260910T185841547998Z/raw/a492c954-1f8c-4780-a42d-3a4e1999fa02.json | - |
| 2026-09-10T18:58:56.133614+00:00 | 5f7a4ccf-e2b4-4e0b-822d-3b2e4f9c7e02 | smoke_freeze_G/no_prior/rep-1 | 79b0b96e5e51 | ok | results/smoke-freeze/20260910T185841547998Z/raw/5f7a4ccf-e2b4-4e0b-822d-3b2e4f9c7e02.json | - |
| 2026-09-10T18:58:56.138544+00:00 | dcd43422-ea6e-4dd3-b9be-8a06cc1369bd | smoke_freeze_G/generic_prior/rep-1 | 79b0b96e5e51 | provider_failure | - | HTTPError |

Smoke freeze VOID 20260910T185841547998Z: smoke call failed: provider_failure/HTTPError. Do not proceed; record correction before a new attempt.

Gate 4/5 retry audit finalization 2026-09-10T19:00:32.057021+00:00: fresh authorized session 20260910T185841547998Z stopped on call 4 HTTP 503 UNAVAILABLE/high demand; 3 valid completions, 0 parser failures, no automatic retry, unchanged settings/assets, no passing freeze, no coin flip, no scientific calls. Evidence: pilot/v2/model-freeze-attempts/20260910T185841Z-gemini-smoke-retry/gate4_gate5_result.json.
