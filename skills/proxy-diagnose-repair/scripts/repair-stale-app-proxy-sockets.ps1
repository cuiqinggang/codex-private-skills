param(
  [int]$ProxyPort = 7890,
  [switch]$RestartWeChatAppEx,
  [string]$OutputDir = ""
)

$ErrorActionPreference = "Continue"
if (-not $OutputDir) {
  $OutputDir = Join-Path (Get-Location) ("output\network-diagnostics\stale-app-sockets-" + (Get-Date -Format "yyyyMMdd-HHmmss"))
}
New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null
$report = Join-Path $OutputDir "stale-app-proxy-sockets.md"

function Add-Report($Text) {
  $Text | Add-Content -LiteralPath $report -Encoding utf8
}

function Get-NetstatRows {
  netstat -ano |
    Select-String "127.0.0.1:$ProxyPort" |
    ForEach-Object {
      $parts = ($_.Line -split "\s+") | Where-Object { $_ }
      if ($parts.Count -ge 5) {
        [pscustomobject]@{
          Raw = $_.Line
          Proto = $parts[0]
          Local = $parts[1]
          Remote = $parts[2]
          State = $parts[3]
          OwningPid = [int]$parts[4]
        }
      }
    }
}

Set-Content -LiteralPath $report -Value "# Stale App Proxy Socket Repair" -Encoding utf8
Add-Report ""
Add-Report ("Time: " + (Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz"))
Add-Report "Proxy port: 127.0.0.1:$ProxyPort"
$mode = if ($RestartWeChatAppEx) { "RestartWeChatAppEx" } else { "DryRun" }
Add-Report "Mode: $mode"
Add-Report ""

$rows = @(Get-NetstatRows)
$staleRows = @($rows | Where-Object { $_.State -match "CLOSE_WAIT|FIN_WAIT" })

Add-Report "## Stale Rows"
if ($staleRows.Count -eq 0) {
  Add-Report "No CLOSE_WAIT/FIN_WAIT rows found for this proxy port."
} else {
  foreach ($row in $staleRows) {
    $proc = Get-CimInstance Win32_Process -Filter "ProcessId=$($row.OwningPid)" -ErrorAction SilentlyContinue
    Add-Report ("- PID {0} {1}: {2}" -f $row.OwningPid, $proc.Name, $row.Raw.Trim())
  }
}

$wechatPids = @(
  $staleRows |
    ForEach-Object {
      $proc = Get-CimInstance Win32_Process -Filter "ProcessId=$($_.OwningPid)" -ErrorAction SilentlyContinue
      if ($proc.Name -eq "WeChatAppEx.exe") { $_.OwningPid }
    } |
    Sort-Object -Unique
)

Add-Report ""
Add-Report "## WeChatAppEx Candidates"
if ($wechatPids.Count -eq 0) {
  Add-Report "No stale WeChatAppEx.exe sockets found."
} else {
  foreach ($procId in $wechatPids) {
    $proc = Get-CimInstance Win32_Process -Filter "ProcessId=$procId" -ErrorAction SilentlyContinue
    Add-Report ("- PID {0}: {1}" -f $procId, $proc.CommandLine)
  }
}

if ($RestartWeChatAppEx -and $wechatPids.Count -gt 0) {
  Add-Report ""
  Add-Report "## Action"
  foreach ($procId in $wechatPids) {
    try {
      Stop-Process -Id $procId -ErrorAction Stop
      Add-Report "Stopped WeChatAppEx PID $procId without Force."
    } catch {
      Add-Report "Graceful stop failed for PID ${procId}: $($_.Exception.Message)"
      try {
        Stop-Process -Id $procId -Force -ErrorAction Stop
        Add-Report "Stopped WeChatAppEx PID $procId with Force."
      } catch {
        Add-Report "Force stop failed for PID ${procId}: $($_.Exception.Message)"
      }
    }
  }
  Start-Sleep -Seconds 3
  Add-Report ""
  Add-Report "## Post-Action Rows"
  $postRows = @(Get-NetstatRows | Where-Object { $_.State -match "CLOSE_WAIT|FIN_WAIT" })
  if ($postRows.Count -eq 0) {
    Add-Report "No CLOSE_WAIT/FIN_WAIT rows found after action."
  } else {
    foreach ($row in $postRows) {
      Add-Report ("- PID {0}: {1}" -f $row.OwningPid, $row.Raw.Trim())
    }
  }
}

Get-Content -LiteralPath $report
