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

Post-VOID technical diagnosis 2026-09-11: no new provider or candidate call was made. US$0.002204 exactly fits 1,040 input tokens plus the full 4,096-token completion allowance at frozen Z.AI pricing. The earlier direct 1,024-token failure had `finish_reason=length`, 1,023 reasoning tokens, reasoning present, and `content=null`; therefore 4,096 exhaustion by reasoning is the likely cause, though the failed generation body is unrecoverable. Recommended max_tokens: 16,384, proposal only. The adapter now retains credential-scrubbed complete provider JSON before content validation. Evidence: pilot/v2/VOID_TECHNICAL_DIAGNOSIS.md.
| 2026-09-12T09:01:34.089071+00:00 | d3e6356b-f080-4faa-887e-39f482b08542 | stress_smoke_G/A_G/rep-1 | 1403c7a87bda | ok | results/stress-smoke-16384/20260912T090056Z/raw/d3e6356b-f080-4faa-887e-39f482b08542.json | - |
| 2026-09-12T09:02:23.999254+00:00 | e2e4380f-523c-48d8-a1e7-680937b3175e | stress_smoke_G/B/rep-1 | 1403c7a87bda | ok | results/stress-smoke-16384/20260912T090056Z/raw/e2e4380f-523c-48d8-a1e7-680937b3175e.json | - |
| 2026-09-12T09:03:01.559232+00:00 | 13b86974-273e-44d5-93ff-1ab9f551d4fc | stress_smoke_G/A_G/rep-2 | 1403c7a87bda | ok | results/stress-smoke-16384/20260912T090056Z/raw/13b86974-273e-44d5-93ff-1ab9f551d4fc.json | - |
| 2026-09-12T09:03:38.092828+00:00 | 99ed207b-16b7-4302-a626-32fc4dc3dc43 | stress_smoke_G/B/rep-2 | 1403c7a87bda | ok | results/stress-smoke-16384/20260912T090056Z/raw/99ed207b-16b7-4302-a626-32fc4dc3dc43.json | - |
| 2026-09-12T09:04:40.152319+00:00 | 8d8f8736-f796-4b04-8c44-6dd40fb2ecec | stress_smoke_G/A_G/rep-3 | 1403c7a87bda | ok | results/stress-smoke-16384/20260912T090056Z/raw/8d8f8736-f796-4b04-8c44-6dd40fb2ecec.json | - |
| 2026-09-12T09:05:16.202665+00:00 | e4444a5e-dc39-43ae-84e8-fb7519e28786 | stress_smoke_G/B/rep-3 | 1403c7a87bda | ok | results/stress-smoke-16384/20260912T090056Z/raw/e4444a5e-dc39-43ae-84e8-fb7519e28786.json | - |
| 2026-09-12T09:06:11.878998+00:00 | 5b794fbe-e9bc-491c-87f0-a4e8ab9914c0 | stress_smoke_G/A_G/rep-4 | 1403c7a87bda | ok | results/stress-smoke-16384/20260912T090056Z/raw/5b794fbe-e9bc-491c-87f0-a4e8ab9914c0.json | - |
| 2026-09-12T09:07:00.959485+00:00 | 076d48b0-9641-490f-a37e-ff483c9a06ae | stress_smoke_G/B/rep-4 | 1403c7a87bda | ok | results/stress-smoke-16384/20260912T090056Z/raw/076d48b0-9641-490f-a37e-ff483c9a06ae.json | - |
| 2026-09-12T09:07:49.182274+00:00 | fa789531-7512-4f55-a2d5-e4d6b7e096bb | stress_smoke_G/A_G/rep-5 | 1403c7a87bda | ok | results/stress-smoke-16384/20260912T090056Z/raw/fa789531-7512-4f55-a2d5-e4d6b7e096bb.json | - |
| 2026-09-12T09:08:31.901537+00:00 | ef94b796-e8af-4157-b265-b5ce5c645f9b | stress_smoke_G/B/rep-5 | 1403c7a87bda | ok | results/stress-smoke-16384/20260912T090056Z/raw/ef94b796-e8af-4157-b265-b5ce5c645f9b.json | - |
| 2026-09-12T09:09:10.306160+00:00 | ed784cea-173c-460b-a2b0-c9445a36f0ce | stress_smoke_P/A_P/rep-1 | 1403c7a87bda | ok | results/stress-smoke-16384/20260912T090056Z/raw/ed784cea-173c-460b-a2b0-c9445a36f0ce.json | - |
| 2026-09-12T09:10:00.872675+00:00 | 8fc07179-5bfa-4b5b-a0d5-0a7ddb5fe1bd | stress_smoke_P/C/rep-1 | 1403c7a87bda | ok | results/stress-smoke-16384/20260912T090056Z/raw/8fc07179-5bfa-4b5b-a0d5-0a7ddb5fe1bd.json | - |
| 2026-09-12T09:10:50.729581+00:00 | f05d785f-5721-4c8d-902f-8ab956f49af2 | stress_smoke_P/A_P/rep-2 | 1403c7a87bda | ok | results/stress-smoke-16384/20260912T090056Z/raw/f05d785f-5721-4c8d-902f-8ab956f49af2.json | - |
| 2026-09-12T09:11:37.230962+00:00 | 14b8e2f2-fdf4-4a34-80a2-6089f61b4977 | stress_smoke_P/C/rep-2 | 1403c7a87bda | ok | results/stress-smoke-16384/20260912T090056Z/raw/14b8e2f2-fdf4-4a34-80a2-6089f61b4977.json | - |
| 2026-09-12T09:12:27.200989+00:00 | a6b3001a-e862-42bb-8891-40488db556a4 | stress_smoke_P/A_P/rep-3 | 1403c7a87bda | ok | results/stress-smoke-16384/20260912T090056Z/raw/a6b3001a-e862-42bb-8891-40488db556a4.json | - |
| 2026-09-12T09:13:25.938825+00:00 | 13aba349-5c86-49ad-a601-3111e62d4abd | stress_smoke_P/C/rep-3 | 1403c7a87bda | ok | results/stress-smoke-16384/20260912T090056Z/raw/13aba349-5c86-49ad-a601-3111e62d4abd.json | - |
| 2026-09-12T09:14:29.282327+00:00 | 86408524-a293-4ca9-b341-c3bedd9992f5 | stress_smoke_P/A_P/rep-4 | 1403c7a87bda | ok | results/stress-smoke-16384/20260912T090056Z/raw/86408524-a293-4ca9-b341-c3bedd9992f5.json | - |
| 2026-09-12T09:14:29.294850+00:00 | 92afdb66-41fb-413a-9034-1ece976d032b | stress_smoke_P/C/rep-4 | 1403c7a87bda | provider_failure | - | ChunkedEncodingError |

