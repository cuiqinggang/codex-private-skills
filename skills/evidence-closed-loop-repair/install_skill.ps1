param(
    [string]$Destination = "C:\AI\skills\evidence-closed-loop-repair"
)

$ErrorActionPreference = "Stop"
$Source = Split-Path -Parent $MyInvocation.MyCommand.Path

if (-not (Test-Path (Join-Path $Source "SKILL.md"))) {
    throw "SKILL.md not found in source folder: $Source"
}

if (Test-Path $Destination) {
    $stamp = Get-Date -Format "yyyyMMdd-HHmmss"
    $backup = "$Destination.backup-$stamp"
    Write-Host "Existing skill found. Backing up to: $backup"
    Move-Item -Path $Destination -Destination $backup
}

New-Item -ItemType Directory -Path (Split-Path -Parent $Destination) -Force | Out-Null
Copy-Item -Path $Source -Destination $Destination -Recurse -Force
Write-Host "Installed to: $Destination"
Write-Host "Run self-test: python `"$Destination\scripts\self_test.py`""
