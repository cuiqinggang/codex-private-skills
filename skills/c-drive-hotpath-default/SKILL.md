---
name: c-drive-hotpath-default
description: Use when configuring, launching, diagnosing, or saving outputs for local apps, AI tools, Codex tasks, ComfyUI, Hermes, Knowledge Brain, CodeGraph, or Windows automation where disk placement matters; enforces C drive SSD as the default hot runtime path and treats D/H/K mechanical or backup drives as opt-in only.
---

# C Drive Hotpath Default

## Core Rule

Default all active runtime, saves, generated outputs, caches, temp directories, virtual environments, logs, app launchers, scheduled tasks, and working folders to the system SSD on `C:`.

Treat `H:` as history-only. Never write, mirror, sync, update, or create backups from C to H. Treat `K:` as backup/archive/restore/delivery-only; a C-to-K backup requires both a verified C-drive source and the user's explicit approval for that specific backup operation. A missing C-drive source must block instead of falling back to H or K.

## User Preference

The user clarified on 2026-07-04:

- `C:` is the fast system SSD and the default place for solving problems.
- `D:` is a normal mechanical work disk, not an active system/runtime disk.
- Do not silently run apps, write temp files, save generated outputs, or schedule scans on `D:`.
- If a task needs another disk, ask or proceed only when the user explicitly names that disk.

The user clarified again on 2026-07-07:

- The active runtime disk is now `C:` / the Windows system disk.
- Future runs should launch directly from C-drive hot paths by default.
- Backup/reference disks must not become the active runtime path just because an old scheduled task or wrapper still points there.
- If a protected Windows task cannot be edited away from `H:` or `K:`, the non-C target may exist only as a compatibility shim that immediately forwards to the real C-drive launcher.

## Trigger Phrases

Use this skill when the user says or implies:

- `D盘发热`
- `机械盘很烫`
- `硬盘一直转`
- `为什么机械盘在运行`
- `默认放C盘`
- `不要用D盘运行`
- `输出到C盘`
- `临时目录到C盘`
- `机械盘只做普通盘`
- `C盘热路径`
- `H盘旧路径`
- `K盘只是备份`
- `ComfyUI输出到C盘`
- `知识库不要扫机械盘`

## Required Preflight

Before launching or configuring a local app or long-running workflow, check for hot-path leaks:

1. App command line: no `--output-directory`, `--input-directory`, `--temp-directory`, cache, log, model, workspace, or data path should point to `D:`, `H:`, or `K:` unless requested.
2. Scheduled tasks: no automatic recurring task should point to mechanical or backup drives unless requested.
3. Process list: no current process should be running from or writing active temp/output data to `D:`, `H:`, or `K:` unless requested.
4. Environment variables: `TEMP`, `TMP`, user profile, app data, and project runtime roots should stay on `C:`.
5. Knowledge/skill paths: active Codex skills and Knowledge Brain hot paths should use C-drive copies first.

## Default Placement Matrix

Use `C:` by default:

- app installs and launchers
- active project workspaces
- generated outputs unless user says archive/export elsewhere
- `input`, `output`, `temp`, `cache`, `logs`
- Python/Node virtual environments
- Codex skills and hot Knowledge Brain indexes
- recurring scheduled tasks and health checks
- active model downloads unless the user explicitly chooses cold storage

Use `H:` only for explicitly requested historical inspection. Use `K:` only for explicitly requested backup/archive/restore/delivery work after the applicable gate:

- C-to-K backup after C verification and per-operation user approval
- archive
- restore source
- disaster recovery
- large cold storage
- manual transfer
- cleanup/migration target
- historical reference inspection

## Windows Disk Heat Diagnostic SOP

When the user says a mechanical drive is hot, noisy, spinning, or unexpectedly active:

1. Identify disk number, model, serial, media type, and drive letters.
2. Sample physical and logical disk I/O for at least 3-5 seconds.
3. Check active processes whose command line or executable path references non-C drives.
4. Check scheduled tasks and startup entries that reference non-C drives.
5. Check pagefile, temp paths, indexing, sync jobs, backup jobs, and app output/temp directories.
6. Move future runtime paths back to `C:` when safe.
7. Do not delete old data or format partitions without explicit user approval.
8. Shorten idle disk timeout only when the user wants mechanical drives to cool down.

## Cross-Drive Reference Migration Safety

When restoring a historical reference from `H:` or `K:` into the C-drive hot path after explicit user approval:

