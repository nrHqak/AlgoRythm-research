# PRE_RUN_REVIEW_V2 — adversarial audit of the v2 pilot specification

**Reviewer stance:** hostile peer reviewer attempting to reject the v2 design, with the v1 review's findings treated as prior art rather than as credit.
**Reviewed:** `PILOT_PROTOCOL_V2.md`, `GENERIC_PLACEBO_PRIOR.md`, `generic_placebo_prior.json`, `PROMPT_DIFF_V2.md`, `GROUND_TRUTH_PROTOCOL.md`, `SAMPLING_PROTOCOL.md`, `STATISTICAL_ANALYSIS_PLAN.md`, `MODEL_FREEZE_PROTOCOL.md`, `CLAIM_BOUNDARIES_V2.md`, `CHANGELOG_V1_TO_V2.md`, `prompts/system_v2.txt`, both v2 configs — plus the Codex code they depend on.
**Date:** 2026-09-10. No experiment was run, no results inspected, no dataset selected.

**Reviewer conflict, restated:** this audits a specification the same agent authored, twice over. It is not independent review. The v1 pass demonstrated the format can produce a BLOCK; that is not a reason to trust this pass more. Two findings below (V-1, V-6) are defects that v2 *introduced*, and one of them was closed by amendment before commit rather than shipped.

---

## 1. Did v2 achieve the authorized primary goal?

The authorization required the design to distinguish:

> "additional debugging guidance helps" **from** "PATTERN-SPECIFIC structural information helps"

**Yes, this is achieved.** The C-vs-B comparison holds constant: presence of a delimited block, its position, its delimiters, its numbered-list format, its checkpoint count (matched per label), its instructional tone, its opening/closing sentence structure, and its length within ±8 words (mean 4.2). The system prompt, user template, program set, model, and settings are identical on both sides. The only systematic difference is whether the checklist's content is derived from the program's algorithmic pattern.

That is a genuine identification of the causal contribution of pattern specificity, and it is what v1 could not do at all.

**One narrower alternative survives, and it is not the one the authorization named.** The placebo is *constant across programs*; the pattern prior is *selected per program*. So a positive C−B is consistent with "guidance tailored to the program on any axis helps," not only with "pattern-specific guidance helps." Ruling that out would need a fourth arm — a per-program checklist tailored on a non-pattern axis — which is out of scope at n=30. This is disclosed in `GENERIC_PLACEBO_PRIOR.md` §5 and prohibited as a claim in `CLAIM_BOUNDARIES_V2.md` §3. It is a real limit on interpretation, not a failure of the authorized goal.

---

## 2. Findings

### V-1 — The reordering in Change 2 opened a mirror-image circularity channel *(fatal class; closed by amendment before commit)*

v1's F2 was that pattern priors could shape the ground truth. v2 fixed it by freezing `faulty_lines` first, blinded. That reordering, on its own, created the inverse exposure: the labeling pass now runs *after* the fault line is known, so a labeler who also consulted the checkpoint lists could choose, among defensible labels, the class whose checklist sits on the known faulty line — pointing arm C's prior at the answer by construction and inflating C for reasons unrelated to pattern information.

This was not in the v1 review; it is a defect v2 introduced by fixing F2 in one direction only.

**Closed by amendment** (`GROUND_TRUTH_PROTOCOL.md` §6, added during this pass, before commit): the labeling pass is blinded to `faulty_lines` and to `PATTERN_PRIORS.md`, works from `PATTERN_VOCABULARY.md` (which contains no checkpoint lists) plus the unannotated source, and carries a mandatory exclusion rule for any case where the label choice is not separable from knowledge of the fault location.

**Residual — and this is the single most significant unresolved-by-construction risk in v2:** with one annotator, this is a discipline-and-exclusion control, not a structural guarantee. A person cannot unsee what they recorded an hour earlier. Its strength rests on the single-line/unambiguous filter making most labels determinable from code shape alone. A second annotator for the labeling pass would close it completely and is recommended wherever one is available.

### V-2 — The delimiter tag is anti-conservative in arm B *(important; the only bias in v2 that favours the hypothesis)*

`experiments/prompts.py` wraps every prior in `<ALGORITHMIC_PATTERN_PRIOR>`. In arm C, tag and content agree. In arm B, a tag promising pattern information wraps generic advice. A model that notices the mismatch may discount B's block — which would depress B and **inflate C − B for a reason unrelated to pattern content**.

