param([ValidateRange(1,5)][int]$FirstRound=1,[ValidateRange(1,5)][int]$LastRound=5)
$ErrorActionPreference='Stop'
if($LastRound -lt $FirstRound){throw 'INVALID_ROUND_RANGE'}
$Root=$PSScriptRoot
$freeze=Get-Content (Join-Path $Root 'REALITY-F002.json') -Raw -Encoding UTF8 | ConvertFrom-Json
if($freeze.task_id -ne 'HERMES-ECO-20261014' -or $freeze.contract_ref -ne 'F002' -or $freeze.prior_attempt_reconciled -ne $true){throw 'PRIOR_ATTEMPT_OR_FREEZE_NOT_RECONCILED'}
foreach($name in @('Invoke-Acceptance.ps1','prepare.py','evidence_guard.py')){
 $expected=$freeze.source_sha256.PSObject.Properties[$name].Value
 if(-not $expected -or (Get-FileHash (Join-Path $Root $name)).Hash.ToLowerInvariant() -ne $expected){throw 'FROZEN_SOURCE_HASH_MISMATCH'}
}
$fixtureSha=(Get-FileHash (Join-Path $Root 'FIXTURE-MANIFEST.json')).Hash.ToLowerInvariant()
if($fixtureSha -ne $freeze.fixtures_sha256){throw 'FIXTURE_FREEZE_MISMATCH'}
$Py='C:\Users\A\.hermes\hermes-agent\venv\Scripts\python.exe'
$DataPath='C:\Users\A\.hermes'
$src=Get-Content -LiteralPath 'C:\Users\A\Hermes_Windows_Native_014\launcher\start-hermes-openwebui.ps1' -Raw
$ast=[System.Management.Automation.Language.Parser]::ParseInput($src,[ref]$null,[ref]$null)
$fn=$ast.Find({param($n) $n -is [System.Management.Automation.Language.FunctionDefinitionAst] -and $n.Name -eq 'Get-ApiServerHeaders'},$true)
if(-not $fn){throw 'EXISTING_AUTH_READER_MISSING'}
. ([scriptblock]::Create($fn.Extent.Text))
$Headers=Get-ApiServerHeaders
$Base='http://127.0.0.1:8642'
function Save-Text($Path,$Value){
 $temporary=$Path+'.'+$PID+'.tmp'
 [IO.File]::WriteAllText($temporary,[string]$Value,(New-Object Text.UTF8Encoding($false)))
 Move-Item -LiteralPath $temporary -Destination $Path -Force
}
function Save-Json($Path,$Value){Save-Text $Path ($Value|ConvertTo-Json -Depth 30)}
$expectedConfig=[string]$freeze.config_sha256
$results=@()
try {
 $health=Invoke-RestMethod "$Base/health/detailed" -Headers $Headers -TimeoutSec 15
 if($health.status -ne 'ok' -or $health.readiness.status -ne 'ok'){throw 'GATEWAY_NOT_READY'}
 if($health.gateway_busy){throw 'GATEWAY_BUSY_NO_DISPATCH'}
 $sets=Invoke-RestMethod "$Base/v1/toolsets" -Headers $Headers -TimeoutSec 15
 Save-Json (Join-Path $Root 'NATIVE-TOOLSETS-AFTER.json') $sets
 foreach($name in @('web','delegation','todo','session_search','cronjob')){if(-not @($sets.data|Where-Object {$_.name -eq $name -and $_.enabled}).Count){throw "TOOLSET_NOT_ACTIVE_$name"}}
 for($round=$FirstRound;$round -le $LastRound;$round++) {
  $Dir=Join-Path $Root ('R{0:d2}' -f $round)
  foreach($receipt in @('round-result.json','request-1.json','request-2.json','ack-1.json','ack-2.json')){
   if(Test-Path (Join-Path $Dir $receipt)){throw 'PRIOR_RECEIPT_RECONCILE_FIRST_NO_REDISPATCH'}
  }
  if((Get-FileHash 'C:\Users\A\.hermes\config.yaml').Hash.ToLowerInvariant() -ne $expectedConfig){throw 'CONFIG_CHANGED_STOP_BATCH'}
  $wall=[Diagnostics.Stopwatch]::StartNew();$accepted=(Get-Date).ToUniversalTime().ToString('o')
  $phaseResults=@();$activeRun='';$ok=$false;$errorType=$null;$errorMessage=$null;$postPending=$false
  try {
   foreach($phase in @(1,2)) {
    $Prompt=Get-Content (Join-Path $Dir "prompt-$phase.txt") -Raw -Encoding UTF8
    $body=@{input=$Prompt;model='DeepSeek-V4.1-Flash';instructions='Follow the explicit task write/read scope. Use only real tools. Never access credentials or other users sessions. No purchases, installs, scheduling, production changes, or browser actions.'}|ConvertTo-Json -Compress
    $bytes=[Text.Encoding]::UTF8.GetBytes($body)
    $h=@{};foreach($key in $Headers.Keys){$h[$key]=$Headers[$key]}
    $h['Idempotency-Key']='hermes-eco-20261014-r'+$round+'-p'+$phase+'-f002'
    Save-Text (Join-Path $Dir "request-$phase.json") $body
    $postPending=$true
    $ack=Invoke-RestMethod "$Base/v1/runs" -Method Post -Headers $h -Body $bytes -ContentType 'application/json; charset=utf-8' -TimeoutSec 30
    $activeRun=$ack.run_id
    if(-not $activeRun){throw 'MISSING_ADMISSION_RECEIPT_RECONCILE_FIRST'}
    $postPending=$false
    Save-Json (Join-Path $Dir "ack-$phase.json") @{run_id=$activeRun;ack=$ack;accepted_utc=$accepted;elapsed_ms=$wall.ElapsedMilliseconds}
    Write-Output ('RUN_STARTED round={0} phase={1} run_id={2}' -f $round,$phase,$activeRun)
    $deadline=(Get-Date).AddMinutes(12)
    do {
     Start-Sleep -Seconds 5
     $state=Invoke-RestMethod "$Base/v1/runs/$activeRun" -Headers $Headers -TimeoutSec 20
     Save-Json (Join-Path $Dir "run-$phase.json") $state
     if($state.status -in @('completed','failed','cancelled','interrupted','blocked','awaiting_approval','waiting_for_approval')){break}
     if((Get-Date) -gt $deadline){throw 'RUN_TIMEOUT_REQUIRES_RECONCILIATION'}
    } while($true)
    if($state.status -ne 'completed'){throw ('RUN_NOT_COMPLETED_'+$state.status)}
    $sse=Invoke-WebRequest "$Base/v1/runs/$activeRun/events" -Headers $Headers -UseBasicParsing -TimeoutSec 20
    Save-Text (Join-Path $Dir "events-$phase.sse") $sse.Content
    if((Get-FileHash 'C:\Users\A\.hermes\config.yaml').Hash.ToLowerInvariant() -ne $expectedConfig){throw 'CONFIG_CHANGED_DURING_RUN'}
    $replay=Invoke-WebRequest "$Base/v1/runs" -Method Post -Headers $h -Body $bytes -ContentType 'application/json; charset=utf-8' -UseBasicParsing -TimeoutSec 20
    $replayed=$replay.Content|ConvertFrom-Json
    if($replayed.run_id -ne $activeRun -or $replay.Headers['Idempotency-Replayed'] -ne 'true'){throw 'IDEMPOTENCY_RECEIPT_FAILED'}
    Save-Json (Join-Path $Dir "idempotency-$phase.json") @{same_run_id=$true;replayed=$true;run_id=$activeRun}
    & $Py (Join-Path $Root 'prepare.py') grade $Dir $phase
    if($LASTEXITCODE -ne 0){throw "INDEPENDENT_GRADE_FAILED_PHASE_$phase"}
    $phaseResults+=@{phase=$phase;run_id=$activeRun;status='PASS';usage=$state.usage}
    $activeRun=''
   }
   $ok=$true
  } catch {
   $errorType=$_.Exception.GetType().Name;$errorMessage=$_.Exception.Message
   if($postPending){Save-Json (Join-Path $Dir 'DISPATCH-UNKNOWN.json') @{state='UNKNOWN';action='RECONCILE_ONLY';automatic_retry=$false}}
   if($activeRun){
    # Stop only this acceptance run; never stop the gateway or unrelated sessions.
    try { $stop=Invoke-RestMethod "$Base/v1/runs/$activeRun/stop" -Method Post -Headers $Headers -ContentType 'application/json' -Body '{}' -TimeoutSec 15;Save-Json (Join-Path $Dir 'scoped-stop.json') $stop } catch {}
   }
  }
  $wall.Stop()
  $result=@{round=$round;pass=$ok;full_wall_ms=$wall.ElapsedMilliseconds;accepted_utc=$accepted;phases=$phaseResults;error_type=$errorType;error=$errorMessage;contract_ref='F002';config_sha256=$expectedConfig;fixture_sha256=$fixtureSha}
  Save-Json (Join-Path $Dir 'round-result.json') $result;$results+=$result
  $auditText=(& $Py (Join-Path $Root 'evidence_guard.py') $Root --through $round --require-current-pass) -join "`n"
  $auditExit=$LASTEXITCODE
  if($auditText){Save-Text (Join-Path $Root 'BATCH-RESULT.json') $auditText}
  if($auditExit -ne 0){throw 'RECEIPT_AUDIT_NOT_PASSED_NO_REDISPATCH'}
  Write-Output ($result|ConvertTo-Json -Depth 12 -Compress)
  if(-not $ok){throw 'BATCH_STOPPED_FOR_REPAIR_NO_FALSE_PASS'}
 }
} finally {$Headers=$null}
