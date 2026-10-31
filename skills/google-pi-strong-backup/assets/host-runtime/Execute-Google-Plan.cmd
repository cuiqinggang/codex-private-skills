@echo off
chcp 65001 >nul
"C:\Program Files\PowerShell\7\pwsh.exe" -NoLogo -NoProfile -Command "& 'C:\Users\A\.codex\skills\powershell-reliability-guard\scripts\Invoke-GuardedPowerShell.ps1' -Path 'C:\Users\A\Documents\DSH-Workspace\gsb-pi-google-v2-20261031\Invoke-PiBackupFromClipboard.ps1' -Target PowerShell7 -ScriptArguments @('-NoPause')"
pause
