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


---

# Block 1. Theoretical foundations

**Project context.** Research question: does using a *classified algorithmic pattern* (e.g., "this must be a two-pointer solution") as a structural prior improve automatic logical-fault localization in novice programmers' code, compared to pattern-agnostic localization? Hypothesis: knowing the intended pattern lets the localizer check pattern-specific failure points first (two pointers → pointer-shift and stop conditions; DP → base cases and transitions), yielding higher Top-1/Top-3/Top-5 accuracy.

**This block covers.** (1a) Notional machines; (1b) program comprehension and debugging research; (1c) the Competent Programmer Hypothesis (CPH) and why it does *not* transfer to novice code; (1d) taxonomies of novice logical errors and the taxonomy gap that motivates the project.

**Verification key.** Compiled 2026-08-29 from web search + publisher/abstract pages. Items marked **[V]** were confirmed against a fetched primary page, DBLP, publisher record, or multiple independent snippets including the exact bibliographic record. Items marked **[S]** were seen only in search snippets (title/venue verified, but full text not fetched). Items marked **⚠️ UNVERIFIED** could not be confirmed and should be re-checked before citation in the final paper. Where a widely repeated detail could not be verified, it is explicitly flagged rather than asserted.

---

## 1a. Notional machines: the gap between the novice's mental model and actual execution

### Overview

The notional-machine (NM) literature is the theoretical backbone for the claim that novices do not naturally see what a program will *do*: they hold a machine model in which the computer "understands" intent, while executed reality differs. The project's core idea — supplying an *intended algorithmic pattern* as a localization prior — operationalizes this gap: the pattern is an explicit, expert-level fragment of the notional machine of algorithms, used where the novice's own mental machine is unreliable.

### Core works

| # | Work | Venue/Year | Identifier | Status |
|---|------|-----------|------------|--------|
| A1 | du Boulay, O'Shea & Monk — "The Black Box Inside the Glass Box: Presenting Computing Concepts to Novices" | Int. J. Man-Machine Studies 14, pp. 237–249, 1981 | ScienceDirect / Sussex author page | [V] |
| A2 | du Boulay — "Some Difficulties of Learning to Program" | J. Educational Computing Research 2(1), pp. 57–73, 1986 | DOI 10.2190/3LFX-9RRF-67T8-UVK9 | [V] |
| A3 | Sorva — "Notional Machines and Introductory Programming Education" | ACM TOCE 13(2), Article 8, 2013 | DOI 10.1145/2483710.2483713 | [V] |
| A4 | Sorva — *Visual Program Simulation in Introductory Programming Education* (PhD thesis) | Aalto University, 2012 | ResearchGate / Semantic Scholar record | [V] |
| A5 | Fincher et al. (12 authors) — "Notional Machines in Computing Education: The Education of Attention" | ITiCSE-WGR '20, pp. 21–50, 2020 | DOI 10.1145/3437800.3439202 | [V] |
| A6 | Dickson, Brown & Becker — "Engage Against the Machine: Rise of the Notional Machines as Effective Pedagogical Devices" | ITiCSE '20, pp. 159–165, 2020 | DOI 10.1145/3341525.3387404 | [V] |

### A1. du Boulay, O'Shea & Monk (1981), "The Black Box Inside the Glass Box: Presenting Computing Concepts to Novices"

- **Authors:** Benedict du Boulay, Tim O'Shea, John Monk. **Venue:** *International Journal of Man-Machine Studies*, vol. 14, pp. 237–249 (1981). Reprinted 1989 in Soloway & Spohrer (eds.). Author list and pagination confirmed via du Boulay's Sussex publications page and the archived journal header ("Man-Machine Studies (1981) 14, 237–249"). **[V]**
- **Method:** A position/conceptual paper from the Computers in the Curriculum project (Chelsea College). It analyzes why novices fail to predict program behavior and proposes that teaching must make the execution model explicit.
- **Key content (this is the first formulation of the notional machine idea):** the computer as the novice sees it is a "black box"; teachers should replace it with a "glass box" — a *notional machine*, a specified, teachable abstraction of the machine that executes programs, whose state (variables, flow of control) can be examined. Two persistent confusion sources highlighted: (i) programs are *static text* but execution is *dynamic*; (ii) different layers of the machine (language constructs vs. underlying state changes) get conflated. Recommended techniques include tracing, concrete models, and explicit discussion of "what the machine does next."
- **Limitations (as viewed by later literature):** conceptual paper, no empirical evaluation; the machine described is oriented to Basic/Logo-era languages; later authors note the definition is loose and the paper does not give criteria for choosing among candidate machines (this critique is made explicit in A5/A6 — [S] for the attribution of that critique).
- **Relevance:** origin of the project's central metaphor: an expert's "glass box" includes *algorithm-level* machinery (plans, invariants), not just language-level machinery. The project tests whether handing the localizer an explicit algorithm-level glass box (the classified pattern) compensates for the novice's black box.

### A2. du Boulay (1986), "Some Difficulties of Learning to Program"

- **Venue:** *Journal of Educational Computing Research* 2(1), pp. 57–73, February 1986. DOI 10.2190/3LFX-9RRF-67T8-UVK9. ~1,158 citations per Google Scholar (snippet figure). **[V]**
- **Method:** analytic synthesis of the difficulties novices face, grounded in the author's SOLO/logo teaching experiments and the 1981 framework.
- **Key content — the classic difficulty list (five areas; widely reproduced in later reviews):**
  1. **General orientation** — what programming is *for*; understanding the goal and the nature of the task.
  2. **The notional machine** — understanding what the computer will actually do with a program (the execution model of A1).
  3. **Notation** — syntax and semantics of the language; scaling difficulty with the number of constructs.
  4. **Structures** — acquiring higher-level "plans"/idioms (e.g., running totals, counted loops) and composing them; novices lack the stereotyped chunks experts have.
  5. **Pragmatics** — planning, testing, debugging: managing the whole activity, including error-finding skills novices rarely have.
- **Limitations:** no quantitative study of error frequencies; based on Logo/procedural languages of the early 1980s; the five areas overlap and are not operationalized as measurable categories.
- **Relevance:** area 4 ("structures" = plan/idiom knowledge) is exactly the layer the project manipulates; area 5 (pragmatics) motivates teaching debugging explicitly, which automatic fault localization can scaffold.

### A3. Sorva (2013), "Notional Machines and Introductory Programming Education"

- **Venue:** *ACM Transactions on Computing Education* 13(2), Article 8, June 2013. DOI 10.1145/2483710.2483713. ~331 citations per Semantic Scholar; ~889 per Google Scholar (snippet figures). **[V]**
- **Method:** integrative review and position paper that revitalized the NM concept after two decades of neglect; connects NMs to mental models, misconceptions, visualization and feedback.
- **Key content:**
  - Canonical definition (quoted from the paper via ACM full-text snippets): a notional machine is *"a characterization of the computer in its role as executor of programs in a particular language or a set of related languages."*
  - Argues the machine should be an explicit **target of instruction** (taught, tested, discussed), not something students are expected to absorb implicitly.
  - Discusses **notional machines at different levels of abstraction**: from low-level memory/bytecode-style machines up through language-level machines to higher-level conceptual machines — i.e., there is not one NM but a stack of them, and different pedagogical goals pick different levels.
  - Points to promising techniques: program visualization/simulation (VPS), tracing exercises, and questions about learners' own code (later developed by others into QLCs — questions about learners' code).
- **Limitations:** review/position paper; acknowledges little empirical evidence existed on which NM choices help learning; the "typology" is a discussion framework rather than a validated classification instrument. (Specific sub-typology labels beyond the levels-of-abstraction discussion could not be re-verified from fetched text — treat finer-grained "roles" lists as ⚠️ UNVERIFIED.)
- **Relevance:** gives the project vocabulary for saying that a *classified algorithmic pattern* is a high-level notional-machine element: just as novices need an explicit machine for `while`-loops, they (and tools built for them) benefit from explicit machines for two-pointer/DP-style solution structures.

