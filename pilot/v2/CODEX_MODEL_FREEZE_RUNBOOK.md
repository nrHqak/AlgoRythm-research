# v2 model freeze and later execution runbook

Prepared 2026-09-10. **Not executed against any provider or scientific candidate.**
The authoritative scientific rules remain in `MODEL_FREEZE_PROTOCOL.md`,
`PILOT_PROTOCOL_V2.md`, and the sampling/ground-truth protocols.

## 1. Supply provider information explicitly

Run from the repository root using `.venv/bin/python` (the verified environment).
Supply the following environment variables yourself; no key is written to files:

- `LLM_API_KEY`: valid key for the selected endpoint.
- `PILOT_PROVIDER_LABEL`: stable provider name.
- `PILOT_BASE_URL`: OpenAI-compatible base URL ending at the API version, without `/chat/completions`, credentials, query, or fragment.
- `PILOT_MODEL_ID`: exact pinned version, not an undated family name or moving alias.
- `PILOT_MODEL_REFERENCE`: provider documentation/version reference proving the ID is pinned.

Choosing an exact identifier is a provider-documentation check, not something a
regular expression can prove. The command rejects `latest` as a pinned ID; it also
requires the provider's returned model string to equal the request exactly. A
missing echoed identity is **unverified**, not an implicit match, and blocks the
freeze. There is no automatic alias resolution or model substitution.

Only if the provider offers no pinned version may the operator instead pass
`--model-kind alias_only --accepted-alias-risk '…explicit recorded justification…'`.
Record the resolved build in the reference/risk text if exposed. This is the
exception already specified in the frozen protocol, not a default fallback.

## 2. Execute the smoke check, then commit its record

**Only run this after valid credentials and the provider/model information above
have been explicitly supplied.** No such information was supplied for this
preflight task, so the live gate remains BLOCKED.

```bash
: "${LLM_API_KEY:?Supply a valid provider credential}"
: "${PILOT_PROVIDER_LABEL:?Supply the provider name}"
: "${PILOT_BASE_URL:?Supply the provider base URL}"
: "${PILOT_MODEL_ID:?Supply the exact pinned model ID}"
: "${PILOT_MODEL_REFERENCE:?Supply the model version reference}"

.venv/bin/python -m experiments.model_preflight \
  --provider openai_compatible \
  --provider-label "$PILOT_PROVIDER_LABEL" \
  --base-url "$PILOT_BASE_URL" \
  --model "$PILOT_MODEL_ID" \
  --model-kind pinned \
  --model-reference "$PILOT_MODEL_REFERENCE" \
  --temperature 0 --max-tokens 1024 --timeout 120 \
  --output pilot/v2/MODEL_FREEZE_RECORD.json

git add pilot/v2/MODEL_FREEZE_RECORD.json results/smoke-freeze EXPERIMENT_LOG.md
git commit -m "Freeze provider and session order after smoke validation"
```

This uses **only** the committed `data/smoke/manifest.json`: three original programs,
two prompt shapes, both prior files = **12 calls** (6 A, 3 B, 3 C). It saves exact
raw prompts/responses before parsing plus processed smoke records. Every artifact
is under a smoke-only session. No Top-K accuracy is computed for model selection.
An inaccurate but mechanically valid response is allowed. All-zero suspicion
scores, empty/malformed responses, truncation, transport failures, or identity
mismatch reject this smoke attempt. Requiring every smoke response to parse is a
conservative operational application of “pass cleanly”; it meets the protocol's
≥90% minimum without changing the scientific parser-failure scoring policy.

A successful attempt writes the dated settings, returned model, finish reasons,
call count, fixture/prompt/prior hashes, and **one random session-order coin flip**.
The main runner requires this record to exist in `HEAD` with unchanged bytes. No
coin was flipped in this preflight task. A failed attempt leaves `VOID.json` and a
log entry, never a passing freeze. Diagnose and document the correction; use a new
artifact/record name for any subsequent attempt. Only mechanical validity and
increasing `max_tokens` may influence this process; never tune priors or select a
model for an arm's accuracy. Raising `max_tokens` requires a new smoke attempt and
new committed freeze, with the same settings then used for both sessions.

## 3. Complete the dataset gate before any real call

Follow `SAMPLING_PROTOCOL.md` and both blinds in `GROUND_TRUTH_PROTOCOL.md`.
Commit the write-once ground-truth record **before** beginning pattern annotation.
Record all stage counts, exclusions, seed 20260910, frame/class allocations,
draw order, and final frozen manifest. Neither smoke fixtures nor synthetic test
programs may enter the frame. Set `PILOT_MANIFEST` to its actual path, then run:

```bash
.venv/bin/python -m experiments.validate_manifest "$PILOT_MANIFEST"
```

