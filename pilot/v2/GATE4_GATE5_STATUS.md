# Gate 4 / Gate 5 Gemini model-freeze status

**Final status: BLOCKED**

Latest attempt recorded 2026-09-10T19:00:32.057021+00:00 on `agent/codex-gate7`.
The user explicitly authorized one fresh registered smoke attempt with exactly
the same settings, and required another immediate stop on HTTP 503.

| Item | Result |
|---|---|
| Gate 4 | **BLOCK** — call 4 returned HTTP 503 / `UNAVAILABLE` |
| Gate 5 | **BLOCK** — no session-order coin flip |
| Provider | Google Gemini API via OpenAI-compatible endpoint (`google_gemini`) |
| API base URL | `https://generativelanguage.googleapis.com/v1beta/openai/` |
| Exact model requested | `gemini-3.8-flash` |
| Exact completion identity returned | `gemini-3.8-flash` on all 3 successful responses |
| Smoke calls attempted | 4 of the registered 12 |
| Successful smoke calls completed | 3 |
| Parser successes / failures | 3 / 0 |
| Provider failures | 1; HTTP 503 on call 4 |
| Accepted generation parameters | `temperature=0`, `max_tokens=1024`; exact model and frozen system/user messages |
| Timeout | 120 seconds, unchanged |
| Scientific repetitions | 5, unchanged; not used as the smoke repetition count |
| Frozen session order | None; zero coin flips |
| Scientific candidate calls | 0 |
| Full pilot | **NOT YET AUTHORIZED** |

## Fresh attempt and stop

The unchanged `experiments.model_preflight.run` procedure created the new session
`20260910T185841547998Z`. HTTP statuses were **200, 200, 200, 503**. Each successful
response was non-empty, valid structured JSON, passed the parser and nonzero-score
check, returned the exact requested model identifier, and ended with
`finish_reason=stop`. Call 4 returned Google's high-demand `UNAVAILABLE` error.
The registered procedure immediately aborted and wrote the session's `VOID.json`.

No automatic retry, model substitution, token-limit increase, parameter change,
prompt edit, prior edit, or dataset edit occurred. No new metadata calls or
scientific calls were made. The prior authenticated metadata/identity verification
remains linked in this attempt's start record. No localization accuracy was
computed or used to choose settings.

Before execution, the provider/settings dictionary was compared with the previous
VOID session and found identical. All smoke inputs, prompt/prior files, the
scientific manifest, both scientific configuration files, execution code, and
primary comparison code were checked against the previous attempt's Git commit.
Their SHA-256 hashes remain unchanged after execution.

Only the same four HTTP request fields were sent: `model`, `temperature`,
`max_tokens`, and `messages`. The observer recorded payloads and response bodies
without changing requests or retry behavior. No extra generation parameters were
added. Provider defaults and their evidence are retained in the
[earlier identity/settings record](model-freeze-attempts/20260910T184351Z-gemini-model-lookup/identity_verification.json);
no new claim is made that unexposed effective defaults were independently frozen.
A passing model/settings freeze still does not exist.

## Evidence

- [Attempt authorization, exact settings, and asset hashes](model-freeze-attempts/20260910T185841Z-gemini-smoke-retry/attempt_start.json).
- [Exact HTTP payloads and responses](model-freeze-attempts/20260910T185841Z-gemini-smoke-retry/smoke_http_exchanges.json).
- [Execution summary](model-freeze-attempts/20260910T185841Z-gemini-smoke-retry/smoke_execution_summary.json).
- [Machine-readable Gate 4/5 result](model-freeze-attempts/20260910T185841Z-gemini-smoke-retry/gate4_gate5_result.json).
- [New VOID smoke session](../../results/smoke-freeze/20260910T185841547998Z/): original raw/processed records, settings manifest, and VOID marker.
- [Experiment log](../../EXPERIMENT_LOG.md): all four calls and the aborted session.

The prior credential precheck and first VOID smoke attempt remain intact. The
credential was used only in process memory, supplied through the temporary
`LLM_API_KEY` process environment, and removed after execution. No authorization
header or credential was included in the retained evidence.

No `MODEL_FREEZE_RECORD.json` was created. Gate 5 remains unexecuted because
Gate 4 did not complete. A further smoke attempt requires a fresh instruction;
no retry or monitor was scheduled. Any future attempt must preserve both VOID
attempts and must not send a scientific candidate before a passing freeze is
committed and the full pilot is separately authorized.

The evidence commit is available with
`git log -1 --format=%H -- pilot/v2/GATE4_GATE5_STATUS.md`.