### A4. Sorva (2012), *Visual Program Simulation in Introductory Programming Education* (PhD thesis)

- **Institution:** Aalto University, School of Science, Department of Computer Science and Engineering; Doctor of Science (Technology); advisor Lauri Malmi; May 2012. **[V]**
- **Method:** builds and studies **UUhistle**, a tool for *visual program simulation* (VPS): the student, not the software, manipulates the visualization — moving arrows, updating variable boxes, growing the call stack — to explain step-by-step how a program executes. Several empirical studies of CS1 students using VPS for learning and assessment.
- **Key results:** VPS functioned both as a learning activity and as an assessment technique (students' execution-model competence can be graded by watching their simulation actions); the thesis connects VPS directly to making the notional machine concrete and to repairing mental models. (Exact effect sizes were not re-verified from the thesis text — ⚠️ treat quantitative claims as unverified here; the journal follow-up "Students' ways of experiencing visual program simulation", *Computer Science Education* 2013, with J. Lönnberg, is the citable empirical companion [S].)
- **Limitations (stated in thesis, per abstract/summaries [S]):** small-scale studies; tool-specific results; VPS is time-consuming to use at scale.
- **Relevance:** the strongest existing evidence that *explicit step-level execution modeling* is learnable and gradeable. A fault localizer that explains a bug at pattern level ("the left pointer's shift condition is wrong") presumes exactly the machine-level fluency VPS trains — the project can position its tool as a diagnostic complement to VPS-style exercises.

### A5. Fincher, Jeuring, Miller, Donaldson, du Boulay, Hauswirth, Hellas, Hermans, Lewis, Mühling, Pearce & Petersen (2020), "Notional Machines in Computing Education: The Education of Attention"

- **Venue:** ITiCSE-WGR '20 (Working Group Reports of the 2020 ACM conference on Innovation and Technology in Computer Science Education), pp. 21–50. DOI 10.1145/3437800.3439202. Full 12-author list confirmed via DBLP. **[V]**
- **Important clarification for the dossier owner:** the title often guessed ("Notional Machines and Programming Language Semantics in Undergraduate Education") is actually the title of **Dagstuhl Seminar 19281** (July 2019), whose report (Guzdial et al., *DagRep* 9(7), DOI 10.4230/DagRep.9.7.1) spawned the working-group line. The ITiCSE working-group report proper is A5 above. **[V]**
- **Method:** an international working group's systematic review + conceptual analysis: first-hand account of the origin of NMs, a systematic literature review tracking the use and development of the concept, and a set of definitional characteristics.
- **Key content:** defines NMs as *"a pedagogic device to assist the understanding of some aspect of programs or programming"*; documents that the term has been used loosely across 40 years; argues for treating the NM as a designed, selectable artifact ("education of attention" — pointing learners at the right aspects of execution); identifies open questions (which machine, for whom, at which level, with what evidence).
- **Limitations (stated):** the field still lacks empirical comparisons of alternative NMs; the report is a research agenda, not a measurement framework.
- **Relevance:** the authoritative modern citation for "notional machine" claims; also the source of the framing that choosing a machine = choosing what learners attend to — parallel to the project's claim that choosing a pattern prior = choosing what the localizer attends to.

### A6. Dickson, Brown & Becker (2020), "Engage Against the Machine: Rise of the Notional Machines as Effective Pedagogical Devices"

- **Venue:** ITiCSE '20, pp. 159–165. DOI 10.1145/3341525.3387404. Free PDF at twistedsquare.com/Notional-Machines.pdf (co-author's site). **[V]**
- **Method:** position/survey paper distilling what teachers should do with NMs; motivates a "rise" of NMs as everyday pedagogical devices rather than theory relics.
- **Key content:** re-states the NM as "an abstract model of an execution environment" and "a pedagogic device to assist the understanding of some aspect of programs"; argues most effort went into tools and misconceptions, while **explicit teacher-facing use of NMs** is underdeveloped; sketches classroom moves (visualizations, contrasting machines, discussing execution explicitly).
- **Limitations:** conceptual; no controlled evaluation.
- **Relevance:** supports the transfer claim that explicit models (here: explicit algorithm patterns) are legitimate pedagogical devices whose value a tool can operationalize.

### Follow-up papers, 2015–2026 (list with details)

| Paper | Authors (first 3) | Venue/Year | Identifier | Note |
|-------|-------------------|-----------|------------|------|
| "Towards a Notional Machine for Runtime Stacks and Scope: When Stacks Don't Stack Up" | John Clements, Shriram Krishnamurthi | ICER '22, pp. 206–222 | DOI 10.1145/3501385.3543961 | **[V]** Builds a specific NM for stacks/scope; shows novices' "stacks don't stack up" misconceptions; demonstrates NMs can be designed per-concept and evaluated. |
| "Evaluating the Utility of Notional Machine Representations to Help Novices Learn to Code Trace" | Veronica Chiarelli, Nadia Markova, Kasia Muldner | ICER '23 | DOI 10.1145/3568813.3600119 | **[V]** (bibliography) Two studies comparing NM *representations* (e.g., anthropomorphic/actor-style vs. other) for teaching tracing; found representations differ in usefulness ⚠️ exact numbers unverified (ACM full page returned 403). Directly relevant: NM choice changes tracing performance → model choice changes error-detection performance. |
| "Computational Thinking and Notional Machines: The Missing Link" | Bhagya Munasinghe, Tim Bell, Anthony V. Robins | ACM TOCE 23(4), pp. 1–27, Dec 2023 | DOI 10.1145/3627829 | **[V]** Argues CT concepts and NMs are two views of the same underlying ideas; situates NM theory within modern CS curricula. |
| "Notional Machines and Programming Language Semantics in Education" (seminar report) | Guzdial et al. | Dagstuhl Seminar 19281 report, 2019 | DOI 10.4230/DagRep.9.7.1 | **[S]** Community-forming agenda paper combining computing education + formal semantics. |
| "Explanations of Data Systems Concepts in CS Education" (WG report collecting/categorizing NMs for databases) | D. Miedema et al. | ITiCSE-WGR 2025 | DOI 10.1145/3760545.3783971 | **[S]** Shows the NM research program is still active and is being *categorized by subdomain* — precedent for treating "the NM of a domain" as a designed object. |
| 2025 ITiCSE Working Group proposal on collecting notional machines across subtopics | (WG proposal) | iticse.acm.org/2025 | working-group proposals page | **[S]** Evidence of ongoing community effort. |

