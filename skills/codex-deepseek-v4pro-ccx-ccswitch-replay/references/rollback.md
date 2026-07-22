# Rollback

## Restore Codex Config

If default Codex config was changed, restore from backup:

```powershell
${REDACTED_SECRET}
```

Known success-run backup:

```text
${REDACTED_SECRET}
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
${REDACTED_SECRET}
```

Stop CC Switch before replacing the directory.

## Confirm Default GPT Route

```powershell
${REDACTED_SECRET}
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
