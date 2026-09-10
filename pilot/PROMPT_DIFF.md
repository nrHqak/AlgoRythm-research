# Prompt Diff (FROZEN v1)

**Status:** Frozen by the Claude scientific-specification handoff, 2026-09-10.
**Purpose:** make the control-vs-treatment difference legible and auditable in one place, and record that Claude verified — by reading, not modifying — `experiments/prompts.py` and `experiments/safety.py` that the engineering layer mechanically enforces exactly this diff. Do not treat this document as a second implementation; the single source of truth for the mechanics is Codex's code.

## File → CLI-flag map

The frozen scientific-content files plug into `experiments/run_pilot.py` (per `docs/PILOT_RUNBOOK.md`) as follows:

| Frozen file | CLI flag | Role |
|---|---|---|
| `pilot/prompts/system.txt` | `--system-prompt` | System-role message, identical for both conditions. Added by this handoff — see `CLAUDE_HANDOFF.md` for why it exists alongside the two files this handoff was explicitly asked to produce. |
| `pilot/prompts/control.txt` | `--user-template` | The shared user-role template. Used **as-is** (after `.format()` substitution) for the `pattern_agnostic` condition; also the exact prefix of the `oracle_pattern_prior` condition's prompt. |
| `pilot/pattern_priors.json` | `--priors` | Per-pattern frozen prior strings. Valid as-is because JSON is a syntactic subset of YAML that `yaml.safe_load` (used by `experiments/run_pilot.py::load_prior_map`) parses correctly; no conversion step is required. If a literal `.yaml` copy is ever preferred for stylistic reasons, it must be byte-identical in content once parsed — do not hand-edit a second copy. |
| `pilot/config/pilot.yaml` | `--config` | Already frozen by Codex; conditions/metrics/statistics names referenced throughout this handoff are read from here, not re-declared. |

`pilot/prompts/pattern_prior.txt` is **not** a runtime input — it is the authoring template documented in `PATTERN_PRIORS.md`.

## The mechanical diff (as implemented in `experiments/prompts.py::build_prompt_pair`)

```
control_user_prompt   = control.txt.format(program_id=..., task_id=..., problem_context=..., numbered_buggy_source=...)
treatment_user_prompt = control_user_prompt.rstrip()
                         + "\n\n<ALGORITHMIC_PATTERN_PRIOR>\n"
                         + pattern_priors.json[program.pattern_label].strip()
                         + "\n</ALGORITHMIC_PATTERN_PRIOR>"
```

- **System prompt:** byte-identical for both conditions (same file, read once, passed to both). Verified at analysis time by `experiments/safety.py::assert_paired_settings` (`system_prompt_hash` must match within a program/repetition pair) and `assert_raw_prompt_symmetry` (re-derives the diff from the raw saved prompts and rejects any pair where it does not hold exactly).
- **User prompt:** identical for both conditions up to and including the exact text produced by `control.txt`; the treatment condition appends **only** the delimited `<ALGORITHMIC_PATTERN_PRIOR>...</ALGORITHMIC_PATTERN_PRIOR>` block, whose inner text is the frozen string for that program's `pattern_label` from `pattern_priors.json`. `experiments/prompts.py::assert_only_prior_differs` raises before any run is executed if this does not hold; `experiments/safety.py::assert_raw_prompt_symmetry` re-checks it after the fact from the immutable raw response files.
- **Delimiters** `<ALGORITHMIC_PATTERN_PRIOR>` / `</ALGORITHMIC_PATTERN_PRIOR>` are fixed constants in `experiments/prompts.py` (`PRIOR_OPEN`, `PRIOR_CLOSE`) — not a scientific choice, not reproduced by value here to avoid drift between two copies; see that file for the exact strings.

## Why `pattern_label` cannot appear as a template placeholder, but the prior text can name the pattern

`experiments/prompts.py::FORBIDDEN_TEMPLATE_FIELDS` bans `{pattern_label}` (and `{faulty_lines}`, `{fixed_source}`, `{fixed_source_path}`, `{ground_truth}`) as a substitution field inside `control.txt`. This guards the **shared template**: if `pattern_label` were a valid field, it would have to be filled identically for both conditions (the template is shared code), which would leak the pattern into the control condition too and destroy the `pattern_agnostic` arm's meaning.

This is unrelated to — and does not block — the treatment condition legitimately *naming* the pattern in prose inside its frozen prior string (e.g. "This program is intended to solve the task using two pointers..."). That text is not a template substitution; it is a static, pre-authored string looked up in Python from `pattern_priors.json` by `program.pattern_label` and inserted only into the treatment prompt, outside the template-formatting step entirely. Revealing the pattern is the treatment manipulation — the forbidden-fields list exists to stop it from leaking into the *shared* code path, not to stop it existing at all.

## What the diff does NOT touch

- `faulty_lines` (ground-truth fault location) never appears in either prompt; both `validate_user_template` and the forbidden-fields list block it structurally, independent of anything in this document.
- `fixed_source` / `fixed_source_path` (the reference solution) never appear in either prompt, for the same structural reason.
- Provider, model, temperature, max_tokens, and condition order are identical within a program/repetition pair by construction (`assert_paired_settings`), and are protocol parameters, not prompt content — see `PILOT_PROTOCOL.md`.

## Consistency check performed

Before committing, `pilot/prompts/control.txt` was exercised against the live `experiments.prompts.validate_user_template` and `experiments.prompts.build_prompt_pair` functions (not reimplemented) with a synthetic `ProgramRecord` and each of the 12 frozen priors, confirming: (a) the template validates, (b) `.format()` succeeds without a `KeyError` on the doubled braces in the JSON example, (c) `build_prompt_pair`'s own internal `assert_only_prior_differs` check passes for all 12 priors. See `CLAUDE_HANDOFF.md` for the exact commands run.