**Additional unverified but noteworthy [S]:** "Capturing and Characterising Notional Machines" (ITiCSE '20 companion short paper); "Using Notional Machines to Automatically Assess Students' …" (SIGCSE 2024 poster, DOI 10.1145/3626253.3635524 — NMs + QLCs generating questions about learners' own code); "Creating Notional Machines to Support Learners" (DOI 10.1145/3770761.3777279). Together these show a live 2024–2026 thread on *machine-assisted* NM work — the closest adjacent space to the project's tooling.

### Sub-section synthesis (1a)

The NM literature establishes, across 45 years, that (i) novices' execution models are systematically incomplete and goal-directed, (ii) making the machine explicit helps, and (iii) machines can be *designed per concept* (Clements & Krishnamurthi). What it has **not** done is design or evaluate a notional machine **at the algorithm-pattern level** (two pointers, sliding window, DP) as a *structural prior inside a fault-localization tool* — prior work uses NMs only for teaching, visualization, or question generation. Framing: *pattern-aware localization is notional-machine scaffolding applied to diagnosis instead of instruction.*

---

## 1b. Program comprehension: how novices read and understand code

### Overview

Comprehension research explains *what representations* a reader builds (beacons, plans, control-flow/data-flow models) and *where comprehension breaks down* for novices; the debugging literature shows these breakdowns cause failed fault finding. Together they predict what the project exploits: a reader (human or algorithm) that knows the *intended plan* can localize faults faster, because faults live at plan boundaries.

### Expert-comprehension theories

| # | Work | Venue/Year | Identifier | Status |
|---|------|-----------|------------|--------|
| B1 | Brooks — "Towards a Theory of the Comprehension of Computer Programs" | Int. J. Man-Machine Studies 18(6), pp. 543–554, 1983 | ScienceDirect S0020737383800315 | [V] |
| B2 | Pennington — "Stimulus structures and mental representations in expert comprehension of computer programs" | Cognitive Psychology 19(3), pp. 295–341, 1987 | DOI 10.1016/0010-0285(87)90007-7 | [V] |
| B3 | Letovsky — "Cognitive processes in program comprehension" | J. Systems and Software 7(4), pp. 325–339, 1987 (workshop version 1986) | DOI 10.1016/0164-1218(87)90032-X | [V] |
| B4 | von Mayrhauser & Vans — "Program Comprehension During Software Maintenance and Evolution" | IEEE Computer 28(8), pp. 44–55, 1995 | DOI 10.1109/2.402076 | [V] |

**B1. Brooks (1983).** Method: a *sufficiency theory* of program comprehension (a computational/theoretical account, not a controlled experiment). Key content: comprehension as **top-down hypothesis generation and verification** driven by domain knowledge; **beacons** — distinctive code features (idioms, naming, statement patterns) that cue hypotheses about the program's goals; **systematic vs. opportunistic** reading strategies, with bottom-up processing as backup when top-down knowledge fails. Limitations: a theory "sufficient" in principle, validated only informally against protocol evidence; beacons were elaborated empirically later (e.g., Wiedenbeck's studies [S]). Relevance: **beacons are the strongest single theoretical argument for the project.** An algorithmic pattern is a beacon *set* at a higher abstraction level (e.g., two pointers: symmetric loop + opposing index updates); a pattern-aware localizer is literally a beacon-driven hypothesis generator, as prescribed by Brooks, and Top-k accuracy measures how well its hypotheses rank.

**B2. Pennington (1987).** Method: controlled experiments in which expert programmers comprehended a ~200-line program and were probed with recognition/recall and question tasks, separating micro- vs. macro-structure. Key results: experts build multiple mental representations — a **program model** (control-flow and data-flow relations) and a **situation model** (what the program does in the domain); the **control-flow representation dominates** — text-structure knowledge is acquired first and function abstraction lags. Limitations: single program, single language (FORTRAN-era), experts only; later work showed representation dominance is task- and knowledge-dependent [S]. Relevance: novices stall at the program-model level and never form a situation model; the project supplies the missing situation model ("this is a two-pointer partition") so that failures can be interpreted against intent.

**B3. Letovsky (1986/1987).** Method: think-aloud protocol study of experienced programmers comprehending an unfamiliar program; analysis of their knowledge sources and cognitive processes. Key content: comprehension is **opportunistic** — driven by questions ("why?", "how does X work?"); programmers make **conjectures** (assumed correct knowledge) that are checked lazily; knowledge types include plan knowledge, rules of discourse, and implementation-side knowledge. Limitations: small number of participants (case-study scale); descriptive model. Relevance: (i) the "conjecture" concept maps onto *assumed-correct pattern scaffolding* in the project (the pattern is assumed, deviations are faults); (ii) question-driven comprehension anticipates Ko & Myers' interrogative debugging (below).

**B4. von Mayrhauser & Vans (1995).** Method: synthesis of large-scale field and protocol studies of professional maintainers into an **integrated meta-model** of comprehension. Key content: four interacting components — the **top-down model**, the **situation model**, the **program model**, and a persistent **knowledge base**; plus "as-needed" processes; maintainers switch strategies by task, and in large systems systematic comprehension is replaced by opportunistic, hypothesis-driven search. The citing literature credits this line with the estimate that maintainers spend ~50–90% of their time on comprehension [S]. Limitations: industrial, large-scale code; expert maintainers; qualitative strategy models. Relevance: canonical citation that maintenance/debugging ≈ comprehension; and the meta-model's top-down/situation components are precisely what a pattern classifier provides to the localizer.

### Novice comprehension

**B5. Soloway, Bonar & Ehrlich (1983), "Cognitive strategies and looping constructs: an empirical study."** *CACM* 26(11), pp. 853–860. DOI 10.1145/358436 (PDF: dl.acm.org/doi/pdf/10.1145/358436). **[V]** Method: empirical study (Yale Cognition and Programming Project) of which looping strategy novices choose when writing a summation loop, comparing "loop-and-a-half" (test in the middle / while-true-break), read-ahead while-loops, etc. Key results: novices strongly prefer the **loop-and-a-half** strategy matching their natural "first do, then check" plan; language constructs that force a different order impose extra cognitive cost — i.e., novices map language constructs onto *cognitive plans* imperfectly. Limitations: single task (summing loop), lab setting. Relevance: earliest hard evidence that novice code embodies *plans*, and bugs arise at the language↔plan interface — the plan level is the right granularity for the project's priors.

**B6. Robins, Rountree & Rountree (2003), "Learning and Teaching Programming: A Review and Discussion."** *Computer Science Education* 13(2), pp. 137–172. DOI 10.1076/csed.13.2.137.14200. ~2,712 citations (T&F snippet). **[V]** Method: narrative literature review synthesizing novice/expert differences, knowledge types, and mental models. Key content: organizes novice knowledge into syntax, semantics, and other categories; highlights the role of **problem-solving plans/schemas** and **program comprehension** as bottlenecks; discusses consistency of mental models and the "generation gap" (tracing vs. writing). Recommends teaching semantic* levels and program dynamics explicitly. Limitations: review (no new data); pre-2003 literature. Relevance: the standard "state of novice understanding" citation; its plan/schema framing is the educational side of the pattern-prior idea.

**B7. Dehnadi & Bornat (2006), "The Camel Has Two Humps" + critiques.** Middlesex University working paper (2006), eis.sla.mdx.ac.uk/research/PhDArea/saeed/paper1.pdf. **[V]** (existence/venue; full text not fetched). Method: a "semantic profiling" test administered *before* instruction; claims the test predicts which students will pass the first programming course, implying a bimodal distribution of innate ability. Key results: original paper reported pre-test scores separating eventual pass/fail groups. **Critiques/replications (all [V] as to existence):** independent replications largely failed; Bornat himself published **"Camels and humps: a retraction"** (2014, eis.mdx.ac.uk/staffpages/r_bornat/papers/camel_hump_retraction.pdf), conceding the evidence does not support that some people *cannot* learn to program; Basnet et al. (2018, *EURASIA J. Math Sci Tech Ed*) found no robust bimodality in CS1 grade distributions; the ICER 2022 registered-reports paper (DOI 10.1145/3501385.3543971) uses this history as the canonical example of replication difficulty. Relevance: cautionary tale for the project's own claims — reported "innate ability" effects dissolved under replication, so any pattern-prior accuracy gains must be replicated across cohorts/datasets and pre-registered if possible.

**B8. Perkins & Martin (1986), "Fragile knowledge and neglected strategies in novice programmers."** In Soloway & Iyengar (eds.), *Empirical Studies of Programmers*, Ablex. ACM DL record DOI 10.5555/21842.28896. **[V]** Method: clinical/interview study of first-year BASIC students while they worked on programs. Key content: novice knowledge is **fragile** — present but unreliable in use (fragmented, inert, misplaced); and novices possess but **neglect strategies** (systematic testing, careful tracing, stepwise debugging) that would rescue them. Limitations: qualitative, small n, BASIC-era. Relevance: gives the project its user-story: the novice usually *has* the knowledge that the pattern's failure points exist but neglects to check them; a pattern-aware localizer operationalizes the neglected strategy.

