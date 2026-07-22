param(
    [int]$DiskNumber,
    [string]$DriveLetter,
    [string]$ExpectedModelRegex = '',
    [string]$ExpectedLabel = '',
    [string]$OutputRoot = "$env:USERPROFILE\Desktop"
)

$ErrorActionPreference = 'Stop'

function Stop-WithReport {
    param([string]$Message)
    Add-Log $Message
    Add-Log 'RESULT=STOPPED'
    Add-Log 'NO_WRITE_ACTION_PERFORMED_TO_USB=TRUE'
    Write-Host "REPORT=$script:Report"
    exit 1
}

function Add-Log {
    param([string]$Text)
    $Text | Tee-Object -FilePath $script:Report -Append
}

function Add-Section {
    param([string]$Text)
    Add-Log ''
    Add-Log "===== $Text ====="
}

if (-not $DriveLetter) {
    throw 'DriveLetter is required, e.g. D'
}

$DriveLetter = $DriveLetter.TrimEnd(':')
$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$outDir = Join-Path $OutputRoot "rescue_usb_readonly_inspect_$stamp"
New-Item -ItemType Directory -Path $outDir -Force | Out-Null
$script:Report = Join-Path $outDir 'INSPECT_REPORT.txt'

Add-Log '===== Rescue USB ReadOnly Inspect ====='
Add-Log "Time=$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
Add-Log 'Mode=READ_ONLY'

$disk = Get-Disk -Number $DiskNumber -ErrorAction Stop
$vol = Get-Volume -DriveLetter $DriveLetter -ErrorAction Stop
$parts = @(Get-Partition -DiskNumber $DiskNumber -ErrorAction Stop | Sort-Object PartitionNumber)

Add-Section 'Target Gate'
$disk | Format-List Number,FriendlyName,SerialNumber,BusType,MediaType,PartitionStyle,Size,OperationalStatus,HealthStatus,IsBoot,IsSystem,IsReadOnly,IsOffline | Out-String | Tee-Object -FilePath $script:Report -Append
$vol | Format-List DriveLetter,FileSystemLabel,FileSystem,DriveType,HealthStatus,SizeRemaining,Size | Out-String | Tee-Object -FilePath $script:Report -Append
$parts | Format-Table DiskNumber,PartitionNumber,DriveLetter,Type,GptType,Size,Offset -AutoSize | Out-String | Tee-Object -FilePath $script:Report -Append

if ($disk.BusType -ne 'USB') { Stop-WithReport "Target Disk $DiskNumber is not USB." }
if ($disk.IsBoot -or $disk.IsSystem) { Stop-WithReport "Target Disk $DiskNumber is boot/system." }
if ($ExpectedModelRegex -and $disk.FriendlyName -notmatch $ExpectedModelRegex) { Stop-WithReport "Target model mismatch: $($disk.FriendlyName)" }
if ($ExpectedLabel -and $vol.FileSystemLabel -ne $ExpectedLabel) { Stop-WithReport "Target label mismatch: $($vol.FileSystemLabel)" }

Add-Log 'TARGET_GATE=PASS'

Add-Section 'Root Listing And Boot Markers'
$root = "$DriveLetter`:\"
Get-ChildItem -LiteralPath $root -Force -ErrorAction Stop |
    Select-Object Mode,Length,LastWriteTime,Name |
    Format-Table -AutoSize |
    Out-String |
    Tee-Object -FilePath $script:Report -Append

$markers = @(
    'EFI',
    'EFI\Boot\bootx64.efi',
    'EFI\Microsoft\Boot\BCD',
    'boot',
    'boot\BCD',
    'bootmgr',
    'bootmgr.efi',
    'sources',
    'sources\boot.wim',
    'BMRAnswerFile.xml',
    'Macrium',
    'Drivers'
)

foreach ($marker in $markers) {
    $path = Join-Path $root $marker
    if (Test-Path -LiteralPath $path) {
        Add-Log "FOUND: $path"
    } else {
        Add-Log "MISS : $path"
    }
}

Add-Section 'Safety Confirmation'
Add-Log 'NO_WRITE_ACTION_PERFORMED_TO_USB=TRUE'
Add-Log 'NO_FORMAT_PERFORMED=TRUE'
Add-Log 'NO_PARTITION_CHANGE_PERFORMED=TRUE'
Add-Log 'RESULT=READONLY_INSPECT_DONE'
Add-Log "REPORT=$script:Report"
Write-Host "REPORT=$script:Report"
