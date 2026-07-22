param(
  [string] $Profile = "codex",
  [string] $Workspace = "K:\AI\remote-codex-workspace",
  [string] $ConfigPath = "$env:USERPROFILE\.lark-channel\config.json",
  [string] $LogDir = "$env:USERPROFILE\.lark-channel\profiles\codex\logs",
  [string] $OutputDir = "K:\AI\remote-codex-workspace\maintenance"
)

$ErrorActionPreference = "Continue"

function Invoke-Measure {
  param([scriptblock] $Script)
  $sw = [System.Diagnostics.Stopwatch]::StartNew()
  try {
    $output = & $Script 2>&1 | Out-String
    $ok = $LASTEXITCODE -eq 0 -or $null -eq $LASTEXITCODE
    return [pscustomobject]@{ ok = $ok; ms = [int]$sw.ElapsedMilliseconds; output = ($output.Trim()) }
  } catch {
    return [pscustomobject]@{ ok = $false; ms = [int]$sw.ElapsedMilliseconds; output = $_.Exception.Message }
  } finally {
    $sw.Stop()
  }
}

function Get-BridgeProcesses {
  Get-CimInstance Win32_Process |
    Where-Object {
      $_.CommandLine -and
      ($_.CommandLine -like "*lark-channel-bridge*" -or $_.CommandLine -like "*.lark-channel*") -and
      $_.Name -in @("node.exe", "cmd.exe")
    } |
    Select-Object ProcessId, Name, CommandLine
}

function Mask-Text {
  param([string] $Text)
  if ([string]::IsNullOrEmpty($Text)) { return "" }
  $masked = $Text
  $masked = $masked -replace "(?i)(app[_ -]?secret|token|api[_ -]?key|password|access[_ -]?key|ticket)\s*[:=]\s*[^`"\s,;]+", '$1=***'
  $masked = $masked -replace "cli_[A-Za-z0-9]+", "cli_***"
  return $masked
}

New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null

$started = Get-Date
$bridgeProcesses = @(Get-BridgeProcesses)
$configExists = Test-Path -LiteralPath $ConfigPath
$configStatus = "missing"
$defaultAccess = $null
$maxAccess = $null
$configuredWorkspace = $null

if ($configExists) {
  try {
    $config = Get-Content -LiteralPath $ConfigPath -Raw -Encoding UTF8 | ConvertFrom-Json
    $defaultAccess = $config.profiles.$Profile.permissions.defaultAccess
    $maxAccess = $config.profiles.$Profile.permissions.maxAccess
    $configuredWorkspace = $config.profiles.$Profile.workspaces.default
    if ($defaultAccess -eq "workspace" -and $maxAccess -eq "workspace") {
      $configStatus = "pass"
    } else {
      $configStatus = "danger-permission"
    }
  } catch {
    $configStatus = "invalid-json"
  }
}

$bridgeHelp = Invoke-Measure { lark-channel-bridge --help }
$bridgeStatus = Invoke-Measure { lark-channel-bridge status --profile $Profile }
$bridgePs = Invoke-Measure { lark-channel-bridge ps }
$codexVersion = Invoke-Measure { codex --version }
$whereCodex = Invoke-Measure { where.exe codex }

$latestLog = $null
$logSignals = [ordered]@{
  requestTimedOut = 0
  reconnect = 0
  skillLoadError = 0
  eaddrinuse = 0
  tokenMention = 0
  appSecretMention = 0
}
$sanitizedRecentLog = @()

if (Test-Path -LiteralPath $LogDir) {
  $latestLog = Get-ChildItem -LiteralPath $LogDir -File -ErrorAction SilentlyContinue |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1
  if ($latestLog) {
    $recentLines = @(Get-Content -LiteralPath $latestLog.FullName -Tail 200 -Encoding UTF8 -ErrorAction SilentlyContinue)
    foreach ($line in $recentLines) {
      if ($line -match "request timed out") { $logSignals.requestTimedOut++ }
      if ($line -match "(?i)reconnect|reconnecting") { $logSignals.reconnect++ }
      if ($line -match "(?i)failed to load skill|skill load") { $logSignals.skillLoadError++ }
      if ($line -match "EADDRINUSE") { $logSignals.eaddrinuse++ }
      if ($line -match "(?i)token") { $logSignals.tokenMention++ }
      if ($line -match "(?i)app[_ -]?secret") { $logSignals.appSecretMention++ }
    }
    $sanitizedRecentLog = @($recentLines | Select-Object -Last 20 | ForEach-Object { Mask-Text $_ })
  }
}

$workspaceExists = Test-Path -LiteralPath $Workspace
$testFile = Join-Path $Workspace "TEST_FEISHU_CODEX_OK.txt"
$testFileExists = Test-Path -LiteralPath $testFile
$desktopTestFile = Join-Path ([Environment]::GetFolderPath("Desktop")) "TEST_FEISHU_CODEX_OK.txt"
$systemTestFile = "C:\Windows\TEST_FEISHU_CODEX_OK.txt"

