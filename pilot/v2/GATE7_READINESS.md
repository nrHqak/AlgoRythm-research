# Gate 7 readiness

Dataset base: `9c837677cd17f52f9b1c8f9cb664f28b84743fe1` on
`origin/agent/antigravity-data-v2`. Work branch: `agent/codex-gate7`.
Audit date: 2026-09-10 UTC. No provider selected and no live model calls made.

| Gate | Result |
|---|---|
| Dataset sanity | **PASS** |
| Test provenance | **PASS** — reproducible third-party archive/mirror |
| Scientific freeze integrity | **PASS**, within the repository evidence scope below |
| Model freeze | **WAITING FOR USER** |
| Full pilot | **NOT YET AUTHORIZED** |

## Complete starting state

Fetched `origin` and independently verified both ancestors with
`git merge-base --is-ancestor`:

| Required ancestor | Verified commit |
|---|---|
| `origin/agent/claude-science` | `579c68737ca4bd762bcbd7e57e3d28577e2c40bc` |
| `origin/agent/codex-v2-preflight` | `96de08d9cf2c7cc40c7f3028da1f15b74a035a13` |

The starting tree contains `pilot/v2/`, `analysis/compare_v2_sessions.py`,
`data/manifests/pilot_manifest_v2_1.json`, and
`data/ANTIGRAVITY_HANDOFF_V2_1.md`. The worktree was clean before branching.

## Independent dataset sanity

The authoritative manifest is `data/manifests/pilot_manifest_v2_1.json`.
Its `selection_frozen_at` is `2026-09-10T17:51:43.488565+00:00`.
SHA-256 before and after execution, matching the handoff and committed bytes:

`d53bcdc232f7e4daebca3248e53e060143a32e2638bb99959fda4c0db38e6ca3`

| Check | Result |
|---|---|
| Exactly 30 records, all included | PASS — 30 |
| Unique program IDs | PASS — 30 |
| Unique task IDs | PASS — 30 |
| Valid buggy/fixed/test paths | PASS — all 90 files exist |
| Exactly one frozen faulty line | PASS — all 30 match the earlier ground-truth CSV and single-line replacement diff |
| Buggy has at least one passing and one failing test | PASS — all 30 |
| Fixed passes all available packaged tests | PASS — 211/211 |
| Physical LOC within frozen [25, 300] | PASS — observed [25, 155] |
| Denominator equals physical buggy LOC; context omitted | PASS — all 30 |
| Labels belong to frozen vocabulary | PASS — all 30; allocation 8/8/7/7 |
| Syntax valid under pinned Python | PASS — Python 3.14.3, both versions |
| Stable manifest/source/test hashes | PASS — all input bytes unchanged |
| Previous candidate LLM-result artifact | PASS — none found for any of the 30 IDs |

Independent execution: **422 subprocess runs**, 211 cases × two versions;
buggy totals 153 passing / 58 failing, fixed totals 211 passing / 0 failing.
No execution timed out. All per-program counts match the committed dynamic
eligibility CSV. No membership, testcases, annotations, priors, prompts, or
scientific analysis code were edited.

The verifier independently implements the recorded output-comparison semantics
and runs every case with the dynamic filter's 2.5-second timeout. “Available”
means the frozen packaged suite; it does not imply exhaustive upstream tests.

Evidence:
[GATE7_DATASET_SANITY.json](../../data/manifests/GATE7_DATASET_SANITY.json),
[audit_gate7_dataset.py](../../scripts/audit_gate7_dataset.py), and
[GATE7_FREEZE_INTEGRITY.json](../../data/manifests/GATE7_FREEZE_INTEGRITY.json).
The existing `experiments.validate_manifest` also returns `valid: true`.
The existing regression suite passed: **65 tests in 8.94 seconds** (`pytest -q`).
An additional provenance replay using only the newly recorded commit pins
passed for all 30 tasks / 211 cases; its per-task evidence matched the initial
provenance audit. These checks made no live model calls.

## Test provenance

