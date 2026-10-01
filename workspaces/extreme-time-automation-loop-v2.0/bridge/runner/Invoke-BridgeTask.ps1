param(
  [Parameter(Mandatory=$true)][string]$TaskFile,
  [Parameter(Mandatory=$true)][string]$ResultDir
)

$ErrorActionPreference = 'Stop'
$started = [DateTimeOffset]::UtcNow
New-Item -ItemType Directory -Path $ResultDir -Force | Out-Null

function Write-BridgeResult {
  param([string]$Status,[int]$ExitCode,[string]$Message,[string]$TaskId,[string]$Stdout,[string]$Stderr)
  $ended = [DateTimeOffset]::UtcNow
  $obj = [ordered]@{
    schema_version = 1
    task_id = $TaskId
    status = $Status
    exit_code = $ExitCode
    message = $Message
    started_utc = $started.ToString('o')
    ended_utc = $ended.ToString('o')
    duration_ms = [math]::Round(($ended-$started).TotalMilliseconds,3)
    runner_name = $env:RUNNER_NAME
    machine_name = $env:COMPUTERNAME
    stdout_file = $Stdout
    stderr_file = $Stderr
  }
  $obj | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath (Join-Path $ResultDir 'result.json') -Encoding UTF8
}

$taskPath = (Resolve-Path -LiteralPath $TaskFile).Path
$task = Get-Content -LiteralPath $taskPath -Raw -Encoding UTF8 | ConvertFrom-Json
$taskId = [string]$task.task_id
if ($task.schema_version -ne 1) { throw 'Unsupported schema_version.' }
if ($taskId -notmatch '^[A-Za-z0-9._-]{3,100}$') { throw 'Invalid task_id.' }
if ([string]::IsNullOrWhiteSpace([string]$task.payload_path)) { throw 'payload_path is required.' }

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..\..')).Path
$payloadRelative = ([string]$task.payload_path).Replace('/','\')
$allowedPrefix = 'workspaces\extreme-time-automation-loop-v2.0\bridge\payloads\'
if (-not $payloadRelative.StartsWith($allowedPrefix,[System.StringComparison]::OrdinalIgnoreCase)) {
  throw 'payload_path is outside the allowed bridge payload directory.'
}
$payloadFullPath = (Resolve-Path (Join-Path $repoRoot $payloadRelative)).Path
if (-not $payloadFullPath.StartsWith((Join-Path $repoRoot $allowedPrefix),[System.StringComparison]::OrdinalIgnoreCase)) {
  throw 'Resolved payload escaped allowed directory.'
}

$payloadText = Get-Content -LiteralPath $payloadFullPath -Raw -Encoding UTF8
$forbidden = @(
  '(?i)netsh\s+winhttp\s+(set|reset)\s+proxy',
  '(?i)\b(Disable|Remove|Set)-NetAdapter\b',
  '(?i)ProxyEnable|ProxyServer',
  '(?i)\bFormat-Volume\b|\bClear-Disk\b|\bRemove-Partition\b|\bdiskpart\b|\bbcdedit\b',
  '(?i)(Remove-Item|\bdel\b|\brd\b|\brmdir\b).*[\\/]Windows([\\/]|\b)'
)
foreach ($pattern in $forbidden) {
  if ($payloadText -match $pattern) { throw "Payload blocked by bridge boundary: $pattern" }
}

$timeout = [int]$task.timeout_seconds
if ($timeout -lt 1 -or $timeout -gt 86400) { throw 'timeout_seconds must be 1..86400.' }
$expected = if ($null -eq $task.expected_exit_code) { 0 } else { [int]$task.expected_exit_code }

$workDir = Join-Path $env:RUNNER_TEMP ("etal-bridge\" + $taskId)
New-Item -ItemType Directory -Path $workDir -Force | Out-Null
$stdout = Join-Path $ResultDir 'stdout.txt'
$stderr = Join-Path $ResultDir 'stderr.txt'

$args = @(
  '-NoProfile','-NonInteractive','-ExecutionPolicy','Bypass',
  '-File',('"' + $payloadFullPath + '"'),
  '-BridgeWorkDir',('"' + $workDir + '"'),
  '-TaskFile',('"' + $taskPath + '"')
)
$p = Start-Process -FilePath 'pwsh' -ArgumentList $args -PassThru -RedirectStandardOutput $stdout -RedirectStandardError $stderr
if (-not $p.WaitForExit($timeout * 1000)) {
  try { $p.Kill($true) } catch {}
  Write-BridgeResult -Status 'TIMEOUT' -ExitCode 124 -Message 'Task exceeded timeout.' -TaskId $taskId -Stdout $stdout -Stderr $stderr
  exit 124
}

$exitCode = $p.ExitCode
if ($exitCode -eq $expected) {
  Write-BridgeResult -Status 'PASS' -ExitCode $exitCode -Message 'Task completed with expected exit code.' -TaskId $taskId -Stdout $stdout -Stderr $stderr
  Write-Host "BRIDGE_PASS $taskId"
  exit 0
}

Write-BridgeResult -Status 'FAIL' -ExitCode $exitCode -Message "Unexpected exit code; expected $expected." -TaskId $taskId -Stdout $stdout -Stderr $stderr
exit 1
