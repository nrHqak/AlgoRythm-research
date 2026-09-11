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
| 2026-09-11T17:40:03.553129+00:00 | 54de7396-1a1e-473d-ba21-f9d72c825ee7 | smoke_freeze_G/no_prior/rep-1 | 79b0b96e5e51 | ok | results/smoke-freeze/20260911T173958167354Z/raw/54de7396-1a1e-473d-ba21-f9d72c825ee7.json | - |
| 2026-09-11T17:40:08.729324+00:00 | 6a3c48b9-3b97-4f6f-a7b0-df6db055b0e4 | smoke_freeze_G/generic_prior/rep-1 | 79b0b96e5e51 | ok | results/smoke-freeze/20260911T173958167354Z/raw/6a3c48b9-3b97-4f6f-a7b0-df6db055b0e4.json | - |
| 2026-09-11T17:40:11.409682+00:00 | 607c8f17-0934-4a31-9593-00a226a99d21 | smoke_freeze_G/no_prior/rep-1 | 79b0b96e5e51 | ok | results/smoke-freeze/20260911T173958167354Z/raw/607c8f17-0934-4a31-9593-00a226a99d21.json | - |
| 2026-09-11T17:40:16.819386+00:00 | 87f68c80-5704-45d2-b263-0fd3de0635f0 | smoke_freeze_G/generic_prior/rep-1 | 79b0b96e5e51 | ok | results/smoke-freeze/20260911T173958167354Z/raw/87f68c80-5704-45d2-b263-0fd3de0635f0.json | - |
| 2026-09-11T17:40:23.225660+00:00 | b0932639-1439-4502-a082-0556021ae0b1 | smoke_freeze_G/no_prior/rep-1 | 79b0b96e5e51 | ok | results/smoke-freeze/20260911T173958167354Z/raw/b0932639-1439-4502-a082-0556021ae0b1.json | - |
| 2026-09-11T17:40:32.894779+00:00 | 0979b296-72b7-4a53-9d16-38a64b9818f6 | smoke_freeze_G/generic_prior/rep-1 | 79b0b96e5e51 | ok | results/smoke-freeze/20260911T173958167354Z/raw/0979b296-72b7-4a53-9d16-38a64b9818f6.json | - |
| 2026-09-11T17:40:35.850088+00:00 | 30eb4992-8352-4cbe-acc8-0fba16c49b89 | smoke_freeze_P/no_prior/rep-1 | 79b0b96e5e51 | ok | results/smoke-freeze/20260911T173958167354Z/raw/30eb4992-8352-4cbe-acc8-0fba16c49b89.json | - |
| 2026-09-11T17:40:39.778907+00:00 | 39cde1ab-3759-453f-9fb5-0195d53642d9 | smoke_freeze_P/pattern_prior/rep-1 | 79b0b96e5e51 | ok | results/smoke-freeze/20260911T173958167354Z/raw/39cde1ab-3759-453f-9fb5-0195d53642d9.json | - |
| 2026-09-11T17:40:43.429633+00:00 | fc51c8be-e1fe-4e95-9f91-26010b4ba1ce | smoke_freeze_P/no_prior/rep-1 | 79b0b96e5e51 | ok | results/smoke-freeze/20260911T173958167354Z/raw/fc51c8be-e1fe-4e95-9f91-26010b4ba1ce.json | - |
| 2026-09-11T17:40:48.237295+00:00 | 0b5d66b6-49c7-4f81-95c6-f9707d8941a1 | smoke_freeze_P/pattern_prior/rep-1 | 79b0b96e5e51 | ok | results/smoke-freeze/20260911T173958167354Z/raw/0b5d66b6-49c7-4f81-95c6-f9707d8941a1.json | - |
| 2026-09-11T17:40:59.092085+00:00 | adf2875d-49d7-4ac9-9bc0-135e5a386c1f | smoke_freeze_P/no_prior/rep-1 | 79b0b96e5e51 | ok | results/smoke-freeze/20260911T173958167354Z/raw/adf2875d-49d7-4ac9-9bc0-135e5a386c1f.json | - |
| 2026-09-11T17:40:59.096730+00:00 | 4c548c94-440b-4fc5-aaf8-a1c0902faf29 | smoke_freeze_P/pattern_prior/rep-1 | 79b0b96e5e51 | provider_failure | - | ValueError |

Smoke freeze VOID 20260911T173958167354Z: smoke call failed: provider_failure/ValueError. Do not proceed; record correction before a new attempt.

OpenRouter Gate 4/5 audit finalization 2026-09-11T17:43:34.517235+00:00: exact model and Z.AI provider matched on all 12 HTTP responses; 11 valid completions, call 12 truncated at 1024 tokens (1023 reasoning) with null content. Session 20260911T173958167354Z VOID; no parser failures, no retry or parameter change, no passing freeze, no coin flip, no scientific calls. Evidence: pilot/v2/model-freeze-attempts/20260911T173446Z-openrouter-smoke/gate4_gate5_result.json.

Pre-results technical amendment 2026-09-11: user authorized max_tokens 1024 -> 4096 because "1024 output tokens caused a valid smoke response to terminate before a usable completion was produced." All other provider, model, Z.AI endpoint pin, routing, temperature, repetition, prompt, prior, dataset, ground-truth, sampling, and statistical settings remain unchanged. Committed before a fresh smoke attempt and before any scientific candidate call. Evidence: pilot/v2/PRE_RESULTS_AMENDMENT_MAX_TOKENS_4096.md.
