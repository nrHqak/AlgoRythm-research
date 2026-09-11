# Provider-response persistence fix

The first scientific request exposed an evidence-ordering defect. The OpenAI
compatible adapter validated `choices[0].message.content` and raised on `null`
before `run_one` could write the provider response. The processed failure survived,
but the generation ID, finish reason, usage, reasoning tokens, and reasoning body
did not.

The adapter now returns received JSON responses without validating the content
type. `run_one` writes the following evidence before any content or parser check:

- the complete provider response JSON;
- HTTP status;
- usage object;
- finish and native finish reasons;
- content type and reasoning-presence metadata;
- requested system/user prompts and the existing provenance hashes.

Only after that write does `run_one` classify null/non-string content as
`provider_failure/MissingCompletionContent`. Model and underlying-provider checks,
session health thresholds, prompts, priors, model settings, and statistical code
are unchanged.

Request headers are never persisted. The response JSON is copied through a
credential scrubber that removes an exact API-key echo and values under standard
credential keys. Tests prove that a complete synthetic null-content response,
including reasoning and usage, is saved before validation and that an echoed
credential is absent from the artifact.
