[CmdletBinding(SupportsShouldProcess=$true)]
param(
    [string]$BackupRoot = "H:\Codex_Reinstall_Skill_Backup_20260611",
    [string]$CodexSkills = "$env:USERPROFILE\.codex\skills",
    [string]$AgentsRoot = "$env:USERPROFILE\.agents",
    [string]$CurrentBackupRoot = ("K:\AI\backups\skills_backups\current-codex-agents-before-restore_{0}" -f (Get-Date -Format "yyyyMMdd_HHmmss")),
    [string]$ReportPath = "$env:USERPROFILE\Desktop\1\output\codex-skill-restore-non-conflict-report.md",
    [switch]$CValidated,
    [switch]$UserApprovedBackup
)

Write-Warning "This restore script copies only missing Codex skills. Run it only after the user has confirmed restore. It never overwrites same-name skills and always skips .system."
if (-not $CValidated -or -not $UserApprovedBackup) {
    throw "BACKUP_NOT_AUTHORIZED: require -CValidated and -UserApprovedBackup before preserving current C state to K."
}
if (-not ([System.IO.Path]::GetFullPath($CurrentBackupRoot).StartsWith('K:\', [System.StringComparison]::OrdinalIgnoreCase))) {
    throw "BACKUP_TARGET_FORBIDDEN: current-state backup destination must be on K:."
}
$time = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$source = Join-Path $BackupRoot "codex-skills"
$copied = New-Object System.Collections.Generic.List[string]
$skipped = New-Object System.Collections.Generic.List[string]
$failed = New-Object System.Collections.Generic.List[string]

function Count-Dirs([string]$Path) {
    if (-not (Test-Path -LiteralPath $Path)) { return 0 }
    return @(Get-ChildItem -LiteralPath $Path -Directory -Force -ErrorAction SilentlyContinue).Count
}

New-Item -ItemType Directory -Force -Path (Split-Path -Parent $ReportPath) | Out-Null
if (-not (Test-Path -LiteralPath $source)) {
    throw "Backup codex skills not found: $source"
}
New-Item -ItemType Directory -Force -Path $CodexSkills | Out-Null
New-Item -ItemType Directory -Force -Path $CurrentBackupRoot | Out-Null

$codexRoot = Join-Path $env:USERPROFILE ".codex"
if (Test-Path -LiteralPath $codexRoot) {
    Copy-Item -LiteralPath $codexRoot -Destination (Join-Path $CurrentBackupRoot ".codex") -Recurse -Force -ErrorAction Continue
}
if (Test-Path -LiteralPath $AgentsRoot) {
    Copy-Item -LiteralPath $AgentsRoot -Destination (Join-Path $CurrentBackupRoot ".agents") -Recurse -Force -ErrorAction Continue
}

foreach ($skill in Get-ChildItem -LiteralPath $source -Directory -Force) {
    if ($skill.Name -eq ".system") {
        $skipped.Add(".system skipped")
        continue
    }
    $target = Join-Path $CodexSkills $skill.Name
    if (Test-Path -LiteralPath $target) {
        $skipped.Add("$($skill.Name) exists")
        continue
    }
    try {
        if ($PSCmdlet.ShouldProcess($target, "Copy missing skill $($skill.Name)")) {
            Copy-Item -LiteralPath $skill.FullName -Destination $target -Recurse -Force -ErrorAction Stop
            $copied.Add($skill.Name)
        }
    } catch {
        $failed.Add("$($skill.Name): $($_.Exception.Message)")
    }
}

$report = @"
# Codex Non-Conflict Skill Restore Report

- Time: $time
- Source: $source
- Target: $CodexSkills
- Current-state backup: $CurrentBackupRoot
- Final Codex skill count: $(Count-Dirs $CodexSkills)

## Copied

$($copied | ForEach-Object { "- $_" } | Out-String)

## Skipped

$($skipped | ForEach-Object { "- $_" } | Out-String)

## Failed

$($failed | ForEach-Object { "- $_" } | Out-String)

## Safety

Same-name targets were not overwritten. `.system` was skipped. Agents skills were not overwritten.
"@
$report | Set-Content -LiteralPath $ReportPath -Encoding UTF8
Write-Host "Restore report: $ReportPath"
