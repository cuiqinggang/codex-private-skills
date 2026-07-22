param(
  [string]$TaskName = "Codex_SelfImprovement_Audit_Biweekly",
  [string]$Time = "10:30",
  [string]$Day = "MON"
)

$ErrorActionPreference = "Stop"

${REDACTED_SECRET}
if (-not (Test-Path -LiteralPath $scriptPath)) {
  throw "Audit script not found: $scriptPath"
}

$argument = "-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File `"$scriptPath`" -Mode ReportOnly"

$previousErrorActionPreference = $ErrorActionPreference
$ErrorActionPreference = "Continue"
$existing = schtasks /query /TN $TaskName /FO LIST 2>$null
$ErrorActionPreference = $previousErrorActionPreference
if ($LASTEXITCODE -eq 0 -and $existing) {
  schtasks /delete /TN $TaskName /F | Out-Null
}

schtasks /create /TN $TaskName /SC WEEKLY /MO 2 /D $Day /ST $Time /TR "powershell.exe $argument" /F | Out-Null

$query = schtasks /query /TN $TaskName /FO LIST /V
${REDACTED_SECRET}
New-Item -ItemType Directory -Force -Path $reportRoot | Out-Null
$query | Set-Content -LiteralPath (Join-Path $reportRoot "scheduled-task-latest.txt") -Encoding UTF8

Write-Output "CODEX_SELF_IMPROVEMENT_BIWEEKLY_TASK_REGISTERED"
Write-Output $TaskName
