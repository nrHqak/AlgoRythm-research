# Statistical Analysis Plan (FROZEN v2)

**Status:** frozen 2026-09-10, before any data exists. Every rule below is pre-registered; none may be selected after seeing results.
**Resolves:** `pilot/PRE_RUN_REVIEW.md` **N3** (no rule for combining five per-repetition tests), **N4** (power floor undisclosed), **N5** (EXAM semantics), and authorization Change 4 (observational unit).
**Supersedes:** `pilot/PRE_EXPERIMENT_COMMIT.md` "Primary and secondary analyses" for execution. That file's stopping rules and no-tuning rules remain in force unchanged.

---

## 1. Notation

- Programs `i = 1..30`; repetitions `r = 1..5`.
- Arms: `A_G`, `B` (session G); `A_P`, `C` (session P). See `PILOT_PROTOCOL_V2.md` §2–3.
- `h_X^K(i, r) ∈ {0,1}` — Top-K hit for program `i`, arm `X`, repetition `r`, taken from `analysis/metrics.py::evaluate_record`'s `top1`/`top3`/`top5` fields. Parser failures and provider failures score `0`, per the frozen `count_as_failure` policy.
- `e_X(i, r) ∈ [0,1]` — the `exam` field from the same source; failures score `1.0`.

## 2. The experimental unit is one PROGRAM

**The primary experimental unit is one program, not one LLM invocation.** The five repetitions are repeated measurements of the same unit under the same condition; they are not five independent observations.

**Explicitly prohibited:** pooling 30 × 5 = 150 calls per arm and treating them as n=150. The pooled transition counts that `analysis/run_analysis.py` emits (`topk.*.pooled_transitions`) are for visualization only — Codex's own code labels them "not an independent-sample test," and they may not be used as the basis of any inferential statement.

## 3. Aggregation rule (chosen in advance, one method)

For each program `i` and arm `X`:

```
H_X^K(i) = 1  if  sum_r h_X^K(i, r) >= 3
           0  otherwise
```

**Majority of five.** Chosen because: it yields the binary paired outcome exact McNemar requires; with an odd number of repetitions no tie is possible; it is robust to a single anomalous run; and it introduces no threshold beyond the natural majority. It is equivalent to thresholding the mean hit rate at 0.5, stated in the form that makes the binary outcome explicit.

For EXAM:

```
E_X(i) = mean_r e_X(i, r)
```

which is exactly what `analysis/statistics.py::paired_by_program` already computes.

No other aggregation may be substituted after the fact. If the determinism check (§4) shows all five repetitions agree everywhere, the majority rule is a no-op and this must be stated, not quietly ignored.

## 4. Repetitions, temperature, and what they now mean

v1 froze `--temperature 0` while justifying five repetitions by an averaging precedent that exists to capture stochasticity — two rationales that cancel (`PRE_RUN_REVIEW.md` N2). v2 resolves this **in favour of keeping temperature 0**, and reinterprets the repetitions:

- **Temperature stays 0.** It removes a noise source the pilot has no power to average out at n=30, and it makes the run closer to reproducible for an external reader.
- **The five repetitions are a determinism probe, not an averaging device.** Temperature 0 is not a determinism guarantee (batched serving, MoE routing, and floating-point non-associativity all break it), and some reasoning models ignore the parameter entirely.

**Mandatory reported quantity — the determinism rate:** the fraction of (program, arm) cells in which all five raw responses are byte-identical, and separately, the fraction in which all five Top-1 outcomes agree. If determinism is at or near 100%, then **the effective information content of the pilot is 30 paired observations per comparison, not 150**, and every report must say so.

## 5. Metrics

| Metric | Status | Notes |
|---|---|---|
| **Top-1** | **Primary** | The single pre-registered primary endpoint |
| Top-3, Top-5 | Secondary | Reported without alpha adjustment, labeled secondary |
| **EXAM\*** | Secondary, descriptive | Renamed with an asterisk deliberately: as implemented it is a **censored, line-based** statistic — the denominator is the physical line count (`SAMPLING_PROTOCOL.md` §5) rather than IJSEKE 2025's inspectable statements, and a faulty line absent from the returned ranking is assigned rank = denominator, i.e. exactly 1.0. It is therefore **not comparable to published EXAM values** and may not be presented as if it were. |
| Ranking length | Mandatory diagnostic | Mean entries returned per arm. A material B-vs-C difference means the Top-K comparison is mediated by response length (`PROMPT_DIFF_V2.md` §4.3) and must be reported as such |
| Parser-failure rate | Mandatory diagnostic | Per arm |
| Prompt length | Mandatory diagnostic | Per arm, checked against `GENERIC_PLACEBO_PRIOR.md` §4 |

## 6. Comparisons

### 6.1 Primary — C vs B, Top-1, program level

Exact McNemar on the 30 paired binary outcomes `{(H_C^1(i), H_B^1(i))}`:

- `b` = #{i : H_C = 1, H_B = 0} — pattern-only successes
- `c` = #{i : H_C = 0, H_B = 1} — generic-only successes
- two-sided exact binomial test of `min(b,c) ~ Binomial(b+c, 0.5)`

This is precisely what `analysis/statistics.py::exact_mcnemar` computes; it is reused as-is, passing **B as `control` and C as `treatment`** so its `control_miss_treatment_hit` field means "pattern-only successes."

