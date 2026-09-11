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
| 2026-09-11T17:52:43.555101+00:00 | d68744b3-05fc-4d36-94f6-4404c7c53cc7 | smoke_freeze_G/no_prior/rep-1 | 79b0b96e5e51 | ok | results/smoke-freeze/20260911T175238631073Z/raw/d68744b3-05fc-4d36-94f6-4404c7c53cc7.json | - |
| 2026-09-11T17:52:48.641760+00:00 | 133f413e-6c5c-49a3-aed6-356b7cc4c51e | smoke_freeze_G/generic_prior/rep-1 | 79b0b96e5e51 | ok | results/smoke-freeze/20260911T175238631073Z/raw/133f413e-6c5c-49a3-aed6-356b7cc4c51e.json | - |
| 2026-09-11T17:52:52.319763+00:00 | 8762f8dc-40c4-4fde-953e-9c58a5c75a7f | smoke_freeze_G/no_prior/rep-1 | 79b0b96e5e51 | ok | results/smoke-freeze/20260911T175238631073Z/raw/8762f8dc-40c4-4fde-953e-9c58a5c75a7f.json | - |
| 2026-09-11T17:52:56.294023+00:00 | 63077558-cbde-4920-a4f4-273c536b48e2 | smoke_freeze_G/generic_prior/rep-1 | 79b0b96e5e51 | ok | results/smoke-freeze/20260911T175238631073Z/raw/63077558-cbde-4920-a4f4-273c536b48e2.json | - |
| 2026-09-11T17:53:02.820156+00:00 | 3f311e23-f069-4ca2-b6c7-7e74c604dcc8 | smoke_freeze_G/no_prior/rep-1 | 79b0b96e5e51 | ok | results/smoke-freeze/20260911T175238631073Z/raw/3f311e23-f069-4ca2-b6c7-7e74c604dcc8.json | - |
| 2026-09-11T17:53:12.542982+00:00 | 65385b54-c01f-4143-a22c-2b45bd486831 | smoke_freeze_G/generic_prior/rep-1 | 79b0b96e5e51 | ok | results/smoke-freeze/20260911T175238631073Z/raw/65385b54-c01f-4143-a22c-2b45bd486831.json | - |
| 2026-09-11T17:53:17.346936+00:00 | 248cc7de-448f-4d2b-8b4c-7e6d54599fa4 | smoke_freeze_P/no_prior/rep-1 | 79b0b96e5e51 | ok | results/smoke-freeze/20260911T175238631073Z/raw/248cc7de-448f-4d2b-8b4c-7e6d54599fa4.json | - |
| 2026-09-11T17:53:20.229266+00:00 | 87ee12d9-054f-4256-9fea-06b9c3677c9d | smoke_freeze_P/pattern_prior/rep-1 | 79b0b96e5e51 | ok | results/smoke-freeze/20260911T175238631073Z/raw/87ee12d9-054f-4256-9fea-06b9c3677c9d.json | - |
| 2026-09-11T17:53:23.813968+00:00 | 9a3a4179-c896-4674-9f35-2f272aeb5815 | smoke_freeze_P/no_prior/rep-1 | 79b0b96e5e51 | ok | results/smoke-freeze/20260911T175238631073Z/raw/9a3a4179-c896-4674-9f35-2f272aeb5815.json | - |
| 2026-09-11T17:53:29.240246+00:00 | 1a3514f4-d695-4488-a4d8-bd59c2a8b2f7 | smoke_freeze_P/pattern_prior/rep-1 | 79b0b96e5e51 | ok | results/smoke-freeze/20260911T175238631073Z/raw/1a3514f4-d695-4488-a4d8-bd59c2a8b2f7.json | - |
| 2026-09-11T17:53:41.018707+00:00 | d2dd0e54-db1f-4c7d-bbb7-14406bc690f5 | smoke_freeze_P/no_prior/rep-1 | 79b0b96e5e51 | ok | results/smoke-freeze/20260911T175238631073Z/raw/d2dd0e54-db1f-4c7d-bbb7-14406bc690f5.json | - |
| 2026-09-11T17:53:51.160259+00:00 | e0e388fc-e7f8-4029-aa8c-c1b417feafd7 | smoke_freeze_P/pattern_prior/rep-1 | 79b0b96e5e51 | ok | results/smoke-freeze/20260911T175238631073Z/raw/e0e388fc-e7f8-4029-aa8c-c1b417feafd7.json | - |

OpenRouter Gate 4/5 PASS 2026-09-11T17:53:51.172389+00:00: the fresh post-amendment smoke completed 12/12 calls with exact model `z-ai/glm-5.3-flash`, pinned provider `Z.AI` (`z-ai/fp8`), fallbacks disabled, temperature 0, max_tokens 4096, and zero parser failures. Only after all calls passed, one registered coin flip froze session order G then P. Scientific calls: 0. Evidence: pilot/v2/model-freeze-attempts/20260911T175238Z-openrouter-smoke-4096/gate4_gate5_result.json and pilot/v2/MODEL_FREEZE_RECORD.json.
| 2026-09-11T18:11:10.755305+00:00 | 177cea9f-c6b3-48a4-b957-b60336875f25 | algorythm_pattern_prior_pilot_v2_generic/generic_prior/rep-1 | d53bcdc232f7 | provider_failure | - | ValueError |

Session 20260911T181032Z-G VOID: provider_failure rate >5% within first 50 calls; session is void. Do not resume; document a corrected freeze.

Full scientific pilot attempt finalized 2026-09-11: Session G stopped after its first call recorded provider_failure/ValueError (`provider completion content must be a string`). The frozen first-50 health rule marked session `20260911T181032Z-G` VOID. Session P was not started, no call was retried, and no scientific analysis was run. Calls attempted: 1/600; successful: 0; provider failures: 1; parser failures: 0. Reconciled OpenRouter cost: US$0.002204; exact token usage unavailable because the null-content provider response was rejected before raw-response persistence. Evidence: pilot/v2/FULL_PILOT_STATUS.md and results/scientific-run/20260911T181032Z/full_pilot_void.json.
