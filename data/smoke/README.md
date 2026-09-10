# SMOKE DATA — NEVER SCIENTIFIC DATA

Three original, hand-written Python bugs created for the v2 engineering preflight.
No ConDefects program, candidate frame, or scientific sample was used. These IDs
and files are permanently ineligible for any scientific dataset.

`manifest.json` is runner-compatible smoke metadata. `faulty_lines` describes
known defects solely to exercise storage/parsing; smoke accuracy is never used
for model selection or prior tuning. Fixed sources and JSON function test cases
allow offline fixture verification. All three buggy functions are runnable.

Use `python -m experiments.model_preflight --help` for the provider check.
The check makes 12 calls: three programs × two prompt shapes × two prior files
(six no-block, three generic, three pattern). Outputs are engineering-only.
No scientific sampling thresholds apply to these deliberately tiny fixtures.
