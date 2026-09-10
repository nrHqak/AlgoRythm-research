# PRE_RUN_REVIEW — adversarial audit of the frozen pilot specification

**Reviewer stance:** hostile peer reviewer attempting to reject `algorythm_pattern_prior_pilot` before any data is selected.
**Reviewed:** `PILOT_PROTOCOL.md`, `PATTERN_VOCABULARY.md`, `PATTERN_PRIORS.md`, `PROMPT_DIFF.md`, `ANNOTATION_GUIDE.md`, `PRE_EXPERIMENT_COMMIT.md`, `SCIENTIFIC_RISKS.md`, `CLAIM_BOUNDARIES.md` (all FROZEN v1, commit `81fd51d`), plus the Codex engineering code they depend on (`experiments/prompts.py`, `experiments/run_pilot.py`, `experiments/safety.py`, `experiments/providers/http.py`, `experiments/storage.py`, `analysis/metrics.py`, `analysis/statistics.py`, `analysis/run_analysis.py`).
**Date:** 2026-09-10. No experiment was run, no results were inspected, and no frozen file was modified in producing this review.

**Disclosure of reviewer conflict:** this review audits a specification the same agent authored. It is therefore not an independent review, and several findings below are self-inflicted defects in that authorship. Where a finding contradicts the frozen documents' own reassurances, the finding is stated in favour of the reviewer, not the author.

---

## PASS / BLOCK verdict

# **BLOCK**

The specification is internally coherent, well-cited, and unusually disciplined about freeze mechanics and claim hygiene. That is not sufficient. **The two-arm design cannot isolate the causal contribution of pattern-specific structural information** — which is the project's entire novelty claim — and five further defects would materially damage the run or its interpretability if data selection proceeded today.

Stated as plainly as the brief requires:

> **The current design cannot isolate the causal contribution of pattern-specific structural information.** A positive result is fully explained by the alternative hypothesis "giving the model ~130 additional words of any structured debugging guidance improves localization." Nothing in the frozen v1 specification distinguishes these two explanations, and `CLAIM_BOUNDARIES.md` as written does not require that ambiguity to be disclosed when the result is reported.

The block is on the **scientific** design, not the engineering. Codex's infrastructure is sound and several of its safety checks are stronger than the protocol gives them credit for.

### Audit question → verdict map

| # | Question posed | Verdict | Where |
|---|---|---|---|
| 1 | n=30 coherent with a 12-class vocabulary? | **No** — ~2.5 programs/class; the "treatment" is 12 interventions pooled | N1 |
| 2 | Does control-vs-treatment create a length/extra-context confound? | **Yes**, unavoidably; the frozen mitigation does not address it | F1, N5 |
| 3 | Is a matched-length placebo prior required? | **Yes** — required to support the actual hypothesis | F1 |
| 4 | Do the priors leak fault locations? | **Not directly** — but the *annotation procedure* creates a circular path | F2 |
| 5 | Are oracle labels used/described correctly? | **Overstated** — single-rater proxy, not an oracle | N6 |
| 6 | Can selection cherry-pick? | **Yes** — three unblinded judgment gates, no sampling frame | F3 |
| 7 | Same-task programs violating independence? | **Yes, likely** — unconstrained; ~1.65 programs/task in the source | F3 |
| 8 | Are 5 reps at temperature 0 meaningful? | **Internally inconsistent** — the two settings cancel each other's rationale | N2 |
| 9 | Is McNemar at the right observational level? | **Code: yes. Protocol: incomplete** — no rule for combining 5 tests | N3, N4 |
| 10 | Are Top-K/EXAM well-defined for multi-line faults? | **No** — the convention exists only in code, and biases by fault width | F3, N5 |

---

## Fatal issues that must be fixed before data selection

### F1. No placebo arm — the design cannot attribute any effect to *pattern-specific* information

The manipulation is not one variable. Moving from `pattern_agnostic` to `oracle_pattern_prior` changes at least five things simultaneously:

1. pattern-specific structural content (the intended variable);
2. ~119–138 additional words of prompt (`PATTERN_PRIORS.md` length audit);
3. the presence of an explicit, ordered, numbered checklist format;
4. an instruction to check certain things **first, in order** — i.e. an attention/search-order directive;
5. the meta-signal that this program *has* a recognizable algorithmic structure at all.

