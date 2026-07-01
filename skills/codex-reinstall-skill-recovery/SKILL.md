---
name: codex-reinstall-skill-recovery
description: "Recover and verify Codex skill packages after a Codex Desktop reinstall or migration from a backup folder. Use when the user asks to recover skill packages, restore skills from H drive or another backup, check .codex/skills and .agents/skills, perform read-only backup checks, detect conflicts, copy only missing non-conflicting skills, back up before restoring, check Codex++ residue, or generate SHA256 diff reports. Also use for Chinese requests such as \u6062\u590d\u6280\u80fd\u5305, \u4ece H \u76d8\u6062\u590d Codex \u6280\u80fd, \u68c0\u67e5\u6280\u80fd\u5305\u5907\u4efd, or \u91cd\u88c5\u540e\u63a5\u56de\u6280\u80fd."
---

# Codex Reinstall Skill Recovery

## Overview

Use this skill to safely reattach saved Codex skills after reinstalling Codex Desktop. The default posture is conservative: inspect first, preserve official new files, back up current state before copying, and never overwrite same-name skill directories unless the user explicitly asks after seeing a diff.

## Workflow

1. Confirm the backup root and current roots.
   - Default backup root: `H:\Codex_Reinstall_Skill_Backup_20260611`
   - Default current Codex skills: `C:\Users\A\.codex\skills`
   - Default current Agents skills: `C:\Users\A\.agents\skills`
   - Adjust paths when the user gives a different backup location.

2. Start read-only.
   - Check required backup files and directories.
   - Read the machine-readable index and preservation notes if present.
   - Count backup and current skill directories.
   - List same-name conflicts and non-conflicting restore candidates.
   - Check known Codex++ residue paths only by existence.

3. Restore only after user confirmation.
   - Back up current `C:\Users\A\.codex\skills`, `C:\Users\A\.agents\skills`, `config.toml`, and `.skill-lock.json` when present.
   - Copy only missing skill directories from the backup.
   - Skip existing same-name directories such as official `.system`.
   - Do not delete, move, or modify the backup.
   - Do not change auth, SQLite, plugin cache, system proxy, registry, Windows Store, or environment variables.

4. Verify after restore.
   - Recount current skills.
   - Ensure every backup skill exists in the target.
   - Generate an execution report with backup location, copied packages, skipped packages, and remaining missing packages.

5. Run hash/diff when conflicts remain.
   - Compare official `.system` and same-name Agents skills using recursive file lists and SHA256 hashes.
   - Prefer keeping the current official `.system` unless a specific old file is needed.
   - Treat `__pycache__`, `.pyc`, and other generated cache differences as usually safe to ignore.

## Scripts

Use the bundled scripts instead of rewriting long PowerShell by hand.

### `scripts/recovery_check_restore.ps1`

Performs read-only checks by default. Add `-Restore` only after user confirmation to back up current skills and copy missing non-conflicting skills.

Example read-only check:

```powershell
powershell -ExecutionPolicy Bypass -File C:\Users\A\.codex\skills\codex-reinstall-skill-recovery\scripts\recovery_check_restore.ps1
```

Example restore after confirmation:

```powershell
powershell -ExecutionPolicy Bypass -File C:\Users\A\.codex\skills\codex-reinstall-skill-recovery\scripts\recovery_check_restore.ps1 -Restore
```

Useful parameters:

- `-BackupRoot <path>`
- `-CurrentCodexSkills <path>`
- `-CurrentAgentsSkills <path>`
- `-ReportPath <path>`

### `scripts/compare_skill_hashes.ps1`

Compares `.system` and same-name Agents skill packages with recursive SHA256 hashes and writes a Markdown diff report.

Example:

```powershell
powershell -ExecutionPolicy Bypass -File C:\Users\A\.codex\skills\codex-reinstall-skill-recovery\scripts\compare_skill_hashes.ps1
```

## Reporting

Always report:

- Whether index files were read.
- Backup skill counts versus current skill counts.
- Same-name conflicts.
- Non-conflicting restore candidates.
- What was copied, skipped, or left missing.
- Backup-before-restore location.
- Any Codex++ residue found.
- Clear next action requiring user confirmation.

If a write target is outside the active workspace, ask for or use the available file-system permission path before restoring. If permission is unavailable, stop after read-only reporting.
