param(
    [string]$BackupRoot = 'H:\Codex_Reinstall_Skill_Backup_20260611',
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
    [string]$ReportPath = '',
    [switch]$Restore
)

$ErrorActionPreference = 'Stop'

$timestamp = Get-Date -Format 'yyyyMMdd-HHmmss'
if ([string]::IsNullOrWhiteSpace($ReportPath)) {
    $mode = if ($Restore) { 'restore' } else { 'check' }
    $ReportPath = Join-Path $OutputRoot "codex-reinstall-skill-recovery-$mode-report-$timestamp.md"
}

$backupCodexSkills = Join-Path $BackupRoot 'codex-skills'
$backupAgentsSkills = Join-Path $BackupRoot 'agents-skills'
$machineIndex = Join-Path $BackupRoot 'codex-reinstall-machine-readable-index.md'
$notes = Join-Path $BackupRoot 'codex-desktop-reinstall-preservation-notes.md'
$copyLog = Join-Path $BackupRoot 'copy-log.tsv'

function Get-DirNames {
    param([string]$Path)
    if (-not (Test-Path -LiteralPath $Path -PathType Container)) {
        return @()
    }
    return @(Get-ChildItem -LiteralPath $Path -Directory -Force | Select-Object -ExpandProperty Name | Sort-Object)
}

function MdList {
    param($Items)
    $arr = @($Items)
    if ($arr.Count -eq 0) {
        return '- none'
    }
    return (($arr | ForEach-Object { "- $_" }) -join "`r`n")
}

function Add-Lines {
    param($Target, $Items)
    foreach ($item in @($Items)) {
        $Target.Add([string]$item)
    }
}

$pathChecks = @(
    $BackupRoot,
    $backupCodexSkills,
    $backupAgentsSkills,
    $machineIndex,
    $notes,
    $copyLog,
    $CurrentCodexSkills,
    $CurrentAgentsSkills,
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
)

$hCodex = Get-DirNames $backupCodexSkills
$hAgents = Get-DirNames $backupAgentsSkills
$cCodexBefore = Get-DirNames $CurrentCodexSkills
$cAgentsBefore = Get-DirNames $CurrentAgentsSkills

$codexConflicts = @($hCodex | Where-Object { $cCodexBefore -contains $_ } | Sort-Object)
$agentsConflicts = @($hAgents | Where-Object { $cAgentsBefore -contains $_ } | Sort-Object)
$codexDirect = @($hCodex | Where-Object { $cCodexBefore -notcontains $_ } | Sort-Object)
$agentsDirect = @($hAgents | Where-Object { $cAgentsBefore -notcontains $_ } | Sort-Object)
$codexCopied = New-Object System.Collections.Generic.List[string]
$agentsCopied = New-Object System.Collections.Generic.List[string]
$backupBeforeRestore = ''

if ($Restore) {
    $backupBeforeRestore = Join-Path $OutputRoot "codex-reinstall-pre-restore-backup-$timestamp"
    New-Item -ItemType Directory -Path $backupBeforeRestore -Force | Out-Null
    New-Item -ItemType Directory -Path (Join-Path $backupBeforeRestore '.codex') -Force | Out-Null
    New-Item -ItemType Directory -Path (Join-Path $backupBeforeRestore '.agents') -Force | Out-Null

    if (Test-Path -LiteralPath $CurrentCodexSkills -PathType Container) {
        Copy-Item -LiteralPath $CurrentCodexSkills -Destination (Join-Path $backupBeforeRestore '.codex') -Recurse -Force
    }
    if (Test-Path -LiteralPath $CurrentAgentsSkills -PathType Container) {
        Copy-Item -LiteralPath $CurrentAgentsSkills -Destination (Join-Path $backupBeforeRestore '.agents') -Recurse -Force
    }
${REDACTED_SECRET}
${REDACTED_SECRET}
    }
${REDACTED_SECRET}
${REDACTED_SECRET}
    }

    foreach ($name in $codexDirect) {
        $src = Join-Path $backupCodexSkills $name
        $dst = Join-Path $CurrentCodexSkills $name
        if (-not (Test-Path -LiteralPath $dst)) {
            Copy-Item -LiteralPath $src -Destination $dst -Recurse -Force
            $codexCopied.Add($name)
        }
    }

    foreach ($name in $agentsDirect) {
        $src = Join-Path $backupAgentsSkills $name
        $dst = Join-Path $CurrentAgentsSkills $name
        if (-not (Test-Path -LiteralPath $dst)) {
            Copy-Item -LiteralPath $src -Destination $dst -Recurse -Force
            $agentsCopied.Add($name)
        }
    }
}

