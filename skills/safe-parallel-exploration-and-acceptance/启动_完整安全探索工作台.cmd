@echo off
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\dashboard\workbench-menu.ps1" %*
exit /b %ERRORLEVEL%

