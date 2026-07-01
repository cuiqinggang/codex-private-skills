param(
  [ValidateSet('Approval','Auto','ReportOnly')]
  [string]$Mode = 'Approval',
  [switch]$NoSound,
  [int]$MinHoursBetweenRuns = 24,
  [switch]$Force
)

$ErrorActionPreference = 'Stop'
$Workspace = 'C:\Users\A\Desktop\1'
$Root = Join-Path $Workspace 'output\TASK-20260520-AI-SYSTEM-EVOLUTION-LOOP'
$Poc = Join-Path $Root 'prototype\evolution_loop_poc.py'
$SkillDir = 'C:\Users\A\.codex\skills\system-evolution'
$HRoot = 'H:\AI_System_Evolution'
$StartedAt = Get-Date
$Now = $StartedAt.ToString('yyyy-MM-dd HH:mm:ss')

function Write-Utf8File {
  param([string]$Path, [string]$Content)
  $dir = Split-Path -Parent $Path
  if ($dir -and -not (Test-Path $dir)) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }
  [System.IO.File]::WriteAllText($Path, $Content, [System.Text.Encoding]::UTF8)
}

function Play-SystemEvolutionSound {
  param([bool]$Success)
  if ($NoSound) { return }
  try {
    Add-Type -AssemblyName System.Speech
    $voice = New-Object System.Speech.Synthesis.SpeechSynthesizer
    $message = if ($Success) { 'System evolution report generated. Please check the pending approval plan.' } else { 'System evolution run failed. Please check the log.' }
    [void]$voice.SpeakAsync($message)
    if ($Success) { [System.Media.SystemSounds]::Exclamation.Play() } else { [System.Media.SystemSounds]::Hand.Play() }
  } catch {
    $warn = "[$Now] Sound warning: $($_.Exception.Message)"
    Add-Content -LiteralPath (Join-Path $Root 'logs\system-evolution-runner.log') -Value $warn -Encoding UTF8
  }
}

function Sync-ToHDrive {
  if ($Mode -eq 'ReportOnly') { return }
  if (-not (Test-Path 'H:\')) { return }
  $destSkill = Join-Path $HRoot 'skills\system-evolution'
  New-Item -ItemType Directory -Force -Path $destSkill | Out-Null
  Copy-Item -Path (Join-Path $SkillDir '*') -Destination $destSkill -Recurse -Force

  foreach ($sub in @('reports','plans','actions','state','logs')) {
    $src = Join-Path $Root $sub
    $dst = Join-Path $HRoot $sub
    if (Test-Path $src) {
      New-Item -ItemType Directory -Force -Path $dst | Out-Null
      Copy-Item -Path (Join-Path $src '*') -Destination $dst -Recurse -Force -ErrorAction SilentlyContinue
    }
  }
}

function Get-LastSuccessfulRunTime {
  param([string]$SummaryPath)
  if (-not (Test-Path $SummaryPath)) { return $null }
  try {
    $summary = Get-Content -Raw -LiteralPath $SummaryPath | ConvertFrom-Json
    if (-not [bool]$summary.pass) { return $null }
    return (Get-Item -LiteralPath $SummaryPath).LastWriteTime
  } catch {
    return $null
  }
}

try {
  if (-not (Test-Path $Poc)) { throw "PoC script missing: $Poc" }
  New-Item -ItemType Directory -Force -Path (Join-Path $Root 'logs') | Out-Null
  $logPath = Join-Path $Root 'logs\system-evolution-runner.log'

  if (($MinHoursBetweenRuns -gt 0) -and (-not $Force)) {
    $summaryPathForCooldown = Join-Path $Root 'evidence\run-summary.json'
    $lastSuccess = Get-LastSuccessfulRunTime -SummaryPath $summaryPathForCooldown
    if ($lastSuccess) {
      $age = New-TimeSpan -Start $lastSuccess -End $StartedAt
      if ($age.TotalHours -lt $MinHoursBetweenRuns) {
        $ageText = '{0:N2}' -f $age.TotalHours
        Add-Content -LiteralPath $logPath -Value "[$Now] SKIP Mode=$Mode LastSuccess=$($lastSuccess.ToString('yyyy-MM-dd HH:mm:ss')) AgeHours=$ageText MinHours=$MinHoursBetweenRuns" -Encoding UTF8
        Write-Output "SYSTEM_EVOLUTION_RUN_SKIPPED Mode=$Mode LastSuccess=$($lastSuccess.ToString('yyyy-MM-dd HH:mm:ss')) AgeHours=$ageText MinHours=$MinHoursBetweenRuns Root=$Root"
        exit 0
      }
    }
  }

  Add-Content -LiteralPath $logPath -Value "[$Now] START Mode=$Mode" -Encoding UTF8

  Push-Location $Workspace
  $output = & python $Poc --root $Root 2>&1
  $exit = $LASTEXITCODE
  Pop-Location
  Add-Content -LiteralPath $logPath -Value ($output | Out-String) -Encoding UTF8
  if ($exit -ne 0) { throw "PoC failed with exit code $exit" }

  $summaryPath = Join-Path $Root 'evidence\run-summary.json'
  $summary = Get-Content -Raw -LiteralPath $summaryPath | ConvertFrom-Json
  $pass = [bool]$summary.pass

  $pending = @"
# System Evolution Pending Approval Plan

- Generated at: $Now
- Mode: $Mode
- Trigger phrase: system evolution
- Full name: intelligence-supported system evolution plan
- PASS: $pass

## Low-risk automatic actions

See actions\low-risk-auto-actions.md.

## Codex/Hermes validation actions

See actions\codex-validation-tasks.md.

## Production upgrades requiring user approval

See actions\manual-approval-required.md.

## Current policy

The runner is in $Mode mode. Approval mode only writes reports, pending actions, and reminders; it does not modify production systems. Auto mode is still limited to low-risk file/report/task-package work; production upgrades still require explicit user approval.
"@
  Write-Utf8File -Path (Join-Path $Root 'actions\pending-approval.md') -Content $pending

  $notice = @"
# System Evolution Latest Notice

- Time: $Now
- Status: $(if ($pass) { 'PASS' } else { 'PARTIAL/FAIL' })
- Fetched sources: $($summary.fetched_source_count)
- Candidate intelligence items: $($summary.candidate_count)
- Selected intelligence items: $($summary.selected_count)
- Upgrade suggestions: $($summary.upgrade_suggestions_count)
- Codex/Hermes validation tasks: $($summary.codex_validation_task_count)
- Pending approval plan: actions\pending-approval.md
- Full report: reports\system-evolution-report.md
- Final report: reports\report.md

Note: this run did not modify production systems.
"@
  Write-Utf8File -Path (Join-Path $Root 'reports\latest-system-evolution-notice.md') -Content $notice

  Sync-ToHDrive
  Play-SystemEvolutionSound -Success:$pass
  Add-Content -LiteralPath $logPath -Value "[$Now] END PASS=$pass" -Encoding UTF8
  Write-Output "SYSTEM_EVOLUTION_RUN_PASS Mode=$Mode Root=$Root"
  exit 0
} catch {
  $err = $_.Exception.Message
  $failNotice = "# System Evolution Run Failed`r`n`r`n- Time: $Now`r`n- Error: $err`r`n"
  Write-Utf8File -Path (Join-Path $Root 'reports\latest-system-evolution-notice.md') -Content $failNotice
  Play-SystemEvolutionSound -Success:$false
  Write-Error $err
  exit 1
}
