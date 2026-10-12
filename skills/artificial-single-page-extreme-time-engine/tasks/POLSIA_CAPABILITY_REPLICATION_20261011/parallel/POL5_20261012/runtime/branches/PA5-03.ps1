$r='C:\AI\Polsia-V5-Parallel-20261012';$w=Join-Path $r 'save-status.ps1';$id='PA5-03';$ErrorActionPreference='Stop'
try{
& $w $id RUNNING '只读核验已安装的业务工作流与权限' 0
$s=@(@{name='n8n健康';url='http://127.0.0.1:5678/healthz'},@{name='n8n管理';url='http://127.0.0.1:5678/rest/workflows'},@{name='模型桥';url='http://127.0.0.1:8788/healthz'})
$res=@(foreach($x in $s){$code=0;try{$z=Invoke-WebRequest $x.url -TimeoutSec 7 -ErrorAction Stop;$code=[int]$z.StatusCode}catch{try{$code=[int]$_.Exception.Response.StatusCode}catch{}};[ordered]@{name=$x.name;http=$code}})
& $w $id RUNNING '三处接口已实测，按授权与真实执行分层判断' 2 'workflow-probe.json'
$path=Join-Path $r 'branches\PA5-03-workflow-probe.json'
[IO.File]::WriteAllText($path,([ordered]@{time=(Get-Date).ToString('o');services=$res;real_workflow_executions=0}|ConvertTo-Json -Depth 7),[Text.UTF8Encoding]::new($false))
$api=@($res|Where-Object {$_.name -eq 'n8n管理'})[0]
if($api.http -in @(401,403)){& $w $id BLOCKED '工作流管理未授权，保留问题继续其它分支' 3 'PA5-03-workflow-probe.json' ('正式管理接口HTTP'+$api.http)}
else{& $w $id DONE_SCOPED '只读接口核验完成，工作流实际执行尚未认证' 4 'PA5-03-workflow-probe.json'}
}catch{& $w $id ERROR ('工作流检查异常：'+$_.Exception.Message) 0 '' $_.Exception.Message}