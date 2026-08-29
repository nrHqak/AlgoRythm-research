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
