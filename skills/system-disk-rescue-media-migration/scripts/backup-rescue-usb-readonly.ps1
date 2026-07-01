param(
    [int]$DiskNumber = 4,
    [string]$DriveLetter = 'D',
    [string]$ExpectedModelRegex = 'Kingston DataTraveler 3\.0',
    [string]$ExpectedLabel = 'VEEAMRE',
    [string]$ExpectedFileSystem = 'FAT32',
    [string[]]$BackupBaseCandidates = @('G:\USB_Backups','K:\USB_Backups','J:\USB_Backups','I:\USB_Backups','H:\USB_Backups',"$env:USERPROFILE\Desktop")
)

$ErrorActionPreference = 'Stop'

function Add-Log {
    param([string]$Text)
    $Text | Tee-Object -FilePath $script:Report -Append
}

function Add-Section {
    param([string]$Text)
    Add-Log ''
    Add-Log "===== $Text ====="
}

function Fail {
    param([string]$Message)
    Add-Log "STOP=$Message"
    Add-Log 'RESULT=STOPPED'
    Add-Log 'NO_WRITE_ACTION_PERFORMED_TO_USB=TRUE'
    Write-Host "REPORT=$script:Report"
    exit 1
}

$DriveLetter = $DriveLetter.TrimEnd(':')
$root = "$DriveLetter`:\"
$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'

$disk = Get-Disk -Number $DiskNumber -ErrorAction Stop
$vol = Get-Volume -DriveLetter $DriveLetter -ErrorAction Stop

$sourceFiles = @(Get-ChildItem -LiteralPath $root -Force -Recurse -File -ErrorAction SilentlyContinue)
$usedBytes = ($sourceFiles | Measure-Object Length -Sum).Sum
if (-not $usedBytes) { $usedBytes = 0 }
$neededBytes = [math]::Max([double]$usedBytes * 1.25, 5GB)

$backupBase = $null
foreach ($candidate in $BackupBaseCandidates) {
    $qualifier = Split-Path $candidate -Qualifier
    if (-not $qualifier) { continue }
    if (-not (Test-Path -LiteralPath $qualifier)) { continue }
    $letter = $qualifier.TrimEnd(':')
    $targetVol = Get-Volume -DriveLetter $letter -ErrorAction SilentlyContinue
    if ($targetVol -and $targetVol.DriveType -ne 'Removable' -and $targetVol.SizeRemaining -gt $neededBytes) {
        $backupBase = $candidate
        break
    }
}

if (-not $backupBase) {
    throw "No non-removable backup destination has enough space. Needed bytes: $neededBytes"
}

$backupRoot = Join-Path $backupBase "VEEAMRE_Kingston_838B\backup_$stamp"
$filesDir = Join-Path $backupRoot 'D_root_files'
$reportDir = Join-Path $backupRoot 'reports'
New-Item -ItemType Directory -Path $filesDir -Force | Out-Null
New-Item -ItemType Directory -Path $reportDir -Force | Out-Null
$script:Report = Join-Path $reportDir 'BACKUP_REPORT.txt'

Add-Log '===== Rescue USB ReadOnly Backup ====='
Add-Log "Time=$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
Add-Log 'Mode=BACKUP_AND_VERIFY_ONLY'
Add-Log "BackupRoot=$backupRoot"

Add-Section 'Target Gate'
$disk | Format-List Number,FriendlyName,SerialNumber,BusType,MediaType,PartitionStyle,Size,OperationalStatus,HealthStatus,IsBoot,IsSystem,IsReadOnly,IsOffline | Out-String | Tee-Object -FilePath $script:Report -Append
$vol | Format-List DriveLetter,FileSystemLabel,FileSystem,DriveType,HealthStatus,SizeRemaining,Size | Out-String | Tee-Object -FilePath $script:Report -Append
Get-Partition -DiskNumber $DiskNumber | Sort-Object PartitionNumber | Format-Table DiskNumber,PartitionNumber,DriveLetter,Type,GptType,Size,Offset -AutoSize | Out-String | Tee-Object -FilePath $script:Report -Append

if ($disk.BusType -ne 'USB') { Fail "Disk $DiskNumber is not USB." }
if ($disk.IsBoot -or $disk.IsSystem) { Fail "Disk $DiskNumber is boot/system." }
if ($ExpectedModelRegex -and $disk.FriendlyName -notmatch $ExpectedModelRegex) { Fail "Disk model mismatch: $($disk.FriendlyName)" }
if ($ExpectedLabel -and $vol.FileSystemLabel -ne $ExpectedLabel) { Fail "Volume label mismatch: $($vol.FileSystemLabel)" }
if ($ExpectedFileSystem -and $vol.FileSystem -ne $ExpectedFileSystem) { Fail "Filesystem mismatch: $($vol.FileSystem)" }

Add-Log 'TARGET_GATE=PASS'

