@echo off
start "Codex Quota Panel" powershell.exe -STA -NoProfile -ExecutionPolicy Bypass -File "%~dp0CodexQuotaPanel.ps1"
start "Codex Quota Watchdog" /min powershell.exe -WindowStyle Hidden -NoProfile -ExecutionPolicy Bypass -File "%~dp0QuotaPanelWatchdog.ps1"
