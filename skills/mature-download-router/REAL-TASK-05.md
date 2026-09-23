# REAL-TASK-05 — mature-download-router v0.1.2 minimal

```text
【成熟下载工具最短调用路由｜v0.1.2最小下载成功验证｜05｜实】
TASK_TIME_ID=AED-20260923T1902+0800
TASK_SEQUENCE=05
WORKDIR=C:\AI\Mature-Download-Router-Real-Test
```

只做一件事：把一个极小公开文件交给已经安装的 aria2 1.37.0 下载成功。

禁止增加其他测试；禁止检查 hf/gh；禁止多任务；禁止自建下载逻辑；禁止修改 Windows/FlClash/Git 持久代理设置。

执行一条 PowerShell 命令链：

```powershell
$Root='C:\AI\Mature-Download-Router-Real-Test\minimal'; New-Item -ItemType Directory -Force -Path $Root | Out-Null; $Out=Join-Path $Root 'README.rst'; Remove-Item -LiteralPath $Out -Force -ErrorAction SilentlyContinue; $sw=[System.Diagnostics.Stopwatch]::StartNew(); & aria2c --no-conf=true --all-proxy='http://127.0.0.1:7890' -d $Root -o 'README.rst' 'https://raw.githubusercontent.com/aria2/aria2/release-1.37.0/README.rst'; $rc=$LASTEXITCODE; $sw.Stop(); $f=Get-Item -LiteralPath $Out -ErrorAction SilentlyContinue; if($rc -eq 0 -and $f -and $f.Length -gt 0){ Write-Host 'VALID_REAL=PASS'; Write-Host ('OUTPUT='+$f.FullName); Write-Host ('OUTPUT_BYTES='+$f.Length); Write-Host ('T_VALID_MS='+[math]::Round($sw.Elapsed.TotalMilliseconds,3)); Write-Host 'REAL_CERTIFIED=YES'; Write-Host 'ACTION=STOP_RETURN_TO_GPT_FOR_FINAL_VALIDATION'; Write-Host 'RETURN_TO_VIRTUAL=NO' } else { Write-Host 'VALID_REAL=FAIL'; Write-Host ('EXIT_CODE='+$rc); if($f){$bytes=$f.Length}else{$bytes=0}; Write-Host ('OUTPUT_BYTES='+$bytes); Write-Host ('T_VALID_MS='+[math]::Round($sw.Elapsed.TotalMilliseconds,3)); Write-Host 'REALITY_DELTA=MINIMAL_ARIA2_DOWNLOAD_FAILED'; Write-Host 'ACTION=STOP'; Write-Host 'RETURN_TO_VIRTUAL=YES' }
```

最终只回传：

```text
【成熟下载工具最短调用路由｜v0.1.2最小下载成功验证｜05｜实】
VALID_REAL=
OUTPUT=
OUTPUT_BYTES=
T_VALID_MS=
REAL_CERTIFIED=
REALITY_DELTA=
ACTION=
RETURN_TO_VIRTUAL=
【成熟下载工具最短调用路由｜v0.1.2最小下载成功验证｜05｜实】
```
