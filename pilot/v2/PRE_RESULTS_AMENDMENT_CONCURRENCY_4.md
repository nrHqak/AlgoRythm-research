# Pre-results execution amendment: bounded concurrency 4

**Status:** validated and frozen before any v2.2 scientific result exists.

**Date:** 2026-09-13 (Asia/Atyrau)

**Scope:** execution scheduling only

## Reason

The registered 32,768-token stress test projected approximately 6.37 hours for
600 sequential calls. Before any valid v2.2 scientific result existed, bounded
concurrency of four requests was authorized to reduce wall-clock time without
changing the scientific design.

## Scheduling freeze

- At most four API requests may be active concurrently.
- Concurrency is permitted only within one session.
- Every Session G request must complete and Session G must pass integrity and
  completeness checks before any Session P request begins.
- Each request ID is the SHA-256 of canonical JSON containing only
  `program_id`, scientific arm (`A_G`, `B`, `A_P`, or `C`), and repetition.
- Raw responses are atomically published as immutable files before parsing.
- Result and experiment-log ordering follows the registered call plan, never
  worker completion order.
- Selective retries and resume are prohibited for the scientific execution.

## Values retained unchanged

| Setting | Frozen value |
|---|---|
| Manifest | `data/manifests/pilot_manifest_v2_2.json` |
| Model | `z-ai/glm-5.3-flash` |
| Provider | OpenRouter |
| Underlying provider | Z.AI (`z-ai/fp8`), pinned |
| Fallbacks | disabled |
| Temperature | 0 |
| Max tokens | 32,768 |
| Repetitions | 5 |
| Session order | G then P |
| Conditions | A_G / B / A_P / C |
| Prompts, labels, priors, sample, quotas, seed | unchanged committed bytes |
| Statistical analysis | unchanged committed code and plan |

## Synthetic concurrency preflight

The registered run at
`results/concurrency-preflight-32768/20260912T202632Z-fresh/` used two large
synthetic programs and no scientific candidate. It exercised all four prompt
shapes with five calls each.

| Check | Result |
|---|---:|
| Workers | 4 |
| Valid calls | 20/20 |
| Parser failures | 0 |
| Content-null failures | 0 |
| Length truncations | 0 |
| Provider/model mismatches | 0 |
| Rate-limit failures | 0 |
| Observed throughput | 4.8676688 calls/minute |
| Projected 600-call runtime | 2.0543715 hours |
| Actual preflight cost | US$0.03163337 |

The scheduling amendment passes its pre-results gate and is frozen at four
workers. This amendment does not itself authorize any further change to the
scientific design.
