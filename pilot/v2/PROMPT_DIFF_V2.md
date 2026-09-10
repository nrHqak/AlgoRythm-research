# Prompt Diff v2 (FROZEN)

**Status:** frozen 2026-09-10. Supersedes `pilot/PROMPT_DIFF.md` (v1, preserved unmodified) for execution.
**Purpose:** state exactly what differs between the three arms, and record that the differences were verified by executing Codex's live code — not by reimplementing or restating it.

## 1. File → CLI-flag map

| Frozen file | CLI flag | Session | Role |
|---|---|---|---|
| `pilot/v2/prompts/system_v2.txt` | `--system-prompt` | **both** | System-role message, byte-identical across all three arms and both sessions |
| `pilot/prompts/control.txt` (v1, unchanged) | `--user-template` | **both** | Shared user-role template; used as-is for arm A and as the exact prefix of arms B and C |
| `pilot/v2/generic_placebo_prior.json` | `--priors` | G only | Generic/placebo block text (arm B) |
| `pilot/pattern_priors.json` (v1, unchanged) | `--priors` | P only | Pattern-specific block text (arm C) |
| `pilot/v2/config/pilot_v2_generic.yaml` | `--config` | G only | Arms A_G vs B |
| `pilot/v2/config/pilot_v2_pattern.yaml` | `--config` | P only | Arms A_P vs C |

`pilot/prompts/pattern_prior.txt` and `pilot/prompts/system.txt` are v1 artifacts, retained for history; **`system.txt` is not used in v2** (replaced by `system_v2.txt`, see §3).

## 2. The three prompts

Built by `experiments/prompts.py::build_prompt_pair`, unmodified:

```
shared    = control.txt.format(program_id=..., task_id=..., problem_context=..., numbered_buggy_source=...)

arm A     = shared
arm B     = shared.rstrip() + "\n\n<ALGORITHMIC_PATTERN_PRIOR>\n" + generic_placebo_prior.json[label].strip()  + "\n</ALGORITHMIC_PATTERN_PRIOR>"
arm C     = shared.rstrip() + "\n\n<ALGORITHMIC_PATTERN_PRIOR>\n" + pattern_priors.json[label].strip()         + "\n</ALGORITHMIC_PATTERN_PRIOR>"
```

- **A vs B** and **A vs C** differ by exactly one delimited block. Enforced pre-run by `assert_only_prior_differs` and re-verified post-run by `experiments/safety.py::assert_raw_prompt_symmetry` against the immutable raw files.
- **B vs C** — the primary comparison — differ **only in the text inside the block.** Everything outside the delimiters is byte-identical: same system prompt, same rendered user template (same per-program `shared_prompt_hash`), same delimiters, same position in the message, same model settings. The block itself is matched on format, checkpoint count, tone, and length within a declared tolerance (`GENERIC_PLACEBO_PRIOR.md` §4).

Note that Codex's built-in symmetry checks operate **within** a session, so they verify A-vs-B in session G and A-vs-C in session P. The B-vs-C invariants are cross-session and must be asserted separately — the required assertions are listed in `PILOT_PROTOCOL_V2.md` §3.1 and `STATISTICAL_ANALYSIS_PLAN.md` §6.

## 3. Why the system prompt changed in v2

The v1 system prompt (`pilot/prompts/system.txt`) ended with:

> "If the user message includes a delimited block that **names the program's intended algorithmic pattern**, treat it as a hint about where to look first…"

Under v1's two-arm design this was merely inelegant. Under v2 it would be **fatal to the primary comparison**: the sentence accurately describes arm C's block and inaccurately describes arm B's, so the two arms would be framed differently by the shared system prompt — an uncontrolled B/C difference outside the delimited block, defeating the entire point of the placebo. v2 therefore describes the block neutrally:

> "If the user message includes a **delimited block of debugging guidance**, treat it as a hint about where to look first…"

A second, smaller change: v1's reviewer framing listed "loop bounds, comparison directions, **pointer or index updates, base cases**, and the order in which state is updated." Two of those terms (`pointer`, `base case`) are vocabulary-class-specific and were handing a small amount of pattern-specific information to every arm for free, including arm B. v2 narrows this to "loop bounds, comparison directions, index updates, initialization, and the order in which state is updated." The framing's scientific motivation (the CPH-inversion argument, `dossier/01_block1_theory.md` §1c) is preserved; the two leak-prone terms are not.

Both changes are pre-results, apply identically to all three arms, and are recorded in `CHANGELOG_V1_TO_V2.md`.

## 4. Disclosed residual asymmetries

1. **The delimiter tag is `<ALGORITHMIC_PATTERN_PRIOR>` in all arms**, including arm B, where it wraps generic content. The tag name is semantically apt for C and mildly incongruent for B. It is *identical* in both arms, so it is matched — but a model that reads the tag as a promise of pattern information may treat B's contents differently than it would under a neutral tag. The tag cannot be changed without editing `PRIOR_OPEN`/`PRIOR_CLOSE` in `experiments/prompts.py`, which this protocol does not do. Recorded as a known limitation; if a future version is permitted to touch Codex's constants, a neutral tag such as `<DEBUGGING_PRIOR>` would remove it.
2. **Arm A is not zero-guidance** — the shared system prompt contains generic reviewer framing (§3). Affects A vs B and A vs C only; C vs B is unaffected because the framing is identical on both sides.
3. **Ranking length is a free parameter.** `control.txt` instructs "List only lines you have a genuine reason to suspect," so response length varies by model and possibly by arm; longer rankings mechanically raise Top-3/Top-5 hit rates and reduce EXAM censoring. v1's review (N5) raised this. v2 deliberately does **not** fix the ranking length, for two reasons: (a) the primary comparison is inherently balanced, since B and C both present a numbered checklist of 4–5 items and should induce similar response lengths; (b) forcing a fixed length would degrade EXAM into a near-degenerate censored statistic and would change the task relative to the cited baselines. Instead, **mean ranking length per arm is a mandatory reported diagnostic** (`PILOT_PROTOCOL_V2.md` §5, `STATISTICAL_ANALYSIS_PLAN.md` §5): if B and C differ materially in ranking length, the Top-K comparison between them is mediated and must be reported as such.

## 5. What the diff never touches

- `faulty_lines` appears in no prompt in any arm — structurally blocked by `FORBIDDEN_TEMPLATE_FIELDS` and `validate_user_template`, independent of this document.
- `fixed_source` / `fixed_source_path` appear in no prompt in any arm, same mechanism.
- `{pattern_label}` cannot be a template field (it would leak the label into arm A and arm B via the shared template). The pattern name legitimately appears in arm C's *block text*, which is looked up in Python outside the template-formatting step — that is the manipulation, and it is confined to arm C.

## 6. Consistency check performed

Before committing, both priors files were exercised against the live `experiments.prompts.validate_user_template` and `experiments.prompts.build_prompt_pair` with a synthetic `ProgramRecord`, for all 12 labels × both priors files (24 prompt pairs), confirming: the template validates; `.format()` succeeds; `build_prompt_pair`'s internal `assert_only_prior_differs` raises nothing; and, for each label, the arm-B and arm-C prompts are byte-identical outside the delimited block. Both configs were parsed and checked against the runner's own validation rules. Exact commands and results are recorded in `CHANGELOG_V1_TO_V2.md` §5.
