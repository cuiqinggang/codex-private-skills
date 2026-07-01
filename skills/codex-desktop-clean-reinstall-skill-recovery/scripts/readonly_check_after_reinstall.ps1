[CmdletBinding()]
param(
    [string]$BackupRoot = "H:\Codex_Reinstall_Skill_Backup_20260611",
    [string]$CodexSkills = "$env:USERPROFILE\.codex\skills",
    [string]$AgentsSkills = "$env:USERPROFILE\.agents\skills",
    [string]$ReportPath = "$env:USERPROFILE\Desktop\1\output\codex-official-reinstall-recovery-check-report.md"
)

$time = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
function Count-Dirs([string]$Path) {
    if (-not (Test-Path -LiteralPath $Path)) { return 0 }
    return @(Get-ChildItem -LiteralPath $Path -Directory -Force -ErrorAction SilentlyContinue).Count
}
function Names([string]$Path) {
    if (-not (Test-Path -LiteralPath $Path)) { return @() }
    return @(Get-ChildItem -LiteralPath $Path -Directory -Force -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Name)
}

$backupCodex = Join-Path $BackupRoot "codex-skills"
$backupAgents = Join-Path $BackupRoot "agents-skills"
$backupCodexNames = Names $backupCodex
$currentCodexNames = Names $CodexSkills
$conflicts = @($backupCodexNames | Where-Object { $currentCodexNames -contains $_ })
$candidates = @($backupCodexNames | Where-Object { $currentCodexNames -notcontains $_ -and $_ -ne ".system" })

$residuePaths = @(
    "$env:LOCALAPPDATA\Programs\Codex++",
    "$env:LOCALAPPDATA\CodexPlusPlus",
    "$env:APPDATA\CodexPlusPlus"
)
$residueLines = foreach ($path in $residuePaths) { "- $path : $(Test-Path -LiteralPath $path)" }

New-Item -ItemType Directory -Force -Path (Split-Path -Parent $ReportPath) | Out-Null
$report = @"
# Codex Official Reinstall Recovery Check Report

- Time: $time
- Stage: post-reinstall-readonly-check
- Backup root: $BackupRoot
- Backup root exists: $(Test-Path -LiteralPath $BackupRoot)
- Backup codex skills count: $(Count-Dirs $backupCodex)
- Backup agents skills count: $(Count-Dirs $backupAgents)
- Current codex skills count: $(Count-Dirs $CodexSkills)
- Current agents skills count: $(Count-Dirs $AgentsSkills)
- Current `.system` exists: $(Test-Path -LiteralPath (Join-Path $CodexSkills ".system"))
- Agents `learned` exists: $(Test-Path -LiteralPath (Join-Path $AgentsSkills "learned"))

## Non-Conflicting Codex Restore Candidates

$($candidates | ForEach-Object { "- $_" } | Out-String)

## Same-Name Conflicts

$($conflicts | ForEach-Object { "- $_" } | Out-String)

## Codex++ Residue Path Check

$($residueLines -join "`r`n")

## Safety

Read-only check only. No delete, copy, overwrite, move, registry, Store, proxy, or account changes were made.
"@
$report | Set-Content -LiteralPath $ReportPath -Encoding UTF8
Write-Host "Read-only report: $ReportPath"
