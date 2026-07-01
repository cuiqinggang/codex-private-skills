# Successful Case 2026-06-11

This case preserved skills, removed broken old Codex state, handled Codex++ residue, reinstalled official Codex, and prepared safe restoration.

## Preserved Data

- `C:\Users\A\.codex\skills` contained 66 skill packages.
- `C:\Users\A\.agents\skills` contained 31 skill packages.
- Backup root: `H:\Codex_Reinstall_Skill_Backup_20260611`.
- Backup outputs included `codex-skills`, `agents-skills`, `copy-log.tsv`, preservation notes, and a machine-readable index.
- Total preserved skill packages: 97.

## Deletion Finding

PowerShell `Remove-Item -Recurse -Force "$env:USERPROFILE\.codex"` failed because of `node_modules`, `.pnpm`, long path residue, and directory-not-empty errors.

Successful fallback:

```powershell
cmd /c rmdir /s /q "%USERPROFILE%\.codex"
Test-Path "$env:USERPROFILE\.codex"
```

Verification returned `False`.

## Codex++ Finding

`winget list Codex` showed `Codex++ ARP\User\X64\CodexPlusPlus 1.2.4`. The uninstall path could launch `codex-plus-plus-manager.exe` instead of a real uninstaller. The safe response is to stop repeated uninstall attempts, list residue, and ask before forced cleanup.

## Store Finding

Official reinstall through Microsoft Store / winget could stall at 22% or 24%, or show initialization failure. Recovery path: `wsreset`, Store repair/reset, service checks, proxy/TUN review, Store/DesktopAppInstaller re-registration, then retry official install.

## Post-Reinstall Result

- H-drive `codex-skills`: 66, intact.
- H-drive `agents-skills`: 31, intact.
- Current `.codex\skills`: 1, `.system`.
- Current `.agents\skills`: 32, including restored/known skills plus `learned`.
- Codex++ install folders and shortcuts were not found.
- 65 custom Codex skills were safe restore candidates.
- `.system` must not be overwritten.
- Agents skills must be diffed before overwrite.
