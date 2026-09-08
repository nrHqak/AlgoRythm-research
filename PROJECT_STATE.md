# Current Research Question

See `AGENTS.md` and `dossier/99_synthesis.md`. No additional wording is frozen here yet.

# Frozen Decisions

- No pattern vocabulary, prompt wording, pattern prior, annotation rule, condition order, or parser-failure policy has been frozen by Codex.
- Confirmatory execution requires the responsible scientific handoff files and a pre-treatment-frozen data manifest.

# Current Stage

Pilot infrastructure ready; scientific inputs and acquired candidate data are pending.

# Completed

- Repository and dossier context reviewed as required by `AGENTS.md`.
- Initial pilot directory structure and environment scaffold created.
- Validated manifest schema, provider abstraction, paired runner, immutable raw-response storage, structured parser, safety gates, evaluation, statistics, reports, audit, and figures implemented.
- Unit and full mock-pipeline tests pass. Mock outputs are engineering-only and were generated in temporary test storage.

# In Progress

No scientific experiment is running.

# Blocked

- Frozen scientific prompt and pattern-prior handoff has not been provided.
- Dataset acquisition, candidate discovery, and reproducibility verification remain with Antigravity; no pilot manifest is present.
- No provider/model credentials or exact model selection were supplied, so no scientific LLM calls were made.

# Next Actions

1. Receive and review Claude's frozen scientific handoff.
2. Receive Antigravity's candidate manifest and validate it with `python -m experiments.validate_manifest`.
3. Record the approved condition order and parser-failure policy.
4. Execute a complete pilot session, then generate and review the reports and adversarial audit.

# Latest Experimental Results

No scientific experiment has been run. Temporary mock-provider integration checks are not research evidence.

# Known Risks

See `dossier/99_synthesis.md`, especially section S5. The engineering audit additionally flags differential parser failures, prompt-length confounding, missing/duplicate pairs, setting mismatches, and post-freeze exclusions.

# Agent Handoffs

- Claude handoff: pending.
- Antigravity manifest/data handoff: pending.
- Codex engineering handoff: see `docs/PILOT_RUNBOOK.md`; no result handoff exists until a real pilot is run.
