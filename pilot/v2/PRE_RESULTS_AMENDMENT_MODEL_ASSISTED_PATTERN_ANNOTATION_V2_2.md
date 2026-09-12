# PRE-RESULTS AMENDMENT — v2.2 model-assisted pattern annotation

**Authorized:** 2026-09-12  
**Status:** frozen before any valid scientific result  
**Scope:** pattern labeling for the frozen 232-program task-independent frame

## Amendment

The planned manual-human/oracle annotation is replaced by **independent
blinded model-assisted annotation**. Annotator A is Claude and Annotator B is
Codex. Both annotate all 232 programs independently. These labels must never be
described as human labels or oracle labels.

The reason for the amendment is operational: the user cannot manually classify
232 programs within the available time. This change was authorized before any
valid scientific result existed. Earlier scientific attempts were declared VOID
for technical output-token failures. No localization metrics or performance
results were inspected. Their preserved files remain audit history and are not
inputs to this annotation procedure.

This amendment supersedes the manual-human assumption for v2.2 pattern labels.
It does not rewrite or delete any earlier protocol, provenance audit, manifest,
VOID-run evidence, or freeze record.

## Frozen frame and allowed inputs

The annotation population is the same 232-program task-independent frame in
`annotation_v2_2/frame_manifest.json`. The only program packet supplied to an
annotator is `annotation_v2_2/blinded_records.jsonl`, containing:

- annotation index;
- `program_id` and `task_id`;
- buggy source;
- allowed task metadata: contest, problem letter, difficulty, AtCoder URL, and
  source line count.

Each annotator also receives the frozen `pilot/PATTERN_VOCABULARY.md` and its
confusable-pair rules. Each record receives exactly one of the 12 frozen slugs,
`outside_vocabulary`, or `uncertain`, together with confidence and a short
rationale.

The following data are prohibited annotation inputs: every old v2.1 AST/regex
label, `faulty_lines`, any `fixed.py`, buggy/fixed diffs, pattern priors, the
generic placebo prior, old sample membership, and previous LLM localization
outputs. The blinded packet structurally omits these fields.

Frozen input hashes at the time of Codex annotation:

- frame manifest SHA-256:
  `947a9f1bc338b44b8374826e8e4a7c918766bfd06d2ea73ba032539872c71219`
- blinded records SHA-256:
  `8a1924066287ec9b9110018e5e301736dd4d1921be9b4dc0d06396264bdf0b99`
- pattern vocabulary SHA-256:
  `bba2bfe5659f365eb48192d5c6c8c073139a11a8d4b468c564eb031ba8bd7d5b`

## Independence and blinding

Claude and Codex produce separate files and must not see the other annotator's
answers before both files are frozen. Codex did not open, parse, hash, validate,
or otherwise inspect a Claude annotation file while producing
`data/manifests/pattern_annotations_codex_v2_2.csv`. Codex used only the allowed
blinded packet, vocabulary, and confusable-pair rules.

Codex annotation SHA-256:
`dc89712a1cfd056652f05899d816605fdce757ace3ba8d181974fd48879a5c40`.

## Agreement analysis and adjudication

After both annotation files exist, run
`scripts/compare_pattern_annotations_v2_2.py` with their explicit paths. The
tool computes raw agreement, Cohen's kappa, the full confusion matrix, total
disagreements, and disagreements by each annotator's pattern label. It creates a
blinded disagreement packet containing only:

- `program_id` and `task_id`;
- buggy source and allowed task metadata;
- Claude label and Codex label.

The comparison stage does not resolve or overwrite any disagreement. A third
independent adjudicator receives only that disagreement packet. An agreed label
must record `label_source = model-consensus`; a label selected after third-party
adjudication must record `label_source = model-adjudicated`.

Agreement is a reliability statistic, not evidence that either model is
correct. No sampling or scientific execution may treat the labels as human or
oracle ground truth.

## Limitations

- The annotators are models and may share training-data exposure, common
  heuristics, and correlated mistakes; their errors are not independent in the
  same sense as two independently trained human experts.
- Some submissions implement a noncanonical method or contain too little
  structure to identify the intended algorithm confidently.
- Task metadata can support interpretation but does not prove which technique
  the buggy submission attempted.
- The frozen 12-class vocabulary omits valid techniques such as Union-Find,
  network flow, segment/Fenwick trees, linear bases, and several number-theory
  methods. `outside_vocabulary` is therefore substantive, not a failed label.
- Cohen's kappa is sensitive to class prevalence and cannot establish label
  validity. Third-model adjudication can resolve a recorded disagreement but
  cannot turn the resulting labels into human/oracle labels.

## Scientific state

This amendment and both independent annotations must be committed before any
new sample is drawn or any scientific candidate is sent to the localization
model. The scientific experiment remains unrun under v2.2.
