# Block 3. Fault localization for novice programmers

Verification legend: **[V]** verified from fetched primary source; **[S]** from credible search snippets only; **⚠️** unverified; **NOT FOUND** = not located after repeated attempts.

---

## 3a. Spectrum-Based Fault Localization (SBFL) — formulas and evidence

**Canonical survey [V]:** C. Song Wong, Wei Gao, Zhenyu Li, Ruitao Feng, Yueqi Lyu, Yong Wang, Lin Chen. "A Survey on Software Fault Localization." **IEEE Transactions on Software Engineering (TSE) 42(8), 2016**, DOI 10.1109/TSE.2015.2477715 — 154 surveyed papers (2006–2013). The standard SBFL citation.

**Mechanics.** For each program element e (statement/branch): `ef` = tests covering e that failed, `ep` = tests covering e that passed, `nf` = failed tests total, `np` = passed tests total. Suspiciousness(e) computed per formula; elements ranked descending.

| Formula | Definition | Origin / status |
|---|---|---|
| **Tarantula** | (ef/nf) / [(ef/nf) + (ep/np)] | Jones, Harrold & Stasko, "Visualization of test information to assist fault localization," **ISSTA 2002** [V] |
| **Ochiai** | ef / sqrt(nf × (ef + ep)) | adapted to FL from biology (species-overlap coefficient); discussed in Wong et al. survey [V]; generally **outperforms Tarantula** |
| **Jaccard** | ef / [ef + ep + nf] | also in Wong et al. survey [V] |
| **OP2** | ef − ep/(ep+1+0.001) | Naish et al. lineage; best Python performer in novice MBFL study below [V] |
| **DStar (D*)** | ef* / [ep + (nf − ef)], star parameter * (best at *=3) | Wong, Debroy et al., "The DStar Method for Effective Software Fault Localization," **IEEE TSE 39(4), 2013**, DOI 10.1109/TSE.2012.53 [V] |

**Combination study [S]:** Zou et al., "An empirical study of combining 40 fault localization techniques" (TSE lineage, UIUC Lingming Zhang group) — combining formulas helps; supports "ensemble" framing.

**Novice-transfer evidence (critical):**
- **Qi et al. 2013** (cited in VsusFL intro [V]): tested 15 FL techniques on real **novice** programs → poor performance across the board.
- **Araujo et al. 2016** (IEEE, doc 7757727) [V-cited]: "Applying spectrum-based fault localization on novice's programs" — **~40% of novice programs don't satisfy FL preconditions** (e.g., fail ALL tests → no passing spectrum; or pass all → nothing to localize).
- **Empirical study 2023** [S]: SBFL on 122 real student programs from a Chinese university OJ — again degraded vs Defects4J-world results.

