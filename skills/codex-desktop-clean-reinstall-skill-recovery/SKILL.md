---
name: codex-desktop-clean-reinstall-skill-recovery
description: "Use when Codex Desktop on Windows must be safely backed up, cleaned, reinstalled from official Microsoft Store or winget channels, checked after reinstall, or restored from a user-approved K-drive backup, especially after Codex++ residue, Store install stalls, proxy residue, or .codex node_modules deletion failures. Never use H as the active or recovery source."
---

# Codex Desktop Clean Reinstall Skill Recovery

## Purpose

Use this skill for the controlled Windows workflow that preserves Codex skills, removes broken Codex/Codex++ state, reinstalls official Codex, checks the new environment, and restores only non-conflicting skills.

## When To Use

- Codex Desktop is stuck, misrouting models, failing to start, or carrying proxy residue.
- Codex processes are running (`Get-Process -Name Codex`) but NO window appears (MainWindowHandle=0) — **zombie process syndrome**.
- Codex++ / CodexPlusPlus was installed and may have taken over official Codex.
${REDACTED_SECRET}
- Official Codex has been reinstalled and the user explicitly approved a specific backup under `K:\AI\backups` for restoration.
- `.codex` deletion fails because of `node_modules`, `.pnpm`, long paths, or "directory not empty" errors.

## Risk Levels

- **Read-only checks:** safe to run without confirmation.
- **Backup and report creation:** safe; may create files under the requested backup/report paths.
- **Non-conflicting skill restore:** medium risk; back up current `.codex` and `.agents` first, skip same-name targets, skip `.system`.
- **Danger actions:** stop for explicit user confirmation before deleting `.codex`, deleting `.agents`, deleting Codex++ folders, deleting registry uninstall entries, overwriting any skill, copying `auth.json`, changing proxy/account/Store/environment state, or installing Codex++.

## Core Rules

1. **Protect before delete.** Before repair, check and report existence of `skills`, `.agents\skills`, `config.toml`, `auth.json`, `sessions`, and `session_index.jsonl`. Do not copy sensitive auth files to long-term backup unless the user explicitly asks.
2. **Never overwrite the new official `.codex`.** Do not replace `auth.json`, `config.toml`, `installation_id`, `state_*.sqlite`, `logs_*.sqlite`, `goals_*.sqlite`, `memories_*.sqlite`, `plugins`, `sessions`, or `.system`.
${REDACTED_SECRET}
4. **Treat Codex++ as high-risk residue.** If Codex++ paths, shortcuts, or `winget list Codex` entries exist, list them and stop before deleting.
5. **Use `rmdir` when PowerShell fails on long paths.** If `Remove-Item` fails on `.codex` with `node_modules`, `.pnpm`, long path, missing path part, or directory-not-empty errors, use `cmd /c rmdir /s /q "%USERPROFILE%\.codex"`, then verify `Test-Path "$env:USERPROFILE\.codex"` returns `False`.
6. **Fix Store before using third-party sources.** Prefer official `winget install Codex -s msstore`. If Store stalls at 22%/24%, use `wsreset`, Store repair/reset, service checks, proxy/TUN checks, re-registration, and retry official channels. Do not recommend third-party download sites.
7. **Restore only non-conflicting skills.** Copy only backup skill directories that do not exist in the target. Never overwrite same-name directories.
8. **Agents first get diffed.** For `.agents\skills`, compare counts, sizes, and hashes; do not overwrite same-name skills until the user decides.
9. **Every stage writes a report.** Include time, stage, actions done, skipped actions, path existence, counts, conflicts, risks, next step, and whether confirmation is required.
10. **Danger actions require a pause.** Do not automate destructive system or identity changes.

## Standard Workflow

### A. Preserve Before Uninstall

${REDACTED_SECRET}
2. After validating the C source and obtaining explicit approval for this exact backup, create `K:\AI\backups\Codex_Reinstall_Skill_Backup_YYYYMMDD`; otherwise stop with `BACKUP_NOT_AUTHORIZED`.
3. Copy skills to `codex-skills` and `agents-skills`.
4. Generate `copy-log.tsv`, `codex-desktop-reinstall-preservation-notes.md`, and `codex-reinstall-machine-readable-index.md`.
5. Verify counts and report.
6. Stop before deletion.

Use `scripts\preserve_codex_skills.ps1`.

### B. Clean Old Environment

