# 2026-06-23 GLM-5.2 Default, DeepSeek Official V4 Pro Switch, Qwen3-VL 235B

## Use When

Hermes must keep the main/default model on OpenRouter `z-ai/glm-5.2`, but also
needs a lower-cost explicit switch to DeepSeek official `deepseek-v4-pro`.
Qwen3-VL 235B should remain available as the multimodal/vision model.

## Hard Boundaries

- Do not change Windows proxy, FlClash, Telegram proxy, node, or rules.
- Do not print `.env` or provider keys.
- Back up `config.yaml`, `.env`, and `plugins\telegram_model_router\__init__.py`
  before changing model routing.
- Do not restore automatic "complex task" routing unless the user explicitly
  asks for it. It previously caused provider/key mismatch failures.

## Known Good Shape

Main config stays expensive but high quality:

```yaml
model:
  provider: openrouter
  default: z-ai/glm-5.2
```

DeepSeek official credentials belong in `C:\Users\A\.hermes\.env`:

```text
DEEPSEEK_API_KEY=...
DEEPSEEK_BASE_URL=https://api.deepseek.com
```

Qwen3-VL 235B can remain under `auxiliary.vision`:

```yaml
auxiliary:
  vision:
    provider: openrouter
    model: qwen/qwen3-vl-235b-a22b-instruct
    base_url: https://openrouter.ai/api/v1
```

## Router Rule

Telegram switching should be explicit only:

- Default / GLM trigger clears session override and returns to configured
  `z-ai/glm-5.2`.
- DeepSeek trigger sets session override to:
  - `provider=deepseek`
  - `model=deepseek-v4-pro`
  - `base_url=https://api.deepseek.com`
  - `api_key=os.getenv("DEEPSEEK_API_KEY")`
  - `api_mode=chat_completions`

Important: set `api_key` explicitly from `DEEPSEEK_API_KEY` in the override.
If it is left blank, Hermes may reuse the OpenRouter key for a DeepSeek provider
request and fail in confusing ways.

Recommended trigger phrases:

```text
deepseek-v4-pro
deepseek pro
use deepseek
切换deepseek
省钱
低成本
glm-5.2
z-ai/glm-5.2
切回默认
用默认模型
```

Ignore slash commands in the router so normal Telegram bot commands keep their
native behavior.

## Verification

Run the bridge diagnostic first:

```powershell
powershell -ExecutionPolicy Bypass -File "C:\Users\A\.codex\skills\hermes-telegram-persistent-bridge\scripts\check-hermes-telegram.ps1"
```

Then verify three layers:

1. Direct provider checks:
   - OpenRouter `z-ai/glm-5.2` returns a fixed marker.
   - DeepSeek official `deepseek-v4-pro` returns a fixed marker.
   - OpenRouter `qwen/qwen3-vl-235b-a22b-instruct` returns a fixed marker.
2. Hermes CLI checks:
   - `hermes -z "Reply exactly: HERMES_GLM52_CLI_OK" --provider openrouter --model z-ai/glm-5.2 --ignore-rules`
   - `hermes -z "Reply exactly: HERMES_DEEPSEEK_CLI_OK" --provider deepseek --model deepseek-v4-pro --ignore-rules`
3. Real Telegram checks from phone or Desktop Telegram:
   - `glm-5.2 默认模型测试：请只回复 HERMES_TELEGRAM_GLM52_OK`
   - `deepseek-v4-pro 测试：请只回复 HERMES_TELEGRAM_DEEPSEEK_OK`
   - `glm-5.2 切回默认模型测试：请只回复 HERMES_TELEGRAM_GLM52_BACK_OK`

Acceptance requires a matching fresh inbound message and `response ready` in
`C:\Users\A\.hermes\logs\gateway.log`, plus `agent.log` showing the intended
provider/model for the call.

## Web Slowdown Note

When browser/WebUI first token feels very slow but Telegram is usable, check
`agent.log` input token counts. A long Hermes session can grow near hundreds of
thousands of input tokens, making each GLM call slow even when the upstream API
itself is healthy. For WebUI speed tests, use a fresh/new chat or a small
context before blaming the provider.
