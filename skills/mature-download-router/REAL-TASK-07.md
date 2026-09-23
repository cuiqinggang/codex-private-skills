# REAL-TASK-07 — exact prechecked sample

【成熟下载工具最短调用路由｜v0.1.3预验证样本限时复现｜07｜实】
TASK_TIME_ID=AED-20260923T1902+0800
TASK_SEQUENCE=07
WORKDIR=C:\AI\Mature-Download-Router-Real-Test
PRE_RELEASE_REAL_FETCH=PASS

这个资源已经由 GPT 侧真实取件成功、写入共同私库并回读一致。

只做这一件事：用本机已有 curl.exe 复现同一个 665-byte 文件。

禁止换 URL。
禁止换工具。
禁止增加其他测试。
禁止修改持久代理设置。
禁止分析下载器。

PowerShell:

$Root='C:\AI\Mature-Download-Router-Real-Test\v013-prechecked'
New-Item -ItemType Directory -Force -Path $Root | Out-Null
$Out=Join-Path $Root 'config.json'
Remove-Item -LiteralPath $Out -Force -ErrorAction SilentlyContinue
$Url='https://huggingface.co/openai-community/gpt2/resolve/main/config.json'
$ExpectedBytes=665
$ExpectedSha='0daed7749b4f02b8f76240d5444551d7b08712dab4d0adb8239c56ba823bb7b4'
$sw=[System.Diagnostics.Stopwatch]::StartNew()
& curl.exe -L --fail --silent --show-error --proxy 'http://127.0.0.1:7890' --connect-timeout 10 --max-time 30 --output $Out $Url
$rc=$LASTEXITCODE
$sw.Stop()
$f=Get-Item -LiteralPath $Out -ErrorAction SilentlyContinue
if($f){$bytes=$f.Length}else{$bytes=0}
if($f){$sha=(Get-FileHash -LiteralPath $Out -Algorithm SHA256).Hash.ToLowerInvariant()}else{$sha=''}
$t=[math]::Round($sw.Elapsed.TotalMilliseconds,3)
if($rc -eq 0 -and $bytes -eq $ExpectedBytes -and $sha -eq $ExpectedSha -and $t -le 30000){
  Write-Host 'VALID_REAL=PASS'
  Write-Host ('OUTPUT='+$Out)
  Write-Host ('OUTPUT_BYTES='+$bytes)
  Write-Host ('SHA256='+$sha)
  Write-Host ('T_VALID_MS='+$t)
  Write-Host 'LOCAL_REAL_CERTIFIED=YES'
  Write-Host 'ACTION=STOP_RETURN_TO_GPT_FOR_FINAL_VALIDATION'
  Write-Host 'RETURN_TO_VIRTUAL=NO'
} else {
  Write-Host 'VALID_REAL=FAIL'
  Write-Host ('EXIT_CODE='+$rc)
  Write-Host ('OUTPUT_BYTES='+$bytes)
  Write-Host ('SHA256='+$sha)
  Write-Host ('T_VALID_MS='+$t)
  Write-Host 'LOCAL_REAL_CERTIFIED=NO'
  Write-Host 'REALITY_DELTA=PRECHECKED_SAMPLE_LOCAL_REPRO_FAIL'
  Write-Host 'ACTION=STOP'
  Write-Host 'RETURN_TO_VIRTUAL=YES'
}

最终只回传：
【成熟下载工具最短调用路由｜v0.1.3预验证样本限时复现｜07｜实】
VALID_REAL=
OUTPUT=
OUTPUT_BYTES=
SHA256=
T_VALID_MS=
LOCAL_REAL_CERTIFIED=
REALITY_DELTA=
ACTION=
RETURN_TO_VIRTUAL=
【成熟下载工具最短调用路由｜v0.1.3预验证样本限时复现｜07｜实】
