param(
  [string]$OutputDirectory = "",
  [switch]$NoWrite
)

$ErrorActionPreference = "Continue"

function Invoke-TextCommand {
  param([string]$Command, [string[]]$Arguments = @())
  try {
    $output = & $Command @Arguments 2>&1
    return @{
      ok = ($LASTEXITCODE -eq 0 -or $null -eq $LASTEXITCODE)
      exit_code = $LASTEXITCODE
      output = (($output | Select-Object -First 20) -join "`n")
    }
  } catch {
    return @{ ok = $false; exit_code = $null; output = $_.Exception.Message }
  }
}

$codexHome = Join-Path $env:USERPROFILE ".codex"
$configPath = Join-Path $codexHome "config.toml"
$agentsPath = Join-Path $codexHome "AGENTS.md"

$codexCli = Invoke-TextCommand -Command "codex" -Arguments @("--version")
$npmCodex = Invoke-TextCommand -Command "npm" -Arguments @("list", "-g", "@openai/codex", "--depth=0")
$node = Invoke-TextCommand -Command "node" -Arguments @("--version")
$npm = Invoke-TextCommand -Command "npm" -Arguments @("--version")
$git = Invoke-TextCommand -Command "git" -Arguments @("--version")
$python = Invoke-TextCommand -Command "python" -Arguments @("--version")
$gh = Invoke-TextCommand -Command "gh" -Arguments @("--version")
$winget = Invoke-TextCommand -Command "winget" -Arguments @("--version")

$modelLine = $null
$pluginLines = @()
if (Test-Path -LiteralPath $configPath) {
  $modelLine = (Select-String -LiteralPath $configPath -Pattern '^model\s*=' | Select-Object -First 1).Line
  $pluginLines = Select-String -LiteralPath $configPath -Pattern '^\[plugins\."(.+)"\]' | ForEach-Object { $_.Matches[0].Groups[1].Value }
}

$agentsText = ""
if (Test-Path -LiteralPath $agentsPath) {
  $agentsText = Get-Content -LiteralPath $agentsPath -Raw
}

$appVersion = $null
try {
  $appVersion = (Get-AppxPackage -Name OpenAI.Codex | Select-Object -First 1 -ExpandProperty Version)
} catch {
  $appVersion = $null
}

$checks = [ordered]@{
  codex_home_exists = (Test-Path -LiteralPath $codexHome)
  config_exists = (Test-Path -LiteralPath $configPath)
  agents_exists = (Test-Path -LiteralPath $agentsPath)
  model_is_gpt55 = ($modelLine -eq 'model = "gpt-5.5"')
  agents_has_yesterday_first = ($agentsText -match 'yesterday-replay-controlled-coding')
  agents_blocks_prerelease = ($agentsText -match 'alpha, beta, pre-release')
  codex_cli_available = $codexCli.ok
  npm_codex_installed = ($npmCodex.output -match '@openai/codex@')
  npm_codex_not_alpha = -not ($npmCodex.output -match 'alpha|beta|pre')
  desktop_app_present = ($null -ne $appVersion)
  node_available = $node.ok
  npm_available = $npm.ok
  git_available = $git.ok
  python_available = $python.ok
  winget_available = $winget.ok
  superpowers_enabled = ($pluginLines -contains 'superpowers@openai-curated')
  browser_enabled = ($pluginLines -contains 'browser@openai-bundled')
  browser_use_enabled = ($pluginLines -contains 'browser-use@openai-bundled')
  chrome_enabled = ($pluginLines -contains 'chrome@openai-bundled')
}

$result = [ordered]@{
  timestamp = (Get-Date).ToString("s")
  codex_home = $codexHome
  codex_cli = $codexCli.output
  npm_codex = $npmCodex.output
  desktop_app_version = $appVersion
  node = $node.output
  npm = $npm.output
  git = $git.output
  python = $python.output
  gh = $gh.output
  winget = $winget.output
  model_line = $modelLine
  enabled_plugins = $pluginLines
  checks = $checks
  pass = -not ($checks.Values -contains $false)
}

$json = $result | ConvertTo-Json -Depth 6

if (-not $NoWrite) {
  if ([string]::IsNullOrWhiteSpace($OutputDirectory)) {
    $OutputDirectory = Join-Path (Get-Location) ("output\codex-lite-power-check-" + (Get-Date -Format "yyyyMMdd-HHmmss"))
  }
  New-Item -ItemType Directory -Force -Path $OutputDirectory | Out-Null
  $outFile = Join-Path $OutputDirectory "codex-lite-power-check.json"
  $json | Set-Content -LiteralPath $outFile -Encoding UTF8
  Write-Output "REPORT=$outFile"
}

Write-Output $json
if ($result.pass) {
  Write-Output "CODEX_LITE_POWER_CHECK_PASS"
  exit 0
}

Write-Output "CODEX_LITE_POWER_CHECK_FAIL"
exit 1
