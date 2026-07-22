# 2026-06-17 GLM5 Router Provider Mismatch

## Trigger

Use this when Hermes config says:

```yaml
model:
  provider: openrouter
  default: z-ai/glm-5-turbo
```

but Telegram complex tasks still fail with:

```text
Provider authentication failed
Authentication Fails, Your api key: ****63ed is invalid
Credential pool provider mismatch: pool=openrouter, agent=deepseek
telegram_model_router: Pro route ... model=deepseek-v4-pro
```

## Root Cause

The local Telegram router plugin was forcing complex Telegram messages to
`deepseek-v4-pro` while the runtime credential pool/default provider was
OpenRouter. That caused a DeepSeek request to carry an OpenRouter key and fail
with HTTP 401.

The root file was:

```text
${REDACTED_SECRET}
```

## Safe Fix

Do not change proxy settings, Qwen vision config, or OpenRouter key.

Back up first:

```text
${REDACTED_SECRET}
```

Patch the Telegram router so it only clears old overrides and does not force
DeepSeek Pro/Flash. Marker:

```text
GLM5_TURBO_ROUTER_NEUTRAL_PATCH_20260617
```

Restart through the normal Windows native launcher, not a bare `hermes.exe`
process, so `HERMES_HOME`, proxy environment, logs, and `gateway_state.json`
refresh correctly:

```text
H:\Hermes_Windows_Native_014\START-HERMES-WEBUI.cmd
```

## Acceptance

Required evidence:

- `config.yaml` still has `model.provider=openrouter` and
  `model.default=z-ai/glm-5-turbo`.
- Qwen vision still exists:
  `qwen/qwen3-vl-235b-a22b-instruct`.
- OpenRouter direct GLM5 test returns HTTP 200.
- Qwen3-VL direct test returns HTTP 200.
- Gateway `/v1/chat/completions` returns HTTP 200.
- Latest post-restart logs show `provider=openrouter model=z-ai/glm-5-turbo`
  and no new `telegram_model_router: Pro route ... deepseek-v4-pro`.

## 2026-06-17 Evidence

- Real listener after normal restart: PID `1848`.
- Gateway state refreshed to PID `1848`.
- Gateway reply test returned HTTP 200 in about 23.33 seconds.
- Latest API call used `provider=openrouter`, `model=z-ai/glm-5-turbo`.
- Qwen3-VL direct OpenRouter test returned HTTP 200 with
  `QWEN3_VL_PRESENT_OK`.
