# Reproducibility

This file tracks how another researcher can recreate the engineering environment and, once experiments exist, reproduce their results. Scientific context and constraints are in `AGENTS.md` and `dossier/99_synthesis.md`.

## Environment

1. Clone the repository and switch to the experiment branch.
2. Use Python 3.11 when available; otherwise record the exact compatible Python version used.
3. Create an isolated environment with `python -m venv .venv`.
4. Activate it and install dependencies with `python -m pip install -r requirements.txt`.
5. Copy `.env.example` to `.env` only when a provider is needed, and keep all real credentials out of version control.

## Data and Protocol

Dataset manifests, acquisition provenance, checksums, exclusions, frozen prompts, and pattern priors must be recorded before confirmatory execution. Placeholders are not experimental evidence.

## Runs and Results

No experiment has been run. Exact commands, configuration hashes, software versions, seeds, raw-response locations, and generated result files will be added when the infrastructure and authorized inputs are available.