Every other bias in v2 runs against the hypothesis (strong placebo, easy-case filtering, system-prompt framing shared by all arms, conservative parser policy). This one runs toward it, which makes it disproportionately important despite being small.

**Recommended fix, not applied:** a one-line change to the `PRIOR_OPEN` / `PRIOR_CLOSE` constants — e.g. `<DEBUGGING_PRIOR>` — applied identically to both arms, removing the incongruity entirely. This requires editing Codex's `experiments/prompts.py`, which is outside this handoff's ownership and was not done unilaterally. It should be requested before the run.

**If the change is declined,** the pilot can still run as calibration, provided that (a) every report of the primary comparison discloses the asymmetry and its direction, and (b) the manual spot-check in `PILOT_PROTOCOL_V2.md` §5.6 explicitly looks for arm-B transcripts in which the model remarks on, questions, or discounts the block's contents. This must be fixed before any confirmatory run.

### V-3 — The dry run has no data to run on *(operational; blocking for step 1 of the execution order)*

`MODEL_FREEZE_PROTOCOL.md` §3 requires a ≥10-call dry run on `data/smoke/`. **`data/smoke/` contains only a README** — no fixtures exist. The model-freeze gate is therefore currently unexecutable, and the temptation when this is discovered mid-setup will be to "just use a couple of candidate programs," which is precisely the contamination the protocol forbids.

**Required before step 1:** create 3–5 small buggy Python programs as smoke fixtures — hand-written, or drawn from ConDefects programs that are permanently marked excluded and can never enter the frame. Trivial work; it simply has to happen first, and be committed so the provenance is auditable.

### V-4 — The primary comparison cannot be computed by any code that exists *(important; sequencing)*

C vs B is cross-session, and `analysis/run_analysis.py` analyzes one session at a time and pivots on exactly two condition names. The primary result therefore depends on an additive analysis script that does not yet exist. If it is never written, the pilot yields only A-vs-B and A-vs-C — i.e. it degenerates to a more expensive v1.

Worse, if the script is written *after* the data is in hand, its author is making implementation choices with results visible. `STATISTICAL_ANALYSIS_PLAN.md` §6.1 pre-specifies the aggregation, the tests, and the assertions tightly enough that the script should be mechanical — but "should be" is doing real work in that sentence.

**Recommended:** write and validate the script **before** the main run, against mock sessions (`--allow-mock` / `--allow-mock-analysis`), and commit it. Then the run cannot influence it.

### V-5 — v2 is expected to produce a statistically null primary result *(by design; must not be mistaken for failure)*

Three v2 decisions each compress the achievable C−B gap: a deliberately *strong* placebo (§1 of `GENERIC_PLACEBO_PRIOR.md`), the single-line/clean-localization filter that admits mostly easy faults, and the omission of `problem_context`. Layered on `STATISTICAL_ANALYSIS_PLAN.md` §7's arithmetic — at least 6 one-directional discordant pairs before p ≤ 0.05 is even reachable at n=30 — a null primary result is the *likely* outcome.

This is coherent, because the pilot's stated job is estimating the discordance rate, not testing the hypothesis; a null still yields `b`, `c`, and `π_d`. But two consequences need stating in advance, and the protocol states only the first:

- a null must never be reported as evidence against the hypothesis (`CLAIM_BOUNDARIES_V2.md` §1 covers this);
- **if `ψ = b/(b+c)` lands near 0.5, the sizing formula explodes and the pilot will fail to size the confirmatory study at all.** That outcome should be pre-named as a legitimate result — "the pilot could not size the study; the effect, if present, is smaller than this design can resolve" — rather than treated as a reason to re-run with different settings until a usable number appears.

### V-6 — `PILOT_PROTOCOL_V2.md` §3.3 slightly oversells the duplicated control arm *(minor; framing)*

The document calls the A_G/A_P duplication "a designed benefit." It is not designed; it is **forced**. Codex's runner requires exactly two conditions per session, and every session's control arm is the no-block prompt, so running two sessions necessarily produces arm A twice. The null-calibration use is a genuine and valuable repurposing of a structural cost — but presenting a constraint as a design choice is the kind of framing a reviewer should discount, and a reader deserves to know 300 of the 600 calls go to a duplicated control because the tooling gives no alternative.

