# Pilot Results

> Generated from immutable run records. Percentages are always accompanied by raw counts.

Exact programs: **30**; repetitions: **5**; run records: **300**.

## Top-K

| metric | condition | hits | total | rate |
|---|---|---:|---:|---:|
| top1 | no_prior | 57 | 150 | 0.3800 |
| top1 | pattern_prior | 64 | 150 | 0.4267 |
| top3 | no_prior | 76 | 150 | 0.5067 |
| top3 | pattern_prior | 85 | 150 | 0.5667 |
| top5 | no_prior | 81 | 150 | 0.5400 |
| top5 | pattern_prior | 86 | 150 | 0.5733 |

| metric | paired mean delta | clustered bootstrap 95% CI |
|---|---:|---:|
| top1 | 0.0467 | [-0.0400, 0.1467] |
| top3 | 0.0600 | [-0.0400, 0.1667] |
| top5 | 0.0333 | [-0.0467, 0.1200] |

| metric | repetition | control-only | treatment-only | exact two-sided p | adjusted OR |
|---|---:|---:|---:|---:|---:|
| top1 | 1 | 1 | 4 | 0.375 | 3.0000 |
| top1 | 2 | 4 | 6 | 0.753906 | 1.4444 |
| top1 | 3 | 2 | 4 | 0.6875 | 1.8000 |
| top1 | 4 | 2 | 2 | 1 | 1.0000 |
| top1 | 5 | 4 | 4 | 1 | 1.0000 |
| top3 | 1 | 2 | 4 | 0.6875 | 1.8000 |
| top3 | 2 | 2 | 3 | 1 | 1.4000 |
| top3 | 3 | 4 | 2 | 0.6875 | 0.5556 |
| top3 | 4 | 0 | 5 | 0.0625 | 11.0000 |
| top3 | 5 | 2 | 5 | 0.453125 | 2.2000 |
| top5 | 1 | 2 | 4 | 0.6875 | 1.8000 |
| top5 | 2 | 2 | 2 | 1 | 1.0000 |
| top5 | 3 | 4 | 1 | 0.375 | 0.3333 |
| top5 | 4 | 1 | 5 | 0.21875 | 3.6667 |
| top5 | 5 | 2 | 4 | 0.6875 | 1.8000 |

McNemar tests are reported separately for each repetition to avoid treating stochastic repetitions of one program as independent programs. Bootstrap intervals resample programs and retain repetitions within each resampled cluster.

## EXAM

Control mean: 0.4800; treatment mean: 0.4451; treatment minus control: -0.0349.

## Failures and exclusions

Parser failures: **0**; provider failures: **0**; pre-treatment exclusions: **0**.

## Strongest justified claim

This pilot does not establish a reliable Top-1 improvement: the mean paired delta was 0.047 and its 95% bootstrap interval [-0.040, 0.147] included zero.

## Scope limits

These results do not by themselves establish generalization to other datasets, pattern vocabularies, providers, models, temperatures, prompts, or predicted (non-oracle) labels.
