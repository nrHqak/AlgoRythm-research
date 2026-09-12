# Pattern-Label Provenance Audit

**Status:** Investigation only. **No frozen manifest, script, or dataset file
has been modified by this audit.** `data/manifests/pilot_manifest_v2_1.json`,
`data/manifests/pilot_manifest_v2.json`, `scripts/package_final_sample.py`,
and `scripts/package_final_sample_v2_1.py` are unchanged as of this writing.
**Pre-results:** no valid scientific run exists, so this remains a pre-results
data-integrity finding, not a post-hoc reinterpretation of any result.

**Trigger:** `pilot_manifest_v2_1.json` records `pattern_source: "AST rule"`
for all 30 included programs, which does not match the human-annotation
provenance format `pilot/ANNOTATION_GUIDE.md` §2.5 specifies (e.g.,
`"atcoder-task-tag+manual-verification"`), and is inconsistent with the
disclosure `pilot/v2/CLAIM_BOUNDARIES_V2.md` §4.1 requires ("pattern labels
were assigned by a human annotator... not predicted by a model"). This was
first surfaced as an open flag in `paper/PAPER_SOURCE_AUDIT.md` and
`paper/APA7_PAPER_DRAFT.md` ("Oracle Pattern Labels"). This document is the
full investigation that flag called for.

**Method:** full git history of the manifest and its producing scripts;
direct reading of `scripts/package_final_sample.py`,
`scripts/package_final_sample_v2_1.py`, `scripts/build_ground_truth_freeze.py`,
`scripts/build_inventory.py`; a byte-diff of the pattern-classification logic
between the v2.0 and v2.1 packaging scripts; and a direct manual re-read of
six of the 30 sampled programs' actual `buggy.py` source against their
recorded `pattern_label`, chosen to cover four different classes.

---

## 1. Actual labeling mechanism

Pattern labels for **both** the v2.0 sample (commit `e60b5e4`) and the
corrected v2.1 sample (commit `9c83767`) were assigned entirely by a
hardcoded, deterministic **regex/keyword heuristic function**,
`classify_program(src: str, task_id: str)`, embedded directly in the
packaging scripts (`scripts/package_final_sample.py` lines 69–107;
`scripts/package_final_sample_v2_1.py` lines 82–120 — **the two functions are
byte-identical**, confirmed by direct diff). It runs once per candidate, over
the **entire frame** (232 programs for v2.1, before class selection), not
just the final 30.

The function tests the raw buggy-source text against an ordered chain of
`re.search` patterns for library/idiom signatures — e.g., `dp\s*=\s*\[` or
`memo\s*=` for dynamic programming; `deque`/`queue` combined with
`popleft`/`append`/`get` for BFS; `bisect`/`bisect_left`/`bisect_right` **as
bare word matches anywhere in the file** for binary search; a `while` loop
containing a `<`/`<=` comparison **combined with `// 2` occurring anywhere
else in the same file** as a second binary-search signature; `accumulate` or
a `pref`/`cumsum`/`acc`/`prefix` variable assignment for prefix sums;
`heapq` for greedy; `Counter(` or `defaultdict(int)` for hash-map counting; a
narrowly-named two-pointer `while` loop shape; `.sort(`/`sorted(` for
sorting; `permutations`/`combinations`/`product` for brute force; and a
turn/step/grid/`dx`/`dy` vocabulary for simulation — evaluated in a fixed
`if`/`elif` precedence order, with **`brute_force_implementation` as the
unconditional final fallback** for any program matching none of the above.

**No human ever assigned, reviewed, or overrode a pattern label at any
stage.** No commit, handoff document, or manifest field records a human
labeling pass separate from this function's output.

## 2. Evidence

- `scripts/package_final_sample_v2_1.py:82` — `def classify_program(src: str,
  task_id: str) -> tuple[str, str, str, str]:`. **The `task_id` parameter is
  never referenced inside the function body** (verified: the only occurrence
  of the string `task_id` within the function's 39 lines is the `def` line
  itself). `ANNOTATION_GUIDE.md` §2 step 1 requires labeling to start "from
  the task's own reference/intended solution technique, using AtCoder task
  metadata/editorial where available" — this input is structurally
  unavailable to the function that actually produced every label in this
  study.
- `scripts/package_final_sample_v2_1.py:99–120` — every `return` statement
  in `classify_program` hardcodes the literal string `"AST rule"` as the
  second tuple element, which is written verbatim into the `pattern_source`
  field. This is not a runtime-computed provenance description; it is a
  constant baked into the source code, identical for every one of the 30
  records (confirmed: `grep pattern_source
  data/manifests/pilot_manifest_v2_1.json` returns `"AST rule"` 30 times,
  with no other value present).
- **No `ast` module is imported or used in either packaging script**
  (confirmed: `grep -n "^import\|^from"` on both files lists `csv`, `json`,
  `random`, `re`, `subprocess`, `sys`, `collections`, `datetime`, `pathlib`,
  and for v2.0 additionally `socket`/`urllib.request` — never `ast`). No
  abstract syntax tree is ever constructed or traversed by this
  classification step; it operates on raw source text via `re.search`.
- `data/manifests/condfects_inventory_v2.csv` (built by
  `scripts/build_inventory.py`) has no pattern-related column at all — its
  header is `program_id,task_id,buggy_path,fixed_path,tests_path,loc,
  python_version,runs_successfully,passing_test_count,failing_test_count,
  evaluation_denominator,eligibility_status,exclusion_reason`. This confirms
  no pattern label of any kind — human or automated — existed anywhere in
  the pipeline before the packaging script assigned one.
- `data/manifests/ground_truth_freeze_v2.csv` (built by
  `scripts/build_ground_truth_freeze.py`) likewise carries no pattern field;
  it records only `decision`/`faulty_lines`/`exclusion_reason` for the
  fault-location adjudication (S1–S4 of `GROUND_TRUTH_PROTOCOL.md`), which
  **is** a correctly mechanical implementation of that document's §3
  decision table and is not in question here.
- `data/manifests/SAMPLING_AUDIT_V2_1.md` §3 states: "pattern counts were
  computed under blinded classification rules adhering to
  `pilot/PATTERN_VOCABULARY.md`." This sentence is true only in the narrow
  sense that a script cannot be influenced by knowledge of a fault line — it
  creates a materially misleading impression that the
  `GROUND_TRUTH_PROTOCOL.md` §6 human-annotator blinding procedure was
  followed. It was not: no human annotator, blinded or otherwise, was
  involved at any point.
- `AGENTS.md` contains no reference to "Antigravity," "pattern_label," or
  "annotat[ion]" at all — the only place a human-annotator responsibility
  for pattern labeling is asserted is `pilot/ANNOTATION_GUIDE.md`'s
  "Audience" line, which was not honored by the pipeline that actually ran.
- `pilot_manifest_v2_1.csv` additionally records a `pattern_confidence`
  column with values `high`/`medium`/`low` per program. This is not a
  calibrated confidence score; it is the third hardcoded tuple element in
  the same `classify_program` branches (e.g., every `dp_table`,
  `bfs_queue`/`graph_adj`, `bisect`/`manual_bs`, `itertools`, and
  fallback-default match is unconditionally `"high"`), and provides no
  independent evidence of label accuracy.

## 3. Meaning of "AST rule"

`"AST rule"` is a literal, author-written constant embedded in the
classification function, not a description generated from what actually
happened at runtime. It is:

- **Accurate** in one narrow respect: it correctly signals that the label
  did **not** come from a human annotator, which is consistent with this
  audit's other findings.
- **Inaccurate** as a technical description: no Abstract Syntax Tree is
  built or inspected anywhere in the labeling code; the mechanism is
  lexical/regex pattern matching over raw source text, not structural AST
  analysis. A program's actual AST shape (e.g., whether a `while` loop's
  condition and a stray `// 2` division belong to the same logical construct)
  is exactly the information a real AST-based rule would have and this
  heuristic does not — which is the direct cause of the misclassifications
  in §4 below.
