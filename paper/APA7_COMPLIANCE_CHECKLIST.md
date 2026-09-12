# APA 7 Compliance Checklist — `APA7_PAPER_DRAFT.md`

Status as of this pre-results draft. "Markdown-only" items are things that
cannot be verified or fully realized in a plain-text `.md` file and require
action when the manuscript is transferred into a word processor or LaTeX
template for actual submission.

## Title

| Item | Status | Note |
|---|---|---|
| Concise, describes the study | ✅ Done | "Algorithm-Pattern-Specific Structural Priors for Large Language Model Fault Localization in Novice Code: A Pre-Registered Calibration Pilot" |
| No abbreviations in title | ✅ Done | — |
| Title case, bold, centered, upper half of title page | ⚠️ Markdown-only | Bold/centering not representable in plain Markdown; apply in final formatting |
| Author name(s) | ❌ **Open — student action required** | Placeholder only. Per `AGENTS.md` §3.2 item 7, generative AI may not author the final research plan/abstract/citations; the student must supply and take ownership of authorship. |
| Institutional affiliation | ❌ **Open — student action required** | Placeholder only |

## Abstract

| Item | Status | Note |
|---|---|---|
| 150–250 words | ✅ Done | ~230 words (recount at final formatting; Markdown word count is approximate) |
| Single paragraph, no indentation | ⚠️ Markdown-only | Apply in final formatting |
| Results sentence present but placeholder | ✅ Done | `[RESULT PENDING — TO BE INSERTED AFTER A VALID PILOT RUN COMPLETES.]` |
| Covers purpose, method, and (pending) results | ✅ Done | — |
| No citations in abstract | ✅ Done | Verified — none present |

## Keywords

| Item | Status | Note |
|---|---|---|
| Italicized "*Keywords:*" run-in line, indented, immediately below abstract | ⚠️ Markdown-only | Present as `*Keywords:*` line; apply indentation and italics in final formatting |
| 4–7 lowercase terms, comma-separated | ✅ Done | 8 terms listed — trim to ≤7 at final formatting if the venue enforces a hard cap |

## Heading Levels

| Item | Status | Note |
|---|---|---|
| Consistent hierarchy | ⚠️ Partial / needs remapping | This draft uses Markdown `##` for what should be APA **Level 1** (centered, bold, title case: Introduction, Related Work, Method, Measures, Statistical Analysis Plan, Reproducibility, Results, Discussion, Threats to Validity and Limitations, Future Work, Conclusion, References) and `###` for **Level 2** (flush left, bold, title case: e.g., "Dataset: ConDefects-Python," the four Discussion scenario headings). No Level 3–5 headings were needed given this paper's structure. |
| "Introduction" heading present | ⚠️ Stylistic deviation, disclosed | Strict APA 7 omits an explicit "Introduction" heading and repeats the paper's title instead at that position. This draft uses an explicit "Introduction" heading for clarity given its use as a working/review document; correct to the title-repeat convention if submitting to a venue that enforces it strictly. |
| Table/Figure numbering does not collide with heading levels | ⚠️ **Known deviation — see Tables/Figures below** | — |

## Citations

| Item | Status | Note |
|---|---|---|
| Author–date in-text format, e.g., (Author, Year) or Author (Year) | ✅ Done | Used throughout |
| Multi-author citations follow APA 7 et al. rules (name all authors up to 20 at first citation for works with ≤20 authors; use "et al." after the first author for 3+ authors on subsequent citations) | ⚠️ Partial | Several long author-list works (e.g., Fincher et al., Lister et al.) are spelled out at first mention per convention; verify "et al." is applied consistently on any repeat citation if the same source is cited more than once in the final version |
| Every in-text citation has a matching reference entry | ✅ Verified in this pass | Cross-checked manually; see below |
| No citation to a source not read/verified by the project | ⚠️ Disclosed | Several sources are cited based on the project's own literature-review dossier's verification labels ([V]/[S]); sources marked [S]-only or flagged incomplete in the dossier are flagged identically in the reference list below rather than silently upgraded to [V] status |

## References

