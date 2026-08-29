# Block 2. Algorithm/pattern classification from code

Verification legend: **[V]** = verified from fetched primary source (arXiv page, journal full text, official repo README); **[S]** = verified only from search-result snippets of credible sources; **⚠️** = unverified / contradictory, treat with caution; **NOT FOUND** = could not locate after repeated attempts.

Context for relevance judgments: the project needs (a) evidence that algorithm/pattern classification from source code is a well-established task with known accuracy ceilings, and (b) a defensible choice of classifier architecture for a school-scale pipeline (AST-based classifier already prototyped in AlgoRythm).

---

## 2a. The POJ-104 benchmark

**[V]** Cross-checked across: TBCNN paper (arXiv:1409.5718 abstract page), CodeXGLUE official README (raw.githubusercontent.com/microsoft/CodeXGLUE), UniXcoder paper description surfaced in search (ar5iv 2203.03850), CompilerGym and HuggingFace dataset pages.

| Property | Value |
|---|---|
| Classes | 104 programming problems from Peking University Online Judge (POJ) |
| Programs per class | 500 accepted (correct) submissions per problem |
| Total | ~52,000 programs |
| Language | C/C++ (accepted solutions only) |
| Introduced for ML by | Mou et al., TBCNN paper, AAAI 2016 (arXiv:1409.5718) |
| Canonical distribution | microsoft/CodeXGLUE repo: (1) `Code-Code/Clone-detection-POJ-104` (given a code, retrieve Top-K semantic clones); (2) `Code-Code/Code-classification-POJ104` (104-way classification, eval = Accuracy) |
| Split (clone task, official) | 64 / 16 / 24 problems (train/valid/test = 32,000 / 8,000 / 12,000 programs) |
| License | CodeXGLUE code = MIT; **datasets = Computational Use of Data Agreement (C-UDA)** — permissive for research, not public domain |
| Mirrors | HuggingFace `semeru/Code-Code-CloneDetection-POJ104`; CompilerGym `poj104` |

