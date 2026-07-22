# Full Ecosystem Removal Model

## Purpose

Use this when the target is not one app but a software ecosystem: 360-like security suites, "software manager + browser + updater + guard" bundles, IME suites, driver assistants, ad blockers, and tools with self-protection.

The core idea: do not "delete a program". Remove the ecosystem's ability to exist.

## The Ecosystem Layers

A sticky ecosystem can survive through any of these layers:

1. Product inventory
   - Main app, companion app, browser, updater, software manager, compression tool, driver tool, rescue tool.
2. User integration
   - Start menu, tray, startup app, default browser/homepage, IME language list, context menu.
3. Process graph
   - Watchdog process, updater, tray process, helper process, parent process reviving children.
4. Services
   - Windows services that start at boot or on demand.
5. Drivers
   - Kernel/system drivers that protect files, network, disk, browser, or security features.
6. Scheduled tasks
   - Update, repair, telemetry, restart, health check, reinstaller.
7. Shell/browser hooks
   - Explorer extensions, browser protection, homepage lock, URL protocol handlers.
8. Registry/COM/TSF
   - COM/CLSID, CTF/TIP for IMEs, uninstall registry, App Paths, services, drivers.
9. Files and data
   - Program Files, ProgramData, AppData, temp folders, caches, logs, quarantine.
10. Early boot residue
   - Locked DLLs/drivers that require Safe Mode, startup task, Session Manager pending delete, or recovery environment.

## Removal Is A Dependency Problem

If B can revive A, deleting A first is wasted effort.

Preferred order:

1. Inventory all related products and paths.
2. Disable/exit self-protection if the UI provides a legitimate option.
3. Use official uninstallers for each related product.
4. Reboot.
5. Remove user integrations.
6. Remove services/tasks/startups.
7. Remove drivers only after confirming ownership and risk.
8. Remove COM/shell/browser/TSF registrations.
9. Take ownership and delete files.
10. If locked, use Safe Mode or `PendingFileRenameOperations`.
11. Verify from final state backward.

## 360-Like Full Removal Strategy

360 is a high-value reference because it often involves "protection" semantics:

- It may ask whether to continue uninstalling or keep protection.
- It may use wording that nudges retention.
- It may have related products beyond the obvious one.
- It may leave residual folders until reboot.
- It may require Safe Mode if normal mode keeps components loaded.

### Step 1: Inventory The Full 360 Family

Do not uninstall only one visible product and assume the ecosystem is gone.

Check installed products:

```powershell
winget list | Select-String -Pattern '360|Qihoo|Qihu|Total Security'

Get-ItemProperty 'HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*',
  'HKLM:\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*' -ErrorAction SilentlyContinue |
  Where-Object {
    $_.DisplayName -match '360|Qihoo|Qihu|Total Security' -or
    $_.Publisher -match '360|Qihoo|Qihu'
  } |
  Select-Object DisplayName,DisplayVersion,Publisher,InstallLocation,UninstallString
```

Check likely folders:

```powershell
Get-ChildItem 'C:\Program Files','C:\Program Files (x86)','C:\ProgramData',
  "$env:APPDATA","$env:LOCALAPPDATA" -ErrorAction SilentlyContinue |
  Where-Object { $_.Name -match '360|Qihoo|Qihu' } |
  Select-Object FullName
```

### Step 2: Use Official Uninstallers First

Official 360 guidance for 360 Total Security starts from Control Panel / Programs and Features and then follows the uninstall procedure, including confirmation prompts and reboot/checking residue afterward.

360 community guidance for 360 Security Guard says to choose the actual uninstall path in prompts such as protection-abandon / leaving prompts and then reboot so residual files/folders can be removed.

Operational rule:

- Read every uninstall prompt.
- Choose the real uninstall path.
- Avoid buttons that mean continue protection, repair, keep settings, or postpone.
- Reboot once after official uninstall before judging residue.

### Step 3: Check Live Process Graph

```powershell
Get-Process |
  Where-Object { $_.ProcessName -match '360|QH|Qihu|Qihoo|Total|Safe|Guard' } |
  Select-Object ProcessName,Id,Path

Get-CimInstance Win32_Process |
  Where-Object { $_.Name -match '360|QH|Qihu|Qihoo|Total|Safe|Guard' -or $_.CommandLine -match '360|Qihoo|Qihu' } |
  Select-Object ProcessId,ParentProcessId,Name,CommandLine
```

If processes restart, identify parent process. Do not blindly kill proxy/network/security-critical components unless the user approves and the risk is understood.

### Step 4: Check Services And Drivers

Security suites may survive below the normal process layer.

