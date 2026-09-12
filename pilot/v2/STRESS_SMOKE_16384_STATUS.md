# 16,384-token stress-smoke status

**Status: PASS**

## Historical incomplete attempt

The attempt at `results/stress-smoke-16384/20260912T090056Z/` is preserved
unchanged as historical evidence. By explicit user direction it is classified
as **ABORTED / INCOMPLETE DUE TO LOCAL EXECUTION INTERRUPTION**, rather than a
model/provider scientific failure. Its 17 completed calls were not reused.

## Fresh registered attempt

The one fresh attempt at
`results/stress-smoke-16384/20260912T103649Z-fresh/` used only the synthetic
fixture in `data/smoke-stress/`. It sent no ConDefects or other scientific
candidate.

All 20 registered calls completed in frozen G-then-P order: A_G, B, A_P, and C
five times each. Every response reported exact model
`z-ai/glm-5.3-flash`, pinned underlying provider Z.AI (`z-ai/fp8`), disabled
fallbacks, temperature 0, max_tokens 16,384, non-null content,
`finish_reason=stop`, and parser success.

| Check | Result |
|---|---:|
| Calls successful | 20/20 |
| Parser failures | 0 |
| Content-null failures | 0 |
| Length truncations | 0 |
| Transport failures | 0 |
| Model/provider mismatches | 0 |
| Scientific candidates sent | 0 |
| Average input tokens | 2,541.75 |
| Average output tokens | 3,811.55 |
| Average reasoning tokens | 3,641.00 |
| Maximum output tokens | 12,455 |
| Average cost per call | US$0.0020021095 |
| Projected 600-call cost | US$1.2012657 |
| Cost gate | PASS (≤ US$4.50) |

The pre-results max_tokens amendment is validated and frozen. The repository is
ready for a separately authorized clean scientific rerun; no scientific call
was made in this step.