Check `--help` if using explicit validation flags. Manifest schema validation
alone does not certify blinding, test execution, frame enumeration, or sampling;
the committed procedural record closes those requirements. The runner enforces
30 ConDefects-Python programs, unique task IDs, single fault lines, omitted context,
physical-line denominators and length limits in addition to its existing checks.
**All six gates must be closed and real execution authorized before step 4.**

## 4. Later main execution (commands prepared, not run)

Set `PILOT_FREEZE=pilot/v2/MODEL_FREEZE_RECORD.json` and supply unique
`PILOT_G_SESSION` / `PILOT_P_SESSION`. Use exactly the provider and settings stored
in that record. If tokens or timeout were raised, update the literals below to
match; mismatches abort before a provider call. Execute the two commands below in
the order of `session_order` in the committed record, back-to-back on the same day.
The order is not a choice to revisit after seeing a session.

```bash
.venv/bin/python -m experiments.run_pilot \
  --config pilot/v2/config/pilot_v2_generic.yaml \
  --manifest "$PILOT_MANIFEST" \
  --system-prompt pilot/v2/prompts/system_v2.txt \
  --user-template pilot/prompts/control.txt \
  --priors pilot/v2/generic_placebo_prior.json \
  --provider openai_compatible --provider-label "$PILOT_PROVIDER_LABEL" \
  --base-url "$PILOT_BASE_URL" --model "$PILOT_MODEL_ID" \
  --temperature 0 --max-tokens 1024 --timeout 120 \
  --condition-order counterbalanced --model-freeze "$PILOT_FREEZE" \
  --session-id "$PILOT_G_SESSION"

.venv/bin/python -m experiments.run_pilot \
  --config pilot/v2/config/pilot_v2_pattern.yaml \
  --manifest "$PILOT_MANIFEST" \
  --system-prompt pilot/v2/prompts/system_v2.txt \
  --user-template pilot/prompts/control.txt \
  --priors pilot/pattern_priors.json \
  --provider openai_compatible --provider-label "$PILOT_PROVIDER_LABEL" \
  --base-url "$PILOT_BASE_URL" --model "$PILOT_MODEL_ID" \
  --temperature 0 --max-tokens 1024 --timeout 120 \
  --condition-order counterbalanced --model-freeze "$PILOT_FREEZE" \
  --session-id "$PILOT_P_SESSION"
```

An identity mismatch stops immediately. The first-50 failure-rate gate is checked
on each chronological prefix (so a failure on the first call stops immediately).
A completed session below 80% `ok` is void. Diagnostics remain saved with a VOID
marker and a log entry; neither analyzer will produce scientific reports from it.
No automatic retries occur; `--resume` refuses a void session. Processed failure
keys are included in duplicate detection even when no raw response exists.

Exit code 1 means aborted/void: stop and investigate. Exit code 2, retained from
the existing runner, means a completed session contains counted failures but has
passed the session-health gates (≥80% ok); retain those records under
`count_as_failure`. Do not treat code 2 as permission to repeat failed responses.
Exit code 0 means all newly created responses parsed successfully. Scientific
validity is never inferred from hit rate: **valid 0% accuracy is not an outage**.

## 5. Later analysis (all outputs remain separate)

```bash
.venv/bin/python -m analysis.run_analysis \
  --config pilot/v2/config/pilot_v2_generic.yaml --manifest "$PILOT_MANIFEST" \
  --session-id "$PILOT_G_SESSION" --results-root results \
  --report-root results/v2-analysis/G --parser-failure-policy count_as_failure

.venv/bin/python -m analysis.run_analysis \
  --config pilot/v2/config/pilot_v2_pattern.yaml --manifest "$PILOT_MANIFEST" \
  --session-id "$PILOT_P_SESSION" --results-root results \
  --report-root results/v2-analysis/P --parser-failure-policy count_as_failure

.venv/bin/python -m analysis.compare_v2_sessions \
  --generic-session "results/processed/algorythm_pattern_prior_pilot_v2_generic/$PILOT_G_SESSION" \
  --pattern-session "results/processed/algorythm_pattern_prior_pilot_v2_pattern/$PILOT_P_SESSION" \
  --manifest "$PILOT_MANIFEST" \
  --output results/v2-analysis/C_vs_B.json
```

Never pass `--allow-mock-analysis` for scientific evidence. The cross-session JSON
follows the SAP reporting order: integrity → null gate → primary → secondary →
diagnostics → sizing → claim boundary. Use its **program-level** results for the
primary comparison, not the native analyzer's pooled call counts or per-call mean
deltas. Native reports remain secondary diagnostics; all five repetition tests
are also included together in the cross-session report. Read the null gate before
interpreting the primary p-value, including the frozen `0 >= 0` tie case.
Apply `CLAIM_BOUNDARIES_V2.md` and perform the protocol's manual transcript spot
check only after a properly authorized real run exists.
