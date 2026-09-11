# Pre-results technical amendment: max_tokens 4096

**Status:** authorized and committed before any scientific candidate call.

**Date:** 2026-09-11

**Scope:** model transport/output allowance only

**Supersedes for the next smoke and both later scientific sessions:**

`max_tokens = 1024`

**New frozen value:** `max_tokens = 4096`

## Reason

> 1024 output tokens caused a valid smoke response to terminate before
> a usable completion was produced.

The evidence is the OpenRouter smoke session
`results/smoke-freeze/20260911T173958167354Z`. Its twelfth request returned
HTTP 200 from the exact requested model and pinned Z.AI provider, but reported
`finish_reason=length`, `content=null`, 1,024 completion tokens, and 1,023
reasoning tokens. The registered preflight procedure rejected the response and
marked the attempt VOID. The first eleven calls completed and parsed successfully.

This amendment is permitted by `MODEL_FREEZE_PROTOCOL.md` §§2–3 and §4.1: the
token limit has a floor of 1,024, may be raised when smoke reveals truncation,
and must then be re-tested in a fresh smoke attempt and used identically in both
scientific sessions. The value may not be lowered after this amendment.

No result from a scientific candidate exists. The decision uses only mechanical
smoke validity, not localization accuracy. No smoke response was used to tune a
prompt, prior, dataset choice, annotation, statistical method, model, provider,
or provider route.

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
| Prompts and priors | unchanged committed bytes |
| Smoke dataset | unchanged `data/smoke/` fixtures |
| Scientific dataset and ground truth | unchanged v2.1 frozen sample |
| Sampling and statistical analysis | unchanged |

The next action is one completely fresh 12-call registered smoke attempt using
`data/smoke/` and `max_tokens=4096`. Any failure blocks Gate 4. Only a clean
12/12 result may create `MODEL_FREEZE_RECORD.json` and perform the single
pre-registered Gate 5 session-order coin flip. The 600 scientific calls remain
unauthorized.
