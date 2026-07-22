param(
  [Parameter(Mandatory=$true)][string]$SiteRoot,
  [string]$ExpectedProjectId = "",
  [string]$OutputJson = ""
)

$ErrorActionPreference = "Stop"
$root = (Resolve-Path -LiteralPath $SiteRoot).Path
$hostingPath = Join-Path $root ".openai\\hosting.json"
$packagePath = Join-Path $root "package.json"
$labPath = Join-Path $root "public\\lab"

$missing = @()
foreach ($item in @($hostingPath, $packagePath, $labPath)) {
  if (-not (Test-Path -LiteralPath $item)) { $missing += $item }
}
if ($missing.Count -gt 0) {
  [pscustomobject]@{ result="BLOCKED"; reason="missing_required_paths"; missing=$missing } | ConvertTo-Json -Depth 6
  exit 2
}

$hosting = Get-Content -LiteralPath $hostingPath -Encoding utf8 -Raw | ConvertFrom-Json
$head = (& git -C $root rev-parse HEAD).Trim()
$branch = (& git -C $root branch --show-current).Trim()
$remote = (& git -C $root remote -v | Select-Object -First 1)
$status = @(& git -C $root status --short)
$manifestPath = Join-Path $labPath "prompt-manifest.json"
$prompt = $null

if (Test-Path -LiteralPath $manifestPath) {
  $manifest = Get-Content -LiteralPath $manifestPath -Encoding utf8 -Raw | ConvertFrom-Json
  $assetPath = Join-Path $labPath $manifest.asset_path
  if (Test-Path -LiteralPath $assetPath) {
    $bytes = [IO.File]::ReadAllBytes($assetPath)
    $text = [Text.Encoding]::UTF8.GetString($bytes)
    $sha = (Get-FileHash -LiteralPath $assetPath -Algorithm SHA256).Hash
    $prompt = [ordered]@{
      path = $assetPath
      characters = $text.Length
      bytes = $bytes.Length
      sha256 = $sha
      expected_characters = $manifest.character_count
      expected_bytes = $manifest.byte_count
      expected_sha256 = $manifest.sha256
      verified = ($text.Length -eq $manifest.character_count -and $bytes.Length -eq $manifest.byte_count -and $sha -eq $manifest.sha256)
    }
  }
}

$result = [ordered]@{
  result = "PASS"
  site_root = $root
  project_id = $hosting.project_id
  expected_project_id = $ExpectedProjectId
  project_id_matches = ([string]::IsNullOrWhiteSpace($ExpectedProjectId) -or $hosting.project_id -eq $ExpectedProjectId)
  git_head = $head
  git_branch = $branch
  git_remote = $remote
  git_status = $status
  codegraph_index_present = (Test-Path -LiteralPath (Join-Path $root ".codegraph"))
  codegraph_cli_available = [bool](Get-Command codegraph -ErrorAction SilentlyContinue)
  prompt = $prompt
}

if (-not $result.project_id_matches -or ($prompt -and -not $prompt.verified)) {
  $result.result = "BLOCKED"
}

$json = $result | ConvertTo-Json -Depth 8
if ($OutputJson) {
  $parent = Split-Path -Parent $OutputJson
  if ($parent) { New-Item -ItemType Directory -Force -Path $parent | Out-Null }
  [IO.File]::WriteAllText($OutputJson, $json, [Text.UTF8Encoding]::new($false))
}
$json
if ($result.result -ne "PASS") { exit 3 }

