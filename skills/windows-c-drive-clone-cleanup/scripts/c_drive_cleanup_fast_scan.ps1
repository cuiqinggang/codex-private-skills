param(
  [string]$OutputDir = "C:\Users\A\Documents\Codex\2026-06-28\c-c-c-c-200-gb\outputs"
)

$ErrorActionPreference = "SilentlyContinue"
$stamp = (Get-Date).ToString("yyyyMMdd-HHmmss")
$nullDest = "C:\Users\A\Documents\Codex\2026-06-28\c-c-c-c-200-gb\work\robocopy-null"
New-Item -ItemType Directory -Force -Path $OutputDir,$nullDest | Out-Null

function Get-RoboSize {
  param([string]$Path)
  if (-not (Test-Path -LiteralPath $Path)) {
    return [pscustomobject]@{ Path=$Path; Exists=$false; Bytes=0; GB=0; Class="missing" }
  }
  $out = & robocopy $Path $nullDest /L /S /BYTES /NJH /NFL /NDL /NP /R:0 /W:0 2>$null
  $bytesLine = $out | Where-Object { $_ -match '^\s*Bytes\s*:' } | Select-Object -Last 1
  $bytes = 0L
  if ($bytesLine -match 'Bytes\s*:\s+([0-9]+)') { $bytes = [int64]$Matches[1] }
  [pscustomobject]@{
    Path=$Path
    Exists=$true
    Bytes=$bytes
    GB=[math]::Round($bytes/1GB,2)
    Class=""
  }
}

$disk = Get-CimInstance Win32_LogicalDisk -Filter "DeviceID='C:'" |
  Select-Object DeviceID,
    @{n="SizeGB";e={[math]::Round($_.Size/1GB,2)}},
    @{n="FreeGB";e={[math]::Round($_.FreeSpace/1GB,2)}},
    @{n="UsedGB";e={[math]::Round(($_.Size-$_.FreeSpace)/1GB,2)}}

$paths = @(
  @{Path="C:\Users\A\AppData\Local\Temp"; Class="safe-clean-temp"},
  @{Path="C:\Windows\Temp"; Class="safe-clean-temp-admin"},
  @{Path="C:\Windows\SoftwareDistribution\Download"; Class="safe-clean-windows-update-cache"},
  @{Path="C:\ProgramData\Microsoft\Windows\DeliveryOptimization\Cache"; Class="safe-clean-delivery-cache"},
  @{Path="C:\ProgramData\Microsoft\Windows\WER"; Class="safe-clean-error-reports"},
  @{Path="C:\Users\A\AppData\Local\CrashDumps"; Class="safe-clean-crash-dumps"},
  @{Path="C:\`$Recycle.Bin"; Class="safe-clean-recycle-bin-review"},
  @{Path="C:\Windows.old"; Class="safe-clean-after-confirm-old-windows"},
  @{Path="C:\Users\A\Downloads"; Class="review-user-files"},
  @{Path="C:\Users\A\Desktop"; Class="review-user-files"},
  @{Path="C:\Users\A\Videos"; Class="review-user-files"},
  @{Path="C:\Users\A\Documents\Codex"; Class="review-codex-workspaces"},
  @{Path="C:\Users\A\.codex"; Class="review-codex-config-skills"},
  @{Path="C:\Users\A\AppData\Local\Packages"; Class="review-store-app-data"},
  @{Path="C:\Users\A\AppData\Local\Docker"; Class="review-docker"},
  @{Path="C:\Users\A\.ollama"; Class="review-ai-models"},
  @{Path="C:\Users\A\.cache\huggingface"; Class="review-ai-models"},
  @{Path="C:\Users\A\AppData\Local\pip\Cache"; Class="safe-clean-dev-cache"},
  @{Path="C:\Users\A\AppData\Local\npm-cache"; Class="safe-clean-dev-cache"},
  @{Path="C:\Users\A\AppData\Local\pnpm"; Class="review-dev-store"},
  @{Path="C:\Users\A\AppData\Local\Microsoft\Edge\User Data\Default\Cache"; Class="safe-clean-browser-cache"},
  @{Path="C:\Users\A\AppData\Local\Google\Chrome\User Data\Default\Cache"; Class="safe-clean-browser-cache"}
)

$results = foreach ($p in $paths) {
  $r = Get-RoboSize -Path $p.Path
  $r.Class = $p.Class
  $r
}
$results = $results | Sort-Object Bytes -Descending

$outJson = Join-Path $OutputDir "c-drive-cleanup-fast-scan-$stamp.json"
$outMd = Join-Path $OutputDir "c-drive-cleanup-fast-scan-$stamp.md"

[ordered]@{ generatedAt=(Get-Date).ToString("s"); disk=$disk; candidates=$results } |
  ConvertTo-Json -Depth 5 |
  Set-Content -LiteralPath $outJson -Encoding UTF8

$lines = New-Object System.Collections.Generic.List[string]
$lines.Add("# C Drive Cleanup Fast Scan")
$lines.Add("")
$lines.Add("Generated: $((Get-Date).ToString('yyyy-MM-dd HH:mm:ss'))")
$lines.Add("")
$lines.Add("## Disk")
$lines.Add("")
$lines.Add("| Drive | Size GB | Used GB | Free GB |")
$lines.Add("|---|---:|---:|---:|")
$lines.Add("| $($disk.DeviceID) | $($disk.SizeGB) | $($disk.UsedGB) | $($disk.FreeGB) |")
$lines.Add("")
$lines.Add("## Candidates")
$lines.Add("")
$lines.Add("| GB | Class | Path |")
$lines.Add("|---:|---|---|")
foreach ($r in $results) {
  $lines.Add("| $($r.GB) | $($r.Class) | `$($r.Path)` |")
}
$lines | Set-Content -LiteralPath $outMd -Encoding UTF8

[pscustomobject]@{
  Markdown=$outMd
  Json=$outJson
  CSizeGB=$disk.SizeGB
  CUsedGB=$disk.UsedGB
  CFreeGB=$disk.FreeGB
  TopCandidates=($results | Select-Object -First 10)
}
