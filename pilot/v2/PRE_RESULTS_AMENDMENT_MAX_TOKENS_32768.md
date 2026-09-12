# Pre-results technical amendment: max_tokens 32768

**Status:** authorized for validation before any new scientific run.

**Date:** 2026-09-12

**Scope:** model transport/output allowance only

**Supersedes:** `max_tokens = 16384`

**Proposed amended value:** `max_tokens = 32768`

## Reason

The clean scientific attempt in Session G is VOID. Its first 17 calls were
mechanically valid. Call 18 returned HTTP 200 from the exact requested model
and pinned provider, but consumed all 16,384 output tokens, of which 16,383
were reported as reasoning tokens, and returned `finish_reason=length` with
`content=null`. The frozen first-50 health rule immediately invalidated the
session. No localization metric or scientific result was inspected, Session P
was not started, and the valid calls will never be reused.

This amendment changes only the completion allowance from 16,384 to 32,768. It
is a PRE-RESULTS technical execution change caused solely by confirmed
output-token exhaustion. It does not use localization performance.

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

Before any new scientific run, the amended allowance must pass one fresh
50-call stress test using only large synthetic fixtures. It must exercise all
four frozen prompt shapes, retain each full response before parsing, and pass
the exact model/provider, parser, content, finish-reason, cost, and runtime
checks. Any failure blocks the amendment.

The live OpenRouter metadata query recorded in
`model-freeze-attempts/20260912T122253Z-openrouter-stress-32768/` reports that
the exact `z-ai/fp8` endpoint supports `reasoning` and `reasoning_effort`.
Reasoning effort remains unspecified and unchanged. No reasoning-control
parameter may be added during this amendment or stress test.

A 50/50 pass must also project no more than US$4.50 for 600 scientific calls.
Passing creates a readiness freeze only; it does not authorize or start a
scientific run.
