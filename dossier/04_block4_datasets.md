# Block 4. Datasets and benchmarks — detailed inventory

Verification legend: **[V]** verified from fetched primary source; **[S]** credible snippets only; **⚠️** unverified.

Context question per dataset: (a) exact size/structure; (b) license/access; (c) prior use; (d) **reuse for the pattern-conditioned localization project vs need for own dataset.**

---

## 4.1 POJ-104 — algorithm-classification benchmark
**[V — see Block 2a for full details]**
- 104 problems × 500 accepted programs = ~52,000 C/C++ solutions from Peking University OJ; introduced by Mou et al. (TBCNN, AAAI 2016).
- Distribution: microsoft/CodeXGLUE (two tasks: clone-detection-POJ-104; Code-classification-POJ104). **Code MIT; data under C-UDA** (research-permissive).
- Prior use: TBCNN, NCC, CodeBERT, UniXcoder, CCT-LM, InvPT, code2vec baselines.
- **Suitability:** good for validating a *problem-level* classifier; NOT labeled by algorithmic pattern; solutions are all-correct (no bugs) → **cannot support localization experiments**. Use as classifier pretraining/auxiliary only.

## 4.2 Codeflaws — APR/FL benchmark from Codeforces
**[V — GitHub codeflaws/codeflaws + ICSE 2017 poster]**
- **3,902 defects** extracted from **7,436 C programs** (buggy–patched pairs), crawled from Codeforces; ~39–40 automatically-derived defect classes (e.g., missing/incorrect guard condition, missing/incorrect function call, small vs big edits).
- Origin: Tan et al. (UCL), "Codeflaws: A Programming Competition Benchmark for Evaluating Automated Program Repair Tools," **ICSE 2017 (poster)**. Download: codeflaws.github.io (codeflaws.tar.gz).
- Prior use: standard APR benchmark (GenProg et al.); now one of the three FL datasets in arXiv:2512.03421.
- **⚠️ Caveat (from the Dec-2025 LLM paper [V]):** suspected **data leakage** — older models outperform newer ones at Top-1 on it; treat results on Codeflaws as leak-contaminated.
- **Suitability:** programs are competition solutions (mostly algorithmic!), with bug+fix diff → **good raw material for pattern-labeled localization after relabeling by algorithmic technique**; C only.

## 4.3 ConDefects — novice-program FL dataset (Java + Python)
**[V — via IJSEKE 2025 full text + GitHub appmlk/ConDefects]**
- From AtCoder submissions (Oct 2021 – Sep 2023). **Java: 1,254 faulty programs / 810 tasks / 2,045 files / avg 259.22 LOC / avg 22.45 functions. Python: 1,625 faulty programs / 985 tasks / 2,864 files / avg 49.03 LOC / avg 2.91 functions.**
- Used (as "Condefects", Java side) in arXiv:2512.03421 (503-program sample; LOC 6–314, avg 33–36; tests 34–43 per program).
- GitHub: appmlk/ConDefects (research artifact).
- **Suitability:** HIGH for localization baselines (novice-like, buggy+fixed, tasks known); **AtCoder tasks map to known algorithm categories** (AtCoder problem metadata exists) → a realistic route to pattern labels via task→technique mapping; per-problem correct reference solutions available on AtCoder.

## 4.4 BugT — leakage-free novice FL dataset
**[V — full text of arXiv:2512.03421]**
- **7,097 C + 22,547 C++ + 10,507 Python = 40,151 programs** from **BuctOJ**, an internal online-judge network of Beijing University of Chemical Technology — **chosen specifically because it cannot have leaked into LLM training data** (internal network).
- 503-program subset used per language in the paper (unified 1,509 across datasets; difficulty binned in 5 levels ×100); ground truth = labeled faulty line.
- Availability: tied to paper's artifact — github.com/**Xucranger/PLofLBFL**; C++ subset used. ⚠️ Whether the full BugT is released vs only the subset must be checked at the repo.
- **Suitability:** gold-standard "clean" evaluation set; but **access may require author contact**, and OJ tasks are course exercises (algorithmic, beginner level) — pattern labeling would again go through task metadata or own annotation.

