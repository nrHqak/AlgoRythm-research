# Four-worker concurrency preflight status

**Status: PASS**

The fresh registered preflight
`results/concurrency-preflight-32768/20260912T202632Z-fresh/` completed 20/20
synthetic calls using four workers. All ten Session G calls completed and were
validated before Session P began. The retained plan contains five calls for
each of A_G, B, A_P, and C.

Every response used `z-ai/glm-5.3-flash` through OpenRouter's pinned Z.AI
endpoint (`z-ai/fp8`), with fallbacks disabled, temperature 0, and
`max_tokens=32768`. There were zero parser, content-null, length, identity,
rate-limit, or other provider failures.

Observed wall time was 246.5246 seconds, or 4.8676688 calls/minute. The direct
throughput projection for 600 calls is 7,395.7374 seconds (2.0543715 hours).
Actual preflight cost was US$0.03163337.

No v2.2 scientific candidate was sent. The scientific pilot may begin only
from the separately committed four-worker execution freeze.
