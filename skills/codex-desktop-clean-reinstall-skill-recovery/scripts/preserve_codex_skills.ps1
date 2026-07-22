[CmdletBinding(SupportsShouldProcess=$true)]
param(
    [string]$BackupRoot = ("K:\AI\backups\Codex_Reinstall_Skill_Backup_{0}" -f (Get-Date -Format "yyyyMMdd")),
    [string]$CodexSkills = "$env:USERPROFILE\.codex\skills",
    [string]$AgentsSkills = "$env:USERPROFILE\.agents\skills",
    [string]$ReportPath = "$env:USERPROFILE\Desktop\1\output\codex-desktop-reinstall-preservation-notes.md",
    [switch]$CValidated,
    [switch]$UserApprovedBackup
)

$ErrorActionPreference = "Continue"
$time = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$copyLog = Join-Path $BackupRoot "copy-log.tsv"
$indexPath = Join-Path $BackupRoot "codex-reinstall-machine-readable-index.md"
$notesPath = Join-Path $BackupRoot "codex-desktop-reinstall-preservation-notes.md"

function Get-SkillCount([string]$Path) {
    if (-not (Test-Path -LiteralPath $Path)) { return 0 }
    return @(Get-ChildItem -LiteralPath $Path -Directory -Force -ErrorAction SilentlyContinue).Count
}

function Copy-SkillTree([string]$Source, [string]$Target, [string]$Label) {
    if (-not (Test-Path -LiteralPath $Source)) {
        Add-Content -LiteralPath $copyLog -Value "$Label`tMISSING_SOURCE`t$Source`t$Target`t0"
        return
    }
    if ($PSCmdlet.ShouldProcess($Target, "Copy $Label skills from $Source")) {
        New-Item -ItemType Directory -Force -Path $Target | Out-Null
        Copy-Item -LiteralPath (Join-Path $Source "*") -Destination $Target -Recurse -Force -ErrorAction Continue
        Add-Content -LiteralPath $copyLog -Value "$Label`tCOPIED`t$Source`t$Target`t$(Get-SkillCount $Target)"
    }
}

if (-not $CValidated -or -not $UserApprovedBackup) {
    throw "BACKUP_NOT_AUTHORIZED: require -CValidated and -UserApprovedBackup for this exact C-to-K backup."
}
if (-not ([System.IO.Path]::GetFullPath($BackupRoot).StartsWith('K:\', [System.StringComparison]::OrdinalIgnoreCase))) {
    throw "BACKUP_TARGET_FORBIDDEN: backup destination must be on K:."
}
if (-not (Test-Path -LiteralPath $CodexSkills -PathType Container)) {
    throw "BLOCKED_C_SOURCE_MISSING: $CodexSkills"
}

New-Item -ItemType Directory -Force -Path $BackupRoot | Out-Null
New-Item -ItemType Directory -Force -Path (Split-Path -Parent $ReportPath) | Out-Null
"label`tstatus`tsource`ttarget`tcount" | Set-Content -LiteralPath $copyLog -Encoding UTF8

$codexTarget = Join-Path $BackupRoot "codex-skills"
$agentsTarget = Join-Path $BackupRoot "agents-skills"
Copy-SkillTree -Source $CodexSkills -Target $codexTarget -Label "codex-skills"
Copy-SkillTree -Source $AgentsSkills -Target $agentsTarget -Label "agents-skills"

$codexSourceCount = Get-SkillCount $CodexSkills
$agentsSourceCount = Get-SkillCount $AgentsSkills
$codexBackupCount = Get-SkillCount $codexTarget
$agentsBackupCount = Get-SkillCount $agentsTarget

$sensitive = @(
    "$env:USERPROFILE\.codex\config.toml",
    "$env:USERPROFILE\.codex\auth.json",
    "$env:USERPROFILE\.codex\sessions",
    "$env:USERPROFILE\.codex\session_index.jsonl"
)

$sensitiveLines = foreach ($path in $sensitive) {
    "- $path : $(Test-Path -LiteralPath $path)"
}

$index = @"
# Codex Reinstall Machine-Readable Index

- created_at: $time
- backup_root: $BackupRoot
- codex_source: $CodexSkills
- codex_source_count: $codexSourceCount
- codex_backup_count: $codexBackupCount
- agents_source: $AgentsSkills
- agents_source_count: $agentsSourceCount
- agents_backup_count: $agentsBackupCount
- copy_log: $copyLog
"@
$index | Set-Content -LiteralPath $indexPath -Encoding UTF8

$report = @"
# Codex Desktop Reinstall Preservation Notes

- Time: $time
- Stage: preserve-before-uninstall
- Backup root: $BackupRoot
- Codex source count: $codexSourceCount
- Codex backup count: $codexBackupCount
- Agents source count: $agentsSourceCount
- Agents backup count: $agentsBackupCount
- Copy log: $copyLog
- Machine-readable index: $indexPath

## Sensitive State Presence Only

$($sensitiveLines -join "`r`n")

## Safety

No deletion was performed. Sensitive files were not copied by this script.
"@
$report | Set-Content -LiteralPath $notesPath -Encoding UTF8
$report | Set-Content -LiteralPath $ReportPath -Encoding UTF8
Write-Host "Preservation report: $ReportPath"
