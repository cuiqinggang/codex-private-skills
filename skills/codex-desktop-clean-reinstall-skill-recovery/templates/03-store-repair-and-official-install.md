# Store Repair And Official Install

Goal: reinstall official Codex without third-party sources.

## Primary Install

```powershell
winget install Codex -s msstore
```

## If Store Stalls At 22% / 24%

1. Cancel the stalled download.
2. Run `wsreset`.
3. Use Windows Settings > Apps > Microsoft Store > Advanced options > Terminate / Repair / Reset.
4. Reboot if needed.
5. Check services:
   - Microsoft Store Install Service
   - Windows Update
   - Background Intelligent Transfer Service
   - Delivery Optimization
6. Temporarily disable proxy, TUN, and global proxy only with user confirmation.
7. Re-register Store and DesktopAppInstaller:

```powershell
Get-AppxPackage -allusers Microsoft.WindowsStore | Foreach {
  Add-AppxPackage -DisableDevelopmentMode -Register "$($_.InstallLocation)\AppXManifest.xml"
}

Get-AppxPackage -allusers Microsoft.DesktopAppInstaller | Foreach {
  Add-AppxPackage -DisableDevelopmentMode -Register "$($_.InstallLocation)\AppXManifest.xml"
}
```

8. Retry official install.

Do not use third-party download sites.