- **Materially incomplete** as a provenance record: it does not disclose
  that the classifier never consults task metadata, was never reviewed by a
  human, and was applied identically to both the flawed v2.0 sample and the
  corrected v2.1 sample without modification.

## 4. Concrete misclassification evidence (direct source inspection, six of the thirty final programs)

Six programs across four of the pilot's four sampled classes were read
directly against their recorded label. Two of the six are clear
misclassifications under `PATTERN_VOCABULARY.md`'s own class definitions,
both concentrated in the `binary_search` class:

| Program | Task | Recorded label | Confidence | Actual code | Verdict |
|---|---|---|---|---|---|
| `46026874` | `abc237_c` | `binary_search` | high | Trims a string from both ends with two independent `while` pointer loops (`left`, `right`), then checks the remainder for a palindrome via `for i in range(length//2)`. No search-space halving, no midpoint, no monotonic predicate. | **Misclassified.** This is a two-pointer trim + linear palindrome check, not binary search. The regex fired because the file contains *both* an unrelated `while ... < ...` loop (the trim) *and* an unrelated `// 2` (the palindrome half-length) — two independent code fragments the heuristic's conjunction treats as one signal. |
| `39342455` | `arc139_b` | `binary_search` | high | A greedy/arithmetic cycle-offset optimization (`for i in range(a+5): ...`) with a recursive helper; `import bisect` is present but `bisect.bisect*` is **never called** anywhere in the file. | **Misclassified.** The regex `\b(bisect\|bisect_left\|bisect_right)\b` matches the bare word "bisect" in an unused import statement. No binary search is performed by this program. |
| `52742757` | `abc324_e` | `binary_search` | high | Calls `bisect.bisect` and `bisect.bisect_left` on two sorted arrays to count range matches. | Correct. Genuine library-based binary search. |
| `46008577` | `abc298_e` | `dynamic_programming` | high | Explicit `dp=[[0 for _ in range(N+1)] for _ in range(N+1)]` table with a nested-loop recurrence fill. | Correct. Genuine DP table. |
| `45044587` | `abc257_c` | `sorting_based` | medium | Sorts `(weight, group)` pairs via `people.sort()`, then does a single linear pass over the sorted order maintaining a running count and a max. | Correct, and a good match to `PATTERN_VOCABULARY.md`'s `sorting_based` definition. |
| `45723196` | `abc300_b` | `brute_force_implementation` | high | Nested loop over all grid-shift offsets `(x, y)`, checking every cell for each candidate shift. | Correct **only by construction**: this program matched none of the classifier's positive rules and fell through to the unconditional default. It happens to genuinely be brute-force enumeration, but the classifier did not detect that — it simply ran out of other rules. |