**PASS:** every packaged input/output pair matches
`conlacda/atcoder-testcases` at a recorded immutable Git commit, including the
full selected order for each task. All 30 suites / 211 cases are classified as a
**reproducible third-party archive/mirror**. The mirror is not established to be
maintained or published by AtCoder. No ConDefects `Test.zip` acquisition is shown
by the executed scripts. No official-page fallback is needed to reproduce this
sample's packaged content.

See [TESTCASE_PROVENANCE_AUDIT.md](../../data/TESTCASE_PROVENANCE_AUDIT.md)
and its per-case URL/checksum evidence. It documents original moving refs,
missing acquisition logs, Gate 7 reconstruction pins, small-case selection,
comparator semantics, and the difference from a full AtCoder judge suite.

The old narrative roster is unreliable: **27 faulty-line values and 28
difficulty values differ from the manifest**. These are documentation errors,
not detected mutations of the frozen JSON. All 30 manifest fault lines agree
with the original committed ground truth and mechanical diffs. The new audit
records the discrepancies without changing frozen data.

## Scientific freeze integrity

| Required assertion after v2.1 `selection_frozen_at` | Result and evidence |
|---|---|
| Sample membership unchanged | PASS — v2.1 JSON/CSV have one introducing commit, `9c83767`; current bytes equal those first committed bytes. The documented v2.0 → v2.1 replacement predates this freeze. |
| `faulty_lines` unchanged | PASS — all 30 agree with `ground_truth_freeze_v2.csv`, introduced in ancestor `60ddd8a` and never changed. |
| Pattern-specific priors unchanged | PASS — JSON and prose remain byte-identical to `81fd51d`. |
| Generic placebo prior unchanged | PASS — JSON and prose remain byte-identical to `579c687`. |
| Primary statistical code committed before results | PASS — `analysis/compare_v2_sessions.py` introduced unchanged in `96de08d` (2026-09-10 12:03:09 UTC), before dataset freeze; statistics/metrics in `c5265d0`, SAP in `579c687`. No scientific results exist in the inspected record. |
| No real candidate sent to an LLM | PASS in the audited record — no raw/processed/session results or candidate-bearing response artifacts, no run entries in `EXPERIMENT_LOG.md`, and the committed dataset handoff attests no model evaluation. Gate 7 made zero model calls and did not display candidate source to the assistant. |

The history check examined all fetched refs, 68 reachable historical JSON blobs,
current local JSON/JSONL artifacts including untracked files outside tool caches,
and the `results/` history. That directory contains only its original README
files. No candidate ID occurs in a response-bearing artifact. Per-program
absence checks and exact asset hashes are in `GATE7_FREEZE_INTEGRITY.json`.

**Evidence limit:** Git and the available working tree cannot prove the absence
of unrecorded external calls, deleted uncommitted artifacts, or intermediate
uncommitted edits. The PASS is for the available repository record, supported
by the prior operator's handoff; it is not a provider-side audit. Git topology
establishes the ground-truth commit precedes selection. Its CSV's literal
`18:05:00+00:00` row timestamps conflict with the earlier commit time and even
postdate v2.1's timestamp, so those row timestamps are not used as chronological
proof and have been preserved rather than silently corrected.

## Model freeze: waiting for user information

Read and retained the requirements in
[MODEL_FREEZE_PROTOCOL.md](MODEL_FREEZE_PROTOCOL.md) and
[CODEX_MODEL_FREEZE_RUNBOOK.md](CODEX_MODEL_FREEZE_RUNBOOK.md).
No provider/model information or credential has been explicitly supplied for
this execution task. No credential values were inspected, printed, or written.
There is no passing `MODEL_FREEZE_RECORD.json`, and no session-order coin has
been flipped.

Provide these exact inputs next:

| Input | How to supply it |
|---|---|
| Provider name | `PILOT_PROVIDER_LABEL` or tell me the name |
| OpenAI-compatible API base URL | `PILOT_BASE_URL`; API-version base without `/chat/completions`, credentials, query, or fragment |
| Exact pinned model identifier | `PILOT_MODEL_ID`; the exact request string, not an invented family name |
| Provider documentation proving that version is pinned | `PILOT_MODEL_REFERENCE` or a documentation URL |
| API credential | Set `LLM_API_KEY` securely in the environment available to the execution process; tell me it is set. Do not paste the key into chat or commit it. |

