# Replay Checklist

## G01 Check Default GPT Route

- Target: confirm the main Codex route is untouched.
- Location: PowerShell.
- Command:

```powershell
$c = Get-Content -LiteralPath "C:\Users\A\.codex\config.toml" -Raw
$c -match 'model\s*=\s*"gpt-5\.5"'
$c -match 'superpowers'
```

- Success: model is GPT-5.5 and Superpowers is present.
- Failure: missing file, model changed, or Superpowers missing.
- Recovery: restore `config.toml` backup before continuing.
- Continue: only on success.

## G02 Check Ports 3000 And 13000

- Target: preserve Open WebUI and reserve CCX port.
- Location: PowerShell.
- Command:

```powershell
netstat -ano | Select-String -Pattern ':3000\s|:13000\s'
```

- Success: `3000` may be occupied by Open WebUI; `13000` is free or used by CCX.
- Failure: `13000` used by unrelated process.
- Recovery: use `13001` or `13002`, then update every URL consistently.
- Continue: only after a valid CCX port is chosen.

## G03 Check Or Start CCX

- Target: run CCX/API Proxy.
- Location: CCX tool directory.
- Command:

```powershell
Start-Process -FilePath ".\ccx-windows-amd64.exe" -WorkingDirectory "." -WindowStyle Hidden
```

- Success: `http://localhost:13000/health` responds.
- Failure: process exits or port is wrong.
- Recovery: inspect `.env`, set `PORT=13000`, keep `ENABLE_WEB_UI=true`.
- Continue: only on health response.

## G04 Configure DeepSeek V4 Pro

- Target: configure a CCX Responses channel.
- Location: CCX web UI or admin API.
- Operation:
  - Channel name: `DeepSeek-V4Pro-Backup-via-CCX`
  - Service type: OpenAI-compatible upstream for Responses channel
  - Base URL: `https://api.deepseek.com`
  - Model: `deepseek-v4-pro`
  - Do not add DeepSeek Flash.
- Success: channel appears and upstream ping is healthy.
- Failure: missing DeepSeek key, upstream 401, unsupported Responses channel.
- Recovery: if key missing, output `NEED_DEEPSEEK_API_KEY`; otherwise diagnose upstream.
- Continue: only when ping is healthy.

## G05 Check Or Start CC Switch

- Target: open CC Switch.
- Location: extracted CC Switch directory.
- Command:

```powershell
Start-Process -FilePath ".\cc-switch.exe" -WorkingDirectory "."
```

- Success: CC Switch opens and `C:\Users\A\.cc-switch\cc-switch.db` exists.
- Failure: portable zip cannot run.
- Recovery: use official v3.14.1 MSI administrative extraction.
- Continue: only when CC Switch database exists.

## G06 Configure Backup Provider

- Target: add backup Codex provider without enabling it as default.
- Location: CC Switch UI.
- Fields:
  - App: Codex
  - Name: `DeepSeek-V4Pro-Backup-via-CCX`
  - API URL: `http://localhost:13000/v1`
  - Model: `deepseek-v4-pro`
  - API key: CCX proxy access key, not DeepSeek official key
  - Current/default: no
- Success: provider exists and is backup-only.
- Failure: provider cannot be saved or writes over default provider.
- Recovery: restore `C:\Users\A\.cc-switch` backup and retry.
- Continue: only when default provider remains GPT.

## G07 Verify Health

- Target: verify CCX service.
- Location: PowerShell.
- Command:

```powershell
Invoke-RestMethod -Uri "http://localhost:13000/health"
```

- Success: status is healthy.
- Failure: no response or unhealthy.
- Recovery: restart CCX and inspect `.env`.
- Continue: only on healthy.

## G08 Verify Responses

- Target: verify CCX Responses route.
- Location: PowerShell.
- Command: use `scripts\verify-deepseek-v4pro-backup.ps1`.
- Success: output includes `DEEPSEEK_V4PRO_CODEX_BACKUP_OK`.
- Failure: reports DeepSeek, CCX, auth, or Responses layer.
- Recovery: fix the reported layer only.
- Continue: only on exact marker.

## G09 Verify Codex Exec

- Target: prove Codex can use the backup route without editing default config.
- Location: PowerShell.
- Command: see `references/verification.md`.
- Success: exit code `0` and exact marker.
- Failure: Codex provider/auth/Responses compatibility.
- Recovery: do not edit default GPT config; fix temporary provider settings first.
- Continue: only on exact marker.

## G10 Report

- Target: report `PASS` or `SAFE_STOP_PASS`.
- Success: all verification passed and default GPT route is unchanged.
- Safe stop: missing key, missing component, unsupported CCX/CC Switch, or verification failure without config damage.
- Failure: default GPT changed, Flash added, key leaked, or success claimed without evidence.
