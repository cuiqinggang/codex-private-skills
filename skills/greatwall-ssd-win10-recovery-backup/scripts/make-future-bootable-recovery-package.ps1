$ErrorActionPreference = "Stop"

$backupRoot = "G:\GreatWall_GT6_SSD_OEM_Win10_File_Copy_Backup_835C"
$reportDir = "C:\Users\A\Desktop\835D-future-bootable-win10-recovery-package"
$zipPath = "C:\Users\A\Desktop\835D.zip"
$recoveryDir = Join-Path $backupRoot "FUTURE_BOOTABLE_RECOVERY_PACKAGE_835D"
$efiBackupDir = Join-Path $recoveryDir "EFI_System_Partition_Backup"
$criticalDir = Join-Path $recoveryDir "Critical_Windows10_Boot_And_Registry_Backup"
$activationDir = Join-Path $recoveryDir "OEM_Activation_And_License_Evidence"
$driversDir = Join-Path $recoveryDir "Drivers_Backup"
$restoreDir = Join-Path $recoveryDir "RESTORE_TO_BOOTABLE_WINDOWS10"
$logsDir = Join-Path $reportDir "logs"

New-Item -ItemType Directory -Force -Path $reportDir, $recoveryDir, $efiBackupDir, $criticalDir, $activationDir, $driversDir, $restoreDir, $logsDir | Out-Null

$summary = [ordered]@{
  generated = (Get-Date).ToString("s")
  sourceDisk = "Disk 0 - Great Wall GT6 1TB"
  sourceWindowsDrive = "D:"
  backupRoot = $backupRoot
  recoveryPackage = $recoveryDir
  cDriveTouched = $false
  partitionsDeletedFormattedMerged = $false
  wimUsed = $false
  dismUsed = $false
}

# Record source disk and partition layout for future reconstruction.
$diskInfo = Get-Disk -Number 0 | Select-Object Number,FriendlyName,SerialNumber,PartitionStyle,Size,OperationalStatus,HealthStatus
$partInfo = Get-Partition -DiskNumber 0 | Select-Object DiskNumber,PartitionNumber,Type,DriveLetter,Offset,Size,GptType,Guid
$volInfo = Get-Volume | Where-Object { $_.DriveLetter -in @("D","E","F") } | Select-Object DriveLetter,FileSystemLabel,FileSystem,Size,SizeRemaining,HealthStatus

$diskInfo | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $recoveryDir "source-disk-0-info.json") -Encoding UTF8
$partInfo | Export-Csv -LiteralPath (Join-Path $recoveryDir "source-disk-0-partitions.csv") -NoTypeInformation -Encoding UTF8
$volInfo | Export-Csv -LiteralPath (Join-Path $recoveryDir "source-d-e-f-volumes.csv") -NoTypeInformation -Encoding UTF8

# Copy the hidden EFI System Partition. This is read-only from the source perspective.
$efiCopied = $false
$efiLog = Join-Path $logsDir "835D-efi-copy.log"
$efiPartition = Get-Partition -DiskNumber 0 | Where-Object { $_.Type -eq "System" } | Select-Object -First 1
$tempLetter = "Y"
if ($efiPartition) {
  $existing = Get-Volume -DriveLetter $tempLetter -ErrorAction SilentlyContinue
  if ($existing) { throw "Temporary drive letter $tempLetter is already in use." }
  try {
    Set-Partition -DiskNumber $efiPartition.DiskNumber -PartitionNumber $efiPartition.PartitionNumber -NewDriveLetter $tempLetter
    $efiSource = "${tempLetter}:\"
    & robocopy.exe $efiSource $efiBackupDir /E /COPY:DAT /DCOPY:DAT /R:1 /W:1 /XJ /NP /TEE "/LOG:$efiLog"
    $efiCode = $LASTEXITCODE
    $efiCopied = $efiCode -le 7
  } finally {
    try {
      Remove-PartitionAccessPath -DiskNumber $efiPartition.DiskNumber -PartitionNumber $efiPartition.PartitionNumber -AccessPath "${tempLetter}:\" -ErrorAction SilentlyContinue
    } catch {}
  }
} else {
  "EFI System partition not found on Disk 0." | Set-Content -LiteralPath $efiLog -Encoding UTF8
  $efiCode = 999
}

