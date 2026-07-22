@echo off
set SCRIPT=%USERPROFILE%\.codex\manual-paste-attachments\install-auto-longtext-fileclip.ps1
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT%" -Start
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "Add-Type -AssemblyName PresentationFramework; [System.Windows.MessageBox]::Show('Auto long-text converter is ON. Copy long text, then press Ctrl+V in Codex.','Codex Long Text Fallback') | Out-Null"
