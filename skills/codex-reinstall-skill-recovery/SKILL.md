---
name: codex-reinstall-skill-recovery
description: "Recover and verify Codex skill packages after a Codex Desktop reinstall or migration from a backup folder. Use when the user explicitly asks to recover Codex skill packages after a reinstall or migration from an approved K-drive backup or another specified backup root; inspect first, detect conflicts, copy only missing non-conflicting skills, preserve current C-drive skills, and produce SHA256 diff evidence. Do not use H as an active or recovery source."
---

# Codex Reinstall Skill Recovery

## Overview

Use this skill to safely reattach saved Codex skills after reinstalling Codex Desktop. The default posture is conservative: inspect first, preserve official new files, back up current state before copying, and never overwrite same-name skill directories unless the user explicitly asks after seeing a diff.

## Workflow

1. Confirm the backup root and current roots.
   - Backup root: require the user to specify an approved backup under `K:\AI\backups`; never infer H as the source.
${REDACTED_SECRET}
${REDACTED_SECRET}
   - Adjust paths when the user gives a different backup location.

2. Start read-only.
   - Check required backup files and directories.
   - Read the machine-readable index and preservation notes if present.
   - Count backup and current skill directories.
   - List same-name conflicts and non-conflicting restore candidates.
   - Check known Codex++ residue paths only by existence.

3. Restore only after user confirmation.
${REDACTED_SECRET}
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
${REDACTED_SECRET}
```

Example restore after confirmation:

```powershell
${REDACTED_SECRET}
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
${REDACTED_SECRET}
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