`SCIENTIFIC_RISKS.md` §2 acknowledges (2) and states a mitigation — that all 12 priors are held to a 119–138 word band. **That mitigation is a non-sequitur for the primary comparison.** Holding prior length constant *across patterns* controls between-pattern variance; it does nothing whatsoever about the control-vs-treatment length difference, which is the confound that matters. The frozen risk register thus creates a false impression that the principal threat to validity has been partially handled. It has not been handled at all.

This matters more here than in a generic prompt ablation because the project's novelty claim is specifically *pattern conditioning*. `dossier/07_block7_novelty.md`'s differentiation from PROUST and from 2024–2026 LLM-FL work rests on the prior being **pattern-derived**, not merely on the localizer receiving more guidance. A two-arm pilot cannot speak to that distinction even directionally.

**Required fix (one of):**
- **(a) Recommended — add a third arm as a second session.** Create `pilot/placebo_priors.json` mapping all 12 slugs to a *single identical* generic debugging checklist, matched on word count (119–138) and checkpoint count (4–5), containing no pattern-specific content (e.g. loop bounds; comparison direction; off-by-one on indices; order of state updates; boundary/empty-input cases). Run it as a separate session, then compare (pattern − control) against (placebo − control).
  **Engineering constraint, verified:** this requires a **new config file with a different `experiment_name`**. `experiments/run_pilot.py` builds `raw_root = output_root/"raw"/experiment_name` and `existing_execution_keys()` rglobs that whole tree across *all* sessions; the control-arm execution key excludes `prior_hash` (it is `None` for control) and is otherwise identical between the two sessions, so re-running under the same `experiment_name` aborts with "duplicate run detected". Using `--resume` would skip the control arm entirely and then fail `assert_condition_balance` at analysis. A second config (`experiment_name: algorythm_pattern_prior_placebo_pilot`) avoids both. No Codex code changes required.
- **(b) Cheaper — retarget the single comparison** so that the *control* is the matched-length generic checklist and the treatment is the pattern checklist. This isolates pattern-specificity directly in one session, at the cost of losing the "prior vs. nothing" contrast. Note the mechanical constraint: `build_prompt_pair` makes the treatment prompt a strict extension of the control prompt, so the generic checklist would have to live in the shared template and the pattern block would sit *on top of* it (an additive, not substitutive, design) — weaker, and still length-confounded, though by a smaller margin.
- **(c) Accept and hard-restrict** — run two arms, and make the pattern-specificity ambiguity a *mandatory* qualifier on every reported delta (see F5). This is the only option that requires no extra budget, and it is the minimum acceptable outcome.

Cost of (a): doubles the call budget (300 → 600).

### F2. Ground-truth annotation is not blind to the pattern priors — circular by construction

The priors themselves are clean: I re-read all 12 and they contain no line numbers, no program-specific identifiers, and no information derivable from the fix diff. **Item 4's direct leakage concern is not substantiated.** The leakage vector is elsewhere — in how ground truth is produced.

