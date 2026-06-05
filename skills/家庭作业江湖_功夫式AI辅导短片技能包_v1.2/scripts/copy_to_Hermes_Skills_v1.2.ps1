$ErrorActionPreference = 'Stop'
Write-Host 'G01_BEGIN'
$zipName = 'homework_jianghu_ai_shortfilm_skill_v1.2.zip'
$downloads = Join-Path $env:USERPROFILE 'Downloads'
$desktop = [Environment]::GetFolderPath('Desktop')
$candidates = @(
  (Join-Path $downloads $zipName),
  (Join-Path $desktop $zipName)
)
$src = $candidates | Where-Object { Test-Path $_ } | Select-Object -First 1
if (-not $src) {
  Write-Host 'G01_FAIL_ZIP_NOT_FOUND'
  Write-Host "请先把 $zipName 下载到 下载 文件夹或桌面。"
  Write-Host 'G01_END'
  exit 1
}
$destRoot = 'H:\Hermes_Skills'
$dest = Join-Path $destRoot '家庭作业江湖_功夫式AI辅导短片技能包_v1.2'
if (-not (Test-Path $destRoot)) {
  Write-Host 'G01_FAIL_H_SKILLS_NOT_FOUND'
  Write-Host "没有找到 $destRoot"
  Write-Host 'G01_END'
  exit 1
}
if (Test-Path $dest) {
  $bak = "$dest.bak_$(Get-Date -Format yyyyMMdd_HHmmss)"
  Rename-Item -LiteralPath $dest -NewName (Split-Path $bak -Leaf)
  Write-Host "G01_BACKUP_OLD=$bak"
}
New-Item -ItemType Directory -Force -Path $dest | Out-Null
Expand-Archive -LiteralPath $src -DestinationPath $dest -Force
$skill = Join-Path $dest 'SKILL.md'
$timeline = Join-Path $dest 'remotion\shot_timeline_0.2s_v1.2.csv'
if ((Test-Path $skill) -and (Test-Path $timeline)) {
  Write-Host 'G01_PASS_SKILL_V12_SAVED'
  Write-Host "SKILL_PATH=$skill"
  Write-Host "TIMELINE_PATH=$timeline"
} else {
  Write-Host 'G01_FAIL_EXTRACT_INCOMPLETE'
  Write-Host "DEST=$dest"
  exit 1
}
Write-Host 'G01_END'
