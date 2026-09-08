# Pilot Engineering Runbook

This runbook describes the engineering interface only. It does not define the scientific protocol, prompt wording, pattern vocabulary, or prior content owned by other agents.

## Required frozen inputs

- A JSON or YAML manifest validated by `python -m experiments.validate_manifest MANIFEST`.
- A system-prompt text file from the scientific handoff.
- One shared user-template text file containing `{numbered_buggy_source}` and, optionally, `{program_id}`, `{task_id}`, and `{problem_context}`.
- A YAML prior map whose keys exactly match the manifest's final oracle labels.
- An explicit condition-order and parser-failure policy from the frozen protocol.

The treatment prompt is constructed mechanically from the exact control prompt plus one delimited prior block. No fixed source or faulty-line ground truth is accepted as a prompt-template field.

## Manifest shape

```yaml
manifest_version: 1
dataset_name: example-only
created_at: 2026-09-01T00:00:00Z
selection_frozen_at: 2026-09-02T00:00:00Z
programs:
  - program_id: unique-id
    task_id: source-task-id
    buggy_source_path: ../raw/example/buggy.py
    fixed_source_path: ../raw/example/fixed.py
    tests_path: ../raw/example/tests
    faulty_lines: [7]
    pattern_label: label-from-scientific-handoff
    pattern_source: annotation-record-id
    loc: 12
    difficulty: source-defined-level
    inclusion_status: included
    exclusion_reason: null
    exclusion_decided_at: null
    problem_context_path: ../raw/example/problem.txt
    evaluation_denominator: 12
```

`evaluation_denominator` is optional and defaults to `loc`. It exists so the frozen methodology can supply the exact number of inspectable statements without forcing the engineering layer to infer a scientific definition.

## Execution

```sh
.venv/bin/python -m experiments.run_pilot \
  --manifest data/manifests/pilot.yaml \
  --system-prompt pilot/prompts/system.txt \
  --user-template pilot/prompts/user_template.txt \
  --priors pilot/prompts/priors.yaml \
  --provider openai_compatible \
  --provider-label PROVIDER_NAME \
  --base-url PROVIDER_CHAT_API_BASE \
  --model MODEL_NAME \
  --temperature TEMPERATURE \
  --max-tokens MAX_TOKENS \
  --condition-order FROZEN_ORDER
```

Credentials are read only from `.env`/the process environment. Raw responses are immutable JSON files under `results/raw/`; parsed records are separate files under `results/processed/`. A duplicate execution key aborts the run unless `--resume` is used to skip records that already exist.

The `mock` provider is available only with `--allow-mock`. Its outputs are engineering fixtures and must never be used as scientific evidence. Analysis of a mock session additionally requires `--allow-mock-analysis` and watermarks every generated report.

## Analysis

```sh
.venv/bin/python -m analysis.run_analysis \
  --manifest data/manifests/pilot.yaml \
  --session-id SESSION_ID \
  --parser-failure-policy FROZEN_POLICY
```

This creates the required CSV, JSON, Markdown reports, adversarial audit, handoff, and four programmatic figures. The analyzer aborts on missing pairs, duplicate runs, setting mismatches, manifest mismatches, or missing raw-response files.
