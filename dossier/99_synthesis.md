# Synthesis and Recommendations

This section converts the dossier into a defensible project design. Every choice cites the block that justifies it.

---

## S1. Recommended dataset design

**What exists (Block 4):** no public dataset joins (novice buggy code) × (algorithmic-pattern label) × (line-level fault ground truth). Codeflaws/ConDefects/BugT have the first two minus patterns; POJ-104/AOJ/COFO have patterns minus bugs.

**Recommended corpus — "three layers":**

| Layer | Source | Size | Purpose |
|---|---|---|---|
| **L1 Main** | ConDefects-Python (AtCoder 2021–23) + Codeflaws-C subset | **300–500 programs total**, ≥30 per pattern | primary Top-K evaluation |
| **L2 Showcase** | QuixBugs (~40 single-bug classic algorithms) | 40 | worked examples; hand-verified pattern-specific checks; paper's Figure 1 material |
| **L3 Fresh slice** | AlgoRythm sandbox logs (own platform) | 50–150 submissions, leakage-free | kills the "everything is contaminated" objection; needs ethics protocol (below) |

**Inclusion filters (from Block 3 hazards):** program must compile; have ≥1 passing and ≥1 failing test (Araujo 2016: ~40% of novice programs fail all tests — excluded); exactly one fault (per fix diff ≤1 hunk, or manual verification); length 10–300 lines.

**Pattern vocabulary (10–12 classes, calibrated to Block 2 feasibility evidence):**
`two pointers · sliding window · binary search · prefix sums · dynamic programming · greedy · DFS/BFS (graph traversal) · sorting-based · hash-map counting · brute force / implementation · intervals · simulation`
Rationale: Watanobe et al. classified 6–7 algorithm categories at F1 95.7 with structural features alone; Lu et al. 97% with GNN on student code; AlDeSCo's catalog already contains binary search/bubble sort/fibonacci motifs. Confusable pairs (BFS vs DFS) stay as separate classes only if annotator agreement supports it.

**Ground truth for fault location:** first-changed-line of the accepted fix, adjusted by manual review (fix may refactor); mark "fault line" as the minimal executed region consistent with the diff (single statement or line range).

**Labeling protocol:** task→pattern mapping built from AtCoder/Codeforces problem tags + acceptance criteria; then double annotation (author + 2 independent CS-students) of a 100-program calibration set; report **Cohen's κ ≥ 0.70** (from Block 5 precedent: quantitative agreement = judge credibility); adjudicate disagreements; release all labels publicly (CC-BY-4.0) — the annotation itself is a contribution.

**Tooling:** Python + `tree-sitter`/`ast` module for parsing; pytest-based runner for test suites; `mutmut` (Python mutation testing) for MBFL baseline; git repo per program with buggy/fixed versions (Defects4J-style layout, cite Just et al. ISSTA 2014 as the format).

**Licenses:** ConDefects research artifact + Codeflaws (public GitHub) + C-UDA-style terms respected (Block 4 table); own annotations CC-BY-4.0; no redistribution of platform-user data without protocol.

---

## S2. Recommended architecture (classifier + localizer), with alternatives rejected

### S2.1 Pattern classifier
**Primary: fine-tuned CodeBERT-base (125M)** on the L1/L2 corpora, 10–12-way classification.
- Why: CodeBERT = 82.67 MAP@R on POJ-104 retrieval (CodeXGLUE official, Block 2c); small enough for Colab; identifiers+structure both visible; UniXcoder-base the drop-in upgrade if accuracy plateaus (InvPT-style robustness on transformed code is a bonus, Block 2c).
- **Required companion baselines:** (a) Watanobe-style structural-feature CNN (identifier-stripped, Block 2f) — proves the signal is structural, not identifier leakage; (b) AlDeSCo-style DSL rules for 3–5 patterns (Block 2d, artifact on Zenodo) — the interpretable component.
- Report 10-fold CV + per-class P/R/F1 (Watanobe protocol, Block 2f).

### S2.2 Localizer — the experiment's core
Five arms, all evaluated identically (Top-1/3/5 + EXAM):