## 4.5 Defects4J — the industrial FL benchmark (contrast case)
**[V — GitHub rjust/defects4j + Just et al., ISSTA 2014, DOI 10.1145/2610384.2628055]**
- **854 bugs (+10 deprecated)** across 17+ real Java open-source projects; buggy+fixed versions with triggering tests; extensible framework. Prior use: virtually all FL/APR research (e.g., AutoFL: 149/353 [S-cited in 2512.03421]).
- **Suitability: NONE for the project's core claim** — professional code, not novice; no algorithm-pattern labels; include only as a contrast row in Related Work ("why novice code differs"). MSR 2025 paper "Revisiting Defects4J for Fault Localization" documents its ongoing dominance [S].

## 4.6 IntroClass & ManyBugs — student-C-program repair benchmarks
**[S — repairbenchmarks.cs.umass.edu]**
- **IntroClass**: small C programs with real student bugs from intro-course assignments (used in genetic improvement/APR studies since ~2015); **ManyBugs**: 185 defects in 9 larger C programs (non-student). Host: repairbenchmarks.cs.umass.edu.
- **Suitability:** IntroClass is directly novice-flavored; small scale; C; license = academic use (check site); candidate auxiliary set. ⚠️ Exact bug counts to re-verify at host (commonly cited: IntroClass ~1,000+ buggy submissions / ~298 defects [S]).

## 4.7 QuixBugs — small multi-language buggy programs
**[S]**
- ~40 small programs (Python + Java versions) each with a single bug; standard APR testbed (single-line bugs). Origin: Lin et al. 2017 (program-repair.org).
- **Suitability:** tiny; good for smoke tests and worked examples in the paper; not for statistical claims. Several programs ARE classic algorithms (quicksort, BFS, DFS, binary search...) — **actually convenient for hand-verifying pattern-specific failure points!**

## 4.8 Supporting corpora found during research
| Dataset | Size / content | Access | Role for project |
|---|---|---|---|
| **COFO** (arXiv:2503.18251, 2025) **[S]** | 12,885 C++ Codeforces solutions, 443 problems; two-level task: "Infer the Task" and **"Infer the Technique"** | arXiv/GitHub (check repo) | Closest public **technique-labeled** source; candidate for classifier pretraining or label vocabulary calibration |
| **Aizu Online Judge** (AOJ) **[V via Watanobe full text]** | Source of Watanobe et al.'s 61,614-code corpora (45,398 across 6 algorithm categories; 16,216 sorting-only) | AOJ public API/archive | Openly re-collectable; category labels exist (e.g., "sorting", "graph") |
| **IBM Project CodeNet** (arXiv:2105.12655) **[S]** | ~4,000 problems, 14M submissions, 55 languages | Open (research registration) | Optional large-scale pretraining for code encoders |
| **BigCloneEval / BigCloneBench** **[V via AlDeSCo paper]** | Large clone benchmark incl. algorithm-labeled subsets | GitHub | Used by AlDeSCo for pattern-recognition eval (Fibonacci, Bubble Sort, Binary Search subsets) |
| **AlDeSCo artifact** (zenodo.org/records/11217414) **[V]** | DSL pattern catalog + matching tool (ICCQ 2024) | Zenodo (open) | Reuse its **pattern catalog** as interpretable-prior component & ablation partner |
| **Blackbox** (UK, Brown et al.) **[S — known in field]** | Millions of novice BlueJ Java sessions | Request-based (anonymized) | Only if a large novice-Java corpus is wanted; access latency — plan ahead |

## 4.9 Gap analysis → what the project's own dataset must add
No located dataset provides **(student/novice buggy code) × (algorithmic-pattern label) × (localized fault ground truth)** simultaneously:
- POJ-104/AOJ/COFO: pattern-ish labels, **no bugs**;
- Codeflaws/ConDefects/BugT/IntroClass: bugs + fault location, **no pattern labels** (task IDs only; mapping exists only implicitly via task catalogs);
- QuixBugs: both implicitly (classic algorithms) but n≈40.
**⇒ The project needs a relabeled/merged corpus** (e.g., ConDefects-Python + Codeflaws + own AlgoRythm sandbox logs, with tasks mapped to the 10–15-pattern curriculum vocabulary), plus ideally a fresh leakage-free slice collected on AlgoRythm itself. Detailed design in the Synthesis section.
