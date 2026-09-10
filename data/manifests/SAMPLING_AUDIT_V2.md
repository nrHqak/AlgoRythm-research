# SAMPLING_AUDIT_V2: Pilot Manifest v2 Sampling & Verification Audit

**Dataset & Reproducibility Engineering Audit Report**  
**Project:** AlgoRythm — Pattern-Conditioned Fault Localization Research  
**Protocol Phase:** Gate 6 Final Scientific Sample Freeze ($n=30$)  
**Sampling Seed:** `20260910` (Frozen & Immutable)  
**Manifest Version:** 1 (`pilot_manifest_v2.json`, `pilot_manifest_v2.csv`)  
**Timestamp:** 2026-09-10T16:25:57Z  

---

## 1. Executive Summary & Research Gate 6 Status

This audit document certifies the mechanical inventory, ground-truth defect isolation, task deduplication, algorithmic pattern labeling, deterministic stratified sampling, and physical test-suite packaging for the **Pilot v2 Scientific Sample ($n=30$)**.

### Key Milestones Completed:
1. **Mechanical Inventory ($S_1 = 2,864$):** Complete catalog of all Python submissions from ConDefects recorded in `data/manifests/condfects_inventory_v2.csv`.
2. **Ground Truth Freeze ($S_2 = 1,324 \rightarrow S_3 = 1,008$):** Verified single-line defect isolation committed to git (`60ddd8a`) and pushed **prior** to pattern classification under strict double-blinding.
3. **Task Deduplication ($|F| = 566$):** Deterministic task-level deduplication using seed `20260910`, ensuring independent task contexts.
4. **Pattern Stratification:** Identification of top 4 algorithmic classes satisfying the quota threshold ($\ge 7$ candidates per class):
   - `brute_force_implementation` (Quota = 8)
   - `dynamic_programming` (Quota = 8)
   - `graph_traversal_dfs_bfs` (Quota = 7)
   - `binary_search` (Quota = 7)
5. **Deterministic Sample Selection ($n = 30$):** Sampled according to rank order 1..30 with seed `20260910`.
6. **Package & Test Verification:** 30 isolated directories created under `data/raw/<program_id>/` containing `buggy.py`, `fixed.py`, and `tests.json`. All 30 programs dynamically tested against both buggy and fixed code.
7. **Validation & Regression Gate:** Manifest validated via `experiments.validate_manifest` (`valid: true`), and all 65 preflight regression tests passed cleanly via `pytest tests/ -v`.

---

## 2. Dataset Provenance & Upstream Inventory

- **Dataset Name:** ConDefects (Python subset)
- **Upstream Repository:** `https://github.com/appmlk/ConDefects.git`
- **Source Git HEAD Commit:** `43f0834a82c5e3bc4516c079fe7765f63b1a15cd` (2024-06-25, "Update README.md")
- **License:** Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
- **Primary Literature Precedent:**
  - Yang, Mei, & Yang (2025). *An Empirical Study of Mutation-Based Fault Localization for Novice Programs: Python vs. Java*. IJSEKE 35(07).
  - Xu et al. (2025). *Exploring the Potential and Limitations of Large Language Models for Novice Program Fault Localization*. arXiv:2512.03421.
- **Upstream Size:** 2,864 novice Python submissions across 985 AtCoder competitive programming tasks (ABC, ARC, AGC).

---

## 3. Mechanical Inclusion & Exclusion Funnel

The mechanical filtering pipeline systematically pruned unparseable and out-of-bounds programs before any manual or algorithmic evaluation:

```
Total ConDefects Python Submissions: 2,864 (985 unique tasks)
│
├── [Exclude] SyntaxError on buggy or fixed code: 1
│     └── agc061_a / 40898300 (SyntaxError: unmatched ')')
│
├── [Exclude] LOC < 25: 1,474
│     └── Excluded to ensure sufficient algorithmic context for FL
│
└── [Exclude] LOC > 300: 65
      └── Excluded to prevent context window overflow and intractable complexity
│
└── Evaluated Ground-Truth Pool (S2): 1,324 programs (627 unique tasks)
```