### V-7 — The null-calibration gate is weakest exactly when it is least needed *(minor; note only)*

The gate compares `d_null` (A_G vs A_P discordance) against `d_primary`. At temperature 0 with a deterministic model, `d_null` will be 0 and the gate passes trivially. That is arguably correct behavior — no drift means nothing to guard against — and when determinism is low, `d_null` grows and the gate bites. So the gate is well-calibrated to the actual threat. One residual: it measures drift for the *no-block* prompt shape, and does not directly bound drift for the longer block-bearing prompts used in B and C.

### V-8 — Five repetitions is more than a determinism probe needs *(minor; efficiency)*

`STATISTICAL_ANALYSIS_PLAN.md` §4 reinterprets the repetitions as a determinism probe, which is the right resolution of v1's N2 — but a probe does not need five samples. Three would suffice and would save 240 of the 600 calls. Retaining five is defensible (robustness if stochasticity turns out to be present, and comparability with the arXiv:2512.03421 protocol), and `--repetitions` is available as a runner override if budget matters more. Flagged as a tradeoff the executor should make knowingly rather than inherit.

### V-9 — Frame feasibility is assumed, not established *(minor; contingencies exist)*

The 4-class rule needs 4 classes with ≥7 eligible programs each after a demanding filter stack. A rough transit of ConDefects-Python (1,625 faulty programs, 985 tasks) through one-per-task, ≥1 pass/≥1 fail, ≥25 lines, single-line-fix-only, and vocabulary-fit suggests a frame in the low hundreds, which should support the rule comfortably — but this is an estimate, not a count. `SAMPLING_PROTOCOL.md` §6 has explicit contingencies (3 classes at 10 each; then 6 classes at 5 each; then a recorded deviation), so a thin frame cannot become a licence to improvise. No action needed beyond executing §7's recording requirements honestly.

### V-10 — Unchanged carry-over limitations

Neither introduced nor resolved by v2, and all disclosed: n=30 is calibration-only; a single provider/model bounds generalization; single-annotator labels with no κ; ConDefects leakage remains unprobed (v1 N11); EXAM\* remains a censored, line-based statistic that is not comparable to published EXAM; ranking length remains a measured-not-controlled mediator (v1 N5, reasoning in `PROMPT_DIFF_V2.md` §4.3).

---

## 3. What must happen before the first real call

These are execution gates, not design defects. The design is approved with them outstanding; the run is not.

1. **Create smoke fixtures** in `data/smoke/` (V-3) — never from the candidate frame.
2. **Request the neutral delimiter tag** from Codex (V-2). If declined, record the decision and adopt the two disclosure/detection mitigations.
3. **Write and validate the cross-session analysis script** against mock sessions, and commit it (V-4).
4. **Execute `MODEL_FREEZE_PROTOCOL.md`** — pin the exact model identifier, verify the echoed string matches, pass the dry run cleanly.
5. **Record the session-order coin flip** and all frozen model parameters.
6. **Execute `SAMPLING_PROTOCOL.md`** with both blinds in force (`GROUND_TRUTH_PROTOCOL.md` §1 and §6), committing the ground-truth record *before* labeling begins.

---

## 4. Verdict

# **RUN PILOT**

Subject to the six gates in §3, which are setup steps rather than revisions.

**Reasoning.** The v1 BLOCK rested on one thing: the design could not attribute anything to pattern specificity. v2 fixes that with a matched placebo whose parity is mechanically verified rather than asserted, and the remaining fatal-class findings from v1 (F2–F5) are closed by procedural controls that are checkable from the committed record. The one fatal-class defect v2 introduced (V-1) was found in this pass and closed before commit, with its residual disclosed. Nothing that remains prevents the pilot from producing exactly what it is for: an honest discordance estimate, a noise floor, and a validated pipeline.

**This is not an endorsement of the pilot's likely result.** V-5 says plainly that a null is the expected outcome, and V-2 identifies the one asymmetry that could manufacture a false positive. A reviewer approving this design is approving a *calibration instrument*, not a finding — and `CLAIM_BOUNDARIES_V2.md` is the part of this specification that carries the most weight after the numbers arrive.

**What would flip this back to BLOCK:** running before the §3 gates are closed; writing the cross-session analysis script after seeing data; a single annotator performing the labeling pass without applying §6's exclusion rule; or any use of the pilot result as confirmatory evidence.
