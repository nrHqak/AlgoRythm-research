"""Offline routing/identity guards using only the committed smoke fixtures."""
import json
from types import SimpleNamespace
from unittest.mock import Mock, patch

import pytest

from experiments.health import assert_session_health
from experiments.model_preflight import run, validate_freeze
from experiments.providers.routing import routing_settings
from experiments.safety import SafetyViolation
from tests.test_v2_preflight import ROOT, smoke_args


def args_for(tmp_path):
    args = smoke_args(tmp_path)
    args.provider_label = "openrouter"
    args.base_url = "https://openrouter.ai/api/v1"
    args.model = "z-ai/glm-5.3-flash"
    args.openrouter_provider = "z-ai/fp8"
    args.openrouter_provider_name = "Z.AI"
    return args


def response(provider="Z.AI", model="z-ai/glm-5.3-flash"):
    result = Mock()
    result.json.return_value = {
        "model": model, "provider": provider,
        "choices": [{"message": {"content": '{"ranking":[{"line":1,"score":1}]}'}, "finish_reason": "stop"}],
    }
    return result


def test_pinned_route_all_smoke_calls_and_frozen_pin(tmp_path, monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "offline-test-not-a-key")
    args = args_for(tmp_path)
    with patch("experiments.providers.http.requests.post", return_value=response()) as post, \
         patch("experiments.model_preflight.secrets.randbits", return_value=0) as coin:
        freeze = run(args)
    assert post.call_count == freeze["calls"] == freeze["parse_successes"] == 12
    coin.assert_called_once_with(1)
    assert freeze["echoed_underlying_providers"] == ["Z.AI"]
    assert freeze["session_order"] == ["G", "P"]
    for call in post.call_args_list:
        payload = call.kwargs["json"]
        assert set(payload) == {"model", "temperature", "max_tokens", "messages", "provider"}
        assert payload["provider"] == {"only": ["z-ai/fp8"], "order": ["z-ai/fp8"],
                                       "allow_fallbacks": False, "require_parameters": True}
        assert payload["temperature"] == 0 and payload["max_tokens"] == 1024
    args.model_freeze = args.output
    args.condition_order = "counterbalanced"
    args.system_prompt = ROOT / "pilot/v2/prompts/system_v2.txt"
    args.user_template = ROOT / "pilot/prompts/control.txt"
    with patch("experiments.model_preflight.assert_committed"):
        validate_freeze(args, 5)
        args.openrouter_provider = "different-endpoint"
        with pytest.raises(SafetyViolation, match="differ"):
            validate_freeze(args, 5)
        args.openrouter_provider = "z-ai/fp8"
        data = json.loads(args.output.read_text())
        data["echoed_underlying_providers"] = []
        args.output.write_text(json.dumps(data))
        with pytest.raises(SafetyViolation, match="underlying"):
            validate_freeze(args, 5)


@pytest.mark.parametrize("actual", [None, "OtherProvider"])
def test_missing_or_changed_provider_aborts_before_coin(tmp_path, monkeypatch, actual):
    monkeypatch.setenv("OPENROUTER_API_KEY", "offline-test-not-a-key")
    args = args_for(tmp_path)
    with patch("experiments.providers.http.requests.post", return_value=response(actual)) as post, \
         patch("experiments.model_preflight.secrets.randbits") as coin:
        with pytest.raises(SafetyViolation, match="UnderlyingProviderMismatch"):
            run(args)
    assert post.call_count == 1
    coin.assert_not_called()
    assert not args.output.exists()
    assert list(args.artifacts.glob("*/VOID.json"))
    raw = json.loads(next(args.artifacts.glob("*/raw/*.json")).read_text())
    assert raw["response_metadata"]["actual_underlying_provider"] == actual


def test_underlying_drift_after_first_50_is_immediate_failure():
    # This check precedes rate thresholds, so even a late single drift is fatal.
    records = [SimpleNamespace(error_type=None) for _ in range(100)]
    records[-1].error_type = "UnderlyingProviderMismatch"
    with pytest.raises(SafetyViolation, match="UnderlyingProviderMismatch"):
        assert_session_health(records)


@pytest.mark.parametrize("url,slug,name", [
    ("https://openrouter.ai/api/v1", None, None),
    ("https://openrouter.ai/api/v1", "z-ai/fp8", None),
    ("https://other.invalid/api/v1", "z-ai/fp8", "Z.AI"),
    ("http://openrouter.ai/api/v1", "z-ai/fp8", "Z.AI"),
])
def test_cannot_silently_route_without_complete_pin(url, slug, name):
    with pytest.raises(ValueError, match="OpenRouter requires"):
        routing_settings(SimpleNamespace(base_url=url, openrouter_provider=slug, openrouter_provider_name=name))


def test_http_503_stops_without_retry_or_coin(tmp_path, monkeypatch):
    from requests import HTTPError
    monkeypatch.setenv("OPENROUTER_API_KEY", "offline-test-not-a-key")
    bad = response()
    bad.raise_for_status.side_effect = HTTPError("503 offline fixture")
    args = args_for(tmp_path)
    with patch("experiments.providers.http.requests.post", side_effect=[response(), bad]) as post, \
         patch("experiments.model_preflight.secrets.randbits") as coin:
        with pytest.raises(SafetyViolation, match="HTTPError"):
            run(args)
    assert post.call_count == 2
    coin.assert_not_called()
    assert not args.output.exists()
