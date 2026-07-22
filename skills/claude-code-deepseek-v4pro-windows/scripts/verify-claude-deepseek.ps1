param(
  [Parameter(Mandatory = $true)]
  [string]$TaskOutputDir
)

$ErrorActionPreference = 'Continue'

New-Item -ItemType Directory -Force -Path $TaskOutputDir | Out-Null
$report = Join-Path $TaskOutputDir 'report.md'

function Add-Line {
  param([string]$Line)
  Add-Content -LiteralPath $report -Value $Line -Encoding UTF8
  Write-Host $Line
}

function Add-Output {
  param([string]$Label, $Output)
  Add-Line $Label
  if ($Output) {
    $Output | ForEach-Object { Add-Line ("  " + $_.ToString()) }
  } else {
    Add-Line '  <empty>'
  }
}

Add-Line '# Claude Code DeepSeek V4 Pro Verification'
Add-Line ('Started: ' + (Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz'))

Add-Line '## G02 Environment'
foreach ($cmd in @(
  @{Name='claude'; Args=@('--version')},
  @{Name='node'; Args=@('--version')},
  @{Name='npm.cmd'; Args=@('--version')},
  @{Name='git'; Args=@('--version')}
)) {
  try {
    $out = & $cmd.Name @($cmd.Args) 2>&1
    Add-Line ("Command: " + $cmd.Name + " " + ($cmd.Args -join ' '))
    Add-Line ("ExitCode: " + $LASTEXITCODE)
    Add-Output 'Output:' $out
  } catch {
    Add-Line ("CommandError: " + $cmd.Name + " " + $_.Exception.Message)
  }
}

Add-Line '## G04 Key Check'
$key = [Environment]::GetEnvironmentVariable('DEEPSEEK_API_KEY', 'User')
if ([string]::IsNullOrWhiteSpace($key)) {
  Add-Line 'Result: G04_NEED_DEEPSEEK_API_KEY'
  exit 2
}
Set-Item -Path Env:\DEEPSEEK_API_KEY -Value $key
Add-Line ("Evidence: user_env_present=True; key_length=" + $key.Length + "; full_key_printed=False")
Add-Line 'Result: G04_PASS'

Add-Line '## G05 Env Verify'
$vars = @{
  ANTHROPIC_BASE_URL = 'https://api.deepseek.com/anthropic'
  ANTHROPIC_MODEL = 'deepseek-v4-pro[1m]'
  ANTHROPIC_DEFAULT_OPUS_MODEL = 'deepseek-v4-pro[1m]'
  ANTHROPIC_DEFAULT_SONNET_MODEL = 'deepseek-v4-pro[1m]'
  ANTHROPIC_DEFAULT_HAIKU_MODEL = 'deepseek-v4-flash'
  CLAUDE_CODE_SUBAGENT_MODEL = 'deepseek-v4-flash'
  CLAUDE_CODE_EFFORT_LEVEL = 'max'
}

$envOk = $true
foreach ($name in $vars.Keys) {
  $value = [Environment]::GetEnvironmentVariable($name, 'User')
  if ($value -ne $vars[$name]) { $envOk = $false }
  Set-Item -Path ("Env:\" + $name) -Value $value
  Add-Line ($name + '=' + $value)
}
$token = [Environment]::GetEnvironmentVariable('ANTHROPIC_AUTH_TOKEN', 'User')
Set-Item -Path Env:\ANTHROPIC_AUTH_TOKEN -Value $token
Add-Line ("ANTHROPIC_AUTH_TOKEN_present=" + (-not [string]::IsNullOrWhiteSpace($token)) + "; full_token_printed=False; token_length=" + $token.Length)
if (-not $envOk -or [string]::IsNullOrWhiteSpace($token)) {
  Add-Line 'Result: G05_FAIL'
  exit 1
}
Add-Line 'Result: G05_PASS'

Add-Line '## G06 Minimal API'
$g06 = Join-Path $TaskOutputDir 'g06-temp'
New-Item -ItemType Directory -Force -Path $g06 | Out-Null
Push-Location -LiteralPath $g06
try {
  $out = & claude -p "Respond with exactly: DS_CLAUDE_CODE_OK" 2>&1
  $exit = $LASTEXITCODE
} finally {
  Pop-Location
}
Add-Line ("ExitCode: " + $exit)
Add-Output 'Output:' $out
if ($exit -ne 0 -or (($out | Out-String) -notlike '*DS_CLAUDE_CODE_OK*')) {
  Add-Line 'Result: G06_FAIL'
  exit 1
}
Add-Line 'Result: G06_PASS'

Add-Line '## G07 Read-only Project'
$testDir = Join-Path $TaskOutputDir 'test-project'
New-Item -ItemType Directory -Force -Path $testDir | Out-Null
Set-Content -LiteralPath (Join-Path $testDir 'README.md') -Value "# Test Project`n" -Encoding UTF8
function Snapshot([string]$Root) {
  Get-ChildItem -LiteralPath $Root -Recurse -Force -File | Sort-Object FullName | ForEach-Object {
    $rel = $_.FullName.Substring($Root.Length).TrimStart('\')
    $hash = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash
    [pscustomobject]@{Path=$rel; Length=$_.Length; Hash=$hash}
  }
}
$before = @(Snapshot $testDir)
Push-Location -LiteralPath $testDir
try {
  $out = & claude -p "Inspect the current directory structure, answer in one Chinese sentence, and do not modify files." 2>&1
  $exit = $LASTEXITCODE
} finally {
  Pop-Location
}
$after = @(Snapshot $testDir)
$same = (($before | ConvertTo-Json -Compress) -eq ($after | ConvertTo-Json -Compress))
Add-Line ("ExitCode: " + $exit)
Add-Output 'Output:' $out
Add-Line ("NoModificationEvidence: before_after_snapshot_equal=" + $same)
if ($exit -eq 0 -and $same) {
  Add-Line 'Result: G07_PASS'
  Add-Line 'FINAL_PASS_CLAUDE_CODE_DEEPSEEK_V4PRO_READY'
  exit 0
}
Add-Line 'Result: G07_FAIL'
exit 1
