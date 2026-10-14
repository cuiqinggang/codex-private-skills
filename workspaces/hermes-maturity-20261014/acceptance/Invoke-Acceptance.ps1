param([int]$FirstRound=1,[int]$LastRound=5)
$ErrorActionPreference='Stop'
$Root=$PSScriptRoot
$Py='C:\Users\A\.hermes\hermes-agent\venv\Scripts\python.exe'
$DataPath='C:\Users\A\.hermes'
$src=Get-Content -LiteralPath 'C:\Users\A\Hermes_Windows_Native_014\launcher\start-hermes-openwebui.ps1' -Raw
$ast=[System.Management.Automation.Language.Parser]::ParseInput($src,[ref]$null,[ref]$null)
$fn=$ast.Find({param($n) $n -is [System.Management.Automation.Language.FunctionDefinitionAst] -and $n.Name -eq 'Get-ApiServerHeaders'},$true)
if(-not $fn){throw 'EXISTING_AUTH_READER_MISSING'}
. ([scriptblock]::Create($fn.Extent.Text))
$Headers=Get-ApiServerHeaders
$Base='http://127.0.0.1:8642'
function Save-Json($Path,$Value){[IO.File]::WriteAllText($Path,($Value|ConvertTo-Json -Depth 30),(New-Object Text.UTF8Encoding($false)))}
function Save-Text($Path,$Value){[IO.File]::WriteAllText($Path,[string]$Value,(New-Object Text.UTF8Encoding($false)))}
$delta=Get-Content (Join-Path $Root 'CONFIG-DELTA.json') -Raw -Encoding UTF8|ConvertFrom-Json
$results=@()
try {
 $health=Invoke-RestMethod "$Base/health/detailed" -Headers $Headers -TimeoutSec 15
 if($health.gateway_busy){throw 'GATEWAY_BUSY_NO_DISPATCH'}
 $sets=Invoke-RestMethod "$Base/v1/toolsets" -Headers $Headers -TimeoutSec 15
 Save-Json (Join-Path $Root 'NATIVE-TOOLSETS-AFTER.json') $sets
 foreach($name in @('web','delegation','todo','session_search','cronjob')){if(-not @($sets.data|Where-Object {$_.name -eq $name -and $_.enabled}).Count){throw "TOOLSET_NOT_ACTIVE_$name"}}
 for($round=$FirstRound;$round -le $LastRound;$round++) {
  $Dir=Join-Path $Root ('R{0:d2}' -f $round)
  if(Test-Path (Join-Path $Dir 'round-result.json')){throw 'ROUND_ALREADY_ATTEMPTED_RECONCILE_FIRST'}
  if((Get-FileHash 'C:\Users\A\.hermes\config.yaml').Hash.ToLowerInvariant() -ne $delta.after_sha256){throw 'CONFIG_CHANGED_STOP_BATCH'}
  $wall=[Diagnostics.Stopwatch]::StartNew();$accepted=(Get-Date).ToUniversalTime().ToString('o')
  $phaseResults=@();$activeRun='';$ok=$false
  try {
   foreach($phase in @(1,2)) {
    $Prompt=Get-Content (Join-Path $Dir "prompt-$phase.txt") -Raw -Encoding UTF8
    $body=@{input=$Prompt;model='DeepSeek-V4.1-Flash';instructions='Follow the explicit task write/read scope. Use only real tools. Never access credentials or other users sessions. No purchases, installs, scheduling, production changes, or browser actions.'}|ConvertTo-Json -Compress
    $bytes=[Text.Encoding]::UTF8.GetBytes($body)
    $h=@{};foreach($key in $Headers.Keys){$h[$key]=$Headers[$key]}
    $h['Idempotency-Key']='hermes-eco-20261014-r'+$round+'-p'+$phase+'-f001'
    Save-Text (Join-Path $Dir "request-$phase.json") $body
    $ack=Invoke-RestMethod "$Base/v1/runs" -Method Post -Headers $h -Body $bytes -ContentType 'application/json; charset=utf-8' -TimeoutSec 30
    $activeRun=$ack.run_id
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
    $sse=Invoke-WebRequest "$Base/v1/runs/$activeRun/events" -Headers $Headers -UseBasicParsing -TimeoutSec 20
    Save-Text (Join-Path $Dir "events-$phase.sse") $sse.Content
    if($state.status -ne 'completed'){throw ('RUN_NOT_COMPLETED_'+$state.status)}
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
   if($activeRun){
    # Stop only this acceptance run; never stop the gateway or unrelated sessions.
    try { $stop=Invoke-RestMethod "$Base/v1/runs/$activeRun/stop" -Method Post -Headers $Headers -ContentType 'application/json' -Body '{}' -TimeoutSec 15;Save-Json (Join-Path $Dir 'scoped-stop.json') $stop } catch {}
   }
  }
  $wall.Stop()
  $result=@{round=$round;pass=$ok;full_wall_ms=$wall.ElapsedMilliseconds;accepted_utc=$accepted;phases=$phaseResults;error_type=$errorType;error=$errorMessage}
  Save-Json (Join-Path $Dir 'round-result.json') $result;$results+=$result
  Save-Json (Join-Path $Root 'BATCH-RESULT.json') @{task_id='HERMES-ECO-20261014';results=$results;consecutive_pass=@($results|Where-Object {$_.pass}).Count;final_valid=($results.Count -eq 5 -and $ok);cold_boot_verified=$false}
  Write-Output ($result|ConvertTo-Json -Depth 12 -Compress)
  if(-not $ok){throw 'BATCH_STOPPED_FOR_REPAIR_NO_FALSE_PASS'}
 }
} finally {$Headers=$null}
