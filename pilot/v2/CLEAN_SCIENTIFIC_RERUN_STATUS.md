# Clean scientific rerun status

**Experiment status: VOID**

The clean scientific rerun began with frozen Session G under commit
`f3fa5347bf33b4d481e11ee5645c659338d854d0`. The session used the exact
committed OpenRouter configuration, model `z-ai/glm-5.3-flash`, pinned Z.AI
endpoint `z-ai/fp8`, disabled fallbacks, temperature 0, max_tokens 16,384,
five repetitions, the v2.1 scientific manifest, and G-then-P session order.

The first 17 calls completed successfully. Call 18 returned HTTP 200 from the
exact requested model and pinned provider, but its complete persisted envelope
contained `content=null`, `finish_reason=length`, 16,384 output tokens, and
16,383 reasoning tokens. The frozen first-50 health rule therefore observed
one provider failure in 18 attempts (5.56%, above 5%) and immediately marked
Session G VOID.

The failed call was not retried. The remaining 282 Session G calls were not
sent, Session P was not started, and no statistical analysis or result figure
was generated. No localization performance result was inspected or reported.

| Execution item | Recorded value |
|---|---:|
| Scientific calls attempted | 18/600 |
| Valid calls | 17 |
| Provider failures | 1 |
| Parser failures | 0 |
| Total input tokens | 19,221 |
| Total output tokens | 152,365 |
| Total reasoning tokens | 149,590 |
| Total tokens | 171,586 |
| Actual OpenRouter cost | US$0.07752965 |

All 18 provider responses retained stable model and underlying-provider
identity. The failure is output-token exhaustion at the frozen 16,384-token
limit. Under the registered policy, the experiment is VOID and is not ready
for scientific review.
