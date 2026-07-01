param(
  [string]$OutputDir = "C:\Users\A\Documents\Codex\2026-06-28\c-c-c-c-200-gb\outputs"
)

$ErrorActionPreference = "SilentlyContinue"
$stamp = (Get-Date).ToString("yyyyMMdd-HHmmss")
$logPath = Join-Path $OutputDir "c-drive-cache-recycle-cleanup-$stamp.md"
New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null

function Get-Size {
  param([string]$Path)
  if (-not (Test-Path -LiteralPath $Path)) { return 0L }
  $sum = (Get-ChildItem -LiteralPath $Path -Force -Recurse -ErrorAction SilentlyContinue |
    Where-Object { -not $_.PSIsContainer } |
    Measure-Object -Property Length -Sum).Sum
  if ($null -eq $sum) { 0L } else { [int64]$sum }
}

function Clear-Contents {
  param([string]$Path)
  $before = Get-Size -Path $Path
  if (Test-Path -LiteralPath $Path) {
    Get-ChildItem -LiteralPath $Path -Force -ErrorAction SilentlyContinue |
      ForEach-Object { Remove-Item -LiteralPath $_.FullName -Recurse -Force -ErrorAction SilentlyContinue }
  }
  $after = Get-Size -Path $Path
  [pscustomobject]@{
    Path=$Path
    BeforeGB=[math]::Round($before/1GB,2)
    AfterGB=[math]::Round($after/1GB,2)
    FreedGB=[math]::Round(($before-$after)/1GB,2)
  }
}

$targets = @(
  "C:\Users\A\AppData\Local\Temp",
  "C:\Users\A\AppData\Local\npm-cache"
)
$results = foreach ($target in $targets) { Clear-Contents -Path $target }

$recycleBefore = Get-Size -Path "C:\`$Recycle.Bin"
Clear-RecycleBin -DriveLetter C -Force -ErrorAction SilentlyContinue
$recycleAfter = Get-Size -Path "C:\`$Recycle.Bin"
$results += [pscustomobject]@{
  Path="C:\`$Recycle.Bin"
  BeforeGB=[math]::Round($recycleBefore/1GB,2)
  AfterGB=[math]::Round($recycleAfter/1GB,2)
  FreedGB=[math]::Round(($recycleBefore-$recycleAfter)/1GB,2)
}

$disk = Get-CimInstance Win32_LogicalDisk -Filter "DeviceID='C:'" |
  Select-Object DeviceID,
    @{n="SizeGB";e={[math]::Round($_.Size/1GB,2)}},
    @{n="FreeGB";e={[math]::Round($_.FreeSpace/1GB,2)}},
    @{n="UsedGB";e={[math]::Round(($_.Size-$_.FreeSpace)/1GB,2)}}

$lines = New-Object System.Collections.Generic.List[string]
$lines.Add("# C Drive Cache And Recycle Cleanup")
$lines.Add("")
$lines.Add("Generated: $((Get-Date).ToString('yyyy-MM-dd HH:mm:ss'))")
$lines.Add("")
$lines.Add("| Freed GB | Before GB | After GB | Path |")
$lines.Add("|---:|---:|---:|---|")
foreach ($r in $results) {
  $lines.Add("| $($r.FreedGB) | $($r.BeforeGB) | $($r.AfterGB) | $($r.Path) |")
}
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
