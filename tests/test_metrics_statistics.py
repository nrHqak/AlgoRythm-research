from __future__ import annotations

from datetime import datetime, timezone

import numpy as np
import pandas as pd

from analysis.metrics import conservative_fault_rank, evaluate_record
from analysis.statistics import clustered_bootstrap_delta, exact_mcnemar
from experiments.models import ParsedRunRecord, RankingResponse


def test_conservative_worst_rank_tie_handling() -> None:
    ranking = RankingResponse.model_validate(
        {
            "ranking": [
                {"line": 8, "score": 0.9, "reason": ""},
                {"line": 9, "score": 0.8, "reason": ""},
                {"line": 10, "score": 0.8, "reason": ""},
                {"line": 11, "score": 0.7, "reason": ""},
            ]
        }
    )
    assert conservative_fault_rank(ranking, [9], 20) == 3
    assert conservative_fault_rank(ranking, [19], 20) == 20


def test_exact_mcnemar_reports_raw_discordant_counts() -> None:
    result = exact_mcnemar(np.array([1, 1, 0, 0]), np.array([1, 0, 1, 1]))
    assert result["control_hit_treatment_miss"] == 1
    assert result["control_miss_treatment_hit"] == 2
    assert result["discordant_pairs"] == 3


def test_bootstrap_clusters_repetitions_by_program() -> None:
    frame = pd.DataFrame(
        {
            "program_id": ["a", "a", "a", "a", "b", "b", "b", "b"],
            "condition": ["c", "c", "t", "t", "c", "c", "t", "t"],
            "top1": [0, 0, 1, 1, 1, 1, 1, 1],
        }
    )
    result = clustered_bootstrap_delta(
        frame,
        metric="top1",
        control_name="c",
        treatment_name="t",
        iterations=100,
        seed=7,
    )
    assert result["n_programs"] == 2
    assert result["mean_delta"] == 0.5


def test_parser_failure_is_a_miss_even_for_tiny_program() -> None:
    record = ParsedRunRecord(
        run_id="r",
        session_id="s",
        execution_key="e",
        experiment_name="x",
        program_id="p",
        task_id="t",
        condition="control",
        repetition=1,
        provider="mock",
        model="mock",
        temperature=0,
        max_tokens=10,
        timestamp=datetime.now(timezone.utc),
        latency=0.1,
        token_usage={},
        raw_response_path="raw.json",
        parsed_response=None,
        status="parser_failure",
        error_type="ResponseParseError",
        error_message="invalid",
        source_line_count=2,
        loc=2,
        evaluation_denominator=2,
        faulty_lines=[1],
        pattern_label="label",
        difficulty="level",
        system_prompt_hash="a",
        shared_prompt_hash="b",
        prior_hash=None,
        prompt_chars=10,
        prompt_tokens_estimate=3,
        manifest_hash="m",
    )
    metrics = evaluate_record(record)
    assert (metrics["top1"], metrics["top3"], metrics["top5"], metrics["exam"]) == (
        0,
        0,
        0,
        1.0,
    )