1. Close Codex.
2. Stop Codex-related processes only after the user is ready.
3. Try normal uninstall first.
4. If Codex++ opens its manager instead of uninstalling, record an uninstall abnormality, stop `winget`, inspect paths, write a forced-clean plan, and wait for confirmation.
5. Delete `.codex` only after backup and confirmation. If `Remove-Item` fails, use the `cmd rmdir` fallback.
6. Verify `.codex` removal with `Test-Path`.
7. Run `winget list Codex`.
8. Report.

Use `templates\02-clean-uninstall-codex-and-codexplusplus.md` as the operator checklist.

### C. Official Reinstall

1. Use official channel: `winget install Codex -s msstore`.
2. If Store stalls, run Store repair steps.
3. Do not use third-party installers.
4. Launch official Codex and confirm Codex++ manager does not appear.
5. Report.

Use `templates\03-store-repair-and-official-install.md`.

### D. Post-Reinstall Read-Only Check

1. Check a user-approved historical restore source; H is read-only history and must never receive writes.
2. Check current `.codex` and `.agents`.
3. Count skills.
4. Detect `.system` and Agents `learned`.
5. Check Codex++ residue paths and shortcuts.
${REDACTED_SECRET}
7. Stop before restore.

Use `scripts\readonly_check_after_reinstall.ps1`.

### E. Restore Skills

1. Back up current `.codex` and `.agents` to K only after C validation and explicit per-operation approval.
2. Copy only missing Codex skills from H-drive backup.
3. Skip `.system`.
4. Diff Agents skills; do not overwrite.
5. Write restore report and updated index.
6. Never sync this skill package to H. Any C-to-K backup is a separate explicitly approved operation after C validation.

Use `scripts\restore_non_conflict_codex_skills.ps1` and `scripts\check_agents_skill_diff.ps1`.

### F. Zombie Process Recovery (窗口不显示但进程运行)

**症状**: `Get-Process -Name Codex` 显示多个进程（Responding=True），但 `MainWindowHandle=0`、`MainWindowTitle=""`。Codex 尝试启动但窗口从不出现。

**根因**: Windows Store App 的 Codex 后台进程变成了僵尸进程——没有关联的 UI 窗口。重新启动 Codex 时，它检测到已有进程并附加到它们，而不是创建新的 UI 窗口。这些进程继续运行和写日志，但永远不会显示窗口。

**修复流程（无需重新安装）**:

1. **杀进程**: 强制终止所有 Codex 进程。
```powershell
Get-Process -Name "Codex" -ErrorAction SilentlyContinue | Stop-Process -Force
```

2. **技能包冷启动**（可选，若步骤1后仍不显示窗口则执行）: 临时移走 `.system` 之外的所有技能包，让 Codex 做一次干净的首次扫描，确认窗口能出现。
```powershell
New-Item -ItemType Directory -Path "$env:USERPROFILE\Desktop\codex-skills-temp" -Force
Get-ChildItem -LiteralPath "$env:USERPROFILE\.codex\skills" -Directory | Where-Object { $_.Name -ne ".system" } | Move-Item -Destination "$env:USERPROFILE\Desktop\codex-skills-temp\" -Force
```

3. **启动验证**: 
```powershell
Start-Process "shell:AppsFolder\OpenAI.Codex_2p2nqsd0c76g0!App"
Start-Sleep -Seconds 30
Get-Process -Name "Codex" | Where-Object { $_.MainWindowHandle -ne 0 }
```

4. **恢复技能包**（若执行了步骤2）: 关闭 Codex，移回所有技能包，重新启动。
```powershell
Get-Process -Name "Codex" | Stop-Process -Force
Get-ChildItem -LiteralPath "$env:USERPROFILE\Desktop\codex-skills-temp" -Directory | Move-Item -Destination "$env:USERPROFILE\.codex\skills\" -Force
Remove-Item -LiteralPath "$env:USERPROFILE\Desktop\codex-skills-temp" -Recurse -Force
```

5. **最终验证**: 确认 Codex 窗口出现且所有技能包加载正常。

**已验证案例** (2026-06-30): 108 个技能包全部恢复后 Codex 正常启动，窗口正常渲染。问题不是技能包数量或冲突，纯粹是僵尸进程残留。

**复发案例** (2026-06-30 15:24): 同一天再次出现相同问题。7个进程全部 MainWindowHandle=0。仅杀进程后直接启动即成功，无需冷启动。根因分析发现：
- 3个开机启动项和4个计划任务都不直接启动 Codex 应用
- Codex Store App 无后台任务注册
- Windows 快速启动 (HiberbootEnabled=1) 可能导致关机前僵尸进程状态残留到开机后
- 根因是 Codex 偶发 app-server 初始化超时，进程残留后再次启动挂载到旧僵尸

