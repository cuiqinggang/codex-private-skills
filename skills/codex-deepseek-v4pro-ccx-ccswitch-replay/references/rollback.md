# Rollback

## Restore Codex Config

If default Codex config was changed, restore from backup:

```powershell
Copy-Item -LiteralPath "<backup>\config.toml" -Destination "C:\Users\A\.codex\config.toml" -Force
```

Known success-run backup:

```text
C:\Users\A\Desktop\1\output\TASK-20260514-CODEX-DEEPSEEK-V4PRO-VIDEO-REPLAY\backups\20260514-172915\config.toml
```

If no backup exists, stop with `SAFE_STOP_PASS` and do not invent a replacement config.

## Stop CCX

```powershell
Get-Process | Where-Object { $_.Path -like "*ccx-windows-amd64.exe*" } | Stop-Process
```

Stopping CCX stops the backup route from consuming DeepSeek API.

## Disable Or Delete CC Switch Provider

Preferred: use CC Switch UI to disable or remove provider:

```text
DeepSeek-V4Pro-Backup-via-CCX
```

If the database must be restored, use the `.cc-switch` backup:

```text
C:\Users\A\Desktop\1\output\TASK-20260514-CODEX-DEEPSEEK-V4PRO-VIDEO-REPLAY\backups\20260514-175310\.cc-switch
```

Stop CC Switch before replacing the directory.

## Confirm Default GPT Route

```powershell
$c = Get-Content -LiteralPath "C:\Users\A\.codex\config.toml" -Raw
$c -match 'model\s*=\s*"gpt-5\.5"'
$c -match 'deepseek'
```

Expected:

- GPT-5.5 check is true.
- DeepSeek check is false in default `config.toml`.

## Confirm No DeepSeek Spend

- CCX stopped, or
- CCX channel disabled, or
- CC Switch provider disabled/removed, and
- Codex is not using the `Enter API key` backup route.

If any check is unclear, stop and report `SAFE_STOP_PASS`.
