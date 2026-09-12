# 32,768-token stress-smoke status

**Status: PASS**

The fresh registered stress run at
`results/stress-smoke-32768/20260912T122827Z/` used only three large synthetic
programs. It exercised all four frozen prompt shapes in G-then-P order and
sent no scientific candidate. After the v2.2 consensus sample was frozen, all
retained request and response records were revalidated against the 30
authoritative program IDs; there was no overlap.

Every call reported the exact model `z-ai/glm-5.3-flash`, pinned underlying
provider Z.AI (`z-ai/fp8`), disabled fallbacks, temperature 0, and
`max_tokens=32768`. All 50 responses had non-null content,
`finish_reason=stop`, and parser success.

| Check | Result |
|---|---:|
| Calls successful | 50/50 |
| Parser failures | 0 |
| Content-null failures | 0 |
| Length truncations | 0 |
| Transport failures | 0 |
| Model/provider mismatches | 0 |
| Scientific candidates sent | 0 |
| Average input tokens | 2,369.60 |
| Average output tokens | 3,410.12 |
| P95 output tokens (nearest rank) | 5,939 |
| Maximum output tokens | 10,069 |
| Maximum reasoning tokens | 9,870 |
| Average cost per call | US$0.001863892 |
| Projected 600-call cost (equal-arm) | US$1.0849793 |
| Projected serial runtime (equal-arm) | 6.3656019 hours |
| Cost gate | PASS (<= US$4.50) |

The pre-results `max_tokens=32768` amendment is validated and frozen for the
authoritative v2.2 consensus sample. No v2.2 scientific call was made.
