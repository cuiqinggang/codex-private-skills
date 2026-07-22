---
name: windows-sticky-software-removal
description: Use when Windows software is hard to uninstall or leaves sticky remnants, especially input methods, security suites, 360-like tools, IMEs, shell extensions, proxy/network clients, drivers, services, scheduled tasks, COM/TSF registrations, files locked by Explorer or other apps, or uninstallers that report success but leave processes, folders, or registry entries behind.
---

# Windows Sticky Software Removal

Use this skill when a Windows application behaves like "请神容易送神难": normal uninstall appears to succeed, but processes, startup entries, input methods, services, registry registrations, or locked files remain.

## Trigger Keywords

- 难卸载
- 删除不掉
- 卸载失败
- 卸载器显示成功但还在
- 牛皮糖软件
- 360 一样难删
- 输入法删不掉
- 讯飞输入法残留
- iFlyIME / iFlytek
- 文件被占用 / access denied
- 重启后删除
- PendingFileRenameOperations

## Core Rule

Do not start by force-deleting random folders. First identify why the software is being revived or locked.

Common layers:

1. Installed package registration: winget, Uninstall registry.
2. User-facing configuration: language list, default input method, startup apps.
3. Runtime lock: running EXE/DLL loaded by Explorer, app windows, shell, IME framework, proxy tools, or service host.
4. Persistence: service, scheduled task, Run/RunOnce, COM/CLSID, TSF/CTF, shell extension, driver.
5. Permission/ownership: ACL or TrustedInstaller/SYSTEM ownership.
6. Early boot cleanup: scheduled task at startup or Session Manager pending delete.

## Difficulty Levels

- Level 1: ordinary app residue. Package removed, leftover folders/registry can be deleted after closing app.
- Level 2: shell/startup app. Explorer, tray app, browser, or updater revives it; remove startup/task/service and retry.
- Level 3: IME/input framework. TSF/CTF, language list, COM/CLSID, and active input contexts can revive it.
- Level 4: security-suite/360-like software. Self-protection, services, drivers, browser/homepage hooks, shell extensions, and protected files may require Safe Mode or Session Manager deletion.
- Level 5: driver/rootkit-like or unknown origin. Stop and use Safe Mode, trusted rescue environment, vendor cleanup tool, or malware-removal workflow.

## Required Preflight

Before destructive cleanup:

- Confirm the exact product identity and install path.
- Confirm the user wants removal.
- Avoid shutting down proxy/network clients unless the user explicitly approves.
- Never delete broad vendor folders if they may contain unrelated products.
- Prefer removing the software from active system integration first, then delete files.

## Recommended Flow

Read [sop/STICKY-WINDOWS-UNINSTALL-SOP.md](sop/STICKY-WINDOWS-UNINSTALL-SOP.md) before acting.

Use scripts only after adapting constants such as product name, install path, GUIDs, and process names.

## Lessons From Xunfei IME Case

The 2026-06-14 Xunfei IME case is the reference failure review:

- Uninstaller and winget said success.
- App still appeared in `winget list`.
- Processes revived after `taskkill`.
- Windows user language list still included the IME TSF tip.
- Current applications revived the IME through Windows input context.
- First boot cleanup ran but failed on `iFlyIMEQuickLaunch.dll`.
- A second, lower-level boot delete queue using `PendingFileRenameOperations` was needed.

Read [reviews/2026-06-14-xunfei-ime-removal-review.md](reviews/2026-06-14-xunfei-ime-removal-review.md).

## 360/Security Suite Reference

360 and 360 Total Security public guidance and community experience show a higher-difficulty version of the same model:

- vendor uninstaller first;
- choose the true uninstall/leave/protection-abandon path;
- reboot after official uninstall because residual files may be removed then;
- if residue remains, inspect services, drivers, startup, scheduled tasks, browser/homepage hooks, install folders, and registry;
- if normal mode cannot delete, use Safe Mode or startup-before-login deletion.

Read [sop/SECURITY-SUITE-360-REMOVAL-NOTES.md](sop/SECURITY-SUITE-360-REMOVAL-NOTES.md).

For full "software ecosystem" removals, read [sop/FULL-ECOSYSTEM-REMOVAL-MODEL.md](sop/FULL-ECOSYSTEM-REMOVAL-MODEL.md). This is the primary model for 360-like bundles where several products, services, drivers, tasks, browser hooks, and file-protection components may protect each other.

## Acceptance Criteria

A removal is not complete until:

- Package manager no longer lists it.
- User-facing integration no longer lists it.
- Related processes are absent after a wait.
- Main install directory is absent, or deletion is scheduled in `PendingFileRenameOperations`.
- Startup/service/task/COM/TSF entries are removed or understood.
- A log records exactly what was removed and what remains.

Use the "Backward Proof" section in the SOP: start from the desired final state and confirm each prerequisite chain. A command succeeding is not proof of removal.

## Usage Log

Append each use to [logs/usage-log.md](logs/usage-log.md).
