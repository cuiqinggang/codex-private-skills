$ErrorActionPreference = "Stop"

$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$backupRoot = "G:\GreatWall_GT6_SSD_OEM_Win10_File_Copy_Backup_835C"
$reportDir = "C:\Users\A\Desktop\835C-ssd-simple-file-copy-backup"
$zipPath = "C:\Users\A\Desktop\835C.zip"

New-Item -ItemType Directory -Force -Path $backupRoot, $reportDir | Out-Null

$readme = @"
# Great Wall GT6 SSD Original Windows 10 File Copy Backup - 835C

Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')

Purpose:
- Original Great Wall GT6 SSD preinstalled Windows 10 baseline backup.
- This is a simple file/folder copy of D:, E:, and F: to G:.

Method:
- No WIM.
- No DISM.
- No compression.
- No deep verification.
- No partition delete, format, merge, shrink, or resize.

Excluded:
- pagefile.sys
- hiberfil.sys
- swapfile.sys
- `$Recycle.Bin
- System Volume Information
- Common temp/cache folders

Target:
- $backupRoot
"@

$readmePath = Join-Path $backupRoot "README_Original_GreatWall_GT6_SSD_Windows10_Baseline_835C.md"
$readme | Set-Content -LiteralPath $readmePath -Encoding UTF8

$copies = @(
  @{ Source = "D:\"; Dest = (Join-Path $backupRoot "D_system_original") },
  @{ Source = "E:\"; Dest = (Join-Path $backupRoot "E_software_original") },
  @{ Source = "F:\"; Dest = (Join-Path $backupRoot "F_documents_original") }
)

$commonArgs = @(
  "/E",
  "/COPY:DAT",
  "/DCOPY:DAT",
  "/R:1",
  "/W:1",
  "/XJ",
  "/FFT",
  "/NP",
  "/TEE"
)

$excludeDirs = @(
  "`$Recycle.Bin",
  "System Volume Information",
  "Temp",
  "Windows\Temp",
  "Windows\SoftwareDistribution\Download",
  "AppData\Local\Temp",
  "INetCache",
  "Cache"
)

$excludeFiles = @(
  "pagefile.sys",
  "hiberfil.sys",
  "swapfile.sys"
)

$results = @()
foreach ($copy in $copies) {
  New-Item -ItemType Directory -Force -Path $copy.Dest | Out-Null
  $drive = $copy.Source.Substring(0, 1)
  $log = Join-Path $reportDir "835C-robocopy-$drive.log"
  $args = @($copy.Source, $copy.Dest) + $commonArgs + @("/LOG:$log", "/XD") + $excludeDirs + @("/XF") + $excludeFiles
  & robocopy.exe @args
  $code = $LASTEXITCODE
  $results += [pscustomobject]@{
    Source = $copy.Source
    Destination = $copy.Dest
    RobocopyExitCode = $code
    RobocopyStatus = if ($code -le 7) { "OK_OR_MINOR_SKIPS" } else { "FAILED" }
    Log = $log
  }
}

$inventory = foreach ($copy in $copies) {
  $dest = $copy.Dest
  $files = @(Get-ChildItem -LiteralPath $dest -Recurse -Force -File -ErrorAction SilentlyContinue)
  [pscustomobject]@{
    Source = $copy.Source
    Destination = $dest
    FileCount = $files.Count
    SizeGB = [math]::Round((($files | Measure-Object -Property Length -Sum).Sum) / 1GB, 3)
  }
}

$results | Export-Csv -LiteralPath (Join-Path $reportDir "835C-copy-results.csv") -NoTypeInformation -Encoding UTF8
$inventory | Export-Csv -LiteralPath (Join-Path $reportDir "835C-destination-inventory.csv") -NoTypeInformation -Encoding UTF8

$anyFail = @($results | Where-Object { $_.RobocopyExitCode -gt 7 }).Count -gt 0
$status = if ($anyFail) { "SSD_SIMPLE_FILE_COPY_BACKUP_WARN" } else { "SSD_SIMPLE_FILE_COPY_BACKUP_PASS" }

$report = @"
# 835C Simple SSD File Copy Backup - Final Report

Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')

## Result

- Final status: $status
- Source SSD content: D:, E:, F:
- Target backup folder: $backupRoot
- Meaning: Original Great Wall GT6 SSD preinstalled Windows 10 baseline backup.
- Method: simple file/folder copy.
- WIM used: No
- DISM used: No
- Compression used: No
- Deep verification used: No
- D/E/F deleted/formatted/merged: No
- C drive touched: No

## Exclusions

- pagefile.sys
- hiberfil.sys
- swapfile.sys
- `$Recycle.Bin
- System Volume Information
- Common temp/cache folders

## Copy Results

$($results | Format-Table -AutoSize | Out-String)

## Destination Inventory

$($inventory | Format-Table -AutoSize | Out-String)

## Files

- Backup README: $readmePath
- Report folder: $reportDir
- Zip: $zipPath
"@

$reportPath = Join-Path $reportDir "835C-final-report.md"
$report | Set-Content -LiteralPath $reportPath -Encoding UTF8

if (Test-Path -LiteralPath $zipPath) {
  Remove-Item -LiteralPath $zipPath -Force
}
Compress-Archive -LiteralPath $reportDir -DestinationPath $zipPath -Force

Write-Host "835C_STATUS=$status"
Write-Host "835C_BACKUP_ROOT=$backupRoot"
Write-Host "835C_REPORT=$reportPath"
Write-Host "835C_ZIP=$zipPath"

exit $(if ($anyFail) { 1 } else { 0 })