If the provider offers **only** an alias, supply its exact identifier, the
documentation establishing that limitation, the resolved build if exposed, and
your explicit acceptance of the alias risk. The pre-registered alias exception
requires `--model-kind alias_only --accepted-alias-risk ...`; it is not assumed.

Prepared smoke command below is **not executed**. It may run only once the
requested inputs are explicitly supplied and verified. The user has permitted
the registered smoke calls; the full pilot still requires separate explicit
authorization.

```bash
: "${LLM_API_KEY:?Set the credential securely in the execution environment}"
: "${PILOT_PROVIDER_LABEL:?Supply provider name}"
: "${PILOT_BASE_URL:?Supply API base URL}"
: "${PILOT_MODEL_ID:?Supply exact pinned identifier}"
: "${PILOT_MODEL_REFERENCE:?Supply version documentation}"

.venv/bin/python -m experiments.model_preflight \
  --provider openai_compatible \
  --provider-label "$PILOT_PROVIDER_LABEL" \
  --base-url "$PILOT_BASE_URL" \
  --model "$PILOT_MODEL_ID" \
  --model-kind pinned \
  --model-reference "$PILOT_MODEL_REFERENCE" \
  --temperature 0 --max-tokens 1024 --timeout 120 \
  --output pilot/v2/MODEL_FREEZE_RECORD.json
```

This performs 12 calls using only `data/smoke/`: six without a prior, three
generic-placebo, and three pattern-prior. Acceptance checks mechanical validity
and exact echoed model identity, not localization accuracy. A passing record
and smoke artifacts must be committed before any scientific execution. Both
sessions would then use the same frozen settings and recorded random order.

For a later separately authorized pilot, the manifest must be explicitly set to
`data/manifests/pilot_manifest_v2_1.json`; the commands already prepared in the
runbook must not use the obsolete v2.0 manifest. **None of the 600 scientific
calls is authorized or executed by this Gate 7 task.**

## Subsequent Gemini freeze attempt — 2026-09-10

Provider, endpoint, and `gemini-3.8-flash` were supplied by the user. The credential
was unavailable to both login and non-login execution processes. Gates 4 and 5
are BLOCK; zero authenticated API requests, smoke calls, candidate calls, or coin
flips occurred. This supersedes the earlier statement that provider/model inputs
were not supplied. See [GATE4_GATE5_STATUS.md](GATE4_GATE5_STATUS.md) and its
immutable precheck evidence. Full scientific execution remains unauthorized.

## Gemini smoke attempt with supplied credential

Authenticated model retrieval succeeded. The first registered smoke response
matched `gemini-3.8-flash` exactly and parsed successfully; the second returned
HTTP 503 / UNAVAILABLE (high demand). The smoke session is VOID. Gate 4 remains
BLOCK and Gate 5 remains BLOCK with no coin flip. Two calls were attempted, one
succeeded, zero parser failures occurred, and no scientific candidate was sent.
No settings changed. See [GATE4_GATE5_STATUS.md](GATE4_GATE5_STATUS.md) for the
current result; the earlier credential-precheck record remains historical.

## Latest authorized Gemini smoke retry

Fresh session `20260910T185841547998Z` used identical frozen settings and assets.
Calls 1–3 passed; call 4 returned HTTP 503 UNAVAILABLE/high demand. The procedure
stopped and marked the session VOID. Gate 4: BLOCK; Gate 5: BLOCK; parser failures:
0; coin flips: 0; scientific calls: 0. No automatic retry. Current evidence is in
[GATE4_GATE5_STATUS.md](GATE4_GATE5_STATUS.md).

## Latest OpenRouter attempt

The user authorized OpenRouter / `z-ai/glm-5.3-flash`. Z.AI `z-ai/fp8` was pinned
with fallbacks disabled before generation. All 12 responses matched the model and
provider; 11 parsed successfully, while call 12 exhausted max_tokens=1024 and
returned null completion text. The session is VOID. Gate 4: BLOCK; Gate 5: BLOCK;
parser failures: 0; coin flips: 0; scientific calls: 0. Generation settings and
scientific inputs remain unchanged. See [GATE4_GATE5_STATUS.md](GATE4_GATE5_STATUS.md).
