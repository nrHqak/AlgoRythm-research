# ANTIGRAVITY_HANDOFF_V2_1: Corrected Sample Freeze & Gate 6 Pass

**Role:** Dataset & Reproducibility Engineer  
**Project:** AlgoRythm — Pattern-Conditioned Fault Localization Research  
**Branch:** `agent/antigravity-data-v2`  
**Base Engineering Branch:** `agent/codex-v2-preflight`  
**Base Science Branch:** `agent/claude-science`  
**Timestamp:** 2026-09-10T17:53:00Z  

## Final Verdict:
$$\textbf{GATE 6 PASS — CORRECTED SAMPLE FROZEN}$$

---

## 1. Executive Summary

Research Gate 6 is officially **PASSED AND FROZEN** under Version 2.1.

Following the identification of a protocol deviation in v2.0 (omission of pre-deduplication dynamic pass/fail test filtering, which resulted in 3 programs with 0 passing tests on buggy code), the complete candidate population ($n = 1,008$ single-line ground-truth candidates) was re-evaluated against authentic AtCoder test cases.

### Mandatory Preconditions Achieved:
1. **100% Dynamic Precondition Conformance:** All 30 programs in the frozen v2.1 sample have $\ge 1$ passing test and $\ge 1$ failing test on `buggy.py`, and 100% passing tests on `fixed.py`.
2. **Zero Fail-Only or Pass-Only Programs:**
   - 0 programs with all buggy tests failing.
   - 0 programs with all buggy tests passing.
3. **Authentic Provenance:** All test cases originate from official AtCoder contest archives (`atcoder-testcases` and `atcoder.jp`). Zero synthetic tests or LLM generation.
4. **Frozen Ground-Truth Line Numbers Invariant:** All ground-truth line annotations from `ground_truth_freeze_v2.csv` were preserved intact.
5. **No Model Contamination:** Zero candidate programs were evaluated through any LLM or model endpoint.
6. **Sampling Seed Invariant:** `20260910` used for both task deduplication and within-class draw.

---

## 2. Frozen Artifact Inventory (Version 2.1)

| Artifact Path | Description | Checksum / Size |
|---|---|---|
| `data/manifests/pilot_manifest_v2_1.json` | Authoritative v2.1 Pilot Manifest (Pydantic v2 compliant) | `d53bcdc232f7e4daebca3248e53e060143a32e2638bb99959fda4c0db38e6ca3` |
| `data/manifests/pilot_manifest_v2_1.csv` | Authoritative v2.1 Pilot Manifest (Tabular view) | 30 programs, $8+8+7+7$ |
| `data/manifests/dynamic_test_eligibility_v2_1.csv` | Full Dynamic Pass/Fail Audit for all 1,008 candidates | 1,008 records (303 eligible, 705 excluded) |
| `data/manifests/SAMPLING_AUDIT_V2_1.md` | Comprehensive Sampling Audit & Funnel Report | Complete audit trail |
| `data/manifests/SAMPLING_CORRECTION_V2_1.md` | Protocol Deviation Analysis & Correction Plan | Historical deviation record |
| `data/manifests/pilot_manifest_v2.json` | Preserved Historical v2.0 Manifest | `40d7f66382611835d9c53aa8eb3495280725175f3e8f4f52b4cae8ee36dd726d` |
| `data/manifests/pilot_manifest_v2.csv` | Preserved Historical v2.0 CSV Manifest | Historical audit record |
| `data/manifests/SAMPLING_AUDIT_V2.md` | Preserved Historical v2.0 Audit Report | Historical audit record |
| `data/manifests/ground_truth_freeze_v2.csv` | Preserved Frozen Ground-Truth Adjudications | 1,324 evaluated (1,008 includes) |
| `data/raw/<program_id>/` | Source code (`buggy.py`, `fixed.py`) & tests (`tests.json`) | All 30 v2.1 programs verified |
| `scripts/build_dynamic_test_eligibility_v2_1.py` | Full candidate pool test evaluation script | Reproducibility script |
| `scripts/package_final_sample_v2_1.py` | Final sampling & packaging script for v2.1 | Reproducibility script |

---

## 3. Verification & Validation Summary

### 1. Manifest Validation:
```bash
$ .venv/bin/python -m experiments.validate_manifest data/manifests/pilot_manifest_v2_1.json
{
  "valid": true,
  "manifest_sha256": "d53bcdc232f7e4daebca3248e53e060143a32e2638bb99959fda4c0db38e6ca3",
  "dataset_name": "ConDefects-Python",
  "total_records": 30,
  "included_records": 30,
  "excluded_records": 0,
  "selection_frozen_at": "2026-09-10T17:51:43.488565+00:00"
}
```

### 2. Regression Test Suite:
```bash
$ .venv/bin/pytest tests/ -v
============================== 65 passed in 8.57s ==============================
```

### 3. Dynamic Execution Verification on All 30 Sampled Programs:
- **`buggy.py` test pass count:** Min 2, Max 7 (all $\ge 1$)
- **`buggy.py` test fail count:** Min 1, Max 5 (all $\ge 1$)
- **`fixed.py` test pass count:** Min 3, Max 8 (100% of testcases pass)
- **`fixed.py` test fail count:** Exactly 0 across all 30 programs.

---

## 4. Instructions for Gate 7 (Experiment Execution)

The corrected dataset is formally frozen and ready for main experiment execution:
1. Main experiment runner must load `data/manifests/pilot_manifest_v2_1.json` via `experiments.models.load_manifest`.
2. Model identity freeze (`MODEL_FREEZE_PROTOCOL.md`) must be verified before executing API calls.
3. No further modifications to sample membership or ground-truth lines are permitted.
