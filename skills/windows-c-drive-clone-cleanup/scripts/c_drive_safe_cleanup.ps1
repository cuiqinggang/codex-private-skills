param(
${REDACTED_SECRET}
  [int]$TempOlderThanDays = 7
)

$ErrorActionPreference = "SilentlyContinue"
$stamp = (Get-Date).ToString("yyyyMMdd-HHmmss")
$logPath = Join-Path $OutputDir "c-drive-safe-cleanup-$stamp.md"
New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null

function Get-QuickSize {
  param([string]$Path)
  if (-not (Test-Path -LiteralPath $Path)) { return 0L }
  $sum = (Get-ChildItem -LiteralPath $Path -Force -Recurse -ErrorAction SilentlyContinue |
    Where-Object { -not $_.PSIsContainer } |
    Measure-Object -Property Length -Sum).Sum
  if ($null -eq $sum) { 0L } else { [int64]$sum }
}

function Remove-PathContents {
  param(
    [string]$Path,
    [datetime]$OlderThan = [datetime]::MaxValue
  )
  if (-not (Test-Path -LiteralPath $Path)) {
    return [pscustomobject]@{ Path=$Path; BeforeGB=0; AfterGB=0; FreedGB=0; Status="missing" }
  }
  $before = Get-QuickSize -Path $Path
  Get-ChildItem -LiteralPath $Path -Force -ErrorAction SilentlyContinue |
    Where-Object { $_.LastWriteTime -lt $OlderThan } |
    ForEach-Object {
      Remove-Item -LiteralPath $_.FullName -Recurse -Force -ErrorAction SilentlyContinue
    }
  $after = Get-QuickSize -Path $Path
  [pscustomobject]@{
    Path=$Path
    BeforeGB=[math]::Round($before/1GB,2)
    AfterGB=[math]::Round($after/1GB,2)
    FreedGB=[math]::Round(($before-$after)/1GB,2)
    Status="cleaned"
  }
}

$cutoff = (Get-Date).AddDays(-1 * $TempOlderThanDays)
$targets = @(
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
  @{Path="C:\ProgramData\Microsoft\Windows\WER"; Older=(Get-Date).AddDays(1); Note="Windows error reports"}
)

$results = foreach ($t in $targets) {
  $r = Remove-PathContents -Path $t.Path -OlderThan $t.Older
  $r | Add-Member -NotePropertyName Note -NotePropertyValue $t.Note -Force
  $r
}

$npmResult = ""
if (Get-Command npm -ErrorAction SilentlyContinue) {
  $npmResult = (& npm cache clean --force 2>&1) -join "`n"
} else {
  $npmResult = "npm not found"
}

$pipResult = ""
if (Get-Command pip -ErrorAction SilentlyContinue) {
  $pipResult = (& pip cache purge 2>&1) -join "`n"
} else {
  $pipResult = "pip not found"
}

$disk = Get-CimInstance Win32_LogicalDisk -Filter "DeviceID='C:'" |
  Select-Object DeviceID,
    @{n="SizeGB";e={[math]::Round($_.Size/1GB,2)}},
    @{n="FreeGB";e={[math]::Round($_.FreeSpace/1GB,2)}},
    @{n="UsedGB";e={[math]::Round(($_.Size-$_.FreeSpace)/1GB,2)}}

$lines = New-Object System.Collections.Generic.List[string]
$lines.Add("# C Drive Safe Cleanup")
$lines.Add("")
$lines.Add("Generated: $((Get-Date).ToString('yyyy-MM-dd HH:mm:ss'))")
$lines.Add("")
$lines.Add("## Cleaned Paths")
$lines.Add("")
$lines.Add("| Freed GB | Before GB | After GB | Note | Path |")
$lines.Add("|---:|---:|---:|---|---|")
foreach ($r in $results) {
  $lines.Add("| $($r.FreedGB) | $($r.BeforeGB) | $($r.AfterGB) | $($r.Note) | `$($r.Path)` |")
}
$lines.Add("")
$lines.Add("## Package Caches")
$lines.Add("")
$lines.Add("npm:")
$lines.Add('```text')
$lines.Add($npmResult)
$lines.Add('```')
$lines.Add("")
$lines.Add("pip:")
$lines.Add('```text')
$lines.Add($pipResult)
$lines.Add('```')
$lines.Add("")
$lines.Add("## Disk After")
$lines.Add("")
$lines.Add("| Drive | Size GB | Used GB | Free GB |")
$lines.Add("|---|---:|---:|---:|")
$lines.Add("| $($disk.DeviceID) | $($disk.SizeGB) | $($disk.UsedGB) | $($disk.FreeGB) |")
$lines | Set-Content -LiteralPath $logPath -Encoding UTF8

[pscustomobject]@{
  Log=$logPath
  FreedGB=[math]::Round((($results | Measure-Object -Property FreedGB -Sum).Sum),2)
  CUsedGB=$disk.UsedGB
  CFreeGB=$disk.FreeGB
}