---

## 4. Ground-Truth Defect Isolation & Blinding Commitment

The 1,324 candidate programs were evaluated against strict single-line defect criteria using unified diff analysis between `faultyVersion.py` and `correctVersion.py`:

```
Evaluated Pool (S2): 1,324
│
├── [Include] Exact single-line replacement: 1,008
│     └── Exactly 1 hunk, 1 deletion line, 1 addition line (clean 1-to-1 bug fix)
│
├── [Exclude] Multi-hunk diffs: 181
│     └── Multiple independent modification sites across the source
│
├── [Exclude] Multi-line diffs / pure insertions / pure deletions: 130
│     └── Fix spans multiple contiguous lines or consists solely of add/delete
│
└── [Exclude] Non-algorithmic changes: 5
      └── Code modifications unrelated to algorithmic logic (e.g., author comment, unused import)
│
└── Verified Ground-Truth Pool (S3): 1,008 programs (566 unique tasks)
```

### Strict Blinding Affirmation
To guarantee scientific validity and eliminate experimenter bias:
1. The ground truth classifications and exclusion reasons were frozen in `data/manifests/ground_truth_freeze_v2.csv` and committed to Git (commit `60ddd8a`) **before** any pattern classification was performed.
2. The dataset engineer operated in strict isolation from all prior materials:
   - `PATTERN_PRIORS.md` and `pattern_priors.json` were **NEVER** opened, inspected, or referenced.
   - `GENERIC_PLACEBO_PRIOR.md` and `generic_placebo_prior.json` were **NEVER** opened, inspected, or referenced.
   - LLM prompt templates and pipeline prompts were **NEVER** opened, inspected, or referenced.
3. **No candidate program was run through an LLM**, and no model performance data was collected or observed.

---

## 5. Task Deduplication Frame ($|F| = 566$)

To eliminate pseudo-replication (multiple submissions to the same competitive programming problem skewing results), exactly one program per unique `task_id` was selected:

- **Method:** For each unique task in the 1,008 included programs, candidate programs were sorted deterministically by `program_id`.
- **RNG:** Deterministic selection with `random.Random(20260910)`.
- **Result:** 442 duplicate task submissions excluded; 566 unique tasks retained as Frame $F$.

---

## 6. Algorithmic Pattern Labeling & Stratification

Each of the 566 programs in Frame $F$ was classified into its underlying algorithmic pattern using structural AST analysis and problem specifications:

| Algorithmic Class | Count in Frame $F$ | Quota for Pilot ($n=30$) | Included in Pilot? |
|---|:---:|:---:|:---:|
| **`brute_force_implementation`** | **194** | **8** | **YES (Rank 1–8)** |
| **`dynamic_programming`** | **108** | **8** | **YES (Rank 9–16)** |
| **`graph_traversal_dfs_bfs`** | **75** | **7** | **YES (Rank 17–23)** |
| **`binary_search`** | **62** | **7** | **YES (Rank 24–30)** |
| `math_number_theory` | 46 | 0 | No (below top 4) |
| `tree_algorithms` | 28 | 0 | No (below top 4) |
| `greedy_algorithms` | 27 | 0 | No (below top 4) |
| `string_algorithms` | 11 | 0 | No (below top 4) |
| `geometry` | 8 | 0 | No (below top 4) |
| `two_pointers` | 7 | 0 | No (below top 4) |
| **Total** | **566** | **30** | — |

**Selection Rule:** The top 4 algorithmic classes with $\ge 7$ items were selected, with quotas allocated as 8, 8, 7, 7 to total exactly $n = 30$.

---

## 7. Deterministic Pilot Draw

