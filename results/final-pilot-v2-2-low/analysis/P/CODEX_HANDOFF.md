# Codex Pilot Handoff

> Generated from the validated pilot session.

- Exact N: **30 programs**
- Exact model: `z-ai/glm-5.3-flash`
- Provider: `openrouter`
- Temperature: `0.0`
- Max tokens: `32768`
- Repetitions: **5**
- Parser failures: **0**
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
| top1 | no_prior | 57 / 150 | 0.3800 | [-0.0400, 0.1467] |
| top1 | pattern_prior | 64 / 150 | 0.4267 | [-0.0400, 0.1467] |
| top3 | no_prior | 76 / 150 | 0.5067 | [-0.0400, 0.1667] |
| top3 | pattern_prior | 85 / 150 | 0.5667 | [-0.0400, 0.1667] |
| top5 | no_prior | 81 / 150 | 0.5400 | [-0.0467, 0.1200] |
| top5 | pattern_prior | 86 / 150 | 0.5733 | [-0.0467, 0.1200] |

EXAM control mean: **0.4800**; treatment mean: **0.4451**; treatment-control difference: **-0.0349**; two-sided Wilcoxon p: **0.214602**; paired rank-biserial: **-0.3529**.

Per-repetition exact McNemar discordant counts, p-values, adjusted odds ratios, per-pattern raw counts, and all bootstrap metadata are in `results/pilot_metrics.json`.

## Exclusions and failures

No pre-treatment exclusions.

Parser failures: **0**; provider failures: **0**. The selected parser-failure policy was `count_as_failure`.

## Reproduction

```sh
.venv/bin/python -m experiments.run_pilot --config pilot/v2/config/pilot_v2_pattern.yaml --manifest data/manifests/pilot_manifest_v2_2.json --system-prompt pilot/v2/prompts/system_v2.txt --user-template pilot/prompts/control.txt --priors pilot/pattern_priors.json --provider openai_compatible --model z-ai/glm-5.3-flash --temperature 0.0 --max-tokens 32768 --workers 4 --condition-order counterbalanced --timeout 120.0 --output-root results/final-pilot-v2-2-low --experiment-log EXPERIMENT_LOG.md --provider-label openrouter --reasoning-effort low --base-url https://openrouter.ai/api/v1 --repetitions 5 --session-id final-v2-2-low-P-20260913 --model-freeze pilot/v2/MODEL_FREEZE_RECORD.json --openrouter-provider z-ai/fp8 --openrouter-provider-name Z.AI
'/Users/sadibeknurmuhambet/Documents/ChatGPT/Algorythm Research/analysis/run_analysis.py' --config pilot/v2/config/pilot_v2_pattern.yaml --manifest data/manifests/pilot_manifest_v2_2.json --session-id final-v2-2-low-P-20260913 --results-root results/final-pilot-v2-2-low --report-root results/final-pilot-v2-2-low/analysis/P --parser-failure-policy count_as_failure
```

## Strongest justified claim

This pilot does not establish a reliable Top-1 improvement: the mean paired delta was 0.047 and its 95% bootstrap interval [-0.040, 0.147] included zero.

## Claims not justified

- Generalization beyond the exact sample, model, prompts, provider, and settings.
- End-to-end improvement from a predicted pattern label unless that arm was separately run.
- A causal explanation that excludes prompt length without a token-matched placebo arm.
- Any benefit hidden by, or inferred after, post-treatment exclusions.
