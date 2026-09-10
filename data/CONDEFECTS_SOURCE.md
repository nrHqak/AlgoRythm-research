# ConDefects-Python Source Provenance

## 1. Dataset Overview

- **Dataset Name:** ConDefects (Python subset)
- **Primary Research Artifact Repository:** `https://github.com/appmlk/ConDefects.git`
- **Citation/Paper:** 
  - Yang, Mei, & Yang (2025). *An Empirical Study of Mutation-Based Fault Localization for Novice Programs: Python vs. Java*. International Journal of Software Engineering and Knowledge Engineering (IJSEKE), 35(07), DOI: 10.1142/S0218194025500329.
  - Precedent in LLM fault localization: Xu et al. (2025). *Exploring the Potential and Limitations of Large Language Models for Novice Program Fault Localization*. arXiv:2512.03421.
- **Source Platform:** Novice submissions from AtCoder programming contests (ABC, ARC, AGC).

---

## 2. Exact Commits and Versions

- **Cloned/Acquired Repository:** `https://github.com/appmlk/ConDefects.git`
- **Active Repository HEAD Commit:** `43f0834a82c5e3bc4516c079fe7765f63b1a15cd` (Date: 2024-06-25, "Update README.md")
  - Total Python programs: 2,864
  - Total unique tasks with Python programs: 985
  - Time coverage: October 2021 through June 2024
- **Prior Research Release Commit:** `f92adc1308a0d4c98a58a9d949673859ea49d2c2` (Date: 2024-04-24)
  - Total Python programs: 1,625
  - Total unique tasks with Python programs: 526
  - Time coverage: October 2021 through September 2023 (as reported in IJSEKE 2025 and earlier ConDefects paper drafts)
- **Initial Commit:** `4b05fb96a46baacf48be160621121412c795b1de` (Date: 2023-10-11, "Initiate")

---

## 3. Licenses and Legal Compliance

- **Dataset License:** Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
- **Toolkit/Code License:** MIT License (Copyright (c) 2024 appmlk)
- **External Dataset Integrity:** All external dataset files are strictly read-only and preserved without manual edits.

---

## 4. Python Subset Directory Structure

Programs in ConDefects are organized hierarchically by task and language:

```
Code/
  └── <task_id>/                  # e.g., abc221_a, arc136_c, agc061_a
      └── Python/
          └── <program_id>/       # AtCoder submission ID, e.g. 40898300
              ├── faultyVersion.py    # The buggy submission (WA / RE)
              ├── correctVersion.py   # The accepted fix by the same author (AC)
              └── faultLocation.txt   # Author-provided line number annotation
```

### Component Locations:
- **Buggy source:** `Code/<task_id>/Python/<program_id>/faultyVersion.py`
- **Fixed source:** `Code/<task_id>/Python/<program_id>/correctVersion.py`
- **Author fault location:** `Code/<task_id>/Python/<program_id>/faultLocation.txt`
- **Task Metadata:** `date.txt` (task start dates), `difficulty.txt` (task difficulty ratings)

---

## 5. Test Suites and Test Data Structure

- **Origin:** Official AtCoder test cases for the corresponding contest and task.
- **Upstream Archive:** `Test.zip` distributed via OneDrive / Baidu Drive per official ConDefects `README.md`.
- **Mirror Source:** `https://github.com/conlacda/atcoder-testcases.git` (branches keyed by contest name: `abcXXX`, `arcXXX`, `agcXXX`).
- **Structure per task:**
  ```
  <task_id>/
    ├── in/       # Input test files (e.g., example_00, test_01)
    └── out/      # Expected standard output files
  ```
- **Execution model:** Programs read from standard input (`sys.stdin`) and write to standard output (`sys.stdout`). A test passes if the execution completes with returncode 0 and stdout matches the expected output line-by-line (stripping trailing whitespace).

---

## 6. Environment Assumptions

- **Python Runtime:** Python 3.14.3 (pinned virtual environment `.venv`). Solutions are written against standard competitive-programming Python 3 (Python 3.8+ compatibility).
- **External Dependencies:** Solutions rely only on Python standard libraries (`sys`, `collections`, `itertools`, `math`, `heapq`, `bisect`, etc.).
- **Execution Policy:** Execution uses timeout bounds (5.0s per test case) to prevent infinite loops on faulty programs.
