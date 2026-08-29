# Block 7. Novelty check — aggressive verification of the research gap

**Claim to falsify:** "No prior work uses a classified algorithmic pattern as a structural prior for automatic logical-fault localization in novice code, evaluated against pattern-agnostic baselines with Top-K accuracy."

**Verdict: the gap holds as of 2026-08.** Eight query families below produced NO work matching the claim. Several works are close in spirit and MUST be cited and explicitly differentiated; none closes the gap. Confidence: medium-high — keyword search cannot prove absence, and a final direct check should be repeated 1–2 weeks before submission (cheap insurance).

---

## Query families used (all returned no direct match)
1. `"pattern-aware fault localization" OR "algorithm-aware fault localization"` → no verbatim phrase anywhere; nearest: *context-aware*, *code-aware*, *functionality-aware* FL (all industrial, see below).
2. `fault localization + intended algorithm / algorithmic pattern / algorithm classification + student code + LLM` → nearest: Kozaczynski & Ning's concept recognition (1980s–90s, understanding only); Gopinath UT-Austin dissertation (2015, mentions "intended algorithm" phrasing inside FL theory discussion, no pattern classifier).
3. `plan recognition + novice bugs (PROUST line)` → verified ancestor, see B7.1.
4. `LLM misconception detection in student code (2025–2026)` → adjacent, see B7.3.
5. `fault localization + novice + pattern/prior guided (2024–2026)` → nearest: TLFL, FFL, explainable-LLM FL (all pattern-agnostic).
6. `"two pointers"/"sliding window"/"dynamic programming" + bug detection/localization + student code` → **nothing**; the search's own synthesis: "the gap between pattern-aware pedagogy and automated fault localization seems to be an open opportunity."
7. Algorithm recognition papers' own future-work sections (AlDeSCo ICCQ 2024; Watanobe 2023; COFO 2025) → none proposes coupling recognition to debugging.
8. `Fault localization student programs + algorithm label/metadata` → nothing (works that use task metadata use it only to fetch reference solutions, see VsusFL/FFL in Block 3).

---

## B7.1 Closest prior art, ranked by overlap

### #1 — PROUST: intention-based diagnosis of novice bugs (the intellectual ancestor)
- **W. L. Johnson & E. Soloway. "PROUST: Knowledge-Based Program Understanding." 1983/1985 (tech report ERIC ED237055; AAAI 1984 companion "Intention-Based Diagnosis of Programming Errors"); journal version W. L. Johnson, "Understanding and Debugging Novice Programs," *Artificial Intelligence* 52(1), 1990** (214+ citations).
- **What they did:** a library of stereotypical **programming plans** + goals of the assignment; PROUST infers the *intentions* behind a novice's Pascal code, then diagnoses bugs as **differences between intended plans and implemented code**; explains misconceptions like a tutor.
- **Overlap:** the core idea "knowing the intended structure narrows the bug search" — **yes, this is the same conceptual mechanism.**
- **Differences:** (1) plan knowledge is **hand-written per assignment domain** (e.g., the Rainfall Problem), not a *classified* pattern over open task sets; (2) purely knowledge-based/symbolic — no learning, no classifier in the loop; (3) **no quantitative Top-K localization evaluation against baselines** (evaluation was qualitative; N-version validations came later); (4) pre-dates ML entirely.
- **How to cite:** "PROUST established intention-based diagnosis conceptually in the 1980s; we revisit its core insight with a modern learned pattern classifier and measurable Top-K localization, on a benchmark scale impossible for hand-built plan libraries."

### #2 — Hoq et al., EDM 2025: AST-attention localization of logical errors in student code (closest *learned* work)
- **M. Hoq et al. "Automated Identification of Logical Errors in Programs." EDM 2025** (educationaldatamining.org/EDM2025/proceedings/2025.EDM.long-papers.85).
- **What they did:** modified **SANN** (Subtree-Attention Neural Network, AST-embedding) trained **only on correctness labels** on CodeWorkout (Java CS1: 368 students, 57,670 submissions, 50 problems); sigmoid attention highlights AST subtrees likely containing logical errors; correctness prediction 0.87 acc/F1 (beats code2vec 0.81, ASTNN 0.83); on 5 expert-validated problems, error-region identification **recall 83–97%, precision 82–92%**; subtrees reused for knowledge tracing (DKT AUC 72.45 vs 65.87).
- **Overlap:** learned localization of logical errors in novice code via AST attention — very close in data and task.
- **Differences:** (1) **no pattern conditioning whatsoever** — the model never knows which algorithmic technique the solution should use; (2) no pattern classifier anywhere in the pipeline; (3) subtree-level highlighting, no line-level Top-1/3/5 vs FL baselines (no SBFL/MBFL/LLM comparison); (4) error taxonomy (syntactic/strategic/conceptual) applied only by human experts post hoc; (5) authors state mapping errors→misconceptions is future work.
- **Status: does NOT close the gap. Strongest "compare against" citation for the learned baseline family.** Also proves AST-attention works on student code (feasibility support).