Add-Section 'Reports'
Get-Disk | Sort-Object Number | Format-List Number,FriendlyName,SerialNumber,BusType,MediaType,PartitionStyle,Size,OperationalStatus,HealthStatus,IsBoot,IsSystem,IsReadOnly,IsOffline | Out-String | Set-Content -LiteralPath (Join-Path $reportDir 'ALL_DISKS.txt') -Encoding UTF8
Get-Partition | Sort-Object DiskNumber,PartitionNumber | Format-Table DiskNumber,PartitionNumber,DriveLetter,Type,GptType,Size,Offset -AutoSize | Out-String | Set-Content -LiteralPath (Join-Path $reportDir 'ALL_PARTITIONS.txt') -Encoding UTF8
Get-Volume | Sort-Object DriveLetter | Format-Table DriveLetter,FileSystemLabel,FileSystem,DriveType,HealthStatus,SizeRemaining,Size -AutoSize | Out-String | Set-Content -LiteralPath (Join-Path $reportDir 'ALL_VOLUMES.txt') -Encoding UTF8
Get-ChildItem -LiteralPath $root -Force | Select-Object Mode,Length,LastWriteTime,Name | Format-Table -AutoSize | Out-String | Set-Content -LiteralPath (Join-Path $reportDir 'ROOT_LISTING.txt') -Encoding UTF8
Get-ChildItem -LiteralPath $root -Force -Recurse -ErrorAction SilentlyContinue | Select-Object FullName,Length,LastWriteTime,Attributes | Sort-Object FullName | Format-Table -AutoSize | Out-String -Width 4096 | Set-Content -LiteralPath (Join-Path $reportDir 'FULL_TREE.txt') -Encoding UTF8
Add-Log 'REPORTS_WRITTEN=TRUE'

Add-Section 'Robocopy'
$roboLog = Join-Path $reportDir 'ROBOCOPY_LOG.txt'
& robocopy $root $filesDir /E /COPY:DAT /DCOPY:DAT /XJ /R:1 /W:1 /FFT /TEE /LOG:$roboLog
$rc = $LASTEXITCODE
Add-Log "ROBOCOPY_EXIT_CODE=$rc"
if ($rc -ge 8) { Fail "Robocopy failed with exit code $rc" }

Add-Section 'Manifests And Hashes'
$srcFiles = @(Get-ChildItem -LiteralPath $root -Force -Recurse -File -ErrorAction SilentlyContinue | Sort-Object FullName)
$dstFiles = @(Get-ChildItem -LiteralPath $filesDir -Force -Recurse -File -ErrorAction SilentlyContinue | Sort-Object FullName)
$srcFiles | Select-Object @{n='RelativePath';e={$_.FullName.Substring(3)}},FullName,Length,LastWriteTime,Attributes | Export-Csv -LiteralPath (Join-Path $reportDir 'SOURCE_FILE_MANIFEST.csv') -NoTypeInformation -Encoding UTF8
$dstFiles | Select-Object @{n='RelativePath';e={$_.FullName.Substring($filesDir.Length).TrimStart('\')}},FullName,Length,LastWriteTime,Attributes | Export-Csv -LiteralPath (Join-Path $reportDir 'BACKUP_FILE_MANIFEST.csv') -NoTypeInformation -Encoding UTF8

$srcHashRows = foreach ($f in $srcFiles) {
    $h = Get-FileHash -LiteralPath $f.FullName -Algorithm SHA256
    [pscustomobject]@{RelativePath=$f.FullName.Substring(3); SHA256=$h.Hash; Length=$f.Length; FullName=$f.FullName}
}
$dstHashRows = foreach ($f in $dstFiles) {
    $h = Get-FileHash -LiteralPath $f.FullName -Algorithm SHA256
    [pscustomobject]@{RelativePath=$f.FullName.Substring($filesDir.Length).TrimStart('\'); SHA256=$h.Hash; Length=$f.Length; FullName=$f.FullName}
}
$srcHashRows | Export-Csv -LiteralPath (Join-Path $reportDir 'SOURCE_SHA256.csv') -NoTypeInformation -Encoding UTF8
$dstHashRows | Export-Csv -LiteralPath (Join-Path $reportDir 'BACKUP_SHA256.csv') -NoTypeInformation -Encoding UTF8

$dstMap = @{}
foreach ($r in $dstHashRows) { $dstMap[$r.RelativePath.ToLowerInvariant()] = $r }
$verifyRows = foreach ($s in $srcHashRows) {
    $key = $s.RelativePath.ToLowerInvariant()
    if ($dstMap.ContainsKey($key)) {
        $d = $dstMap[$key]
        [pscustomobject]@{RelativePath=$s.RelativePath; SourceLength=$s.Length; BackupLength=$d.Length; SourceSHA256=$s.SHA256; BackupSHA256=$d.SHA256; Match=(($s.Length -eq $d.Length) -and ($s.SHA256 -eq $d.SHA256)); Status='Compared'}
    } else {
        [pscustomobject]@{RelativePath=$s.RelativePath; SourceLength=$s.Length; BackupLength=$null; SourceSHA256=$s.SHA256; BackupSHA256=$null; Match=$false; Status='MissingInBackup'}
    }
}
$verifyRows | Export-Csv -LiteralPath (Join-Path $reportDir 'HASH_VERIFY.csv') -NoTypeInformation -Encoding UTF8
$mismatches = @($verifyRows | Where-Object { -not $_.Match })

Add-Log "SOURCE_FILE_COUNT=$($srcFiles.Count)"
Add-Log "BACKUP_FILE_COUNT=$($dstFiles.Count)"
Add-Log "HASH_COMPARED_COUNT=$($verifyRows.Count)"
Add-Log "HASH_MISMATCH_COUNT=$($mismatches.Count)"

Add-Section 'Final Result'
Add-Log 'NO_WRITE_ACTION_PERFORMED_TO_USB=TRUE'
Add-Log 'NO_FORMAT_PERFORMED=TRUE'
Add-Log 'NO_PARTITION_CHANGE_PERFORMED=TRUE'
if ($mismatches.Count -eq 0 -and $srcFiles.Count -eq $dstFiles.Count) {
    Add-Log 'RESULT=BACKUP_AND_HASH_VERIFY_OK'
} else {
    Add-Log 'RESULT=BACKUP_VERIFY_NEEDS_REVIEW'
}
Add-Log "BACKUP_ROOT=$backupRoot"
Add-Log "REPORT=$script:Report"
Write-Host "REPORT=$script:Report"
