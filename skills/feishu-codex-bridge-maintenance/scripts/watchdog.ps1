param(
  [string] $Profile = "codex",
  [string] $Workspace = "K:\AI\remote-codex-workspace",
  [string] $MaintenanceDir = "K:\AI\remote-codex-workspace\maintenance",
  [int] $MaxRestartsPerWindow = 3,
  [int] $RestartWindowMinutes = 30
)

$ErrorActionPreference = "Continue"

$HealthScript = Join-Path $MaintenanceDir "health-check.ps1"
$HealthJson = Join-Path $MaintenanceDir "health-latest.json"
$StatePath = Join-Path $MaintenanceDir "watchdog-state.json"
$RestartHistory = Join-Path $MaintenanceDir "restart-history.md"
$SkillErrors = Join-Path $MaintenanceDir "SKILL_ERRORS.md"

function Get-LarkBridgeProcesses {
  Get-CimInstance Win32_Process |
    Where-Object {
      $_.CommandLine -and
      ($_.CommandLine -like "*lark-channel-bridge*" -or $_.CommandLine -like "*.lark-channel*") -and
      $_.Name -in @("node.exe", "cmd.exe")
    } |
    Select-Object ProcessId, Name, CommandLine
}

function Write-History {
  param([string] $Message)
  $stamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz"
  Add-Content -LiteralPath $RestartHistory -Encoding UTF8 -Value "- $stamp $Message"
}

function Read-State {
  if (Test-Path -LiteralPath $StatePath) {
    try {
      return Get-Content -LiteralPath $StatePath -Raw -Encoding UTF8 | ConvertFrom-Json
    } catch {
      return [pscustomobject]@{ statusFailCount = 0; restarts = @() }
    }
  }
  return [pscustomobject]@{ statusFailCount = 0; restarts = @() }
}

function Save-State {
  param($State)
  $State | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $StatePath -Encoding UTF8
}

function Restart-Bridge {
  param([string] $Reason)
  $now = Get-Date
  $state = Read-State
  $recent = @($state.restarts | Where-Object {
    try {
      ($now - [datetime]$_.time).TotalMinutes -le $RestartWindowMinutes
    } catch {
      $false
    }
  })
  if ($recent.Count -ge $MaxRestartsPerWindow) {
    Write-History "RESTART-SKIPPED rate-limit reason=$Reason recent=$($recent.Count)"
    return $false
  }

  $targets = @(Get-LarkBridgeProcesses)
  foreach ($proc in $targets) {
    Stop-Process -Id $proc.ProcessId -Force -ErrorAction SilentlyContinue
  }
  Start-Sleep -Seconds 2
  Start-Process -FilePath "$env:APPDATA\npm\lark-channel-bridge.cmd" -ArgumentList @("run", "--profile", $Profile) -WorkingDirectory $Workspace -WindowStyle Hidden
  Start-Sleep -Seconds 5

  $newProcesses = @(Get-LarkBridgeProcesses)
  $restart = [pscustomobject]@{
    time = $now.ToString("o")
    reason = $Reason
    stoppedPids = @($targets | ForEach-Object { $_.ProcessId })
    runningPids = @($newProcesses | ForEach-Object { $_.ProcessId })
  }
  $state.restarts = @($recent + $restart)
  $state.statusFailCount = 0
  Save-State $state
  Write-History "RESTART reason=$Reason stopped=$(@($targets | ForEach-Object { $_.ProcessId }) -join ',') running=$(@($newProcesses | ForEach-Object { $_.ProcessId }) -join ',')"
  return $true
}

New-Item -ItemType Directory -Force -Path $MaintenanceDir | Out-Null
if (-not (Test-Path -LiteralPath $RestartHistory)) {
  Set-Content -LiteralPath $RestartHistory -Encoding UTF8 -Value "# Restart History"
}

if (-not (Test-Path -LiteralPath $HealthScript)) {
  Write-History "FAIL missing health script: $HealthScript"
  throw "Missing health script: $HealthScript"
}

& powershell.exe -NoProfile -ExecutionPolicy Bypass -File $HealthScript -Profile $Profile -Workspace $Workspace -OutputDir $MaintenanceDir | Out-Null
if (-not (Test-Path -LiteralPath $HealthJson)) {
  Write-History "FAIL health output missing"
  throw "Health output missing: $HealthJson"
}

$health = Get-Content -LiteralPath $HealthJson -Raw -Encoding UTF8 | ConvertFrom-Json
$state = Read-State
$config = $health.config

if ($config.defaultAccess -ne "workspace" -or $config.maxAccess -ne "workspace") {
  $targets = @(Get-LarkBridgeProcesses)
  foreach ($proc in $targets) {
    Stop-Process -Id $proc.ProcessId -Force -ErrorAction SilentlyContinue
  }
  Write-History "CRITICAL stopped bridge because unsafe permissions were detected defaultAccess=$($config.defaultAccess) maxAccess=$($config.maxAccess)"
  Write-Output "WATCHDOG_RESULT=CRITICAL_UNSAFE_PERMISSION_STOPPED"
  exit 2
}

$signals = $health.logs.signals
if ($signals.skillLoadError -gt 0) {
  $lines = @()
  $lines += "# Skill Errors"
  $lines += ""
  $lines += "Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz')"
  $lines += ""
  $lines += "- Recent skill-loading warning count: $($signals.skillLoadError)"
  $lines += "- Action: recorded only. No skill was deleted or modified."
  $lines += "- Recommendation: run a separate skill metadata audit to repair malformed SKILL.md frontmatter or invalid UTF-8 files."
  $lines | Set-Content -LiteralPath $SkillErrors -Encoding UTF8
}

if ($signals.requestTimedOut -gt 0) {
  Write-History "NOTE Codex CLI/model timeout observed count=$($signals.requestTimedOut); bridge not restarted for model-layer timeout alone"
}

$needRestart = $false
$reason = ""
if ([int]$health.bridge.processCount -eq 0) {
  $needRestart = $true
  $reason = "missing bridge process"
} elseif (-not [bool]$health.bridge.status.ok) {
  $state.statusFailCount = [int]$state.statusFailCount + 1
  Save-State $state
  if ($state.statusFailCount -ge 2) {
    $needRestart = $true
    $reason = "bridge status failed twice"
  }
} else {
  $state.statusFailCount = 0
  Save-State $state
}

if ($needRestart) {
  $ok = Restart-Bridge -Reason $reason
  if ($ok) {
    Write-Output "WATCHDOG_RESULT=RESTARTED"
  } else {
    Write-Output "WATCHDOG_RESULT=RESTART_RATE_LIMITED"
  }
} else {
  Write-History "OK bridge healthy enough; result=$($health.result) processes=$($health.bridge.processCount)"
  Write-Output "WATCHDOG_RESULT=OK"
}