| Arm | Type | Pattern use |
|---|---|---|
| **A. SBFL** (Ochiai + OP2 + DStar) | classical, needs tests | none — baseline |
| **B. MBFL** (mutmut + OP2, subset n≥150) | classical | none — baseline (protocol: IJSEKE 2025, Block 3b) |
| **C. LLM zero-shot** (open reasoning model, e.g., DeepSeek-R1-class, locally runnable; 5 runs) | LLM | none — 2025 SOTA baseline (arXiv:2512.03421 protocol, Block 3c) |
| **D. LLM + pattern prior** | LLM | pattern label + **pattern-specific failure checklist** injected into the same prompt |
| **E. Prior-reweighted spectrum** (A's spectrum × pattern prior from AST property checkers) | classical+rules | structural prior without LLM |

**The pattern-specific failure checklist** (the scientific object) — one table in the paper, 3–5 checkpoints per pattern, grounded in Block 1 taxonomies:
- two pointers: pointer-shift condition; loop-termination condition; boundary initialization; merge/dedup step;
- sliding window: window-invariant update on expand; shrink condition; answer capture point;
- binary search: mid computation (+1/−1 overflow); left/right update (infinite-loop); boundary return;
- DP: base case; transition completeness (all predecessors); iteration order; memo initialization; index offsets;
- DFS/BFS: visited marking placement; queue/stack discipline; neighbor pruning; termination;
- etc. (12 tables; each checkpoint maps to an AST property checker for Arm E — AlDeSCo DSL is the implementation route).

**Key methodological control (Block 5 + Block 3c):** run D and E under **two label conditions** — *oracle* (gold pattern label; isolates the prior's value) and *realistic* (predicted by S2.1; measures end-to-end pipeline) — and report both. Reviewers/judges ask exactly this; arXiv:2512.03421's ablation style is the template.

### S2.3 Alternatives considered and rejected
- **inst2vec-style IR features** (Block 2b): fails on broken/uncompilable novice code; rejected.
- **Full GNN line-localizer** (Gupta NeurIPS 2019 / Hoq EDM 2025 reproduction) as a 6th arm: valuable but engineering-heavy; keep as *optional*; if included, use Hoq's published SANN recipe (Block 7.2).
- **Hand-written AlDeSCo-only rules as the localizer**: does not generalize beyond catalog (their own stated limitation) → demoted to Arm E component + ablation partner.

---

## S3. Evaluation plan (metrics + statistics)

1. **Metrics:** Top-1 / Top-3 / Top-5 accuracy; **EXAM score**; conservative worst-rank tie-breaking; per-pattern and per-difficulty-bin breakdowns (Block 5.1; difficulty bins 5×~100 per arXiv:2512.03421).
2. **Runs:** LLM arms — 5 repetitions, mean±sd (Block 5.1 protocol); classical arms deterministic.
3. **Hypothesis tests:**
   - **Exact McNemar** (paired binary, same programs, D vs C at Top-1/3/5) — primary test;
   - **One-sided Wilcoxon signed-rank** across difficulty bins (secondary; precedent arXiv:2512.03421);
   - **Bootstrap 10k percentile CIs** on all Top-K deltas (Block 5.2);
   - report effect sizes (McNemar odds ratio; Cliff's delta on EXAM).
4. **Sample size:** **n=300 minimum (30×10 patterns), 500 target** — Block 5.4 power sketch: at n=300, ~45 discordant pairs expected if prior flips ~15%; exact McNemar detects imbalance at α=0.05. Confirm with a 30-program pilot before locking.
5. **Ablations = the paper's spine:** (i) prior on/off (D vs C, E vs A); (ii) oracle vs predicted label; (iii) checklist vs bare pattern name; (iv) difficulty-stratified gains (hypothesis: gains concentrate where LLMs degrade — arXiv:2512.03421 RQ4); (v) cost table per program (seconds + $; their Table 5 format).
6. **Reproducibility:** fixed seeds, released prompts, released labels, environment pinning; cite Pearson ICSE 2017 on FL-evaluation confounds (Block 5.5).

---

## S4. Timeline (reverse-planned from РКНП republican stage, mid-December 2026, and ISEF selection spring 2027)

| When | Milestone | Evidence from blocks |
|---|---|---|
| **Aug 30 – Sep 10, 2026** | Freeze hypothesis & checklist tables; download ConDefects/Codeflaws/QuixBugs; **email BugT authors for access** (long latency); draft Form 1A research plan + consent texts | Blocks 4, 8 |
| **Sep 2026 (by Sep 20)** | **School-stage submission;** IF any human pilot: **IRB/SRC pre-approval BEFORE any data**; start L1 labeling (calibration set) | Block 8.1, 8.3 |
| **Sep 20 – Oct 15** | Labeling + κ; classifier training (CodeBERT + 2 baselines, 10-fold); SBFL/MBFL pipeline on 150-program pilot; pilot stats → final n | S1–S3 |
| **Oct 15 – Oct 20** | **Regional-stage submission** (областной этап) | Block 8.3 |
| **Oct – Nov 15** | Full runs (arms A–E, oracle+realistic, 5×LLM); statistics; ablations; cost tables; begin write-up (EN) | S3 |
| **Nov 15 – Dec 10** | Russian/Kazakh оформление per Положение; тезисы; презентация; **10-minute defense rehearsal**; demo video backup | Block 8.3 |
| **~Dec 10–20, 2026** | **РКНП republican stage** | Block 8.3 |
| **Jan – Feb 2027** | Re-run novelty queries (Block 7.2); refine for Daryn ISEF selection; **250-word English abstract** (AI may NOT write it — Block 8.1); poster; travel/forms | Block 8 |
| **Mar – May 2027** | Regeneron ISEF (category SOFT); logbook + data book current throughout | Block 8 |

**Critical path:** BugT access and IRB paperwork are the two long-latency items — start both in the first week. The core claim must NOT depend on the human pilot (keep L3 optional).

---

## S5. Risks and red flags (ranked)

1. **🚩 Strong LLM baselines may swamp the effect.** o3 reaches Top-1 57.5% on BugT with no prior (Block 3c). Mitigation is built into the design: difficulty-stratified analysis (gains expected mid/hard band), classical-arm gains (Arm E vs A), and the fallback claim — "pattern prior improves classical localization and reduces LLM prompt/steps cost" — both publishable. Decide after pilot data, not after the full run.
2. **🚩 Novelty is time-sensitive.** Gap verified 2026-08 (Block 7), but 2026-H2 preprints appear weekly; mandatory re-run of the 8 query families 2 weeks before every submission. Non-English venues (CNKI) never checked — one sweep required.
3. **🚩 Human subjects paperwork.** Any pilot on people without prior IRB/SRC approval = ISEF violation of the most-flagged kind (Block 8.1). Either calendar approval by mid-September or drop the pilot from the core claim.
4. **Dataset licensing/access.** ConDefects & Codeflaws fine for research; BugT needs author contact; L3 platform data requires written SRC confirmation of the anonymization stance or full Form 4 (Block 4, 8.1, 9).
5. **Classifier error propagation.** Realistic-pipeline accuracy is bounded by classifier accuracy; report oracle + realistic separately (S2.2); if classifier <85%, consider UniXcoder upgrade or vocabulary reduction (merge confusable classes).
6. **Data leakage.** Codeflaws is suspected-contaminated for LLM-era work (Block 3c) — use it for classical arms only, or mark it clearly; keep ConDefects/BugT/AlgoRythm-slice as headline sets.
7. **Ties & degenerate programs.** Worst-rank tie handling mandatory; the ≥1 passing test filter removes the ~40% degenerate stratum (Block 3a, 5.5).
8. **РКНП language & self-research declaration.** Work must be presented in Kazakh/Russian with the independence certificate; keep git history as evidence; AI tools may not author the plan/abstract (Block 8.3, 8.1).
9. **MBFL cost.** ~87 h for 150 Python programs (Block 3b) — budget compute early or subset to n=150 for Arm B and say so.

---

## S6. The one-paragraph project statement (for the research plan's "importance" box)

Novice programmers lose most time not to syntax but to *logical* faults, and modern fault localization for novices is either statistically brittle (SBFL/MBFL: Top-5 ≈ 61% at best on novice data) or computationally expensive and difficulty-sensitive (2025 reasoning-LLMs: high Top-5, degrading with task difficulty). Meanwhile, algorithm recognition from code is solved at >94% accuracy. We connect the two: a pattern classifier supplies a structural prior — a checklist of pattern-specific failure points (pointer-shift conditions for two pointers, base cases and transitions for DP) — that measurably improves Top-1/Top-3/Top-5 fault localization over pattern-agnostic baselines on a new open corpus of ~400 pattern-labeled novice bugs. The idea descends from PROUST's intention-based diagnosis (1985); the learned, quantified, pattern-conditioned version is new (Block 7).
