$ErrorActionPreference='Stop'
$root='C:\AI\Polsia-V5-Parallel-20261012\monitor'
$dest=Join-Path $root 'status.json'
$api='repos/cuiqinggang/codex-private-skills/contents/skills/artificial-single-page-extreme-time-engine/tasks/POLSIA_CAPABILITY_REPLICATION_20261011/parallel/POL5_20261012/clone4'
$batch='PCL4_20261012'
$names=@('网站运行与数据库恢复','历史九类业务能力接入','网站前端与执行交互','截图对标及独立审核')
$expected=@('b69ba0dc9d7f2f1b8a9c8ac54d534ee47634007c','bea3869f4656deacbe0e3dbd8d0a8e01f00423e4','e4627643f5a48a7e13b8096d68d21a0bf54abf9b','33d859fbe2e0ac0c45c40aecdae0511dfa971235')
$now=[DateTime]::UtcNow
$prev=$null
if(Test-Path $dest){try{$prev=Get-Content $dest -Raw -Encoding UTF8 | ConvertFrom-Json}catch{}}
$history=Join-Path $root 'status-pa5-history.json'
if((-not (Test-Path $history)) -and $prev -and $prev.schema -eq 'POLSIA_V5_PROCESS_VIEW_V1'){Copy-Item $dest $history}
$remote=@();$sourceOk=$false;$sourceError=''
try{$resp=(& gh api ("${api}?ref=main") 2>$null | Out-String);if($LASTEXITCODE -ne 0){throw 'gh api failed'};$remote=@($resp|ConvertFrom-Json);$sourceOk=(@($remote).Count -ge 4);if(-not $sourceOk){throw 'contract listing incomplete'}}catch{$sourceError=$_.Exception.Message}
$jobs=@();$alerts=@()
if(-not $sourceOk){$alerts+=('GitHub合同源不可核验：'+$sourceError)}
for($i=0;$i -lt 4;$i++){
 $id='PCL-'+('{0:D2}' -f ($i+1));$fn=$id+'_TASK.md'
 $entry=@($remote|Where-Object {$_.name -eq $fn}|Select-Object -First 1)
 $url='https://github.com/cuiqinggang/codex-private-skills/blob/main/skills/artificial-single-page-extreme-time-engine/tasks/POLSIA_CAPABILITY_REPLICATION_20261011/parallel/POL5_20261012/clone4/'+$fn
 $verified=$sourceOk -and $entry.Count -eq 1 -and $entry[0].sha -eq $expected[$i]
 $status=if($verified){'ASSIGNED_NOT_YET_STARTED'}else{'UNKNOWN'}
 $step=if($verified){'合同已发布并回读；尚无新执行器启动证据'}else{'合同远端当前无法核验，禁止据此判断正在执行'}
 $evidence=if($verified){'GitHub合同SHA '+$entry[0].sha.Substring(0,12)}else{'此前合同SHA '+$expected[$i].Substring(0,12)+'（非当前证明）'}
 $issue=if($verified){''}else{'合同缺失、SHA已变化或GitHub不可用，需重新核对'}
 $receiptName=$id+'_STATUS.json'
 $receipt=@($remote|Where-Object {$_.name -eq $receiptName}|Select-Object -First 1)
 $lastHeartbeat=$null;$checkpoint='';$runtimeProof=$false
 if($verified -and $receipt.Count -eq 1){
  try {
   $body=(& gh api ("${api}/"+$receiptName+'?ref=main') --jq .content 2>$null | Out-String)
   if($LASTEXITCODE -ne 0){throw 'GitHub receipt fetch failed'}
   $rec=([Text.Encoding]::UTF8.GetString([Convert]::FromBase64String(($body -replace '\s','')))|ConvertFrom-Json)
   if($rec.task_id -ne 'POLSIA_CAPABILITY_REPLICATION_20261011' -or $rec.node_id -ne $id){throw 'receipt id mismatch'}
   $step=if($rec.step){[string]$rec.step}else{'执行回执已登记，尚无步骤说明'}
   $checkpoint=[string]$rec.checkpoint
   $lastHeartbeat=[string]$rec.heartbeat_utc
   $evidence=if($rec.evidence_url){[string]$rec.evidence_url}else{$evidence}
   $fresh=$false
   try{$fresh=((($now-[DateTime]::Parse($lastHeartbeat).ToUniversalTime()).TotalSeconds) -ge 0 -and (($now-[DateTime]::Parse($lastHeartbeat).ToUniversalTime()).TotalSeconds) -le 180)}catch{}
   if($rec.status -eq 'RUNNING' -and $rec.runtime_verified -eq $true -and $fresh){$status='RUNNING';$runtimeProof=$true}
   elseif($rec.status -eq 'RUNNING'){$status='STALE';$issue='执行声称运行，但缺少3分钟内有效心跳及独立运行证明'}
   elseif($rec.status -eq 'DONE' -and $rec.independent_verified -eq $true -and $rec.evidence_url){$status='DONE'}
   elseif($rec.status -eq 'DONE'){$status='VERIFYING';$issue='已报告完成，缺少独立验收证据'}
   elseif(@('WAITING','BLOCKED','FAILED','VERIFYING','FROZEN').Contains([string]$rec.status)){$status=[string]$rec.status}
   else{$status='UNKNOWN';$issue='回执状态未知'}
  } catch {$status='UNKNOWN';$issue='执行回执无效或无法读取：'+$_.Exception.Message;$alerts+=($id+' 回执校验失败')}
 }
 $jobs+= [ordered]@{id=$id;name=$names[$i];status=$status;step=$step;planned_steps=0;verified_steps=0;eta=$null;checkpoint=$checkpoint;evidence=$evidence;issue=$issue;contract_url=$url;contract_sha=$expected[$i];source_verified=$verified;last_heartbeat_utc=$lastHeartbeat;runtime_verified=$runtimeProof}
}
$shots=if($prev -and $prev.screenshots){$prev.screenshots}else{[ordered]@{reference=$null;local=$null;reference_at=$null;local_at=$null;local_url=$null}}
$out=[ordered]@{schema='AI_COMPANY_MONITOR_V1_0';version='1.0.0';generated_local=(Get-Date).ToString('yyyy-MM-dd HH:mm:ss');source_checked_utc=$now.ToString('o');source_state=if($sourceOk){'GITHUB_CONTRACTS_VERIFIED'}else{'GITHUB_UNAVAILABLE_OR_INCOMPLETE'};task_id='POLSIA_CAPABILITY_REPLICATION_20261011';batch_id=$batch;mother=[ordered]@{freeze='POLSIA-MOTHER-V008-F001';status='NOT_FULLY_VALIDATED';final_valid=$false};jobs=$jobs;runtime_audit=@();alerts=$alerts;screenshots=$shots;scope='READONLY_MONITOR_EXTERNAL_OWNER';history_file='status-pa5-history.json'}
$tmp=$dest+'.v1new'
[IO.File]::WriteAllText($tmp,($out|ConvertTo-Json -Depth 12),[Text.UTF8Encoding]::new($false))
Move-Item $tmp $dest -Force
'MONITOR_V1_PUBLISHED;PCL='+$jobs.Count+';GITHUB_VERIFIED='+@($jobs|Where-Object source_verified).Count