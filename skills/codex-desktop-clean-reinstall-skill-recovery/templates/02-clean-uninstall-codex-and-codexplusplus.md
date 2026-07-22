# Clean Old Codex And Codex++

Goal: remove broken local state only after preservation and confirmation.

## Read-Only First

- Run `winget list Codex`.
- Check Codex++ paths:
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
- Check desktop/start-menu shortcuts containing Codex++.
- Query uninstall registry entries.

## Process Stop Template

```powershell
Get-Process | Where-Object {
    $_.ProcessName -match "codex|Codex|plus|Plus|node|npm|pnpm"
} | Stop-Process -Force -ErrorAction SilentlyContinue
```

Run this only when cleanup is confirmed.

## `.codex` Deletion

Try normal deletion only after backup and confirmation. If PowerShell fails due to `node_modules`, `.pnpm`, long paths, missing path parts, or directory-not-empty errors:

```powershell
cmd /c rmdir /s /q "%USERPROFILE%\.codex"
Test-Path "$env:USERPROFILE\.codex"
```

Expected verification after successful deletion: `False`.

## Codex++ Abnormal Uninstall

If `winget uninstall` launches `codex-plus-plus-manager.exe` and no uninstall button exists:

1. Record "Codex++ uninstall manager abnormality".
2. Stop repeated attempts.
3. List install folders, registry entries, shortcuts, and running processes.
4. Generate a forced-clean plan.
5. Wait for user confirmation before deleting anything.

Do not delete project folders.