**彻底预防方案** (2026-06-30 部署，2026-06-30 复核加固):
${REDACTED_SECRET}
2. **开机自动清理**: `CodexBootCleanup.vbs` 已放入启动文件夹。开机后等待 20 秒再检查；只有当存在 Codex 进程且没有任何可见窗口时，才静默清理残留进程。不要把“有正常窗口时的无窗口辅助进程”当成僵尸。
3. 可选: 禁用 Windows 快速启动 (`powercfg /hibernate off`) 从根本上解决进程残留。

## Command Library

### 僵尸进程诊断 + 修复
```powershell
# 诊断：检查 Codex 是否有窗口
Get-Process -Name "Codex" | Select-Object Id, MainWindowTitle, MainWindowHandle, Responding, StartTime
# MainWindowHandle=0 且 MainWindowTitle="" → 僵尸进程

# 强制杀进程
Get-Process -Name "Codex" -ErrorAction SilentlyContinue | Stop-Process -Force

# 从 Store 启动
Start-Process "shell:AppsFolder\OpenAI.Codex_2p2nqsd0c76g0!App"

# 技能冷启动（仅当杀进程后窗口仍不出现）
New-Item -ItemType Directory -Path "$env:USERPROFILE\Desktop\codex-skills-temp" -Force
Get-ChildItem -LiteralPath "$env:USERPROFILE\.codex\skills" -Directory | Where-Object { $_.Name -ne ".system" } | Move-Item -Destination "$env:USERPROFILE\Desktop\codex-skills-temp\" -Force
# 启动 Codex 验证窗口 → 关闭 Codex → 恢复技能包
Get-ChildItem -LiteralPath "$env:USERPROFILE\Desktop\codex-skills-temp" -Directory | Move-Item -Destination "$env:USERPROFILE\.codex\skills\" -Force
Remove-Item -LiteralPath "$env:USERPROFILE\Desktop\codex-skills-temp" -Recurse -Force

# 验证修复：至少有一个进程的 MainWindowHandle ≠ 0
Get-Process -Name "Codex" | Where-Object { $_.MainWindowHandle -ne 0 } | Format-Table Id, MainWindowTitle, MainWindowHandle
```

### 常规命令

```powershell
cmd /c rmdir /s /q "%USERPROFILE%\.codex"
Test-Path "$env:USERPROFILE\.codex"
winget list Codex
winget install Codex -s msstore
wsreset
Get-Process | Where-Object {
    $_.ProcessName -match "codex|Codex|plus|Plus|node|npm|pnpm"
} | Stop-Process -Force -ErrorAction SilentlyContinue
Get-ItemProperty `
"HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*",`
"HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*",`
"HKLM:\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*" `
-ErrorAction SilentlyContinue |
Where-Object { $_.DisplayName -match "Codex" -or $_.DisplayName -match "Codex\+\+" -or $_.DisplayName -match "CodexPlusPlus" } |
Select-Object DisplayName, DisplayVersion, InstallLocation, DisplayIcon, UninstallString
Get-AppxPackage -allusers Microsoft.WindowsStore | Foreach {
  Add-AppxPackage -DisableDevelopmentMode -Register "$($_.InstallLocation)\AppXManifest.xml"
}
Get-AppxPackage -allusers Microsoft.DesktopAppInstaller | Foreach {
  Add-AppxPackage -DisableDevelopmentMode -Register "$($_.InstallLocation)\AppXManifest.xml"
}
```

## Bundled Files

- `README.md`: user-facing overview.
- `templates\01-preserve-before-uninstall.md` through `templates\06-final-acceptance-report.md`: stage templates.
- `scripts\preserve_codex_skills.ps1`: safe backup script.
- `scripts\readonly_check_after_reinstall.ps1`: read-only check script.
- `scripts\restore_non_conflict_codex_skills.ps1`: non-overwriting restore script.
- `scripts\check_agents_skill_diff.ps1`: read-only Agents diff script.
- `examples\successful-case-20260611.md`: successful case notes.
- `examples\zombie-process-recovery-20260630.md`: zombie process recovery case — Codex running but no window (2026-06-30).
- `examples\codex-command-package-full-recovery.md`: future copy-paste command package.

## Report Template

```markdown
# Codex Desktop Clean Reinstall Stage Report
- Time:
- Stage:
- Actions executed:
- Actions not executed:
- Path checks:
- Skill counts:
- Conflicts:
- Risks:
- Confirmation required:
- Recommended next step:
```

## Stop Points

Stop and wait for explicit user confirmation before any destructive action, registry deletion, overwrite, sensitive auth copy, proxy/account/Store/environment modification, or Codex++ installation.
