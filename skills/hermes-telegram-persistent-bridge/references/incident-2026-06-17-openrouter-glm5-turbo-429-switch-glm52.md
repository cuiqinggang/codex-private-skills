# 2026-06-17 OpenRouter GLM-5-Turbo 429 Switch to GLM-5.2

## Trigger

Use this when Telegram or API Server reaches Hermes successfully, but the
reply says:

```text
The model provider is rate-limiting requests. Please wait a moment and try again.
```

and logs show:

```text
provider=openrouter model=z-ai/glm-5-turbo
HTTP 429
z-ai/glm-5-turbo is temporarily rate-limited upstream
provider_name=AtlasCloud
```

## Boundary

Do not change Windows proxy, FlClash, Telegram proxy, Telegram login state,
OpenRouter key, or Qwen vision config.

## Root Cause

Hermes, Telegram, and `127.0.0.1:8642` can all be healthy while the selected
OpenRouter upstream model is temporarily rate-limited. In this incident the
blocked model was `z-ai/glm-5-turbo`; the failure was upstream 429, not a local
Gateway failure.

## Safe Fix

1. Run the normal Hermes Telegram diagnostic.
2. Confirm `gateway.log` has Telegram inbound plus `response ready`.
3. Confirm `agent.log` has OpenRouter 429 for the active model.
4. Probe nearby Z.ai/OpenRouter models without printing secrets.
5. Back up `C:\Users\A\.hermes\config.yaml` and `.env`.
6. If the user agrees, switch only:
   ```yaml
   model:
     provider: openrouter
     default: z-ai/glm-5.2
   ```
7. Restart via the normal Windows native launcher:
   ```text
   H:\Hermes_Windows_Native_014\START-HERMES-WEBUI.cmd
   ```

## Acceptance

- Diagnostic script returns PASS.
- `gateway_state.json` shows Telegram and API Server connected.
- A real listener exists on `127.0.0.1:8642`.
- New `agent.log` lines show:
  ```text
  provider=openrouter model=z-ai/glm-5.2
  ```
- No new 429 appears for the post-switch test.
- Real Telegram inbound gets a new `response ready`.
- API Server call with the local API key returns HTTP 200.
- Qwen vision remains:
  ```text
  qwen/qwen3-vl-235b-a22b-instruct
  ```

## 2026-06-17 Evidence

- Backup created:
  `C:\Users\A\.hermes\backups\codex-openrouter-rate-limit-20260617-192703`
- Gateway restarted; new listener PID was `29204`.
- Diagnostic returned PASS.
- Telegram post-switch test used `model=z-ai/glm-5.2` and completed in about
  21.3 seconds with `response ready`.
- API Server authenticated test returned HTTP 200.
- Direct OpenRouter GLM-5.2 probe returned HTTP 200.
