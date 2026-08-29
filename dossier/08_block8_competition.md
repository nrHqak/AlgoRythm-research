# Block 8. Competition requirements — ISEF (Systems Software) and РКНП (Kazakhstan)

Verification legend: **[V]** verified from fetched official page/PDF; **[S]** credible snippets; **⚠️** unverified.

---

## 8.1 ISEF — International Rules: Human Participants research (what the project triggers)

**If the project includes ANY testing on people** (even a small pilot measuring how fast classmates find a bug with/without pattern hints), ISEF classifies it as **Human Participants research**. Exact requirements [V — fetched official rules page "Rules for All Projects" + Human Participants pages]:

- **"Projects involving human participants... must be reviewed and approved by a local or regional IRB or SRC prior to the start of experimentation"** — i.e., BEFORE collecting any data. Retroactive approval is invalid; signature dates on forms must precede the first data point [V + Forms FAQ].
- **Required forms (2027 set already published on sspcdn):**
  - **Form 1** — Checklist for Adult Sponsor;
  - **Form 1A** — Student Checklist + **Research Plan** (see below for required contents);
  - **Form 1B** — Approval Form (signatures before experimentation);
  - **Form 3** — Risk Assessment Form;
  - **Form 4** — Human Participants and Informed Consent (one per participant; sample: `sspcdn.blob.core.windows.net/files/Documents/SEP/ISEF/2027/Forms/4-Sample-Informed-Consent.pdf`).
- **Informed consent/assent:** participation may begin **only after participants have voluntarily given informed consent/assent**; for minors: **child assent + parent/guardian permission**, both in writing [V].
- **IRB composition** (per ISEF rules [S — official page truncated in fetch]): minimum 3 members including a science teacher, a school administrator, and a person knowledgeable about the research area; for minimal-risk education studies a school-based IRB suffices.
- **"Minimal risk" definition:** no more risk than everyday life (educational surveys/quizzes normally qualify) — still requires prior approval, just a lighter review [S].
- **Common pitfall documented by fair guides:** "surveys among classmates without IRB pre-approval is the single most frequent Form 4 violation" [S — exstemplar.com guide].
- **Research Plan (Form 1A) required contents [V — verbatim list]:**
  1. Why is the research important?
  2. What problem(s) will you investigate?
  3. What will be used as a control in the research?
  4. A procedure summary — tell exactly what you will do; **if any materials or methods are potentially risky, explain what safety precautions will be taken**;
  5. Bibliography: list at least five (5) major references (e.g., science journal articles, books, internet sites) from your library research;
  6. If human participants: describe procedures for obtaining informed consent/assent and parental permission, and the risks;
  7. If vertebrate animals/microbial/etc. — analogous sections (not applicable here).
- **Other "Rules for All Projects" constraints that bite [V]:**
  - Abstract: **≤250 words**, in English;
  - **Generative AI may not be used for: constructing/planning the research plan, writing the abstract, creating the poster, or citations** — the research itself must be the student's own; AI may be used only as an object/tool of study (here: the LLM localizer IS the object of study — legitimate);
  - Project window: research eligible if conducted **between Jan 2026 and May 2027** (for ISEF 2027);
  - Team limit 3; grades 9–12; under 20 by ISEF;
  - Data book (logbook) strongly expected; research paper recommended.
- **Practical implication for AlgoRythm data:** *pre-existing* logs collected for platform operation (not for the study) are still human-derived data; if used, either (a) fully anonymize + aggregate so no individual is identifiable (then argue "not human participants research" — but get the local SRC to confirm that judgment IN WRITING before use), or (b) run Form 4 protocol. Do not mix the two without the written confirmation.

## 8.2 ISEF Systems Software (SOFT) category — description & judging

**[V — official categories page]**
- **SYSTEMS SOFTWARE (Code: SOFT)**: "The study or development of software, information processes or methodologies to demonstrate, analyze, or control a process/solution." Includes **algorithms**, cybersecurity, databases, operating systems, programming languages. Sponsor: Microsoft.
- **Grand Awards per category:** 1st $6,000 / 2nd $2,400 / 3rd $1,200 / 4th $600; category 1st-place winners compete for Top Awards (Yancopoulos Innovator Award $100k etc.).
- **Judging criteria (all categories):** Creative Ability; Scientific Thought (+ Engineering Goals); Thoroughness/Skill; Clarity; Teamwork. For algorithms projects, judges expect: a clear hypothesis, a **quantitative comparison vs baselines**, ablation, statistics, and honest limitations.
- **Past SOFT winners (calibration):**
  - ISEF 2024: First Award SOFT044 ("Solving Second..." — truncated in results); Michelle Wei (San Jose) took the **Best of Category/Best of Award in Systems Software**; full lists in the official press releases.
  - ISEF 2025: SOFT008 Second Award; Texas "AssemblyComplete" Fourth; Singapore team 4th prize.
  - Full winner lists: societyforscience.org press releases "Regeneron ISEF 2024/2025 Full Awards"; project database isef.net/viewAll?category=SOFT.
- **Calibration takeaway [S — pattern across winner titles]:** winning SOFT projects pair a working system with a measured benchmark improvement; a pure platform demo scores below a platform + controlled experiment. The fault-localization study provides exactly the experimental core.

