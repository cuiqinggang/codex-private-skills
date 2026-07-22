---
name: windows-c-drive-clone-cleanup
description: Use when the user wants to scan, slim, or safely clean Windows C drive before cloning/migrating a system disk to SSD, especially when preserving useful files matters.
---

# Windows C Drive Clone Cleanup

## Trigger

Use this skill when the user says things like:

- C盘清理
- 系统盘清理
- 系统盘克隆到固态
- 机械硬盘迁移到 SSD
- 克隆前瘦身
- 不要删有用文件

## Proven Rule From 2026-06-28 Run

Do not start by deleting large folders. First separate:

1. Regenerable cache/temp data: safe to clean.
2. User/project assets: review only, do not delete automatically.
3. Docker/model/development stores: inspect before pruning.
4. System component cleanup: prefer Windows tools; DISM may need elevated admin.
5. Clone feasibility: compare source partition size and target disk size, not just used GB.

## SOP

1. Check reusable knowledge first:
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
   - if the C-drive Knowledge Brain is missing, stop with `BLOCKED_C_SOURCE_MISSING`; do not fall back to H or K
2. Scan only:
   - C drive used/free size.
   - Disk and partition layout.
   - Desktop, Downloads, AppData caches, Docker, Codex, AI model caches.
3. Classify:
   - Safe clean: Temp, browser cache, npm/pip cache, crash dumps, WER, recycle bin after user intent is clear.
   - Review: Desktop, Downloads, Documents, `.codex`, Codex workspaces.
   - Inspect first: Docker images/containers/volumes, model stores, databases.
4. Clean safe items first and log before/after GB.
5. Re-scan after cleaning.
6. For SSD migration, verify whether source C partition can fit the target SSD. If source partition is larger than target, recommend shrink/resize-aware migration before cloning.

## Bundled Scripts

- `scripts/c_drive_cleanup_fast_scan.ps1`: scan candidate directories and disk size without deleting.
- `scripts/c_drive_safe_cleanup.ps1`: conservative cleanup for old temp/cache/crash data.
- `scripts/c_drive_cache_recycle_cleanup.ps1`: stronger cache cleanup plus recycle bin after user intent is clear.

Read `references/cleanup-decision-matrix.md` before deleting anything beyond temp/cache/recycle paths.

## Do Not Delete Automatically

- Desktop project/software folders.
${REDACTED_SECRET}
${REDACTED_SECRET}
- AI skills or knowledge folders.
- Docker volumes or stopped containers without user confirmation.
- Model directories without confirming they are old/re-downloadable.

## Acceptance Evidence

For each run, save:

- scan report
- cleanup report
- final recommendation with disk/partition sizes
- note whether destructive cleanup was limited to safe cache/temp/recycle locations

## Recent Use

- 2026-06-28: C drive before SSD migration. C used reduced from 211.08 GB to 204.61 GB. Source C partition was 3725.91 GB on a 4 TB HDD; target SSD was 698.64 GB USB disk, so partition resizing/migration-tool support is required despite low used space.
