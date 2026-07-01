# Security Suite / 360 Removal Notes

## Why This Matters

360-like software is a useful high-difficulty reference case for sticky Windows removal. It has the same broad pattern as the Xunfei IME case, but usually one level deeper:

- normal uninstaller and retention prompts;
- self-protection;
- services and drivers;
- browser/homepage protection;
- related bundled products;
- install directories under `C:\Program Files`, `C:\Program Files (x86)`, `ProgramData`, and user AppData;
- residue that may only delete after reboot, Safe Mode, or early boot deletion.

For a complete graph-based approach, read [FULL-ECOSYSTEM-REMOVAL-MODEL.md](FULL-ECOSYSTEM-REMOVAL-MODEL.md).

## Publicly Observed Mature Practices

From official and community sources:

1. Start with the official uninstall path in Control Panel / Apps.
2. In the 360 uninstall UI, choose the real uninstall/continue/confirm path rather than retention/protection prompts.
3. Reboot after uninstall. Official/community pages mention residual files/folders can be removed after reboot.
4. If normal uninstall fails or leaves residue, close 360 tray processes and check Task Manager.
5. If normal mode deletion fails, boot Safe Mode and delete leftovers.
6. Clean residual services, drivers, startup entries, scheduled tasks, and registry entries only after identifying exact 360-related names and paths.
7. Third-party uninstallers such as Revo-style tools are often recommended by communities for scanning leftovers, but they are optional and must be downloaded only from trusted sources if used.

## 360-Specific Checklist

Inventory:

```powershell
winget list | Select-String -Pattern '360|Qihoo|Qihu|Total Security'
Get-ItemProperty 'HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*','HKLM:\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*' -ErrorAction SilentlyContinue |
  Where-Object { $_.DisplayName -match '360|Qihoo|Qihu|Total Security' -or $_.Publisher -match '360|Qihoo|Qihu' } |
  Select-Object DisplayName,DisplayVersion,Publisher,InstallLocation,UninstallString
```

Runtime:

```powershell
Get-Process | Where-Object { $_.ProcessName -match '360|QH|Qihu|Qihoo|Total' } |
  Select-Object ProcessName,Id,Path
```

Services and drivers:

```powershell
Get-CimInstance Win32_Service |
  Where-Object { $_.Name -match '360|QH|Qihu|Qihoo' -or $_.DisplayName -match '360|QH|Qihu|Qihoo' -or $_.PathName -match '\\360\\|Qihoo|Qihu' } |
  Select-Object Name,DisplayName,State,StartMode,PathName

Get-CimInstance Win32_SystemDriver |
  Where-Object { $_.Name -match '360|QH|Qihu|Qihoo' -or $_.DisplayName -match '360|QH|Qihu|Qihoo' -or $_.PathName -match '\\360\\|Qihoo|Qihu' } |
  Select-Object Name,DisplayName,State,StartMode,PathName
```

Startup and tasks:

```powershell
Get-ScheduledTask | Where-Object { $_.TaskName -match '360|QH|Qihu|Qihoo' -or $_.TaskPath -match '360|QH|Qihu|Qihoo' }
Get-ItemProperty 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Run','HKLM:\Software\Microsoft\Windows\CurrentVersion\Run','HKLM:\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Run' -ErrorAction SilentlyContinue
```

Likely residue locations:

```text
C:\Program Files\360
C:\Program Files (x86)\360
C:\ProgramData\360*
%AppData%\360*
%LocalAppData%\360*
```

## Escalation Ladder

1. Official uninstaller.
2. Reboot and verify.
3. Remove exact startup/task/service residues.
4. Safe Mode delete leftover folders.
5. If specific files are still locked, schedule `PendingFileRenameOperations`.
6. If drivers remain and cannot be stopped, use Safe Mode or Windows Recovery Environment rather than live deletion.

## Warnings

- Do not use random "360 removal tools" from search results. Prefer official vendor pages or trusted uninstallers with source verification.
- Do not remove broad registry keys by keyword until exact product ownership is confirmed.
- Do not disable Defender or network/proxy components as a side effect unless the user approves and the reason is clear.
- Document every deletion and leave a rollback note for services/tasks that were disabled rather than deleted.

## Source Notes

Public references used for this note include:

- 360 Total Security official uninstall guide: Control Panel/Programs removal, confirm uninstall, reboot, check remaining Program Files folder.
- 360 Community posts describing uninstall prompts such as protection-abandon/leaving prompts and reboot cleanup.
- Microsoft community guidance that Windows Defender may require complete removal of third-party antivirus, not just disabling.
- Community posts recommending normal uninstall, force-delete leftovers, Explorer termination, Safe Mode deletion, and third-party leftover scanners.
