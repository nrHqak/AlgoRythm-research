from __future__ import annotations

import json
from pathlib import Path

from analysis.run_analysis import parser as analysis_parser
from analysis.run_analysis import run as analyze
from experiments.run_pilot import parser as runner_parser
from experiments.run_pilot import run as run_pilot


def write(path: Path, content: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def test_mock_pipeline_saves_raw_before_parse_and_generates_all_outputs(tmp_path: Path) -> None:
    data = tmp_path / "data"
    buggy = write(data / "buggy.py", "value = 1\nprint(value)\n")
    fixed = write(data / "fixed.py", "value = 2\nprint(value)\n")
    tests = data / "tests"
    tests.mkdir()
    context = write(data / "problem.txt", "Print the expected value.")
    manifest = write(
        tmp_path / "manifest.yaml",
        "\n".join(
            [
                "manifest_version: 1",
                "dataset_name: smoke-only",
                "created_at: 2020-01-01T00:00:00Z",
                "selection_frozen_at: 2020-01-02T00:00:00Z",
                "programs:",
                "  - program_id: smoke-1",
                "    task_id: task-1",
                f"    buggy_source_path: {buggy}",
                f"    fixed_source_path: {fixed}",
                f"    tests_path: {tests}",
                "    faulty_lines: [1]",
                "    pattern_label: handoff-label",
                "    pattern_source: frozen-handoff-row",
                "    loc: 2",
                "    difficulty: handoff-level",
                "    inclusion_status: included",
                "    exclusion_reason: null",
                "    exclusion_decided_at: null",
                f"    problem_context_path: {context}",
            ]
        )
        + "\n",
    )
    config = write(
        tmp_path / "config.yaml",
        "\n".join(
            [
                "experiment_name: smoke_pipeline",
                "dataset:",
                "  target: smoke-only",
                "  target_n: 1",
                "conditions:",
                "  control: pattern_agnostic",
                "  treatment: oracle_pattern_prior",
                "metrics: [top1, top3, top5, exam]",
                "repetitions: 2",
                "statistics:",
                "  primary: exact_mcnemar",
                "  bootstrap_iterations: 100",
            ]
        )
        + "\n",
    )
    system = write(tmp_path / "system.txt", "Return an ordered JSON ranking.")
    template = write(
        tmp_path / "user.txt",
        "Task {task_id}\n{problem_context}\nSource:\n{numbered_buggy_source}",
    )
    priors = write(tmp_path / "priors.yaml", "handoff-label: frozen prior text\n")
    results = tmp_path / "results"
    experiment_log = write(tmp_path / "EXPERIMENT_LOG.md", "# Test log\n")
    session_id = "smoke-session"

    runner_args = runner_parser().parse_args(
        [
            "--config",
            str(config),
            "--manifest",
            str(manifest),
            "--system-prompt",
            str(system),
            "--user-template",
            str(template),
            "--priors",
            str(priors),
            "--provider",
            "mock",
            "--model",
            "mock-model",
            "--temperature",
            "0",
            "--max-tokens",
            "64",
            "--condition-order",
            "counterbalanced",
            "--session-id",
            session_id,
            "--output-root",
            str(results),
            "--experiment-log",
            str(experiment_log),
            "--allow-mock",
        ]
    )
    assert run_pilot(runner_args) == 0

    raw_files = sorted((results / "raw/smoke_pipeline/smoke-session").glob("*.json"))
    assert len(raw_files) == 4
    raw_payloads = [json.loads(path.read_text(encoding="utf-8")) for path in raw_files]
    assert all(payload["raw_saved_before_parsing"] for payload in raw_payloads)
    assert all("faulty_lines" not in payload["user_prompt"] for payload in raw_payloads)

    analysis_args = analysis_parser().parse_args(
        [
            "--config",
            str(config),
            "--manifest",
            str(manifest),
            "--session-id",
            session_id,
            "--results-root",
            str(results),
            "--parser-failure-policy",
            "count_as_failure",
            "--bootstrap-iterations",
            "100",
            "--allow-mock-analysis",
        ]
    )
    analyze(analysis_args)
    for relative in (
        "pilot_results.csv",
        "pilot_metrics.json",
        "PILOT_RESULTS.md",
        "ADVERSARIAL_AUDIT.md",
        "CODEX_HANDOFF.md",
        "figures/control_vs_prior_topk.png",
        "figures/exam_score.png",
        "figures/per_pattern_delta.png",
        "figures/pairwise_transitions.png",
    ):
        assert (results / relative).is_file(), relative
