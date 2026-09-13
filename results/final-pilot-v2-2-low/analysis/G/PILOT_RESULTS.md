# Pilot Results

> Generated from immutable run records. Percentages are always accompanied by raw counts.

Exact programs: **30**; repetitions: **5**; run records: **300**.

## Top-K

| metric | condition | hits | total | rate |
|---|---|---:|---:|---:|
| top1 | no_prior | 66 | 150 | 0.4400 |
| top1 | generic_prior | 57 | 150 | 0.3800 |
| top3 | no_prior | 80 | 150 | 0.5333 |
| top3 | generic_prior | 72 | 150 | 0.4800 |
| top5 | no_prior | 85 | 150 | 0.5667 |
| top5 | generic_prior | 76 | 150 | 0.5067 |

| metric | paired mean delta | clustered bootstrap 95% CI |
|---|---:|---:|
| top1 | -0.0600 | [-0.1267, 0.0067] |
| top3 | -0.0533 | [-0.1333, 0.0200] |
| top5 | -0.0600 | [-0.1402, 0.0133] |

| metric | repetition | control-only | treatment-only | exact two-sided p | adjusted OR |
|---|---:|---:|---:|---:|---:|
| top1 | 1 | 4 | 0 | 0.125 | 0.1111 |
| top1 | 2 | 4 | 0 | 0.125 | 0.1111 |
| top1 | 3 | 3 | 3 | 1 | 1.0000 |
| top1 | 4 | 2 | 2 | 1 | 1.0000 |
| top1 | 5 | 5 | 4 | 1 | 0.8182 |
| top3 | 1 | 5 | 1 | 0.21875 | 0.2727 |
| top3 | 2 | 3 | 0 | 0.25 | 0.1429 |
| top3 | 3 | 3 | 1 | 0.625 | 0.4286 |
| top3 | 4 | 2 | 3 | 1 | 1.4000 |
| top3 | 5 | 3 | 3 | 1 | 1.0000 |
| top5 | 1 | 4 | 1 | 0.375 | 0.3333 |
| top5 | 2 | 2 | 0 | 0.5 | 0.2000 |
| top5 | 3 | 3 | 1 | 0.625 | 0.4286 |
| top5 | 4 | 2 | 2 | 1 | 1.0000 |
| top5 | 5 | 3 | 1 | 0.625 | 0.4286 |

McNemar tests are reported separately for each repetition to avoid treating stochastic repetitions of one program as independent programs. Bootstrap intervals resample programs and retain repetitions within each resampled cluster.

## EXAM

Control mean: 0.4523; treatment mean: 0.5108; treatment minus control: 0.0585.

## Failures and exclusions

Parser failures: **1**; provider failures: **0**; pre-treatment exclusions: **0**.

## Strongest justified claim

This pilot does not establish a reliable Top-1 improvement: the mean paired delta was -0.060 and its 95% bootstrap interval [-0.127, 0.007] included zero.

## Scope limits

These results do not by themselves establish generalization to other datasets, pattern vocabularies, providers, models, temperatures, prompts, or predicted (non-oracle) labels.
