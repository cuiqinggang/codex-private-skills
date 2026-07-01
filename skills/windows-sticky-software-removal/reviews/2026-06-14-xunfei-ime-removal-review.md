# Failure Review: Xunfei IME Sticky Removal

## Summary

Date: 2026-06-14

Task: remove Xunfei Input Method from Windows after voice input quality was unsatisfactory.

Status: package and input-method registration removed; leftover files were scheduled for next reboot deletion through `PendingFileRenameOperations`.

## What Happened

1. Xunfei IME was installed from a validated Lenovo ordinary-download package after the official Xunfei Windows download link returned 404.
2. User requested removal.
3. `winget uninstall --id iFlytek.iFlyIME` and Xunfei `Uninstall.exe` returned success, but the product remained in the package list and its folder/processes remained.
4. Processes such as `iFlyInput.exe` and `iFlyPlatform.exe` kept returning after `taskkill`.
5. The user switched active input method to Microsoft Pinyin and removed Xunfei from visible settings, but `Get-WinUserLanguageList` still showed Xunfei TIP:
   - `{B722B5D7-0C4C-4933-A7B9-DF8C91F2C643}`
   - profile `{0C7479AF-F27F-488C-A46B-5BDA6BF43E50}`
6. Removing Xunfei from `InputMethodTips` made the user language list clean.
7. Current apps still revived the old input context. Parent processes observed included Explorer/Codex/FlClash, which was not treated as malicious behavior; it was Windows input context loading old IME components.
8. A SYSTEM startup task ran on reboot and performed ownership/ACL work, but deletion still failed on `iFlyIMEQuickLaunch.dll`.
9. The final escalation queued 72 child items plus the target directory in `PendingFileRenameOperations`.

## Root Causes

- IME software integrates with Windows TSF/CTF rather than behaving like a simple app.
- Uninstaller reported success without fully removing TSF/COM registrations and files.
- Current user language list and current-user CTF keys can survive after uninstall.
- Desktop applications can trigger old input contexts and relaunch IME processes.
- DLLs can remain locked even after package removal.
- Direct destructive deletes may fail due to active locks or insufficient/effective permission context.

## Key Evidence

Package removed:

```text
winget list --id iFlytek.iFlyIME
找不到与输入条件匹配的已安装程序包。
```

Language list cleaned:

```text
LanguageTag     : zh-Hans-CN
InputMethodTips : 0804:{81D4E9C9-1D3B-41BC-9E6C-4B40BF79E35E}{FA550B04-5AD7-411F-A5AC-CA038EC515D7}
```

Startup task failed on locked DLL:

```text
target remove attempt 1 failed: 对路径“iFlyIMEQuickLaunch.dll”的访问被拒绝。
...
target remove attempt 12 failed: 对路径“iFlyIMEQuickLaunch.dll”的访问被拒绝。
target still exists; task kept for next startup
```

Pending delete queue written:

```text
scheduled 72 children plus target
PendingCount : 152
IFlyEntries  : 73
```

## Correct Future Flow

1. Normal uninstall.
2. Verify package, processes, folder.
3. Remove active user integration first, especially `Get-WinUserLanguageList` for IMEs.
4. Clean current-user CTF and startup entries.
5. Identify parent process that revives target.
6. Avoid killing proxy/network clients unless explicitly approved.
7. Remove exact system TSF/COM registrations when possible.
8. Try hot delete only after integration cleanup.
9. If hot delete fails, create SYSTEM startup task that only self-deletes after success.
10. If startup task fails on a DLL, queue all remaining files/directories with `PendingFileRenameOperations`.
11. Reboot again and verify.

## Lessons

- "Uninstalled" in winget/control panel is not enough for sticky software.
- For IMEs, always inspect `Get-WinUserLanguageList`.
- Do not assume the process parent is malicious; it may be an app triggering Windows input context.
- Do not close network/proxy tools without explicit user approval.
- A resilient cleanup task must not self-delete until it proves the target folder is gone.
- `PendingFileRenameOperations` is the correct escalation for access-denied locked DLLs after reboot cleanup.
- This case generalizes to 360-like software: uninstall is a state machine across user integration, services/drivers/tasks, file locks, permissions, and boot-time cleanup.
