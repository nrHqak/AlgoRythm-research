# Annotation Guide (FROZEN v1)

**Status:** Frozen by the Claude scientific-specification handoff, 2026-09-10.
**Audience:** whoever assembles the candidate manifest for the pilot or the confirmatory corpus — per `PROJECT_STATE.md`, that is currently listed as Antigravity's responsibility ("Antigravity's candidate manifest and validate it with `python -m experiments.validate_manifest`"). This guide is what that manifest's `pattern_label`, `faulty_lines`, `inclusion_status`, and related fields must be produced by, so the manifest can be validated and run without renegotiating the science.
**Manifest shape reference:** `docs/PILOT_RUNBOOK.md` §"Manifest shape"; field-level validation: `experiments/models.py::ProgramRecord`.

## 1. Selecting candidates

Source: ConDefects-Python (`dossier/04_block4_datasets.md` §4.3) for the pilot; additional sources only for the confirmatory corpus per `dossier/99_synthesis.md` §S1.

A candidate is **includable** only if all of the following hold (`inclusion_status: included`; otherwise `excluded` with a `exclusion_reason` and `exclusion_decided_at` before `selection_frozen_at` — see `experiments/models.py::ProgramRecord.validate_files_and_selection`, which rejects excluded records missing either field, and `ProgramManifest.validate_manifest`, which rejects any exclusion timestamped after the freeze):

1. **Compiles / runs** without a syntax error.
2. **At least one passing and at least one failing test** in `tests_path`. Programs failing all tests are excluded (`exclusion_reason: "fails all tests — FL preconditions undefined, Araujo et al. 2016"`) — this is not a judgment call, check it mechanically by running the test suite.
3. **A single identifiable fault**: the fix (buggy → fixed diff) is one contiguous hunk, or, if not, a manual read confirms every changed line traces to one logical error (e.g. a comparison operator wrong in three call sites of the same helper still counts as one fault). If the diff clearly contains two or more independent fixes, exclude (`exclusion_reason: "multiple independent faults"`).
4. **10–300 physical lines** in `buggy_source_path`.
5. **Fits a class in `PATTERN_VOCABULARY.md`** — see §2. If not, exclude (`exclusion_reason: "pattern outside frozen vocabulary v1"`).

## 2. Assigning `pattern_label`

1. Start from the task's own reference/intended solution technique, using AtCoder task metadata/editorial where available (`dossier/04_block4_datasets.md` §4.3: "AtCoder tasks map to known algorithm categories... a realistic route to pattern labels via task→technique mapping").
2. Read the **candidate's own buggy submission** and confirm it is structurally attempting that same technique (has the shape of a two-pointer loop, a DP table, etc.) — not merely that the task's canonical solution uses it. Label by what the submission is attempting, per `PATTERN_VOCABULARY.md`'s inclusion rule.
3. If the task admits multiple valid techniques (e.g. solvable by either DP or greedy) and the submission is ambiguous, prefer the technique whose structural signature is actually present in the code (a table/memo present → `dynamic_programming`; a sort followed by sequential choice-commitment → `greedy`).
4. Apply the confusable-pair disambiguation rules in `PATTERN_VOCABULARY.md` (two_pointers vs. sliding_window vs. sorting_based; dynamic_programming vs. brute_force_implementation; brute_force_implementation vs. simulation; etc.) in the stated order.
5. Record `pattern_source` as a short machine-readable provenance string, e.g. `"atcoder-task-tag+manual-verification"` or `"manual-annotation-only"` — this field exists precisely so a later audit can tell how confident a given label is.
6. `pattern_label` must be **exactly** one of the 12 slugs in `PATTERN_VOCABULARY.md` — copy-paste, do not retype (case and underscore placement are exact-match requirements downstream: `experiments/run_pilot.py` computes `missing_priors = {p.pattern_label for p in manifest.included} - set(priors)` and aborts the run if any label lacks a matching key in `pilot/pattern_priors.json`).