Stress smoke `20260912T090056Z` BLOCKED: 17/20 calls completed successfully;
call 18 failed during response transport with `ChunkedEncodingError`, was not
retried, and calls 19-20 were not sent. Completed responses had zero parser,
content-null, and length failures. No scientific candidate was sent. The
provisional projection from 17 completed calls was US$1.238168118, but the
registered cost gate remains incomplete because the required 20/20 smoke did
not complete. Evidence: `results/stress-smoke-16384/20260912T090056Z/` and
`pilot/v2/STRESS_SMOKE_16384_STATUS.md`.
| 2026-09-12T10:37:26.235501+00:00 | d0119b2a-4eea-4a1c-b40e-a3b01571aa11 | stress_smoke_G/A_G/rep-1 | 1403c7a87bda | ok | results/stress-smoke-16384/20260912T103649Z-fresh/raw/d0119b2a-4eea-4a1c-b40e-a3b01571aa11.json | - |
| 2026-09-12T10:39:41.294499+00:00 | 07ea4b08-7bdc-4608-9676-db08598609c3 | stress_smoke_G/B/rep-1 | 1403c7a87bda | ok | results/stress-smoke-16384/20260912T103649Z-fresh/raw/07ea4b08-7bdc-4608-9676-db08598609c3.json | - |
| 2026-09-12T10:40:19.325840+00:00 | 4ff17ed2-9fe9-4614-8186-92331face70b | stress_smoke_G/A_G/rep-2 | 1403c7a87bda | ok | results/stress-smoke-16384/20260912T103649Z-fresh/raw/4ff17ed2-9fe9-4614-8186-92331face70b.json | - |
| 2026-09-12T10:40:56.416295+00:00 | d48c825c-2e0c-48e0-9d01-efe854405f2d | stress_smoke_G/B/rep-2 | 1403c7a87bda | ok | results/stress-smoke-16384/20260912T103649Z-fresh/raw/d48c825c-2e0c-48e0-9d01-efe854405f2d.json | - |
| 2026-09-12T10:41:40.169295+00:00 | 7ffe6524-da2d-4e8b-a070-eb6caf919ba5 | stress_smoke_G/A_G/rep-3 | 1403c7a87bda | ok | results/stress-smoke-16384/20260912T103649Z-fresh/raw/7ffe6524-da2d-4e8b-a070-eb6caf919ba5.json | - |
| 2026-09-12T10:42:01.320829+00:00 | 56bcbb55-0829-4802-b785-b0cfc1f1f6f1 | stress_smoke_G/B/rep-3 | 1403c7a87bda | ok | results/stress-smoke-16384/20260912T103649Z-fresh/raw/56bcbb55-0829-4802-b785-b0cfc1f1f6f1.json | - |
| 2026-09-12T10:42:24.307265+00:00 | 0f9c94ae-ef6c-4bba-a1cb-3a52f62c0a9c | stress_smoke_G/A_G/rep-4 | 1403c7a87bda | ok | results/stress-smoke-16384/20260912T103649Z-fresh/raw/0f9c94ae-ef6c-4bba-a1cb-3a52f62c0a9c.json | - |
| 2026-09-12T10:43:14.457275+00:00 | 18dd910f-3b0a-44a6-8de7-a784e42a6231 | stress_smoke_G/B/rep-4 | 1403c7a87bda | ok | results/stress-smoke-16384/20260912T103649Z-fresh/raw/18dd910f-3b0a-44a6-8de7-a784e42a6231.json | - |
| 2026-09-12T10:44:39.986452+00:00 | 50e01315-57dc-4b3d-85f0-a606dab6bf1c | stress_smoke_G/A_G/rep-5 | 1403c7a87bda | ok | results/stress-smoke-16384/20260912T103649Z-fresh/raw/50e01315-57dc-4b3d-85f0-a606dab6bf1c.json | - |
| 2026-09-12T10:45:19.056715+00:00 | 62a8e07a-852f-4467-85ef-e43f412bc423 | stress_smoke_G/B/rep-5 | 1403c7a87bda | ok | results/stress-smoke-16384/20260912T103649Z-fresh/raw/62a8e07a-852f-4467-85ef-e43f412bc423.json | - |
| 2026-09-12T10:45:53.721368+00:00 | 7623bca2-8e75-4819-8102-f9f7bb52729c | stress_smoke_P/A_P/rep-1 | 1403c7a87bda | ok | results/stress-smoke-16384/20260912T103649Z-fresh/raw/7623bca2-8e75-4819-8102-f9f7bb52729c.json | - |
| 2026-09-12T10:46:39.280427+00:00 | 2ef77192-8665-4c49-adff-dc699b64035c | stress_smoke_P/C/rep-1 | 1403c7a87bda | ok | results/stress-smoke-16384/20260912T103649Z-fresh/raw/2ef77192-8665-4c49-adff-dc699b64035c.json | - |
| 2026-09-12T10:47:17.570652+00:00 | 7d3311af-4f0f-4da9-9289-6fde81e3302f | stress_smoke_P/A_P/rep-2 | 1403c7a87bda | ok | results/stress-smoke-16384/20260912T103649Z-fresh/raw/7d3311af-4f0f-4da9-9289-6fde81e3302f.json | - |
| 2026-09-12T10:47:53.593296+00:00 | 24d2db8e-84fd-4b50-af86-c422eb035a6e | stress_smoke_P/C/rep-2 | 1403c7a87bda | ok | results/stress-smoke-16384/20260912T103649Z-fresh/raw/24d2db8e-84fd-4b50-af86-c422eb035a6e.json | - |
| 2026-09-12T10:48:32.425179+00:00 | a8ba983f-50ad-40a6-88cd-7158dc4687f5 | stress_smoke_P/A_P/rep-3 | 1403c7a87bda | ok | results/stress-smoke-16384/20260912T103649Z-fresh/raw/a8ba983f-50ad-40a6-88cd-7158dc4687f5.json | - |
| 2026-09-12T10:48:57.197520+00:00 | 76d9ba84-47db-40a4-9e0b-b131ae0f3e25 | stress_smoke_P/C/rep-3 | 1403c7a87bda | ok | results/stress-smoke-16384/20260912T103649Z-fresh/raw/76d9ba84-47db-40a4-9e0b-b131ae0f3e25.json | - |
| 2026-09-12T10:49:42.261697+00:00 | 68fd6429-4f71-4c7c-880c-b46660fc7276 | stress_smoke_P/A_P/rep-4 | 1403c7a87bda | ok | results/stress-smoke-16384/20260912T103649Z-fresh/raw/68fd6429-4f71-4c7c-880c-b46660fc7276.json | - |
| 2026-09-12T10:50:12.070886+00:00 | bd22cae3-5002-41d5-aaed-76cfeddc5a97 | stress_smoke_P/C/rep-4 | 1403c7a87bda | ok | results/stress-smoke-16384/20260912T103649Z-fresh/raw/bd22cae3-5002-41d5-aaed-76cfeddc5a97.json | - |
| 2026-09-12T10:50:58.242287+00:00 | 08205b68-dd34-4726-99ad-382a0be4906d | stress_smoke_P/A_P/rep-5 | 1403c7a87bda | ok | results/stress-smoke-16384/20260912T103649Z-fresh/raw/08205b68-dd34-4726-99ad-382a0be4906d.json | - |
| 2026-09-12T10:51:46.780888+00:00 | d7fbc862-8c53-4f63-86e0-b075c51b2d2c | stress_smoke_P/C/rep-5 | 1403c7a87bda | ok | results/stress-smoke-16384/20260912T103649Z-fresh/raw/d7fbc862-8c53-4f63-86e0-b075c51b2d2c.json | - |

