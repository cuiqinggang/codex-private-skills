param(
  [string]$OutputDirectory = (Join-Path (Get-Location) "open-design-codex-connectivity-check")
)

$ErrorActionPreference = "SilentlyContinue"
New-Item -ItemType Directory -Force -Path $OutputDirectory | Out-Null

$codexCommands = @("codex", "codex.cmd", "codex.exe")
$codexFound = @()
foreach ($cmd in $codexCommands) {
  $hit = Get-Command $cmd -ErrorAction SilentlyContinue
  if ($hit) {
    $codexFound += [ordered]@{ name = $cmd; source = $hit.Source; version = $hit.Version.ToString() }
  }
}

$openDesignProcesses = Get-CimInstance Win32_Process |
  Where-Object { $_.CommandLine -match "open.?design|opendesign|memory-llm|codex" } |
  Select-Object ProcessId, Name, CommandLine

$logCandidates = @(
${REDACTED_SECRET}
${REDACTED_SECRET}
)

$evidence = @()
foreach ($path in $logCandidates) {
  if (Test-Path -LiteralPath $path) {
    $text = Get-Content -LiteralPath $path -Raw
    $evidence += [ordered]@{
      path = $path
      exists = $true
      mentionsReconnect = ($text -like "*Reconnecting...*")
      mentionsTimeout60 = ($text -like "*60*timeout*" -or $text -like "*60 second*")
      mentionsFinalSuccess = ($text -like "*Final run status succeeded*" -or $text -like "*PASS*")
    }
  } else {
    $evidence += [ordered]@{ path = $path; exists = $false }
  }
}

$pass = ($codexFound.Count -gt 0) -and (($evidence | Where-Object { $_.exists }).Count -gt 0)

$report = [ordered]@{
  created_at = (Get-Date).ToString("s")
  status = $(if ($pass) { "PASS_READONLY_EVIDENCE_AVAILABLE" } else { "FAIL_INSUFFICIENT_EVIDENCE" })
  codexCommands = $codexFound
  relatedProcesses = $openDesignProcesses
  archivedEvidence = $evidence
  note = "Read-only check. No daemon restart, no bundle patch, no model call."
}

$jsonPath = Join-Path $OutputDirectory "open-design-codex-connectivity-check.json"
$report | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $jsonPath -Encoding UTF8

if ($pass) {
  Write-Output "OPEN_DESIGN_CODEX_CONNECTIVITY_READONLY_PASS"
} else {
  Write-Output "OPEN_DESIGN_CODEX_CONNECTIVITY_READONLY_FAIL"
}
Write-Output $jsonPath
