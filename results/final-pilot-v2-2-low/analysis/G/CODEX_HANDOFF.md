# Codex Pilot Handoff

> Generated from the validated pilot session.

- Exact N: **30 programs**
- Exact model: `z-ai/glm-5.3-flash`
- Provider: `openrouter`
- Temperature: `0.0`
- Max tokens: `32768`
- Repetitions: **5**
- Parser failures: **1**
- Provider failures: **0**
- Exclusions: **0**

## Exact programs

- `31456138`
- `35962547`
- `37067201`
- `39201856`
- `41991860`
- `41991921`
- `43171788`
- `43234248`
- `43438224`
- `44805380`
- `44917428`
- `45289055`
- `45325123`
- `45463729`
- `45545460`
- `45759088`
- `45808089`
- `45895898`
- `45923968`
- `45971969`
- `46169156`
- `46196763`
- `52795863`
- `52796362`
- `52899692`
- `53927639`
- `54010856`
- `54718266`
- `55003503`
- `55029036`

## Top-1/3/5 and EXAM

| metric | condition | hits / total | rate | bootstrap treatment-control 95% CI |
|---|---|---:|---:|---:|
| top1 | no_prior | 66 / 150 | 0.4400 | [-0.1267, 0.0067] |
| top1 | generic_prior | 57 / 150 | 0.3800 | [-0.1267, 0.0067] |
| top3 | no_prior | 80 / 150 | 0.5333 | [-0.1333, 0.0200] |
| top3 | generic_prior | 72 / 150 | 0.4800 | [-0.1333, 0.0200] |
| top5 | no_prior | 85 / 150 | 0.5667 | [-0.1402, 0.0133] |
| top5 | generic_prior | 76 / 150 | 0.5067 | [-0.1402, 0.0133] |

EXAM control mean: **0.4523**; treatment mean: **0.5108**; treatment-control difference: **0.0585**; two-sided Wilcoxon p: **0.148792**; paired rank-biserial: **0.3987**.

Per-repetition exact McNemar discordant counts, p-values, adjusted odds ratios, per-pattern raw counts, and all bootstrap metadata are in `results/pilot_metrics.json`.

## Exclusions and failures

No pre-treatment exclusions.

Parser failures: **1**; provider failures: **0**. The selected parser-failure policy was `count_as_failure`.

## Reproduction

```sh
.venv/bin/python -m experiments.run_pilot --config pilot/v2/config/pilot_v2_generic.yaml --manifest data/manifests/pilot_manifest_v2_2.json --system-prompt pilot/v2/prompts/system_v2.txt --user-template pilot/prompts/control.txt --priors pilot/v2/generic_placebo_prior.json --provider openai_compatible --model z-ai/glm-5.3-flash --temperature 0.0 --max-tokens 32768 --workers 4 --condition-order counterbalanced --timeout 120.0 --output-root results/final-pilot-v2-2-low --experiment-log EXPERIMENT_LOG.md --provider-label openrouter --reasoning-effort low --base-url https://openrouter.ai/api/v1 --repetitions 5 --session-id final-v2-2-low-G-20260913 --model-freeze pilot/v2/MODEL_FREEZE_RECORD.json --openrouter-provider z-ai/fp8 --openrouter-provider-name Z.AI
'/Users/sadibeknurmuhambet/Documents/ChatGPT/Algorythm Research/analysis/run_analysis.py' --config pilot/v2/config/pilot_v2_generic.yaml --manifest data/manifests/pilot_manifest_v2_2.json --session-id final-v2-2-low-G-20260913 --results-root results/final-pilot-v2-2-low --report-root results/final-pilot-v2-2-low/analysis/G --parser-failure-policy count_as_failure
```

## Strongest justified claim

This pilot does not establish a reliable Top-1 improvement: the mean paired delta was -0.060 and its 95% bootstrap interval [-0.127, 0.007] included zero.

## Claims not justified

- Generalization beyond the exact sample, model, prompts, provider, and settings.
- End-to-end improvement from a predicted pattern label unless that arm was separately run.
- A causal explanation that excludes prompt length without a token-matched placebo arm.
- Any benefit hidden by, or inferred after, post-treatment exclusions.
