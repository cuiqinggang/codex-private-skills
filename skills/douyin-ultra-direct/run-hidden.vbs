Set sh = CreateObject("WScript.Shell")
cmd = Chr(34) & "C:\Users\A\AppData\Local\Programs\Python\Python313\pythonw.exe" & Chr(34) & " -X utf8 -B " & Chr(34) & "C:\AI\Douyin-Ultra-Direct\run.py" & Chr(34)
sh.Run cmd, 0, False