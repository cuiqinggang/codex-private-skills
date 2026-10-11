param([switch]$Once)
$ErrorActionPreference='Stop'
$monRoot='C:\AI\Polsia-Unified-V4'
$node='C:\AI\Polsia-Codex-20261011\nodes\CODEX-008'
$branchIds=@('ENG','RECOVERY')
foreach($bid in $branchIds){$dir=Join-Path $monRoot ('branches\'+$bid);[void](New-Item -ItemType Directory -Path $dir -Force)}
$completed=@($branchIds | ForEach-Object -Parallel {
 $bid=$_;$base=$using:monRoot;$sourceNode=$using:node
 $dir=Join-Path $base ('branches\'+$bid);$statePath=Join-Path $dir 'status.json'
 if(Test-Path -LiteralPath $statePath){
  $old=Get-Content -LiteralPath $statePath -Raw -Encoding utf8 | ConvertFrom-Json
  if($old.status -eq 'DONE'){return [pscustomobject]@{id=$bid;status='DONE_ALREADY_EXISTS';proof=$old.proof}}
  if($old.status -eq 'RUNNING'){return [pscustomobject]@{id=$bid;status='UNKNOWN_OLD_RUNNING_NO_RETRY';proof='No blind restart'}}
 }
 @{id=$bid;status='RUNNING';utc=[DateTime]::UtcNow.ToString('o');proof='';detail='隔离任务实际执行中'}|ConvertTo-Json |Set-Content -LiteralPath $statePath -Encoding utf8
 $result=[ordered]@{id=$bid;status='ERROR';utc=[DateTime]::UtcNow.ToString('o');proof='';detail='';checks=0}
 try{
  if($bid -eq 'ENG'){
   $manifest=Get-Content -LiteralPath (Join-Path $sourceNode 'SHA256-MANIFEST.json') -Raw -Encoding utf8|ConvertFrom-Json
   $ok=0
   foreach($entry in $manifest.files){
    $f=Join-Path $sourceNode ([string]$entry.path)
    if(-not (Test-Path -LiteralPath $f)){throw 'MISSING: '+$entry.path}
    if((Get-Item -LiteralPath $f).Length -ne [long]$entry.bytes){throw 'SIZE_MISMATCH: '+$entry.path}
    if((Get-FileHash -LiteralPath $f -Algorithm SHA256).Hash -ne [string]$entry.sha256){throw 'HASH_MISMATCH: '+$entry.path}
    $ok++
   }
   if($ok -ne 128){throw 'Expected 128 V008 manifest entries'}
   $result.status='DONE';$result.checks=$ok;$result.proof='V008_IMMUTABLE_MANIFEST_128_OF_128_PASS';$result.detail='V008冻结事实128项逐一SHA验证完成，不涉及业务重跑'
  }elseif($bid -eq 'RECOVERY'){
   $scratch=Join-Path $base 'scratch\isolated_git_recovery'
   if(Test-Path -LiteralPath $scratch){throw 'UNKNOWN_EXISTING_RECOVERY_FIXTURE_DO_NOT_REPLAY'}
   [void](New-Item -ItemType Directory -Path $scratch -Force)
   & git -C $scratch init -q
   if($LASTEXITCODE -ne 0){throw 'git init failed'}
   $fixture=Join-Path $scratch 'fixture.txt'
   'POLSIA_ISOLATED_RECOVERY_GOOD_V4' | Set-Content -LiteralPath $fixture -Encoding utf8
   $good=(Get-FileHash -LiteralPath $fixture -Algorithm SHA256).Hash
   & git -C $scratch add -- fixture.txt
   & git -C $scratch -c user.name='Polsia Isolated Tester' -c user.email='no-reply@example.invalid' commit -q -m 'Isolated recovery baseline V4'
   if($LASTEXITCODE -ne 0){throw 'git commit failed'}
   'DAMAGED_TEST_ONLY' | Set-Content -LiteralPath $fixture -Encoding utf8
   $bad=(Get-FileHash -LiteralPath $fixture -Algorithm SHA256).Hash
   if($good -eq $bad){throw 'FAIL_FAULT_NOT_DETECTED'}
   $history=Join-Path $base 'incidents.jsonl'
   @{utc=[DateTime]::UtcNow.ToString('o');event='TEST_DETECTED';key='RECOVERY_ISOLATED_GIT_DAMAGE';detail='Damage confined to V4 scratch fixture'}|ConvertTo-Json -Compress|Add-Content -LiteralPath $history -Encoding utf8
   & git -C $scratch restore --source=HEAD --worktree -- fixture.txt
   if($LASTEXITCODE -ne 0){throw 'Native git restore failed'}
   $restored=(Get-FileHash -LiteralPath $fixture -Algorithm SHA256).Hash
   if($good -ne $restored){throw 'AUTO_RECOVERY_HASH_MISMATCH'}
   @{utc=[DateTime]::UtcNow.ToString('o');event='TEST_AUTO_RECOVERED';key='RECOVERY_ISOLATED_GIT_DAMAGE';detail='Native git restore verified byte-level SHA equal'}|ConvertTo-Json -Compress|Add-Content -LiteralPath $history -Encoding utf8
   $result.status='DONE';$result.proof='ISOLATED_GIT_DAMAGE_DETECT_AND_RESTORE_SHA_MATCH';$result.checks=1;$result.detail='隔离文件故障由本机自动识别并原生Git恢复；生产未知故障不盲重启'
  }
 }catch{$result.status='ERROR';$result.detail=$_.Exception.Message}
 $result.utc=[DateTime]::UtcNow.ToString('o')
 $result|ConvertTo-Json -Depth 5|Set-Content -LiteralPath $statePath -Encoding utf8
 [pscustomobject]$result
} -ThrottleLimit 2 -TimeoutSeconds 120)
$completed|ConvertTo-Json -Depth 5|Set-Content -LiteralPath (Join-Path $monRoot 'pilot-results.json') -Encoding utf8
$completed|ConvertTo-Json -Compress -Depth 5
& (Join-Path $monRoot 'collect.ps1') -Once
if(@($completed|Where-Object {$_.status -notin @('DONE','DONE_ALREADY_EXISTS')}).Count -gt 0){exit 2}