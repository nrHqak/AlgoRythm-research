# Final v2.2 scientific pilot status

**Status: VOID**

The final frozen execution began Session G under concurrency amendment commit
`b2a2af0d33c71088356dca42dd53b34dd6c6c4da`. It used the authoritative
`data/manifests/pilot_manifest_v2_2.json`, exact model
`z-ai/glm-5.3-flash`, pinned Z.AI endpoint `z-ai/fp8`, disabled fallbacks,
temperature 0, `max_tokens=32768`, five registered repetitions, and four
workers.

The first concurrent batch submitted exactly four Session G calls. One call
completed and parsed successfully. Three calls exhausted the 32,768-token
completion allowance in internal reasoning, returned `finish_reason=length`
with null content, and were recorded as provider failures. The frozen
first-50 health rule therefore marked Session G VOID immediately after the
batch completed.

| Check | Result |
|---|---:|
| Scientific calls submitted | 4/600 |
| Successful calls | 1 |
| Provider failures | 3 |
| Parser failures | 0 |
| Content-null responses | 3 |
| Length truncations | 3 |
| Model/provider mismatches | 0 |
| Session G calls after first batch | 0 |
| Session P calls | 0 |
| Selective retries | 0 |
| Runtime | 366.981338 seconds |
| Actual cost | US$0.0657428 |

All four responses reported the exact frozen model and underlying provider.
The three truncated calls used 32,768 output tokens each; their reasoning-token
counts were 32,763, 32,766, and 32,763. The successful call used 30,940 output
tokens, including 30,823 reasoning tokens.

No statistical analysis or figure generation was run because neither session
is complete. There is no valid scientific result, and the VOID calls may not
be reused or resumed.
