param(
  [string]$RuntimeSkills = "C:\AI\skills",
  [string]$KnowledgeRoot = "K:\AI\knowledge-brain",
  [switch]$Apply
)

$ErrorActionPreference = "Stop"
$Source = Split-Path -Parent $PSScriptRoot
$SkillTarget = Join-Path $RuntimeSkills "static-site-factory"
$KnowledgeTarget = Join-Path $KnowledgeRoot "references\static-site-factory.md"

Write-Host "[PREVIEW] Skill source: $Source"
Write-Host "[PREVIEW] Skill target: $SkillTarget"
Write-Host "[PREVIEW] Knowledge entry: $KnowledgeTarget"

if (-not $Apply) {
  Write-Host "Dry-run only. Re-run with -Apply after reviewing paths."
  exit 0
}

if (Test-Path $SkillTarget) {
  throw "Target already exists. Refusing to overwrite: $SkillTarget"
}

New-Item -ItemType Directory -Force -Path $RuntimeSkills | Out-Null
Copy-Item -Recurse -Force $Source $SkillTarget
New-Item -ItemType Directory -Force -Path (Split-Path -Parent $KnowledgeTarget) | Out-Null
Copy-Item -Force (Join-Path $Source "references\knowledge-entry.md") $KnowledgeTarget

$hash = Get-FileHash (Join-Path $SkillTarget "SKILL.md") -Algorithm SHA256
Write-Host "INSTALL_PASS"
Write-Host "SKILL=$SkillTarget"
Write-Host "KNOWLEDGE=$KnowledgeTarget"
Write-Host "SKILL_MD_SHA256=$($hash.Hash)"
