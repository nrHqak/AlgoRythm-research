# Gate 7 testcase provenance audit

**Verdict: PASS — reproducible third-party archive/mirror.**

Audited against dataset commit `9c837677cd17f52f9b1c8f9cb664f28b84743fe1`
and manifest SHA-256
`d53bcdc232f7e4daebca3248e53e060143a32e2638bb99959fda4c0db38e6ca3`.
Exact audit timestamps, upstream commits, per-case URLs and SHA-256 checksums are
in [GATE7_TESTCASE_PROVENANCE.json](manifests/GATE7_TESTCASE_PROVENANCE.json).

## Classification and evidence

| Classification | Programs | Packaged cases |
|---|---:|---:|
| Official AtCoder source | 0 attributed by this audit | 0 |
| ConDefects-provided artifact | 0 attributed by this audit | 0 |
| Reproducible third-party archive/mirror | 30 | 211 |
| Unknown | 0 | 0 |

All 211 packaged input/output pairs match the decoded upstream files exactly,
including whitespace. For every task, their order also matches the complete
sequence selected by the acquisition script's size/order rule. This is a content
comparison, not a conclusion inferred from the fixed program's output. No
testcase, expected output, cache, candidate source, or manifest was changed.

The matched repository is
[conlacda/atcoder-testcases](https://github.com/conlacda/atcoder-testcases),
published under the GitHub account `conlacda`. Its description identifies a
Dropbox folder as its upstream source. There is no evidence in the inspected
repository that AtCoder maintains or publishes this GitHub mirror. Its contents
must therefore be described as a **third-party archive**, even if the ultimate
data originated with AtCoder. We did not authenticate the Dropbox-to-mirror
chain or compare the archive to AtCoder's original judge bundles.

[ConDefects' README](https://github.com/appmlk/ConDefects/blob/43f0834a82c5e3bc4516c079fe7765f63b1a15cd/README.md)
separately offers `Test.zip` through OneDrive and Baidu Drive. The executed
acquisition code does not download that artifact, and this audit does not
attribute these packaged cases to it.

## Exact acquisition route

The following trace comes from independently reading
`data/CONDEFECTS_SOURCE.md`, `data/manifests/SAMPLING_AUDIT_V2_1.md`,
`scripts/build_dynamic_test_eligibility_v2_1.py`, and
`scripts/package_final_sample_v2_1.py`:

1. The dynamic eligibility script first reuses
   `data/cache/testcases/<task_id>.json` if it exists and parses as JSON.
   Cache records contain only input and expected output, without source URLs,
   filenames, acquisition timestamps, or commit IDs.
2. On a cache miss, it requests the third-party mirror's contest branch:
   `https://raw.githubusercontent.com/conlacda/atcoder-testcases/refs/heads/<contest>/<contest>/<problem>/list.txt`.
   It tries upper/title/lowercase problem letters and `Ex` for problem H.
3. It prioritizes names containing `example`, `sample`, `hand`, or `000`, then
   sorts by listed size, retaining original list order for ties. It selects at
   most eight entries with listed size at most 30,000 bytes. It downloads paired
   `in/<name>` and `out/<name>` files, decoding UTF-8 with errors ignored.
4. Failed individual downloads are skipped. Only if no mirror case remains does
   it request `https://atcoder.jp/contests/<contest>/tasks/<task_id>` and extract
   the English Sample Input/Output blocks. That fallback would be an **official
   AtCoder source for statement samples**, not a full judge suite.
5. The packaging script copies cached pairs unchanged in content and order into
   the committed `data/raw/<program_id>/tests.json`. These are the suites executed
   in the independent Gate 7 sanity check.

The ignored acquisition cache and original network logs are absent from this
checkout. Consequently, the exact historical request route cannot be attested
from acquisition logs. Instead, Gate 7 reconstructs the provenance of **every
executed pair** by exact content matching against pinned mirror files. All 30
suites match the mirror selection sequence; no suite requires the official-page
fallback to reproduce it. Identical statement samples could exist at both sources.

## Reproducibility and limitations

The original fetch used moving branch names. Gate 7 resolves each needed contest
branch to a full commit ID and verifies the frozen bytes at that immutable URL.
These are **Gate 7 reconstruction pins**, not a claim that Antigravity recorded
them at download time. The evidence JSON gives each task's commit, list URL and
hash, selected filenames, and each input/output URL and hash. The committed
packaged JSON and its checksum preserve the actual executed suite even if a
remote host later becomes unavailable.

Only **3–8 cases per task** were packaged (211 total). The maximum-eight and
30,000-byte filters favor examples and small cases; this is not an exhaustive
AtCoder judge suite. “Fixed passes every available test” in Gate 7 means every
test in the frozen manifest's `tests_path`, not every case available elsewhere
on the internet. Small-case selection can miss defects, large-input failures,
and performance failures. This limitation applies to the entire dynamic
eligibility frame, not just the final sample.

The actual comparator strips empty lines and surrounding whitespace, compares
tokens within each remaining line, and accepts numeric tokens when absolute
error is below `1e-6` or relative error is below `1e-6`. It is not a task-specific
AtCoder checker. The dynamic filter uses a 2.5-second timeout per execution;
packaging uses 4 seconds. Gate 7 independently used 2.5 seconds under Python
3.14.3, with no timeouts. `CONDEFECTS_SOURCE.md`'s exact-output/5-second description
does not describe these scripts accurately.

The third-party origin, the reconstructed pins, and these limits are sufficiently
documented and reproducible for the pilot under the user's stated acceptance
criterion. No synthetic data or outputs generated from fixed code were needed
to reproduce any packaged pair. This does not certify how the third-party
publisher originally obtained each pair.

## Corrections to earlier prose

The phrases “official git mirror,” “AtCoder official tests,” and “official
AtCoder contest archives (`atcoder-testcases` ...)” in the source document,
sampling audit, and handoff overstate the evidence. **This audit supersedes
those provenance descriptions**; it does not rewrite frozen historical records.

Separately, the roster in `SAMPLING_AUDIT_V2_1.md` contains 27 faulty-line and
28 difficulty values that disagree with the authoritative JSON. The JSON's
faulty lines match the earlier frozen ground-truth CSV and the single-line code
diffs in all 30 cases. See
[GATE7_ROSTER_DISCREPANCIES.json](manifests/GATE7_ROSTER_DISCREPANCIES.json).
Use the manifest, not that prose table, for execution and analysis.

## Reproduction commands

These commands make no model calls. The provenance command downloads public
testcase files without executing candidates or modifying frozen tests:

```bash
.venv/bin/python scripts/audit_gate7_provenance.py \
  --pins data/manifests/GATE7_TESTCASE_PROVENANCE.json \
  --output /tmp/algorythm-gate7-pinned-replay.json

.venv/bin/python scripts/audit_gate7_dataset.py
```

The first command uses the recorded commits rather than current branch tips.
The second executes both versions against all packaged cases and writes only
`data/manifests/GATE7_DATASET_SANITY.json`, without exposing source or program
output in the report. The separate freeze-integrity evidence supplies the
candidate-result artifact/history check.
