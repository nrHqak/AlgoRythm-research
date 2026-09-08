# Decisions

Scientific decisions remain governed by `AGENTS.md` and `dossier/99_synthesis.md`. Add entries chronologically only when a decision and its evidence are available.

| date | decision | reason | evidence | agent |
|---|---|---|---|---|
| 2026-09-08 | Keep scientific prompt, prior, vocabulary, condition order, and parser-failure policy external and required at runtime | These choices belong to the frozen scientific protocol and must not be silently chosen by the engineering layer | Project brief; `docs/PILOT_RUNBOOK.md` | Codex |
| 2026-09-08 | Save each raw model response in an exclusive-create file before parsing | Preserves failures and prevents post-hoc reconstruction or overwrite | `experiments/run_pilot.py`; integration test | Codex |
| 2026-09-08 | Use per-repetition exact McNemar tests and program-clustered paired bootstrap intervals | Avoids treating stochastic repetitions of one program as independent experimental units | `dossier/05_block5_methodology.md`; `analysis/statistics.py` | Codex |
| 2026-09-08 | Make the EXAM denominator manifest-configurable, defaulting to `loc` | The frozen protocol may define inspectable statements more precisely than the engineering layer can infer | `dossier/05_block5_methodology.md`; `experiments/models.py` | Codex |
