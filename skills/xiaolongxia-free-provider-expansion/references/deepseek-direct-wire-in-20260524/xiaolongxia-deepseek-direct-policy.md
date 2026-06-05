# Xiaolongxia DeepSeek Direct Policy

Current active model route:

```text
Xiaolongxia internal LLM wrapper
  -> DeepSeek official API
  -> deepseek-v4-flash
```

Runtime model:

- Provider: `deepseek-official-direct`
- Base URL: `https://api.deepseek.com`
- Endpoint: `https://api.deepseek.com/chat/completions`
- Model: `deepseek-v4-flash`
- Secret file: `C:\Users\A\xiaolongxia-free-api-local\secrets\deepseek_api_key.txt`
- Thinking mode: disabled with `thinking: { "type": "disabled" }`

Runtime rule:

- Do not route Xiaolongxia through `3011` New API for this DeepSeek path.
- Do not route Xiaolongxia through OpenRouter free models for this DeepSeek path.
- Do not use NVIDIA 70B as runtime fallback unless the user explicitly re-enables it.
- Do not keep the old free-model backups as active fallback models.
- Keep the old free-model and NVIDIA reports as historical evidence only.
- Do not print the DeepSeek key in reports, logs, skills, or terminal summaries.
- Do not send real group messages from this test path.

Latest selftest:

- Output root: `C:\Users\A\Desktop\1\output\XIAOLONGXIA-DEEPSEEK-DIRECT-WIRE-IN-20260524`
- Script: `C:\Users\A\xiaolongxia-free-api-local\scripts\xiaolongxia-deepseek-v4-flash-direct-selftest.ps1`
- Status: direct selftest passed 6/6.
- Average latency: about 1 second in the 2026-05-24 run.

Historical-only routes:

- `3011` New API / OpenRouter free pool: preserved for model-pool management and history, not current runtime.
- NVIDIA NIM 8B/70B: preserved for historical test evidence, not current runtime fallback.
- OpenRouter free model candidates: preserved for reports and skill memory, not current runtime fallback.
