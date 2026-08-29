# Block 5. Methodological precedents for the experiment design

Verification legend: **[V]** verified from fetched primary source; **[S]** credible snippets; **⚠️** unverified.

---

## 5.1 Top-K accuracy and EXAM — exact definitions as used in the located novice-FL literature

**[V] Yang, Mei & Yang (IJSEKE 2025):**
- **Top-N (N=1,3,5):** localization counts as success if a truly faulty statement is among the first N of the produced ranking. Tie handling: **conservative (worst rank)** — if a faulty statement ties with k others at score s, it is assigned the WORST position of the tie block. (Justification cited: 73.58% of developers inspect only the top-5.)
- **EXAM score:** the fraction of statements a developer must inspect before reaching the first faulty one = (rank of first faulty statement)/(total statements); lower is better; reported as dataset average.

**[V] Xu et al. (arXiv:2512.03421):** LLM protocol — ground truth = labeled buggy line number; lines numbered in the prompt to prevent off-by-one output errors; output parsed from JSON; **each configuration repeated 5 times and averaged** (LLM stochasticity); Top-1/3/5 counted per 503-program dataset; difficulty binned into 5 levels (~100 programs each).

**[S] Pearson et al., "Evaluating and Improving Fault Localization," ICSE 2017** (web.eecs.umich.edu PDF; 582+ citations): canonical demonstration that FL-technique comparisons must account for **confounds in evaluation** (test-suite composition, tie handling, metric choice); statistically re-tests prior published claims and supports only 7/10. **Cite this when justifying the project's evaluation protocol.** Companion practitioner guide: hackthology.com "How to evaluate statistical fault localization" (Dietz) [S].

## 5.2 Statistical tests for comparing two methods on one dataset — precedents found

| Test | What it compares | Precedent located | Use in this project |
|---|---|---|---|
| **One-sided Wilcoxon signed-rank** | paired nonparametric comparison of per-difficulty-bin accuracies | arXiv:2512.03421 §6.2 [V]: o3 vs GPT-3.5, α=0.05, p=0.03125 (Condefects, BugT), n.s. p=0.15625 (Codeflaws) | compare pattern-conditioned vs baseline Top-N across difficulty bins / repeated runs |
| **McNemar's test (paired binary)** | per-program hit/miss of Top-N for two techniques on the SAME programs | mlxtend guide (rasbt.github.io/mlxtend/user_guide/evaluate/mcnemar/); Wikipedia/StatPearls; mid-p vs asymptotic variants — Fagerland, Lydersen & Laake [S] | THE natural test for "with-prior vs without-prior Top-N hits" (paired, binary, same items) |
| **5×2cv paired t-test / paired t-test over folds** | classifier accuracy across resampled train/test splits | Dietterich 1998 lineage (standard ML evaluation; mlxtend documents 5×2cv) [S] | classifier comparison (pattern classifier variants) |
| **Bootstrap CIs (percentile, BCa)** | interval estimate for Top-N accuracy / accuracy differences | Efron 2020 (PMC7958418); Simkus 2026 Comm. Stat. (CI-type comparison); luferrer/ConfidenceIntervals GitHub [S] | report CI on every headline Top-N delta |
| **Point-Biserial correlation** | binary (Top-5 hit) vs continuous predictor | IJSEKE 2025 [V]: +0.35/+0.37, p<0.05 | correlate "pattern-prior strength" with success |
| **Spearman rank correlation** | rankings (EXAM vs predictor) | IJSEKE 2025 [V]: 0.64/0.78, p<0.0001 | sanity analyses |

## 5.3 Ablation "with prior / without prior" precedents (any domain)

1. **[V] The prompt-component ablation in arXiv:2512.03421 is itself a context-ablation template:** five orthogonal prompt ingredients (persona, intent, reason, CoT, sort), each removed in turn; effect measured on Top-1. The project's "pattern label as prior" can plug in as exactly such an orthogonal component — added to the prompt of an LLM localizer, and separately into a classical ranker.
2. **[V] CodeXGLUE protocol:** single-model, same split, same metric across tasks — the standard ablation discipline (change one thing).
3. **[V] Watanobe et al. 2023:** 10-fold CV + architecture-family ablation (CNN vs LSTM vs BiLSTM on identical inputs) — the model-selection ablation template at school-computable scale.
4. **[S] ISEF-scale precedent style:** algorithms-track winners typically present system + ablation + statistical test + efficiency table; the exact winning-project anatomy is in Block 8.

## 5.4 How many examples are "enough" — evidence from the located studies

| Study | n per comparison | Effect direction |
|---|---|---|
| IJSEKE 2025 MBFL (Python/Java) | 150 programs per language | differences of 5–15 Top-N points reported as meaningful |
| arXiv:2512.03421 (LLM FL) | 503 per dataset (×5 runs) | 1–2 point Top-1 gaps treated as real only after Wilcoxon |
| FFL (ICSME 2022) [S] | few hundred student programs | similar |
| VsusFL (JSS 2023) [V] | 422 faulty submissions | +9–90% Top-N vs baselines |

Power reasoning for planning (own derivation, to state in the paper): McNemar's test needs *discordant* pairs. If prior-conditioning flips ~15% of programs (hit→hit discordance b, miss→hit c with c>b), then with n=300, b+c≈45 discordant pairs; exact McNemar at α=0.05 detects |c−b| ≥ ~16 (roughly a 60/40+ split of discordants). **⇒ n ≈ 300 faulty programs (≈30 per pattern × 10 patterns) is the defensible minimum; n ≈ 500 matches the 2512.03421 protocol.** ⚠️ Own derivation — validate with a pilot before locking (pilot: 30 programs, measure discordance rate, plug into a power calculator).

## 5.5 Evaluation-design hazards documented in literature (cite all)
- **Ties dominate novice rankings** — must use worst-rank tie-breaking (IJSEKE 2025 [V]; tie-problem study 2024 [S]).
- **Data leakage** — Codeflaws suspected contaminated; prefer leakage-free slices (BugT approach) (2512.03421 [V]).
- **~40% of novice programs violate FL preconditions** (fail all tests) — exclude or handle separately (Araujo et al. 2016 [V-cited]).
- **Confounding in FL evaluation generally** — Pearson et al. ICSE 2017 [S].
- **LLM stochasticity** — 5-run averaging mandatory (2512.03421 [V]); report mean±sd.