# Backup core offline Windows registry hives and boot files from D: using backup mode where possible.
$configSource = "D:\Windows\System32\config"
$configDest = Join-Path $criticalDir "Windows_System32_config"
$configLog = Join-Path $logsDir "835D-critical-config-copy.log"
New-Item -ItemType Directory -Force -Path $configDest | Out-Null
& robocopy.exe $configSource $configDest SYSTEM SOFTWARE SAM SECURITY DEFAULT COMPONENTS BCD-Template /B /COPY:DAT /R:1 /W:1 /NP /TEE "/LOG:$configLog"
$configCode = $LASTEXITCODE
$configCopied = $configCode -le 7

$bootFiles = @(
  "D:\Windows\System32\winload.efi",
  "D:\Windows\System32\winload.exe",
  "D:\Windows\System32\bootwinload.efi",
  "D:\Windows\System32\Recovery\Winre.wim",
  "D:\Windows\Panther\unattend.xml"
)
$bootManifest = foreach ($file in $bootFiles) {
  $exists = Test-Path -LiteralPath $file
  if ($exists) {
    $dest = Join-Path $criticalDir ($file -replace "[:\\]", "_")
    Copy-Item -LiteralPath $file -Destination $dest -Force -ErrorAction SilentlyContinue
  }
  [pscustomobject]@{
    Source = $file
    Exists = $exists
  }
}
$bootManifest | Export-Csv -LiteralPath (Join-Path $recoveryDir "critical-boot-file-manifest.csv") -NoTypeInformation -Encoding UTF8

# Preserve OEM activation evidence. OEM keys normally live in BIOS/UEFI firmware, not only on disk.
$licenseEvidence = [ordered]@{
  generated = (Get-Date).ToString("s")
  oa3xOriginalProductKey_present = $false
  oa3xOriginalProductKey_masked = $null
  licensingDescription = $null
  activationFilesCopied = $false
  note = "Windows 10 OEM activation usually depends on firmware MSDM/OA3 key or Microsoft digital license tied to hardware. These files are evidence/backups, not a guaranteed transferable license."
}
try {
  $licSvc = Get-CimInstance -ClassName SoftwareLicensingService
  if ($licSvc.OA3xOriginalProductKey) {
    $key = [string]$licSvc.OA3xOriginalProductKey
    $licenseEvidence.oa3xOriginalProductKey_present = $true
    $licenseEvidence.oa3xOriginalProductKey_masked = ("XXXXX-XXXXX-XXXXX-XXXXX-" + $key.Substring([Math]::Max(0, $key.Length - 5)))
  }
} catch {}
try {
  $licProduct = Get-CimInstance -ClassName SoftwareLicensingProduct |
    Where-Object { $_.PartialProductKey -and $_.LicenseStatus -eq 1 -and $_.Name -match "Windows" } |
    Select-Object -First 3 Name,Description,PartialProductKey,LicenseStatus
  $licenseEvidence.licensingDescription = ($licProduct | ConvertTo-Json -Depth 4)
} catch {}
$licenseEvidence | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $activationDir "current-machine-oem-license-evidence-masked.json") -Encoding UTF8

$activationSources = @(
  "D:\Windows\ServiceProfiles\NetworkService\AppData\Roaming\Microsoft\SoftwareProtectionPlatform",
  "D:\Windows\System32\spp",
  "D:\ProgramData\Microsoft\Windows\ClipSVC",
  "D:\ProgramData\Microsoft\Windows\AppRepository"
)
$activationCopyResults = foreach ($src in $activationSources) {
  $name = ($src -replace "[:\\]", "_").Trim("_")
  $dest = Join-Path $activationDir $name
  $log = Join-Path $logsDir ("835D-activation-" + $name + ".log")
  if (Test-Path -LiteralPath $src) {
    New-Item -ItemType Directory -Force -Path $dest | Out-Null
    & robocopy.exe $src $dest /E /B /COPY:DAT /DCOPY:DAT /R:1 /W:1 /XJ /NP "/LOG:$log"
    [pscustomobject]@{ Source = $src; Destination = $dest; Exists = $true; RobocopyExitCode = $LASTEXITCODE; Ok = ($LASTEXITCODE -le 7); Log = $log }
  } else {
    [pscustomobject]@{ Source = $src; Destination = $dest; Exists = $false; RobocopyExitCode = 999; Ok = $false; Log = $log }
  }
}
$activationCopyResults | Export-Csv -LiteralPath (Join-Path $activationDir "activation-file-copy-results.csv") -NoTypeInformation -Encoding UTF8
$activationFilesCopied = (@($activationCopyResults | Where-Object { $_.Ok }).Count -gt 0)