## 8.3 РКНП — Республиканский конкурс научных проектов (РНПЦ «Дарын», daryn.kz)

**[V — official РКНП page + official Regulation PDF «Положение РКНП 2024» fetched from daryn.kz/wp-content/uploads/2024/09/Положение-РКНП-2024.pdf]**

| Item | Requirement |
|---|---|
| Organizer | РНПЦ «Дарын» (Republican Scientific-Practical Center "Daryn") under the Ministry of Education (Просвещения) of Kazakhstan |
| Participants | 8–11 grade students (national id-based registration via school) |
| Sections | Mathematics; **Informatics = Направление II "Информатика, информационные и коммуникационные технологии"**; physics; chemistry; biology; ecology; geography; social sciences; technical sciences |
| Stages (2024 timings, expect ~same for 2027) | school stage by **20 September**; city/regional stage by **20 October**; **republican stage: second ten-day period of December** (г. Астана/Алматы venue rotates) |
| Submission package | заявка от школы; научный проект (исследовательская работа) + **тезисы**; презентация; справка о самостоятельности (antiplagiarism declaration); рекомендации НОУ/руководителя |
| Defense | **up to 10 minutes presentation + questions** (poster/presentation based) |
| Evaluation | 10-point scale; criteria per Regulation: актуальность, новизна, эффективность методов исследования, глубина раскрытия темы, научная и прикладная значимость, соответствие результатов задачам, оформление (matches the user's list) |
| Passage rates | per official page: 45% of regional participants pass to the republican stage; in Informatics recently **86 projects → 54** [V page statistics] |
| ISEF linkage | Republican winners/призёры enter the **Daryn selection to represent Kazakhstan at Regeneron ISEF**; international quotas per РНПЦ announcements (ISEF, BRICS/GMOIRs lines) [V page section "МЕЖДУНАРОДНЫЕ СОБЫТИЯ"] |
| Language | project and defense in Kazakh or Russian; **ISEF abstract must additionally be in English** (ISEF rule [V 8.1]) |

**⚠️ Caveat:** the fetched Regulation is the 2024 edition; re-download the 2026/2027 «Положение» from daryn.kz/rknp-ru in September 2026 (the page states the new cycle's dates) — deadlines shift slightly year to year, but the December republican-stage pattern has been stable.

**Reverse timeline anchor:** republican stage ≈ **mid-December 2026** for ISEF 2027 candidacy (NOT Feb 2027 — the Dec-2026 republican РКНП result feeds the spring selection; the user's "end of February 2027" likely refers to the final ISEF-candidate defense round announced by Daryn; treat BOTH dates as deadlines in the Synthesis timeline: material must be finished by mid-November for December, polished through February).

---

# Block 9. Ethics — anonymization & informed consent practices for minors' data

(Concise but complete; sources: ISEF rules above + standard educational-ML practice.)

## 9.1 Informed consent & assent
- **Parent/guardian permission** + **child assent** for every minor participant (ISEF Form 4 pattern [V 8.1]); school administration approval letter.
- Assent text for a bug-finding pilot must state: purpose, what the participant does (find a bug in a short program), time (~15–20 min), data stored (screen recording? none; time + correctness), that grades are unaffected, withdrawal without penalty.
- **Timing rule:** consent materials approved by IRB/SRC **before** recruitment — recruitment materials count as part of the protocol [V 8.1].

## 9.2 Anonymization standard practices (educational ML with minors)
- **Pseudonymous IDs** generated at collection (never school+name); identity mapping kept by a single custodian (teacher), not in the research dataset.
- **Data minimization:** collect only what the experiment needs (code snippet, pattern label, fault location, timing); no names, no birthdates, no device fingerprints.
- **Aggregation & k-anonymity in reporting:** report per-pattern/per-difficulty aggregates; avoid publishing any submission that could identify a student via unique problem sequences.
- **Secure storage:** local encrypted storage or restricted cloud folder; no third-party transfer without explicit consent scope; **if student code is sent to an LLM API, that is a third-party data transfer — must be disclosed in the consent form and the research plan** (or use only locally-runnable models for the human-pilot part).
- **Deletion policy:** define retention (e.g., "raw data deleted after defense; anonymized aggregate may be published").
- **Standards alignment:** FERPA (US) and GDPR Art. 8 (minors' consent age 13–16 by jurisdiction) are the reference norms cited by SIGCSE/ICER-style papers; Kazakhstan's **Law No. 94-V "On Personal Data and Their Protection" (21 May 2013)** requires consent for processing personal data of minors via legal representatives — consistent with the above protocol [S — cite the law number; verify current amendment state before submission].

## 9.3 Publication ethics specific to this project
- The main experiment (datasets: Codeflaws/ConDefects/BugT/QuixBugs + synthetic injections) involves **no humans** → only licensing/acknowledgment obligations (C-UDA etc., see Block 4).
- The optional human pilot → Form 4 protocol above; keep it **optional and separable** from the core result so a paperwork delay cannot sink the main claim.
- Antiplagiarism/самостоятельность справка for РКНП: keep the logbook (git history of the research repo counts) as evidence of independent work; note ISEF's explicit AI-usage boundary [V 8.1].
