# Gate 4 / Gate 5 OpenRouter model-freeze status

**Final status: READY FOR FULL PILOT**

Recorded 2026-09-11T17:53:51.172389+00:00 on `agent/codex-gate7`.
No scientific pilot was authorized or run.

| Item | Result |
|---|---|
| Gate 4 | **PASS** |
| Gate 5 | **PASS** |
| Provider | OpenRouter (`openrouter`) |
| API base | `https://openrouter.ai/api/v1` |
| Exact model requested / returned | `z-ai/glm-5.3-flash` / exact match on all 12 responses |
| Underlying provider | Z.AI, endpoint `z-ai/fp8`; all 12 responses report `Z.AI` |
| Authentication | PASS |
| Smoke calls | 12/12 successful |
| Parser failures | 0 |
| Generation settings | Temperature 0 and max_tokens 4096 accepted on all 12 calls |
| Scientific repetitions / timeout | 5 / 120 seconds |
| Routing | Z.AI endpoint only; fallbacks disabled; supplied parameters required |
| Frozen session order | `G` then `P`: generic-placebo session, then pattern-prior session |
| Estimated full-pilot cost | Approximately **US$1.32** at the output-token cap |
| Scientific calls | 0 |
| Full pilot | **NOT YET AUTHORIZED** |

## Pre-results amendment

The 1,024-token OpenRouter attempt was VOID after its final smoke response ended
at the output limit without usable completion text. The user authorized one
technical amendment before results: `max_tokens` increased from 1,024 to 4,096
because "1024 output tokens caused a valid smoke response to terminate before a
usable completion was produced."

The amendment was committed and pushed as
`99e7c86fe3b77e4d81e0c116a0258110c5252fef` before this smoke began. Provider,
model, Z.AI route, disabled fallbacks, temperature, scientific repetitions,
prompts, priors, dataset, fault lines, sampling, and statistical analysis stayed
unchanged. Earlier VOID attempts remain preserved.

## Gate 4 execution

The fresh registered procedure loaded only the three committed `data/smoke/`
fixtures. It made exactly 12 sequential calls with no automatic retries. Every
request used model `z-ai/glm-5.3-flash`, temperature 0, max_tokens 4096, and the
same OpenRouter routing object:

```json
{
  "only": ["z-ai/fp8"],
  "order": ["z-ai/fp8"],
  "allow_fallbacks": false,
  "require_parameters": true
}
```

All 12 calls returned HTTP 200, non-empty completion text, valid structured JSON,
and parser-valid nonzero rankings. Every response returned exact model identity
`z-ai/glm-5.3-flash`, underlying provider `Z.AI`, and finish reason `stop`.
There were zero parser failures, transport failures, truncations, fallbacks, or
provider-identity mismatches.

The smoke billed 8,939 prompt tokens and 5,801 completion tokens, costing
US$0.00331207. The stored raw and processed records contain only
`smoke-sum`, `smoke-count`, and `smoke-search`; no scientific candidate ID or
scientific call is present.

## Gate 5 execution

Only after Gate 4 passed, the registered code called `secrets.randbits(1)` once.
The observed result was 0, which maps to `G` first. The frozen order is therefore
generic-placebo (`G`) followed by pattern-prior (`P`). The order and method are
written into `MODEL_FREEZE_RECORD.json`.

## Cost estimate

The pinned endpoint price recorded before generation is US$0.15 per million
input tokens and US$0.50 per million output tokens. Offline estimation gives
626,740 input tokens across the frozen 600-call design, or US$0.094011. At the
4,096-token output cap for each call, output cost is US$1.2288, yielding a
planning estimate of **US$1.322811**. This assumes no retries, cache discount,
fees, tax, or price change; actual billed output length may be lower.

## Evidence

- [Authorized amendment](PRE_RESULTS_AMENDMENT_MAX_TOKENS_4096.md)
- [Immutable model freeze](MODEL_FREEZE_RECORD.json)
- [Attempt start and committed amendment SHA](model-freeze-attempts/20260911T175238Z-openrouter-smoke-4096/attempt_start.json)
- [All 12 sanitized HTTP requests and responses](model-freeze-attempts/20260911T175238Z-openrouter-smoke-4096/smoke_http_exchanges.json)
- [Smoke execution summary](model-freeze-attempts/20260911T175238Z-openrouter-smoke-4096/smoke_execution_summary.json)
- [Gate result and one coin flip](model-freeze-attempts/20260911T175238Z-openrouter-smoke-4096/gate4_gate5_result.json)
- [Updated full-pilot cost estimate](model-freeze-attempts/20260911T175238Z-openrouter-smoke-4096/full_pilot_cost_estimate.json)
- [Raw and processed smoke records](../../results/smoke-freeze/20260911T175238631073Z/)
- [Authenticated registry and Z.AI endpoint selection](model-freeze-attempts/20260911T173446Z-openrouter-smoke/provider_metadata.json)
- [Provider routing decision](model-freeze-attempts/20260911T173446Z-openrouter-smoke/routing_decision.json)

The credential and authorization header are absent from every stored artifact.
The full 600-call pilot remains unexecuted and requires separate authorization.
The exact result commit is available with
`git log -1 --format=%H -- pilot/v2/GATE4_GATE5_STATUS.md`.
