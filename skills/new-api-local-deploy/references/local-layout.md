# New API Local Deployment Layout

## Scope

This is the user's phase-one local AI API gateway deployment. It is meant for one-person local use on this Windows machine. The goal is to run New API first, learn the gateway, add upstream model providers, generate local tokens, and track usage before considering public access or larger platform architecture.

## Canonical Locations

${REDACTED_SECRET}
- H drive mirror: `H:\CodexSkills\new-api-local-deploy`
${REDACTED_SECRET}
- Live files:
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}

## Port Layout

Keep services separated:

- Hermes / Open WebUI: `http://localhost:3000`
- New API UI: `http://localhost:3001`
- New API Base: `http://localhost:3001/v1`
- New API console after login: `http://localhost:3001/console`

New API must use this Docker port mapping:

```yaml
ports:
  - "127.0.0.1:3001:3000"
```

Do not use `0.0.0.0`. Do not bind PostgreSQL or Redis to host ports.

## Browser Opening Rule

For user-facing viewing, open New API in real Google Chrome, not the Codex in-app browser. The user reported the in-app browser is unstable for this server page.

Preferred user-facing URL:

```text
http://localhost:3001
```

If already initialized and logged in, the console may be:

```text
http://localhost:3001/console
```

PowerShell fallback to open Chrome:

```powershell
$chromePaths = @(
  "$env:ProgramFiles\Google\Chrome\Application\chrome.exe",
  "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe",
  "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe"
)
$chrome = $chromePaths | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
if (-not $chrome) {
  $cmd = Get-Command chrome.exe -ErrorAction SilentlyContinue
  if ($cmd) { $chrome = $cmd.Source }
}
if ($chrome) { Start-Process -FilePath $chrome -ArgumentList 'http://localhost:3001' }
```

## Compose Topology

Services:

- `new-api`: `calciumion/new-api:latest`
- `postgres`: `postgres:15-alpine`
- `redis`: `redis:7-alpine`

Volumes:

- `pg_data` for PostgreSQL data
- `redis_data` for Redis data
- `./data:/data` for New API local data
- `./logs:/app/logs` for New API logs

Core environment:

```text
${REDACTED_SECRET}
REDIS_CONN_STRING=redis://:${REDIS_PASSWORD}@redis:6379
SESSION_SECRET=${SESSION_SECRET}
CRYPTO_SECRET=${CRYPTO_SECRET}
TZ=Asia/Shanghai
NODE_NAME=new-api-local
ERROR_LOG_ENABLED=true
BATCH_UPDATE_ENABLED=true
```

Required `.env` shape:

```text
POSTGRES_USER=newapi
POSTGRES_PASSWORD=<local random secret, at least 32 chars>
POSTGRES_DB=newapi
REDIS_PASSWORD=<local random secret, at least 32 chars>
SESSION_SECRET=<local random secret, at least 32 chars>
CRYPTO_SECRET=<local random secret, at least 32 chars>
TZ=Asia/Shanghai
```

Generate secrets locally. Do not print actual values in final answers.

## PowerShell Gates

G01 environment check:

```powershell
$os = Get-CimInstance Win32_OperatingSystem
docker --version
docker info --format '{{.ServerVersion}}'
docker compose version
docker ps --format 'table {{.ID}}\t{{.Names}}\t{{.Image}}\t{{.Ports}}\t{{.Status}}'
netstat -ano | Select-String -Pattern ':3001\s+.*LISTENING'
```

Success: Windows is detected, Docker daemon responds, Compose exists, and port 3001 is free or the occupant is intentionally handled.

G02 write config:

```powershell
New-Item -ItemType Directory -Path "$env:USERPROFILE\new-api-local" -Force
```

Create `docker-compose.yml`, `.env`, `README_LOCAL.md`, `data`, and `logs`.

G03 validate and start:

```powershell
Set-Location "$env:USERPROFILE\new-api-local"
docker compose config --quiet
docker compose pull
docker compose up -d
docker compose ps
```

G04 verify:

```powershell
docker compose ps
docker compose logs --tail 120 new-api
docker port new-api
docker port new-api-postgres
docker port new-api-redis
```

Expected:

- `new-api` is `Up` and preferably `healthy`.
- `new-api-postgres` is `Up` and `healthy`.
- `new-api-redis` is `Up` and `healthy`.
- New API host mapping is only `127.0.0.1:3001`.
- PostgreSQL and Redis have no host mappings.

If `Invoke-WebRequest` or `curl.exe` hangs on this machine, verify the page through the Browser skill or another browser observation. The known good state is a page titled `New API` at `/setup` with text including `系统初始化`, `PostgreSQL`, and `下一步`.

For display to the user, use Chrome even if background browser verification succeeds.

## Dashboard Balance Notes

The dashboard can show a current balance such as `$200.00` immediately after first deployment. This is not a real recharge, not upstream provider money, and not a minimum required payment.

It is New API's local internal quota accounting. It affects local gateway limits and consumption tracking after tokens start calling models. Actual money is charged by the upstream provider account connected through the user's upstream API key.

Observed first-deployment evidence from read-only PostgreSQL checks:

```sql
select id, username, role, quota, used_quota, request_count
from users
order by id;
```

Observed result:

```text
id=1
username=xya6338
role=100
quota=100000000
used_quota=0
request_count=0
```

Recharge table check:

```sql
select id, user_id, amount, money, status, payment_method, create_time, complete_time
from top_ups
order by id desc
limit 10;
```

Observed result:

```text
0 rows
```

Interpretation to give the user:

```text
The $200 dashboard balance is New API internal quota. It is not real deposited money. It is not an upstream provider balance. You can ignore the recharge button for local self-use and continue with channel setup and token creation.
```

## Failure Handling