```powershell
Get-CimInstance Win32_Service |
  Where-Object {
    $_.Name -match '360|QH|Qihu|Qihoo' -or
    $_.DisplayName -match '360|QH|Qihu|Qihoo' -or
    $_.PathName -match '\\360\\|Qihoo|Qihu'
  } |
  Select-Object Name,DisplayName,State,StartMode,PathName

Get-CimInstance Win32_SystemDriver |
  Where-Object {
    $_.Name -match '360|QH|Qihu|Qihoo' -or
    $_.DisplayName -match '360|QH|Qihu|Qihoo' -or
    $_.PathName -match '\\360\\|Qihoo|Qihu'
  } |
  Select-Object Name,DisplayName,State,StartMode,PathName
```

Driver rule:

- Do not delete active drivers live unless you know exactly what they are.
- Prefer vendor uninstaller, Safe Mode, or recovery environment.
- If deleting services/drivers, record names and paths first.

### Step 5: Check Tasks, Startup, Browser/Shell Hooks

```powershell
Get-ScheduledTask |
  Where-Object { $_.TaskName -match '360|QH|Qihu|Qihoo' -or $_.TaskPath -match '360|QH|Qihu|Qihoo' } |
  Select-Object TaskName,TaskPath,State

Get-ItemProperty 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Run',
  'HKLM:\Software\Microsoft\Windows\CurrentVersion\Run',
  'HKLM:\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Run' -ErrorAction SilentlyContinue
```

Also inspect:

```text
HKLM:\Software\Microsoft\Windows\CurrentVersion\Explorer\Browser Helper Objects
HKLM:\Software\Microsoft\Windows\CurrentVersion\Shell Extensions
HKLM:\Software\Classes\*\shellex
HKLM:\Software\Classes\Directory\shellex
HKLM:\Software\Classes\CLSID
HKCU:\Software\Microsoft\Internet Explorer
Browser extension folders and policies
```

Only remove entries that point to confirmed 360/Qihoo paths.

### Step 6: Delete Files In The Right Environment

Normal mode:

```powershell
takeown /F "<360-path>" /R /D Y
icacls "<360-path>" /grant SYSTEM:F Administrators:F /T /C
Remove-Item -LiteralPath "<360-path>" -Recurse -Force
```

If normal mode fails:

1. Try a SYSTEM startup task.
2. If a DLL/driver remains locked, use `PendingFileRenameOperations`.
3. If drivers/self-protection remain, use Safe Mode.
4. If Safe Mode still fails or Windows shell is broken, use Windows Recovery Environment.

### Step 7: Final Verification

The job is not done until all are true:

```powershell
winget list | Select-String -Pattern '360|Qihoo|Qihu|Total Security'
Get-Process | Where-Object { $_.ProcessName -match '360|QH|Qihu|Qihoo|Total' }
Get-CimInstance Win32_Service | Where-Object { $_.Name -match '360|QH|Qihu|Qihoo' -or $_.DisplayName -match '360|QH|Qihu|Qihoo' }
Get-CimInstance Win32_SystemDriver | Where-Object { $_.Name -match '360|QH|Qihu|Qihoo' -or $_.DisplayName -match '360|QH|Qihu|Qihoo' }
Get-ScheduledTask | Where-Object { $_.TaskName -match '360|QH|Qihu|Qihoo' -or $_.TaskPath -match '360|QH|Qihu|Qihoo' }
```

And likely folders are absent or known harmless data backups:

```text
C:\Program Files\360
C:\Program Files (x86)\360
C:\ProgramData\360*
%AppData%\360*
%LocalAppData%\360*
```

## Why "Only Delete One Product" Fails

If the ecosystem includes:

- `360Safe` guarding browser/homepage;
- software manager repairing missing components;
- updater scheduled task reinstalling files;
- driver protecting files;
- browser extension holding shell/browser policy;

then deleting only `360Safe` leaves enough of the ecosystem alive to repair or relaunch it.

The right mental model is surgical removal of a connected graph:

```text
Installed product records
  -> services/tasks/startup
  -> drivers/self-protection
  -> browser/shell hooks
  -> processes/watchdogs
  -> files/data
  -> final verification
```

Break the graph in order. Do not tug on one node and call it done.

## Source Notes

Verified themes from public sources:

- 360 Total Security official guide: uninstall from Control Panel/Programs, confirm uninstall, reboot, check Program Files residue.
- 360 Community Security Guard uninstall guidance: choose real uninstall prompts and reboot for residual cleanup.
- Microsoft community: Defender may not become active until third-party antivirus is fully removed.
- Community technical posts: Safe Mode and Explorer termination are common when 360-related DLLs or folders cannot be deleted in normal mode.