Fresh stress smoke `20260912T103649Z-fresh` PASS: 20/20 new calls completed in
frozen G-then-P order with zero parser, content-null, length, transport,
identity, or fallback failures. Exact model `z-ai/glm-5.3-flash`; pinned
underlying provider Z.AI (`z-ai/fp8`); temperature 0; max_tokens 16,384. No
scientific candidate was sent. Average observed cost was US$0.0020021095 per
call; the 600-call projection is US$1.2012657, below the US$4.50 gate. The
earlier attempt is preserved and reclassified by user direction as ABORTED /
INCOMPLETE DUE TO LOCAL EXECUTION INTERRUPTION; none of its calls were reused.
| 2026-09-12T10:59:13.636018+00:00 | 0b5694ff-6340-40b0-9230-f4cdcf021e60 | algorythm_pattern_prior_pilot_v2_generic/generic_prior/rep-1 | d53bcdc232f7 | ok | results/scientific-rerun-16384/raw/algorythm_pattern_prior_pilot_v2_generic/20260912T105822Z-G-clean/0b5694ff-6340-40b0-9230-f4cdcf021e60.json | - |
| 2026-09-12T11:01:49.320368+00:00 | 4b061c24-1153-459c-a8f9-31530687bb42 | algorythm_pattern_prior_pilot_v2_generic/no_prior/rep-1 | d53bcdc232f7 | ok | results/scientific-rerun-16384/raw/algorythm_pattern_prior_pilot_v2_generic/20260912T105822Z-G-clean/4b061c24-1153-459c-a8f9-31530687bb42.json | - |
| 2026-09-12T11:03:34.005577+00:00 | b8bacf6e-c4be-4c85-a01d-cfaec053d6e6 | algorythm_pattern_prior_pilot_v2_generic/no_prior/rep-2 | d53bcdc232f7 | ok | results/scientific-rerun-16384/raw/algorythm_pattern_prior_pilot_v2_generic/20260912T105822Z-G-clean/b8bacf6e-c4be-4c85-a01d-cfaec053d6e6.json | - |
| 2026-09-12T11:05:21.991362+00:00 | 21e5943a-c3f5-424d-b4f7-acd03c0d6745 | algorythm_pattern_prior_pilot_v2_generic/generic_prior/rep-2 | d53bcdc232f7 | ok | results/scientific-rerun-16384/raw/algorythm_pattern_prior_pilot_v2_generic/20260912T105822Z-G-clean/21e5943a-c3f5-424d-b4f7-acd03c0d6745.json | - |
| 2026-09-12T11:06:49.106263+00:00 | 71a8738e-73dd-44d7-bdd9-812e7f746cf6 | algorythm_pattern_prior_pilot_v2_generic/generic_prior/rep-3 | d53bcdc232f7 | ok | results/scientific-rerun-16384/raw/algorythm_pattern_prior_pilot_v2_generic/20260912T105822Z-G-clean/71a8738e-73dd-44d7-bdd9-812e7f746cf6.json | - |
| 2026-09-12T11:08:43.902030+00:00 | 6b954fda-489f-49ae-a6d5-8d20eead1e95 | algorythm_pattern_prior_pilot_v2_generic/no_prior/rep-3 | d53bcdc232f7 | ok | results/scientific-rerun-16384/raw/algorythm_pattern_prior_pilot_v2_generic/20260912T105822Z-G-clean/6b954fda-489f-49ae-a6d5-8d20eead1e95.json | - |
| 2026-09-12T11:09:52.026676+00:00 | c80dd06e-4902-4def-9b25-5f837c6f8d0f | algorythm_pattern_prior_pilot_v2_generic/no_prior/rep-4 | d53bcdc232f7 | ok | results/scientific-rerun-16384/raw/algorythm_pattern_prior_pilot_v2_generic/20260912T105822Z-G-clean/c80dd06e-4902-4def-9b25-5f837c6f8d0f.json | - |
| 2026-09-12T11:11:27.476073+00:00 | 1bf082dd-f929-4d5f-92d4-4cdd31eb93a2 | algorythm_pattern_prior_pilot_v2_generic/generic_prior/rep-4 | d53bcdc232f7 | ok | results/scientific-rerun-16384/raw/algorythm_pattern_prior_pilot_v2_generic/20260912T105822Z-G-clean/1bf082dd-f929-4d5f-92d4-4cdd31eb93a2.json | - |
| 2026-09-12T11:12:43.899118+00:00 | 7f1be757-0475-4703-8889-9089758e7a6b | algorythm_pattern_prior_pilot_v2_generic/generic_prior/rep-5 | d53bcdc232f7 | ok | results/scientific-rerun-16384/raw/algorythm_pattern_prior_pilot_v2_generic/20260912T105822Z-G-clean/7f1be757-0475-4703-8889-9089758e7a6b.json | - |
| 2026-09-12T11:15:00.552551+00:00 | ddc35ac9-5c0c-4386-a332-27a62ab12479 | algorythm_pattern_prior_pilot_v2_generic/no_prior/rep-5 | d53bcdc232f7 | ok | results/scientific-rerun-16384/raw/algorythm_pattern_prior_pilot_v2_generic/20260912T105822Z-G-clean/ddc35ac9-5c0c-4386-a332-27a62ab12479.json | - |
| 2026-09-12T11:16:04.732602+00:00 | a6ff2d87-afcc-4d6a-ad1b-fbcaed57cef4 | algorythm_pattern_prior_pilot_v2_generic/no_prior/rep-1 | d53bcdc232f7 | ok | results/scientific-rerun-16384/raw/algorythm_pattern_prior_pilot_v2_generic/20260912T105822Z-G-clean/a6ff2d87-afcc-4d6a-ad1b-fbcaed57cef4.json | - |
| 2026-09-12T11:18:37.782528+00:00 | aeafcf59-3092-4c3b-bb4a-b238e83d3dd8 | algorythm_pattern_prior_pilot_v2_generic/generic_prior/rep-1 | d53bcdc232f7 | ok | results/scientific-rerun-16384/raw/algorythm_pattern_prior_pilot_v2_generic/20260912T105822Z-G-clean/aeafcf59-3092-4c3b-bb4a-b238e83d3dd8.json | - |
| 2026-09-12T11:18:56.910026+00:00 | 3ae6cb55-9426-4767-91e4-300ae7015fce | algorythm_pattern_prior_pilot_v2_generic/generic_prior/rep-2 | d53bcdc232f7 | ok | results/scientific-rerun-16384/raw/algorythm_pattern_prior_pilot_v2_generic/20260912T105822Z-G-clean/3ae6cb55-9426-4767-91e4-300ae7015fce.json | - |
| 2026-09-12T11:19:18.984038+00:00 | ca25fc42-973f-48b0-a965-1d001729d51b | algorythm_pattern_prior_pilot_v2_generic/no_prior/rep-2 | d53bcdc232f7 | ok | results/scientific-rerun-16384/raw/algorythm_pattern_prior_pilot_v2_generic/20260912T105822Z-G-clean/ca25fc42-973f-48b0-a965-1d001729d51b.json | - |
| 2026-09-12T11:20:36.838643+00:00 | d5d4e85e-c827-4b9c-9944-7fdd4899db06 | algorythm_pattern_prior_pilot_v2_generic/no_prior/rep-3 | d53bcdc232f7 | ok | results/scientific-rerun-16384/raw/algorythm_pattern_prior_pilot_v2_generic/20260912T105822Z-G-clean/d5d4e85e-c827-4b9c-9944-7fdd4899db06.json | - |
| 2026-09-12T11:21:17.975830+00:00 | 3e78c511-deea-4e4a-8ef4-bf1ba8423ecc | algorythm_pattern_prior_pilot_v2_generic/generic_prior/rep-3 | d53bcdc232f7 | ok | results/scientific-rerun-16384/raw/algorythm_pattern_prior_pilot_v2_generic/20260912T105822Z-G-clean/3e78c511-deea-4e4a-8ef4-bf1ba8423ecc.json | - |
| 2026-09-12T11:22:21.361549+00:00 | 557b9a43-7ad5-46c9-8301-5f5738f2efeb | algorythm_pattern_prior_pilot_v2_generic/generic_prior/rep-4 | d53bcdc232f7 | ok | results/scientific-rerun-16384/raw/algorythm_pattern_prior_pilot_v2_generic/20260912T105822Z-G-clean/557b9a43-7ad5-46c9-8301-5f5738f2efeb.json | - |
| 2026-09-12T11:25:18.106696+00:00 | 3d75cf85-f2d8-464c-b41e-9c1a4f979e07 | algorythm_pattern_prior_pilot_v2_generic/no_prior/rep-4 | d53bcdc232f7 | provider_failure | results/scientific-rerun-16384/raw/algorythm_pattern_prior_pilot_v2_generic/20260912T105822Z-G-clean/3d75cf85-f2d8-464c-b41e-9c1a4f979e07.json | MissingCompletionContent |