`ANNOTATION_GUIDE.md` §3 step 3 instructs the annotator, for any fix that refactors, to "use judgment to mark the **minimal buggy-file line range** that a developer inspecting only the buggy file… would need to change." The same annotator, per §2, has already determined `pattern_label`, and may well have read `PATTERN_PRIORS.md` (nothing forbids it — and `ANNOTATION_GUIDE.md` §2.4 actively directs them into `PATTERN_VOCABULARY.md`'s reasoning). An annotator primed with "for DP, check the base case, the transition, the fill order…" will, in ambiguous cases, gravitate to marking exactly those lines as the fault. Ground truth then correlates with the treatment text **by construction**, and the treatment arm is scored against a target that was partly written by the treatment.

No frozen document addresses this. `SCIENTIFIC_RISKS.md` §5 covers `pattern_label` *accuracy* but not `faulty_lines` *contamination*.

**Required fix:** enforce ordering and blinding in the annotation procedure —
1. `faulty_lines` is derived **first**, mechanically from the buggy↔fixed diff, before any pattern reasoning;
2. the person or pass that fixes `faulty_lines` must not have read `pattern_priors.json` / `PATTERN_PRIORS.md` (if one person does both, they must complete and record all `faulty_lines` before opening either file, and must not revise `faulty_lines` afterwards for any reason);
3. any program whose `faulty_lines` cannot be settled from the diff without pattern reasoning is **excluded**, not adjudicated by judgment.

### F3. Selection-integrity constraints are missing — the manifest can be cherry-picked, and several metric preconditions are unstated

`ANNOTATION_GUIDE.md` §6 says "do not include a program solely because it is convenient" and "apply §1's filters mechanically," but §1 contains three unblinded judgment gates (single-fault determination, minimal-line-range determination, pattern-fit determination) and there is **no sampling frame at all** — no requirement to enumerate the filtered candidate pool, no random draw, no seed. `PILOT_PROTOCOL.md` §3 then actively instructs the assembler to *choose* programs to hit pattern quotas ("at least 2 programs per included class"), which is selection on a hypothesis-relevant variable performed by a person who knows the hypothesis.

Five constraints must be added before selection begins. All are cheap, none require touching Codex's code:

1. **Sampling frame.** Enumerate the full filtered candidate pool, record its size, then draw the 30 by fixed-seed pseudorandom sample (stratified by pattern if desired, with the strata declared in advance). Record pool size, seed, and draw order in the manifest provenance. The assembler must not have run any LLM over candidates beforehand.
2. **One program per task.** `task_id` must be unique across the 30 included programs. ConDefects-Python holds 1,625 faulty programs across 985 tasks (`dossier/04_block4_datasets.md` §4.3) — ~1.65 per task — so an unconstrained draw of 30 will very likely include same-task siblings. Same-task programs share a problem statement, an intended pattern, and frequently a fault mode; McNemar treats each pair as independent, and `analysis/statistics.py::clustered_bootstrap_delta` clusters on `program_id` only — **there is no task-level clustering anywhere in the pipeline**, and `ProgramManifest` validates duplicate `program_id` but never duplicate `task_id`. Enforcing uniqueness at selection makes the program-level clustering that already exists correct, at zero cost. *(Audit item 7.)*
3. **Single-line faults only.** Require `len(faulty_lines) == 1`. The multi-line convention exists only in code and is documented in no frozen file: `analysis/metrics.py::conservative_fault_rank` returns the **best (minimum) rank across all faulty lines** (with worst-rank tie-breaking within a score tie). A 3-line fault therefore gets three chances to land in Top-K, so programs with wider faults are systematically easier, and if fault width correlates with pattern (plausible — a DP base-case fix is typically one line, a simulation state-update fix often several), the per-pattern deltas are confounded by width. Both cited baselines (IJSEKE 2025; arXiv:2512.03421, `dossier/03_block3_fault_localization.md` §3b–3c) use single-line ground truth, so this also restores comparability with the published numbers the protocol wants to be comparable to. *(Audit item 10.)*
4. **Minimum program length.** The current floor of 10 physical lines is too low. `evaluation_denominator` defaults to `loc`, so on a 12-line program Top-5 covers >40% of the file and is near-trivially attainable once the model is told which construct to inspect — the treatment arm would saturate Top-5 for structural reasons unrelated to localization quality, leaving Top-1 as the only informative metric. Raise the floor (suggest ≥25 lines, or ≥20 non-blank/non-comment lines) and state the rationale.
5. **`problem_context`: all or none.** `problem_context_path` is optional per record and **no frozen document specifies whether the pilot includes it**. This is not a detail: AtCoder problem statements frequently make the intended technique obvious, so including them partially leaks the pattern into the *control* arm, biasing the measured effect toward zero for reasons unrelated to the prior's value; and varying it across programs adds an uncontrolled per-program variable. `PILOT_PROTOCOL.md` §3 mandates consistency for `evaluation_denominator` but is silent here. Decide one way, apply uniformly, record the decision. (Recommendation: **omit** for the pilot — cleaner isolation of the manipulation; revisit for the confirmatory study, where realism matters more.)

### F4. Operational landmine: a model *alias* will silently produce an all-zero "successful" run

Verified in code. `experiments/providers/http.py` sets `ProviderReply.model = str(body.get("model") or request.model)` — the model string the API echoes back. `experiments/run_pilot.py::run_one` then checks `if reply.provider != provider.name or reply.model != model:` and, on mismatch, records `status="provider_failure"`, `error_type="ModelIdentityMismatch"`.

Most providers echo a **dated snapshot** for an alias request (request `gpt-4o` → response `gpt-4o-2024-08-06`). Every single call would therefore be recorded as a provider failure. The failure mode is not loud:

- `provider_failure` records carry `raw_response_path: None`, so `assert_raw_files_exist` skips them and `assert_raw_prompt_symmetry` finds no pairs to check;
- `assert_condition_balance` still passes (the records exist, correctly balanced);
- `analysis/metrics.py::evaluate_record` scores every failed run `top1=top3=top5=0`, `exam=1.0`.

The result is a complete, non-aborting analysis run reporting 0% vs 0% with a full set of figures — an artifact that looks like a finished experiment and is worth nothing. Budget is spent, and the raw-response files that would normally allow recovery do not exist.

**Required fix:** pin the exact model identifier that the chosen provider echoes back, verify it with a single throwaway call against a **non-manifest** program before the pilot begins, and record the verified string in `PRE_EXPERIMENT_COMMIT.md` alongside provider/temperature/max_tokens. `PILOT_PROTOCOL.md` §2's model-selection criteria should list echoed-identifier verification as a precondition, not leave it to be discovered.

### F5. `CLAIM_BOUNDARIES.md` currently licenses a claim the design cannot support

The mandatory-qualifier list requires (a) n=30, (b) named provider/model, (c) oracle labels, (d) ConDefects-Python, (e) statistical indecisiveness. It does **not** require disclosure that the comparison cannot separate pattern-specific content from matched-length generic guidance. The document explicitly holds up "the pattern prior improved Top-1 accuracy by X points" as a violation *only for missing those five qualifiers* — implying the same sentence **with** them is compliant. Under a two-arm design it is not compliant: the phrase "the pattern prior" asserts precisely the attribution the design cannot make.

**Required fix (whichever route F1 takes):**
- if the placebo arm is run, add its result to the qualifier set;
- if it is not, add a sixth mandatory qualifier: *"this comparison cannot distinguish pattern-specific structural information from any matched-length structured debugging guidance; no attribution to pattern-specificity is supported"* — and add to the "may NOT be claimed" list: *any claim that the effect is attributable to pattern-specific content, or any framing that contrasts this result with pattern-agnostic guidance.*

---

## Important but non-fatal limitations

**N1. n=30 against 12 classes is not one experiment; it is twelve experiments with n≈2.5 each.** *(Audit item 1.)* The treatment is not a single intervention — each pattern receives a *different* 119–138-word text. Pooling assumes the effect is homogeneous across the 12 priors, which is untested and untestable at this n. Two consequences: (i) the per-pattern Top-1 breakdown pre-committed in `PRE_EXPERIMENT_COMMIT.md` is uninterpretable — the ≥2-programs-per-pattern guard in `PILOT_PROTOCOL.md` §3 sets a threshold at a number that is still meaningless; (ii) the discordance rate exported to the confirmatory power calculation (pilot purpose #3) is a *mixture* estimate over whatever pattern mix the 30 programs happen to have, and will not transfer if the confirmatory corpus has a different mix. This is borderline fatal: combined with F1, it means the pilot's scientific yield is close to zero even when it succeeds. **Recommendation:** for the pilot manifest only, draw from **3–4 pattern classes at 8–10 programs each** rather than 12 classes at 2–3. `PATTERN_VOCABULARY.md` stays frozen at 12 — this constrains only which subset the pilot samples, and it buys genuine within-pattern calibration.

**N2. Temperature 0 and 5 repetitions cancel each other's rationale.** *(Audit item 8.)* `PILOT_PROTOCOL.md` §2 justifies temperature 0 as removing run-to-run noise "on top of the already-frozen 5-repetition averaging," while the 5-repetition protocol is inherited from arXiv:2512.03421 *because* it averages LLM stochasticity. If responses are near-identical, the 5 repetitions cost 5× and add almost no information, and the five per-repetition McNemar tests become five near-copies presented as if they were five results. Also: temperature 0 is not a determinism guarantee under batched or MoE serving, and several reasoning models ignore the parameter entirely. **Resolve one way before selection:** either (a) keep temperature 0 and re-purpose repetitions explicitly as a determinism probe — report the identical-response rate and treat the effective sample as 30, not 150; or (b) set a documented non-zero temperature so the repetitions measure what the precedent measures. `--repetitions` is a runner override, so (a) can also reduce reps without editing Codex's config.

**N3. The observational level is right in the code but under-specified in the protocol.** *(Audit item 9.)* Codex handles this correctly: `summarize_topk` runs exact McNemar **per repetition** over 30 program-pairs and labels the pooled transition counts "not an independent-sample test"; `clustered_bootstrap_delta` averages repetitions within program before resampling programs. No repeated-measures inflation. But `PRE_EXPERIMENT_COMMIT.md` designates "per-repetition exact McNemar on top1" as primary **without a rule for combining or reporting the five resulting p-values** — an open forking path (which repetition gets quoted?). **Fix (documentation only):** pre-specify that all five are reported together, that no single repetition's p-value may be quoted alone, and that the program-clustered bootstrap CI is the primary *inferential summary* while exact McNemar remains the config-mandated primary *test*. `pilot.yaml` need not change.

**N4. The primary test is arithmetically incapable of significance in the likely regime.** Computed against the actual implementation (`binomtest(min(b,c), b+c, 0.5, two-sided)`): with `d` discordant pairs the minimum attainable two-sided p is 1.000 (d=1), 0.500 (2), 0.250 (3), 0.125 (4), 0.0625 (5), 0.03125 (6). **At least 6 discordant pairs, all favouring one condition, are required for p≤0.05 to be reachable at all**; if even one discordant runs the other way, 9 are needed. With 30 pairs per repetition this is attainable but not comfortable, and it should be stated in the protocol so that a null result is not misread as evidence of absence. Reinforces "calibration, not confirmation."

**N5. EXAM as implemented is a censored, ranking-length-dependent statistic — and that is the mechanism by which F1's confound reaches the metrics.** Two issues. *(a)* When the faulty line is absent from the returned ranking, `conservative_fault_rank` returns the denominator, so EXAM is exactly 1.0 — a censoring convention, not "fraction of statements inspected," and the denominator defaults to `loc` (physical lines) rather than the inspectable-statement count that IJSEKE 2025's EXAM uses. It should be labelled distinctly (e.g. EXAM\*) or defined explicitly; it is not directly comparable to published EXAM values. *(b)* More seriously, `control.txt` instructs "List only lines you have a genuine reason to suspect," making ranking length model- and condition-dependent. A treatment prompt that hands the model 4–5 checkpoints plausibly elicits **longer** rankings than a bare control prompt — and longer rankings mechanically reduce censoring and raise Top-3/Top-5 hit rates *without any improvement in localization ability*. **Mandatory diagnostic:** record and compare mean ranking length by condition. Without it, a positive Top-5/EXAM result has an untested and quite mundane alternative explanation. **Optional v2 fix:** require a fixed ranking length (e.g. exactly `min(10, evaluation_denominator)` entries) — noting `parse_ranking` rejects any ranking longer than the denominator, so the cap must be expressed relative to it.

**N6. "Oracle" overstates what the label is.** *(Audit item 5.)* The pilot's labels are single-annotator, un-adjudicated, with no κ measured (`ANNOTATION_GUIDE.md` §4's explicit pilot relaxation), and are derived partly from *task-level* editorial metadata then applied to an individual submission. That is a **single-rater gold-standard proxy**, not an oracle. The usage is internally consistent and `SCIENTIFIC_RISKS.md` §3 correctly frames the arm as an upper bound, so this is a precision issue rather than an error — but it has a real consequence: the oracle-vs-predicted gap that the confirmatory study is meant to bound is *understated*, because even the "oracle" side carries unmeasured label noise. The condition name is frozen in Codex's `pilot.yaml` and should **not** be renamed; the protocol should simply describe it accurately.

**N7. Counterbalancing is close to a scientific no-op.** Each call is a stateless HTTP completion with no conversation carryover, so within-pair "order effects" in the psychological sense cannot occur. `PILOT_PROTOCOL.md` §2's rationale ("cancels position/order effects at the individual-call level") overstates it. It does retain two real but minor benefits: it distributes provider-side temporal drift evenly across conditions, and it balances which arm benefits from shared-prefix prompt caching (relevant to any latency or cost comparison, since control and treatment share a long prefix). Keep the setting; correct the rationale in v2.

**N8. The system prompt primes the control arm for a block that is not there.** `system.txt` ends with "If the user message includes a delimited block that names the program's intended algorithmic pattern…". The text is byte-identical across arms — so every symmetry check passes — but its *effect* is not symmetric: in the control condition the model is told about an absent artifact. Effect is probably small; the honest options are to drop the sentence in v2 and let the block speak for itself, or keep it and document the choice.

**N9. Stale internal cross-reference in a frozen document.** `PILOT_PROTOCOL.md` §5 item 4 tells the analyst to check the observed prompt-length gap against "the ~22-word spread across pattern priors" — the frozen value is **19** (`PATTERN_PRIORS.md` length audit; 22 was the pre-trim draft figure). Trivial in magnitude, but it sits inside a stated run-acceptance criterion, and it is exactly the kind of drift the freeze discipline is supposed to prevent.

**N10. "Dry run" is permitted but its data source is unspecified.** `PILOT_PROTOCOL.md` §2 allows a dry run to check truncation and parser behaviour and to justify a model swap. Nothing says what it runs on. A dry run over manifest programs is peeking, and would contaminate the very sample the pilot exists to measure. Specify: **held-out, non-manifest programs only**, outputs discarded and never analyzed. (This also covers the F4 verification call.)

**N11. ConDefects leakage is acknowledged but unprobed.** `SCIENTIFIC_RISKS.md` §6 flags contamination risk and offers no mitigation. A cheap partial probe — on non-manifest programs, ask the model to reproduce the task's canonical solution or recall the problem statement — would at least bound the concern. Optional for the pilot; should be mandatory before ConDefects carries any confirmatory weight.

**N12. Task-level clustering is absent from the analysis code.** Follows from F3.2 and is fully resolved by it: if `task_id` is unique across included programs, program-level clustering (which the bootstrap already does) is the correct level. Recorded here so the dependency is explicit — if the one-program-per-task rule is ever relaxed, the statistics become wrong and Codex's pipeline will not detect it.

---

## Recommended protocol v2 changes, if any

**No changes are made by this review.** The following is the proposed change-set, pending explicit authorization, split by whether it requires editing a frozen file.

### Additive — new files only, no frozen file edited (preferred; preserves the v1 freeze intact)

| Change | Artifact | Addresses |
|---|---|---|
| Placebo arm | `pilot/placebo_priors.json` — all 12 slugs → one identical generic checklist, matched to 119–138 words and 4–5 checkpoints, zero pattern content | F1 |
| Placebo session config | `pilot/config/pilot_placebo.yaml` with a **different** `experiment_name` (execution-key collision otherwise — see F1) | F1 |
| Selection constraints | A dated addendum (e.g. `pilot/SELECTION_CONSTRAINTS_v2.md`) carrying F2's blinding rule and F3's five constraints: sampling frame + seed, unique `task_id`, single-line faults, ≥25-line floor, `problem_context` all-or-none | F2, F3 |
| Run preconditions | Same addendum: verified echoed model identifier; dry runs on non-manifest programs only; mandatory ranking-length-by-condition diagnostic | F4, N5, N10 |
| Claim qualifier | Addendum to `CLAIM_BOUNDARIES.md` (append-only, never a loosening) adding the pattern-specificity qualifier and prohibition | F5 |

### Requires editing frozen v1 files — authorize only if you want v1 superseded rather than amended

| Change | File | Addresses |
|---|---|---|
| Narrow the pilot to 3–4 pattern classes × 8–10 programs | `PILOT_PROTOCOL.md` §3 | N1 |
| Resolve temperature/repetitions coherently | `PILOT_PROTOCOL.md` §2, `PRE_EXPERIMENT_COMMIT.md` item 7 | N2 |
| Pre-specify the five-McNemar reporting rule; name the bootstrap CI as primary inferential summary | `PRE_EXPERIMENT_COMMIT.md` | N3 |
| Document the multi-line-fault convention and define EXAM\* explicitly | `PILOT_PROTOCOL.md` | F3.3, N5 |
| Fixed ranking length | `pilot/prompts/control.txt` | N5 |
| Drop the conditional-block sentence | `pilot/prompts/system.txt` | N8 |
| Describe the label as a single-rater proxy (do **not** rename the condition) | `PILOT_PROTOCOL.md` §3, `SCIENTIFIC_RISKS.md` §3 | N6 |
| Correct the counterbalancing rationale | `PILOT_PROTOCOL.md` §2 | N7 |
| Fix "~22-word" → 19 | `PILOT_PROTOCOL.md` §5.4 | N9 |
| Correct the §2 mitigation to state that prior-length banding does **not** address the control-vs-treatment confound | `SCIENTIFIC_RISKS.md` §2 | F1 |

Note that any edit to `pattern_priors.json`, `PATTERN_VOCABULARY.md`, or the prior text is **out of scope for all of the above** — see below.

---

## Things that must remain frozen

These survive the review unchanged, and must not be touched under any v2:

1. **The 12 prior strings and the 12-class vocabulary.** Nothing in this review is a reason to reword a prior. `PRE_EXPERIMENT_COMMIT.md` rule 2 (no outcome-driven prior tuning) is the single most important commitment in the specification and is strengthened, not weakened, by these findings. N1's recommendation narrows which patterns the *pilot samples*; it does not alter the vocabulary or any prior text.
2. **The mechanical prompt diff, delimiters, and the forbidden-template-field list.** Codex-owned, verified by execution against the live code, and correct. `PROMPT_DIFF.md`'s reasoning about why `pattern_label` is barred as a template field while the prior may name the pattern in prose is sound.
3. **`count_as_failure` as the primary parser-failure policy**, with `exclude` only as a labeled sensitivity pass.
4. **The metric set and `exact_mcnemar` as the config-level primary statistic** — N3's fix is a reporting rule layered on top, not a substitution.
5. **The no-peeking rule, the freeze-before-`selection_frozen_at` discipline, and the no-silent-exclusion rule.**
6. **Every prohibition currently in `CLAIM_BOUNDARIES.md`.** That document may only ever become *more* restrictive; F5 adds to it and removes nothing.
7. **Pilot scope: ConDefects-Python, oracle-label-only, no SBFL/MBFL/Arm-E comparison.** The scope restrictions are correct and the corresponding claim prohibitions are correct.
8. **The "calibration, not confirmation" framing** — this review makes it more true, not less.

Whichever way N2 (temperature/repetitions) is resolved, the resolution must be recorded and frozen **before** data selection, not chosen once the run is underway.

---

## Final recommendation

# **REVISE FIRST**

Do not proceed to dataset selection under frozen v1.

The specification's process discipline is genuinely strong — the freeze mechanics, the immutability guarantees, the pre-registered analysis plan, and the claim register are better than most work at this scale, and Codex's safety checks are more rigorous than the protocol claims. But process discipline around an under-identified comparison yields a rigorously documented uninterpretable result.

**Minimum viable revision before selection may begin** (in dependency order):

1. Decide F1 — placebo arm (recommended) or accept the attribution ceiling and adopt F5's mandatory qualifier. *This decision determines what the pilot is for; everything else follows.*
2. Adopt F2's annotation blinding and ordering rule.
3. Adopt F3's five selection constraints.
4. Decide N1 — 12 classes × ~2.5 or 3–4 classes × 8–10.
5. Decide N2 — temperature/repetitions.
6. Verify F4's echoed model identifier before spending budget.

Items 1–5 are decisions, not work; they can be settled in a single pass and recorded in one addendum. Item 6 is a single API call. None requires modifying Codex's infrastructure, and — if the additive route is taken — none requires breaking the v1 freeze.

With those six settled, this becomes a defensible calibration pilot. Without item 1 in particular, it produces a number that cannot be attributed to the phenomenon the project exists to study.
