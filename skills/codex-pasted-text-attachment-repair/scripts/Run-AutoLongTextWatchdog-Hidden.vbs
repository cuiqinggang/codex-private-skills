Option Explicit

Dim shell
Dim command

Set shell = CreateObject("WScript.Shell")
command = "powershell.exe -NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File " & Chr(34) & "C:\Users\A\.codex\manual-paste-attachments\watch-auto-longtext-fileclip.ps1" & Chr(34) & " -MinChars 2000"
shell.Run command, 0, False