### Debugging-specific literature

**B9. Lister, Adams, Fitzgerald, Fone, Hamer, Lindholm, McCartney, Moström, Sanders, Seppälä, Simon & Thomas (2004), "A Multi-National Study of Reading and Tracing Skills in Novice Programmers."** ITiCSE 2004 Working Group Reports (*ACM SIGCSE Bulletin* 36(4), pp. 119–150). DOI 10.1145/1041624.1041673. **[V]** Method: multi-institution test battery (7 countries) of code reading, tracing, and "explain in plain English" tasks. Key results: the working group concluded that the **majority of students performed much more poorly than expected**; students trace better than they abstract purpose (the "explain in plain English" gap), supporting a neo-Piagetian reading of novice competence: tracing precedes holistic explanation. Limitations: instrument-driven; institutions self-selected; per-question percentages vary across sites (specific aggregate percentages not re-verified here ⚠️). Relevance: establishes tracing as the measurable base skill; the project's Top-k localization task is a cousin of tracing (state-tracking to find where intent breaks).

**B10. Venables, Tan & Lister (2009), "A closer look at tracing, explaining and code writing skills in the novice programmer."** ICER '09 (also *Computer Science Education* 19(4), 2009). DOI 10.1145/1584322.1584336. **[V]** Method: follow-up quantitative study relating tracing, explaining, and writing scores. Key results: tracing+explaining performance explains roughly **46% of the variance** in code-writing performance (figure as reported in citing/abstract snippets [S]); students scoring below ~50% on tracing struggle to explain code. Limitations: single institution; correlational. Relevance: quantifies the tracing→debugging pipeline the project builds on.

**B11. Fowler, Smith IV, Hassan, Poulsen, West, Heeren et al. (2022), "Reevaluating the relationship between explaining, tracing, and writing skills in CS1 in a replication study."** *Computer Science Education* 22(3)?, 2022. DOI 10.1080/08993408.2022.2079866; open PDF at par.nsf.gov/servlets/purl/10340072. **[V]** (bibliography; full text not fetched). Method: conceptual replication of Lopez et al. (2008) with a larger cohort (non-majors, Python; >600 students per snippets). Key results: per Semantic Scholar's summary, the study **replicates a slightly simplified skill hierarchy** (sequence → tracing → explaining → writing) [S — result-level wording]. Limitations: non-major population; simplified hierarchy. Relevance: the tracing/writing hierarchy is robust at scale — supports using trace-grounded features in a novice-code localizer.

**B12. McCauley, Fitzgerald, Lewandowski, Murphy, Simon, Thomas & Zander (2008), "Debugging: a review of the literature from an educational perspective."** *Computer Science Education* 18(2), pp. 67–92. DOI 10.1080/08993400802114581. **[V]** (This is the correct venue of the review the user recalled as "~2008"; it is a journal review, not a conference paper.) Key content: organizes debugging research around definitions of debugging, what skilled debuggers do, what novices do, and instructional interventions; notes debugging is rarely explicitly taught and novices' strategies are poorly matched to fault types. Relevance: baseline reference for "pattern-agnostic" debugging instruction — the state the project compares against.

**B13. Fitzgerald, Lewandowski, McCauley, Murphy, Simon, Thomas & Zander (2008), "Debugging: finding, fixing and flailing, a multi-institutional study of novice debuggers."** *Computer Science Education* 18(2), pp. 93–116. DOI 10.1080/08993400802114508. **[V]** Method: multi-institution qualitative/quantitative study of how CS1/CS2 students debug; strategy coding of think-aloud sessions. Key results: novice debugging is characterized by **flailing** — unplanned trial-and-error with weak hypothesis generation; students rarely use systematic strategies. Limitations: self-report/observational; US-centric institutions. Relevance: "flailing" is the human baseline the project's automatic localizer must beat; a pattern prior is a hypothesis generator that directly counteracts flailing.

**B14. Murphy, Lewandowski, McCauley, Simon, Thomas & Zander (2008), "Debugging: the good, the bad, and the quirky — a qualitative analysis of novices' strategies."** SIGCSE '08, pp. 163–167. DOI 10.1145/1352135.1352191. **[V]** *Authorship note:* this companion paper is by **Murphy et al.** — Sue Fitzgerald is *not* an author (she leads B13); the two are easy to conflate. Key results: categorizes novice strategies (e.g., bisection-style narrowing vs. line-by-line vs. quirks like relying on print statements); finds most novices lack effective strategies. Relevance: same as B13, strategy-level.

**B15. Ko & Myers — the Whyline line of work.**
- **"Designing the Whyline: A Debugging Interface for Asking Questions About Program Behavior."** CHI 2004, pp. 151–158. DOI 10.1145/985692.985712. **[V]** Method: design + user study of the Whyline for the end-user language Alice: the user selects *why did / why didn't* questions about output; the tool answers from recorded execution with causal chains. Key results: supported question-driven fault diagnosis for non-programmers (2004 effect sizes not re-verified ⚠️).
- **"Debugging Reinvented: Asking and Answering Why and Why Not Questions about Program Behavior" (the Java Whyline).** ICSE 2008, pp. 301–310. DOI 10.1145/1368088.1368130; PDF: cs.cmu.edu/~NatProg/papers/Ko2008JavaWhyline.pdf. **[V]** Method: records full execution traces; constructs the space of *why/why-not* questions and answers them via causal chains linking output → UI events → source. Key results (abstract, [S] via snippet quoting the PDF): **"Preliminary results suggest that Whyline users were twice as successful in half the time"** on real bug reports vs. conventional tools; Best Paper, ICSE 2008; Most Influential Paper, ICSE 2018. Limitations (stated): trace recording scales poorly; limited question space; small-n evaluation [S].
- **"Finding causes of program output with the Java Whyline."** CHI 2009, pp. 1569–1578. DOI 10.1145/1518701.1518942. **[V]** — mechanism paper (causality extraction at scale).
- Relevance: the Whyline answers *behavioral* questions; the project's pattern prior tells the localizer *which behavioral questions are structurally plausible first* (two pointers: "why didn't the pointers meet?"). Closest systems-software ancestor of the proposal.

**B16. Baron & Feitelson (2024), "Why Is Recursion Hard to Comprehend? An Experiment with Experienced Programmers in Python."** ITiCSE 2024. DOI 10.1145/3649217.3653636. **[V]** Method: controlled experiment isolating which structural aspects of recursion impede comprehension. Key results: difficulties concentrate on **base-case recognition and stopping conditions** even for experienced programmers (finding as characterized in citing work [S]; exact statistics unverified). Relevance: a *pattern-specific* failure-point result — exactly the "DP/recursion: check base cases first" logic of the project's hypothesis, shown empirically for one pattern family.

**2020–2026 note on tracing↔debugging.** Beyond B11/B16, recent empirical work connects tracing competence to debugging in novices (e.g., trace-based skill dimensions in *Computer Applications in Engineering Education*, 2023, identifying tracing/explaining/writing as distinct-but-related skills [S]; "Enhancing Novice Programmers' Debugging Skills Through Systematic Education", 2024 [S]). No 2020s paper was found linking *pattern classification* to localization — the adjacent modern literature is LLM-based (see 1d, MacNeil et al. 2024).

### Sub-section synthesis (1b)

Readers localize faults by matching code against *intended plans* using beacons, and they fail when the plan inventory is missing or the plan-to-code mapping breaks at plan boundaries (loop guards, pointer updates, base cases); novice debugging studies confirm the failure mode ("flailing"). The project's contribution slot: turn the expert's plan knowledge into a machine-usable prior and measure the accuracy gain — nobody in the reviewed corpus has done that for algorithmic-pattern-level plans.

