# REAL-TASK-06 — one minimal mature-tool download

```text
【成熟下载工具最短调用路由｜最小成熟工具下载成功验证｜06｜实】
TASK_TIME_ID=AED-20260923T1902+0800
TASK_SEQUENCE=06
WORKDIR=C:\AI\Mature-Download-Router-Real-Test
```

只做一件事：

> 使用本机已有 curl.exe，通过已知现有代理 http://127.0.0.1:7890，下载 Hugging Face 上的一个 665-byte config.json。

不要检查 aria2/hf/gh；不要多任务；不要修改代理；不要增加其他测试。

执行：

```powershell
$Root='C:\AI\Mature-Download-Router-Real-Test\minimal-curl'
New-Item -ItemType Directory -Force -Path $Root | Out-Null
$Out=Join-Path $Root 'config.json'
Remove-Item -LiteralPath $Out -Force -ErrorAction SilentlyContinue
$Url='https://huggingface.co/openai-community/gpt2/resolve/main/config.json'
$sw=[System.Diagnostics.Stopwatch]::StartNew()
& curl.exe -L --fail --silent --show-error --proxy 'http://127.0.0.1:7890' --connect-timeout 10 --max-time 30 --output $Out $Url
$rc=$LASTEXITCODE
$sw.Stop()
$f=Get-Item -LiteralPath $Out -ErrorAction SilentlyContinue
if($rc -eq 0 -and $f -and $f.Length -gt 0){
  Write-Host 'VALID_REAL=PASS'
  Write-Host ('OUTPUT='+$f.FullName)
  Write-Host ('OUTPUT_BYTES='+$f.Length)
  Write-Host ('T_VALID_MS='+[math]::Round($sw.Elapsed.TotalMilliseconds,3))
  Write-Host 'REAL_CERTIFIED=YES'
  Write-Host 'ACTION=STOP_RETURN_TO_GPT_FOR_FINAL_VALIDATION'
  Write-Host 'RETURN_TO_VIRTUAL=NO'
} else {
  if($f){$bytes=$f.Length}else{$bytes=0}
  Write-Host 'VALID_REAL=FAIL'
  Write-Host ('EXIT_CODE='+$rc)
  Write-Host ('OUTPUT_BYTES='+$bytes)
  Write-Host ('T_VALID_MS='+[math]::Round($sw.Elapsed.TotalMilliseconds,3))
  Write-Host 'REALITY_DELTA=MINIMAL_CURL_DOWNLOAD_FAILED'
  Write-Host 'ACTION=STOP'
  Write-Host 'RETURN_TO_VIRTUAL=YES'
}
```

最终只回传：

```text
【成熟下载工具最短调用路由｜最小成熟工具下载成功验证｜06｜实】
VALID_REAL=
OUTPUT=
OUTPUT_BYTES=
T_VALID_MS=
REAL_CERTIFIED=
REALITY_DELTA=
ACTION=
RETURN_TO_VIRTUAL=
【成熟下载工具最短调用路由｜最小成熟工具下载成功验证｜06｜实】
```
