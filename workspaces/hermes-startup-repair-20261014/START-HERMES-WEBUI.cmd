@echo off
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "C:\Users\A\.codex\skills\powershell-reliability-guard\scripts\Invoke-GuardedPowerShell.ps1" -Path "C:\Users\A\Hermes_Windows_Native_014\launcher\start-hermes-openwebui.ps1" -Target WindowsPowerShell51
if errorlevel 1 pause
