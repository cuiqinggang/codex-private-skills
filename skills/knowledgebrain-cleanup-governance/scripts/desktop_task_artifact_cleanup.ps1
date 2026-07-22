[CmdletBinding()]
param(
    [string]$DesktopPath = "$env:USERPROFILE\Desktop",
    [datetime]$Since = [datetime]::Today,
    [string]$RunLabel = ("desktop-cleanup-" + (Get-Date -Format 'yyyyMMdd-HHmmss')),
    [string]$ArchiveRoot = 'K:\AI\_COLD_ARCHIVE',
    [Parameter(Mandatory = $true)]
    [string]$ManifestPath,
    [string]$NameRegex = '^(step|s\d|test_|nodpi|cursor|box|verify|click|light|find_|full_|wide_|zoom_|btn_|douyin_|pixel_|fine_|check_|paste_|ocr_|shot|screenshot_|prepare_|super_)',
    [string[]]$Extensions = @('.png', '.py'),
    [switch]$Execute
)

$ErrorActionPreference = 'Stop'

function Quote-LiteralPath([string]$Path) {
    return "'" + $Path.Replace("'", "''") + "'"
}

$desktopResolved = (Resolve-Path -LiteralPath $DesktopPath).Path
$manifestFullPath = [System.IO.Path]::GetFullPath($ManifestPath)

if (-not $Execute) {
    $targetDirectory = Join-Path (Join-Path $ArchiveRoot $RunLabel) 'task-artifacts'
    $candidates = Get-ChildItem -LiteralPath $desktopResolved -File -Force |
        Where-Object {
            $_.LastWriteTime -ge $Since -and
            $_.Extension.ToLowerInvariant() -in $Extensions -and
            $_.Name -match $NameRegex -and
            -not ($_.Attributes -band [IO.FileAttributes]::ReparsePoint)
        } |
        Sort-Object Name

    $rows = foreach ($item in $candidates) {
        $target = Join-Path $targetDirectory $item.Name
        [pscustomobject]@{
            move_id          = [guid]::NewGuid().ToString('N')
            classification   = 'COLD_ARCHIVE_TASK_ARTIFACT'
            source_path      = $item.FullName
            target_path      = $target
            bytes            = $item.Length
            file_count       = 1
            latest_write_time= $item.LastWriteTime.ToString('o')
            reason           = 'Finished-task screenshot/check/grid or one-off helper; durable result verified elsewhere.'
            status           = 'PLANNED'
            rollback_command = "Move-Item -LiteralPath $(Quote-LiteralPath $target) -Destination $(Quote-LiteralPath $item.FullName)"
        }
    }

    $manifestDirectory = Split-Path -Parent $manifestFullPath
    if ($manifestDirectory) { New-Item -ItemType Directory -Path $manifestDirectory -Force | Out-Null }
    $rows | Export-Csv -LiteralPath $manifestFullPath -NoTypeInformation -Encoding UTF8
    Write-Output "PLAN_MANIFEST=$manifestFullPath"
    Write-Output "PLANNED_COUNT=$($rows.Count)"
    Write-Output "PLANNED_BYTES=$(($rows | Measure-Object bytes -Sum).Sum)"
    exit 0
}

if (-not (Test-Path -LiteralPath $manifestFullPath -PathType Leaf)) {
    throw "Execute requires an existing reviewed manifest: $manifestFullPath"
}

$rows = @(Import-Csv -LiteralPath $manifestFullPath)
foreach ($row in $rows) {
    if ($row.status -ne 'PLANNED') { continue }
    if (-not (Test-Path -LiteralPath $row.source_path -PathType Leaf)) {
        $row.status = 'SKIPPED_NOT_FOUND'
        continue
    }
    if (Test-Path -LiteralPath $row.target_path) {
        $row.status = 'SKIPPED_TARGET_EXISTS'
        continue
    }
    $targetParent = Split-Path -Parent $row.target_path
    New-Item -ItemType Directory -Path $targetParent -Force | Out-Null
    try {
        Move-Item -LiteralPath $row.source_path -Destination $row.target_path
        if ((-not (Test-Path -LiteralPath $row.source_path)) -and (Test-Path -LiteralPath $row.target_path -PathType Leaf)) {
            $row.status = 'MOVED'
        } else {
            $row.status = 'ERROR_MOVE_FAILED'
        }
    } catch {
        $row.status = 'ERROR_MOVE_FAILED'
        $row.reason = $row.reason + ' Error: ' + $_.Exception.Message
    }
}

$rows | Export-Csv -LiteralPath $manifestFullPath -NoTypeInformation -Encoding UTF8
$groups = $rows | Group-Object status | Sort-Object Name
foreach ($group in $groups) {
    Write-Output ("STATUS_{0}={1}" -f $group.Name, $group.Count)
}
if ($rows.Where({ $_.status -eq 'ERROR_MOVE_FAILED' }).Count -gt 0) { exit 2 }