---

## 1c. The Competent Programmer Hypothesis (CPH)

### Original formulation

**C1. DeMillo, Lipton & Sayward (1978), "Hints on Test Data Selection: Help for the Practicing Programmer."** *Computer* (IEEE) 11(4), pp. 34–41 (some sources cite 34–43; the arXiv reference list gives 34–41). DOI 10.1109/C-M.1978.218136. All three authors at Georgia Tech at the time. **[V]**

- **What it did:** introduced program mutation as a practical testing approach, resting on two assumptions: the **Competent Programmer Hypothesis** and (in the companion 1979 paper "Program Mutation: An Approach to Software Testing") the **coupling effect**.
- **CPH wording.** Verified verbatim quote *as quoted by Ahmed et al. (arXiv:2104.02517v2, §2, [V])*: DeMillo et al. relied on the assumption that *"Programmers have one great advantage that is almost never exploited: they create programs that are close to being correct!"* The canonical paraphrase used across the mutation-testing literature ([V] across multiple sources): competent programmers write programs that are **close to correct**; a faulty program differs from some correct program P' by **a few simple syntactic deviations**, which mutation operators can simulate. Budd's thesis states it formally as: "The competent programmer hypothesis asserts that with high probability either P is correct or some program in Σ (the set of mutants of P) is the correct program" **[S — quoted in a search summary of the gwern.net-hosted thesis PDF; re-verify against the PDF before quoting in print]**.
- The arXiv paper also notes DeMillo et al. **offered no proof** of the assumption ([V]).
- **Limitations:** the hypothesis is an *assumption*, motivated by observation of professional development practice, not an empirical law; the paper's scope is testing (test-data selection), not education.

**C2. Budd (1980), *Mutation Analysis of Program Test Data* (PhD thesis, Yale University).** Advisor: Richard Lipton, "who originated the concept of mutation analysis" (thesis acknowledgment [V] via gwern.net-hosted text snippets). Also available as DTIC report ADA068118. **[V]** Method: first implementation of a mutation system (the "Pilot Mutation System"), plus experiments formalizing mutation analysis. Key content/results: formalizes CPH and the coupling effect; empirically studies mutant behavior and test adequacy. Limitations: 1980-scale hardware and program corpora. Relevance: the second canonical source for CPH; shows the hypothesis was always about *professional programmers* producing nearly-correct code.

### What Knight & Leveson (1986) actually showed — and the common misattribution

**C3. Knight & Leveson (1986), "An Experimental Evaluation of the Assumption of Independence in Multiversion Programming."** *IEEE Transactions on Software Engineering* SE-12(1), January 1986. DOI 10.1109/TSE.1986.6312924. **[V]**

- **Method:** 27 independently developed versions of an anti-missile launch-decision program, written independently by programmers at two universities from the same specification; versions run against a very large set of randomly generated inputs (on the order of a million, per secondary summaries ⚠️ — re-verify the exact count against the paper) and coincident (same-input) failures recorded.
- **Key results:** the independence assumption — the "fundamental axiom" of N-version programming, namely that independently developed versions will fail independently — was **rejected**: different versions failed **on the same inputs** significantly more than independence predicts. Correlated faults arise despite independent people, methods, and languages.
- **Role of CPH (clarification):** this paper is **not** the origin of CPH and does not propose it; CPH comes from DeMillo–Lipton–Sayward (1978) / Budd (1980). What K&L test is a *different but cousin* assumption used in fault-tolerant software: that residual faults in independently written versions are independent. The two are related because both are optimistic assumptions about error distributions across programmers. **[V for the paper's content and the independence-axiom framing; the explicit CPH↔K&L contrast is this dossier's synthesis.]**
- **Relevance:** K&L is the *professional-programmer* evidence that errors are **correlated across developers** — shared specification blind spots, shared idioms. If even independent professionals correlate, novices — who share teaching materials, copy each other, and hold the same misconceptions — should correlate *far more*. That is the empirical bridge from 1c to 1d.

### Why CPH does not transfer to novice code (papers that discuss or test this)

| # | Paper | Venue/Year | Claim about CPH for novices | Status |
|---|-------|-----------|------------------------------|--------|
| C4 | Hu, Ahmed, Mechtaev, Leong & Roychoudhury — "Re-Factoring Based Program Repair Applied to Programming Assignments" (tool: Refactory) | ASE 2019 | Student submissions are "often severely incorrect," in **stark contrast** to CPH; motivates repair via matching against *other students'* correct solutions rather than minimal-edit mutants | [V] (authors/venue/DOI 10.1109/ASE.2019.00044; the "stark contrast" phrasing seen in the author-hosted PDF snippet [S]) |
| C5 | Tanujaya, Voigtländer & Westphal — "Mutating Sample Solutions to Improve Prolog Exercise Tasks and Their Test Suites" | WLP@KI 2022, Trier | The search summary states the paper argues CPH "just does not apply" to student exercises and proposes mutating sample solutions to simulate realistic student mistakes | [V] bibliography (wlp2022.dfki.de/data/papers/004.pdf); the CPH-non-applicability attribution is **[S]** — re-verify wording |
| C6 | Clegg — *The Application of Mutation Testing to Enhance the Automated Assessment of Introductory Programming Assignments* (PhD thesis, Univ. of Sheffield, supervisor Phil McMinn) | 2021 | Student programs can **violate CPH** (multiple, compounding faults); **higher-order mutants** are more analogous to real student programs than first-order mutants | [V] bibliography (ben.clegg.li/pdf/bclegg-thesis-2021.pdf); the HOM-analogy attribution is **[S]** |
| C7 | Perretta, DeOrio, Guha & Bell — "On the Use of Mutation Analysis for Evaluating Student Test Suite Quality" | ISSTA 2022 | (Adjacent, positive result) mutation analysis *works* for grading student test suites: strong correlation between mutation score and manually-seeded-fault detection; moderately strong vs. all-pairs grading | [V] (DOI 10.1145/3533767.3534217) |
| C8 | Ahmed, Stein, Herbold, Trautsch & Grabowski — "A new perspective on the competent programmer hypothesis through the reproduction of bugs with repeated mutations" | arXiv 2021 (v2 2023); journal version in *Software Testing, Verification and Reliability*, DOI 10.1002/stvr.1874 | Tests CPH itself on professional bug databases: real bugs often require **chains of many mutations** to reproduce; concludes CPH "seems to be true" in the weak sense, **but standard mutation operators miss important real-bug types** | [V] (arXiv page + Wiley page) |

**Reading of the evidence.** Three lines converge: (i) novices violate CPH's *near-correctness* premise (C4, C5, C6 — multiple severe faults, non-minimal deviations, missing constructs); (ii) even professionals' real faults are not always small/syntactic (C8 — long mutation chains); (iii) yet mutation-style *differences-from-correct* remain useful in education (C7) — CPH fails as an assumption of minimal single-token deviation but survives weakly as "a nearby correct program exists." Pivotal framing for the project: **pattern-agnostic localizers inherit CPH's bias toward minimal, syntax-adjacent deviations, which is systematically wrong for novices; pattern priors re-anchor the search on semantic fault positions novices actually produce (boundaries, base cases, pointer updates).**

**Renamings for education contexts.** A search for "competent student hypothesis" / "competent learner hypothesis" as an established term returned **NOT FOUND** — no published renaming of CPH for education was identified after multiple attempts. The nearest established education-side analog is the **intention-based diagnosis** assumption of PROUST (Johnson & Soloway, "Intention-Based Diagnosis of Novice Programming Errors," AAAI-84; expanded as "Understanding and debugging novice programs," *Artificial Intelligence* 52(1), 51–97, 1991 [S for exact pages/volume]): novice errors are **systematic and traceable to intended plans and underlying misconceptions**, not random — which is precisely the assumption the project needs, and it predates the CPH-transfer debate. If the project coins a term, "competent-student-style plan hypothesis" would need to be presented as new, with PROUST cited as the precedent.

