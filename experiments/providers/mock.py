from __future__ import annotations

import json
import re
import time
from datetime import datetime, timezone

from experiments.providers.base import CompletionRequest, LLMProvider, ProviderReply


class MockProvider(LLMProvider):
    """Deterministic engineering-only provider; never valid for scientific claims."""

    name = "mock"

    def complete(self, request: CompletionRequest) -> ProviderReply:
        started = time.perf_counter()
        lines = [int(value) for value in re.findall(r"(?m)^(\d+):", request.user_prompt)]
        ranking = [
            {"line": line, "score": max(0.0, 1.0 - index * 0.01), "reason": "mock"}
            for index, line in enumerate(lines)
        ]
        raw = json.dumps({"ranking": ranking}, ensure_ascii=False)
        return ProviderReply(
            raw_response=raw,
            latency=time.perf_counter() - started,
            token_usage={"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
            provider=self.name,
            model=request.model,
            timestamp=datetime.now(timezone.utc),
            response_metadata={"engineering_only": True},
        )