$severity = "PASS"
$issues = New-Object System.Collections.Generic.List[string]

if ($bridgeProcesses.Count -eq 0) {
  $severity = "FAIL"
  $issues.Add("No lark-channel-bridge process found.")
}
if ($configStatus -eq "danger-permission") {
  $severity = "FAIL"
  $issues.Add("Unsafe bridge permissions detected: defaultAccess=$defaultAccess maxAccess=$maxAccess.")
}
if (-not $workspaceExists) {
  if ($severity -ne "FAIL") { $severity = "WARN" }
  $issues.Add("Workspace does not exist: $Workspace.")
}
if ($logSignals.requestTimedOut -gt 0 -or $logSignals.skillLoadError -gt 0) {
  if ($severity -eq "PASS") { $severity = "WARN" }
  $issues.Add("Recent logs contain Codex timeout or skill-loading warnings.")
}

$result = [ordered]@{
  generatedAt = $started.ToString("o")
  result = $severity
  issues = @($issues)
  bridge = [ordered]@{
    processCount = $bridgeProcesses.Count
    processes = @($bridgeProcesses | ForEach-Object {
      [ordered]@{ pid = $_.ProcessId; name = $_.Name; commandLine = (Mask-Text $_.CommandLine) }
    })
    help = [ordered]@{ ok = $bridgeHelp.ok; ms = $bridgeHelp.ms }
    status = [ordered]@{ ok = $bridgeStatus.ok; ms = $bridgeStatus.ms; output = (Mask-Text $bridgeStatus.output) }
    ps = [ordered]@{ ok = $bridgePs.ok; ms = $bridgePs.ms; output = (Mask-Text $bridgePs.output) }
  }
  config = [ordered]@{
    path = $ConfigPath
    exists = $configExists
    status = $configStatus
    defaultAccess = $defaultAccess
    maxAccess = $maxAccess
    workspace = $configuredWorkspace
  }
  codex = [ordered]@{
    version = [ordered]@{ ok = $codexVersion.ok; ms = $codexVersion.ms; output = $codexVersion.output }
    where = [ordered]@{ ok = $whereCodex.ok; ms = $whereCodex.ms; output = $whereCodex.output }
  }
  workspace = [ordered]@{
    path = $Workspace
    exists = $workspaceExists
    testFile = $testFile
    testFileExists = $testFileExists
    desktopRootTestFileExists = (Test-Path -LiteralPath $desktopTestFile)
    systemRootTestFileExists = (Test-Path -LiteralPath $systemTestFile)
  }
  logs = [ordered]@{
    dir = $LogDir
    latest = if ($latestLog) { $latestLog.FullName } else { $null }
    latestLastWriteTime = if ($latestLog) { $latestLog.LastWriteTime.ToString("o") } else { $null }
    signals = $logSignals
    recentSanitizedTail = $sanitizedRecentLog
  }
}

$jsonPath = Join-Path $OutputDir "health-latest.json"
$mdPath = Join-Path $OutputDir "health-latest.md"
$result | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $jsonPath -Encoding UTF8

$md = @()
$md += "# Feishu Codex Bridge Health"
$md += ""
$md += "- Generated: $($result.generatedAt)"
$md += "- Result: $($result.result)"
$md += "- Bridge processes: $($result.bridge.processCount)"
$md += "- Config permission: defaultAccess=$defaultAccess maxAccess=$maxAccess"
$md += "- Workspace: $Workspace"
$md += "- Codex version check: ok=$($result.codex.version.ok) ms=$($result.codex.version.ms) output=$($result.codex.version.output)"
$md += "- Latest log: $($result.logs.latest)"
$md += "- Latest log write: $($result.logs.latestLastWriteTime)"
$md += ""
$md += "## Issues"
if ($issues.Count -eq 0) {
  $md += "- None."
} else {
  foreach ($issue in $issues) { $md += "- $issue" }
}
$md += ""
$md += "## Log Signals"
foreach ($key in $logSignals.Keys) { $md += "- ${key}: $($logSignals[$key])" }
$md += ""
$md += "## Bridge Processes"
foreach ($proc in $result.bridge.processes) {
  $md += "- PID $($proc.pid) $($proc.name): $($proc.commandLine)"
}
$md += ""
$md += "## Notes"
$md += "- Secrets are masked. This report does not print app secrets, tokens, API keys, or passwords."
$md += '- `request timed out` means the Codex CLI/model request layer is slow; it is not by itself proof that the Feishu WebSocket bridge is down.'
$md | Set-Content -LiteralPath $mdPath -Encoding UTF8

Write-Output "HEALTH_RESULT=$severity"
Write-Output "JSON=$jsonPath"
Write-Output "MD=$mdPath"
