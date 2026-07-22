param(
${REDACTED_SECRET}
)

$ErrorActionPreference = "Continue"
New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null
$report = Join-Path $OutputDir "ClaudeCode_Cursor_Existing_Stack_Info_Report.md"

function Get-CmdLine($Name) {
  $cmd = Get-Command $Name -ErrorAction SilentlyContinue
  if ($cmd) { return $cmd.Source }
  return "NOT_FOUND"
}

function Get-VersionLine($Command, $CommandArgs) {
  try {
    $output = & $Command @CommandArgs 2>&1 | Select-Object -First 3
    if ($LASTEXITCODE -eq 0 -or $output) { return ($output -join " ") }
    return "NO_OUTPUT"
  } catch {
    return "ERROR: $($_.Exception.Message)"
  }
}

function Get-EnvPresence($Name) {
  $user = [Environment]::GetEnvironmentVariable($Name, "User")
  $machine = [Environment]::GetEnvironmentVariable($Name, "Machine")
  $process = [Environment]::GetEnvironmentVariable($Name, "Process")
  [PSCustomObject]@{
    Name = $Name
    Process = [bool]$process
    User = [bool]$user
    Machine = [bool]$machine
  }
}

$envNames = @(
  "ANTHROPIC_BASE_URL",
  "ANTHROPIC_MODEL",
  "ANTHROPIC_DEFAULT_OPUS_MODEL",
  "ANTHROPIC_DEFAULT_SONNET_MODEL",
  "ANTHROPIC_DEFAULT_HAIKU_MODEL",
  "CLAUDE_CODE_SUBAGENT_MODEL",
  "ANTHROPIC_AUTH_TOKEN",
  "ANTHROPIC_API_KEY",
  "DEEPSEEK_API_KEY"
)

$ports = Get-NetTCPConnection -LocalPort 15721 -ErrorAction SilentlyContinue |
  Select-Object LocalAddress, LocalPort, State, OwningProcess

$lines = @()
$lines += "# Claude Code Cursor Existing Stack Info Report"
$lines += ""
$lines += "Generated: $(Get-Date -Format o)"
$lines += ""
$lines += "## Commands"
$lines += ""
$lines += "| Command | Path | Version Probe |"
$lines += "|---|---|---|"
$lines += "| claude | $(Get-CmdLine claude) | $(Get-VersionLine claude @('--version')) |"
$lines += "| ccr | $(Get-CmdLine ccr) | $(Get-VersionLine ccr @('--version')) |"
$lines += "| node | $(Get-CmdLine node) | $(Get-VersionLine node @('--version')) |"
$lines += "| npm | $(Get-CmdLine npm.cmd) | $(Get-VersionLine npm.cmd @('--version')) |"
$lines += "| git | $(Get-CmdLine git) | $(Get-VersionLine git @('--version')) |"
$lines += ""
$lines += "## Secret-Safe Environment Presence"
$lines += ""
$lines += "| Name | Process | User | Machine |"
$lines += "|---|---:|---:|---:|"
foreach ($item in ($envNames | ForEach-Object { Get-EnvPresence $_ })) {
  $lines += "| $($item.Name) | $($item.Process) | $($item.User) | $($item.Machine) |"
}
$lines += ""
$lines += "## Important Paths"
$lines += ""
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
$lines += "- PowerShell profile: $(Test-Path $PROFILE)"
$lines += ""
$lines += "## Legacy Proxy Port 15721"
$lines += ""
if ($ports) {
  $lines += ($ports | Format-Table -AutoSize | Out-String)
} else {
  $lines += "No listener found on local port 15721."
}
$lines += ""
$lines += "## Next Required Reports"
$lines += ""
$lines += '- `ClaudeCode_Cursor_Blocker_Report.md`'
$lines += '- `ClaudeCode_Cursor_PreDeploy_Blocker_Elimination_Report.md`'

$lines | Set-Content -LiteralPath $report -Encoding UTF8
Write-Output $report
