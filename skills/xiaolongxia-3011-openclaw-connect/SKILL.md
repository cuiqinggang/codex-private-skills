---
name: xiaolongxia-3011-openclaw-connect
description: Use when connecting, verifying, repairing, or documenting the Windows-side OpenClaw / Xiaolongxia integration with the isolated local 3011 New API free model pool. Includes provider configuration, model allowlist, smoke tests, fallback policy, rate-limit placement, rollback, and strict isolation from Hermes, Open WebUI, old 3001 New API, and real group chat entrances.
metadata:
  short-description: OpenClaw to Xiaolongxia 3011 free model pool
---

# Xiaolongxia 3011 OpenClaw Connect

Use this skill for the Windows-only OpenClaw / Xiaolongxia connection to the isolated local free model pool.

## Fixed Boundaries

- Do not modify Hermes / 爱马仕.
- Do not modify Open WebUI.
- Do not modify the old `3001` New API.
- Do not use WSL as a prerequisite.
- Do not connect real Feishu, WeChat, Telegram, or other group chat entrances.
- Do not direct-connect Google / Gemini.
- Do not write OpenRouter raw keys.
- Do not print token, password, admin account, or secret file contents.
- Do not expose OpenClaw publicly; keep gateway on loopback.

## Current Verified Layout

- OpenClaw command: `C:\Users\A\AppData\Roaming\npm\openclaw.cmd`
- OpenClaw state: `C:\Users\A\.openclaw`
- OpenClaw config: `C:\Users\A\.openclaw\openclaw.json`
- Gateway port: `127.0.0.1:18789`
- Free pool management UI only: `http://localhost:3011`
- Free pool API Base: `http://localhost:3011/v1`
- Xiaolongxia New API token file: `C:\Users\A\xiaolongxia-free-api-local\secrets\xiaolongxia_newapi_token.txt`
- Provider id: `xiaolongxia-free`

OpenClaw may write an agent-level provider snapshot at `C:\Users\A\.openclaw\agents\main\agent\models.json`. The expected token marker there is `secretref-managed`, not a real token.

## 2026-05-24 Safety Incident: 3011 Is Not Xiaolongxia UI

On 2026-05-24, a Xiaolongxia autostart/browser-open attempt mistakenly treated `http://localhost:3011` as the Xiaolongxia product UI and the user observed Hermes/AiMaShi being opened. This is an isolation failure pattern.

Rules after the incident:

- Before any Xiaolongxia/OpenClaw/browser recovery, run `G00-NewAPI-Start-And-Login`: independently open and log in to `http://127.0.0.1:3011`, read-only confirm a New API backend page, and write `3011_CONFIRMED_AS_NEW_API_NOT_XIAOLONGXIA_UI`.
- Latest G00 savepoint on 2026-05-24 passed. Admin username is `xya6338`; password is stored only at `C:\Users\A\xiaolongxia-free-api-local\secrets\newapi_admin_xya6338_login.txt`. Do not print the password.
- Latest G00 evidence root: `C:\Users\A\Desktop\1\output\XIAOLONGXIA-G00-NEWAPI-START-LOGIN-20260524`.
- `3011` is New API/model-pool management, not Xiaolongxia product UI and not OpenClaw browser UI.
- Do not build or run Xiaolongxia browser autostart around `3011`.
- `18798` is not trusted unless a fresh readonly check proves it is listening and belongs to Xiaolongxia.
- OpenClaw manual gateway/browser recovery uses `http://127.0.0.1:18789/` after health and identity checks.
- If Hermes/AiMaShi opens during a Xiaolongxia task, stop immediately. Disable `Xiaolongxia_Autostart_Logon`, keep `C:\Users\A\Xiaolongxia_AutoStart` scripts disabled, and do not continue browser testing.
- For the full rollback and recovery runbook, use `xiaolongxia-openclaw-gateway-safety-recovery`.

## Model Route

Primary:

- `xiaolongxia-free/liquid/lfm-2.5-1.2b-instruct:free`

Formal backup order after per-model evidence on 2026-05-23:

1. `xiaolongxia-free/openai/gpt-oss-120b:free`
2. `xiaolongxia-free/openai/gpt-oss-20b:free`

Candidate-only models:

- `xiaolongxia-free/baidu/cobuddy:free`: command succeeded, but it did not return the required `MODEL_BAIDU_OK` marker in the 2026-05-23 per-model evidence run. Do not keep it in the formal backup list until a later per-model marker test passes.
- `xiaolongxia-free/google/gemma-4-31b-it:free`: returned 429 in the 2026-05-23 per-model evidence run. Current status is `UNAVAILABLE_OR_LIMITED`.

Final fallback only:

- `xiaolongxia-free/openrouter/free`

`openrouter/free` passed its marker test, but it is still only the last fallback because it is a changing free route, not a deterministic model. Do not let it replace a named model in the formal backup list.

Gemma image support is not verified. Do not claim image support unless a later image smoke test passes through OpenClaw -> 3011 -> OpenRouter.

## Provider Shape

Use `models.providers.xiaolongxia-free` in `openclaw.json`:

```json
{
  "baseUrl": "http://localhost:3011/v1",
  "api": "openai-completions",
  "auth": "api-key",
  "authHeader": true,
  "apiKey": { "source": "file", "provider": "xiaolongxia-free-token", "id": "value" },
  "timeoutSeconds": 60,
  "request": { "allowPrivateNetwork": true }
}
```

Every free model entry should be text-only and disable tools:

```json
{
  "input": ["text"],
  "compat": {
    "supportsTools": false,
    "requiresStringContent": true,
    "strictMessageKeys": true
  }
}
```

## Verification Commands

Preflight:

```powershell
openclaw --version
openclaw config validate
docker ps --filter "name=xiaolongxia" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
Get-NetTCPConnection -LocalPort 18789 -ErrorAction SilentlyContinue
```

Gateway health:

```powershell
openclaw gateway health --json --timeout 20000
```

Strict smoke test:

```powershell
openclaw infer model run --gateway --model "xiaolongxia-free/liquid/lfm-2.5-1.2b-instruct:free" --prompt "请只回复：XIAOLONGXIA_3011_MODEL_OK" --json
```

Gemma text smoke:

```powershell
openclaw infer model run --gateway --model "xiaolongxia-free/google/gemma-4-31b-it:free" --prompt "请只回复：GEMMA_OPENROUTER_TEXT_OK" --json
```

Use `openclaw infer model run --gateway` for strict model probes. The OpenClaw `/v1/chat/completions` HTTP surface treats the OpenAI `model` field as an agent target; backend model overrides require `x-openclaw-model`, so it is less reliable for exact marker probes.

## Fallback Placement

OpenClaw can call each provider/model, but deterministic fallback switching belongs in the Xiaolongxia application layer or message adapter. Treat the free pool as a model-call backend, not the group policy brain.

Switch on:

- 429: cool down current model for 10-30 minutes.
- 402: stop the free pool route and report quota/balance/BYOK issue.
- 5xx, timeout, empty reply: switch after 3 consecutive failures.
- model-not-found or access denied: immediately switch to the next verified model.

## Rate Limits

Implement these in the Xiaolongxia message adapter, not inside OpenClaw:

- Same group: one reply per 10 seconds.
- Same user: one reply per 30 seconds.
- Global: at most 10 replies per minute.
- Daily default: 300 requests.
- Daily hard max: 800 requests.
- Only respond to `@小龙虾` or explicit trigger words by default.

## Rollback

Before modifying OpenClaw:

1. Back up `C:\Users\A\.openclaw`.
2. Back up `C:\Users\A\.openclaw\openclaw.json`.
3. Back up `C:\Users\A\.openclaw\agents\main\agent\models.json` if present.

Rollback:

1. Stop the `127.0.0.1:18789` listener if it is OpenClaw/node.
2. Restore the backed-up config files.
3. Run `openclaw config validate`.
4. Start the gateway again on loopback only.

## Latest Replay Evidence

Successful replay output root:

`C:\Users\A\Desktop\1\output\OPENCLAW-XIAOLONGXIA-3011-MATURE-REPLAY-20260523`

Per-model evidence output root:

`C:\Users\A\Desktop\1\output\OPENCLAW-XIAOLONGXIA-3011-MODEL-EVIDENCE-20260523`

Latest status:

`XIAOLONGXIA_3011_MODEL_EVIDENCE_REDUCED_PASS`

Per-model marker results:

- `liquid/lfm-2.5-1.2b-instruct:free`: pass, formal primary.
- `openai/gpt-oss-120b:free`: pass, formal backup.
- `openai/gpt-oss-20b:free`: pass, formal backup.
- `baidu/cobuddy:free`: failed marker, candidate only.
- `google/gemma-4-31b-it:free`: 429, `UNAVAILABLE_OR_LIMITED`, candidate only.
- `openrouter/free`: pass, final fallback only.

Fallback still belongs in the Xiaolongxia application layer or message adapter. OpenClaw provides the provider/model call path.

Important files:

- `G08-smoke-test.md`
- `G09-normal-scenarios.md`
- `G10-fallback-switch.md`
- `G11-gemma-availability.md`
- `G12-error-handling.md`
- `G13-rate-limit.md`
- `G14-stability.md`
- `final-report.md`
- `model-evidence.md`
- `model-evidence.json`

## Latest G00 New API Login Evidence

Output root:

`C:\Users\A\Desktop\1\output\XIAOLONGXIA-G00-NEWAPI-START-LOGIN-20260524`

Latest status:

`G00_NEWAPI_START_AND_LOGIN_PASS`

Required marker:

`3011_CONFIRMED_AS_NEW_API_NOT_XIAOLONGXIA_UI`

Confirmed:

- `3011` is New API / model-pool management, not Xiaolongxia UI.
- Login as admin `xya6338` succeeded.
- Password is stored only at `C:\Users\A\xiaolongxia-free-api-local\secrets\newapi_admin_xya6338_login.txt`.
- Dashboard, Channels, Models, Tokens, and Settings pages were reachable.
- Channel page showed `openrouter-free`, group `xiaolongxia-free-pool`, type `OpenRouter`, status enabled.
- No channel/model/token/group/route production configuration was modified.

Use `xiaolongxia-openclaw-gateway-safety-recovery` and its `references/g00-newapi-start-login-20260524.md` for the detailed runbook and evidence file list.