---

## 1d. Taxonomies of novice logical errors

### Classic catalogs

**D1. Brown & Burton (1978), "Diagnostic Models for Procedural Bugs in Basic Mathematical Skills."** *Cognitive Science* 2(2), pp. 155–192. DOI 10.1207/s15516709cog0202_4. ~2,600 citations. **[V]** Method: the **BUGGY** diagnostic modeling system: a procedural-network formalism in which a student's arithmetic (esp. multi-digit subtraction) errors are reproduced by a *deep-structure* generative model — diagnosis = finding the single procedural modification that generates the student's exact error pattern. Key results: systematic, individually stable "bugs" (e.g., borrow-related variants) reproduce large fractions of student error patterns; diagnosis becomes model-fitting rather than error-listing. Limitations: arithmetic domain; procedural bugs only; assumes a *single* coherent bug per student (later work found mixed states). Relevance: the founding template for "diagnosis by matching against a generative model of plausible faults" — the project's localizer does the same, with algorithmic-pattern-conditioned fault models replacing subtraction bug templates.

**D2. Pea (1986), "Language-Independent Conceptual 'Bugs' in Novice Programming."** *Journal of Educational Computing Research* 2(1), pp. 25–36. DOI 10.2190/689T-1R2A-X4W4-29J2. Open full text at telearn.hal.science/hal-00190538. **[V]** Method: analysis of student errors across languages (Logo/Pascal/BASIC-era) to find language-independent conceptual bug classes. Key content (verified from abstract): three classes of bugs — **parallelism** (assuming the machine does several things at once / next-steps merging), **intentionality** (attributing goals to the machine), and **egocentrism** (assuming the machine shares the programmer's view/knowledge) — and one root **"superbug": the default assumption that "there is a hidden mind somewhere in the programming language that has intelligent interpretive powers."** The widely repeated *labels* "superplan bug," "lose-augeas bug," and "commissioned-author bug" appear in the article body per secondary literature but could **not** be verified in any fetched page after 3–4 attempts — **⚠️ UNVERIFIED**; if used in the paper, verify against the PDF or cite the three verified class names instead. Limitations: interpretive; no frequency data. Relevance: explains *why* novice faults concentrate at intent-machinery junctions — the same junctions the project's pattern-specific failure points target.

**D3. Spohrer & Soloway (1986), "Novice Mistakes: Are the Folk Wisdoms Correct?"** *Communications of the ACM* 29(7), pp. 624–632. DOI 10.1145/6138.6145. ~507 citations. **[V]** Method: empirical evaluation of two "folk wisdoms" about novice errors against an analyzed corpus of buggy novice Pascal programs, using the **goal/plan analysis** of Spohrer, Soloway & Pope (*Human–Computer Interaction*, 1985, "A Goal/Plan Analysis of Buggy Pascal Programs") and companions ("Where the Bugs Are," DOI 10.1145/317456.317465). Key content/results: distinguishes **plan bugs** (wrong/missing/mis-ordered plans — the "deep structure") from **symbolic bugs** (superficial misinterpretations of language constructs); finds that the folk wisdom attributing novice failures mainly to symbolic-level misunderstanding is wrong — most observed errors are **plan-level**, and a large share occur during **plan composition** (integrating known plans). Limitations: Pascal, small course corpus, manual analysis. Relevance: **the single most on-point classic for the project**: bugs live at plan boundaries, so a system that knows which plan was intended has a structural head start in fault localization.

**D4. du Boulay (1986) error types.** (Same paper as A2; error-side content: difficulties across orientation / notional machine / notation / structures / pragmatics; debugging weakness as a *pragmatic* deficiency rather than a knowledge gap.) [V]

### Modern / empirical taxonomies

**D5. Qian & Lehman (2017), "Students' Misconceptions and Other Difficulties in Introductory Programming: A Literature Review."** *ACM TOCE* 18(1), Article 1. DOI 10.1145/3077618. **[V]** Method: literature review synthesizing CS1/CS2 misconception studies. Key content: organizes difficulties into three knowledge domains — **syntactic**, **conceptual**, **strategic** — and catalogs construct-level misconceptions (variables/assignment, control flow, OOP, references); notes contributing factors (natural language, math background, instruction). Limitations: review-level; categories are knowledge domains, not fault classes; no algorithm-level dimension. Relevance: the current default citation for "what novices get wrong," and proof that the dominant taxonomy is *construct-level*, not *pattern-level*.

**D6. Altadmri & Brown (2015, 2016), Blackbox studies.** (a) "37 Million Compilations: Investigating Novice Programming Mistakes in Large-Scale Student Data," SIGCSE '15, DOI 10.1145/2676723.2677258; (b) "Novice Java Programming Mistakes: Large-Scale Data vs. Educator Beliefs," *ACM TOCE* 16(2), 2016, DOI 10.1145/2994154 (companion to the ICER '14 "Investigating novice programming mistakes: educator beliefs vs. student data," DOI 10.1145/2632320.2632343). **[V]** Method: mining the **Blackbox** telemetry of BlueJ — ~37M compilation events from ~250,000 students — to rank Java mistake frequencies, then comparing to educator consensus rankings. Key results: educator beliefs about the most common novice mistakes **do not match** empirical frequencies; the top empirically common mistakes include unbalanced parentheses/brackets, misuse of `=`/`==`-type confusions, and constructor/object issues (exact ordering in paper [S]). Limitations: compilation errors only (no logic-error content); Java/BlueJ only; telemetry populations skew. Relevance: the strongest large-scale evidence that expert intuition about novice errors is unreliable — an argument for *data-driven* pattern-conditioned priors instead of hand-intuited ones.

