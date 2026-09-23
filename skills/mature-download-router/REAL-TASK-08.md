# REAL-TASK-08 — mature-download-router v0.1.4

【成熟下载工具最短调用路由｜v0.1.4预跑成熟样本本地复现｜08｜实】

TASK_TIME_ID=AED-20260923T1902+0800
TASK_SEQUENCE=08
METHOD=first-principles-physical-limit-convergence@4.6.1
REALITY_FOUNDATION=local-ai-reality-foundation@1.1.6
SKILL=mature-download-router@0.1.4
GPT_DISPATCH_TIMESTAMP=2026-09-23T23:55:29+08:00
WORKDIR=C:\AI\Mature-Download-Router-Real-Test

本轮只复现一个已经由 GPT 侧真实取件成功、保存并回读验证的公开小文件。

冻结事实：

```text
TOOL=hf
LOCAL_VERSION=1.19.0
REPO=openai-community/gpt2
FILE=config.json
REVISION=607a30d783dfa663caf39e06633721c8d4cfcd7e
EXPECTED_BYTES=665
EXPECTED_SHA256=0daed7749b4f02b8f76240d5444551d7b08712dab4d0adb8239c56ba823bb7b4
HTTP_PROXY=http://127.0.0.1:7890
HTTPS_PROXY=http://127.0.0.1:7890
TIME_LIMIT=30000ms
```

禁止：
- 换 URL / repo / revision / file；
- 换工具；
- 调用 curl.exe 或 Invoke-WebRequest；
- 增加 fallback；
- 多任务；
- 修改持久代理设置；
- 安装或升级工具；
- 重新设计方案。

直接执行这一条冻结动作：

```powershell
$Root='C:\AI\Mature-Download-Router-Real-Test\v014-hf'
New-Item -ItemType Directory -Force -Path $Root | Out-Null
$Out=Join-Path $Root 'config.json'
Remove-Item -LiteralPath $Out -Force -ErrorAction SilentlyContinue

$oldHttp=$env:HTTP_PROXY
$oldHttps=$env:HTTPS_PROXY

$env:HTTP_PROXY='http://127.0.0.1:7890'
$env:HTTPS_PROXY='http://127.0.0.1:7890'

$sw=[System.Diagnostics.Stopwatch]::StartNew()

& hf download openai-community/gpt2 config.json --revision 607a30d783dfa663caf39e06633721c8d4cfcd7e --local-dir $Root --force-download

$rc=$LASTEXITCODE
$sw.Stop()

if($null -eq $oldHttp){ Remove-Item Env:HTTP_PROXY -ErrorAction SilentlyContinue } else { $env:HTTP_PROXY=$oldHttp }
if($null -eq $oldHttps){ Remove-Item Env:HTTPS_PROXY -ErrorAction SilentlyContinue } else { $env:HTTPS_PROXY=$oldHttps }

$f=Get-Item -LiteralPath $Out -ErrorAction SilentlyContinue
if($f){
  $bytes=$f.Length
  $sha=(Get-FileHash -LiteralPath $Out -Algorithm SHA256).Hash.ToLowerInvariant()
} else {
  $bytes=0
  $sha=''
}
$t=[math]::Round($sw.Elapsed.TotalMilliseconds,3)

if($rc -eq 0 -and $bytes -eq 665 -and $sha -eq '0daed7749b4f02b8f76240d5444551d7b08712dab4d0adb8239c56ba823bb7b4' -and $t -le 30000){
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
  Write-Host 'REALITY_DELTA=PREEXECUTED_HF_SAMPLE_LOCAL_REPRO_FAIL'
  Write-Host 'ACTION=STOP'
  Write-Host 'RETURN_TO_VIRTUAL=YES'
}
```

最终只回传：

```text
【成熟下载工具最短调用路由｜v0.1.4预跑成熟样本本地复现｜08｜实】
VALID_REAL=
OUTPUT=
OUTPUT_BYTES=
SHA256=
T_VALID_MS=
LOCAL_REAL_CERTIFIED=
REALITY_DELTA=
ACTION=
RETURN_TO_VIRTUAL=
【成熟下载工具最短调用路由｜v0.1.4预跑成熟样本本地复现｜08｜实】
```