Set sh = CreateObject("WScript.Shell")
cmd = Chr(34) & "C:\Users\A\AppData\Local\Programs\Python\Python313\pythonw.exe" & Chr(34) & " -X utf8 -B " & Chr(34) & "C:\AI\Douyin-Ultra-Direct\run.py" & Chr(34)
rc = sh.Run(cmd, 0, True)
If rc <> 0 Then
  sh.Popup "本次下载未完成。解析服务可能暂时不可用，请稍后重试或把链接发给 GPT。", 10, "抖音极速直下", 16
End If