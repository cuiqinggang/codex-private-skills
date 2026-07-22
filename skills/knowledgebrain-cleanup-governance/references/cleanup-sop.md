# Cleanup SOP

## Purpose

Use this SOP to move bulky but valuable material out of daily Knowledge Brain paths while preserving recoverability.

## Standard Roots

Cold archive:

```text
K:\AI\_COLD_ARCHIVE\knowledgebrain-cleanup-YYYYMMDD\
```

Rebuildable quarantine:

```text
K:\AI\_QUARANTINE_REBUILDABLE\knowledgebrain-cleanup-YYYYMMDD\
```

## Manifest Fields

Use CSV with these columns:

```text
move_id,classification,source_path,target_path,bytes,file_count,latest_write_time,reason,status,rollback_command
```

Statuses:

- `PLANNED`
- `MOVED`
- `SKIPPED_ACTIVE_RECENT`
- `SKIPPED_CORE_FILE`
- `SKIPPED_NOT_FOUND`
- `SKIPPED_AMBIGUOUS`
- `SKIPPED_GIT_METADATA`
- `SKIPPED_PARENT_PLANNED`
- `SKIPPED_TARGET_EXISTS`
- `ERROR_MOVE_FAILED`

## What To Move

Move to cold archive:

- old screenshots
- old evidence
- old reports
- old outputs
- old media files
- old zip or delivery packages
- inactive video/image generation workspaces
- skill package asset folders that are not required at runtime

Move to rebuildable quarantine:

- `node_modules`
- `dist`
- `build`
- `.cache`
- `__pycache__`
- `tmp`
- `temp`
- `logs`

## What To Keep

Never move automatically:

- `SKILL.md`
- `README.md`
- `INDEX.md`
- `ROUTING_MAP.md`
- `sync_policy.json`
- `sync_manifest.json`
- `*.ps1` tools unless explicitly archiving a whole inactive tool package
- `.git`
- active skill roots
- current project roots
- Obsidian note bodies
- files modified in the last 24 hours

## Skill Slimming

For skill packages, move only bulky subdirectories such as:

- `assets`
- `evidence`
- `screenshots`
- `visual-evidence`
- `original-video`
- `original-package`
- `video_keyframes`
- `reports\creation-*`
- `90-ARCHIVE`
- `backups`

After moving skill assets, write `ARCHIVED_ASSETS_POINTER.md` inside the skill root with:

- archive target
- manifest path
- moved source paths
- rollback instruction

## Obsidian Cleanup

Do not move note bodies. Move only bulky attachments/evidence such as:

- `05_EVIDENCE_REPORTS`
- `screenshots`
- `assets`
- `backups`

Write an Obsidian pointer note under:

```text
K:\AI\obsidian-vaults\AI-COMPANY-KNOWLEDGE-OS\01_META
```

## Long Path Fallback

If preserving the full relative path exceeds Windows path handling limits:

1. Stop trying the same long target.
2. Move the residual to `LONGPATH_RESIDUAL` under the same archive root.
3. Write a mapping note with original source, fallback target, reason, and rollback command.
4. Mention this in the final report.

## Final Report Checklist

The final report must include:

- why cleanup was continued
- pre-cleanup problem summary
- moved paths and destinations
- cold archive count and size
- rebuildable quarantine count and size
- skipped paths and reasons
- manifest path
- supplemental manifest path, if any
- rollback method
- before/after audit comparison
- health check result
- two light sync results
- final status: `PASS_CLEANED` or `PASS_CLEANED_WITH_SKIPS`
