param([switch]$Persist)
$ErrorActionPreference = 'Stop'
$root = 'C:\AI\GPT-Windows-Bridge-B\persistence'
$id = 'tunnel_6acbeee2ce888191b775cd53429c7597'
$exe = 'C:\AI\GPT-Windows-Bridge-B\tunnel\v0.0.16\tunnel-client.exe'
$r = [ordered]@{
  utc = [DateTime]::UtcNow.ToString('o'); state = 'UNKNOWN'
  clients = 0; matching = 0; pid = $null; parent_alive = $false
  ready = $false; control_plane = $null; poll_failures = $null
  mcp = $null; mcp_child = $null; mcp_generation = $null
  response_delivery = $null; delivery_terminal_failures = $null; dispatcher_failures = $null; initialize_epoch = $null; proxy = $null; error_type = $null
}
try {
  $all = @(Get-CimInstance Win32_Process -Filter "Name='tunnel-client.exe'")
  $match = @($all | Where-Object { ([string]$_.CommandLine).Contains($id) })
  $r.clients = $all.Count; $r.matching = $match.Count
  $candidate = $null; $pathOnly = $false
  if ($all.Count -eq 1 -and $match.Count -eq 1) { $candidate = $match[0] }
  elseif ($all.Count -eq 1 -and [string]::IsNullOrWhiteSpace($all[0].CommandLine)) {
    $candidate = $all[0]; $pathOnly = $true
  }
  if ($all.Count -eq 0) { $r.state = 'PROCESS_MISSING' }
  elseif (!$candidate) { $r.state = 'PROCESS_IDENTITY_UNVERIFIED' }
  elseif (-not [string]::IsNullOrWhiteSpace($candidate.ExecutablePath) -and $candidate.ExecutablePath -ne $exe) { $r.state = 'PROCESS_PATH_MISMATCH' }
  else {
    $p = $candidate; $r.pid = [int]$p.ProcessId
    $r.parent_alive = @((Get-CimInstance Win32_Process -Filter "ProcessId=$($p.ParentProcessId)")).Count -eq 1
    $ports = @(Get-NetTCPConnection -State Listen -OwningProcess $p.ProcessId |
      Where-Object { $_.LocalAddress -eq '127.0.0.1' } |
      Select-Object -ExpandProperty LocalPort -Unique)
    if ($ports.Count -ne 1) { $r.state = 'HEALTH_PORT_AMBIGUOUS' }
    else {
      $h = Invoke-RestMethod -UseBasicParsing -TimeoutSec 5 -Uri ('http://127.0.0.1:'+$ports[0]+'/health?details=true')
      $r.ready = [bool]$h.ready
      $r.control_plane = $h.components.'control-plane'.state
      $r.poll_failures = $h.components.'control-plane'.details.consecutive_failures
      $r.mcp = $h.components.mcp.state
      $r.mcp_child = $h.components.mcp.details.child_state
      $r.mcp_generation = $h.components.mcp.details.child_generation
      $r.initialize_epoch = $h.components.mcp.details.initialize_epoch
      $r.dispatcher_failures = $h.components.dispatcher.details.failures
      $r.delivery_terminal_failures = $h.components.'response-delivery'.details.terminal_failures
      if ($h.components.PSObject.Properties.Name -contains 'response-delivery') {
        $r.response_delivery = $h.components.'response-delivery'.state
      }
      $r.proxy = $h.components.proxy.state
      if (!$r.ready) { $r.state = 'NOT_READY' }
      elseif ($r.control_plane -ne 'polling') { $r.state = 'CONTROL_PLANE_DEGRADED' }
      elseif ($r.mcp -ne 'initialized' -or $r.mcp_child -ne 'running') { $r.state = 'MCP_NOT_INITIALIZED' }
      elseif ($pathOnly) { $r.state = 'HEALTHY_PATH_ONLY' }
      else { $r.state = 'HEALTHY' }
    }
  }
} catch {
  $r.state = 'PROBE_ERROR'
  $r.error_type = $_.Exception.GetType().Name
}
$line = $r | ConvertTo-Json -Compress -Depth 5
if ($Persist) {
  $file = Join-Path $root 'Tunnel-Health.jsonl'
  if (Test-Path -LiteralPath $file) {
    if ((Get-Item -LiteralPath $file).Length -gt 524288) {
      Move-Item -LiteralPath $file -Destination ($file+'.previous') -Force
    }
  }
  Add-Content -LiteralPath $file -Value $line -Encoding UTF8
}
Write-Output $line