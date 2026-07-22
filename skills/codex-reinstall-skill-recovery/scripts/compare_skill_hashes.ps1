param(
    [string]$BackupRoot = 'H:\Codex_Reinstall_Skill_Backup_20260611',
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
    [string]$ReportPath = ''
)

$ErrorActionPreference = 'Stop'

$timestamp = Get-Date -Format 'yyyyMMdd-HHmmss'
if ([string]::IsNullOrWhiteSpace($ReportPath)) {
    $ReportPath = Join-Path $OutputRoot "codex-reinstall-skill-hash-diff-report-$timestamp.md"
}

$backupCodexSkills = Join-Path $BackupRoot 'codex-skills'
$backupAgentsSkills = Join-Path $BackupRoot 'agents-skills'

$comparisons = @(
    [pscustomobject]@{
        Name = 'codex .system'
        BackupPath = (Join-Path $backupCodexSkills '.system')
        CurrentPath = (Join-Path $CurrentCodexSkills '.system')
    }
)

if (Test-Path -LiteralPath $backupAgentsSkills -PathType Container) {
    $agentNames = @(Get-ChildItem -LiteralPath $backupAgentsSkills -Directory -Force | Select-Object -ExpandProperty Name | Sort-Object)
    foreach ($agentName in $agentNames) {
        $comparisons += [pscustomobject]@{
            Name = "agents $agentName"
            BackupPath = (Join-Path $backupAgentsSkills $agentName)
            CurrentPath = (Join-Path $CurrentAgentsSkills $agentName)
        }
    }
}

function Get-FileMap {
    param([string]$Root)
    $map = @{}
    if (-not (Test-Path -LiteralPath $Root -PathType Container)) {
        return $map
    }
    $rootFull = (Resolve-Path -LiteralPath $Root).Path.TrimEnd('\')
    $files = @(Get-ChildItem -LiteralPath $Root -File -Recurse -Force)
    foreach ($file in $files) {
        $relative = $file.FullName.Substring($rootFull.Length).TrimStart('\')
        $hash = (Get-FileHash -LiteralPath $file.FullName -Algorithm SHA256).Hash
        $map[$relative] = $hash
    }
    return $map
}

function Format-List {
    param($Items, [int]$Limit = 80)
    $arr = @($Items)
    if ($arr.Count -eq 0) {
        return @('- none')
    }
    $out = New-Object System.Collections.Generic.List[string]
    foreach ($item in ($arr | Select-Object -First $Limit)) {
        $out.Add("- $item")
    }
    if ($arr.Count -gt $Limit) {
        $out.Add("- ... truncated, $($arr.Count - $Limit) more")
    }
    return $out
}

function Add-Lines {
    param($Target, $Items)
    foreach ($item in @($Items)) {
        $Target.Add([string]$item)
    }
}

$results = New-Object System.Collections.Generic.List[object]
foreach ($comparison in $comparisons) {
    $backupExists = Test-Path -LiteralPath $comparison.BackupPath -PathType Container
    $currentExists = Test-Path -LiteralPath $comparison.CurrentPath -PathType Container
    $backupMap = Get-FileMap $comparison.BackupPath
    $currentMap = Get-FileMap $comparison.CurrentPath
    $backupKeys = @($backupMap.Keys | Sort-Object)
    $currentKeys = @($currentMap.Keys | Sort-Object)
    $missingInCurrent = @($backupKeys | Where-Object { -not $currentMap.ContainsKey($_) } | Sort-Object)
    $extraInCurrent = @($currentKeys | Where-Object { -not $backupMap.ContainsKey($_) } | Sort-Object)
    $common = @($backupKeys | Where-Object { $currentMap.ContainsKey($_) } | Sort-Object)
    $different = @($common | Where-Object { $backupMap[$_] -ne $currentMap[$_] } | Sort-Object)
    $results.Add([pscustomobject]@{
        Name = $comparison.Name
        BackupPath = $comparison.BackupPath
        CurrentPath = $comparison.CurrentPath
        BackupFileCount = $backupKeys.Count
        CurrentFileCount = $currentKeys.Count
        MissingInCurrent = $missingInCurrent
        ExtraInCurrent = $extraInCurrent
        Different = $different
        Identical = ($backupExists -and $currentExists -and $missingInCurrent.Count -eq 0 -and $extraInCurrent.Count -eq 0 -and $different.Count -eq 0)
    })
}

$identicalCount = @($results | Where-Object { $_.Identical }).Count
$differentResults = @($results | Where-Object { -not $_.Identical })

$report = New-Object System.Collections.Generic.List[string]
$report.Add('# Codex reinstall skill hash/diff report')
$report.Add('')
$report.Add("Generated at: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz')")
$report.Add('Read-only check: no skill package was modified.')
$report.Add('')
$report.Add('## Summary')
$report.Add('')
$report.Add("- Total compared packages: $($results.Count)")
$report.Add("- Identical packages: $identicalCount")
$report.Add("- Packages with differences: $($differentResults.Count)")
$report.Add('')
$report.Add('## Package table')
$report.Add('')
$report.Add('| Package | Backup files | Current files | Missing | Extra | Different hashes | Status |')
$report.Add('| --- | ---: | ---: | ---: | ---: | ---: | --- |')
foreach ($result in $results) {
    $status = if ($result.Identical) { 'identical' } else { 'different' }
    $report.Add("| $($result.Name) | $($result.BackupFileCount) | $($result.CurrentFileCount) | $($result.MissingInCurrent.Count) | $($result.ExtraInCurrent.Count) | $($result.Different.Count) | $status |")
}
$report.Add('')

if ($differentResults.Count -gt 0) {
    $report.Add('## Difference details')
    $report.Add('')
    foreach ($result in $differentResults) {
        $report.Add("### $($result.Name)")
        $report.Add('')
        $report.Add("- Backup path: $($result.BackupPath)")
        $report.Add("- Current path: $($result.CurrentPath)")
        $report.Add("- Missing in current: $($result.MissingInCurrent.Count)")
        Add-Lines $report (Format-List $result.MissingInCurrent)
        $report.Add('')
        $report.Add("- Extra in current: $($result.ExtraInCurrent.Count)")
        Add-Lines $report (Format-List $result.ExtraInCurrent)
        $report.Add('')
        $report.Add("- Different hashes: $($result.Different.Count)")
        Add-Lines $report (Format-List $result.Different)
        $report.Add('')
    }
} else {
    $report.Add('## Difference details')
    $report.Add('')
    $report.Add('- No differences found.')
}

$report.Add('')
$report.Add('## Recommendation')
$report.Add('')
if ($differentResults.Count -eq 0) {
    $report.Add('- No restore action is needed for .system or Agents skills.')
} else {
    $report.Add('- Do not overwrite automatically. Review differences first.')
    $report.Add('- Prefer keeping current official .system unless a specific old file is needed.')
    $report.Add('- Treat __pycache__ and .pyc differences as usually safe to ignore.')
}

Set-Content -LiteralPath $ReportPath -Value ($report -join "`r`n") -Encoding UTF8

[pscustomobject]@{
    ReportPath = $ReportPath
    TotalCompared = $results.Count
    Identical = $identicalCount
    Different = $differentResults.Count
    DifferentPackages = @($differentResults | Select-Object -ExpandProperty Name)
} | ConvertTo-Json -Depth 4
