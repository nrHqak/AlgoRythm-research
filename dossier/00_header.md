# RESEARCH DOSSIER
## Pattern-Conditioned Fault Localization for Novice Programmers — literature, datasets, methodology, competition requirements

**Compiled:** 2026-08-29 · **For:** AlgoRythm research project (РКНП Kazakhstan, Informatics, Direction II → Regeneron ISEF Systems Software / Algorithms)
**Research question:** Does using a classified algorithmic pattern as a structural prior improve automatic logical-fault localization accuracy in novice code, vs pattern-agnostic localization?

**Contents:** Block 1 Theory (notional machines, comprehension, CPH, error taxonomies) · Block 2 Algorithm classification · Block 3 Fault localization for novices · Block 4 Datasets · Block 5 Methodology · Block 6 Visualization tools · Block 7 Novelty check (verdict: gap confirmed) · Block 8 ISEF/РКНП requirements · Block 9 Ethics · Synthesis & Recommendations.

**Verification legend used throughout:** [V] verified from fetched primary source; [S] credible snippet only; ⚠️ unverified; NOT FOUND honestly reported. Every located work carries: title / authors / year / venue / link / method / exact numbers / stated limitations / relevance.

**Headline findings (details inside):**
1. **The research gap is real** (Block 7): intention-based debugging dates to PROUST (1985), but no modern work conditions fault localization on a *classified algorithmic pattern*; the 2024–2026 wave of recognition work (AlDeSCo, Watanobe, COFO) explicitly stops at recognition.
2. **Baselines are well-quantified** (Block 3): MBFL Top-5 ≈ 61% on novice Python (IJSEKE 2025); 2025 reasoning-LLMs reach Top-5 ≈ 81–89% but degrade with task difficulty and cost $0.015–0.49/program (arXiv:2512.03421).
3. **No dataset joins pattern + bug + location** (Block 4) → a relabeled corpus (~300–500 programs) is a publishable contribution in itself.
4. **Any human pilot requires IRB/SRC pre-approval BEFORE data collection** (Block 8) — calendar it in September 2026 or keep the core experiment non-human.
