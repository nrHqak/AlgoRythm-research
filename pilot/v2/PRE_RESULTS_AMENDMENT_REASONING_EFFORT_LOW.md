# Pre-results execution amendment: low reasoning effort

Date: 2026-09-13 (Asia/Atyrau)

Status: **FROZEN after a passing synthetic preflight; no scientific calls were made under this amendment.**

## Classification and scope

This is a **PRE-RESULTS execution amendment**. It changes only the controllable reasoning effort from the model default (`max`) to `low`. It does not change the dataset, sample, labels, prompts, priors, statistical plan, session order, repetitions, model, provider, endpoint pin, token allowance, or concurrency.

The latest scientific attempt remains VOID. Its raw and processed records are preserved as audit evidence, are not retried, and were not used for scientific performance analysis. No valid scientific performance result had been observed before this amendment.

## Reason

> The model's default reasoning behavior consumed essentially the entire
> 32,768-token completion allowance on real scientific-shaped requests,
> preventing a final structured response. Reasoning effort is reduced solely
> to ensure completion reliability and budget feasibility; no valid scientific
> performance result had been observed.

The token allowance is not increased, and the model/provider are not changed.

## Live OpenRouter metadata

OpenRouter metadata was queried before implementing or executing the amendment. The immutable filtered record is `pilot/v2/model-freeze-attempts/20260912T205114Z-openrouter-reasoning-metadata/reasoning_metadata.json` (SHA-256 `7cc3e8aff1013829be87f3a2e343977caa245a1624e24d55da54e72fd96ef73e`).

- model: `z-ai/glm-5.3-flash`
- canonical slug: `z-ai/glm-5.3-flash-20260826`
- supported efforts: `max`, `high`, `low`
- default effort: `max`
- default enabled: `true`
- mandatory: `true`
- supports `max_tokens`: `true`
- selected effort: `low` (explicitly supported and the lowest listed effort)
- pinned endpoint: `Z.AI`, tag `z-ai/fp8`

The request adapter sends the documented nested value `"reasoning": {"effort": "low"}` and retains the requested value in each raw response envelope.

## Frozen execution settings

- manifest: `data/manifests/pilot_manifest_v2_2.json` (unchanged; SHA-256 `9f2db14bd38647e611bed87c72c87f7c934a2c824388751e2969ad4cab9ef8fc`)
- provider: OpenRouter
- model: `z-ai/glm-5.3-flash`
- underlying provider: Z.AI (`z-ai/fp8`), pinned
- fallbacks: disabled
- temperature: `0`
- max tokens: `32768`
- reasoning effort: `low`
- repetitions: `5`
- workers: `4`
- session order: G, then P, with a strict barrier
- conditions: A_G, B, A_P, C
- selective retries: disabled

## Realistic synthetic preflight

The preflight used four non-candidate, explicitly synthetic fixtures representing binary search, brute-force implementation, dynamic programming, and graph traversal. Their registered LOC values were 58, 134, 149, and 89; all four prompt forms covered all four pattern families. The scientific manifest was read only for identifiers and hashes; candidate source files were neither loaded nor sent.

Artifact: `results/reasoning-preflight-low/20260912T205800Z/PASS.json`
SHA-256: `4ba6b160ec5ecf000295ec482cef0c491cd418887cb2088407a8ce9e8b2ab062`

- valid calls: 20/20
- content-null failures: 0
- length truncations: 0
- parser failures: 0
- provider/model mismatches: 0
- rate-limit failures: 0
- average reasoning tokens: 54.25
- maximum reasoning tokens: 301
- average output tokens: 153.30
- average final-content tokens: 99.05
- average cost: US$0.000248016 per call
- projected 600-call cost: US$0.1488096 (gate: no more than US$4.50)
- observed projected 600-call runtime: 832.35 seconds (0.2312 hours)

This passes the registered mechanical and cost gate. It does not constitute scientific evidence and no scientific pilot was started.
