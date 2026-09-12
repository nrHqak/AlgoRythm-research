# 16,384-token stress-smoke status

**Status: BLOCKED**

The single registered no-retry attempt used only the synthetic fixture in
`data/smoke-stress/`. It sent no scientific candidate.

Seventeen calls completed successfully with exact model
`z-ai/glm-5.3-flash`, pinned underlying provider Z.AI (`z-ai/fp8`), disabled
fallbacks, temperature 0, max_tokens 16,384, non-null content,
`finish_reason=stop`, and parser success. Call 18, arm C repetition 4, failed
during HTTP response transport with `ChunkedEncodingError`. It produced no
complete provider envelope and therefore is not classified as a
`content=null` response. The call was not retried. Calls 19 and 20 were not
sent.

Across the 17 completed calls, average usage was 2,537.352941 input tokens,
3,929.823529 output tokens, and 3,762.176471 reasoning tokens. Maximum output
was 5,224 tokens. Average observed cost was US$0.002063613529 per completed
call, giving a provisional 600-call projection of US$1.238168118. The
registered cost gate is incomplete because it requires all 20 calls.

The 20/20 acceptance threshold was not met. The amended token allowance is not
cleared for scientific execution, and the scientific pilot must not run.
