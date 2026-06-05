---
name: xiaolongxia-free-model-pool
description: Use when deploying, repairing, verifying, documenting, or updating the isolated local New API free model pool for Xiaolongxia using OpenRouter free models. Keeps the pool separate from Hermes and Open WebUI.
---

# Xiaolongxia Free Model Pool

## Purpose

Use this skill for the Xiaolongxia local free model API pool. It is a New API based local gateway for lightweight group-chat replies and daily low-cost tasks.

The pool is not the Hermes gateway. Do not connect it to Hermes, do not load Hermes messages into it, and do not modify Open WebUI for this pool unless the user explicitly starts a separate integration task.

## Fixed Local Layout

- Project directory: `C:\Users\A\xiaolongxia-free-api-local`
- UI URL: `http://localhost:3011`
- API Base: `http://localhost:3011/v1`
- New API container: `xiaolongxia-new-api`
- PostgreSQL container: `xiaolongxia-postgres`
- Redis container: `xiaolongxia-redis`
- Docker host binding: `127.0.0.1:3011:3000`
- PostgreSQL and Redis must not expose host ports.

Keep these separate:

- Hermes / Open WebUI: `http://localhost:3000`
- Old New API / desktop route: `http://localhost:3001`
- Xiaolongxia free model pool: `http://localhost:3011`

## Secret Rule

Never print API keys, New API tokens, admin passwords, or `.env` secrets.

Known local secret files:

- `C:\Users\A\xiaolongxia-free-api-local\secrets\openrouter_api_key.txt`
- `C:\Users\A\xiaolongxia-free-api-local\secrets\xiaolongxia_newapi_token.txt`
- `C:\Users\A\xiaolongxia-free-api-local\secrets\admin_username.txt`
- `C:\Users\A\xiaolongxia-free-api-local\secrets\admin_password.txt`

Only report whether these files exist and are usable.

## Current Pool Settings

- Channel name: `openrouter-free`
- Channel tag: `xiaolongxia-free-pool`
- Group: `xiaolongxia-free-pool`
- Token name: `xiaolongxia-free-token`
- Temporary primary model: `liquid/lfm-2.5-1.2b-instruct:free`
- Fallback route: `openrouter/free`

OpenRouter free models can be rate-limited. Treat 429 as a normal temporary upstream condition and try another configured free model.

Current runtime order from the 2026-05-23 expanded test:

1. `liquid/lfm-2.5-1.2b-instruct:free`
2. `baidu/cobuddy:free`
3. `google/gemma-4-31b-it:free`
4. `openai/gpt-oss-120b:free`
5. `openai/gpt-oss-20b:free`

Keep `openrouter/free` as last fallback only.

Do not call the temporary primary a permanent primary until it passes: at least 50 tests, success rate >= 90%, Chinese usable-answer rate >= 80%, no consecutive 429, no 402, acceptable average latency, and safety-boundary pass rate >= 90%.

## Safe Workflow

1. Check containers:

```powershell
docker ps --filter "name=xiaolongxia" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

2. Start or repair only this stack:

```powershell
Set-Location C:\Users\A\xiaolongxia-free-api-local
docker compose up -d
docker compose ps
```

3. Verify port isolation:

```powershell
docker port xiaolongxia-new-api
docker port xiaolongxia-postgres
docker port xiaolongxia-redis
```

Expected:

- New API: `3000/tcp -> 127.0.0.1:3011`
- PostgreSQL: no output
- Redis: no output

4. Verify HTTP:

```powershell
Invoke-WebRequest -UseBasicParsing http://127.0.0.1:3011
Invoke-RestMethod http://127.0.0.1:3011/api/status
```

5. Verify models with the local token from the secret file. Do not print the token.

6. Verify chat with the current primary order. If a model is limited or returns an empty reply, switch to the next model.

## Free Pool Operations

Model inventory:

```powershell
Set-Location C:\Users\A\xiaolongxia-free-api-local
.\scripts\update-free-model-pool.ps1
```

Outputs:

- `data\free-models-current.json`
- `data\free-models-current.md`
- `reports\daily-free-pool-YYYYMMDD-HHMMSS.md`

Model test:

```powershell
Set-Location C:\Users\A\xiaolongxia-free-api-local
.\scripts\test-free-models.ps1 -MaxModels 10
```

Expanded model test:

```powershell
Set-Location C:\Users\A\xiaolongxia-free-api-local
.\scripts\test-free-models-expanded.ps1
```

Model count difference:

```powershell
# See latest reports\model-count-diff-*.md
```

Xiaolongxia call simulation without OpenClaw:

```powershell
Set-Location C:\Users\A\xiaolongxia-free-api-local
.\scripts\simulate-xiaolongxia-chat-call.ps1
```

Daily lightweight maintenance:

```powershell
Set-Location C:\Users\A\xiaolongxia-free-api-local
.\scripts\update-free-model-pool.ps1 -RunLightTest -LightTestMaxModels 5
```

Policy files:

- `config\xiaolongxia-free-routing-policy.md`
- `config\xiaolongxia-rate-limit-policy.md`
- `reports\daily-free-pool-template.md`

Use these files to decide whether a model is suitable for Xiaolongxia:

- It is a text model.
- It has zero pricing or an explicit `:free` suffix.
- It is configured in local New API or is intentionally added after backup.
- It passes the Chinese phrase-following smoke test.
- It is not currently in 429/402 cooldown.
- It has acceptable latency for group chat.

## Error Handling

- 429: temporary upstream free-tier rate limit. Cool down 10 to 30 minutes and switch model.
- 402: upstream payment/BYOK/credit block. Stop the free pool route and report quota/balance state; do not keep cycling models blindly.
- 5xx: cool down 10 minutes.
- Timeout: cool down 5 minutes.
- Empty reply: count as failure and switch.
- Three consecutive 5xx or empty replies: switch to next model and cool down the failed model.

## Database Change Rule

Before changing channels, tokens, users, options, or model abilities, create a PostgreSQL backup under:

`C:\Users\A\Desktop\1\output\<task-id>\backups`

Use the isolated container only:

```powershell
docker exec xiaolongxia-postgres pg_dump -U newapi -d newapi
```

Do not dump or alter the old `new-api-postgres` container unless the task is explicitly about the old New API service.

## Xiaolongxia Client Handoff

Give Xiaolongxia:

```text
API Base: http://localhost:3011/v1
API Key: value stored in C:\Users\A\xiaolongxia-free-api-local\secrets\xiaolongxia_newapi_token.txt
Temporary primary model: liquid/lfm-2.5-1.2b-instruct:free
Fallback model: openrouter/free
Pool/group: xiaolongxia-free-pool
```

Recommended runtime limits:

- Reply only when explicitly addressed.
- Same group: 1 reply per 10 seconds.
- Same user: 1 reply per 30 seconds.
- Global: 10 replies per minute.
- Enforce a daily cap in the Xiaolongxia app.
- Default daily cap: 300 requests.
- Hard maximum daily cap: 800 requests.
- For medical, legal, finance, account, password, command execution, or private-data topics, give general guidance or escalate.

## Completion Criteria

Only report success when all are true:

- `xiaolongxia-new-api`, `xiaolongxia-postgres`, and `xiaolongxia-redis` are running.
- New API is healthy or `/api/status` succeeds.
- UI root `http://localhost:3011` returns HTTP 200.
- `/v1/models` returns configured free models using the Xiaolongxia token.
- A simple chat completion succeeds through the pool.
- `data\free-models-current.json` and `.md` exist after inventory update.
- Latest `reports\free-model-test-*.md` records at least 5 tested models.
- Latest `reports\free-model-test-expanded-*.md` records multi-scenario tests.
- Latest `reports\xiaolongxia-call-simulation-*.md` proves trigger, cooldown, and fallback behavior without OpenClaw.
- No secrets are printed.
- Hermes and Open WebUI are untouched.
