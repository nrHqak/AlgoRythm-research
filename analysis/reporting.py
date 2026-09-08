from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
from matplotlib import pyplot as plt  # noqa: E402

from experiments.storage import write_json_atomic


def write_text_atomic(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(content.rstrip() + "\n", encoding="utf-8")
    temporary.replace(path)


def make_figures(
    frame: pd.DataFrame,
    metrics: dict[str, Any],
    output_dir: Path,
    control_name: str,
    treatment_name: str,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    conditions = [control_name, treatment_name]

    topk = frame.groupby("condition")[["top1", "top3", "top5"]].agg(["sum", "count"])
    x = np.arange(3)
    width = 0.36
    fig, ax = plt.subplots(figsize=(8, 5))
    for offset, condition in zip((-width / 2, width / 2), conditions, strict=True):
        rates = [topk.loc[condition, (metric, "sum")] / topk.loc[condition, (metric, "count")] for metric in ("top1", "top3", "top5")]
        bars = ax.bar(x + offset, rates, width, label=condition)
        for bar, metric in zip(bars, ("top1", "top3", "top5"), strict=True):
            hits = int(topk.loc[condition, (metric, "sum")])
            total = int(topk.loc[condition, (metric, "count")])
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f"{hits}/{total}", ha="center", va="bottom", fontsize=8)
    ax.set_xticks(x, ["Top-1", "Top-3", "Top-5"])
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("Hit rate")
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_dir / "control_vs_prior_topk.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7, 5))
    data = [frame.loc[frame.condition == condition, "exam"].to_numpy() for condition in conditions]
    ax.boxplot(data, tick_labels=conditions, showmeans=True)
    ax.set_ylabel("EXAM (lower is better)")
    fig.tight_layout()
    fig.savefig(output_dir / "exam_score.png", dpi=180)
    plt.close(fig)

    pattern = frame.groupby(["pattern_label", "condition"])["top1"].mean().unstack()
    pattern["delta"] = pattern[treatment_name] - pattern[control_name]
    pattern = pattern.sort_values("delta")
    fig, ax = plt.subplots(figsize=(9, max(4, len(pattern) * 0.45)))
    colors = ["#b94a48" if value < 0 else "#3c8d5a" for value in pattern["delta"]]
    ax.barh(pattern.index, pattern["delta"], color=colors)
    ax.axvline(0, color="black", linewidth=0.8)
    ax.set_xlabel("Top-1 treatment − control")
    fig.tight_layout()
    fig.savefig(output_dir / "per_pattern_delta.png", dpi=180)
    plt.close(fig)

    transition = metrics["topk"]["top1"]["pooled_transitions"]
    matrix = np.array(
        [
            [transition["both_miss"], transition["treatment_only"]],
            [transition["control_only"], transition["both_hit"]],
        ]
    )
    fig, ax = plt.subplots(figsize=(5.5, 5))
    image = ax.imshow(matrix, cmap="Blues")
    for row in range(2):
        for column in range(2):
            ax.text(column, row, str(matrix[row, column]), ha="center", va="center")
    ax.set_xticks([0, 1], ["Treatment miss", "Treatment hit"])
    ax.set_yticks([0, 1], ["Control miss", "Control hit"])
    fig.colorbar(image, ax=ax, shrink=0.8)
    fig.tight_layout()
    fig.savefig(output_dir / "pairwise_transitions.png", dpi=180)
    plt.close(fig)


def strongest_claim(metrics: dict[str, Any]) -> str:
    top1 = metrics["topk"]["top1"]
    lower, upper = top1["bootstrap"]["percentile_95_ci"]
    delta = top1["bootstrap"]["mean_delta"]
    if lower > 0:
        return (
            "Within this exact pilot sample, model, settings, and repetition protocol, "
            f"the treatment increased mean Top-1 hit rate by {delta:.3f}; the paired "
            f"program-clustered 95% bootstrap interval was [{lower:.3f}, {upper:.3f}]."
        )
    if upper < 0:
        return (
            "Within this exact pilot configuration, treatment Top-1 performance was lower "
            f"by {abs(delta):.3f} on average; the 95% bootstrap interval excluded zero."
        )
    return (
        "This pilot does not establish a reliable Top-1 improvement: the mean paired delta "
        f"was {delta:.3f} and its 95% bootstrap interval [{lower:.3f}, {upper:.3f}] included zero."
    )


def render_results_markdown(metrics: dict[str, Any]) -> str:
    evidence_warning = (
        "> **Engineering-only mock output. This is not scientific evidence.**"
        if metrics.get("engineering_only")
        else "> Generated from immutable run records. Percentages are always accompanied by raw counts."
    )
    lines = [
        "# Pilot Results",
        "",
        evidence_warning,
        "",
        f"Exact programs: **{metrics['n_programs']}**; repetitions: **{metrics['repetitions']}**; "
        f"run records: **{metrics['n_run_records']}**.",
        "",
        "## Top-K",
        "",
        "| metric | condition | hits | total | rate |",
        "|---|---|---:|---:|---:|",
    ]
    for metric in ("top1", "top3", "top5"):
        for condition, values in metrics["topk"][metric]["conditions"].items():
            lines.append(
                f"| {metric} | {condition} | {values['hits']} | {values['total']} | {values['rate']:.4f} |"
            )
    lines.extend(
        [
            "",
            "| metric | paired mean delta | clustered bootstrap 95% CI |",
            "|---|---:|---:|",
        ]
    )
    for metric in ("top1", "top3", "top5"):
        bootstrap = metrics["topk"][metric]["bootstrap"]
        lower, upper = bootstrap["percentile_95_ci"]
        lines.append(
            f"| {metric} | {bootstrap['mean_delta']:.4f} | [{lower:.4f}, {upper:.4f}] |"
        )
    lines.extend(
        [
            "",
            "| metric | repetition | control-only | treatment-only | exact two-sided p | adjusted OR |",
            "|---|---:|---:|---:|---:|---:|",
        ]
    )
    for metric in ("top1", "top3", "top5"):
        for test in metrics["topk"][metric]["per_repetition_exact_mcnemar"]:
            lines.append(
                f"| {metric} | {test['repetition']} | "
                f"{test['control_hit_treatment_miss']} | {test['control_miss_treatment_hit']} | "
                f"{test['exact_two_sided_p']:.6g} | {test['haldane_anscombe_odds_ratio']:.4f} |"
            )
    lines.extend(
        [
            "",
            "McNemar tests are reported separately for each repetition to avoid treating stochastic "
            "repetitions of one program as independent programs. Bootstrap intervals resample programs "
            "and retain repetitions within each resampled cluster.",
            "",
            "## EXAM",
            "",
            f"Control mean: {metrics['exam']['control_mean']:.4f}; treatment mean: "
            f"{metrics['exam']['treatment_mean']:.4f}; treatment minus control: "
            f"{metrics['exam']['mean_difference_treatment_minus_control']:.4f}.",
            "",
            "## Failures and exclusions",
            "",
            f"Parser failures: **{metrics['safety']['parser_failures']}**; provider failures: "
            f"**{metrics['safety']['provider_failures']}**; pre-treatment exclusions: "
            f"**{metrics['exclusions']['count']}**.",
            "",
            "## Strongest justified claim",
            "",
            strongest_claim(metrics),
            "",
            "## Scope limits",
            "",
            "These results do not by themselves establish generalization to other datasets, pattern "
            "vocabularies, providers, models, temperatures, prompts, or predicted (non-oracle) labels.",
        ]
    )
    return "\n".join(lines)


def render_adversarial_audit(metrics: dict[str, Any]) -> str:
    adv = metrics["adversarial"]
    warning = (
        "> **Engineering-only mock output. This is not scientific evidence.**"
        if metrics.get("engineering_only")
        else "> The purpose of this audit is to look for explanations that weaken an apparent treatment gain."
    )
    return "\n".join(
        [
            "# Adversarial Audit",
            "",
            warning,
            "",
            "## Pattern concentration",
            "",
            json.dumps(
                {
                    "rate_deltas": adv["per_pattern_top1_delta"],
                    "net_hits": adv["per_pattern_top1_net_hits"],
                    "dominant_positive_pattern": adv["dominant_positive_pattern"],
                    "dominant_positive_pattern_share": adv["dominant_positive_pattern_share"],
                },
                indent=2,
                ensure_ascii=False,
            ),
            "",
            "## Program influence",
            "",
            json.dumps(adv["leave_one_program_out_top1"], indent=2, ensure_ascii=False),
            "",
            "## Repetition dependence",
            "",
            json.dumps(adv["per_repetition_top1_delta"], indent=2, ensure_ascii=False),
            "",
            "## Parser failures",
            "",
            json.dumps(adv["parser_failures_by_condition"], indent=2, ensure_ascii=False),
            "",
            "## Prompt-length confound",
            "",
            json.dumps(adv["prompt_length_by_condition"], indent=2, ensure_ascii=False),
            "",
            "The treatment is necessarily longer because it contains the prior. A token-matched placebo "
            "arm is required to separate prior content from prompt-length effects; this two-arm pilot cannot.",
            "",
            "## Reasonable statistical alternatives",
            "",
            json.dumps(adv["complete_case_sensitivity"], indent=2, ensure_ascii=False),
            "",
            "## Audit verdict",
            "",
            strongest_claim(metrics),
        ]
    )


def render_handoff(metrics: dict[str, Any], reproduce_command: str) -> str:
    programs = "\n".join(f"- `{program}`" for program in metrics["program_ids"])
    settings = metrics["settings"]
    topk_lines = [
        "| metric | condition | hits / total | rate | bootstrap treatment-control 95% CI |",
        "|---|---|---:|---:|---:|",
    ]
    for metric in ("top1", "top3", "top5"):
        ci = metrics["topk"][metric]["bootstrap"]["percentile_95_ci"]
        for condition, values in metrics["topk"][metric]["conditions"].items():
            topk_lines.append(
                f"| {metric} | {condition} | {values['hits']} / {values['total']} | "
                f"{values['rate']:.4f} | [{ci[0]:.4f}, {ci[1]:.4f}] |"
            )
    exclusion_lines = [
        f"- `{entry['program_id']}`: {entry['reason']} (decided {entry['decided_at']})"
        for entry in metrics["exclusions"]["programs"]
    ]
    lines = [
        "# Codex Pilot Handoff",
        "",
        (
            "> **Engineering-only mock output. This is not a scientific result handoff.**"
            if metrics.get("engineering_only")
            else "> Generated from the validated pilot session."
        ),
        "",
        f"- Exact N: **{metrics['n_programs']} programs**",
        f"- Exact model: `{settings['model']}`",
        f"- Provider: `{settings['provider']}`",
        f"- Temperature: `{settings['temperature']}`",
        f"- Max tokens: `{settings['max_tokens']}`",
        f"- Repetitions: **{metrics['repetitions']}**",
        f"- Parser failures: **{metrics['safety']['parser_failures']}**",
        f"- Provider failures: **{metrics['safety']['provider_failures']}**",
        f"- Exclusions: **{metrics['exclusions']['count']}**",
        "",
        "## Exact programs",
        "",
        programs or "None.",
        "",
        "## Top-1/3/5 and EXAM",
        "",
        *topk_lines,
        "",
        f"EXAM control mean: **{metrics['exam']['control_mean']:.4f}**; treatment mean: "
        f"**{metrics['exam']['treatment_mean']:.4f}**; treatment-control difference: "
        f"**{metrics['exam']['mean_difference_treatment_minus_control']:.4f}**; two-sided "
        f"Wilcoxon p: **{metrics['exam']['wilcoxon_two_sided_p']:.6g}**; paired rank-biserial: "
        f"**{metrics['exam']['paired_rank_biserial']:.4f}**.",
        "",
        "Per-repetition exact McNemar discordant counts, p-values, adjusted odds ratios, "
        "per-pattern raw counts, and all bootstrap metadata are in `results/pilot_metrics.json`.",
        "",
        "## Exclusions and failures",
        "",
        *(exclusion_lines or ["No pre-treatment exclusions."]),
        "",
        f"Parser failures: **{metrics['safety']['parser_failures']}**; provider failures: "
        f"**{metrics['safety']['provider_failures']}**. The selected parser-failure policy was "
        f"`{metrics['parser_failure_policy']}`.",
        "",
        "## Reproduction",
        "",
        "```sh",
        reproduce_command,
        "```",
        "",
        "## Strongest justified claim",
        "",
        strongest_claim(metrics),
        "",
        "## Claims not justified",
        "",
        "- Generalization beyond the exact sample, model, prompts, provider, and settings.",
        "- End-to-end improvement from a predicted pattern label unless that arm was separately run.",
        "- A causal explanation that excludes prompt length without a token-matched placebo arm.",
        "- Any benefit hidden by, or inferred after, post-treatment exclusions.",
    ]
    return "\n".join(lines)


def write_outputs(
    *,
    frame: pd.DataFrame,
    metrics: dict[str, Any],
    results_root: Path,
    reproduce_command: str,
    control_name: str,
    treatment_name: str,
) -> None:
    results_root.mkdir(parents=True, exist_ok=True)
    csv_path = results_root / "pilot_results.csv"
    csv_temporary = csv_path.with_suffix(".csv.tmp")
    frame.sort_values(["program_id", "repetition", "condition"]).to_csv(
        csv_temporary, index=False
    )
    csv_temporary.replace(csv_path)
    write_json_atomic(results_root / "pilot_metrics.json", metrics)
    write_text_atomic(results_root / "PILOT_RESULTS.md", render_results_markdown(metrics))
    write_text_atomic(
        results_root / "ADVERSARIAL_AUDIT.md", render_adversarial_audit(metrics)
    )
    write_text_atomic(
        results_root / "CODEX_HANDOFF.md", render_handoff(metrics, reproduce_command)
    )
    make_figures(frame, metrics, results_root / "figures", control_name, treatment_name)
