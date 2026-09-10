# Model Freeze Protocol (FROZEN v2)

**Status:** frozen 2026-09-10, before any provider or model has been selected.
**Resolves:** `pilot/PRE_RUN_REVIEW.md` **F4** — the model-alias failure mode, in which a plausible-looking configuration produces a complete, non-aborting, entirely worthless run.

---

## 1. The failure mode this exists to prevent

Verified in Codex's code, not hypothesized:

- `experiments/providers/http.py` sets `ProviderReply.model = str(body.get("model") or request.model)` — the identifier the API **echoes back**.
- `experiments/run_pilot.py::run_one` then checks `if reply.provider != provider.name or reply.model != model:` and, on mismatch, records `status="provider_failure"`, `error_type="ModelIdentityMismatch"`.

Most providers echo a **dated snapshot** in response to an alias request (`gpt-4o` → `gpt-4o-2024-08-06`; `…-latest` → a pinned build). Every call would then be a provider failure — and the failure is quiet:

- `provider_failure` records carry `raw_response_path: None`, so `assert_raw_files_exist` skips them and `assert_raw_prompt_symmetry` finds no pairs to check;
- `assert_condition_balance` still passes — the records exist and are balanced;
- `analysis/metrics.py::evaluate_record` scores every failed run `top1 = top3 = top5 = 0`, `exam = 1.0`.

The result is a complete analysis run, with figures, reporting 0% vs 0% — an artifact that looks finished, has no raw responses to recover from, and consumed the entire budget.

## 2. Freeze requirements

Before the dry run:

1. **Provider fixed.** One `openai_compatible` HTTP(S) endpoint, recorded by base URL. No mid-study provider change; a change voids the study and requires a fresh freeze.
2. **Exact model identifier fixed.** The precise string to be sent as `model`. **Moving aliases are prohibited** where a pinned identifier exists — no bare `…-latest`, no undated family name. If the provider offers only an alias, this must be recorded explicitly as an accepted risk, together with the alias's resolved build at freeze time if the API exposes it.
3. **Echoed identity verified.** The string the provider returns in `body["model"]` must **exactly equal** the string sent. This is the specific check that the alias failure mode violates.
4. **Settings fixed:** `temperature = 0`, `max_tokens` (floor 1024, may be raised after §3 finds truncation, never lowered), `--timeout`.
5. **All of the above recorded** in a dated pre-experiment record, committed **before** the main run, alongside the session-order coin flip required by `PILOT_PROTOCOL_V2.md` §3.2.

The same frozen values must be used for **both** sessions (`PILOT_PROTOCOL_V2.md` §3.1). Changing any of them between sessions invalidates the primary comparison.

## 3. Dry run

**Data:** smoke/test fixtures only (`data/smoke/`), never a candidate program from the sampling frame, and never a program that could enter the manifest. This is a hard rule: a dry run over candidates is peeking, and would contaminate the sample the pilot exists to measure (`SAMPLING_PROTOCOL.md` §1).

**Size:** at least 10 calls — at least 5 with no prior block and at least 5 with a block, so that both prompt shapes are exercised. Use both `generic_placebo_prior.json` and `pattern_priors.json` at least once each.

**Purpose:** verify that the configuration produces valid, non-empty, parseable, untruncated structured responses. Nothing else.

**Explicitly prohibited use of the dry run:**
- tuning, rewording, or "improving" any prior — pattern or placebo (`pilot/PRE_EXPERIMENT_COMMIT.md` rule 2, extended in `GENERIC_PLACEBO_PRIOR.md` §6);
- tuning the system prompt or user template;
- choosing a model on the basis of which one appears to favour any arm.

The only decisions the dry run may drive are: accept/reject the model on mechanical validity grounds, and raise `max_tokens`.

## 4. Abort criteria

### 4.1 Dry-run aborts (fix and re-run the dry run; do not proceed)

| Condition | Action |
|---|---|
| **Any** `ModelIdentityMismatch` (echoed model ≠ requested string) | **Abort.** Correct the model string to the echoed identifier and re-dry-run. This is the F4 landmine; there is no acceptable rate above zero. |
| Parse-success rate < 9/10 | **Abort.** The prompt/schema/model combination is not fit for the run. Change the model — **not** the priors. |
| Any empty or whitespace-only completion | **Abort.** Investigate before proceeding. |
| Any `finish_reason == "length"` (truncation) | **Abort.** Raise `max_tokens` and re-dry-run. |
| Any provider transport error not attributable to a transient network fault | **Abort.** Resolve before proceeding. |

A dry run must pass **cleanly**, not "mostly," before the main run begins.

### 4.2 Main-run aborts

| Condition | Action |
|---|---|
| `provider_failure` rate > 5% within the first 50 calls | **Stop the run.** Diagnose before spending further budget. Do not `--resume` past an unexplained failure cluster. |
| Any `ModelIdentityMismatch` at any point | **Stop immediately.** The model identity changed underneath the run; everything after the change is not comparable to what came before. |
| Overall `ok` rate < 80% across a completed session | **The session is void as scientific data.** It may be reported as an engineering finding only. |
| **All** records non-`ok` | **Void.** Explicitly: this must fail loudly and must never be analyzed, reported, or interpreted as a 0%-vs-0% scientific result. |
| Mock provider used (`--allow-mock`, or `engineering_only: true` in the session manifest) | **Void as science.** Codex's analyzer already refuses these without `--allow-mock-analysis`; that guard may not be passed for any run intended as evidence. |
| Any `PILOT_PROTOCOL_V2.md` §3.1 cross-session invariant fails | **The primary comparison is void.** Do not adjust for it; re-run both sessions under a corrected configuration. |

### 4.3 The loud-failure principle

A void run is a **result to be recorded**, not a setback to be worked around. Record it in `EXPERIMENT_LOG.md` with its cause, and re-run from a corrected freeze. Under no circumstances may a void or degraded run be silently retried until it produces analyzable-looking numbers — that converts a configuration failure into a selection effect on runs.

## 5. Recording

Committed before the main run:

- provider name and base URL;
- exact model identifier sent, and the identifier echoed back;
- whether the identifier is a pinned snapshot or an alias (and the resolved build, if exposed);
- `temperature`, `max_tokens`, `--timeout`;
- dry-run date, call count, parse-success count, any `finish_reason` values observed;
- the session-order coin flip (`PILOT_PROTOCOL_V2.md` §3.2).

During the run, `experiments/run_pilot.py` records provider, model, temperature, and max_tokens into the immutable `session_manifest.json`, and each raw payload carries `actual_provider` / `actual_model`. Those are the authoritative record; this document's purpose is to ensure the values written there are correct **before** 600 calls are spent.