Key caveats for the project:
- The "94% TBCNN" number and later CodeXGLUE numbers use **different split protocols and even different tasks** (classification vs clone retrieval) — accuracy numbers across papers are NOT directly comparable. Any literature table in the final paper must state task + split.
- POJ-104 labels are **problem IDs, not algorithmic patterns**. 104 arbitrary judge problems ≠ "two pointers / sliding window / DP" vocabulary. A pattern-level classifier (the project's need) has no ready-made POJ-style benchmark — this is part of the research gap.

**Related dataset found during search [S]:**
- **COFO** — "COFO: A Dataset of Code Contests Solutions for Program Analysis" (arXiv:2503.18251, 2025). 12,885 C++ solutions from Codeforces, 443 problems, curated from 1M+ submissions; introduces a **two-level task: "Infer the Task" and "Infer the Technique"** (i.e., inferring the algorithmic technique applied). This is the closest public dataset to a *pattern-level* classification target and should be examined in Block 4.
- **Aizu Online Judge (AOJ)** — source of Watanobe et al.'s datasets (see 2f); openly accessible research-friendly OJ archive (details in Block 4).
- **Project CodeNet** (IBM, arXiv:2105.12655) — large multi-language OJ dataset, usable for auxiliary pretraining.

---

## 2b. Classic neural code-classification models

### TBCNN — Tree-Based Convolutional Neural Network **[V]**
- Lili Mou, Ge Li, Lu Zhang, Tao Wang, Zhi Jin. "Convolutional Neural Networks over Tree Structures for Programming Language Processing." **AAAI 2016** (paper states "accepted to AAAI-16"). arXiv:1409.5718.
- **Method.** Programs are parsed to ASTs and binarized. A fixed-depth sliding "tree-based convolution" window (over parent–children node tuples, with separate weights for left/right child = "child-order weighting") extracts structural features local to each subtree; dynamic pooling folds variable-length trees into a fixed vector; softmax classification head on top. Pretraining task: predicting AST node types (network pretraining as "a particular form of regularization").
- **Results.** On the OJ (POJ-104) program classification task: **accuracy ≈ 94%**, outperforming the baselines they compared (structured (recursive) encoding, GSN). Applied also to C++ bug finding (a labeled-code task).
- **Limitations.** Fixed-depth convolution; binarization distorts n-ary trees; no attention; authors note performance is task-specific.
- **Relevance.** The canonical evidence that **AST-structural encodings beat plain token streams** for algorithm classification — directly supports the project's AST-classifier premise.

### code2vec **[V]** (arXiv:1803.09473; journal version POPL 2019; earlier "A General Path-Based Representation" appeared 2018)
- Uri Alon, Meital Zilberstein, Omer Levy, Eran Yahav (Technion).
- **Method.** Decomposes each AST into a set of **path-contexts** (terminal-to-terminal paths through the AST + the tokens at both ends), embeds them, and aggregates with a **soft attention** into a single code vector.
- **Results.** Original task = Java method naming on the "Asleep-at-the-keyboard" corpus (10 large Java projects): **top-1 precision 59.8%, top-2 65.8%, top-5 67.7%** on held-out C# test projects, beating the previous attention model (53.8/59.7/62.7); trained on ~12M contexts. Per abstract, also strong on C# (e.g., ~73% C# F1 in this work family).
- **Limitations.** Variable-name agnosticism is partial (identifiers carry a lot); path contexts lose global structure; authors note attention heads align with syntactic categories.
- **Relevance.** Provides the *representation* (AST paths + attention) the project can reuse; classification head is trivial to swap in.
- **POJ-104 use by third parties:** in the official CodeXGLUE clone-detection-POJ-104 leaderboard, **code2vec scores MAP@R = 1.98** (near zero) vs CodeBERT 82.67 — a striking demonstration that pure path-context similarity is weak for retrieval-style tasks. ⚠️ Did not find a credible third-party *classification*-accuracy paper applying code2vec directly to POJ-104.

### code2seq **[S]**
- Uri Alon, Shaked Brody, Omer Levy, Eran Yahav. "code2seq: Generating Sequences from Structured Representations of Code." **ICLR 2019** (arXiv:1808.01400).
- **Method.** Same AST path-context family as code2vec, but the encoder produces **sequences** (method names, summaries) with an LSTM decoder + attention; demonstrates both captioning and classification uses.
- **Results.** State-of-the-art method naming at the time (Java, C#); abstract framing: "predicting a sequence of subtokens."
- **Limitations / Relevance.** For the project, code2seq matters mainly as evidence that AST paths generalize across tasks; generation head is unnecessary for pattern classification.

### inst2vec / Neural Code Comprehension (NCC) **[V]** (abstract fetched)
- Tal Ben-Nun, Alice Shocher, Torsten Hoefler (ETH Zurich). "Neural Code Comprehension: A Learnable Representation of Code Semantics." **NeurIPS 2018**, arXiv:1806.07336.
- **Method.** Instead of source text, compiles to **LLVM IR** and builds a "contextual flow" graph (data + control flow between IR statements); learns statement embeddings with an RNN via a skip-gram-style objective over contexts; embeddings are language-independent (source-language-agnostic).
- **Results.** Per abstract: "outperforms previous models" and **sets a new state of the art on algorithm classification from code (104-class OJ task)** at publication time; also predicts optimal CPU/GPU mappings. In the later CodeXGLUE clone table, "NCC" variants score MAP@R 39.95 / 54.19 (much below transformer models) — task-dependent.
- **Limitations.** Requires compilation to IR (hard for broken novice code! — a direct practical obstacle for the project); loses identifier semantics.
- **Relevance.** Evidence that **semantic (execution-level) representations help**; but IR-based pipelines fail exactly on syntactically broken submissions, which matters if the classifier must run pre-repair. **Exact inst2vec POJ-104 classification accuracy number: ⚠️ not re-verified from primary source.**

### ast2vec
- **NOT FOUND as a distinct peer-reviewed model with that exact name.** The term appears in the literature informally for AST embedding variants. The concrete lineage covering this niche is: TBCNN (2016) → AST paths (2018–2019) → tree-LSTM/GNN hybrids (2019–2021). Do not cite "ast2vec" in the final paper without pinning down a primary source.

---

## 2c. Pretrained transformers and GNNs applied to algorithm classification

### CodeXGLUE official numbers (clone-detection-POJ-104, MAP@R) **[V]** — from the official README:
| Model | MAP@R |
|---|---|
| code2vec | 1.98 |
| NCC (inst2vec variant) | 39.95 / 54.19 |
| Aroma | 52.02 / 55.39 |
| RoBERTa | 76.67 |
| MISIM-GNN | 82.45 |
| **CodeBERT** | **82.67** |

### CodeBERT **[S]**
- Zhangyin Feng, Daya Guo, Duyu Tang, et al. "CodeBERT: A Pre-Trained Model for Programming and Natural Language." **Findings of EMNLP 2020** (arXiv:2002.08155). Bimodal (code+docstring) transformer; 6 languages; downstream tasks incl. clone detection, defect prediction. On POJ-104 clone task: 82.67 MAP@R [V via CodeXGLUE README]. Applied widely to code classification fine-tuning.

### GraphCodeBERT **[S]**
- Daya Guo, Shuo Ren, Shuai Lu, et al. "GraphCodeBERT: Pre-training Code Representations with Data Flow." **ICLR 2021** (arXiv:2009.08366). Adds **data-flow** as a structural signal into pretraining (guides attention via variable-use graph). Clone-detection-POJ-104: ~80.24 MAP@R per a citing paper's table [S, secondary].

### UniXcoder **[V-structure/S-numbers]**
- Junyi Li, Daya Guo, Duyu Tang, Nan Duan, et al. "Unified Cross-Modal Pre-training for Code Representation." **ACL 2022** (arXiv:2203.03850). Unified encoder over AST + comment + code with prefix adapters; supports understanding + generation. Search-verified snippet: "For POJ-104 dataset, it consists of 104 problems and includes 500 C/C++ programs each" (their clone evaluation). Reported ~82.67 MAP@R class results circulate; ⚠️ exact UniXcoder *classification*-task accuracy on POJ-104 not re-verified here.

### InvPT **[S]**
- Yifeng He, Yundi Xu, Christopher Castro Gaw Gonzalo, Zili Wang, Hao Chen. "Invariant Pretraining for Robust Code Representations." arXiv:2608.15412 (cross-listed cs.LG→cs.SE). Encoder-based pretraining **without paired natural-language data**; evaluates robustness on **transformed code** (semantics-preserving transformations) — relevant because novice code is "distributionally shifted" from pretraining corpora. Fine-tunes on CodeXGLUE Code-classification-POJ104 (UCD-GWX repo). ⚠️ Exact POJ-104 classification accuracy not extracted (full table not surfaced).

### CCT-Code / CCT-LM **[S]**
- "CCT-Code: Cross-Consistency Training for Multilingual..." (arXiv:2305.11626). Claims **new SOTA on POJ-104 (96.73% MAP)** with encoder-based CCT-LM. Useful as a 2023-era ceiling reference [S, secondary — verify before citing].

### MISIM-GNN **[S]**
- Fang et al. (Intel), "MISIM: An End-to-End Neural System for Code Similarity" (arXiv:2006.05265) — GNN over a semantic-enhanced AST (slope-annotated); 82.45 MAP@R on POJ-104 clone task per CodeXGLUE README [V for the number].

### GNN on student programs **[V] (cited within fetched Watanobe full text)**
- M. Lu, Y. Wang, D. Tan, L. Zhao. "Student program classification using gated graph attention neural network." **IEEE Access 9:87857–87868, 2021**. Gated GNN over **AST + data flow**, classifies *student* programs, reports **97% accuracy**. Directly relevant precedent: GNN classifiers work on student code, not just OJ archives.

### CNN on structural features (Watanobe et al., full text fetched — detailed in 2f) **[V]**

---

## 2d. The "AST Patterns for Algorithm Recognition" paper (2024/2026) **[V]**

**Denis Neumüller, Florian Sihler, Raphael Straub, Matthias Tichy** (Ulm University). "Exploring the Effectiveness of Abstract Syntax Tree Patterns for Algorithm Recognition."
- **Venue:** 4th International Conference on Code Quality (**ICCQ 2024**), DOI 10.1109/ICCQ60895.2024.10576984 (IEEE Xplore document 10576984); arXiv posting 2026 (arXiv:2605.06098, note: the *arXiv upload* is recent; the conference paper itself is 2024).
- **Method.** Prototype **AlDeSCo**: a **domain-specific language for expressing AST search patterns** that capture the key features of an algorithm (structural motifs), plus a matching algorithm over the DSL patterns, plus a **catalog of ready-to-use algorithm patterns** created manually from reference implementations (found via web search). (Tech report "Generating an Algorithm Catalog..." — Ulm University, 2025, also referenced.)
- **Evaluation.** On a subset of **BigCloneEval** containing three algorithms (Fibonacci, Bubble Sort, Binary Search):
  - avg **F1 = 0.74**, vs **0.35 for CodeLlama** on the same task;
  - avg **recall 0.62**, vs best clone-detection tool **0.20**.
- **Limitations (from the paper/abstract).** Small evaluation set (3 algorithms); patterns hand-crafted; **weak generalization beyond the fixed catalog of known algorithm classes** (matches the project's preliminary finding); no learner, purely pattern-matching.
- **Relevance.** HIGH. This is the strongest recent baseline family for *rule-based* pattern recognition on ASTs. Crucially, AlDeSCo **stops at recognition** — it does not use the recognized pattern to steer fault localization. That unused downstream step is precisely the project's gap. Reproducibility package: zenodo.org/records/11217414.

---

## 2e. Program concept recognition — the classics (pre-ML)

All verified bibliographically [V/S via ACM DL, MIT AI Lab TR index, Semantic Scholar]:

| Work | Venue/Year | Method summary | Relevance |
|---|---|---|---|
| **Wills, "Automated Program Recognition by Graph Parsing"** (PhD thesis, MIT AI Lab TR-1358) | 1992 | GRASPR system: programs → attributed flow graphs; recognizes **clichés** (common computational structures) by graph parsing with a flow-graph chart parser. Earlier feasibility demo: Wills, "Automated Program Recognition: A Feasibility Demonstration," *Artificial Intelligence* (1990). | The intellectual ancestor of "recognize the algorithmic pattern in the code" — supports framing. |
| **Quilici, "A Memory-Based Approach to Recognizing Programming Plans"** | CACM 37(5):84–93, 1994 | Case-based/memory-based plan recognition: stores known programming-plan instances, retrieves and *adapts* the best match to label code (vs pure parsing). DOI 10.1145/175290.175301. | Anticipates "compare against reference solution structure" — exactly the project's prior mechanism. |
| **Ning, Engberts & Kozaczynski, "Automated Program Concept Recognition" / "Automatic Control Understanding for Natural Programs"** | ~1992–1994 (IJCAI-93 workshop lineage; ACM DL entries) | Hybrid program understanding: recognize abstract concepts via **programming plans** linking concepts to code constructs. | The term "concept recognition" origin; taxonomy vocabulary. |
| **Biggerstaff, Mitbander & Webster, "Program Understanding and the Concept Assignment Problem"** | ICSE 1993 / CACM 37(5), May 1994 | Defines the **concept assignment problem**: mapping human-oriented concepts (e.g., "queue", "binary search") to program fragments. | Conceptual foundation: pattern labels ↔ code regions mapping. |
| **Rich & Waters, The Programmer's Apprentice project** | MIT, 1980s; IEEE Software 1988 retrospective etc. | Knowledge-based assistant with plans and clichés ("The Programmer's Apprentice: research program"; "The Disciplined Programming Methodology" line). | Historical support for "structural knowledge about intent helps reasoning about code." |
| **Taherkhani, "Recognizing Sorting Algorithms with the C4.5 Decision Tree Classifier"** | ICPC 2010 | Hand-selected features → C4.5 decision trees distinguish sorting algorithm implementations (per Watanobe et al.'s bibliography). | Early ML pattern-recognition-on-code precedent. |
| **Shalaby et al., "Automatic Algorithm Recognition of Source-Code Using Machine Learning"** | ICMLA 2017 | ML over code features to recognize algorithm categories. | Bridge work pre-deep-learning. |
| **Bui, Jiang & Yu, "Cross-language learning for program classification using bilateral tree-based convolutional neural networks"** | AAAI-W 2018 | TBCNN extension, cross-language transfer. | Evidence of representation robustness across languages. |

Takeaway for the final paper's Related Work: the field ran a full arc **rule-based plan recognition (1987–1994) → feature/ML (2010–2017) → deep AST models (2016–)**; pattern labels got *coarser* (104 arbitrary problems) even as accuracy rose. The project re-couples the modern stack with the *semantic* pattern vocabulary the classics targeted.

---

## 2f. Classifying algorithms/strategies in real student/OJ code — modern works

### Watanobe, Rahman, Amin & Kabir, "Identifying algorithm in program code based on structural features using CNN classification model" **[V — full text fetched]**
- **Applied Intelligence 53(10):12210–12236 (online 2022-09-23, issue 2023), Springer. DOI 10.1007/s10489-022-04078-y.**
- **Method.** 61,614 C++ accepted solutions from **Aizu Online Judge (AOJ)**, two datasets: **A** (45,398 codes, 6 categories: computational geometry, number theory, flow network, shortest path, query data structures, combinatorial optimization) and **B** (16,216 codes, 7 sorting algorithms: counting/bubble/insertion/merge/selection/shell/quick). Preprocessing: strip comments and **all user-defined identifiers**; keep only **structural features** (if/else, loops, arithmetic/bitwise/assignment/comparison operators, brackets); tokenize to 17 token IDs → one-hot binary matrix → three parallel conv layers (filters 16/32/64 × width 17), maxpool, dropout, FC, softmax.
- **Results.** Best CNN-Arch-III (avg over 10-fold CV): **precision 95.65 / recall 95.85 / F1 95.70**; Dataset A eval F=94.5%, Dataset B (sorting) F=96.9%. Same-data baselines: **LSTM 83.10% acc / 82.02 F**, **BiLSTM 84.64% acc / 84.14 F**. 10-fold cross-validation; extensive hyperparameter sweep (BS 16/32/64, LR 1e-2/1e-3/1e-4, ReLU/LeakyReLU); deeper CNNs (4–6 layers) did not improve.
- **Limitations (authors').** Only C++; token set may not transfer; different problem sets/languages may degrade; classification is category-level, not full pattern semantics.
- **Relevance.** Very high — proves **structural (identifier-free) features alone classify algorithms at ~95%** in real OJ code. Direct template for AlgoRythm's classifier evaluation design (per-category precision/recall, 10-fold CV).

### Lu, Wang, Tan & Zhao (2021), IEEE Access — student program classification via gated graph attention NN over AST+data flow, **97% accuracy** **[V via fetched citation]**. Strongest "works on student code" precedent.

### Strategy-level classification in computing-education venues **[S — to deepen if time permits]**
- "Find One Solution that Solves both Problems!..." (ACM, dl.acm.org/doi/10.1145/3724389.3730788) — students comparing structurally equivalent problems, common algorithmic approach.
- "Teaching Algorithm Design: A Literature Review" (SIGCSE TS 2026) — taxonomy of algorithm-design education work.
- LLM-based classification of student solutions by SOLO taxonomy level (NSF PAR 10591788, 2025) — LLMs rating solution *quality levels*, not algorithm family.
- "Identifying algorithm in program code..." (above) is the flagship for *algorithm* labels; SIGCSE/ITiCSE strategy-classification work found so far targets correctness/complexity, not pattern families. ⚠️ Additional ICER/ITiCSE strategy-classification papers likely exist; not fully enumerated in this pass.

### Search-term coverage for the novelty check (2f/7 overlap)
Searched: "algorithmic pattern classification source code", "recognize two pointers sliding window code", "algorithm idiom recognition", "algorithmic technique identification". Concrete positive hits: **COFO's "Infer the Technique" task** (arXiv:2503.18251) and **AlDeSCo's pattern catalog** (ICCQ 2024). Both recognize the technique; **neither couples it to debugging/localization.**

---

## Implications for the project (Block 2 → design choices)

1. **Classifier architecture ranking for a school-scale project:**
   - **(1) Fine-tuned small transformer (CodeBERT/125M or UniXcoder-base) on own labeled corpus** — best accuracy-per-effort, handles identifiers+structure, runs on one GPU/Colab; expected ≥90% on a 10–15-class pattern vocabulary (extrapolating CodeXGLUE-class results and Watanobe's 95% with a *smaller* model).
   - **(2) AST path-context model (code2vec-style) re-implemented** — small, interpretable, verifiable; matches the existing AlgoRythm AST sandbox; ~85–93% expected.
   - **(3) Structural-feature CNN (Watanobe-style) as a strong simple baseline** — cheap, language-portable, and its "identifier-free" property is a good ablation axis (does pattern signal live in structure or in names?).
   - **(4) AlDeSCo-style DSL pattern matching** — not learned; valuable as an *interpretable prior* component and ablation partner (learned classifier vs hand-written patterns).
2. **Feasible pattern vocabulary** (supported by literature): two pointers, sliding window, binary search, DFS/BFS, DP (with subtypes: 1D/2D/knapsack/LIS), prefix sums, sorting-based, greedy, brute force, hash-map counting, intervals. AlDeSCo's catalog + Watanobe's categories + COFO's technique labels confirm each of these families is recognizable; expect the hardest confusions within graph-traversal variants (BFS vs DFS vs Dijkstra).
3. **Metrics protocol precedent:** 10-fold cross-validation (Watanobe), per-class precision/recall/F1 + confusion matrix, and fixed train/test splits with reported protocol — copy this; POJ-104 history shows split differences make numbers incomparable.
4. **Data path:** no public dataset labels by the project's pattern vocabulary — AlDeSCo's Zenodo package (zenodo.org/records/11217414), COFO (technique labels), CodeXGLUE POJ-104 (C-UDA license, research OK), and AOJ/CodeNet for augmentation are the building blocks; own annotation will be needed (see Block 4 & Synthesis).
5. **Key gap confirmed:** every located work ends at *recognition*. None conditions downstream fault localization on the recognized pattern (checked recognition papers' stated future work + searches in Block 7).