**Two of three directly-inspected `binary_search` programs (67%) are
confirmed misclassified**, both via a distinct false-positive mechanism (an
unused import; two unrelated code fragments coinciding in one file). This is
not a hypothetical risk raised by reading the classifier's source in the
abstract — it is a verified defect in the actual, currently frozen n = 30
sample. Given `binary_search` is one of only four classes in this pilot (7 of
30 programs, and 22 of 232 in the sampling frame that determined class
selection at S6–S7), a ≥50% within-class label-error rate, if it holds
across the full class, is large enough to compromise both the per-class
descriptive breakdown (`Table 3` of the paper draft) and, more seriously, the
integrity of the primary C-vs-B comparison for any `binary_search` program
whose true attempted technique is something else — in condition C, such a
program would receive `pilot/pattern_priors.json`'s `binary_search` checklist
(midpoint computation, boundary updates, search-predicate direction), which
targets failure modes largely irrelevant to the program's actual logic.

A further, structural (not spot-checked, but directly readable from the
code) concern: `brute_force_implementation` is the classifier's **sole
unconditional fallback** — any program matching none of the other eleven
rules is labeled `brute_force_implementation` regardless of what it actually
attempts. In the v2.1 frame, `brute_force_implementation` is also the
**largest class by a wide margin** (94 of 232 eligible frame programs, and 8
of the final 30) — a class size that is at least partly a default-bucket
artifact of the classifier's structure, not solely a true distribution of
attempted techniques in the underlying corpus. This is corroborated by the
frame's recorded **zero eligible `two_pointers` candidates**: the
classifier's `has_two_pointers` regex requires a `while` loop combined with
one of a narrow, specific set of variable-name/operator conventions
(`l +=`/`left +=`/`i +=` and `r -=`/`right -=`/`j -=`), which is far
narrower than the genuine variety of two-pointer code shapes documented in
`ANNOTATION_GUIDE.md` §5's own worked example (which uses a plain sort +
two-pointer scan with no assumption about variable naming). A "0 eligible
two-pointer programs in 232 candidates" result is more consistent with
systematic under-detection by an over-narrow regex than with a true absence
of two-pointer solutions in a 232-program sample of competitive-programming
submissions.

