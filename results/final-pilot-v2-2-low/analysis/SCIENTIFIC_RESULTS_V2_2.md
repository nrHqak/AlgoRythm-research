# Scientific pilot v2.2 results

## Integrity

The frozen v2.2 pilot completed 600/600 registered calls. Session G produced 299 valid parsed responses and one parser failure; Session P produced 300 valid parsed responses. Provider failures were zero. The preregistered `count_as_failure` policy was applied to the single parser failure. Both sessions passed the frozen integrity rules, and neither contains a `VOID.json` marker.

The scientific manifest, prompts, priors, model, provider pin, temperature, maximum token allowance, reasoning effort, repetitions, concurrency, session order, and statistical analysis were unchanged from pre-results freeze commit `f8c00ffbdf8b3e92df300b743a2057e0ae8e451a`.

## Preregistered program-level comparison

The experimental unit is the program. Each program-level Top-K value is the majority result across its five repetitions.

| Metric | B | C | C − B |
|---|---:|---:|---:|
| Top-1 | 12/30 (40.00%) | 12/30 (40.00%) | 0.00 pp |
| Top-3 | 15/30 (50.00%) | 18/30 (60.00%) | +10.00 pp |
| Top-5 | 16/30 (53.33%) | 19/30 (63.33%) | +10.00 pp |
| EXAM\* (mean; lower is better) | 0.510798 | 0.445055 | −0.065743 |

For the primary Top-1 comparison, exact McNemar p = 1.0. There were six discordant programs: three improved from B miss to C hit (`b=3`) and three changed from B hit to C miss (`c=3`). The program-clustered 10,000-resample bootstrap 95% interval for C − B was [−0.166667, 0.166667].

The result is null: this pilot does not show a Top-1 improvement from the pattern-specific prior. The interval is compatible with effects in either direction and should not be described as evidence of equivalence or absence of effect.

## Null-control calibration

A_G Top-1 was 13/30 (43.33%); A_P Top-1 was 12/30 (40.00%). The A_P − A_G drift was −3.33 percentage points, with five discordant programs and exact McNemar p = 1.0. Because null-control discordance (5) was lower than primary discordance (6), the preregistered interpretability gate passed.

## Per-pattern Top-1 findings

These values are descriptive only.

| Pattern | Programs | C − B Top-1 |
|---|---:|---:|
| binary_search | 7 | 0.00 pp |
| brute_force_implementation | 8 | +25.00 pp |
| dynamic_programming | 8 | −25.00 pp |
| graph_traversal_dfs_bfs | 7 | 0.00 pp |

The equal and opposite descriptive changes for brute-force implementation and dynamic programming cancel in the pooled Top-1 result. The sample is too small for confirmatory per-pattern claims.

## Operational totals

- prompt tokens: 718,300
- completion tokens: 509,495
- reasoning tokens: 429,072
- final-content tokens: 80,423
- prompt plus completion tokens: 1,227,795
- OpenRouter cost: US$0.29696674
- wall-clock runtime: 3,385.523 seconds (56 minutes 25.523 seconds), measured from Session G start through Session P completion and including the integrity barrier

## Registered outputs

- cross-session report: `C_vs_B.json`
- operational summary: `operational_summary.json`
- Session G and P tables: `G/pilot_results.csv`, `P/pilot_results.csv`
- Session G and P metrics: `G/pilot_metrics.json`, `P/pilot_metrics.json`
- Session G and P result reports, adversarial audits, and handoffs
- eight registered PNG figures under `G/figures/` and `P/figures/`
