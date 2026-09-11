# OpenRouter model freeze

The user authorized changing provider from Gemini to OpenRouter and requesting
`z-ai/glm-5.3-flash`, while retaining temperature 0, five
scientific repetitions, the registered 12-call smoke procedure, and all frozen
scientific inputs. Earlier Gemini VOID attempts remain preserved.

The first OpenRouter smoke attempt then demonstrated mechanical truncation at
1,024 output tokens. The pre-results amendment in
`PRE_RESULTS_AMENDMENT_MAX_TOKENS_4096.md` raises only `max_tokens` to 4,096.
It was authorized and committed before any scientific candidate call. This
provider runbook now uses that amended value.

Authenticated registry evidence and the provider choice made before generation
are in `model-freeze-attempts/20260911T173446Z-openrouter-smoke/`.
Pin **Z.AI**, endpoint **`z-ai/fp8`**, whose registry name identifies the upstream
release `z-ai/glm-5.3-flash-20260826`. Send the user-requested model ID unchanged.
The API registry does not expose an immutable weights digest.

The transport adds only the user-requested provider routing object:

```json
{
  "provider": {
    "only": ["z-ai/fp8"],
    "order": ["z-ai/fp8"],
    "allow_fallbacks": false,
    "require_parameters": true
  }
}
```

OpenRouter documents these controls in its
[provider-routing guide](https://openrouter.ai/docs/guides/routing/provider-selection).
The original `model`, `temperature`, `max_tokens`, and system/user messages are
unchanged in shape. No reasoning, JSON-mode, sampling, or retry parameter is added.
The parser still validates JSON requested by the frozen prompt.

Use a credential provided securely through `OPENROUTER_API_KEY`. No automatic
`.env` discovery or credential copying into a repository file is needed.

```bash
.venv/bin/python -m experiments.model_preflight \
  --provider openai_compatible --provider-label openrouter \
  --base-url https://openrouter.ai/api/v1 \
  --model z-ai/glm-5.3-flash --model-kind pinned \
  --model-reference pilot/v2/model-freeze-attempts/20260911T173446Z-openrouter-smoke/routing_decision.json \
  --openrouter-provider z-ai/fp8 --openrouter-provider-name Z.AI \
  --temperature 0 --max-tokens 4096 --timeout 120 \
  --output pilot/v2/MODEL_FREEZE_RECORD.json
```

Every smoke completion must report `model=z-ai/glm-5.3-flash` and `provider=Z.AI`
exactly. Missing or mismatched provider identity is a provider failure; the raw
record is saved first, then the smoke procedure stops. The same check applies
to every later scientific call, including an immediate session-health stop for
provider drift after the first 50 calls. No automatic retries or fallbacks occur.

On success, the existing single session-order coin flip runs once. The freeze
settings retain the routing object and expected name, plus the observed provider
set. A later main run must supply the same two OpenRouter routing flags along
with the existing runbook arguments; missing/changed routing fails the committed
freeze check. Its session manifest and recorded command retain the pin. No full
pilot command is executed by this runbook's smoke step.

Offline verification before this provider's first smoke call: **74 tests passed**,
including provider pinning across 12 fixture calls, missing/changed identity,
changed freeze routing, late provider drift, and HTTP 503 without retries or a
coin flip. Frozen prompts, priors, datasets, scientific configurations, statistical
analysis code, and generation settings were not changed.

For the fresh post-amendment smoke, generation settings differ from the earlier
VOID attempt only in `max_tokens=4096`. Temperature remains zero. A passing
freeze must record 4,096 and the later generic and pattern sessions must both
use 4,096 exactly.

The fresh attempt passed 12/12 calls with zero parser failures. Every response
reported exact model `z-ai/glm-5.3-flash`, provider `Z.AI`, and finish reason
`stop`. Gate 5 then executed its single registered coin flip and froze order
`G`, then `P`. The passing record is `MODEL_FREEZE_RECORD.json`; the full pilot
remains unauthorized.