Programs within each selected class in Frame $F$ were sorted by `program_id` and deterministically sampled using seed `20260910`:
- `brute_force_implementation`: Draw 8 of 194.
- `dynamic_programming`: Draw 8 of 108.
- `graph_traversal_dfs_bfs`: Draw 7 of 75.
- `binary_search`: Draw 7 of 62.

Selection ranks 1 through 30 were assigned consecutively to the sampled programs.

---

## 8. Empirical Packaging & Dynamic Test Verification

All 30 sampled programs were packaged into `data/raw/<program_id>/`:
- `buggy.py`: The faulty novice Python code.
- `fixed.py`: The accepted (AC) corrected Python code by the same author.
- `tests.json`: A list of test fixtures `{"input": "...", "expected_output": "..."}`.

### Dynamic Execution Verification:
Every program was executed against its test suite using Python 3.14:
- **100% (30/30) of programs pass all test cases on `fixed.py`**.
- **90% (27/30) of programs have $\ge 1$ passing test and $\ge 1$ failing test on `buggy.py`**, satisfying standard dynamic fault-localization criteria.
- **10% (3/30) of programs (`abc248_d`, `arc140_b`, `agc059_a`) have 0 passing tests on `buggy.py`**:
  - `abc248_d` (Rank 20): Defect is `print(ans)` which outputs a Python list representation `[x, y]` instead of space-separated integers, failing judge exact-string matching across all tests.
  - `arc140_b` (Rank 22): Defect is a leftover debugging print `print(rs)` that outputs an extraneous line before the answer.
  - `agc059_a` (Rank 26): Defect is a leftover debugging print `print(seg)` that outputs an extraneous line before the answer.
  - In all three cases, the defect is localized to a single line, causing 100% test failure on buggy code and 100% test passing on fixed code.

---

## 9. Comprehensive Pilot v2 Program Roster ($n = 30$)

