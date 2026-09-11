# Technical diagnosis of the first scientific VOID attempt

**Scope:** provider execution mechanics only. No scientific model output or
performance result was observed. No candidate was sent again during diagnosis.

## Likely cause

The failed request most likely consumed all 4,096 completion tokens in internal
reasoning before producing final `message.content`.

The scientific failure record retained `content=null` only indirectly through
the adapter exception and recorded no usage object. Its attributable OpenRouter
charge was US$0.002204. At the frozen Z.AI prices, that charge has an exact fit:

`1,040 × US$0.00000015 input + 4,096 × US$0.0000005 output = US$0.002204`

The request contained 4,029 prompt characters, with the repository estimator
predicting 1,008 tokens. An actual 1,040-token prompt is therefore credible.
The endpoint registry recorded no implicit caching support, so there is no
observed cache discount needed to make the arithmetic fit.

The same pinned model/provider had already shown the exact failure signature at
the earlier 1,024-token cap: 1,024 completion tokens, 1,023 reasoning tokens,
`finish_reason=length`, `native_finish_reason=length`, reasoning text present,
and `message.content=null`. That direct response is preserved in the earlier
smoke HTTP evidence. The passing 4,096-token smoke had a maximum of only 1,146
completion tokens, but its fixtures were 5-11 source lines and did not probe the
real sample's prompt-length range or the model's long-reasoning tail.

The failed scientific generation ID cannot be recovered from local evidence.
OpenRouter's generation-metadata API requires that ID; the old adapter discarded
the provider body before the runner could save it. Consequently, the failed
request's finish reason, reasoning text/count, and input/output counts cannot be
read directly after the fact. The conclusion that 4,096 was exhausted is an
evidence-backed inference from the exact billing fit and the prior identical
signature.

## Recommendation

Recommend `max_tokens=16384`, subject to a new explicit pre-results technical
amendment and a passing stress smoke. A 4× increase is preferable to 8,192 here
because the first real request hit 4,096 despite being only 26 source lines, the
600-call run is sensitive to tail events, and one early provider failure voids a
session under the unchanged health rule. This is a recommendation only; the
committed 4,096 setting has not been amended.

No model, provider, underlying provider, dataset, prompt, prior, statistical
plan, session order, or health threshold changed.
