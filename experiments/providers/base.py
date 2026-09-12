from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class CompletionRequest:
    system_prompt: str
    user_prompt: str
    model: str
    temperature: float
    max_tokens: int
    reasoning_effort: str | None = None


@dataclass(frozen=True)
class ProviderReply:
    raw_response: str | None
    latency: float
    token_usage: dict[str, Any] = field(default_factory=dict)
    provider: str = "unknown"
    model: str = "unknown"
    timestamp: datetime | None = None
    response_metadata: dict[str, Any] = field(default_factory=dict)
    raw_provider_response: Any | None = None
    provider_response_redactions: int = 0
    http_status: int | None = None


class LLMProvider(ABC):
    name: str

    @abstractmethod
    def complete(self, request: CompletionRequest) -> ProviderReply:
        """Return unvalidated model content and a credential-safe provider envelope."""
