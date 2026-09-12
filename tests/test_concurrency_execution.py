"""Offline checks for the bounded-concurrency execution amendment."""
from __future__ import annotations

import json
import threading
import time
from datetime import datetime, timezone
from unittest.mock import patch

import pytest

from experiments.concurrency_preflight_32768 import parser as preflight_parser, run as run_preflight
from experiments.providers.base import LLMProvider, ProviderReply
from experiments.run_pilot import deterministic_run_id_for
from experiments.storage import write_json_new_atomic


class TrackingProvider(LLMProvider):
    name = "openrouter"

    def __init__(self) -> None:
        self.lock = threading.Lock()
        self.active = 0
        self.maximum_active = 0
        self.sessions_started: list[str] = []

    def complete(self, request):
        session = "P" if "synthetic-stress-dp-segments-v1" in request.user_prompt else "G"
        with self.lock:
            self.active += 1
            self.maximum_active = max(self.maximum_active, self.active)
            self.sessions_started.append(session)
        time.sleep(0.01)
        with self.lock:
            self.active -= 1
        return ProviderReply(
            raw_response='{"ranking":[{"line":1,"score":1,"reason":"synthetic"}]}',
            latency=0.01,
            token_usage={
                "prompt_tokens": 100,
                "completion_tokens": 20,
                "cost": 0.0001,
                "completion_tokens_details": {"reasoning_tokens": 5},
            },
            provider="openrouter",
            model="z-ai/glm-5.3-flash",
            timestamp=datetime.now(timezone.utc),
            response_metadata={
                "finish_reason": "stop",
                "actual_underlying_provider": "Z.AI",
                "provider_preferences": {
                    "only": ["z-ai/fp8"],
                    "order": ["z-ai/fp8"],
                    "allow_fallbacks": False,
                    "require_parameters": True,
                },
            },
            raw_provider_response={
                "model": "z-ai/glm-5.3-flash",
                "provider": "Z.AI",
            },
            provider_response_redactions=0,
            http_status=200,
        )


def args_for(tmp_path):
    log = tmp_path / "experiment.md"
    log.write_text("# test\n")
    return preflight_parser().parse_args([
        "--provider", "openai_compatible",
        "--provider-label", "openrouter",
        "--openrouter-provider", "z-ai/fp8",
        "--openrouter-provider-name", "Z.AI",
        "--base-url", "https://openrouter.ai/api/v1",
        "--model", "z-ai/glm-5.3-flash",
        "--model-kind", "pinned",
        "--model-reference", "offline test reference",
        "--temperature", "0",
        "--max-tokens", "32768",
        "--timeout", "120",
        "--workers", "4",
        "--output-root", str(tmp_path / "preflight"),
        "--experiment-log", str(log),
    ])


def test_deterministic_run_id_uses_registered_call_identity():
    first = deterministic_run_id_for(program_id="p", condition="B", repetition=3)
    assert first == deterministic_run_id_for(program_id="p", condition="B", repetition=3)
    assert len(first) == 64
    assert len({
        first,
        deterministic_run_id_for(program_id="q", condition="B", repetition=3),
        deterministic_run_id_for(program_id="p", condition="C", repetition=3),
        deterministic_run_id_for(program_id="p", condition="B", repetition=4),
    }) == 4


def test_atomic_new_json_never_overwrites(tmp_path):
    path = tmp_path / "raw" / "record.json"
    write_json_new_atomic(path, {"value": 1})
    with pytest.raises(FileExistsError):
        write_json_new_atomic(path, {"value": 2})
    assert json.loads(path.read_text()) == {"value": 1}
    assert not list(path.parent.glob("*.tmp"))


def test_concurrency_preflight_is_bounded_and_session_sequential(tmp_path):
    provider = TrackingProvider()
    with patch("experiments.concurrency_preflight_32768.make_provider", return_value=provider):
        result = run_preflight(args_for(tmp_path))
    assert result["status"] == "PASS"
    assert result["aggregate"]["calls_valid"] == 20
    assert result["aggregate"]["failures"] == 0
    assert 2 <= provider.maximum_active <= 4
    assert provider.sessions_started[:10] == ["G"] * 10
    assert provider.sessions_started[10:] == ["P"] * 10
    ordered = sorted((tmp_path / "preflight" / "ordered").glob("call-*.json"))
    assert [json.loads(path.read_text())["order"] for path in ordered] == list(range(1, 21))
    raw = list((tmp_path / "preflight" / "raw").glob("*/*.json"))
    assert len(raw) == 20
    assert not list((tmp_path / "preflight").rglob("*.tmp"))
