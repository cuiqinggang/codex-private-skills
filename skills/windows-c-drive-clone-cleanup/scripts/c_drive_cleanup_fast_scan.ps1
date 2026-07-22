param(
${REDACTED_SECRET}
)

$ErrorActionPreference = "SilentlyContinue"
$stamp = (Get-Date).ToString("yyyyMMdd-HHmmss")
${REDACTED_SECRET}
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
${REDACTED_SECRET}
  @{Path="C:\Windows\Temp"; Class="safe-clean-temp-admin"},
  @{Path="C:\Windows\SoftwareDistribution\Download"; Class="safe-clean-windows-update-cache"},
  @{Path="C:\ProgramData\Microsoft\Windows\DeliveryOptimization\Cache"; Class="safe-clean-delivery-cache"},
  @{Path="C:\ProgramData\Microsoft\Windows\WER"; Class="safe-clean-error-reports"},
${REDACTED_SECRET}
  @{Path="C:\`$Recycle.Bin"; Class="safe-clean-recycle-bin-review"},
  @{Path="C:\Windows.old"; Class="safe-clean-after-confirm-old-windows"},
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
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
