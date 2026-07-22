# Failure Review: C-to-H updates and unguarded backups

## Failure mode

Active C-drive scripts and skills could still copy or mirror results to H, while some K backup routes could be enabled when C material was missing or without per-operation approval.

## Root cause

Older compatibility, reinstall, and system-evolution workflows treated H as a mirror/backup target and treated K as an optional fallback source. Later C-hotpath rules did not fully remove those executable branches.

## Durable prevention

- `C_TO_H_FORBIDDEN` blocks every legacy C-to-H updater.
- `BLOCKED_C_SOURCE_MISSING` replaces H/K fallback.
- `BACKUP_NOT_AUTHORIZED` blocks C-to-K backup unless C validation and explicit per-operation approval are both present.
- Knowledge Brain K sources are disabled for health, light, and deep sync.

## Acceptance evidence

- PowerShell parser passes for modified executable scripts.
- Legacy H sync/install entrypoints fail closed.
- C-to-K preservation scripts fail closed without both approval switches.
- No backup was performed during the repair.
