# Reproducibility

This file tracks how another researcher can recreate the engineering environment and, once experiments exist, reproduce their results. Scientific context and constraints are in `AGENTS.md` and `dossier/99_synthesis.md`.

## Environment

1. Clone the repository and switch to the experiment branch.
2. Use Python 3.11 when available; this setup was verified with Python 3.14.3 because 3.11 was unavailable on the host.
3. Create an isolated environment with `python -m venv .venv`.
4. Activate it and install dependencies with `python -m pip install -r requirements.txt`.
5. Copy `.env.example` to `.env` only when a provider is needed, and keep all real credentials out of version control.

Verify the environment with:

```sh
.venv/bin/python -m pytest
.venv/bin/python -m compileall -q experiments analysis tests
```

Direct dependencies are pinned in `requirements.txt`. Capture `python --version` and `python -m pip freeze` with every real session so transitive dependencies are also preserved.

## Data and Protocol

Dataset manifests, acquisition provenance, checksums, exclusions, frozen prompts, and pattern priors must be recorded before confirmatory execution. Placeholders are not experimental evidence.

## Runs and Results

No scientific experiment has been run. Follow `docs/PILOT_RUNBOOK.md` after the frozen prompt/prior handoff and validated data manifest arrive. The runner stores an immutable session manifest containing input hashes and a credential-free reproduction command; the analyzer records its own command in `results/pilot_metrics.json` and `results/CODEX_HANDOFF.md`.

