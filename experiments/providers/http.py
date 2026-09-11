from __future__ import annotations

import time
from datetime import datetime, timezone
from typing import Any

import requests

from experiments.providers.base import CompletionRequest, LLMProvider, ProviderReply


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
        body: dict[str, Any] = response.json()
        try:
            raw_response = body["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise ValueError("provider response has no chat-completion content") from exc
        if not isinstance(raw_response, str):
            raise ValueError("provider completion content must be a string")
        usage = body.get("usage") if isinstance(body.get("usage"), dict) else {}
        metadata = {
            "provider_request_id": body.get("id"),
            "provider_created": body.get("created"),
            "model_identity_exposed": bool(body.get("model")),
            "finish_reason": body.get("choices", [{}])[0].get("finish_reason"),
        }
        if self.routing is not None:
            metadata.update(
                provider_preferences=self.routing["provider_preferences"],
                expected_underlying_provider=self.routing["expected_provider_name"],
                actual_underlying_provider=body.get("provider"),
            )
        return ProviderReply(
            raw_response=raw_response,
            latency=latency,
            token_usage=usage,
            provider=self.name,
            model=str(body.get("model") or ""),
            timestamp=datetime.now(timezone.utc),
            response_metadata=metadata,
        )
