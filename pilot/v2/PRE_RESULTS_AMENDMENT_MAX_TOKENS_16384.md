# Pre-results technical amendment: max_tokens 16384

**Status:** authorized for validation; stress smoke BLOCKED, so this amendment
is not cleared for a clean scientific rerun.

**Date:** 2026-09-12

**Scope:** model transport/output allowance only

**Supersedes:** `max_tokens = 4096`

**Proposed amended value:** `max_tokens = 16384`

## Reason

The first scientific attempt is VOID. Its first provider response returned
`content=null`, and no usable scientific model output or performance result was
observed or analyzed. The request exhausted the full 4,096-token completion
allowance. Its exact US$0.002204 cost is explained by 1,040 input tokens at
US$0.15/M plus 4,096 completion tokens at US$0.50/M. The same model and pinned
provider had previously exposed 1,023 reasoning tokens in a 1,024-token
`finish_reason=length`, `content=null` smoke response. Together these facts
confirm output-token exhaustion as the technical failure.

This amendment changes only the completion allowance from 4,096 to 16,384. It
is a PRE-RESULTS technical execution change caused solely by confirmed
output-token exhaustion. The decision does not use model localization
performance.

## Values retained unchanged

| Setting | Frozen value |
|---|---|
| Provider | OpenRouter |
| API base | `https://openrouter.ai/api/v1` |
| Model | `z-ai/glm-5.3-flash` |
| Underlying provider | Z.AI, endpoint `z-ai/fp8` |
| Fallbacks | disabled |
| Require supplied parameters | enabled |
| Temperature | 0 |
| Scientific repetitions | 5 |
| Timeout | 120 seconds |
| Scientific manifest | `data/manifests/pilot_manifest_v2_1.json` |
| Session order | G then P |
| Prompts and priors | unchanged committed bytes |
| Dataset, sample membership, and faulty lines | unchanged |
| Sampling and statistical analysis | unchanged |
| Health and failure policy | unchanged |

Before any clean scientific rerun, the amended allowance must pass one fresh
20-call stress smoke using only `data/smoke-stress/`. The run exercises A_G, B,
A_P, and C five times each in frozen G-then-P order. Every response must be
valid and must report the exact model, pinned Z.AI provider, non-null content,
`finish_reason=stop`, and parser success. Any failure blocks the amendment.

After a 20/20 pass, actual observed cost is multiplied by 600. A projection
above US$4.50 blocks the scientific rerun. Passing the stress check and cost
gate authorizes a readiness commit only; it does not execute or authorize any
scientific candidate call.

## Validation outcome

The single no-retry stress attempt on 2026-09-12 stopped after call 18. Calls
1-17 completed and parsed; call 18 failed during response transport with
`ChunkedEncodingError`. No complete response existed for that call, so it was
not a `content=null` response. Because the registered rule requires 20/20, the
stress smoke and amendment validation are BLOCKED. Calls 19-20 were not sent,
and no scientific candidate was sent.
