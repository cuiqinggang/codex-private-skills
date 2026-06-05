param(
  [string]$ReportPath
)

$ErrorActionPreference = 'Stop'

function Write-ReportLine {
  param([string]$Line)
  if ($ReportPath) {
    Add-Content -LiteralPath $ReportPath -Value $Line -Encoding UTF8
  }
  Write-Host $Line
}

$key = [Environment]::GetEnvironmentVariable('DEEPSEEK_API_KEY', 'User')
if ([string]::IsNullOrWhiteSpace($key)) {
  Write-ReportLine 'G05_FAIL_NEED_DEEPSEEK_API_KEY'
  exit 2
}

$desired = [ordered]@{
  ANTHROPIC_BASE_URL = 'https://api.deepseek.com/anthropic'
  ANTHROPIC_AUTH_TOKEN = $key.Trim()
  ANTHROPIC_MODEL = 'deepseek-v4-pro[1m]'
  ANTHROPIC_DEFAULT_OPUS_MODEL = 'deepseek-v4-pro[1m]'
  ANTHROPIC_DEFAULT_SONNET_MODEL = 'deepseek-v4-pro[1m]'
  ANTHROPIC_DEFAULT_HAIKU_MODEL = 'deepseek-v4-flash'
  CLAUDE_CODE_SUBAGENT_MODEL = 'deepseek-v4-flash'
  CLAUDE_CODE_EFFORT_LEVEL = 'max'
}

foreach ($entry in $desired.GetEnumerator()) {
  [Environment]::SetEnvironmentVariable($entry.Key, [string]$entry.Value, 'User')
  Set-Item -Path ("Env:\" + $entry.Key) -Value ([string]$entry.Value)
}

$ok = $true
foreach ($entry in $desired.GetEnumerator()) {
  $actual = [Environment]::GetEnvironmentVariable($entry.Key, 'User')
  if ([string]$actual -ne [string]$entry.Value) {
    $ok = $false
    Write-ReportLine ("VERIFY_FAIL " + $entry.Key)
  }
}

Write-ReportLine ("ANTHROPIC_BASE_URL=" + [Environment]::GetEnvironmentVariable('ANTHROPIC_BASE_URL', 'User'))
Write-ReportLine ("ANTHROPIC_MODEL=" + [Environment]::GetEnvironmentVariable('ANTHROPIC_MODEL', 'User'))
Write-ReportLine ("ANTHROPIC_DEFAULT_HAIKU_MODEL=" + [Environment]::GetEnvironmentVariable('ANTHROPIC_DEFAULT_HAIKU_MODEL', 'User'))
$token = [Environment]::GetEnvironmentVariable('ANTHROPIC_AUTH_TOKEN', 'User')
Write-ReportLine ("ANTHROPIC_AUTH_TOKEN_present=" + (-not [string]::IsNullOrWhiteSpace($token)) + "; full_token_printed=False; token_length=" + $token.Length)

if ($ok) {
  Write-ReportLine 'G05_PASS'
  exit 0
}

Write-ReportLine 'G05_FAIL'
exit 1
