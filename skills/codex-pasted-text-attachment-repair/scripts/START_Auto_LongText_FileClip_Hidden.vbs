Option Explicit

Dim shell
Dim command

Set shell = CreateObject("WScript.Shell")
command = "powershell.exe -NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File " & Chr(34) & "C:\Users\A\.codex\manual-paste-attachments\install-auto-longtext-fileclip.ps1" & Chr(34) & " -Start"
shell.Run command, 0, False
