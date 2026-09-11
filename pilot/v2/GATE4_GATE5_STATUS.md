# Gate 4 / Gate 5 OpenRouter model-freeze status

**Final status: BLOCKED**

Recorded 2026-09-11T17:43:34.517235+00:00 on `agent/codex-gate7`. The user authorized changing
provider to OpenRouter and exact model to `z-ai/glm-5.3-flash`, with the same
frozen generation settings and smoke procedure. All earlier Gemini attempts
remain preserved. No scientific pilot was authorized or run.

| Item | Result |
|---|---|
| Gate 4 | **BLOCK** — call 12 truncated, with no completion text |
| Gate 5 | **BLOCK** — no session-order coin flip |
| Provider | OpenRouter (`openrouter`) |
| API base | `https://openrouter.ai/api/v1` |
| Exact model requested / returned | `z-ai/glm-5.3-flash` / exact match on all 12 responses |
| Underlying provider | Z.AI, endpoint `z-ai/fp8`; all 12 responses report `Z.AI` |
| Authentication | PASS — authenticated key check HTTP 200 |
| Smoke calls | 12 attempted; 11 successful, 1 provider failure |
| Parser failures | 0; the null final completion was rejected before parsing |
| Generation settings | Temperature 0, max_tokens 1024; unchanged |
| Scientific repetitions / timeout | 5 / 120 seconds; unchanged |
| Routing | One endpoint only; fallbacks disabled; all supplied parameters required |
| Frozen session order | None; zero coin flips |
| Estimated full-pilot cost | Approximately **US$0.40** under the assumptions below |
| Scientific calls | 0 |
| Full pilot | **NOT YET AUTHORIZED** |

## Routing and execution

Before generation, authenticated API checks verified access and the exact model's
registry entry. Selected the model publisher's Z.AI endpoint, which advertises
`temperature` and `max_tokens` support. The recorded endpoint name identifies
`z-ai/glm-5.3-flash-20260826`; the API request retained the exact user-supplied ID.
No immutable model-weights digest is exposed.

The requested provider pin required a transport extension committed as
`ac28ebf8e0c8047905788913a75c7d7d5fcc015d` before live generation. It adds only
`provider.only=["z-ai/fp8"]`, `provider.order=["z-ai/fp8"]`,
`provider.allow_fallbacks=false`, and `provider.require_parameters=true`.
The generation payload otherwise retains the original model/temperature/token
fields and frozen messages. It adds no reasoning setting, JSON-mode parameter,
seed, tool, or alternate model. OpenRouter's controls are documented in the
[provider-routing guide](https://openrouter.ai/docs/guides/routing/provider-selection).

The extension records the returned underlying provider on each response, fails
on missing/mismatched identity, and carries the pin into smoke/main settings and
freeze validation. Provider drift is fatal even after the first 50 main calls.
Offline verification passed **74 tests**, including pin consistency, missing or
changed identity, freeze mismatch, late drift, and HTTP 503 without retries or
coin flips. No scientific configurations, prior text, prompt text, sample, or
statistical analysis code changed.

The existing 12-call smoke procedure used only the original three `data/smoke/`
fixtures, both prompt shapes, and both prior files. Calls 1–11 returned non-empty
valid structured JSON, passed the parser/nonzero-score check, and finished with
`stop`. All model and underlying-provider identities matched.

Call 12 returned HTTP 200 but `finish_reason=length`, `content=null`, 1,024
completion tokens and 1,023 reasoning tokens. The adapter raised
`ValueError: provider completion content must be a string`, so the registered
procedure saved a provider-failure record and marked the session VOID. The full
HTTP response is retained separately, including the truncation metadata and
reasoning-token usage that identify the cause. HTTP 200 alone is not a successful
smoke completion. No token increase, reasoning adjustment, rerun, or provider
switch followed this failure.

No `MODEL_FREEZE_RECORD.json` was created. Gate 5 remains unexecuted because
all 12 smoke calls must pass before the one registered coin flip. Any later retry
or proposed parameter correction must be explicitly instructed and documented;
this task made no such change and scheduled no retry.

## Cost estimate

The pinned endpoint lists US$0.15 per million input tokens and US$0.50 per million
output tokens. Offline character-count estimation of the frozen 600 scientific
prompts gives 626,740 input tokens (characters divided by four, rounded up per
request). No scientific prompt was sent or printed for this calculation.

Estimated input cost is US$0.094011. At 1,024 completion tokens for each of 600
calls, output cost is US$0.3072, giving **US$0.401211**. This is a planning estimate,
not a guaranteed ceiling: input tokenization is approximate, fees/taxes and price
changes are excluded, and no cache discount or retry is assumed. Current smoke
billing does not establish the future scientific output length.

## Evidence

- [Authentication and full model-endpoint registry](model-freeze-attempts/20260911T173446Z-openrouter-smoke/provider_metadata.json).
- [Provider selection before generation](model-freeze-attempts/20260911T173446Z-openrouter-smoke/routing_decision.json).
- [Attempt settings and asset hashes](model-freeze-attempts/20260911T173446Z-openrouter-smoke/attempt_start.json).
- [All 12 exact HTTP payloads/responses](model-freeze-attempts/20260911T173446Z-openrouter-smoke/smoke_http_exchanges.json).
- [Execution summary](model-freeze-attempts/20260911T173446Z-openrouter-smoke/smoke_execution_summary.json).
- [Machine-readable gate result](model-freeze-attempts/20260911T173446Z-openrouter-smoke/gate4_gate5_result.json).
- [Full-pilot cost estimate](model-freeze-attempts/20260911T173446Z-openrouter-smoke/full_pilot_cost_estimate.json).
- [VOID smoke session](../../results/smoke-freeze/20260911T173958167354Z/): original session manifest, raw/processed records, and VOID marker.
- [Execution instructions and transport guards](OPENROUTER_MODEL_FREEZE_RUNBOOK.md).

The key was used only in process memory and supplied through `OPENROUTER_API_KEY`.
No credential or authorization header is retained in these artifacts; the key
check's account response was not stored. Frozen inputs and the committed transport
code remained unchanged throughout the live attempt. The actual raw HTTP evidence
was observed without altering requests or automatic-retry behavior.

The exact result commit is available with
`git log -1 --format=%H -- pilot/v2/GATE4_GATE5_STATUS.md`.