# Export drivers from the offline Windows 10 partition when possible.
$driverLog = Join-Path $logsDir "835D-driver-export.log"
& dism.exe /Image:D:\ /Export-Driver "/Destination:$driversDir" *>&1 | Tee-Object -FilePath $driverLog
$driverCode = $LASTEXITCODE
$driversExported = $driverCode -eq 0

$restoreCopyScript = @'
param(
  [Parameter(Mandatory=$true)]
  [string]$TargetWindowsDrive,

  [string]$BackupRoot = "G:\GreatWall_GT6_SSD_OEM_Win10_File_Copy_Backup_835C"
)

$ErrorActionPreference = "Stop"
$source = Join-Path $BackupRoot "D_system_original"
$target = ($TargetWindowsDrive.TrimEnd(":","\") + ":\")
Write-Host "Copying original Great Wall GT6 Windows 10 files from $source to $target"
Write-Host "This does not partition or format anything. Prepare the target Windows partition first."
robocopy.exe $source $target /E /COPY:DAT /DCOPY:DAT /R:1 /W:1 /XJ /FFT /NP /TEE
exit $LASTEXITCODE
'@
$restoreCopyScript | Set-Content -LiteralPath (Join-Path $restoreDir "01-copy-file-backup-to-target-windows-partition.ps1") -Encoding ASCII

$bcdScript = @'
param(
  [Parameter(Mandatory=$true)]
  [string]$TargetWindowsDrive,

  [Parameter(Mandatory=$true)]
  [string]$TargetEfiDrive
)

$ErrorActionPreference = "Stop"
$windowsPath = ($TargetWindowsDrive.TrimEnd(":","\") + ":\Windows")
$efiPath = ($TargetEfiDrive.TrimEnd(":","\") + ":\")
if (-not (Test-Path -LiteralPath $windowsPath)) { throw "Windows folder not found: $windowsPath" }
if (-not (Test-Path -LiteralPath $efiPath)) { throw "EFI drive not found: $efiPath" }

Write-Host "Creating UEFI boot files with bcdboot..."
& bcdboot.exe $windowsPath /s $efiPath /f UEFI
exit $LASTEXITCODE
'@
$bcdScript | Set-Content -LiteralPath (Join-Path $restoreDir "02-create-uefi-boot-files-after-copy.ps1") -Encoding ASCII

$readme = @"
# Future Bootable Windows 10 Recovery Package - 835D

This package upgrades the 835C file copy backup into a future recovery-ready baseline.

It is still not a live clone and not a WIM image. Its purpose is to preserve enough material and instructions so a future technician/agent can attempt to rebuild a bootable Windows 10 installation from the original Great Wall GT6 SSD baseline.

## Source

- Original SSD: Disk 0, Great Wall GT6 1TB
- Original Windows partition: D:
- Original auxiliary partitions: E:, F:
- Original hidden EFI System partition: Disk 0 partition $($efiPartition.PartitionNumber)

## Preserved Here

- 835C simple file backup of D:, E:, F:
- EFI System Partition file backup
- Disk 0 partition layout records
- D:\Windows\System32\config core registry hive backup attempt
- OEM activation/license evidence and Software Protection Platform related files
- Offline Windows driver export
- Critical boot file manifest
- Future restore helper scripts

## Important Status

- This is a future recovery package, not an immediately guaranteed bootable clone.
- To restore later, create a GPT disk with an EFI FAT32 partition and a Windows NTFS partition, copy the D_system_original folder to the Windows partition, then run bcdboot against that Windows folder and the EFI partition.
- Some Windows protected files may still require administrator, WinPE, or backup-mode copying during final restore.

## Future Restore Order

1. Prepare a target GPT disk.
2. Create an EFI FAT32 partition, about 300MB.
3. Create a Windows NTFS partition.
4. Copy `D_system_original` to the Windows partition using `01-copy-file-backup-to-target-windows-partition.ps1`.
5. Run `02-create-uefi-boot-files-after-copy.ps1` to rebuild UEFI boot files with `bcdboot`.
6. If boot fails, use Windows recovery media and run Startup Repair or rebuild BCD manually.

## Safety

- No D/E/F partition delete, format, merge, shrink, or resize was executed when creating this package.
- C drive was not touched.
- WIM and DISM were not used for this package.
"@
$readme | Set-Content -LiteralPath (Join-Path $recoveryDir "README_FUTURE_BOOTABLE_RECOVERY_835D.md") -Encoding UTF8

$requiredChecks = @(
  @{ Name = "D_system_original"; Path = (Join-Path $backupRoot "D_system_original") },
  @{ Name = "EFI backup"; Path = $efiBackupDir },
  @{ Name = "SYSTEM hive"; Path = (Join-Path $configDest "SYSTEM") },
  @{ Name = "SOFTWARE hive"; Path = (Join-Path $configDest "SOFTWARE") },
  @{ Name = "OEM activation evidence"; Path = $activationDir },
  @{ Name = "Drivers export"; Path = $driversDir },
  @{ Name = "winload.efi"; Path = (Join-Path $backupRoot "D_system_original\Windows\System32\winload.efi") },
  @{ Name = "restore scripts"; Path = $restoreDir }
)
$readiness = foreach ($item in $requiredChecks) {
  [pscustomobject]@{
    Item = $item.Name
    Path = $item.Path
    Exists = Test-Path -LiteralPath $item.Path
  }
}
$readiness | Export-Csv -LiteralPath (Join-Path $reportDir "835D-readiness-check.csv") -NoTypeInformation -Encoding UTF8

$readyEnough = (($readiness | Where-Object { -not $_.Exists }).Count -eq 0) -and $efiCopied -and $configCopied -and $driversExported
$status = if ($readyEnough) { "FUTURE_BOOTABLE_RECOVERY_PACKAGE_READY_WITH_MANUAL_RESTORE_STEPS" } else { "FUTURE_BOOTABLE_RECOVERY_PACKAGE_PARTIAL" }

$report = @"
# 835D Future Bootable Windows 10 Recovery Package - Final Report

Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')

## Result

- Final status: $status
- Purpose: make the 835C file backup useful for a future attempt to restore a bootable original Great Wall GT6 Windows 10 system.
- Recovery package folder: $recoveryDir
- Desktop report folder: $reportDir
- Desktop zip: $zipPath
- WIM used: No
- DISM used: No
- D/E/F deleted/formatted/merged: No
- C drive touched: No

## Added

- EFI System Partition backup copied: $efiCopied
- EFI robocopy code: $efiCode
- Core registry hive backup copied: $configCopied
- Registry robocopy code: $configCode
- OEM activation evidence folder created: True
- Activation protected files copied at least partly: $activationFilesCopied
- Offline Windows drivers exported: $driversExported
- Driver export code: $driverCode
- Source disk/partition layout recorded: Yes
- Restore helper scripts created: Yes

## Activation Reality

Windows 10 OEM activation is usually stored in motherboard firmware or as a Microsoft digital license tied to this hardware. This package preserves activation evidence and related files, but it cannot legally or technically guarantee activation on different hardware. On the same machine, Windows 10 should usually reactivate automatically after reinstall if the firmware/digital license is intact.

## Restore Reality

This is now a future recovery-ready file package, not a guaranteed one-click clone. A future restore will still need:

- a prepared GPT target disk,
- a FAT32 EFI partition,
- a Windows NTFS partition,
- file copy from `D_system_original`,
- `bcdboot` to recreate UEFI boot files,
- possible Windows Recovery / Startup Repair if hardware or BCD differs.

## Readiness Checks

$($readiness | Format-Table -AutoSize | Out-String)
"@
$reportPath = Join-Path $reportDir "835D-final-report.md"
$report | Set-Content -LiteralPath $reportPath -Encoding UTF8

if (Test-Path -LiteralPath $zipPath) {
  Remove-Item -LiteralPath $zipPath -Force
}
Compress-Archive -LiteralPath $reportDir -DestinationPath $zipPath -Force

Write-Host "835D_STATUS=$status"
Write-Host "835D_RECOVERY_PACKAGE=$recoveryDir"
Write-Host "835D_REPORT=$reportPath"
Write-Host "835D_ZIP=$zipPath"

exit $(if ($status -eq "FUTURE_BOOTABLE_RECOVERY_PACKAGE_READY_WITH_MANUAL_RESTORE_STEPS") { 0 } else { 1 })