$cCodexAfter = Get-DirNames $CurrentCodexSkills
$cAgentsAfter = Get-DirNames $CurrentAgentsSkills
$codexMissingAfter = @($hCodex | Where-Object { $cCodexAfter -notcontains $_ } | Sort-Object)
$agentsMissingAfter = @($hAgents | Where-Object { $cAgentsAfter -notcontains $_ } | Sort-Object)
$extraAgentsAfter = @($cAgentsAfter | Where-Object { $hAgents -notcontains $_ } | Sort-Object)

$report = New-Object System.Collections.Generic.List[string]
$report.Add('# Codex reinstall skill recovery report')
$report.Add('')
$report.Add("Generated at: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz')")
$report.Add("Mode: $(if ($Restore) { 'restore' } else { 'read-only check' })")
$report.Add('')
$report.Add('## Path status')
$report.Add('')
foreach ($path in $pathChecks) {
    $status = if (Test-Path -LiteralPath $path) { 'exists' } else { 'missing' }
    $report.Add("- $path : $status")
}
$report.Add('')
$report.Add('## Index status')
$report.Add('')
$report.Add("- Machine index read: $(Test-Path -LiteralPath $machineIndex -PathType Leaf)")
$report.Add("- Preservation notes read: $(Test-Path -LiteralPath $notes -PathType Leaf)")
$report.Add("- Copy log read: $(Test-Path -LiteralPath $copyLog -PathType Leaf)")
$report.Add('')
$report.Add('## Counts')
$report.Add('')
$report.Add("| Location | Before | After |")
$report.Add("| --- | ---: | ---: |")
$report.Add("| Backup Codex skills | $($hCodex.Count) | $($hCodex.Count) |")
$report.Add("| Current Codex skills | $($cCodexBefore.Count) | $($cCodexAfter.Count) |")
$report.Add("| Backup Agents skills | $($hAgents.Count) | $($hAgents.Count) |")
$report.Add("| Current Agents skills | $($cAgentsBefore.Count) | $($cAgentsAfter.Count) |")
$report.Add('')
$report.Add('## Conflicts and candidates')
$report.Add('')
$report.Add('Codex same-name conflicts:')
Add-Lines $report (MdList $codexConflicts)
$report.Add('')
$report.Add('Agents same-name conflicts:')
Add-Lines $report (MdList $agentsConflicts)
$report.Add('')
$report.Add('Codex non-conflicting restore candidates:')
Add-Lines $report (MdList $codexDirect)
$report.Add('')
$report.Add('Agents non-conflicting restore candidates:')
Add-Lines $report (MdList $agentsDirect)
$report.Add('')

if ($Restore) {
    $report.Add('## Restore actions')
    $report.Add('')
    $report.Add("- Backup-before-restore directory: $backupBeforeRestore")
    $report.Add("- Newly copied Codex skills: $($codexCopied.Count)")
    Add-Lines $report (MdList $codexCopied)
    $report.Add('')
    $report.Add("- Newly copied Agents skills: $($agentsCopied.Count)")
    Add-Lines $report (MdList $agentsCopied)
    $report.Add('')
}

$report.Add('## Final verification')
$report.Add('')
$report.Add("- Codex backup skills missing in current after operation: $($codexMissingAfter.Count)")
Add-Lines $report (MdList $codexMissingAfter)
$report.Add('')
$report.Add("- Agents backup skills missing in current after operation: $($agentsMissingAfter.Count)")
Add-Lines $report (MdList $agentsMissingAfter)
$report.Add('')
$report.Add("- Extra current Agents directories preserved: $($extraAgentsAfter.Count)")
Add-Lines $report (MdList $extraAgentsAfter)
$report.Add('')
$report.Add('## Recommendation')
$report.Add('')
if (-not $Restore) {
    $report.Add('- This was read-only. Restore only after explicit user confirmation.')
} else {
    $report.Add('- Restore completed without overwriting same-name skill directories.')
}
$report.Add('- Run compare_skill_hashes.ps1 for .system and same-name Agents packages.')

Set-Content -LiteralPath $ReportPath -Value ($report -join "`r`n") -Encoding UTF8

[pscustomobject]@{
    ReportPath = $ReportPath
    Restore = [bool]$Restore
    BackupBeforeRestore = $backupBeforeRestore
    BackupCodexCount = $hCodex.Count
    CurrentCodexBefore = $cCodexBefore.Count
    CurrentCodexAfter = $cCodexAfter.Count
    CodexCopied = $codexCopied.Count
    CodexMissingAfter = $codexMissingAfter.Count
    BackupAgentsCount = $hAgents.Count
    CurrentAgentsBefore = $cAgentsBefore.Count
    CurrentAgentsAfter = $cAgentsAfter.Count
    AgentsCopied = $agentsCopied.Count
    AgentsMissingAfter = $agentsMissingAfter.Count
} | ConvertTo-Json
