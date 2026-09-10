# SAMPLING_CORRECTION_V2_1: Protocol Deviation Audit & Correction Plan

**Author:** Dataset & Reproducibility Engineer  
**Project:** AlgoRythm — Pattern-Conditioned Fault Localization Research  
**Protocol Phase:** Gate 6 Protocol Correction & Version 2.1 Sample Freeze  
**Timestamp:** 2026-09-10T17:45:00Z  
**Status:** PROTOCOL CORRECTION IN PROGRESS  

---

## 1. Description of the Protocol Deviation

During final preflight verification of the frozen pilot v2 sample ($n=30$), a critical protocol non-conformance was identified regarding **Stage S2 (Mechanical Eligibility Filtering)** as specified in `pilot/v2/SAMPLING_PROTOCOL.md §3`.

### The Specification Requirement (`pilot/v2/SAMPLING_PROTOCOL.md §3`):
> A candidate is eligible only if **all** hold:
> 1. Runs without syntax error under the pinned Python version.
> 2. **At least one passing and at least one failing test** in `tests_path` (Araujo et al. 2016 precondition, `dossier/03_block3_fault_localization.md` §3a). Checked by executing the suite, never by inspection.
> 3. Physical source length ≥ 25 lines and ≤ 300 lines.
> 4. `evaluation_denominator` ≥ 15.
> 5. Single-line fix shape per `GROUND_TRUTH_PROTOCOL.md` §3.

### What Went Wrong in Version 2.0:
In the implementation of the v2 sampling pipeline:
1. Stage S2 mechanical filtering correctly applied the Python 3 syntax validity check and the physical line count bounds ($\text{LOC} \in [25, 300]$), evaluating 1,324 programs and isolating 1,008 single-line defect replacements (S3).
2. However, the requirement of **at least one passing test and at least one failing test on buggy code** was **not executed mechanically across the candidate population prior to task deduplication (S4) and pattern stratification (S6–S8)**.
3. Instead, dynamic test suite execution was deferred to the physical packaging phase (S9) in `scripts/package_final_sample.py`.
4. When test suites were downloaded and executed for the 30 sampled programs, three programs were discovered to fail 100% of judge tests on buggy code:
   - `abc248_d` (submission `45983434`): The defect printed a Python list `print(ans)` instead of space-separated values, causing every judge test to fail exact string matching.
   - `arc140_b` (submission `40407040`): The defect was an extraneous debug statement `print(rs)` executed unconditionally before the final answer.
   - `agc059_a` (submission `37116120`): The defect was an extraneous debug statement `print(seg)` executed unconditionally before the final answer.
5. In `scripts/package_final_sample.py`, these three programs were improperly granted an ad-hoc exemption (`task_id in ("abc248_d", "arc140_b", "agc059_a")`), rationalizing that their single-line fix was valid and that `fixed.py` passed all tests.
6. This exemption directly violated `pilot/v2/SAMPLING_PROTOCOL.md §3` and §8 ("Prohibited: Adjusting a filter threshold after seeing which programs it removes; manual replacements or exemptions").

---

## 2. When It Was Discovered & Impact

- **Discovery Time:** 2026-09-10T16:30Z, immediately following Commit 3 (`e60b5e4`) during Gate 6 post-freeze review.
- **Scientific Impact:** Programs with 0 passing tests on buggy code violate the foundational assumption of dynamic fault localization (SBFL/MBFL/LLM-FL), where spectrum analysis requires both passing executions ($e_p$) and failing executions ($e_f$) to calculate suspiciousness coefficients (Ochiai, Tarantula, DStar). Including programs with 0 passing tests compromises the empirical comparability of the benchmark.
- **Verdict on v2.0 Artifacts:** The manifest `pilot_manifest_v2.json` and its associated sample **cannot be used scientifically** for the main experiment. Gate 6 is marked:
  $$\textbf{BLOCKED — SAMPLE CORRECTION REQUIRED}$$

---

## 3. Strict Blinding & Non-Contamination Affirmations

