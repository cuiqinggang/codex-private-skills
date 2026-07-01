# Incident 2026-06-01 - Hermes 0.15.2 Upgrade Repair

Use this note when a Windows native Hermes upgrade appears stuck, `hermes.exe`
is present but commands fail, 8642 is down, or Telegram stopped after a Hermes
upgrade.

## Symptoms

- `H:\Hermes_Windows_Native_014\venv\Scripts\hermes.exe --version` failed with
  `ModuleNotFoundError: No module named 'hermes_cli.main'`.
- `pip list` showed `WARNING: Ignoring invalid distribution ~ermes-agent`.
- 8642 was not listening, while Open WebUI on 3000 was still available.
- Telegram config/state files still existed, but gateway status failed because
  the Hermes CLI entrypoint was broken.
- After reinstalling 0.15.2, the API server refused to start until
  `API_SERVER_KEY` was set.
- After setting `API_SERVER_KEY`, the old launcher still failed because it
  checked `/v1/models` without `Authorization: Bearer <API_SERVER_KEY>`.

## Repair Order

1. Capture baseline before changing anything:

```powershell
Get-Process hermes -ErrorAction SilentlyContinue
Get-NetTCPConnection -LocalPort 8642,3000,3001 -ErrorAction SilentlyContinue
& "H:\Hermes_Windows_Native_014\venv\Scripts\hermes.exe" --version
& "H:\Hermes_Windows_Native_014\venv\Scripts\hermes.exe" gateway status --deep
powershell -NoProfile -ExecutionPolicy Bypass -File "C:\Users\A\.codex\skills\windows-hermes-operations\scripts\check_windows_hermes_health.ps1"
powershell -NoProfile -ExecutionPolicy Bypass -File "C:\Users\A\.codex\skills\hermes-telegram-persistent-bridge\scripts\check-hermes-telegram.ps1"
```

2. Back up mutable profile/state/log evidence under
   `C:\Users\A\Desktop\1\output\hermes-015-repair-<timestamp>`:

```powershell
C:\Users\A\.hermes\.env
C:\Users\A\.hermes\config.yaml
C:\Users\A\.hermes\gateway_state.json
C:\Users\A\.hermes\channel_directory.json
C:\Users\A\.hermes\logs\*.log
H:\Hermes_Windows_Native_014\reports\daily-start-*.log
```

3. Repair the venv in place:

```powershell
& "H:\Hermes_Windows_Native_014\venv\Scripts\python.exe" -m pip install --no-input --upgrade --force-reinstall "hermes-agent[messaging]==0.15.2"
& "H:\Hermes_Windows_Native_014\venv\Scripts\hermes.exe" --version
```

Expected version:

```text
Hermes Agent v0.15.2 (2026.5.29.2)
```

4. If stderr says `API_SERVER_KEY is required`, add a new random local bearer
   token to `C:\Users\A\.hermes\.env`. Do not print the token.

```powershell
$bytes = New-Object byte[] 32
$rng = [System.Security.Cryptography.RNGCryptoServiceProvider]::Create()
try { $rng.GetBytes($bytes) } finally { $rng.Dispose() }
$key = ($bytes | ForEach-Object { $_.ToString('x2') }) -join ''
```

Set or append:

```text
API_SERVER_KEY=<generated-hex-secret>
```

5. Update any local launcher or healthcheck that calls 8642 so that `/v1/models`
   and other API endpoints include:

```powershell
@{ Authorization = "Bearer $ApiServerKey" }
```

`/health` may return 200 without auth in some builds, but `/v1/models` requires
the bearer token on 0.15.2.

6. Start with the existing mature launcher:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "H:\Hermes_Windows_Native_014\launcher\start-hermes-openwebui.ps1" -NoOpen
```

Expected log:

```text
FINAL_PASS Windows native Hermes page is ready
```

7. Verify Hermes directly:

```powershell
$key = (Get-Content -LiteralPath "C:\Users\A\.hermes\.env" | Where-Object { $_ -match "^API_SERVER_KEY=" } | Select-Object -First 1) -replace "^API_SERVER_KEY=", ""
$headers = @{ Authorization = "Bearer $key" }
Invoke-WebRequest -Uri "http://127.0.0.1:8642/health" -UseBasicParsing -TimeoutSec 10 -Headers $headers
Invoke-WebRequest -Uri "http://127.0.0.1:8642/v1/models" -UseBasicParsing -TimeoutSec 20 -Headers $headers
```

8. Verify actual chat, not only ports:

```powershell
$headers = @{ Authorization = "Bearer $key"; "Content-Type" = "application/json" }
$body = @{ model = "hermes-agent"; messages = @(@{ role = "user"; content = "Reply with exactly HERMES015_PASS." }); stream = $false } | ConvertTo-Json -Depth 6
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8642/v1/chat/completions" -Headers $headers -Body $body -TimeoutSec 180
```

Expected assistant content:

```text
HERMES015_PASS
```

## Telegram Recovery After 0.15.2

After Hermes is healthy, use `hermes-telegram-persistent-bridge` and verify:

- `gateway_state.json` has `api_server=connected` and `telegram=connected`.
- `gateway.log` includes `Connected to Telegram (polling mode)`.
- Telegram `getWebhookInfo.url` is empty for polling mode.
- Bot API `sendMessage` succeeds to home chat `6164003953`.
- An inbound Telegram message produces `response ready` and `Sending response`
  in `C:\Users\A\.hermes\logs\gateway.log`.

If using the Startup-folder fallback, ensure
`C:\Users\A\.hermes\gateway-service\Hermes_Gateway.cmd` and the copy under the
user Startup folder set:

```cmd
set "HTTPS_PROXY=http://127.0.0.1:7890"
set "HTTP_PROXY=http://127.0.0.1:7890"
set "ALL_PROXY=http://127.0.0.1:7890"
```

## Successful Evidence From 2026-06-01

- `hermes --version`: `Hermes Agent v0.15.2 (2026.5.29.2)`.
- `start-hermes-openwebui.ps1 -NoOpen`: `FINAL_PASS Windows native Hermes page is ready`.
- `check_windows_hermes_health.ps1`: `WINDOWS_HERMES_HEALTHCHECK_PASS`.
- `check-hermes-telegram.ps1`: `Result: PASS`.
- Direct chat response: `HERMES015_PASS`.
- `pip check`: `No broken requirements found`.

## Residual Note

The venv may still contain old `~*` pip-uninstall residue directories, including
`~ermes_agent-0.14.0.dist-info`. If `pip check` passes and Hermes/Telegram
runtime checks pass, do not delete those directories during emergency recovery.
Treat cleanup as a separate explicit task.
