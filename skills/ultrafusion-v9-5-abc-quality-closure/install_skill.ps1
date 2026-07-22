param(
    [Parameter(Mandatory=$true)]
    [string]$Destination
)

$ErrorActionPreference = "Stop"
$Source = Split-Path -Parent $MyInvocation.MyCommand.Path

if (-not (Test-Path (Join-Path $Source "SKILL.md"))) {
    throw "源目录缺少 SKILL.md：$Source"
}

if (Test-Path $Destination) {
    $stamp = Get-Date -Format "yyyyMMdd-HHmmss"
    $backup = "$Destination.backup-$stamp"
    Write-Host "发现旧目录，先备份到：$backup"
    Move-Item -Path $Destination -Destination $backup
}

New-Item -ItemType Directory -Path (Split-Path -Parent $Destination) -Force | Out-Null
Copy-Item -Path $Source -Destination $Destination -Recurse -Force

Write-Host "技能已部署到：$Destination"
Write-Host "请运行：python `"$Destination\scripts\self_test.py`""