**This comparison is cross-session and is therefore not produced by `analysis/run_analysis.py`.** It requires one small additive analysis script (an engineering handoff item; it does not modify Codex's pipeline) that:

1. loads both sessions' processed run records;
2. **asserts every invariant in `PILOT_PROTOCOL_V2.md` §3.1** — identical `manifest_hash`, `system_prompt_hash`, `user_template_hash`, per-program `shared_prompt_hash`, `provider`, `model`, `temperature`, `max_tokens`, `repetitions`, `condition_order`, and `engineering_only: false` on both — and **aborts** on any mismatch rather than adjusting for it;
3. asserts condition balance and unique execution keys across the combined set;
4. applies §3's aggregation and computes the tests below.

### 6.2 Null calibration — A_G vs A_P (must be computed and read first)

Identical machinery, applied to the two replicates of arm A. This is the empirical noise floor: any difference here arises from nothing but re-running.

**Pre-declared gate (`PILOT_PROTOCOL_V2.md` §3.3):** let `d_null` and `d_primary` be the discordant-pair counts at Top-1. **If `d_null >= d_primary`, the primary comparison is declared uninterpretable at this sample size**, and is reported that way regardless of its p-value. This rule is fixed now and may not be revised after either quantity is known.

### 6.3 Secondary comparisons

- **A vs C** (within session P) and **A vs B** (within session G) — produced natively by `analysis/run_analysis.py`, plus the program-level aggregation of §3 applied by the same additive script for consistency with the primary. Both must carry the disclosure that arm A is not zero-guidance (`PILOT_PROTOCOL_V2.md` §2).
- **Interval estimates:** program-clustered percentile bootstrap on `mean(H_C − H_B)` and on `mean(E_C − E_B)`, 10,000 iterations, **seed 20260908**, via `analysis/statistics.py::clustered_bootstrap_delta`.
- **EXAM\*:** paired Wilcoxon signed-rank on `{E_C(i) − E_B(i)}`, via `analysis/statistics.py::exam_comparison`.
- **Per-class breakdown:** Top-1 C−B delta within each of the 4 sampled classes (7–8 programs each). Descriptive only — no per-class test is performed or reported as inferential.

### 6.4 Robustness (secondary, reported in full or not at all)

The five per-repetition exact McNemar tests that `analysis/run_analysis.py` emits natively per session are retained as a robustness check. **All five must be reported together; no single repetition's p-value may be quoted on its own**, and none may be selected for emphasis. Under temperature 0 they are expected to be near-identical, which is itself part of the determinism finding.

### 6.5 Multiplicity

One pre-registered primary endpoint (Top-1, C vs B). Everything else is secondary or descriptive and is reported without alpha adjustment, explicitly labeled. No formal correction is applied because the pilot makes no confirmatory claim (`CLAIM_BOUNDARIES_V2.md`); the protection against selective reporting is that this document fixes the full list in advance and requires secondary results to be reported whether or not they are favourable.

## 7. Power, and the pilot's actual statistical job

**The pilot is calibration/exploratory. It is not powered to confirm or refute anything, and it is not intended to.**

The arithmetic is worth stating plainly, because it bounds what any p-value from this design can mean. With exact McNemar on 30 pairs, the minimum attainable two-sided p as a function of the discordant count `d = b + c`, in the best case where every discordant pair favours one arm:

| `d` | 1 | 2 | 3 | 4 | 5 | **6** | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| min p | 1.000 | 0.500 | 0.250 | 0.125 | 0.0625 | **0.031** | 0.016 | 0.008 |

**At least 6 discordant pairs, all favouring one arm, are required for p ≤ 0.05 to be reachable at all**; if even one discordant runs the other way, 9 are needed. A null result is therefore uninformative about the absence of an effect, and must never be reported as evidence of absence.

**What the pilot is actually for** is estimating the discordance rate that sizes the confirmatory study. Report `b`, `c`, `d = b + c`, and `π_d = d / 30` for the C-vs-B comparison, then apply the standard McNemar sizing approximation:

```
n_discordant ≈ (z_{α/2} + z_β)² / (2ψ − 1)²        where ψ = b / (b + c)
N            ≈ n_discordant / π_d
```

Worked example at α = 0.05 two-sided, power 0.80 (`(1.96 + 0.84)² = 7.84`): if the pilot yields ψ = 0.70 and π_d = 0.20, then `n_discordant ≈ 7.84 / 0.16 ≈ 49` and `N ≈ 245`. This replaces the ⚠️-flagged own-derivation estimate of n ≈ 300 in `dossier/05_block5_methodology.md` §5.4 with a data-informed figure — while carrying the caveats that the estimate describes the 4 sampled pattern classes only (`SAMPLING_PROTOCOL.md` §6), a single model, and a single-line-fault sample (`GROUND_TRUTH_PROTOCOL.md` §3).

Because ψ and π_d are themselves estimated from 30 pairs, the resulting `N` is imprecise. Report it as a range using the bootstrap interval on π_d, not as a point value.

## 8. Reporting order (fixed, to prevent narrative reordering after the fact)

1. Run integrity: invariants (§6.1 step 2), parser-failure rates, determinism rate.
2. Null calibration A_G vs A_P and the §6.2 gate verdict.
3. Primary: C vs B at Top-1, with `b`, `c`, `d`, exact p, and bootstrap CI.
4. Secondary: Top-3/Top-5, EXAM\*, A vs C, A vs B.
5. Diagnostics: ranking length, prompt length, per-class deltas.
6. Confirmatory sizing estimate (§7).
7. Claim-boundary check (`CLAIM_BOUNDARIES_V2.md`) applied to every sentence written.
