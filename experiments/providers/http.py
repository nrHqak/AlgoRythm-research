from __future__ import annotations

import time
from datetime import datetime, timezone
from typing import Any

import requests

from experiments.providers.base import CompletionRequest, LLMProvider, ProviderReply


_SENSITIVE_RESPONSE_KEYS = {
    "authorization",
    "api_key",
    "apikey",
    "x_api_key",
    "access_token",
    "refresh_token",
}


def _credential_safe_copy(value: Any, api_key: str) -> tuple[Any, int]:
    """Copy a provider JSON value while removing any echoed credential."""
    if isinstance(value, dict):
        result, redactions = {}, 0
        for key, item in value.items():
            normalized = str(key).lower().replace("-", "_")
            if normalized in _SENSITIVE_RESPONSE_KEYS:
                result[key] = "[REDACTED]"
                redactions += 1
            else:
                result[key], count = _credential_safe_copy(item, api_key)
                redactions += count
        return result, redactions
    if isinstance(value, list):
        result, redactions = [], 0
        for item in value:
            safe, count = _credential_safe_copy(item, api_key)
            result.append(safe)
            redactions += count
        return result, redactions
    if isinstance(value, str) and api_key and api_key in value:
        return value.replace(api_key, "[REDACTED]"), 1
    return value, 0


class OpenAICompatibleProvider(LLMProvider):
    """Minimal adapter for an OpenAI-compatible chat-completions endpoint."""

    def __init__(
        self,
        *,
        base_url: str,
        api_key: str,
        provider_name: str = "openai_compatible",
        timeout_seconds: float = 120.0,
        routing: dict[str, Any] | None = None,
    ) -> None:
        if not base_url.strip():
            raise ValueError("base_url is required")
        if not api_key.strip():
            raise ValueError("LLM_API_KEY is required for the HTTP provider")
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.name = provider_name
        self.timeout_seconds = timeout_seconds
        self.routing = routing

    def complete(self, request: CompletionRequest) -> ProviderReply:
        payload = {
            "model": request.model,
            "temperature": request.temperature,
            "max_tokens": request.max_tokens,
            "messages": [
                {"role": "system", "content": request.system_prompt},
                {"role": "user", "content": request.user_prompt},
            ],
        }
        if self.routing is not None:
            payload["provider"] = self.routing["provider_preferences"]
        started = time.perf_counter()
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=self.timeout_seconds,
        )
        latency = time.perf_counter() - started
        response.raise_for_status()
        body: Any = response.json()
        safe_body, redactions = _credential_safe_copy(body, self.api_key)
        choice = None
        if isinstance(body, dict) and isinstance(body.get("choices"), list) and body["choices"]:
            choice = body["choices"][0]
        message = choice.get("message") if isinstance(choice, dict) else None
        content = message.get("content") if isinstance(message, dict) else None
        raw_response = content if isinstance(content, str) else None
        reasoning = message.get("reasoning") if isinstance(message, dict) else None
        usage = body.get("usage") if isinstance(body, dict) and isinstance(body.get("usage"), dict) else {}
        metadata = {
            "provider_request_id": body.get("id") if isinstance(body, dict) else None,
            "provider_created": body.get("created") if isinstance(body, dict) else None,
            "model_identity_exposed": bool(body.get("model")) if isinstance(body, dict) else False,
            "finish_reason": choice.get("finish_reason") if isinstance(choice, dict) else None,
            "native_finish_reason": choice.get("native_finish_reason") if isinstance(choice, dict) else None,
            "completion_content_type": type(content).__name__,
            "reasoning_present": bool(reasoning),
            "reasoning_chars": len(reasoning) if isinstance(reasoning, str) else None,
        }
        if self.routing is not None:
            metadata.update(
                provider_preferences=self.routing["provider_preferences"],
                expected_underlying_provider=self.routing["expected_provider_name"],
                actual_underlying_provider=body.get("provider") if isinstance(body, dict) else None,
            )
        return ProviderReply(
            raw_response=raw_response,
            latency=latency,
            token_usage=usage,
            provider=self.name,
            model=str(body.get("model") or "") if isinstance(body, dict) else "",
            timestamp=datetime.now(timezone.utc),
            response_metadata=metadata,
            raw_provider_response=safe_body,
            provider_response_redactions=redactions,
            http_status=response.status_code,
        )
