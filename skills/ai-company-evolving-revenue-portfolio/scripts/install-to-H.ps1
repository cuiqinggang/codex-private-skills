param(
    [string]$TargetRoot = 'H:\AI\skills',
    [switch]$AlsoHermesSkills
)

$ErrorActionPreference = 'Stop'

$SkillName = 'ai-company-evolving-revenue-portfolio'
$SourceDir = Split-Path -Parent $PSScriptRoot
$TargetDir = Join-Path $TargetRoot $SkillName

if (-not (Test-Path -LiteralPath $TargetRoot)) {
    New-Item -ItemType Directory -Force -Path $TargetRoot | Out-Null
}

$SourceFull = [System.IO.Path]::GetFullPath($SourceDir)
$TargetFull = [System.IO.Path]::GetFullPath($TargetDir)

if ($SourceFull -ieq $TargetFull) {
    Write-Host "Already installed at $TargetDir"
} else {
    Copy-Item -LiteralPath $SourceDir -Destination $TargetDir -Recurse -Force
    Write-Host "Installed to $TargetDir"
}

if ($AlsoHermesSkills) {
    $HermesRoot = 'H:\AI\Hermes\skills'
    if (-not (Test-Path -LiteralPath $HermesRoot)) {
        New-Item -ItemType Directory -Force -Path $HermesRoot | Out-Null
    }
    $HermesTarget = Join-Path $HermesRoot $SkillName
    Copy-Item -LiteralPath $SourceDir -Destination $HermesTarget -Recurse -Force
    Write-Host "Installed to $HermesTarget"
}