| Item | Status | Note |
|---|---|---|
| Alphabetical by first author surname | ✅ Done | — |
| Hanging indent | ⚠️ Markdown-only | Not representable in plain Markdown; apply in final formatting |
| DOIs as `https://doi.org/...` links | ✅ Done where known | 24 of 34 entries carry a DOI verified in the project's own literature-review dossier |
| No fabricated DOIs or bibliographic fields | ✅ Done | Every entry lacking full verification is explicitly flagged in-line rather than completed with an invented value (see `PAPER_SOURCE_AUDIT.md` for the full list) |
| Incomplete references flagged rather than invented | ✅ Done | 10 of 34 entries carry an explicit `[flag: ...]` note (Araujo et al.; du Boulay/O'Shea/Monk; Johnson 1990; Jones/Harrold/Stasko; Gupta et al.; Hoq et al.; Li et al.; Wong et al. DStar; Wong et al. 2016 survey; Xu et al. 2025; Yang/Mei/Yang) |
| Reference count | 34 entries | See `PAPER_SOURCE_AUDIT.md` for per-entry sourcing |

## Tables

| Item | Status | Note |
|---|---|---|
| Numbered sequentially, "Table N" above italic title-case caption | ⚠️ **Known deviation, disclosed** | This draft numbers the three Results tables **Table 1–3** per the task's explicit instruction (to match the required Results skeleton exactly), and labels the four Method tables **Table M1–M2** (only 2 are used; M1 sampling funnel, M2 execution parameters) to avoid collision. **Strict APA 7 requires one continuous numbering sequence for the whole paper** (Method tables would become Table 1–2, Results tables Table 3–5). Renumber sequentially at camera-ready. |
| Table notes (*Note.* lines) used for necessary qualifications | ✅ Done | Present on Table M1 and Table 2 |
| No vertical rules; horizontal rules only at top, below header, at bottom | ⚠️ Markdown-only | Markdown tables render with full grid lines; apply APA table borders in final formatting |
| All three Results tables contain explicit placeholders, no fabricated values | ✅ Verified | Every data cell reads `[RESULT PENDING]` |

## Figures

| Item | Status | Note |
|---|---|---|
| At least one figure planned | ⚠️ **Not yet produced** | Two figures are named as pending in the Results section (Figure 1: sampling-funnel flow diagram; Figure 2: per-condition Top-K bar chart with bootstrap CIs) but neither has been rendered as an actual image. **Action required**: produce both once (a) the funnel counts are finalized/re-verified [already available now, independent of results] and (b) valid Top-K data exist. |
| Figure numbering does not collide with table numbering conventions | ✅ Done | Separate Figure/Table sequences per APA convention |

## Statistical Notation

| Item | Status | Note |
|---|---|---|
| Italicized statistical symbols (*n*, *p*, *M*, *SD*, etc.) | ⚠️ Markdown-only | Represented with Markdown `*...*` italics where used (e.g., *n* = 30, *p* ≤ .05); verify italics render correctly after conversion out of Markdown |
| *p*-values reported without leading zero | ✅ Done | e.g., ".031" not "0.031" in the power table |
| Equations for EXAM and McNemar given in display math | ✅ Done | Present in Measures and Statistical Analysis Plan; uses LaTeX-style `$...$`/`$$...$$` delimiters — confirm the final rendering target (Word equation editor, LaTeX, or a Markdown renderer with MathJax) supports this syntax, or convert manually |
| Effect-size/CI reporting convention (95% CI) | ✅ Planned, placeholder | Table 2 specifies the CI method (program-clustered percentile bootstrap, 10,000 iterations, seed 20260908) even though values are pending |

## Abbreviations

| Item | Status | Note |
|---|---|---|
| Each abbreviation defined at first use | ✅ Done | SBFL, MBFL, LLM, FL, CI all spelled out at first occurrence |
| Abbreviations used consistently thereafter | ✅ Done | — |
| "EXAM\*" notation explained at first use | ✅ Done | Explicitly distinguished from published EXAM in Measures |

## Citation/Reference Correspondence

Manually cross-checked in this pass: every in-text citation in
`APA7_PAPER_DRAFT.md` (Introduction, Related Work, Method, Measures,
Statistical Analysis Plan, Discussion, Threats to Validity, Future Work) has a
corresponding entry in the References list, and every entry in the References
list is cited at least once in the body text. No orphaned citations or
unused references were found in this pass. Re-verify this correspondence
after any future edit to either the body text or the reference list, since it
is not enforced automatically in a plain Markdown file.

## Other APA 7 Mechanics Not Yet Addressed (flag for final formatting pass)

- Running head / page header (APA 7 professional papers do not require a
  running head unless the venue requests one; student papers omit it by
  default — confirm the target venue's requirement).
- Page numbers.
- 1-inch margins, double-spacing, 12-point serif font (Times New Roman) or an
  accessible sans-serif alternative per APA 7's 2020+ guidance — none of
  these are meaningful in a Markdown file and must be set in the final
  word-processor template.
- Level of indentation for block quotations (none used in this draft, so not
  applicable at present).

## Outstanding Blockers Before This Paper Can Be Submitted Anywhere

1. Author name(s) and affiliation must be supplied by the student researcher(s)
   (ISEF/competition AI-authorship constraint, `AGENTS.md` §3.2 item 7).
2. The `pattern_source: "AST rule"` vs. oracle-human-label discrepancy
   (`APA7_PAPER_DRAFT.md`, Method, "Oracle Pattern Labels") must be resolved.
3. The 10 flagged, incompletely verified reference entries must be checked
   against primary bibliographic sources.
4. Table numbering must be made sequential across the whole paper at
   camera-ready (see "Tables" above).
5. Figures 1 and 2 must be produced.
