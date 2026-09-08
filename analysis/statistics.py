from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd
from scipy.stats import binomtest, wilcoxon


def exact_mcnemar(control: np.ndarray, treatment: np.ndarray) -> dict[str, Any]:
    control = np.asarray(control, dtype=int)
    treatment = np.asarray(treatment, dtype=int)
    if control.shape != treatment.shape:
        raise ValueError("McNemar inputs must have identical shape")
    control_only = int(np.sum((control == 1) & (treatment == 0)))
    treatment_only = int(np.sum((control == 0) & (treatment == 1)))
    discordant = control_only + treatment_only
    p_value = 1.0 if discordant == 0 else float(
        binomtest(min(control_only, treatment_only), discordant, 0.5, alternative="two-sided").pvalue
    )
    return {
        "control_hit_treatment_miss": control_only,
        "control_miss_treatment_hit": treatment_only,
        "discordant_pairs": discordant,
        "exact_two_sided_p": p_value,
        "treatment_improvement_odds_ratio": (
            None if control_only == 0 and treatment_only > 0 else
            (treatment_only / control_only if control_only else 1.0)
        ),
        "treatment_improvement_odds_ratio_is_infinite": bool(
            control_only == 0 and treatment_only > 0
        ),
        "haldane_anscombe_odds_ratio": (treatment_only + 0.5) / (control_only + 0.5),
    }


def paired_by_program(
    frame: pd.DataFrame,
    metric: str,
    control_name: str,
    treatment_name: str,
) -> pd.DataFrame:
    means = frame.groupby(["program_id", "condition"], as_index=False)[metric].mean()
    pivot = means.pivot(index="program_id", columns="condition", values=metric)
    return pivot[[control_name, treatment_name]].dropna()


def clustered_bootstrap_delta(
    frame: pd.DataFrame,
    *,
    metric: str,
    control_name: str,
    treatment_name: str,
    iterations: int,
    seed: int,
) -> dict[str, Any]:
    paired = paired_by_program(frame, metric, control_name, treatment_name)
    if paired.empty:
        raise ValueError(f"no paired program observations for {metric}")
    deltas = paired[treatment_name].to_numpy() - paired[control_name].to_numpy()
    rng = np.random.default_rng(seed)
    indices = rng.integers(0, len(deltas), size=(iterations, len(deltas)))
    samples = deltas[indices].mean(axis=1)
    lower, upper = np.percentile(samples, [2.5, 97.5])
    return {
        "unit": "program (repetitions retained within program means)",
        "n_programs": int(len(deltas)),
        "iterations": iterations,
        "seed": seed,
        "mean_delta": float(deltas.mean()),
        "percentile_95_ci": [float(lower), float(upper)],
    }


def paired_rank_biserial(control: np.ndarray, treatment: np.ndarray) -> float:
    differences = np.asarray(treatment, dtype=float) - np.asarray(control, dtype=float)
    nonzero = differences[differences != 0]
    if len(nonzero) == 0:
        return 0.0
    absolute = np.abs(nonzero)
    order = absolute.argsort()
    ranks = np.empty(len(absolute), dtype=float)
    ranks[order] = np.arange(1, len(absolute) + 1, dtype=float)
    for value in np.unique(absolute):
        mask = absolute == value
        ranks[mask] = ranks[mask].mean()
    positive = ranks[nonzero > 0].sum()
    negative = ranks[nonzero < 0].sum()
    return float((positive - negative) / (positive + negative))


def cliffs_delta(control: np.ndarray, treatment: np.ndarray) -> float:
    control = np.asarray(control, dtype=float)
    treatment = np.asarray(treatment, dtype=float)
    if len(control) == 0 or len(treatment) == 0:
        return float("nan")
    differences = treatment[:, None] - control[None, :]
    return float((np.sum(differences > 0) - np.sum(differences < 0)) / differences.size)


def exam_comparison(
    frame: pd.DataFrame,
    control_name: str,
    treatment_name: str,
) -> dict[str, Any]:
    paired = paired_by_program(frame, "exam", control_name, treatment_name)
    control = paired[control_name].to_numpy()
    treatment = paired[treatment_name].to_numpy()
    if np.allclose(control, treatment):
        wilcoxon_p = 1.0
    else:
        wilcoxon_p = float(wilcoxon(treatment, control, alternative="two-sided").pvalue)
    return {
        "n_programs": int(len(paired)),
        "control_mean": float(control.mean()),
        "treatment_mean": float(treatment.mean()),
        "mean_difference_treatment_minus_control": float((treatment - control).mean()),
        "wilcoxon_two_sided_p": wilcoxon_p,
        "paired_rank_biserial": paired_rank_biserial(control, treatment),
        "cliffs_delta_descriptive": cliffs_delta(control, treatment),
    }


def leave_one_program_out_delta(
    frame: pd.DataFrame,
    metric: str,
    control_name: str,
    treatment_name: str,
) -> dict[str, Any]:
    paired = paired_by_program(frame, metric, control_name, treatment_name)
    deltas = paired[treatment_name] - paired[control_name]
    if len(deltas) <= 1:
        return {"n_programs": int(len(deltas)), "min": None, "max": None, "most_influential": None}
    leave_one_out = {program_id: float(deltas.drop(program_id).mean()) for program_id in deltas.index}
    original = float(deltas.mean())
    influential = max(leave_one_out, key=lambda key: abs(leave_one_out[key] - original))
    return {
        "n_programs": int(len(deltas)),
        "original_delta": original,
        "min": min(leave_one_out.values()),
        "max": max(leave_one_out.values()),
        "most_influential": influential,
        "delta_without_most_influential": leave_one_out[influential],
    }
