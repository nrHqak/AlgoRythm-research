# Proposed non-candidate stress smoke

**Status:** proposed, not created or executed. No scientific candidate may be
used for this step.

The existing smoke programs contain 5-11 source lines and produced 637-870 input
tokens. The frozen scientific sample spans 25-155 physical lines. Offline prompt
construction gives a maximum of 8,310 characters for arm B and 8,248 for arm C;
the 90th percentiles are approximately 5,484 and 5,455 characters.

Create one wholly synthetic `dynamic_programming` fixture outside the scientific
sampling frame with these properties:

- 150-160 physical source lines, targeting 155;
- enough independent helpers, nested state transitions, boundary handling, and
  initialization to produce 8,500-9,000 total system-plus-user prompt characters;
- one planted single-line logical fault, at least one passing and one failing
  test in the buggy version, and all tests passing in the fixed version;
- a permanent `SMOKE DATA — NEVER SCIENTIFIC DATA` marker and a program/task ID
  that cannot collide with ConDefects IDs;
- no copied candidate source, problem statement, fault line, or model response.

After an explicit max-token amendment, run exactly 20 stress calls: five frozen
repetitions for each of A_G, B, A_P, and C, in frozen G-then-P session order.
Use the unchanged model, Z.AI pin, disabled fallbacks, temperature, prompts, and
prior files. This mirrors the real arm structure while testing the longest
prompt class and stochastic reasoning tail.

Acceptance is mechanical only: 20/20 HTTP responses retained in full before
content validation; exact model and Z.AI identity; no fallback; non-null,
non-empty final content; `finish_reason=stop`; valid structured JSON; parser
success; and no all-zero provider failure. Record input, completion, and reasoning
tokens on every call. Do not inspect localization accuracy or tune the fixture,
prompt, or prior from model performance.
