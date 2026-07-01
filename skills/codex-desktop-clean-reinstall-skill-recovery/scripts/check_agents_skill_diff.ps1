[CmdletBinding()]
param(
    [string]$BackupAgentsSkills = "H:\Codex_Reinstall_Skill_Backup_20260611\agents-skills",
    [string]$CurrentAgentsSkills = "$env:USERPROFILE\.agents\skills",
    [string]$ReportPath = "$env:USERPROFILE\Desktop\1\output\agents-skill-diff-report.md"
)

$time = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
function Get-DirSummary([string]$Path) {
    if (-not (Test-Path -LiteralPath $Path)) {
        return [pscustomobject]@{ FileCount = 0; TotalBytes = 0; Hash = "MISSING" }
    }
    $files = @(Get-ChildItem -LiteralPath $Path -Recurse -File -Force -ErrorAction SilentlyContinue)
    $hashInput = foreach ($file in $files | Sort-Object FullName) {
        $relative = $file.FullName.Substring($Path.Length).TrimStart("\")
        $hash = (Get-FileHash -LiteralPath $file.FullName -Algorithm SHA256 -ErrorAction SilentlyContinue).Hash
        "$relative`t$($file.Length)`t$hash"
    }
    $joined = ($hashInput -join "`n")
    $bytes = [System.Text.Encoding]::UTF8.GetBytes($joined)
    $sha = [System.Security.Cryptography.SHA256]::Create()
    $digest = [BitConverter]::ToString($sha.ComputeHash($bytes)).Replace("-", "")
    return [pscustomobject]@{ FileCount = $files.Count; TotalBytes = ($files | Measure-Object Length -Sum).Sum; Hash = $digest }
}
function Names([string]$Path) {
    if (-not (Test-Path -LiteralPath $Path)) { return @() }
    return @(Get-ChildItem -LiteralPath $Path -Directory -Force -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Name)
}

$backupNames = Names $BackupAgentsSkills
$currentNames = Names $CurrentAgentsSkills
$allNames = @($backupNames + $currentNames | Sort-Object -Unique)
$rows = foreach ($name in $allNames) {
    $b = Join-Path $BackupAgentsSkills $name
    $c = Join-Path $CurrentAgentsSkills $name
    $bs = Get-DirSummary $b
    $cs = Get-DirSummary $c
    $status = if ($backupNames -notcontains $name) { "only-current" }
        elseif ($currentNames -notcontains $name) { "only-backup" }
        elseif ($bs.Hash -eq $cs.Hash) { "same" }
        elseif ($bs.FileCount -ne $cs.FileCount) { "file-count-different" }
        else { "hash-different" }
    [pscustomobject]@{
        Name = $name
        Status = $status
        BackupFiles = $bs.FileCount
        CurrentFiles = $cs.FileCount
        BackupBytes = $bs.TotalBytes
        CurrentBytes = $cs.TotalBytes
    }
}

New-Item -ItemType Directory -Force -Path (Split-Path -Parent $ReportPath) | Out-Null
$table = $rows | Sort-Object Status, Name | Format-Table -AutoSize | Out-String
$report = @"
# Agents Skill Diff Report

- Time: $time
- Backup Agents skills: $BackupAgentsSkills
- Current Agents skills: $CurrentAgentsSkills
- Mode: read-only

```text
$table
```

No files were copied, overwritten, deleted, or moved.
"@
$report | Set-Content -LiteralPath $ReportPath -Encoding UTF8
Write-Host "Agents diff report: $ReportPath"
