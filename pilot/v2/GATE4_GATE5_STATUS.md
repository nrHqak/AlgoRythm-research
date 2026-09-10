# Gate 4 / Gate 5 Gemini model-freeze status

**Final status: BLOCKED**

Recorded 2026-09-10T18:48:33.298695+00:00 on `agent/codex-gate7`.
This replaces the earlier credential-precheck status; that attempt's evidence
remains in `model-freeze-attempts/20260910T183315Z-gemini-credential-precheck/`.

| Item | Result |
|---|---|
| Gate 4 | **BLOCK** — second smoke call returned HTTP 503 / `UNAVAILABLE` |
| Gate 5 | **BLOCK** — Gate 4 did not pass; no coin flip |
| Provider | Google Gemini API via OpenAI-compatible endpoint (`google_gemini`) |
| API base URL | `https://generativelanguage.googleapis.com/v1beta/openai/` |
| Exact model ID requested | `gemini-3.8-flash` |
| Model identity returned by metadata API | `models/gemini-3.8-flash` |
| Model identity returned by completion API | `gemini-3.8-flash` — exact match |
| Native metadata version field | `3.0` — recorded literally, not an immutable build digest |
| Authenticated model metadata requests | 2; both HTTP 200 |
| Smoke calls attempted / HTTP responses | 2 / 2 |
| Successful smoke calls completed | 1 of the required 12 |
| Parser successes / failures | 1 / 0 |
| Provider failures | 1; HTTP 503 on call 2 |
| Accepted generation parameters on call 1 | `model=gemini-3.8-flash`, `temperature=0`, `max_tokens=1024`, system/user messages |
| Timeout | 120 seconds, unchanged |
| Scientific repetitions | 5, unchanged; not applied to the smoke procedure |
| Frozen session order | None; zero coin flips |
| Scientific candidate calls | 0 |
| Full pilot | **NOT YET AUTHORIZED** |

## Identity verification before smoke

The exact OpenAI-compatible model retrieval endpoint returned HTTP 200 with ID
`models/gemini-3.8-flash`, owned by Google. The initial literal comparison against
the bare generation ID marked the lookup BLOCK. Before any generation call, the
[provider resource-name documentation](https://ai.google.dev/api/models) and an
additional native metadata retrieval established that `models/` is the resource
namespace. The native response names the same exact model and includes
`generateContent` in supported methods. The initial observation is retained,
with this metadata-only review recorded separately in `identity_verification.json`.

The [specific model page](https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash)
identifies the requested code as stable, and the
[version naming guide](https://ai.google.dev/gemini-api/docs/models#model-version-name-patterns)
distinguishes a specific stable release from a moving latest alias. The API
exposes no immutable weight/build digest. No alternative identifier was selected.
The frozen **completion** identity check was not relaxed or normalized: the first
smoke response echoed `gemini-3.8-flash` exactly and passed that check.

## Registered smoke outcome

Executed the existing `experiments.model_preflight.run` procedure using only
`data/smoke/manifest.json`, the committed smoke fixtures, frozen prompts, and
frozen prior files. The planned procedure is 12 calls (6 without a prior,
3 generic-placebo, 3 pattern-prior), with no selection based on fault-localization
accuracy. No scientific candidate or sampling-frame source was sent.

1. `smoke-sum`, no prior: HTTP 200, exact model echo, non-empty valid structured
   JSON, parser success, nonzero suspicion scores, and `finish_reason=stop`.
2. `smoke-sum`, generic prior: HTTP 503. Google returned `UNAVAILABLE` and reported
   high demand. The procedure immediately aborted and wrote `VOID.json`.

This is a provider availability failure, not a parser failure, model-identity
failure, or observed parameter rejection. There was no retry, model change,
parameter change, prompt change, or prior tuning. In particular, no larger token
limit or alternative reasoning setting was tried. Neither a passing
`MODEL_FREEZE_RECORD.json` nor a session-order coin flip exists.

## Generation and transport settings

The existing HTTP adapter sends exactly `model`, `temperature`, `max_tokens`, and
system/user `messages`. Those fields were accepted on call 1. It sends no explicit
`top_p`, `top_k`, `reasoning_effort`, `thinking_config`, `response_format`, `seed`,
`stop`, tools, or streaming setting. Structured JSON is required by the frozen
prompt and validated by the existing parser; no new JSON-mode parameter was added.

Native metadata reports default `topP=0.95`, `topK=64`, and `temperature=1`;
the request explicitly overrides temperature to zero. Google's
[model guide](https://ai.google.dev/gemini-api/docs/latest-model) documents default
thinking level `medium`, and its
[compatibility guide](https://ai.google.dev/gemini-api/docs/openai) says an omitted
reasoning setting uses the model default. These are provider-reported/documented
defaults, not values echoed in the completion response. They are recorded without
claiming a completed freeze of all effective generation parameters. Gate 4 must
pass before a model/settings freeze can be certified.

## Evidence and credential handling

- [Machine-readable gate result](model-freeze-attempts/20260910T184351Z-gemini-model-lookup/gate4_gate5_result.json).
- [Compatibility model retrieval](model-freeze-attempts/20260910T184351Z-gemini-model-lookup/model_lookup.json).
- [Native model metadata](model-freeze-attempts/20260910T184351Z-gemini-model-lookup/native_model_metadata.json).
- [Identity review and intended settings](model-freeze-attempts/20260910T184351Z-gemini-model-lookup/identity_verification.json).
- [Exact smoke HTTP payloads/responses](model-freeze-attempts/20260910T184351Z-gemini-model-lookup/smoke_http_exchanges.json), including the failed response body.
- [Execution summary](model-freeze-attempts/20260910T184351Z-gemini-model-lookup/smoke_execution_summary.json).
- [Smoke session](../../results/smoke-freeze/20260910T184609524153Z/): original raw/processed records, settings manifest, and VOID marker.
- [Experiment log](../../EXPERIMENT_LOG.md): both calls and the aborted smoke session.

The user-supplied credential was read from this task's existing user message
straight into process memory and supplied through `LLM_API_KEY` for the registered
procedure. It was not included in command text, printed, or copied to a repository
file. The temporary process environment entry was removed after the attempt.
The observer retained request JSON and response bodies without authorization
headers and did not alter HTTP arguments, returned responses, or retry behavior.
No frozen execution or scientific code was modified.

To resume, request a **fresh registered smoke attempt with the same settings**
after provider availability recovers. Preserve this VOID attempt and use a new
attempt/session path. Passing model and session-order evidence must be committed
before any separately authorized full pilot. A change of provider, model, or
parameters requires a documented decision; none was made here.

The exact evidence commit is available with
`git log -1 --format=%H -- pilot/v2/GATE4_GATE5_STATUS.md`.