- Docker missing or daemon unavailable: stop and ask the user to install/start Docker Desktop.
- Port 3001 occupied: identify the process/container. If it cannot be freed safely, choose the next local port such as `3002` and update README and API Base accordingly. Do not reclaim port 3000 from Hermes/Open WebUI.
- Image pull failure: retry `docker compose pull` once. If still failing, report the exact error and do not switch to an unknown image.
- New API fails: inspect `docker compose logs --tail 200 new-api`, then check `SQL_DSN`, PostgreSQL health, Redis health, `REDIS_CONN_STRING`, and `.env` interpolation.

## Login Auto Recovery

2026-05-22 installed a local logon recovery task so this chain can reconnect
after reboot/login without manual Codex repair.

Files:

${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
- Scheduled task: `HermesNewApiAutoRecover_Logon`
${REDACTED_SECRET}
- Compatibility shims for older startup/task references:
${REDACTED_SECRET}
${REDACTED_SECRET}

The compatibility shims do not restore the old WSL/OpenClaw path. They only
delegate stale Windows startup references to
`Hermes_NewAPI_AutoRecover.ps1`.

Default automatic behavior:

1. Acquire a global mutex so duplicate logon/startup launches do not overlap.
2. Start Docker Desktop if the daemon is unavailable, then wait up to 300 seconds.
3. Run `docker compose config --quiet` and `docker compose up -d` from
${REDACTED_SECRET}
4. Wait for `new-api-postgres`, `new-api-redis`, and `new-api` to be running
   and healthy.
5. Start `open-webui-clean` and wait for healthy/running.
6. Check Hermes `8642` `/health` and `/v1/models`; if unhealthy, run
   `H:\Hermes_Windows_Native_014\START-HERMES-WEBUI.cmd`.
7. Verify:
   - `http://127.0.0.1:3001` returns `200`.
   - `http://127.0.0.1:3001/v1/models` returns `401` without a token.
   - `http://127.0.0.1:8642/health` contains `hermes-agent`.
   - `http://127.0.0.1:8642/v1/models` contains `hermes-agent`.
   - `http://127.0.0.1:3000` returns `200`.
   - Telegram diagnostic script returns `Result: PASS`.
8. Write `FINAL_PASS Hermes New API Telegram auto-recovery complete` or
   `FINAL_FAIL ... incomplete` to the log.

The automatic logon run intentionally does not send Telegram messages and does
not run model chat completions, to avoid boot-time message spam or token/quota
consumption. For a manual full relay probe, run:

```powershell
${REDACTED_SECRET}
```

For a manual Telegram outbound smoke test, run:

```powershell
${REDACTED_SECRET}
```

Verify automation installation:

```powershell
Get-ScheduledTask -TaskName "HermesNewApiAutoRecover_Logon"
Test-Path "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\Hermes_NewAPI_AutoRecover.cmd"
${REDACTED_SECRET}
```

For the full post-reboot and current-state verification sequence, including
Telegram outbound smoke and a direct Hermes -> New API -> model probe, use:

```text
references/reboot-chain-verification.md
```

2026-05-22 current-state evidence to preserve:

- `Hermes_NewAPI_AutoRecover.ps1 -TelegramSmoke` exited `0`, sent Telegram
  smoke `message_id=1305`, and wrote `FINAL_PASS Hermes New API Telegram
  auto-recovery complete`.
- Direct Hermes chat via `http://127.0.0.1:8642/v1/chat/completions` returned
  HTTP `200` with marker `HERMES_E2E_OK_1804`.
- New API logs recorded `/v1/chat/completions` relay `200` and
  `record consume log`.
- Hermes `agent.log` recorded `Turn ended ... response_len=18`.
- This was not a fresh reboot proof because `LAST_BOOT` still showed
  `2026-05-22 15:50:08`; after the next real reboot, re-run the reboot-chain
  verification gates before claiming persistence.

## Post-Deployment User Steps

1. Open `http://localhost:3001` in Google Chrome.
2. Create the administrator account.
3. Enter the backend.
4. If available, set server address to `http://localhost:3001`.
5. Add upstream channels: OpenAI, Claude, Gemini, DeepSeek, Qwen, or other providers.
6. Create a New API token.
7. Configure local clients:

```text
API Base: http://localhost:3001/v1
API Key: <token created in New API>
```

Model list test:

```powershell
curl.exe http://localhost:3001/v1/models -H "Authorization: Bearer <New API token>"
```

Chat test:

```powershell
curl.exe http://localhost:3001/v1/chat/completions -H "Content-Type: application/json" -H "Authorization: Bearer <New API token>" -d "{\"model\":\"<enabled model>\",\"messages\":[{\"role\":\"user\",\"content\":\"你好，测试一下。\"}]}"
```

## Sync Procedure

After any update to this skill:

```powershell
${REDACTED_SECRET}
$dst = 'H:\CodexSkills\new-api-local-deploy'
New-Item -ItemType Directory -Path (Split-Path $dst) -Force | Out-Null
robocopy $src $dst /MIR
```

Then verify both copies:

```powershell
${REDACTED_SECRET}
$dst = 'H:\CodexSkills\new-api-local-deploy'
$srcFiles = Get-ChildItem -LiteralPath $src -Recurse -File | ForEach-Object {
  $rel = $_.FullName.Substring($src.Length).TrimStart('\')
  [PSCustomObject]@{ RelativePath = $rel; Hash = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash }
}
$dstFiles = Get-ChildItem -LiteralPath $dst -Recurse -File | ForEach-Object {
  $rel = $_.FullName.Substring($dst.Length).TrimStart('\')
  [PSCustomObject]@{ RelativePath = $rel; Hash = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash }
}
Compare-Object $srcFiles $dstFiles -Property RelativePath,Hash
```

Expected: no output from `Compare-Object`.
