param(
${REDACTED_SECRET}
  [string]$WikiRoot = "20_LLM_WIKI",
  [string]$OutputPath = ""
)

$ErrorActionPreference = "Stop"

$root = Join-Path $VaultRoot $WikiRoot
if (-not (Test-Path -LiteralPath $root)) {
  throw "Wiki root not found: $root"
}

$files = Get-ChildItem -LiteralPath $root -Recurse -File -Filter *.md
$relativeToVault = {
  param($path)
  $path.Substring($VaultRoot.TrimEnd('\').Length + 1).Replace('\','/')
}

$byStem = @{}
$byRelNoExt = @{}
foreach ($file in $files) {
  $rel = & $relativeToVault $file.FullName
  $relNoExt = [System.IO.Path]::ChangeExtension($rel, $null)
  $byStem[[System.IO.Path]::GetFileNameWithoutExtension($file.Name)] = $true
  $byRelNoExt[$relNoExt] = $true
}

$missingFrontmatter = New-Object System.Collections.Generic.List[string]
$stalePages = New-Object System.Collections.Generic.List[string]
$missingLinks = New-Object System.Collections.Generic.List[string]
$inbound = @{}

foreach ($file in $files) {
  $rel = & $relativeToVault $file.FullName
  $inbound[$rel] = 0
}

$now = Get-Date
foreach ($file in $files) {
  $rel = & $relativeToVault $file.FullName
  $text = Get-Content -LiteralPath $file.FullName -Raw -Encoding UTF8

  if ($text -notmatch '^\s*---[\s\S]*?---') {
    $missingFrontmatter.Add($rel)
  }

  if (($now - $file.LastWriteTime).TotalDays -gt 90) {
    $stalePages.Add($rel)
  }

  $matches = [regex]::Matches($text, '\[\[([^\]|#]+)')
  foreach ($m in $matches) {
    $target = $m.Groups[1].Value.Trim().Replace('\','/')
    $targetNoExt = [System.IO.Path]::ChangeExtension($target, $null)
    $targetStem = [System.IO.Path]::GetFileNameWithoutExtension($target)

    $resolved = $null
    foreach ($candidate in @($target, $targetNoExt)) {
      if ($byRelNoExt.ContainsKey($candidate)) {
        $resolved = $candidate
        break
      }
      if ($byRelNoExt.ContainsKey("20_LLM_WIKI/wiki/$candidate")) {
        $resolved = "20_LLM_WIKI/wiki/$candidate"
        break
      }
    }
    if (-not $resolved -and $byStem.ContainsKey($targetStem)) {
      $resolved = $targetStem
    }

    if (-not $resolved) {
      $missingLinks.Add("$rel -> $target")
    } else {
      foreach ($key in @($inbound.Keys)) {
        $keyNoExt = [System.IO.Path]::ChangeExtension($key, $null)
        if ($keyNoExt -eq $resolved -or [System.IO.Path]::GetFileNameWithoutExtension($key) -eq $resolved) {
          $inbound[$key] = $inbound[$key] + 1
        }
      }
    }
  }
}

$orphans = @()
foreach ($file in $files) {
  $rel = & $relativeToVault $file.FullName
  if ($rel -notmatch '/raw/' -and $rel -ne '20_LLM_WIKI/index.md' -and $inbound[$rel] -eq 0) {
    $orphans += $rel
  }
}

$report = [ordered]@{
  generated = (Get-Date).ToString("s")
  vault_root = $VaultRoot
  wiki_root = $root
  file_count = $files.Count
  missing_frontmatter_count = $missingFrontmatter.Count
  missing_frontmatter = $missingFrontmatter
  missing_links_count = $missingLinks.Count
  missing_links = $missingLinks
  orphan_count = $orphans.Count
  orphans = $orphans
  stale_pages_count = $stalePages.Count
  stale_pages = $stalePages
}

if (-not $OutputPath) {
  $OutputPath = Join-Path (Get-Location) "wiki-lint-basic-report.json"
}

$report | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $OutputPath -Encoding UTF8
Write-Host "WIKI_LINT_BASIC_DONE"
Write-Host "Output: $OutputPath"

