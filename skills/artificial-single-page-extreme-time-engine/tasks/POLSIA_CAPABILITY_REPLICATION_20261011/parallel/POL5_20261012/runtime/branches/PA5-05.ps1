$r='C:\AI\Polsia-V5-Parallel-20261012';$w=Join-Path $r 'save-status.ps1';$id='PA5-05';$ErrorActionPreference='Stop'
try{
& $w $id RUNNING '实测全流程中文单页本地地址' 0
$page=Invoke-WebRequest 'http://127.0.0.1:8766/index.html' -TimeoutSec 12 -ErrorAction Stop
if($page.StatusCode -ne 200){throw '监控页面HTTP状态异常'}
& $w $id RUNNING '真实HTTP200，核验五路合同与冻结' 1 'HTTP200'
$d=Invoke-RestMethod 'http://127.0.0.1:8766/status.json' -TimeoutSec 12
if(@($d.jobs).Count -ne 5 -or $d.mother.freeze -ne 'V008'){throw '五路状态不匹配'}
& $w $id RUNNING '五路数据真实可读，核验截图真实性规则' 2 'status.json'
$h=Get-Content (Join-Path $r 'monitor\index.html') -Raw -Encoding utf8
if($h -notmatch '尚无真实截图'){throw '截图缺失未明确提示'}
& $w $id DONE_SCOPED '已运行成熟组件全流程监控；真实截图仍待接入' 4 'http://127.0.0.1:8766/index.html'
}catch{& $w $id ERROR ('监控错误：'+$_.Exception.Message) 0 '' $_.Exception.Message}