| Rank | Task ID | Program ID | Algorithmic Pattern | LOC | Faulty Line | Test Suite (B_Pass / B_Fail / F_Pass) | Difficulty |
|:---:|:---:|:---:|:---|:---:|:---:|:---:|:---:|
| **01** | `arc157_e` | `39201856` | `brute_force_implementation` | 93 | 34 | 2 (1P / 1F / 2P) | 2877 |
| **02** | `abc266_c` | `45028964` | `brute_force_implementation` | 46 | 40 | 5 (2P / 3F / 5P) | 516 |
| **03** | `arc141_b` | `38039113` | `brute_force_implementation` | 29 | 6 | 5 (4P / 1F / 5P) | 1265 |
| **04** | `arc151_c` | `41930310` | `brute_force_implementation` | 29 | 17 | 6 (5P / 1F / 6P) | 1940 |
| **05** | `abc337_d` | `54495605` | `brute_force_implementation` | 44 | 42 | 6 (5P / 1F / 6P) | 760 |
| **06** | `abc246_d` | `45753152` | `brute_force_implementation` | 29 | 12 | 5 (4P / 1F / 5P) | 1148 |
| **07** | `abc358_g` | `54786893` | `brute_force_implementation` | 28 | 17 | 2 (1P / 1F / 2P) | 1737 |
| **08** | `abc238_d` | `45717530` | `brute_force_implementation` | 30 | 21 | 2 (1P / 1F / 2P) | 921 |
| **09** | `abc285_e` | `48880084` | `dynamic_programming` | 33 | 26 | 3 (2P / 1F / 3P) | 1466 |
| **10** | `abc307_g` | `42981473` | `dynamic_programming` | 25 | 20 | 2 (1P / 1F / 2P) | 2330 |
| **11** | `abc327_e` | `54954766` | `dynamic_programming` | 67 | 51 | 2 (1P / 1F / 2P) | 1227 |
| **12** | `arc128_d` | `26708943` | `dynamic_programming` | 33 | 12 | 2 (1P / 1F / 2P) | 2554 |
| **13** | `abc260_g` | `33361937` | `dynamic_programming` | 61 | 40 | 3 (2P / 1F / 3P) | 2339 |
| **14** | `abc296_h` | `40275095` | `dynamic_programming` | 170 | 115 | 2 (1P / 1F / 2P) | 2822 |
| **15** | `abc299_f` | `40872561` | `dynamic_programming` | 41 | 41 | 3 (2P / 1F / 3P) | 2366 |
| **16** | `abc347_f` | `52760025` | `dynamic_programming` | 142 | 93 | 3 (2P / 1F / 3P) | 2179 |
| **17** | `arc159_a` | `41991860` | `graph_traversal_dfs_bfs` | 29 | 23 | 3 (2P / 1F / 3P) | 698 |
| **18** | `abc247_d` | `46165455` | `graph_traversal_dfs_bfs` | 59 | 57 | 2 (1P / 1F / 2P) | 468 |
| **19** | `abc351_c` | `54968121` | `graph_traversal_dfs_bfs` | 38 | 29 | 3 (2P / 1F / 3P) | 228 |
| **20** | `abc248_d` | `45983434` | `graph_traversal_dfs_bfs` | 33 | 33 | 1 (0P / 1F / 1P) | 793 |
| **21** | `abc355_e` | `54311444` | `graph_traversal_dfs_bfs` | 164 | 121 | 2 (1P / 1F / 2P) | 2299 |
| **22** | `arc140_b` | `40407040` | `graph_traversal_dfs_bfs` | 70 | 25 | 2 (0P / 2F / 2P) | 1092 |
| **23** | `abc317_e` | `52926276` | `graph_traversal_dfs_bfs` | 88 | 70 | 4 (3P / 1F / 4P) | 1085 |
| **24** | `arc149_a` | `43012792` | `binary_search` | 30 | 19 | 3 (2P / 1F / 3P) | 878 |
| **25** | `arc164_a` | `45556032` | `binary_search` | 40 | 31 | 2 (1P / 1F / 2P) | 532 |
| **26** | `agc059_a` | `37116120` | `binary_search` | 132 | 124 | 1 (0P / 1F / 1P) | 1970 |
| **27** | `abc265_d` | `45966660` | `binary_search` | 54 | 43 | 3 (2P / 1F / 3P) | 727 |
| **28** | `arc138_a` | `43171788` | `binary_search` | 25 | 25 | 2 (1P / 1F / 2P) | 837 |
| **29** | `arc134_d` | `36030496` | `binary_search` | 47 | 16 | 2 (1P / 1F / 2P) | 1998 |
| **30** | `arc158_b` | `42045718` | `binary_search` | 25 | 21 | 2 (1P / 1F / 2P) | 1446 |

---

## 10. Manifest Validation & Integrity Checksums

### Verification Output:
```bash
$ .venv/bin/python -m experiments.validate_manifest data/manifests/pilot_manifest_v2.json
{
  "valid": true,
  "manifest_sha256": "40d7f66382611835d9c53aa8eb3495280725175f3e8f4f52b4cae8ee36dd726d",
  "dataset_name": "ConDefects-Python",
  "total_records": 30,
  "included_records": 30,
  "excluded_records": 0,
  "selection_frozen_at": "2026-09-10T16:25:57.314444+00:00"
}
```

### Preflight Test Suite:
```bash
$ .venv/bin/pytest tests/ -v
============================== 65 passed in 8.70s ==============================
```

### Manifest File Hashes:
- `data/manifests/pilot_manifest_v2.json`: `40d7f66382611835d9c53aa8eb3495280725175f3e8f4f52b4cae8ee36dd726d`
- `data/manifests/pilot_manifest_v2.csv`: `f022fa59f0322c3664faeaee7dd2660d5b273d408ebca031d279ca8266205e46`

---

## 11. Compliance & Audit Sign-Off

The sampling, filtering, pattern stratification, and packaging procedures strictly adhered to all scientific, ethical, and engineering constraints set forth in the research charter. Gate 6 is formally **PASSED and FROZEN**.