**Why SBFL degrades on novices (synthesis for the paper's motivation):** novices' buggy programs often fail most/all tests (low `np` discrimination), programs are short (many ties at equal suspiciousness), and single-fault/multi-fault assumptions built for mature software break.

---

## 3b. Mutation-Based Fault Localization (MBFL)

**Mechanics.** Generate mutants of each statement; run the test suite on each mutant; a statement is suspicious if mutants of it **change failing tests to passing** (kills the failure → the real fault likely nearby).

| Technique | Reference | Idea |
|---|---|---|
| **MUSE** | Moon, Kim, Bae, Choi (KAIST), **ICSE 2014** "Mutating Faulty Programs for Fault Localization" [V/KAIST TR] | Contrast mutant behavior of faulty vs correct versions; statement suspicious if its mutants flip failed tests to passed more often than in the reference program. |
| **Metallaxis** | Papadakis & Le Traon [S] | Treats mutants as "faults"; suspiciousness from mutant-test kill patterns (Ochiai-style on mutants). |
| **FEP** | Zhang et al., **ICSE 2017** [S] | Fault Execution Probability — weights mutants by how likely they execute and propagate to failure. |
| **SIMFL** | J. Kim et al., arXiv:1902.09729 (2019) "Ahead of Time Mutation Based Fault Localization" [V-abstract] | Predictive model: mutation-testing results collected **in advance** predict locations of future faults; failure vector as input. |
| **PMBFL** | Xu et al. 2024 (conf. abs. 2024qrsc.conf...78X) [S] | Prediction-based execution info to cut MBFL cost. |
| **Mutation execution strategy** | Zhang et al., Information Sciences 2017, dl.acm.org/doi/10.1016/j.ins.2017.09.006 [S] | Optimal mutant execution order for cost reduction. |

**KEY EMPIRICAL PAPER — MBFL on novice programs, Python vs Java [V, full text fetched]:**
**Yang, Mei & Yang. "An Empirical Study of MBFL on Novice Programs Across Different Programming Languages."** *International Journal of Software Engineering and Knowledge Engineering (IJSEKE)*, Vol. 35, Iss. 07, publ. 2025-07-16. DOI 10.1142/S0218194025500329.
- **Setup.** 150 Python + 150 Java real faulty submissions selected from **ConDefects** (Java: 1,254 faulty programs / 810 tasks / avg 259.22 LOC; Python: 1,625 faulty / 985 tasks / avg 49.03 LOC; AtCoder 2021–2023). Each program: 7 tasks/tests. Metrics: **Top-1/3/5** and **EXAM score**, ties broken **conservatively (worst rank)** — cites that 73.58% of developers inspect only top-5.
- **Mutation operators:** relational (≥, >, ==, ≤, <), logical (&& ↔ ||), arithmetic, shift (≫ ≪), assignment operators; conditional operators.
- **MBFL formulas (on mutant counts akf/anf/akp/anp):** Jaccard, Tarantula, Ochiai, OP2, DStar.
- **Results (150 programs each):**
  - Python: **Top-1 = 45, Top-3 = 70, Top-5 = 92** (OP2 best) → i.e., Top-5 ≈ 61%;
  - Java: **Top-1 = 37, Top-3 = 71, Top-5 = 84** (Ochiai);
  - Avg EXAM: Python 0.284, Java 0.324;
  - Runtime: Python ≈ 87 h total (~1.8× Java's) — MBFL is expensive at novice scale.
- **RQ2 (why Python better):** mutation coverage & mutation score positively correlate with Top-N; tie ratio lower in Python (19.7% vs 14.8%... careful: Python tie ratio reported ~19.7% vs Java 14.8% — see paper); "mutant noise" (misleading surviving mutants) Java 13.12% vs Python 11.48%; CCTs (correct-change traces) Java 8.81% vs Python 5.66%.
- **RQ3 (confidence prediction):** linear confidence score α·(n_fixed/n_failed) + β·(1 − n_same/n_total); Point-Biserial corr with Top-5: +0.35 (Java), +0.37 (Python), p<0.05; Spearman with EXAM: 0.64 (Java), 0.78 (Python), p<0.0001 → MBFL results on novice programs are statistically predictable/confidence-assessable. **This correlation analysis is a methodological template for the project.**
- **Limitations (authors'):** single-fault programs only; small per-program test suites; languages only Java/Python; ConDefects tasks from one platform (AtCoder).
- **Relevance: HIGHEST** — this is the direct pattern-agnostic baseline family to beat, with exact Top-N protocol on novice data.

---

## 3c. LLM-based fault localization for novices (2025)

**[V — FULL TEXT FETCHED (arXiv HTML)]** **Xu, Liu, Wu, Kang, Chen, Liu (BUCT, BIPT, Nantong Univ.). "Exploring the Potential and Limitations of Large Language Models for Novice Program Fault Localization."** arXiv:2512.03421, submitted **2025-12-03**. Journal version: Journal of Systems and Software (S0164121225004005). Code/data: **github.com/Xucranger/PLofLBFL**.
- **Setup.** 503 programs per dataset (1,509 total) from Codeflaws (C), Condefects (Java), BugT (C++); each LLM run **repeated 5×, averaged**; prompt < 2,048 tokens; ground truth = buggy line number; numbered lines injected to prevent line-offset errors; JSON output parsed by regex, up to 10 resubmissions (usually ≤3).
- **Models (13):** closed: OpenAI o3, o1-preview, o1-mini, GPT-4o, GPT-4, GPT-3.5-Turbo; open: ChatGLM4 (9B), ChatGLM3 (6B), DeepSeekR1 (671B), DeepSeekV3 (671B), Llama3-7B, Llama2-7B, Code Llama-7B-Instruct.
- **Prompt components (5):** Novice-persona ("algorithm teacher"), Intent (self-explain code purpose), Reason (justify each suspect line), CoT (two-phase: list suspicious lines → rank), Sort (descending suspiciousness). **Ablation:** o3 & DeepSeekR1 nearly unaffected by prompt design (reasoning-internal); GPT-4 heavily prompt-dependent — removing the Novice persona is the single most damaging removal.
- **Headline results (counts out of 503):**

| Method | Codeflaws T1/T3/T5 | Condefects T1/T3/T5 | BugT T1/T3/T5 |
|---|---|---|---|
| OpenAI o3 | 99 / 215 / 291 | **312 / 373 / 409** | **289 / 413 / 449** |
| DeepSeekR1 | **110** / 206 / 280 | 290 / 371 / 401 | 248 / 345 / 424 |
| DeepSeekV3 | 107 / 212 / 291 | 215 / 316 / 345 | 209 / 294 / 366 |
| GPT-4o | 101 / 213 / 287 | 213 / 310 / 360 | 177 / 288 / 358 |
| GPT-3.5-Turbo | 100 / 194 / 240 | 148 / 248 / 290 | 133 / 223 / 278 |
| Llama3-7B | 58 / 132 / 178 | 100 / 209 / 251 | 102 / 182 / 253 |
| Code Llama | 41 / 104 / 136 | 59 / 147 / 180 | 49 / 108 / 145 |
| **SBFL** (DStar/Ochiai/OP2) | 13 / 54 / 106-107 | **0** / 59 / 170 | **1** / 15 / 20 |
| **MBFL** (DStar/Ochiai/OP2) | 3 / 24 / 75 | 84 / 228 / 300 | **2** / 46 / 135 |

  (Percentages: o3 on BugT = 57.5% Top-1, 89.3% Top-5; SBFL Top-1 ≈ 0% on Condefects/BugT; MBFL Top-1 ≈ 0.4% on BugT. Traditional methods **collapse** on the internal-network dataset; LLMs beat SBFL/MBFL everywhere except Codeflaws Top-1 where MBFL is weak anyway.)
- **Unique-fault analysis (UpSet, RQ2):** on Codeflaws, o3 uniquely localized 26 faults, DeepSeekR1 37; MBFL uniquely localized only 1, SBFL 8 → methods are complementary; hybrid recommended by authors.
- **Difficulty (RQ4):** 5 difficulty bins × ~100; accuracy drops as difficulty rises on Codeflaws/Condefects (e.g., o1-preview Codeflaws 46→61 from Lv.5→Lv.1 Top-1; Condefects 57→86); on BugT top models stay high even at Lv.5 (o3: 94) — BugT ceiling too low to stress SOTA reasoning models.
- **Cost per program (Table 5):** o3 $0.0152/52.4 s; o1-preview $0.4859/96.4 s; o1-mini $0.1497/43.2 s; GPT-4o $0.0092/15.3 s; GPT-4 $0.0673/21.5 s; GPT-3.5-Turbo $0.0034/7.3 s; **SBFL 0.83 s; MBFL 38.28 s** → LLM cost framing for the project's efficiency argument.
- **Over-reasoning finding:** on Codeflaws, o3 < GPT-4o and even < GPT-3.5 at Top-1; authors attribute to (a) suspected **data leakage** in Codeflaws favoring older models, (b) excessive contextual reasoning misleading on simple faults (citing "recitation reasoning" literature).
- **Statistics precedent (for Block 5):** one-sided **Wilcoxon signed-rank test**, α=0.05: o3 vs GPT-3.5 p=0.15625 (Codeflaws, n.s.) vs p=0.03125 (Condefects, BugT, significant) — small-n paired Top-N comparisons ARE testable this way (n=5 difficulty bins per dataset here).
- **User study (RQ5):** 10 novices (5×1yr, 5×3yr experience), 30 BugT samples, 5 dimensions (readability/usefulness/conciseness/relevance/accuracy, both open & closed models 4.36/5 readability); 1-yr group consistently rates higher; closed-source leads conciseness by 0.30. Participants blinded to LLM provenance.
- **Limitations (authors'):** LLM compute cost; over-reasoning; BugT difficulty ceiling; languages C/C++/Java only; single-line ground truth; dataset leakage in Codeflaws suspected.
- **Relevance: HIGHEST.** Defines the exact SOTA baseline set and protocol the project must adopt (503-program samples, 5-run averaging, Top-N, Wilcoxon). Also shows the opening for the project: **no method in the comparison uses any structural prior about the intended algorithm** — and the LLM accuracy degradation with difficulty is precisely where a pattern prior should pay off.

**[S]** "Explainable Fault Localization for Programming Assignments via LLM..." — arXiv:2509.25676 (Sept 2025). LLM-generated explanations of localization for assignments. (Verify details before citing.)

---

## 3d. Novice-specific fault localization systems

**[V, ScienceDirect full intro]** **VsusFL — Li, Wu, Liu, Shen, Wu, Zhang, Chen (Beijing Univ. of Chemical Technology). "Variable-suspiciousness-based Fault Localization for novice programs."** *Journal of Systems and Software* **205 (Nov 2023)**, 111822. DOI 10.1016/j.jss.2023.111822.
- **Method.** Trace **variable value sequences** at runtime (custom C/C++ instrumentation, CppSnooper); find a **correct program version** (same task) from the OJ; build **bipartite graph between faulty-program variables and correct-program variables**; solve matching with the **Hungarian algorithm**; compare value sequences of matched variables; derive statement-level suspiciousness from the first divergence.
- **Data.** 422 real faulty submissions from 33 problems (real OJ).
- **Baselines beaten:** Grace (Lou et al. 2021), ANGELINA (Mechtaev et al. 2016), SBFL (Ochiai/Abreu), VFL (Kim 2019), VSBFL (Li 2021).
- **Results.** Outperforms all on Top-1/3/5; localizes **90%/35%/9% more** than the next best (Grace) at Top-1/3/5 respectively.
- **Extra finding.** Weak correlation between VsusFL and other FL methods' rankings → **combining complementary FL signals is promising** (an argument the project can reuse for adding pattern priors as an orthogonal signal).
- **Limitations.** Needs a semantically equivalent correct reference program; C/C++ focus; single bugs.

**[S] FFL — Le, Thung, Wang, Li, Lo (SMU). "FFL: Fine-grained Fault Localization for Student Programs via Syntactic and Semantic Reasoning."** **ICSME 2022** (IEEE 9978180). Combines syntactic reasoning (compare to correct solution structure) with semantic reasoning (fix candidates). PDF: soarsmu.github.io/lib/exe/fetch.../paper.pdf. *(Numbers: fetch from PDF before citing.)*

**[S] Grace** — Lou et al. 2021 (cited in VsusFL): automated repair+localization for student programs via corrective patches. **ANGELINA** — Mechtaev et al. 2016: search-based repair of student programs (AngelicForest lineage).

**[S] Neural attribution:** Gupta et al., **"Neural Attribution for Semantic Bug-Localization in Student Programs" — NeurIPS 2019** (cited in VsusFL [V]): tree-LSTM trained to predict buggy lines (sensitivity-based explanations over control-flow). The main learned, pattern-agnostic neural baseline in the education space.

**[S] COMPSAC 2024** — "Fault Localization for Novice Programs Combining Static Analysis and Dynamic..." — 223 student-failure programs; static+dynamic hybrid.

**[S] Tie problem** — "An Empirical Study of Fault Localization on Novice Programs and Addressing the Tie Problem" (2024, ResearchGate 383027009): ties dominate novice FL rankings; ties-handling materially changes Top-N.

**[S] "Boosting Spectrum-Based Fault Localization via Multi-Correct Programs"** — IEICE Transactions 2024 (jstage, E107.D): use **multiple correct submissions** of the same task to sharpen spectra. Conceptually the nearest neighbor to "structural prior from reference solutions" found so far — but it uses whole reference programs, not a *pattern class*, and only re-weights spectra. **Does not close the project's gap; must be cited and differentiated.**

**NOT FOUND:** "SCOPE" as an MBFL/FL tool for novices — no credible hit under this name in FL-for-education literature. Possible confusions: SIMFL (predictive MBFL), SCOPE in other SE subfields, or a mis-remembered name. Flag in the final paper only if the user can supply a source.

---

## 3e. Automated Program Repair (APR) for introductory programming assignments

Relation to the project: repair pipelines *contain* a localization component; clustering correct solutions is the education-specific trick most analogous to pattern priors.

| Work | Venue/Year | Method | Relevance |
|---|---|---|---|
| **CLARA** — Riad (Gupta, Mukherjee, Purandare, Damani, IIT Bombay) | **ITiCSE 2018**, DOI 10.1145/3192366.3192387; arXiv:1603.03165 [V] | (1) Cluster **correct** submissions by dynamic behavior (test-value vectors); (2) repair an incorrect submission by aligning its trace to a cluster's traces (trace alignment → edits). Tool: github.com/iradicek/clara | The canonical "cluster correct solutions" precedent. Localization is implicit in trace alignment; no pattern labels. |
| **CEMR** | IEEE 10535720, 2024 [S] | CodeBERT-based edits mined from real student fix pairs to repair IPAs | Learned-edit baseline; needs paired wrong→right data |
| **Brafar** | IEEE 10653064, 2024 [S] | APR for IPAs in the hard case where **no matching control-flow** correct program exists | Explicitly names the structural-mismatch limit of CLARA-style repair |
| APR via generated repair catalogs | IEEE TLT 2024, DOI 10.1109/TLT.2024.3403710 [S] | Catalog-based fixes for intro assignments | Shows 2024 continuation of the line |

**Synthesis for positioning:** the CLARA family uses *other students' correct programs* as the structural reference; AlDeSCo uses *hand-written AST patterns*; VsusFL uses *one matched correct program*. Nobody uses **the task's intended algorithmic pattern class** (shared across many tasks) as a compact, transferable structural prior for localization. That is the gap.

---

## Implications for the project (Block 3 → design choices)

1. **Baselines to implement/compare (minimum credible set):**
   - SBFL: Ochiai, Tarantula, OP2, DStar on the same data (cheap, well-specified).
   - MBFL: OP2-on-mutants protocol from Yang/Mei/Yang 2025 (or MUSE) if compute allows — cite its 87-hour Python cost as the overhead argument.
   - LLM: a reasoning LLM (DeepSeek-R1-class, open) zero-shot pattern-agnostic localizer, per arXiv:2512.03421.
   - Learned neural: Gupta et al. NeurIPS 2019-style tree model if time permits.
2. **Metrics protocol:** Top-1/Top-3/Top-5 with conservative tie handling + EXAM score, exactly as IJSEKE 2025 does; report per-pattern breakdown.
3. **Expected baseline numbers to beat (novice programs):** Top-5 ≈ 61% (MBFL, Python/OP2); SBFL lower; LLM-reasoning higher on easy tasks but degrades with difficulty — the project's pitch: **pattern priors should specifically help the mid/high-difficulty band where LLMs degrade**.
4. **Design hazard found:** ~40% of novice programs may violate FL preconditions (Araujo 2016) — dataset construction must enforce ≥1 passing + ≥1 failing test per program.
5. **Statistical template:** Yang/Mei/Yang's correlation battery (Point-Biserial, Spearman) + the tie-problem paper justify paired stats on Top-N (see Block 5 for exact tests).
