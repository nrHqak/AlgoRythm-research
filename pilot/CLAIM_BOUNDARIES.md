# Claim Boundaries (FROZEN v1) — what this pilot can and cannot support

**Status:** written 2026-09-10, before any pilot data exists — a deliberate pre-commitment, not a post-hoc rationalization. Use this document, together with `CLAIMS.md`'s Supported/Preliminary/Unsupported register, whenever a pilot result is about to be written into `RESEARCH_DOSSIER.md`, an РКНП/ISEF submission draft, or any other external-facing text. If a draft claim is not explicitly licensed below, it does not go in without a documented reason added to this file first.

## May be claimed once the pilot has run (engineering/process claims)

- The frozen prompt/prior pipeline (`experiments/prompts.py`, `experiments/run_pilot.py`, `analysis/run_analysis.py`) executed end-to-end on real ConDefects-Python data without a `SafetyViolation` abort, OR: it aborted, and why (a legitimate and useful pilot outcome).
- The observed parser-failure rate per condition, as a measured engineering fact about this model's behavior on this prompt design.
- The observed discordant-pair count/rate, reported as an input to the confirmatory study's sample-size calculation — e.g. "this pilot's discordance rate suggests n≈X for adequate McNemar power at α=0.05," replacing the dossier's own ⚠️-flagged rough estimate with a data-informed one.
- The observed prompt-length gap between conditions, compared against the length-confound audit predicted in `PATTERN_PRIORS.md`.
- Qualitative observations from the manual spot-check in `PILOT_PROTOCOL.md` §5.5 (e.g. "no fault-location leakage was observed in N inspected treatment transcripts").

## May be claimed only with the stated qualifiers attached, every time, not once in a footnote

- Any Top-1/3/5 or EXAM delta between `pattern_agnostic` and `oracle_pattern_prior` must be stated with: (a) n=30, (b) single provider/model (name it), (c) oracle labels only, (d) ConDefects-Python only, (e) "not statistically decisive at this sample size" if that is what the McNemar/bootstrap result shows (per `SCIENTIFIC_RISKS.md` §1, it almost certainly will not reach decisive power at n=30). A bare sentence like "the pattern prior improved Top-1 accuracy by X points" with no qualifiers is a claim boundary violation regardless of what the number is.

## May NOT be claimed from this pilot, under any result

- That the pattern-prior hypothesis is **confirmed** or **refuted** (`PRE_EXPERIMENT_COMMIT.md` rule 4). n=30 is a calibration sample, not a confirmatory one — this is true independent of whether the observed p-value happens to look small.
- That results generalize beyond ConDefects-Python (no Java, no Codeflaws, no BugT, no AlgoRythm-sandbox data in this pilot — `PILOT_PROTOCOL.md` §3).
- That results generalize beyond oracle (gold) pattern labels to a realistic, classifier-predicted pipeline (`SCIENTIFIC_RISKS.md` §3) — the pilot cannot bound classifier-error propagation because there is no classifier in this pilot's loop.
- That results generalize beyond the single provider/model used to run it (`SCIENTIFIC_RISKS.md` §4) — no claim of the form "LLM-based localization" without naming the specific model, and no claim that a different model (e.g. a different reasoning-model family) would show the same pattern.
- Any comparison against SBFL, MBFL, or the prior-reweighted-spectrum arm — those arms are not implemented or run in this pilot (`PILOT_PROTOCOL.md` §1). A sentence like "our method beats spectrum-based localization" cannot be supported by this pilot under any circumstance.
- Any claim about cost-effectiveness or latency advantage of the prior — this pilot was not designed to isolate cost as an outcome (though `prompt_tokens_estimate`/`latency` are recorded and could be reported descriptively per program, with the same n=30/single-model qualifiers).
- Any claim that pattern labeling itself is reliable at scale — `ANNOTATION_GUIDE.md` §4 explicitly does not compute κ at pilot scale; do not cite pilot-stage labels as evidence of annotation quality.
- Any claim in the ISEF abstract, research plan, or poster that credits generative AI with the pilot's *scientific* conclusions, beyond disclosed engineering assistance — `dossier/08_block8_competition.md` (via `AGENTS.md` §3.2 item 7) records that ISEF forbids generative AI for authoring the research plan/abstract/poster/citations; this pilot's protocol and priors are themselves AI-authored engineering/scientific-specification artifacts and that authorship must be disclosed accurately wherever ISEF rules require it, not folded silently into "the research."

## How to escalate a claim from Preliminary to Supported

Follow `CLAIMS.md`'s existing instruction to move claims between sections "only with documented evidence," per `AGENTS.md`'s verification-label discipline. For anything on the "may not be claimed" list above, the escalation path is never "the pilot happened to show a strong effect" — it is running the confirmatory study (`dossier/99_synthesis.md` §S3–S4) at the frozen target n, with the realistic-label condition included, and only then updating this document itself (as a new version, with a changelog entry) to reflect what the larger study licenses.