## 5. Was there manual or task-based verification before the sample freeze?

**No evidence of any was found.** Checked and found absent:

- No committed file (CSV, JSON, or Markdown) records a human decision,
  rationale, or override for any of the 232 frame programs' or 30 sampled
  programs' pattern labels.
- No commit message, in either `e60b5e4` or `9c83767`, claims a manual
  review pass occurred.
- `data/ANTIGRAVITY_HANDOFF_V2.md` and `data/ANTIGRAVITY_HANDOFF_V2_1.md`
  both enumerate certifications about test-execution correctness, ground-
  truth-line preservation, and absence of LLM evaluation — neither claims a
  human pattern-labeling pass took place.
- `ANNOTATION_GUIDE.md` §4's write-once rationale requirement ("every
  `pattern_label` decision must leave a one-line rationale... referencing
  which rule in §2 applied") has no corresponding artifact anywhere in the
  repository. The `pattern_note` field that does exist in the CSV manifest
  (e.g., `"DP table and recurrence structure"`) is a **canned string per
  classifier branch**, not a per-program rationale — every program landing
  in a given branch receives the identical note regardless of its specific
  content, which is the opposite of what §4 requires.

## 6. Relationship to the earlier "provenance string" framing

`paper/APA7_PAPER_DRAFT.md`'s Method section (as committed prior to this
audit) described the discrepancy provisionally, offering two possibilities:
"either... `"AST rule"` is an artifact of how the dataset-engineering
pipeline populated the `pattern_source` field programmatically after a human
decision was made elsewhere... or... a mechanical rule materially
contributed to labeling." **This audit resolves that open question: the
second possibility is what happened, without qualification.** There was no
human decision "made elsewhere" that the field failed to record; the
regex/keyword heuristic **is** the entire labeling process, for both sample
versions, and it demonstrably mislabels programs in the actual frozen
sample. The paper's Method, Discussion, and Threats-to-Validity sections
require revision to reflect this once a remediation path is chosen (see §8);
that revision is deferred, per the current instruction, until this audit is
reviewed and a path is authorized.

## 7. Verdict

- **Actual labeling mechanism:** A hardcoded, deterministic regex/keyword
  heuristic (`classify_program`, byte-identical in
  `scripts/package_final_sample.py` and
  `scripts/package_final_sample_v2_1.py`), applied uniformly to the entire
  232-program sampling frame with no human review at any point, and no
  consultation of AtCoder task metadata despite `ANNOTATION_GUIDE.md` §2
  requiring it as the first input.
- **Evidence:** See §2 above — exact file/line citations, a confirmed
  byte-identical diff between the v2.0 and v2.1 classification functions, an
  absent `ast` import, an unused `task_id` parameter, and two confirmed
  real-program misclassifications out of three directly inspected
  `binary_search` programs.
- **Meaning of "AST rule":** A hardcoded label, not a runtime-derived
  provenance description. Honest about "not human," inaccurate about "AST,"
  and silent about the classifier's demonstrated error rate and its
  structural blind spots (unused-import and unrelated-code-fragment false
  positives; an unconditional brute-force fallback).
- **Labels scientifically usable:** **NO**, not as currently produced and
  disclosed. Two concrete, independently verified reasons: (a) the labeling
  process violates the frozen protocol's explicit requirement of blinded
  human annotation (`GROUND_TRUTH_PROTOCOL.md` §6, `ANNOTATION_GUIDE.md`
  §2), which is a load-bearing part of the pilot's design (its stated
  purpose is to test an *oracle*-label prior specifically to isolate the
  prior's value from classifier error, per `dossier/99_synthesis.md` §S2.2)
  — using an unverified automated classifier's output while calling it
  "oracle" defeats that purpose by construction, independent of accuracy;
  and (b) the classifier has a demonstrated, non-trivial real error rate in
  the actual frozen sample (2 of 3 inspected `binary_search` programs), which
  directly threatens the internal validity of the primary C-vs-B comparison,
  since a mislabeled program's condition-C prior targets the wrong failure
  surface for that program's actual logic.