To maintain absolute scientific integrity, the following guarantees are affirmed under strict reproducibility audit:
1. **Zero LLM Execution:** Not a single candidate program has been sent to any LLM or model API.
2. **Zero Performance Inspection:** No model output, ranking, accuracy, or localization performance has been observed or generated.
3. **Priors & Placebos Unopened:** The dataset engineer has NOT opened, inspected, or referenced `PATTERN_PRIORS.md`, `pattern_priors.json`, `GENERIC_PLACEBO_PRIOR.md`, `generic_placebo_prior.json`, or prompt templates.
4. **Frozen Ground-Truth Line Numbers Preserved:** The line-level ground-truth adjudications in `ground_truth_freeze_v2.csv` (committed in `60ddd8a` before pattern labeling) remain completely frozen and untouched.
5. **Frozen Seed Preserved:** The sampling seed `20260910` remains strictly immutable.
6. **Preservation of v2 History:** All existing v2 artifacts (`pilot_manifest_v2.json`, `pilot_manifest_v2.csv`, `SAMPLING_AUDIT_V2.md`, `ground_truth_freeze_v2.csv`) are preserved without deletion or modification as permanent historical audit evidence.

---

## 4. Exact Correction Procedure (Version 2.1)

The pipeline is re-executed strictly according to `pilot/v2/SAMPLING_PROTOCOL.md`:

1. **Pre-Deduplication Candidate Pool Evaluation:**
   - Take all 1,008 programs meeting the frozen single-line ground-truth criteria from `ground_truth_freeze_v2.csv`.
   - Acquire test cases for the corresponding tasks from the authoritative repository (`atcoder-testcases`).
   - Dynamically execute each candidate's `faultyVersion.py` and `correctVersion.py` on the test suite with strict timeouts.
   - Record `buggy_pass_count`, `buggy_fail_count`, `fixed_pass_count`, `fixed_fail_count`.
   - Apply mechanical filter: eligible $\iff$ (`buggy_pass_count >= 1` AND `buggy_fail_count >= 1` AND `fixed_fail_count == 0`).
   - Record the full audit in `data/manifests/dynamic_test_eligibility_v2_1.csv` with reason `"fails frozen pass/fail precondition"` for rejected programs.

2. **Intersection with Frozen Single-Line Ground Truth:**
   - Intersect the dynamically eligible programs with the frozen ground-truth decisions. No ground-truth line numbers will be altered.

3. **Rebuild Task-Independent Frame ($F_{v2.1}$):**
   - Re-run task deduplication from the dynamically eligible pool using seed `20260910`.
   - Stable deterministic ordering: sort by `program_id`, select using `random.Random(20260910)`.
   - Exactly one program per `task_id`. Record frame size $|F_{v2.1}|$.

4. **Pattern Labeling:**
   - For programs already labeled in v2, reuse the exact frozen pattern label without modification.
   - For newly introduced task representatives in $F_{v2.1}$, label under strict second-blind protocol (unannotated source, no access to faulty lines or priors, using only `pilot/PATTERN_VOCABULARY.md`).
   - Explicitly document which labels were added during v2.1 correction.

5. **Re-Run Class Selection (§6):**
   - Count eligible programs per class in $F_{v2.1}$ ($\ge 7$ threshold).
   - Rank descending, breaking ties by `pilot/PATTERN_VOCABULARY.md` row order.
   - Select top 4 classes, allocating 8, 8, 7, 7.

6. **Re-Run Seeded Final Draw (§7):**
   - Seed `20260910`, draw order 1..30 without replacement.
   - Output `data/manifests/pilot_manifest_v2_1.json` and `pilot_manifest_v2_1.csv`.
   - Set fresh `selection_frozen_at` timestamp and compute manifest SHA-256.

7. **Empirical Verification of Final Sample:**
   - Verify all 30 programs: `buggy_pass >= 1`, `buggy_fail >= 1`, `fixed_fail == 0`, unique `task_id`, LOC in [25, 300], valid single line.
   - Assert: 0 programs with all buggy tests failing; 0 programs with all buggy tests passing.

8. **Audit & Validation:**
   - Write `data/manifests/SAMPLING_AUDIT_V2_1.md` with complete funnel and V2 vs V2.1 diff.
   - Run `python -m experiments.validate_manifest data/manifests/pilot_manifest_v2_1.json`.
   - Run full regression test suite (`pytest tests/ -v`).
   - Produce `data/ANTIGRAVITY_HANDOFF_V2_1.md`.