## 3. Determining `faulty_lines`

Ground truth = the first-changed-line(s) of the accepted fix (`dossier/99_synthesis.md` §S1: "first-changed-line of the accepted fix, adjusted by manual review (fix may refactor)"). Concretely:
1. Diff `buggy_source_path` against `fixed_source_path`.
2. If the fix is a pure correction (same statement, changed operator/operand/bound), `faulty_lines` = that line's number(s) in the **buggy** file.
3. If the fix refactors around the bug (e.g. splits one line into three, or moves a statement), use judgment to mark the **minimal buggy-file line range** that a developer inspecting only the buggy file, without seeing the fix, would need to change — not every line the diff happens to touch syntactically.
4. `faulty_lines` must be line numbers in the **buggy** file (1-indexed), must not exceed the buggy file's physical line count, and must be unique (`experiments/models.py::ProgramRecord.ground_truth_is_present_and_unique`).

## 4. Annotation reliability protocol

- **Pilot (n=30):** single-annotator labeling is acceptable, but every `pattern_label` decision must leave a one-line rationale in the annotator's own working notes (not necessarily in the manifest) referencing which rule in §2 applied, especially for any candidate that triggered a confusable-pair rule. This is a documented relaxation for calibration purposes only, per `CLAIM_BOUNDARIES.md`.
- **Confirmatory corpus (n≥300, future work):** double annotation is required — the original annotator plus 2 independent annotators on a 100-program calibration subset, reporting Cohen's κ ≥ 0.70 before trusting single-annotator labels on the remainder (`dossier/99_synthesis.md` §S1). Disagreements are adjudicated by a third reader; adjudicated labels, not majority vote, become ground truth. This threshold and procedure are carried over unchanged from the dossier and are not renegotiated by this pilot.
- Any pattern class that repeatedly causes annotator disagreement at the confirmatory stage is a signal to revisit `PATTERN_VOCABULARY.md`'s confusable-pair rules for that class (e.g. formally splitting `graph_traversal_dfs_bfs` into `dfs`/`bfs` if κ data supports it) — not to silently relabel individual programs against the written rule.

## 5. Worked examples (for annotator calibration)

- **`two_pointers` vs. `sorting_based`:** a "3Sum"-style task solved by sorting the array and then, for each fixed first element, running a two-pointer scan over the remainder → the two-pointer scan is the algorithmic core (fixing one element and converging two pointers is the nontrivial idea); label `two_pointers`. A "find the two closest values after sorting" task solved by a single adjacent-pair scan with no convergence logic → label `sorting_based`.
- **`dynamic_programming` vs. `brute_force_implementation`:** a coin-change submission with a `memo = {}` dict and a recursive function checking `if state in memo` before recursing → `dynamic_programming`, even if the memo check is itself buggy (e.g. checking the wrong key) — the memo's *presence* is what defines the class, not its correctness. The same recursive function with no memo at all → `brute_force_implementation`.
- **`brute_force_implementation` vs. `simulation`:** a submission that tries every pair `(i, j)` to find a maximum → `brute_force_implementation` (searching a solution space). A submission that steps a robot through N commands updating its position and direction each step → `simulation` (stepping a described process), even though both use nested/sequential loops.

## 6. What NOT to do

- Do not assign `pattern_label` by copying the task's official tag/category name if it uses different terminology than `PATTERN_VOCABULARY.md` — always map through the definitions in that document, not through a source platform's own taxonomy.
- Do not adjust `faulty_lines` or `pattern_label` after `selection_frozen_at` for any reason connected to how the pilot ran (see `PRE_EXPERIMENT_COMMIT.md`'s stopping rule) — a labeling mistake discovered post-freeze is corrected in a new, separately versioned manifest, not by silently editing the frozen one.
- Do not include a program solely because it is convenient (e.g. short, or already familiar) — apply §1's filters mechanically and record exclusions, per `dossier/05_block5_methodology.md` §5.5's warning about confounds in FL evaluation.