### #3 — FaR-Loc: Functionality-Aware LLM fault localization (closest *naming*)
- **"Enhancing LLM-based Fault Localization with a Functionality-Aware approach" (FaR-Loc), arXiv:2509.20552 (Sept 2025).**
- **What they did:** method-level FL on **Defects4J** (industrial Java): LLM writes a functional description of the failing behavior from test+stack trace; **semantic retrieval** (UniXcoder embeddings) of functionally similar covered methods; LLM re-ranks. Beats SoapFL/AutoFL by +14.6%/+9.1% Top-1, +19.2%/+22.1% Top-5; UniXcoder embeddings up to +49% Top-1.
- **Overlap:** uses "functional intent" as a prior signal — nearest by name and spirit in industrial FL.
- **Differences:** (1) intent = free-text failing-behavior description, **not a discrete algorithmic-pattern class**; (2) retrieval over *this project's own methods*, not knowledge of the intended technique; (3) industrial repos, not novice code; no pattern classifier; no education angle.
- **Status: does NOT close the gap; must be cited as the industrial neighbor.**

### #4 — VsusFL / FFL / CLARA (education FL that uses *a correct program* as reference)
- VsusFL (JSS 2023): matches faulty program's variables to **one correct reference program** via bipartite graph + Hungarian algorithm, then diff's value traces (Block 3). FFL (ICSME 2022): syntactic + semantic reasoning vs reference. CLARA (ITiCSE 2018): clusters correct solutions, repairs via trace alignment.
- **Overlap:** all exploit *reference-solution structure* — conceptually adjacent to "structural prior."
- **Differences:** the prior is a **specific other program** (or cluster), not a transferable **pattern class** that generalizes across tasks; none conditions on the algorithmic technique; none tests whether pattern knowledge (vs a concrete reference) suffices.
- **Status: cite as "reference-based" family; the project's pattern prior is deliberately more compact and task-transferable.**

### #5 — Multi-correct-program boosting (nearest spectrum-level analog)
- **"Boosting Spectrum-Based Fault Localization via Multi-Correct Programs" (IEICE Trans. 2024):** uses multiple correct submissions to sharpen spectra.
- **Differences:** re-weights coverage spectra only; no pattern concept; no novice-focus claims. **Cite and differentiate.**

### #6 — Explainable LLM FL for programming assignments
- **arXiv:2509.25676 (Sept 2025):** LLM-driven fine-grained error locations + explanations for assignments. Pattern-agnostic; no classifier conditioning; complements rather than closes.

### #7 — Algorithm-recognition works stop at recognition
- AlDeSCo (ICCQ 2024): pattern recognition via AST-pattern DSL — explicitly evaluation on recognition only. Watanobe et al. (Applied Intelligence 2023): classification only. COFO (arXiv:2503.18251): "Infer the Technique" task defined, no downstream use. **None proposes downstream localization.**

### #8 — Misconception discovery (2025–2026 wave)
- **McMiner (arXiv:2510.08827, Oct 2025):** LLM tool that *discovers* misconceptions in student code (not predefined ones). CSEDU 2026 targeted-feedback paper. ETH Sonkar et al.: LLMs model student errors.
- **Overlap:** misconception/error semantics in novice code.
- **Differences:** classification/discovery of error *types*, not pattern-conditioned fault *localization* with Top-K accuracy.

---

## B7.2 Residual risks to the novelty claim (honest list)
1. **Non-English literature** (Chinese, Russian venues) may contain pattern-conditioned FL — search coverage here was English-only. Mitigate with one CNKI/DBLP sweep before submission.
2. **Very recent preprints** (2026 H2) may appear between now and the fair; re-run queries `pattern-aware fault localization`, `algorithm-conditioned debugging`, `intended algorithm fault localization` before camera-ready.
3. **The claim must be phrased precisely** to stay true: the novelty is the *coupling* (pattern classifier → pattern-conditioned localization prior → measured Top-K gain vs pattern-agnostic baselines on novice code) — not any individual component.

## B7.3 One-line positioning for the paper
"Intention-based debugging dates to PROUST (Johnson & Soloway, 1985); modern FL for novices is pattern-agnostic (SBFL/MBFL degrade, LLMs degrade with difficulty — Xu et al. 2025; Hoq et al. 2025), and algorithm recognition stops at recognition (Neumüller et al. 2024; Watanobe et al. 2023). We close the loop: a learned pattern classifier supplies a structural prior that measurably improves fault localization accuracy on novice code."