1. Resolve and validate the exact source and destination roots before any rename or copy.
2. Do not trust `Get-ChildItem <drive>:\ -Recurse` as proof that no candidate exists. A top-level reparse-point directory can be skipped. Inspect top-level attributes and explicitly enter the intended data root.
3. Scope candidate uniqueness to the authoritative product/data root and record the scope. Never label a scoped scan as a reliable full-drive scan.
4. Hash the approved restore source before copying and verify the C-drive runtime copy file-by-file. Do not create or refresh any backup as a side effect.
5. Preserve historical-source references in evidence reports; distinguish them from executable, configuration, launcher, or runtime dependencies before changing anything.
6. Treat Git/CodeGraph discovery as a non-fatal capability probe. Under `$ErrorActionPreference = 'Stop'`, temporarily handle native Git stderr/exit codes so `git rev-parse` returning “not a repository” cannot abort a completed migration.
7. Persist the final summary before optional Git/CodeGraph diagnostics, or wrap optional diagnostics so they cannot suppress the migration result.

## Reusable Scripts

- `scripts/diagnose-hotpath.ps1`
  - Read-only diagnostic script.
  - Captures disk inventory, volumes, partitions, disk I/O samples, non-C process command lines, scheduled tasks referencing non-C drives, pagefile, temp paths, services, and power disk idle settings.
${REDACTED_SECRET}

## Checklists And Templates

- `checklists/hotpath-preflight-checklist.md`: before starting any long-running local app or workflow.
- `checklists/d-drive-heat-diagnostic-checklist.md`: when a mechanical drive is hot or unexpectedly active.
- `templates/hotpath-diagnostic-report-template.md`: standard report layout for future updates.
- `templates/agent-rule-patch.md`: draft AGENTS.md patch for future global rule updates.

## Known 2026-07-04 Fixes

- ComfyUI launcher `C:\AI\ComfyUI_Aaki_v3\START_COMFYUI_C_DRIVE_OUTPUT_D.ps1` was changed so input/output/temp use `C:\AI\ComfyUI_Aaki_v3\data`.
- Windows disk idle timeout was changed from 20 minutes to 5 minutes.
- `AI Knowledge Brain Deep Sync`, `AI Knowledge Brain Light Sync`, and `CodeGraph Sync Important Repos Hourly` were disabled where permissions allowed.
- Current D/H leaking processes were stopped.
- The D-drive heat/root-cause report and C-drive hotpath rule were converted into this reusable skill package.
- A durable Knowledge Brain / Obsidian note was created.

## Known Residuals

Two legacy logon tasks were still protected by Windows permissions during the 2026-07-04 run:

- `CodeGraph Sync Important Repos` points to `H:\AI\scripts\codegraph-sync-important-repos.ps1`.
- `Hermes_OpenWebUI_AutoStart` points to `H:\Hermes_Windows_Native_014\AUTO-START-HERMES-OPENWEBUI.cmd`.

2026-07-07 update:

${REDACTED_SECRET}
- `H:\Hermes_Windows_Native_014\AUTO-START-HERMES-OPENWEBUI.cmd` is now only a compatibility shim to the C-drive Hermes launcher.
- When Windows task permissions allow, update the scheduled task actions themselves to point directly to C-drive launchers.

2026-07-13 update:

- Ordinary reusable-asset preflight and scanning are C-drive only by default.
- K-drive skill/workspace inspection requires explicit `--include-backups`; merely starting a complex task must not wake K.
- Skill deployment and report generation must not require or verify a K-drive copy unless the user explicitly requests backup maintenance.

2026-07-15 update:

- Apple HIG reference migration proved that a drive-root recursive scan can return a false zero when the intended data root is a reparse point (`H:\AI`).
- Cross-drive migrations now require explicit authoritative-root scans, scoped uniqueness wording, source/C/backup SHA256 verification, and separation of historical evidence references from runtime dependencies.
- Optional Git/CodeGraph discovery must be non-fatal and must not run before the final migration result is persisted.

2026-07-16 update:

- All C-to-H writes, mirrors, syncs, updates, and backups are forbidden.
- H is history-only and cannot be an update target.
- K is backup/archive/restore/delivery-only and cannot be a daily runtime, search, detection, sync, or update source.
- C-to-K backup requires a verified C source plus explicit approval for that exact backup action.
- Missing C assets must return `BLOCKED_C_SOURCE_MISSING`; no H/K fallback is allowed.

## Acceptance Criteria

A future run passes only when:

- Active process scan shows no unexpected `D:`, `H:`, or `K:` runtime paths.
- Disk I/O sampling shows no sustained writes to mechanical drives during idle.
- New app launchers use C-drive input/output/temp/cache paths by default.
- Any non-C usage is explicitly requested by the user and documented.
- No active rule or script performs C-to-H writes.
- Every C-to-K backup path is blocked unless C verification and per-operation user approval are both present.

## Update Protocol

When this skill is updated:

1. Update `SKILL.md` for the durable rule.
2. Update the relevant checklist/template/script if behavior changed.
3. Add a dated entry to `logs/RECENT_USE.md`.
4. Update the Obsidian/Knowledge Brain note when the user gives a new durable preference.
5. Run Knowledge Brain health check.
6. Report any residual Windows permission blockers honestly.
