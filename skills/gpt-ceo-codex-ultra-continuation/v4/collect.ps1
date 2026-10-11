param([switch]$Once)
$ErrorActionPreference='Stop'
$monitorRoot='C:\AI\Polsia-Unified-V4'
$workspace='C:\AI\Polsia-Codex-20261011'
$now=[DateTime]::UtcNow
function Kv([string]$txt,[string]$key){
 $m=[regex]::Match($txt,'(?m)^'+[regex]::Escape($key)+'=([^\r\n]+)')
 if($m.Success){return $m.Groups[1].Value.Trim()} return ''
}
function PutJson([string]$path,$data){
 $tmp= $path+'.'+$PID+'.tmp'
 ($data | ConvertTo-Json -Depth 12) | Set-Content -LiteralPath $tmp -Encoding utf8
 Move-Item -LiteralPath $tmp -Destination $path -Force
}
function Event([string]$type,[string]$key,[string]$detail){
 $evt=[ordered]@{utc=[DateTime]::UtcNow.ToString('o');event=$type;key=$key;detail=$detail}
 ($evt|ConvertTo-Json -Compress) | Add-Content -LiteralPath (Join-Path $monitorRoot 'incidents.jsonl') -Encoding utf8
}
$config=Get-Content -LiteralPath (Join-Path $monitorRoot 'config.json') -Raw -Encoding utf8|ConvertFrom-Json
$old=$null
try{$old=Get-Content -LiteralPath (Join-Path $monitorRoot 'snapshot.json') -Raw -Encoding utf8|ConvertFrom-Json}catch{}
$issues=[collections.generic.list[string]]::new()
$notes=[collections.generic.list[string]]::new()
$version='UNKNOWN';$node='UNKNOWN';$needs='';$taskState='UNKNOWN';$processes=@()
$inflight=Test-Path -LiteralPath (Join-Path $workspace 'MOTHER_EXECUTION_INFLIGHT.flag')
$needPath=Join-Path $workspace 'MOTHER_NEEDS_GPT.flag'
$versionPath=Join-Path $workspace 'VERSION_CURRENT.md'
$motherPath=Join-Path $workspace 'MOTHER_CURRENT.md'
$verTxt='';$motherTxt=''
try{
 $verTxt=Get-Content -LiteralPath $versionPath -Raw -Encoding utf8
 $motherTxt=Get-Content -LiteralPath $motherPath -Raw -Encoding utf8
 $version=Kv $verTxt 'LAST_FROZEN_VERSION'
 $node=Kv $motherTxt 'NODE_NAME'
 if(-not $node){$node=Kv $motherTxt 'NODE_ID'}
}catch{$issues.Add('MOTHER_STATE_UNREADABLE')}
if(Test-Path -LiteralPath $needPath){
 try{$needs=Kv (Get-Content -LiteralPath $needPath -Raw -Encoding utf8) 'REASON'}catch{$issues.Add('NEEDS_GPT_FLAG_UNREADABLE')}
}
try{
 $procs=@(Get-CimInstance Win32_Process -Filter "Name='codex.exe'" -ErrorAction Stop | Where-Object { $_.CommandLine -like '*Polsia-Codex-20261011*' -and ($_.CommandLine -like '* exec *' -or $_.CommandLine -like '* exec-server *') } | Select-Object -ExpandProperty ProcessId)
}catch{$notes.Add('CODEX_PROCESS_QUERY_UNAVAILABLE')}
if($procs.Count -gt 1){$issues.Add('MULTIPLE_MOTHER_CODEX_PROCESSES')}
try{$t=Get-ScheduledTask -TaskName 'Polsia-Codex-Mother-Continue' -ErrorAction Stop;$taskState=[string]$t.State;if($taskState -eq 'Disabled'){$issues.Add('ORIGINAL_TASK_DISABLED')}}catch{$notes.Add('ORIGINAL_TASK_QUERY_UNAVAILABLE')}
if($version -eq 'V008'){
 try{
  $fr=Join-Path $workspace 'nodes\CODEX-008\FREEZE.md'
  $mf=Join-Path $workspace 'nodes\CODEX-008\SHA256-MANIFEST.json'
  if((Get-FileHash -LiteralPath $fr -Algorithm SHA256).Hash -ne 'DAE228125E797E4CC2ABE3316346D37A1038148826525888AC3496B12A94676F'){$issues.Add('V008_FREEZE_HASH_MISMATCH')}
  if((Get-FileHash -LiteralPath $mf -Algorithm SHA256).Hash -ne '2F3C40F4E80B5B7C49785335FA4AE17A9F592C5BB3603082F0C2FA212CCE7EB7'){$issues.Add('V008_MANIFEST_HASH_MISMATCH')}
 }catch{$issues.Add('V008_IMMUTABLE_FACTS_UNREADABLE')}
}
if($needs -and $needs -ne 'CEO_NEXT_SCOPE_DECISION_REQUIRED'){$issues.Add('MOTHER_NEEDS_GPT_'+$needs)}
if($inflight -and $procs.Count -eq 0){$issues.Add('INFLIGHT_WITHOUT_ACTIVE_CODEX')}
if(Test-Path -LiteralPath (Join-Path $monitorRoot 'test_fault.flag')){$issues.Add('TEST_ONLY_INJECTED_MONITOR_FAULT')}
$latestLog=$null;$logAge=-1
try{
 $latestLog=Get-ChildItem -LiteralPath (Join-Path $workspace 'continuation_logs') -Filter 'Codex-*.log' -File | Sort-Object LastWriteTimeUtc -Descending | Select-Object -First 1
 if($latestLog){$logAge=[math]::Round(($now-$latestLog.LastWriteTimeUtc).TotalSeconds)}
}catch{$notes.Add('LOG_QUERY_UNAVAILABLE')}
if($procs.Count -gt 0 -and $logAge -gt 900){$notes.Add('RUNNING_LOG_STALE_OVER_15_MINUTES_INVESTIGATE')}
$rootStatus='READY'
if($procs.Count -gt 0){$rootStatus='RUNNING'}
elseif($needs -eq 'CEO_NEXT_SCOPE_DECISION_REQUIRED'){$rootStatus='WAITING_CEO'}
elseif($inflight){$rootStatus='UNKNOWN_INFLIGHT'}
elseif($version -eq 'V008'){$rootStatus='FROZEN'}
if($issues.Count -gt 0){$rootStatus='ALERT'}
$branches=@()
foreach($lane in $config.lanes){
 $status=[string]$lane.default_status;$stamp='';$proof='';$detail=[string]$lane.next
 $file=Join-Path $monitorRoot ('branches\'+$lane.id+'\status.json')
 if(Test-Path -LiteralPath $file){
  try{
   $entry=Get-Content -LiteralPath $file -Raw -Encoding utf8 | ConvertFrom-Json
   $status=[string]$entry.status;$stamp=[string]$entry.utc;$proof=[string]$entry.proof
   if($entry.detail){$detail=[string]$entry.detail}
   if($status -eq 'RUNNING' -and $stamp){
    if(([DateTime]::UtcNow-([DateTime]$stamp).ToUniversalTime()).TotalMinutes -gt 10){$status='STALE';$issues.Add('BRANCH_'+$lane.id+'_STALE')}
   }
  }catch{$status='ERROR';$issues.Add('BRANCH_'+$lane.id+'_INVALID_STATE')}
 }
 if($lane.id -eq 'MONITOR'){$status='MONITORING';$detail='Windows原生计划任务定期快照＋可视窗口'}
 if($status -eq 'ERROR' -or $status -eq 'STALE'){$issues.Add('BRANCH_'+$lane.id+'_ERROR')}
 $branches+= [ordered]@{id=$lane.id;name=$lane.name;status=$status;utc=$stamp;proof=$proof;detail=$detail}
}
$newKeys=@($issues | Select-Object -Unique | Sort-Object)
$oldKeys=@();if($old -and $old.alert_keys){$oldKeys=@($old.alert_keys)}
foreach($k in $newKeys){if($k -notin $oldKeys){Event 'DETECTED' $k 'Detected by local V4 native scheduled snapshot; no blind production restart'}}
foreach($k in $oldKeys){if($k -notin $newKeys){Event 'CLEARED' $k 'Latest valid snapshot no longer reproduces issue; incident history retained'}}
$snapshot=[ordered]@{
 schema='POLSIA_UNIFIED_MONITOR_V4';utc=[DateTime]::UtcNow.ToString('o');
 task_id=$config.task_id;freeze=$version;node=$node;root_status=$rootStatus;
 root_reason=$needs;root_pid=@($procs);inflight=$inflight;
 scheduler=$taskState;log_name=if($latestLog){$latestLog.Name}else{''};log_age_sec=$logAge;
 alert_keys=$newKeys;notes=@($notes);branches=$branches;
 capacity=$config.native_capacity;source='LIVE_LOCAL_READ_ONLY_EXCEPT_ISOLATED_TEST_EVENTS';
}
PutJson (Join-Path $monitorRoot 'snapshot.json') $snapshot
if($Once){$snapshot|ConvertTo-Json -Compress -Depth 12}