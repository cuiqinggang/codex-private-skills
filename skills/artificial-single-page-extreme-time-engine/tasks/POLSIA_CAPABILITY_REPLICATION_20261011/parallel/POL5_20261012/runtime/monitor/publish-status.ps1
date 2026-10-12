$ErrorActionPreference='Stop'
$root='C:\AI\Polsia-V5-Parallel-20261012'
$contract=Get-Content (Join-Path $root 'contracts\CEO_APPROVED_FIVE.json') -Raw -Encoding UTF8|ConvertFrom-Json
if($contract.task_id -ne 'POLSIA_CAPABILITY_REPLICATION_20261011' -or @($contract.branches).Count -ne 5){throw 'CONTRACT_INVALID'}
$jobs=@(foreach($b in $contract.branches){
 $f=Join-Path $root ('branches\'+$b.id+'\status.json')
 if(Test-Path $f){
  $s=Get-Content $f -Raw -Encoding UTF8|ConvertFrom-Json
  [ordered]@{id=$b.id;name=$b.name;status=$s.status;step=$s.step;verified_steps=$s.verified_steps;planned_steps=$s.planned_steps;eta=$null;checkpoint=$s.checkpoint;evidence=$s.evidence;issue=$s.issue;updated_utc=$s.updated_utc}
 }else{
  [ordered]@{id=$b.id;name=$b.name;status='QUEUED';step='No receipt';verified_steps=0;planned_steps=4;eta=$null;checkpoint='';evidence='';issue='MISSING_STATUS_FILE';updated_utc=''}
 }
})
$dest=Join-Path $root 'monitor\status.json'
$capture=[ordered]@{reference=$null;local=$null;reference_at=$null;local_at=$null;local_url=$null}
if(Test-Path $dest){try{$prev=Get-Content $dest -Raw|ConvertFrom-Json;if($prev.screenshots){$capture=$prev.screenshots}}catch{}}
# Live evidence: a dispatch receipt is not proof of a currently running worker.
$receiptPath=Join-Path $root 'evidence\five-dispatch-receipt.json'
$runtimeAudit=@()
if(Test-Path $receiptPath){
 try{
  foreach($r in @(Get-Content $receiptPath -Raw -Encoding UTF8 | ConvertFrom-Json)){
   $alive=$false
   try{$alive=($null -ne (Get-Process -Id ([int]$r.pid) -ErrorAction Stop))}catch{}
   $runtimeAudit+= [ordered]@{id=[string]$r.branch;dispatch_pid=[int]$r.pid;pid_exists=$alive;note=if($alive){'PID存在，未验证其仍在执行原任务'}else{'原派发进程已退出；显示的是最后一次阶段回执'}}
  }
 }catch{$alerts+='历史派发回执无法解析'}
}
$out=[ordered]@{schema='POLSIA_V5_PROCESS_VIEW_V1';generated_local=(Get-Date).ToString('yyyy-MM-dd HH:mm:ss');task_id=$contract.task_id;batch_id=$contract.batch_id;mother=[ordered]@{freeze='POLSIA-MOTHER-V008-F001';status='NOT_FULLY_VALIDATED';final_valid=$false};jobs=$jobs;runtime_audit=$runtimeAudit;alerts=@('Not final validated; see branch blockers');screenshots=$capture;scope='LOCAL_ISOLATED_READONLY'}
$tmp=$dest+'.new'
[IO.File]::WriteAllText($tmp,($out|ConvertTo-Json -Depth 9),[Text.UTF8Encoding]::new($false))
Move-Item $tmp $dest -Force
Write-Output ('PUBLISHED:'+@($jobs).Count)