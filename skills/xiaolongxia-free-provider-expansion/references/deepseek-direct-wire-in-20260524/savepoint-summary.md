# DeepSeek V4 Flash Direct Wire-in Savepoint

Date: 2026-05-24

Status: `XIAOLONGXIA_DEEPSEEK_DIRECT_WIRE_IN_PASS`

## Current Decision

Xiaolongxia should use one active model route:

```text
Xiaolongxia internal LLM/provider wrapper
  -> DeepSeek official API
  -> deepseek-v4-flash
```

This route does not use:

- `3011` New API / OpenRouter pool
- OpenRouter free models
- OpenClaw `18789` `/v1` proxy
- NVIDIA 70B fallback

Old free-model and NVIDIA work remains historical evidence only.

## Why This Replaced Previous Routes

- OpenRouter/free routes were useful for early testing but had quota/balance and model instability issues.
- NVIDIA 8B was fast but the user judged the answer quality too weak.
- NVIDIA 70B was higher quality but too slow in visible use.
- DeepSeek official `deepseek-v4-flash` was accepted as cheap enough and much faster.

## Secret Handling

DeepSeek key is stored only as a local secret file:

```text
C:\Users\A\xiaolongxia-free-api-local\secrets\deepseek_api_key.txt
```

Never print the key, copy it into reports, or store it in skill text.

## Required API Behavior

DeepSeek V4 Flash should be called with thinking disabled:

```json
{
  "model": "deepseek-v4-flash",
  "thinking": {
    "type": "disabled"
  }
}
```

Without this, the API can return HTTP 200 while using token budget for hidden reasoning and leaving `content` empty.

## Evidence

Direct official non-thinking API test:

- File: `G02c-deepseek-v4-flash-nonthinking-test.json`
- HTTP: 200
- Marker returned: true
- Latency: 806 ms
- Key printed: false

Final simple Xiaolongxia direct selftest:

- File: `G01-deepseek-direct-selftest.json`
- Tests: 2
- Passed: 2
- Failed: 0
- Average latency: 2003 ms
- `3011` used: false
- OpenRouter used: false
- OpenClaw `18789` proxy used: false
- Real sends: 0
- Key printed: false

## Reusable Command

```powershell
C:\Users\A\xiaolongxia-free-api-local\scripts\xiaolongxia-deepseek-v4-flash-direct-selftest.ps1 -Mode quick
```

Bundled skill copy:

```powershell
C:\Users\A\.codex\skills\xiaolongxia-free-provider-expansion\scripts\xiaolongxia-deepseek-v4-flash-direct-selftest.ps1 -Mode quick
```

## Identity Correction

If Xiaolongxia says it is GPT-4o, that is an identity prompt/hallucination problem, not proof that the route is GPT-4o.

Verified state after the incident:

- OpenClaw config primary at the time: `deepseek-official/deepseek-v4-flash`
- OpenClaw fallback list: empty
- Gateway log showed: `provider=deepseek-official model=deepseek-v4-flash thinking=off`

Recommended identity wording:

```text
我是小龙虾，本地当前使用 DeepSeek 官方 deepseek-v4-flash。不是 GPT-4o。
```

## Current Operational Rule

Use only DeepSeek official `deepseek-v4-flash` for the active Xiaolongxia model path. Do not re-enable fallback chains unless the user explicitly asks.
