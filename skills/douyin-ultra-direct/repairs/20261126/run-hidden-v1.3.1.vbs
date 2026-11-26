Set sh = CreateObject("WScript.Shell")
cmd = Chr(34) & "C:\Users\A\AppData\Local\Programs\Python\Python313\pythonw.exe" & Chr(34) & " -X utf8 -B " & Chr(34) & "C:\AI\Douyin-Ultra-Direct\run-v1.3.1.py" & Chr(34) & " --interactive"
rc = sh.Run(cmd, 0, True)
