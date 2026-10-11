# Native Windows Task Scheduler trigger; Codex CLI is the execution engine.
# No custom scheduler, retry engine, state machine or replacement software.
$ErrorActionPreference = 'Stop'
$root = 'C:\AI\Polsia-Codex-20261011'
$prompt = Join-Path $root 'NEXT_NODE_PROMPT.md'
$rootState = Join-Path $root 'MOTHER_CURRENT.md'
$stopFlags = @('MOTHER_COMPLETE.flag','MOTHER_WAITING_FOR_USER.flag','MOTHER_PAUSE.flag','MOTHER_NEEDS_GPT.flag')
foreach ($flag in $stopFlags) {
  if (Test-Path -LiteralPath (Join-Path $root $flag)) { exit 0 }
}
if (-not (Test-Path -LiteralPath $prompt)) { exit 3 }
$state = Get-Content -LiteralPath $rootState -Raw -Encoding UTF8
if ($state -match '(?m)^MOTHER_FINAL_VALID=YES\r?$') { exit 0 }
$running = @(Get-CimInstance Win32_Process -Filter "name='codex.exe'" | Where-Object {
  $_.CommandLine -like '*Polsia-Codex-20261011*' -and ($_.CommandLine -like '* exec *' -or $_.CommandLine -like '* exec-server *')
})
if ($running.Count -gt 0) { exit 0 }
$inflight = Join-Path $root 'MOTHER_EXECUTION_INFLIGHT.flag'
if (Test-Path -LiteralPath $inflight) {
  $msg = @('TASK_ID=POLSIA_CAPABILITY_REPLICATION_20261011','REASON=PREVIOUS_EXECUTION_OUTCOME_UNKNOWN','NEXT=GPT_VERIFY_LAST_FREEZE_AND_TOOL_RECEIPTS')
  $msg | Set-Content -LiteralPath (Join-Path $root 'MOTHER_NEEDS_GPT.flag') -Encoding UTF8
  exit 7
}
$logDir = Join-Path $root 'continuation_logs'
if (-not (Test-Path -LiteralPath $logDir)) { New-Item -ItemType Directory -Path $logDir | Out-Null }
$stamp = (Get-Date).ToString('yyyyMMdd-HHmmss')
$log = Join-Path $logDir ("Codex-" + $stamp + ".log")
$last = Join-Path $root 'CODEX_CONTINUATION_LAST.md'
$env:PYTHONIOENCODING = 'utf-8'
$OutputEncoding = [Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
$versionPath = Join-Path $root 'VERSION_CURRENT.md'
$beforeVersionText = if(Test-Path -LiteralPath $versionPath){ Get-Content -LiteralPath $versionPath -Raw -Encoding UTF8 }else{ '' }
$beforeVersion = if($beforeVersionText -match '(?m)^LAST_FROZEN_VERSION=(\S+)'){ $Matches[1] }else{'UNKNOWN'}
$started = Get-Date -Format 'yyyy-MM-ddTHH:mm:sszzz'
@("TASK_ID=POLSIA_CAPABILITY_REPLICATION_20261011","START_LOCAL=$started","VERSION_BEFORE=$beforeVersion","LATEST_LOG=$log","STATE=EXECUTING_OR_UNKNOWN") | Set-Content -LiteralPath $inflight -Encoding UTF8
$beforeMother = (Get-Item -LiteralPath $rootState).LastWriteTimeUtc.Ticks
$task = Get-Content -LiteralPath $prompt -Raw -Encoding UTF8
Set-Location -LiteralPath $root
$task | & 'C:\Users\A\AppData\Roaming\npm\codex.cmd' exec -C $root --skip-git-repo-check -s workspace-write -m 'gpt-6.1-sol' -c 'model_reasoning_effort=ultra' -o $last - 2>&1 | Out-File -LiteralPath $log -Encoding UTF8
$code = $LASTEXITCODE
Add-Content -LiteralPath $log -Value ("CODEX_EXIT=" + $code) -Encoding UTF8
if ($code -ne 0) {
  $note = @("TASK_ID=POLSIA_CAPABILITY_REPLICATION_20261011","REASON=CODEX_EXIT_NONZERO","EXIT_CODE=$code","LATEST_LOG=$log","NEXT=GPT_REPLAN_WITH_EXACTLY_ONCE_CHECK")
  $note | Set-Content -LiteralPath (Join-Path $root 'MOTHER_NEEDS_GPT.flag') -Encoding UTF8
  exit $code
}
$afterMother = (Get-Item -LiteralPath $rootState).LastWriteTimeUtc.Ticks
$afterVersionText = if(Test-Path -LiteralPath $versionPath){ Get-Content -LiteralPath $versionPath -Raw -Encoding UTF8 }else{''}
$afterVersion = if($afterVersionText -match '(?m)^LAST_FROZEN_VERSION=(\S+)'){$Matches[1]}else{'UNKNOWN'}
# The canonical GitHub Freeze name is not a local-root filename. Validate the real
# local node Freeze + manifest against both persisted pointers and observed hashes.
$afterMotherText = Get-Content -LiteralPath $rootState -Raw -Encoding UTF8
$motherVersion = if ($afterMotherText -match '(?m)^VERSION=(\S+)') { $Matches[1] } else { '' }
$motherFreezeId = if ($afterMotherText -match '(?m)^FREEZE_ID=(\S+)') { $Matches[1] } else { '' }
$versionFreezeId = if ($afterVersionText -match '(?m)^LATEST_FREEZE_ID=(\S+)') { $Matches[1] } else { '' }
$freezeFile = if ($afterMotherText -match '(?m)^FREEZE_PATH=(.+)$') { $Matches[1].Trim() } else { '' }
$manifestFile = if ($afterMotherText -match '(?m)^MANIFEST_PATH=(.+)$') { $Matches[1].Trim() } else { '' }
$expectedManifest = if ($afterMotherText -match '(?m)^MANIFEST_SHA256=([A-Fa-f0-9]{64})\r?$') { $Matches[1] } else { '' }
$pathRoot = [IO.Path]::GetFullPath($root).TrimEnd('\') + '\'
$freezeInWorkspace = $freezeFile -and [IO.Path]::GetFullPath($freezeFile).StartsWith($pathRoot,[StringComparison]::OrdinalIgnoreCase)
$manifestInWorkspace = $manifestFile -and [IO.Path]::GetFullPath($manifestFile).StartsWith($pathRoot,[StringComparison]::OrdinalIgnoreCase)
$freezeValid = $freezeInWorkspace -and (Test-Path -LiteralPath $freezeFile -PathType Leaf) -and ((Get-Content -LiteralPath $freezeFile -Raw -Encoding UTF8) -match [regex]::Escape($motherFreezeId))
$manifestValid = $manifestInWorkspace -and (Test-Path -LiteralPath $manifestFile -PathType Leaf) -and $expectedManifest -and ((Get-FileHash -LiteralPath $manifestFile -Algorithm SHA256).Hash -eq $expectedManifest)
$validCheckpoint = ($code -eq 0) -and ($afterMother -gt $beforeMother) -and ($afterVersion -ne $beforeVersion) -and ($motherVersion -eq $afterVersion) -and ($motherFreezeId -eq $versionFreezeId) -and $freezeValid -and $manifestValid
if ($validCheckpoint) {
  Remove-Item -LiteralPath $inflight -Force
} elseif(-not (Test-Path -LiteralPath (Join-Path $root 'MOTHER_WAITING_FOR_USER.flag'))) {
  $note = @("TASK_ID=POLSIA_CAPABILITY_REPLICATION_20261011","REASON=CODEX_EXIT_WITHOUT_NEW_VERIFIED_FREEZE","LATEST_LOG=$log","VERSION_BEFORE=$beforeVersion","VERSION_AFTER=$afterVersion","NEXT=GPT_AUDIT_OUTPUT_AND_REPLAN")
  $note | Set-Content -LiteralPath (Join-Path $root 'MOTHER_NEEDS_GPT.flag') -Encoding UTF8
}
exit 0