Session 20260912T105822Z-G-clean VOID: provider_failure rate >5% within first 50 calls; session is void. Do not resume; document a corrected freeze.

Clean scientific rerun finalized VOID: Session G stopped after call 18. The
first 17 calls completed; call 18 returned HTTP 200 with exact model/provider
identity but `content=null`, `finish_reason=length`, 16,384 output tokens, and
16,383 reasoning tokens. The first-50 provider-failure rate was 1/18 (5.56%),
so the frozen health rule invalidated the session. No retry occurred; Session P
and all analyses were not run. Total usage was 19,221 input, 152,365 output,
149,590 reasoning, and 171,586 total tokens; actual OpenRouter cost was
US$0.07752965. Evidence: `pilot/v2/CLEAN_SCIENTIFIC_RERUN_STATUS.md` and
`results/scientific-rerun-16384/`.
| 2026-09-12T12:29:07.155686+00:00 | 5865c108-51ef-405e-bb63-f43ce4f7f288 | stress_smoke_32768_G/A_G/rep-1 | f9a6ef86af7a | ok | results/stress-smoke-32768/20260912T122827Z/raw/5865c108-51ef-405e-bb63-f43ce4f7f288.json | - |
| 2026-09-12T12:29:50.449541+00:00 | 73d371ba-e9ba-4269-8464-7377dafc59b2 | stress_smoke_32768_G/B/rep-1 | f9a6ef86af7a | ok | results/stress-smoke-32768/20260912T122827Z/raw/73d371ba-e9ba-4269-8464-7377dafc59b2.json | - |
| 2026-09-12T12:30:55.771216+00:00 | 37a138fc-0340-47ae-b467-25955eede4bc | stress_smoke_32768_G/A_G/rep-2 | f9a6ef86af7a | ok | results/stress-smoke-32768/20260912T122827Z/raw/37a138fc-0340-47ae-b467-25955eede4bc.json | - |
| 2026-09-12T12:31:29.143644+00:00 | f506ac39-ca24-47bc-bb75-4751bd185140 | stress_smoke_32768_G/B/rep-2 | f9a6ef86af7a | ok | results/stress-smoke-32768/20260912T122827Z/raw/f506ac39-ca24-47bc-bb75-4751bd185140.json | - |
| 2026-09-12T12:32:50.913356+00:00 | d0ee6960-d693-41cd-888e-5ea8f76c641b | stress_smoke_32768_G/A_G/rep-3 | f9a6ef86af7a | ok | results/stress-smoke-32768/20260912T122827Z/raw/d0ee6960-d693-41cd-888e-5ea8f76c641b.json | - |
| 2026-09-12T12:33:45.857718+00:00 | 260cf5a6-6c1a-4046-a2d9-cf6dc67bcb42 | stress_smoke_32768_G/B/rep-3 | f9a6ef86af7a | ok | results/stress-smoke-32768/20260912T122827Z/raw/260cf5a6-6c1a-4046-a2d9-cf6dc67bcb42.json | - |
| 2026-09-12T12:34:19.496384+00:00 | 62910646-521c-4eb8-a30e-dd4c4b8e58aa | stress_smoke_32768_G/A_G/rep-4 | f9a6ef86af7a | ok | results/stress-smoke-32768/20260912T122827Z/raw/62910646-521c-4eb8-a30e-dd4c4b8e58aa.json | - |
| 2026-09-12T12:35:17.203351+00:00 | a16c35a6-6aaa-470d-a03c-370c433dd0d4 | stress_smoke_32768_G/B/rep-4 | f9a6ef86af7a | ok | results/stress-smoke-32768/20260912T122827Z/raw/a16c35a6-6aaa-470d-a03c-370c433dd0d4.json | - |
| 2026-09-12T12:36:05.256701+00:00 | ae81b1dd-71f1-4679-ad0c-47a2db84edf5 | stress_smoke_32768_G/A_G/rep-5 | f9a6ef86af7a | ok | results/stress-smoke-32768/20260912T122827Z/raw/ae81b1dd-71f1-4679-ad0c-47a2db84edf5.json | - |
| 2026-09-12T12:37:11.156699+00:00 | e821d91f-a0bb-4738-acfb-51276330c4b0 | stress_smoke_32768_G/B/rep-5 | f9a6ef86af7a | ok | results/stress-smoke-32768/20260912T122827Z/raw/e821d91f-a0bb-4738-acfb-51276330c4b0.json | - |
| 2026-09-12T12:37:31.439956+00:00 | 1f80a636-9dcf-45b8-a486-412bef05cc6c | stress_smoke_32768_G/A_G/rep-1 | f9a6ef86af7a | ok | results/stress-smoke-32768/20260912T122827Z/raw/1f80a636-9dcf-45b8-a486-412bef05cc6c.json | - |
| 2026-09-12T12:37:50.543108+00:00 | a303c8ce-e9d4-4bb8-add7-21764dbd27f9 | stress_smoke_32768_G/B/rep-1 | f9a6ef86af7a | ok | results/stress-smoke-32768/20260912T122827Z/raw/a303c8ce-e9d4-4bb8-add7-21764dbd27f9.json | - |
| 2026-09-12T12:38:14.543748+00:00 | 869bd66f-9c2c-40a1-b085-46e91591a494 | stress_smoke_32768_G/A_G/rep-2 | f9a6ef86af7a | ok | results/stress-smoke-32768/20260912T122827Z/raw/869bd66f-9c2c-40a1-b085-46e91591a494.json | - |
| 2026-09-12T12:38:28.361553+00:00 | a25441b1-bfc9-48d9-9334-2b3ed61bd82b | stress_smoke_32768_G/B/rep-2 | f9a6ef86af7a | ok | results/stress-smoke-32768/20260912T122827Z/raw/a25441b1-bfc9-48d9-9334-2b3ed61bd82b.json | - |
| 2026-09-12T12:38:46.308740+00:00 | a0af4e70-a7bd-4bec-8ecc-3396e4def021 | stress_smoke_32768_G/A_G/rep-3 | f9a6ef86af7a | ok | results/stress-smoke-32768/20260912T122827Z/raw/a0af4e70-a7bd-4bec-8ecc-3396e4def021.json | - |
| 2026-09-12T12:39:06.774550+00:00 | 105ea27e-d50c-4310-8c7d-a8b6531cba11 | stress_smoke_32768_G/B/rep-3 | f9a6ef86af7a | ok | results/stress-smoke-32768/20260912T122827Z/raw/105ea27e-d50c-4310-8c7d-a8b6531cba11.json | - |
| 2026-09-12T12:39:30.211778+00:00 | 67014e20-d00e-4a65-9a4f-092ddcf3d6a7 | stress_smoke_32768_G/A_G/rep-4 | f9a6ef86af7a | ok | results/stress-smoke-32768/20260912T122827Z/raw/67014e20-d00e-4a65-9a4f-092ddcf3d6a7.json | - |
| 2026-09-12T12:39:48.582867+00:00 | ee7313e4-680d-429b-8fe2-84acabc07ef0 | stress_smoke_32768_G/B/rep-4 | f9a6ef86af7a | ok | results/stress-smoke-32768/20260912T122827Z/raw/ee7313e4-680d-429b-8fe2-84acabc07ef0.json | - |
| 2026-09-12T12:40:09.045403+00:00 | 93029576-25a4-4d95-9b20-fef4c533de9f | stress_smoke_32768_G/A_G/rep-5 | f9a6ef86af7a | ok | results/stress-smoke-32768/20260912T122827Z/raw/93029576-25a4-4d95-9b20-fef4c533de9f.json | - |
| 2026-09-12T12:40:30.657740+00:00 | 2a5df396-44ba-4d0b-96ca-7dccb50960fd | stress_smoke_32768_G/B/rep-5 | f9a6ef86af7a | ok | results/stress-smoke-32768/20260912T122827Z/raw/2a5df396-44ba-4d0b-96ca-7dccb50960fd.json | - |
| 2026-09-12T12:41:27.404774+00:00 | d452042f-81bc-475f-bf92-25a910dd8689 | stress_smoke_32768_G/A_G/rep-1 | f9a6ef86af7a | ok | results/stress-smoke-32768/20260912T122827Z/raw/d452042f-81bc-475f-bf92-25a910dd8689.json | - |
| 2026-09-12T12:42:16.004410+00:00 | e5fccf3c-eb62-488c-81b9-3b0e158f79a0 | stress_smoke_32768_G/B/rep-1 | f9a6ef86af7a | ok | results/stress-smoke-32768/20260912T122827Z/raw/e5fccf3c-eb62-488c-81b9-3b0e158f79a0.json | - |
| 2026-09-12T12:43:09.343024+00:00 | 37f5b443-7e08-4a82-8c99-73dafd8a30a7 | stress_smoke_32768_G/A_G/rep-2 | f9a6ef86af7a | ok | results/stress-smoke-32768/20260912T122827Z/raw/37f5b443-7e08-4a82-8c99-73dafd8a30a7.json | - |
| 2026-09-12T12:45:04.601273+00:00 | a969a697-7978-473c-a669-5ee434a05ec8 | stress_smoke_32768_G/B/rep-2 | f9a6ef86af7a | ok | results/stress-smoke-32768/20260912T122827Z/raw/a969a697-7978-473c-a669-5ee434a05ec8.json | - |
| 2026-09-12T12:45:55.022552+00:00 | 1c8af59d-4b21-4ac0-9c22-14cb83a4a5f1 | stress_smoke_32768_G/A_G/rep-3 | f9a6ef86af7a | ok | results/stress-smoke-32768/20260912T122827Z/raw/1c8af59d-4b21-4ac0-9c22-14cb83a4a5f1.json | - |
| 2026-09-12T12:46:47.133483+00:00 | 7a2e523e-4f5c-4a69-8ff9-9c0ad2a6ea86 | stress_smoke_32768_G/B/rep-3 | f9a6ef86af7a | ok | results/stress-smoke-32768/20260912T122827Z/raw/7a2e523e-4f5c-4a69-8ff9-9c0ad2a6ea86.json | - |
| 2026-09-12T12:47:31.693111+00:00 | 4235c41c-89e4-47da-8118-a8909f3646d2 | stress_smoke_32768_G/A_G/rep-4 | f9a6ef86af7a | ok | results/stress-smoke-32768/20260912T122827Z/raw/4235c41c-89e4-47da-8118-a8909f3646d2.json | - |
| 2026-09-12T12:48:39.109752+00:00 | 8a42fe5f-3de6-4efb-9ec7-dfe45f4de310 | stress_smoke_32768_G/B/rep-4 | f9a6ef86af7a | ok | results/stress-smoke-32768/20260912T122827Z/raw/8a42fe5f-3de6-4efb-9ec7-dfe45f4de310.json | - |
| 2026-09-12T12:49:32.128602+00:00 | f011c63f-91b8-431e-bc4c-e7a8c13add38 | stress_smoke_32768_G/A_G/rep-5 | f9a6ef86af7a | ok | results/stress-smoke-32768/20260912T122827Z/raw/f011c63f-91b8-431e-bc4c-e7a8c13add38.json | - |
| 2026-09-12T12:50:35.214687+00:00 | 4876414f-8ca9-467b-a96b-274affc330aa | stress_smoke_32768_G/B/rep-5 | f9a6ef86af7a | ok | results/stress-smoke-32768/20260912T122827Z/raw/4876414f-8ca9-467b-a96b-274affc330aa.json | - |
| 2026-09-12T12:51:04.529904+00:00 | a32ec587-47ed-45aa-aa47-173743ae9159 | stress_smoke_32768_P/A_P/rep-1 | f9a6ef86af7a | ok | results/stress-smoke-32768/20260912T122827Z/raw/a32ec587-47ed-45aa-aa47-173743ae9159.json | - |
| 2026-09-12T12:51:54.465335+00:00 | 1e02308d-c812-4b35-959e-b7fc44c61d85 | stress_smoke_32768_P/C/rep-1 | f9a6ef86af7a | ok | results/stress-smoke-32768/20260912T122827Z/raw/1e02308d-c812-4b35-959e-b7fc44c61d85.json | - |
| 2026-09-12T12:52:36.343613+00:00 | 522e4234-a9b7-46e4-8275-79edb91ac87b | stress_smoke_32768_P/A_P/rep-2 | f9a6ef86af7a | ok | results/stress-smoke-32768/20260912T122827Z/raw/522e4234-a9b7-46e4-8275-79edb91ac87b.json | - |
| 2026-09-12T12:53:09.933585+00:00 | 3d0a1c7b-ad56-4297-9af3-2bfbfee27683 | stress_smoke_32768_P/C/rep-2 | f9a6ef86af7a | ok | results/stress-smoke-32768/20260912T122827Z/raw/3d0a1c7b-ad56-4297-9af3-2bfbfee27683.json | - |
| 2026-09-12T12:53:41.677818+00:00 | 6387e68e-7b51-45aa-b820-b91a1d2d4291 | stress_smoke_32768_P/A_P/rep-3 | f9a6ef86af7a | ok | results/stress-smoke-32768/20260912T122827Z/raw/6387e68e-7b51-45aa-b820-b91a1d2d4291.json | - |
| 2026-09-12T12:54:24.083185+00:00 | 0b777dd4-a9a5-4747-b412-5c4a7aa4ebca | stress_smoke_32768_P/C/rep-3 | f9a6ef86af7a | ok | results/stress-smoke-32768/20260912T122827Z/raw/0b777dd4-a9a5-4747-b412-5c4a7aa4ebca.json | - |
| 2026-09-12T12:55:20.291238+00:00 | 78a15955-4905-4b8d-8467-9ff386ca1be5 | stress_smoke_32768_P/A_P/rep-4 | f9a6ef86af7a | ok | results/stress-smoke-32768/20260912T122827Z/raw/78a15955-4905-4b8d-8467-9ff386ca1be5.json | - |
| 2026-09-12T12:56:09.240085+00:00 | d1aa41f1-9a29-4bc6-bf90-f63df05c61b3 | stress_smoke_32768_P/C/rep-4 | f9a6ef86af7a | ok | results/stress-smoke-32768/20260912T122827Z/raw/d1aa41f1-9a29-4bc6-bf90-f63df05c61b3.json | - |
| 2026-09-12T12:56:57.676396+00:00 | c39bb1e0-3450-4970-a001-a1510f1c6397 | stress_smoke_32768_P/A_P/rep-5 | f9a6ef86af7a | ok | results/stress-smoke-32768/20260912T122827Z/raw/c39bb1e0-3450-4970-a001-a1510f1c6397.json | - |
| 2026-09-12T12:57:53.635594+00:00 | bfca09e5-66e6-4d67-89fc-8211d6358ae6 | stress_smoke_32768_P/C/rep-5 | f9a6ef86af7a | ok | results/stress-smoke-32768/20260912T122827Z/raw/bfca09e5-66e6-4d67-89fc-8211d6358ae6.json | - |
| 2026-09-12T12:58:06.759535+00:00 | 8f9e8cea-5b2a-4bc0-96ad-efd1d4dc3d3c | stress_smoke_32768_P/A_P/rep-1 | f9a6ef86af7a | ok | results/stress-smoke-32768/20260912T122827Z/raw/8f9e8cea-5b2a-4bc0-96ad-efd1d4dc3d3c.json | - |
| 2026-09-12T12:58:34.646846+00:00 | 61a794b6-ab4c-4a8c-9fe1-c707a770fc3a | stress_smoke_32768_P/C/rep-1 | f9a6ef86af7a | ok | results/stress-smoke-32768/20260912T122827Z/raw/61a794b6-ab4c-4a8c-9fe1-c707a770fc3a.json | - |
| 2026-09-12T12:58:53.992551+00:00 | 9fcf6ba2-4340-460f-9ab9-c632ec3ce0b4 | stress_smoke_32768_P/A_P/rep-2 | f9a6ef86af7a | ok | results/stress-smoke-32768/20260912T122827Z/raw/9fcf6ba2-4340-460f-9ab9-c632ec3ce0b4.json | - |
| 2026-09-12T12:59:15.140482+00:00 | ca086fef-9c1f-405f-97c9-3096fb9cba55 | stress_smoke_32768_P/C/rep-2 | f9a6ef86af7a | ok | results/stress-smoke-32768/20260912T122827Z/raw/ca086fef-9c1f-405f-97c9-3096fb9cba55.json | - |
| 2026-09-12T12:59:41.788956+00:00 | 1f42cb95-f81c-4dae-92ec-e33f201b043f | stress_smoke_32768_P/A_P/rep-3 | f9a6ef86af7a | ok | results/stress-smoke-32768/20260912T122827Z/raw/1f42cb95-f81c-4dae-92ec-e33f201b043f.json | - |
| 2026-09-12T12:59:57.954119+00:00 | e186bfac-767c-4fca-a067-25592af4f63a | stress_smoke_32768_P/C/rep-3 | f9a6ef86af7a | ok | results/stress-smoke-32768/20260912T122827Z/raw/e186bfac-767c-4fca-a067-25592af4f63a.json | - |
| 2026-09-12T13:00:15.444753+00:00 | 0789b8e8-05c5-4eab-98d2-392f10175076 | stress_smoke_32768_P/A_P/rep-4 | f9a6ef86af7a | ok | results/stress-smoke-32768/20260912T122827Z/raw/0789b8e8-05c5-4eab-98d2-392f10175076.json | - |
| 2026-09-12T13:00:38.220390+00:00 | 7560e8c0-aaeb-4eca-b7fc-2434ac55568c | stress_smoke_32768_P/C/rep-4 | f9a6ef86af7a | ok | results/stress-smoke-32768/20260912T122827Z/raw/7560e8c0-aaeb-4eca-b7fc-2434ac55568c.json | - |
| 2026-09-12T13:00:56.810253+00:00 | f325e001-f464-4cb7-8cf6-79bee2d80e1e | stress_smoke_32768_P/A_P/rep-5 | f9a6ef86af7a | ok | results/stress-smoke-32768/20260912T122827Z/raw/f325e001-f464-4cb7-8cf6-79bee2d80e1e.json | - |
| 2026-09-12T13:01:18.863825+00:00 | 042677d9-e53f-4505-80c8-3aaed6def228 | stress_smoke_32768_P/C/rep-5 | f9a6ef86af7a | ok | results/stress-smoke-32768/20260912T122827Z/raw/042677d9-e53f-4505-80c8-3aaed6def228.json | - |

V2.2 pre-results revalidation 2026-09-12: the registered 32,768-token
synthetic stress run remains PASS after the consensus sample freeze. All 50
retained raw exchanges were independently rechecked: exact model
`z-ai/glm-5.3-flash`, pinned Z.AI endpoint (`z-ai/fp8`), fallbacks disabled,
temperature 0, G-then-P order, non-null content, `finish_reason=stop`, and
parser success. No authoritative v2.2 program ID occurs in the stress
evidence. Maximum output was 10,069 tokens; projected equal-arm 600-call cost
is US$1.0849793 and projected serial runtime is 6.3656019 hours. Scientific
calls in this revalidation: 0. The active model-freeze record now freezes only
the authorized max_tokens change, 16,384 to 32,768, for v2.2.