**D7. Ettles, Luxton-Reilly & Denny (2018), "Common logic errors made by novice programmers."** **ACE '18** (20th Australasian Computing Education Conference, Brisbane), pp. 83–89. DOI 10.1145/3160489.3160493. *(Venue correction: ACE, not ITiCSE.)* **[V]** Method: literature-grounded inventory addressing two RQs: which logic errors are most common, and which are most **persistent** (appear across languages/decades). Key results: a catalog of recurring logic-error types (off-by-one, wrong comparison operator, wrong loop bounds, incorrect condition inversion, etc. — exact ranking in paper [S]); persistence finding: many logic errors recur across decades and languages. Limitations: synthesis of published reports rather than new error data. Relevance: the closest existing list to "pattern-generic logical faults"; the project's pattern-specific failure-point tables can be built *on top of* this inventory (each pattern's failure points = a subset instantiation).

**D8. Alzahrani & Vahid (2021), "Common Logic Errors for Programming Learners: A Three-Decade Literature Survey."** 2021 ASEE Annual Conference. DOI 10.18260/1-2--36814. PDF: peer.asee.org. **[V]** Method: three-decade survey consolidating logic-error reports into a unified catalog. Key results: **166 distinct common logic errors classified into 11 categories** (figures as stated in the paper's record/citing works [S]). Limitations: survey aggregation; heterogeneous evidence quality; no link to solution strategies. Relevance: the largest published logical-error catalog — a natural frequency prior source for the project's localizer; notably its categories are pattern-agnostic, which is exactly the baseline to beat.

**D9. Prather, Pettit, Becker, Denny, Hollick, Saran & Kamal (2017), "On Novices' Interaction with Compiler Error Messages: A Human Factors Approach."** ICER '17, pp. 74–82. DOI 10.1145/3106215.3106225. **[V]** Method: eye-tracking + think-aloud usability study of novices reading/acting on compiler error messages (reading, compiling, fixing contexts). Key results: grounded taxonomy of novice reactions (e.g., *overwhelmed, encumbered, conflated, struggling, reading, grasping, inspecting*); most students read only the first line of the message; enhanced messages get read and acted on more often. Limitations: compiler (syntactic) errors only. Relevance: template for how a taxonomy of *reactions/faults* is built and validated; reminder that syntax-level tooling is far more studied than logic-level tooling.

**D10. Malysheva & Kelleher (2020), "Bugs as Features: Describing Patterns in Student Code through a Classification of Bugs."** CHI EA '20 (LBW), pp. 1–7. DOI 10.1145/3334480.3383065. **[V]** Method: late-breaking work proposing a constrained feature set for describing **patterns in student code** via a bug classification (context: novice code analysis for teaching). Key content: bug classes usable as *features* — i.e., a bridge from error taxonomy to machine-usable representations. Limitations: 4-page LBW, preliminary. Relevance: closest modern phrasing of "bug classes as code features" — but its patterns are construct-level, not algorithm-pattern-level.

**D11. MacNeil, Denny, Tran, Leinonen, Bernstein, Hellas, Sarsa & Kim (2024), "Decoding Logic Errors: A Comparative Study on Bug Detection by Students and Large Language Models."** ACE '24. DOI 10.1145/3636243.3636245; arXiv:2311.16017. **[V]** Method: multi-institutional study: **n=964** introductory students and GPT-3/GPT-4 perform the same logic-error *detection* task on novice code. Key results (from arXiv abstract [V]): significant improvement from GPT-3 to GPT-4, and **both LLM generations significantly outperform students** at detecting logic errors. Limitations: detection (yes/no) rather than localization (where/what); no pattern priors; US/India cohorts [S]. Relevance: (i) defines the current SOTA environment — LLMs are the pattern-agnostic baseline of 2026; (ii) citing works ("Improving LLM Classification of Logical Errors", 2024 [S]; Hoq et al., "Automated Identification of Logical Errors in Programs," EDM 2025 [S]) show an active LLM-logic-error thread with no algorithm-pattern conditioning — the project's most direct contemporary gap.

**D12. Neuwinger et al. (2025), "A Systematic Review of Common Beginner Programming Mistakes/Errors."** arXiv:2504.16644. **[S]** — recent synthesis of beginner error categories (syntax slips, operator confusions, loop/conditional structure errors, memory misconceptions); full author list unverified. Relevance: freshest overview confirming no consolidated logical-error taxonomy exists. **D13. Baron & Feitelson (2024)** (see B16) **[V]** supplies pattern-specific failure-point evidence (recursion base cases) — bridging taxonomy and pattern.

### Does ONE established taxonomy exist? (explicit conclusion)

**No.** After reviewing the candidates, there is no single accepted taxonomy of novice logical errors. The most-cited candidates, and their gaps:

- **Brown & Burton (1978)** — deep but domain-specific (arithmetic); single-bug-per-student assumption; not programming.
- **Pea (1986)** — conceptual and language-independent, but interpretive, no frequencies, and its labels are loosely used in secondary literature.
- **Spohrer & Soloway (1986) plan-vs-symbolic + goal/plan model** — the theoretically strongest *programming* taxonomy, but Pascal-era, manually applied, and never operationalized as a machine-checkable catalog at scale.
- **Qian & Lehman (2017)** — the modern default citation, but organized by *knowledge domain* (syntax/concept/strategy), i.e., about what students don't know, not about what fault classes their code exhibits.
- **Blackbox line (Altadmri & Brown 2015/16)** — huge scale but restricted to compilation errors.
- **Ettles et al. (2018) / Alzahrani & Vahid (2021)** — genuine logic-error catalogs (11 categories, 166 errors), but compiled from heterogeneous literature, pattern-agnostic, without frequencies grounded in a single dataset, and without a linkage between error type and solution structure.
- **MacNeil et al. (2024) / LLM-era work** — new data and models, but still detection/classification of *logic errors in general*, not strategy-conditioned localization.

Two structural gaps persist across all of them: (1) **no taxonomy separates fault classes by the intended algorithmic pattern** (two pointers, sliding window, binary search, DP, greedy, backtracking, etc.) — the plan/goal literature (Spohrer & Soloway; Johnson & Soloway's PROUST; Keuning's strategy-based feedback work [S]) gestures at plans in general but never at the named, competition-style pattern catalog; (2) **no published work conditions automatic fault localization on a classified pattern and measures Top-k accuracy gains** — the LLM-baseline literature (D11) explicitly lacks strategy priors. This double gap is the project's novelty claim, and it should be stated exactly that way: not "no one studies novice faults" (they do), but "no one has a *pattern-indexed* fault taxonomy or a pattern-prior-conditioned localizer."

**Adjacent-but-different work to cite as related, not prior art:** mutation-based student assessment (C7), strategy-based automated feedback (Keuning et al. [S]), and notional-machine-driven question generation (1a, SIGCSE 2024 poster [S]).

---

## Implications for the project

- **Theoretical frame to claim:** pattern-aware fault localization = giving the tool the *situation model* it otherwise lacks (Pennington B2, von Mayrhauser & Vans B4) and expert **beacons** (Brooks B1) at algorithm-pattern granularity; it is notional-machine scaffolding (du Boulay 1981/1986; Sorva 2013; Fincher et al. 2020) applied to *diagnosis* rather than instruction.
- **CPH is the right foil.** State the baseline's hidden assumption explicitly: pattern-agnostic localizers inherit CPH (DeMillo–Lipton–Sayward 1978) — near-correct code, small syntactic deviations — and cite Hu et al. 2019, Clegg 2021, Tanujaya et al. 2022, and Ahmed et al. 2023 to argue the assumption fails for novices (multiple severe, structured, plan-level faults). Knight & Leveson 1986 shows correlated errors even among professionals — novices correlate far more (shared misconceptions, Pea 1986).
- **Expected effect locations:** if the hypothesis is right, gains should concentrate exactly at pattern-specific failure points — two-pointer shift/stop conditions, sliding-window boundary arithmetic, DP base cases and transition direction (cf. Baron & Feitelson 2024 on base cases), loop-guard and off-by-one classes from Ettles et al. 2018 / Alzahrani & Vahid 2021.
- **Baselines to compare against:** (a) pattern-agnostic LLM detection (MacNeil et al. 2024 shows LLMs beat students at detection — but detection ≠ localization, and no pattern conditioning exists there); (b) mutation/spectrum-style localization; (c) the same localizer with a *shuffled/wrong* pattern prior (a cheap, powerful ablation that tests whether structure, not just extra information, drives the gain).
- **Replication discipline:** the Dehnadi–Bornat story (retraction 2014) is the cautionary precedent; pre-register the evaluation, use multiple cohorts/datasets (Blackbox-style data or IntroClass-like corpora), and report Top-1/3/5 with confidence intervals.
- **Terminology:** "notional machine," "beacon," "plan bug vs. symbolic bug," "CPH," and "intention-based diagnosis" (PROUST) are the five load-bearing terms; use them precisely (definitions above) and cite the corrected venues — the working-group report is **Fincher et al., ITiCSE-WGR 2020** (not 2022), the debugging review is **McCauley et al., CSE 18(2), 2008**, "The Good, the Bad, and the Quirky" is **Murphy et al.**, and "Common logic errors" is **ACE 2018** (not ITiCSE).
- **Unverified items to re-check before submission:** Pea's superplan/lose-augeas/commissioned-author labels; Knight & Leveson's exact number of test inputs; Chiarelli et al. 2023 result numbers; Budd's formal CPH sentence (quote from the gwern-hosted PDF); the Fowler et al. 2022 result wording; Hoq et al. EDM 2025 and Neuwinger et al. 2025 author lists.

*End of Block 1.*


---

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


---

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


---

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


---

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


---

# Block 6. Algorithm visualization tools — architecture and the "ML-driven selection" question

Verification legend: **[V]** verified from fetched/primary source; **[S]** credible snippets; **⚠️** unverified.

---

## 6.1 Python Tutor (Philip J. Guo)

| Paper | Venue | Content |
|---|---|---|
| "Online Python Tutor: Embeddable Web-Based Program Visualization for CS Education" **[V — PDF at pg.ucsd.edu]** | **SIGCSE 2013** | Architecture: a Python backend executes student code with a modified debugger (`bdb`), records **stack frames + heap objects at every step**, stores the trace, and a JS frontend renders step-by-step frames with arrows for references. Embeddable in any webpage; supported Python/Java/C/C++/JS/Ruby/Ruby... (languages grew over time). Reported **200k+ users in <3 years** at publication. No annotations needed from the author of the code — fully automatic stepping. |
| "Optimizing the Display of Deep Recursion in Code Visualizations" **[V — Taylor&Francis 10.1080/08993408.2017.1406444]** | **Computer Science Education 28(1):1–26, 2018** | Deep recursion overwhelms screen space; introduces visual encodings collapsing repetitive stack frames (e.g., collapsing identical consecutive frames, showing recursion trees). |
| "Python Tutor's Design Guidelines for Building Scalable and Robust Online Program Visualization Systems" **[S — dl.acm.org/doi/fullHtml/10.1145/3472749.3474819]** | **ITiCSE 2021** (82+ cites) | Three guideline sets: user experience, backend architecture (state-capture, sandboxing), scalability. |
- **Limitations (relevant to the project):** linear step-through of raw interpreter states; **no algorithm-level abstraction** (no notion "this is the pointer-shift step of two pointers"); hand-tuned renderers per language, not per algorithm; no ML; no notion of intended pattern → visualization choice is uniform regardless of what the code implements.

## 6.2 VisuAlgo (Steven Halim, NUS)

**[S — visualgo.net + Halim's publications]** Grew out of Halim's NUS work ("Visualising data structures and algorithms through animation" lineage, OOPSLA/SIGCSE-adjacent). Architecture: **hand-crafted per-algorithm JS visualizations** (each algorithm/DS gets a bespoke animation page) + integrated **quiz system**; used in NUS lectures (the site touts student usage counts in the hundreds of thousands across courses). No user code execution — the visualized algorithms are the site's own implementations.
- **Relevance:** the archetype of the *hand-crafted per-algorithm* approach whose authoring cost the project's platform avoids via execution traces + pattern classification.

## 6.3 Algorithm Visualizer (open-source GitHub org)

**[S — github.com/algorithm-visualizer]** Community open-source JS framework: each algorithm ships with **code annotated with visualization API calls** (`Tracer` objects — Array2DTracer, GraphTracer etc.); the frontend replays annotated logs. I.e., per-algorithm authoring effort moved into annotated code, not automatic.

## 6.4 Automatically-generated visualizations (no hand-crafting) — the important family

| Tool / paper | Venue | Mechanism |
|---|---|---|
| **Jeliot 3** — Moreno, Myller et al. **[V — dl.acm.org/doi/10.1145/989863.989928]** | ACM (AVEC/ITiCSE-family), ~2004 | Automatic animation of **unmodified Java programs**: interpreter-based capture of expression evaluation, variable assignments, method calls → continuous animation for novices. BlueJ integration extension exists. No annotations. |
| **WinHipe, Problets** **[S — IEEE TLT 2010 column]** | — | Cited alongside Jeliot 3 as systems capable of **automatic generation** of program animations. |
| "A Framework for the Automatic Generation of Algorithm Animations Based on Design Techniques" **[S — Springer 978-3-540-75195-3_40]** | — | Code is transformed so that execution stores a trace which then **generates the animation** (design-technique-driven templates). |
| Pseudocode-interpretation generator **[S — Granic et al., ResearchGate]** | — | Automatic visualizations from **unmodified pseudocode** via interpretation. |
| **CrossCode** **[S — CHI 2023, dl.acm.org/doi/10.1145/3544548.3581390]** | CHI 2023 | Web-based **multi-level** JS program visualization (different abstraction levels simultaneously). |
| **ALGOGEN: Tool-Generated Verifiable Traces for Reliable Algorithm Visualization** — Liao, Ma et al. **[V — aclanthology.org/2026.findings-acl.156 + arXiv:2605.12159]** | **Findings of ACL 2026** | Addresses hallucination when **LLMs generate algorithm visualizations**: instead of trusting LLM-emitted execution states, uses **tool-generated, verifiable execution traces** to drive the animation ("reliable automated generation of high-quality AV"). OpenReview: openreview.net/forum?id=mo81oKxSwS. |
- **Takeaway:** automatic trace-driven animation is a solved-ish pipeline (interpreter/trace → renderer); the 2026 frontier is making LLM-assisted generation *reliable* via verifiable traces.

## 6.5 Effectiveness evidence (why visualization matters at all)

- **[S] Hundhausen, Douglas & Stedmon, "A Meta-Study of Algorithm Visualization Effectiveness," Journal of Visual Languages & Computing / TOCHI-lineage 2002** (the EVADA meta-analysis): AV shows significant positive effects **when students themselves construct or modify** visualizations — passive viewing is weak. ⚠️ Exact venue (J. Vis. Lang. & Comput. 13(3), 2002) to confirm on final cite.
- **[S] Stasko, "TANGO: A Framework and System for Algorithm Animation," IEEE Computer 23(9), 1990**; earlier Brown & Sedgewick algorithm-animation work (~1984, "Techniques for Algorithm Animation," IEEE Software) — founding literature for the field's framing.
- **[S] "Automatic Generation of Prediction Questions during Program Visualization"** (ScienceDirect S1571066107002642) — generated prediction questions on top of Jeliot 3 visualizations; connects to the project's Socratic tutor angle.

## 6.6 ML-driven / data-driven CHOICE of visualization — does it exist?

- **NOT FOUND as an established research line.** Searches surfaced no work that (a) classifies the learner's code (or task) and (b) selects/generates a pattern-appropriate visualization for it. The closest neighbors:
  - ALGOGEN (2026): automatic AV generation with verifiable traces — but driven by an explicit algorithm specification, not by recognizing *user* code's pattern;
  - CrossCode (2023): multi-level views — level choice is user-driven, not ML-driven;
  - VisuAlgo: curated per-algorithm pages — no user-code recognition at all;
  - Python Tutor: uniform stepping UI regardless of algorithm.
- OverCode (Glassman et al. ~2015, clustering of student solutions for mass visualization) is the nearest "data-driven rendering" idea ⚠️ (not re-verified this session) — it clusters solutions for instructor views, not pattern-driven visualization selection for a single learner's code.
- **⇒ For the ISEF/РКНП "novelty of the platform component" argument:** pattern-classified visualization selection appears to be unoccupied ground; the platform's AST classifier + trace renderer is a plausible first. Must phrase carefully: "to our knowledge" + cite the six tools above as the boundary of prior art.

## Implications for the project
1. Cite Python Tutor + VisuAlgo as the two archetypes (automatic-but-uniform vs beautiful-but-hand-crafted); Jeliot 3 / ALGOGEN as the automatic-generation lineage.
2. The platform's differentiator = **pattern classifier drives which state abstractions to render** (e.g., for two pointers: highlight both pointers + window invariant; for DP: table cells touched at each step). No located prior work does this.
3. Hundhausen meta-study → argue for interactive elements (prediction questions) over passive animation — matches the existing Socratic tutor.


---

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


---

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


---

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
