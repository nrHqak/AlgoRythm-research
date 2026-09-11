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
    result.status_code = 200
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


def test_null_content_provider_body_is_saved_before_validation(tmp_path):
    from experiments.models import load_manifest
    from experiments.providers.http import OpenAICompatibleProvider
    from experiments.run_pilot import run_one

    program = load_manifest(ROOT / "data/smoke/manifest.json").included[0]
    body = {
        "id": "gen-null-content",
        "model": "z-ai/glm-5.3-flash",
        "provider": "Z.AI",
        "choices": [{
            "finish_reason": "length",
            "native_finish_reason": "length",
            "message": {"content": None, "reasoning": "synthetic reasoning retained"},
        }],
        "usage": {
            "prompt_tokens": 1040,
            "completion_tokens": 4096,
            "completion_tokens_details": {"reasoning_tokens": 4095},
            "cost": 0.002204,
        },
    }
    http_response = Mock(status_code=200)
    http_response.json.return_value = body
    provider = OpenAICompatibleProvider(
        base_url="https://openrouter.ai/api/v1",
        api_key="synthetic-secret-not-for-storage",
        provider_name="openrouter",
        routing={
            "provider_preferences": {
                "only": ["z-ai/fp8"],
                "order": ["z-ai/fp8"],
                "allow_fallbacks": False,
                "require_parameters": True,
            },
            "expected_provider_name": "Z.AI",
        },
    )
    with patch("experiments.providers.http.requests.post", return_value=http_response):
        record = run_one(
            provider=provider,
            program=program,
            condition="generic_prior",
            repetition=1,
            experiment_name="synthetic-persistence-test",
            session_id="synthetic-session",
            system_prompt="synthetic system",
            user_prompt="synthetic user",
            shared_prompt_hash="synthetic-shared-hash",
            prior_hash="synthetic-prior-hash",
            manifest_hash="synthetic-manifest-hash",
            model="z-ai/glm-5.3-flash",
            temperature=0,
            max_tokens=4096,
            raw_session_dir=tmp_path / "raw",
            processed_session_dir=tmp_path / "processed",
        )

    assert record.status == "provider_failure"
    assert record.error_type == "MissingCompletionContent"
    assert record.raw_response is None
    assert record.raw_response_path is not None
    raw = json.loads((ROOT / record.raw_response_path).read_text())
    assert raw["raw_saved_before_parsing"] is True
    assert raw["provider_response_json"] == body
    assert raw["http_status"] == 200
    assert raw["token_usage"]["completion_tokens"] == 4096
    assert raw["response_metadata"]["finish_reason"] == "length"
    assert raw["response_metadata"]["reasoning_present"] is True
    assert "synthetic-secret-not-for-storage" not in json.dumps(raw)


def test_provider_response_credential_echo_is_redacted():
    from experiments.providers.base import CompletionRequest
    from experiments.providers.http import OpenAICompatibleProvider

    secret = "synthetic-secret-not-for-storage"
    body = {
        "model": "snapshot",
        "choices": [{"message": {"content": "{}"}, "finish_reason": "stop"}],
        "debug": {"authorization": f"Bearer {secret}", "note": f"echo:{secret}"},
    }
    http_response = Mock(status_code=200)
    http_response.json.return_value = body
    provider = OpenAICompatibleProvider(base_url="https://offline.invalid/v1", api_key=secret)
    with patch("experiments.providers.http.requests.post", return_value=http_response):
        reply = provider.complete(CompletionRequest("system", "user", "snapshot", 0, 1024))
    retained = json.dumps(reply.raw_provider_response)
    assert secret not in retained
    assert reply.provider_response_redactions == 2
