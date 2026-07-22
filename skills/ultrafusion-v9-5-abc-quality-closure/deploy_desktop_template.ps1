param(
    [string]$Destination = "$([Environment]::GetFolderPath('Desktop'))\UltraFusion_V9.5.1_ABC运行母版_RC2"
)

$ErrorActionPreference = "Stop"
$SourceRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$Source = Join-Path $SourceRoot "桌面执行版模板"

if (-not (Test-Path $Source)) {
    throw "源目录不存在：$Source"
}

if (Test-Path $Destination) {
    $stamp = Get-Date -Format "yyyyMMdd-HHmmss"
    $backup = "$Destination.backup-$stamp"
    Write-Host "发现旧目录，先备份到：$backup"
    Move-Item -Path $Destination -Destination $backup
}

Copy-Item -Path $Source -Destination $Destination -Recurse -Force
Write-Host "桌面执行模板已部署到：$Destination"
Write-Host "不要直接使用1号母版；先复制为新的测试副本。"