- **Manifest itself should change:** **YES**, in this reviewer's assessment
  — but this has **not been done**, per instruction, and is not authorized
  by this document. At minimum the `pattern_source` field is wrong as
  written; at maximum, the `pattern_label` values themselves need
  regenerating under a protocol-compliant process, which could change class
  selection (§4's frame-count concerns) and is a materially larger change
  than a metadata fix. Both options are laid out in §8 for explicit
  authorization.
- **Required correction:** See §8 (two options presented; no default
  applied).
- **Does this require rerunning the scientific experiment:** **YES**, in the
  sense that matters: **no valid scientific run has ever completed** (every
  attempt to date is VOID for an unrelated technical reason — output-token
  exhaustion — per `pilot/v2/CLEAN_SCIENTIFIC_RERUN_STATUS.md`), so there is
  no valid result to discard or invalidate. But this finding **must block
  the *next* execution attempt** on the current, unmodified
  `pilot_manifest_v2_1.json`: `pattern_label` is a direct input that selects
  which `pilot/pattern_priors.json` checklist each program receives in
  condition C, so running the frozen 600-call design against labels with a
  demonstrated non-trivial error rate would spend the entire scientific
  budget on a primary comparison whose causal interpretation is already
  compromised before any call is made.

## 8. Proposed remediation (neither applied; requires explicit authorization)

**Option A — Protocol-compliant re-annotation (recommended by this
reviewer).** Perform genuine blinded human pattern labeling exactly as
`GROUND_TRUTH_PROTOCOL.md` §6 and `ANNOTATION_GUIDE.md` §2 specify: a human
annotator, working from the buggy source plus AtCoder task metadata plus
`PATTERN_VOCABULARY.md`'s class definitions and confusable-pair rules only
(no `pattern_priors.json`, no `pattern_source: "AST rule"` field visible, no
knowledge of the automated classifier's prior output), applies the rules in
their stated order and records a one-line, program-specific rationale per
`ANNOTATION_GUIDE.md` §4. Because class *selection* (`SAMPLING_PROTOCOL.md`
§6) depends on frame-wide class counts that were themselves produced by the
same flawed classifier, a fully rigorous repair re-labels the **232-program
frame**, not only the final 30, and re-derives class selection and the
seeded within-class draw from the corrected counts — which may change which
four classes are selected and which specific programs are drawn, even
though the sampling *seed* (20260910) and *procedure* remain unchanged. This
is the only path that lets the paper continue to describe the pilot's labels
as "oracle" / human-assigned, consistent with the pilot's original stated
purpose. Output: a new, separately versioned manifest (e.g.,
`pilot_manifest_v2_2.json`) with a dated changelog entry, following the
project's own established freeze-discipline convention (cf.
`GENERIC_PLACEBO_PRIOR.md` §6: "any future revision requires a v3... applied
before the next data collection, never retroactively").

**Option B — Reframe rather than relabel.** Keep the current automated
labels and the current 30-program sample entirely as-is, but stop describing
them as oracle/human-assigned anywhere in the project's record. This
requires: correcting `pattern_source` from `"AST rule"` to an accurate
description (e.g., `"automated-regex-heuristic-v1, unverified,
task-metadata-blind"`); revising `CLAIM_BOUNDARIES_V2.md` (which is built
specifically around the oracle-label claim, e.g. §4.1's mandatory
disclosure) to describe a **predicted-label**, not oracle-label, pilot; and
disclosing the classifier's demonstrated error rate (§4 above) as a limitation
throughout. This is materially cheaper but changes what the pilot can claim
to test: it no longer isolates the prior's value from classifier error, and
it converts the pilot's "primary purpose" framing (`dossier/99_synthesis.md`
§S2.2's oracle/realistic distinction) into something closer to what that
document called the *realistic* condition, not the calibration pilot's
intended oracle condition.

This reviewer's recommendation is **Option A**, because the entire reason
this pilot uses oracle labels rather than classifier-predicted ones is to
isolate the prior's causal value from classifier error (§7 above); accepting
Option B without that isolation removes the property the pilot was designed
to have, not merely its label. Option A is more work but preserves the
pilot's original scientific purpose. **Neither option is applied by this
document.** Awaiting explicit authorization before any manifest, script, or
claim-boundary file is modified.
