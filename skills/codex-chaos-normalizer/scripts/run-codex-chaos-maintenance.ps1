param(
${REDACTED_SECRET}
${REDACTED_SECRET}
  [int]$RetentionDays = 3,
  [int]$LargeLogMb = 300
)

$ErrorActionPreference = 'Continue'
$skillRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$health = Join-Path $skillRoot 'scripts\codex-chaos-health.ps1'
$compact = Join-Path $skillRoot 'scripts\compact-codex-logs-after-exit.ps1'
$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$runRoot = Join-Path $CodexHome 'repair-logs\scheduled'
$runDir = Join-Path $runRoot "codex-chaos-maintenance-$stamp"
New-Item -ItemType Directory -Force -Path $runDir | Out-Null
$transcript = Join-Path $runDir 'maintenance.log'

Start-Transcript -LiteralPath $transcript -Force | Out-Null
try {
  Write-Host "Codex Chaos Maintenance started: $stamp"
  Write-Host "Workspace: $Workspace"
  Write-Host "CodexHome: $CodexHome"

  $diagnoseJson = Join-Path $runDir 'diagnose-before.json'
  & $health -Mode Diagnose -Workspace $Workspace -CodexHome $CodexHome -CpuSampleSeconds 3 -Json |
    Set-Content -LiteralPath $diagnoseJson -Encoding UTF8

  $normalizeJson = Join-Path $runDir 'normalize.json'
  & $health -Mode Normalize -Workspace $Workspace -CodexHome $CodexHome -CpuSampleSeconds 2 -Json |
    Set-Content -LiteralPath $normalizeJson -Encoding UTF8

  $db = Join-Path $CodexHome 'logs_2.sqlite'
  $dbMb = 0
  if (Test-Path -LiteralPath $db) {
    $dbMb = [math]::Round((Get-Item -LiteralPath $db).Length / 1MB, 2)
  }
  Write-Host "logs_2.sqlite MB: $dbMb"

  $existingWatcher = Get-CimInstance Win32_Process |
    Where-Object { $_.CommandLine -like '*compact-codex-logs-after-exit.ps1*' -and $_.CommandLine -notlike '*Get-CimInstance*' } |
    Select-Object -First 1

  if ($dbMb -ge $LargeLogMb -and -not $existingWatcher) {
    $watcherDir = Join-Path $runDir 'compact-watcher'
    New-Item -ItemType Directory -Force -Path $watcherDir | Out-Null
    $stdout = Join-Path $watcherDir 'stdout.log'
    $stderr = Join-Path $watcherDir 'stderr.log'
    $status = Join-Path $watcherDir 'status.txt'
    $args = @(
      '-NoProfile',
      '-WindowStyle', 'Hidden',
      '-ExecutionPolicy', 'Bypass',
      '-File', $compact,
      '-CodexHome', $CodexHome,
      '-RetentionDays', [string]$RetentionDays,
      '-StatusPath', $status
    )
    $proc = Start-Process -FilePath powershell.exe -ArgumentList $args -WindowStyle Hidden -RedirectStandardOutput $stdout -RedirectStandardError $stderr -PassThru
    Write-Host "Started offline compaction watcher PID=$($proc.Id), status=$status"
  } elseif ($existingWatcher) {
    Write-Host "Offline compaction watcher already running PID=$($existingWatcher.ProcessId)"
  } else {
    Write-Host "Log DB below LargeLogMb threshold; watcher not needed."
  }

  $afterJson = Join-Path $runDir 'diagnose-after.json'
  & $health -Mode Diagnose -Workspace $Workspace -CodexHome $CodexHome -CpuSampleSeconds 2 -Json |
    Set-Content -LiteralPath $afterJson -Encoding UTF8

  Write-Host "Codex Chaos Maintenance finished: $runDir"
} finally {
  Stop-Transcript | Out-Null
}
