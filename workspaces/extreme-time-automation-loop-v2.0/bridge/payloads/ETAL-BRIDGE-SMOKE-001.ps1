param(
  [Parameter(Mandatory=$true)][string]$BridgeWorkDir,
  [Parameter(Mandatory=$true)][string]$TaskFile
)
$ErrorActionPreference='Stop'
New-Item -ItemType Directory -Path $BridgeWorkDir -Force | Out-Null
$evidence = [ordered]@{
  smoke_id = 'ETAL-BRIDGE-SMOKE-001'
  status = 'PASS'
  machine = $env:COMPUTERNAME
  runner_name = $env:RUNNER_NAME
  os = [System.Environment]::OSVersion.VersionString
  powershell = $PSVersionTable.PSVersion.ToString()
  utc = [DateTimeOffset]::UtcNow.ToString('o')
  task_file = $TaskFile
}
$evidence | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath (Join-Path $BridgeWorkDir 'bridge-smoke-evidence.json') -Encoding UTF8
Get-Content -LiteralPath (Join-Path $BridgeWorkDir 'bridge-smoke-evidence.json') -Raw | Write-Output
exit 0
