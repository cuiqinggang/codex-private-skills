# Kilo Integration

## Preferred Placement

Put the local 27B model in Kilo/Cursor as a selectable local model, not as the default.

Keep current default:

```json
{
  "model": "openrouter/deepseek/deepseek-v4-pro"
}
```

Add local 27B as an optional provider/model so the user can select it from Kilo when privacy, offline use, or local cost control matters.

## Local Endpoint

The verified local server is:

```text
Base URL: http://127.0.0.1:1234/v1
Model: qwen3.6-27b-iq4-xs-mtp
Provider style: LM Studio or OpenAI Compatible
API key: usually not required by llama.cpp; if UI requires a value, use a harmless placeholder such as local.
```

Kilo 7.3.46 has built-in provider IDs:

- `lmstudio`
- `openai-compatible`
- `ollama`
- `litellm`

Prefer `lmstudio` or `openai-compatible` for the local llama.cpp server.

## User Experience

If the 27B service is already running:

- selecting the model in Kilo should not reload the model into the thread.
- Kilo sends requests to the already loaded local server.
- first streamed token is usually around 1 second for short prompts.

If the 27B service is not running:

- start `scripts/start-qwen27b-mtp.ps1`.
- wait until `/v1/models` returns `qwen3.6-27b-iq4-xs-mtp`.
- initial load can be tens of seconds to around a minute depending on disk/cache/GPU state; measure it on the target machine before promising an exact number.

Use Kilo mode by default:

```powershell
${REDACTED_SECRET}
```

Kilo can send large agent prompts. On 2026-07-06, a trivial Kilo run sent about 18815 tokens, so the 4096 context server rejected it. The verified Kilo server used:

```text
ctx-size: 24576
KV cache: q4_0
MTP: draft-mtp + spec-default + p-min 0.5
```

For direct API chat where speed matters more than Kilo agent context, use:

```powershell
${REDACTED_SECRET}
```

Fast mode uses 4096 context and f16 KV. It is faster but not enough for normal Kilo agent prompts.

## Verified Kilo Config

Kilo config accepted this local provider without warnings:

```json
"provider": {
  "local-qwen27b": {
    "npm": "@ai-sdk/openai-compatible",
    "name": "Local Qwen3.6 27B MTP",
    "options": {
      "baseURL": "http://127.0.0.1:1234/v1"
    },
    "models": {
      "qwen3.6-27b-iq4-xs-mtp": {
        "name": "Qwen3.6 27B IQ4_XS MTP"
      }
    }
  }
}
```

Validation:

```powershell
${REDACTED_SECRET}
${REDACTED_SECRET}
```

Expected model:

```text
local-qwen27b/qwen3.6-27b-iq4-xs-mtp
```

Live CLI proof on 2026-07-06 returned:

```text
是的，当前会话正由本地模型 `local-qwen27b/qwen3.6-27b-iq4-xs-mtp` 驱动。
```

## When To Use Local 27B

Use local 27B for:

- private local drafts
- offline or low-cost code reasoning
- medium-complex Chinese analysis
- tasks where 25-30 tok/s is acceptable

Prefer DeepSeek V4 Pro for:

- high-stakes code execution
- long agentic edits
- tool-heavy workflows
- cases where local 27B quality is uncertain

Prefer Qwen3-VL route for visual/video keyframe tasks.
