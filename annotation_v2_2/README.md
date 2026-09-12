# v2.2 Blinded Pattern-Annotation Workspace

Remediation of the pattern-label provenance violation documented in
`data/PATTERN_LABEL_PROVENANCE_AUDIT.md` (Option A, authorized by the user).
The v2.0/v2.1 samples were labeled by an unreviewed regex/keyword heuristic,
not by blinded human annotation as `pilot/v2/GROUND_TRUTH_PROTOCOL.md` §6
and `pilot/ANNOTATION_GUIDE.md` §2 require. This workspace exists to produce
genuine, protocol-compliant labels over the same 232-program frame.

**`data/manifests/pilot_manifest_v2_1.json` is permanently preserved,
unmodified, as audit history. Nothing here touches it.**

## What's in this directory

- `blinded_records.jsonl` — 232 records, one per program in the
  reconstructed frame F_v2.1, each containing **only**: annotation index,
  `program_id`, `task_id`, contest, problem letter, difficulty, an AtCoder
  URL (for optional manual lookup — never auto-fetched), line count, and the
  full buggy source. Built by `scripts/build_annotation_workspace_v2_2.py`.
- `frame_manifest.json` — reconstruction provenance: seed, procedure,
  source-file checksum, and an explicit list of every field deliberately
  excluded from every record (fault lines, fixed source, diffs, priors, the
  old automated label, old confidence/rank — none of it was ever loaded
  into this workspace).
- `PATTERN_VOCABULARY_CHEATSHEET.md` — the 12 frozen pattern classes with
  their definitions and confusable-pair rules, condensed from
  `pilot/PATTERN_VOCABULARY.md` for quick reference during annotation, plus
  the number-key legend the CLI uses.
- `README.md` — this file.

## How blinding is enforced

Structurally, not just by discipline: the record-builder script never reads
`ground_truth_freeze_v2.csv`'s `faulty_lines` column, never reads any
`fixed.py`, never reads `pilot/pattern_priors.json` or
`pilot/v2/generic_placebo_prior.json`, and never reads the old
`pattern_label`/`pattern_source` from `pilot_manifest_v2.json` or
`pilot_manifest_v2_1.json`. None of that information exists anywhere in
`blinded_records.jsonl` — it cannot leak into the CLI because it was never
loaded into the process that built the workspace. Verified by a leak scan
across the workspace file (see `data/PATTERN_LABEL_PROVENANCE_AUDIT.md`'s
remediation trail); re-run the scan yourself any time with:

```sh
grep -il "faulty_lines\|pattern_label\|pattern_source\|AST rule\|selection_rank\|correctVersion" annotation_v2_2/blinded_records.jsonl
```

(should print nothing).

## How to annotate

```sh
.venv/bin/python scripts/annotate_patterns_v2_2.py
```

This resumes automatically — it always shows the next program that does not
yet have a confirmed label, in a fixed order (`sorted(task_id)`, matching
the frame's own construction order). Safe to interrupt with Ctrl+C at any
point; every decision is written to
`data/manifests/pattern_annotations_v2_2.csv` immediately, so nothing is
lost and nothing needs to be redone.

**Per program you'll see:** `task_id`, contest/problem/difficulty, an
AtCoder URL you can open by hand if you want problem-statement context
(never fetched automatically — no network calls happen), the full buggy
source with line numbers, and a line of **neutral structural signals**
(e.g., "sort/sorted, while loop" — raw facts only, never a suggested label).

**You'll be asked:**
1. **Label** — a digit `1`–`12` (see the printed legend, or
   `PATTERN_VOCABULARY_CHEATSHEET.md` for full definitions), `o` for
   `outside_vocabulary`, `u` for uncertain (revisit later), or `s` to skip
   without a note. **Speed tip:** type a combined token like `5h` to give
   the label and confidence in one entry.
2. **Confidence** — `h` / `m` / `l` (skipped for uncertain/skip).
3. **Note** — free text, or just press Enter to leave blank.

Other commands at the label prompt: `v` reprints the full vocabulary text,
`b` goes back one record, `q` quits and saves.

**Useful flags:**

```sh
.venv/bin/python scripts/annotate_patterns_v2_2.py --stats
# progress only, no prompts — safe to run anytime, including mid-session

.venv/bin/python scripts/annotate_patterns_v2_2.py --revisit
# only shows programs you marked uncertain/skip

.venv/bin/python scripts/annotate_patterns_v2_2.py --edit 45028964
# re-annotate one specific program_id; the new decision supersedes the old
# one (append-log: the CSV keeps both rows, the latest wins)
```

## When you're done

Run:

```sh
.venv/bin/python scripts/validate_pattern_annotations_v2_2.py
```

This writes `data/manifests/PATTERN_ANNOTATION_AUDIT_V2_2.md` with
completeness status, class distribution, confidence breakdown, and the
`outside_vocabulary` list with reasons. It will tell you plainly whether
you've reached 232/232 confirmed. **Sampling (Step 5, producing
`pilot_manifest_v2_2.json`) does not start until that report says
COMPLETE, and only after you explicitly ask for it.**
