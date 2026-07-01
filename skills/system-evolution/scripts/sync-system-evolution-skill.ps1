$ErrorActionPreference = 'Stop'
$SkillDir = 'C:\Users\A\.codex\skills\system-evolution'
$Dest = 'H:\AI_System_Evolution\skills\system-evolution'
if (-not (Test-Path 'H:\')) {
  Write-Output 'H drive not present; skipped.'
  exit 0
}
New-Item -ItemType Directory -Force -Path $Dest | Out-Null
Copy-Item -Path (Join-Path $SkillDir '*') -Destination $Dest -Recurse -Force
Write-Output "SYNCED $Dest"
