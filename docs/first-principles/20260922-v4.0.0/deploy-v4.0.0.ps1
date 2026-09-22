param(
  [string]$Repo = 'C:\Users\A\Documents\Codex\codex-private-skills',
  [string]$Branch = 'codex/first-principles-physical-limit-convergence-v4.0.0'
)

$ErrorActionPreference = 'Stop'
$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$skillRoot = Join-Path $HOME '.codex\skills'
$backupRoot = Join-Path $HOME ".codex\backups\first-principles-v4-$stamp"
$tmp = Join-Path $env:TEMP "fp-v4-$stamp"

Write-Host 'CURRENT_PHASE=实际验证'
Write-Host 'OBJECTIVE=min(T_VALID)'
Write-Host 'PROXY_CHANGE=FORBIDDEN'

if (-not (Test-Path -LiteralPath $Repo -PathType Container)) {
  throw "REPO_NOT_FOUND=$Repo"
}

$git = (Get-Command git -ErrorAction Stop).Source
& $git -C $Repo fetch origin $Branch
if ($LASTEXITCODE -ne 0) { throw 'GIT_FETCH_FAIL' }

& $git -C $Repo worktree add --detach $tmp "origin/$Branch"
if ($LASTEXITCODE -ne 0) { throw 'WORKTREE_ADD_FAIL' }

try {
  New-Item -ItemType Directory -Path $skillRoot -Force | Out-Null
  New-Item -ItemType Directory -Path $backupRoot -Force | Out-Null

  foreach ($name in @('first-principles-physical-limit-convergence','local-ai-reality-foundation')) {
    $src = Join-Path $tmp "skills\$name"
    $dst = Join-Path $skillRoot $name
    if (-not (Test-Path -LiteralPath $src -PathType Container)) {
      throw "SOURCE_SKILL_MISSING=$src"
    }
    if (Test-Path -LiteralPath $dst) {
      Copy-Item -LiteralPath $dst -Destination (Join-Path $backupRoot $name) -Recurse -Force
      Remove-Item -LiteralPath $dst -Recurse -Force
    }
    Copy-Item -LiteralPath $src -Destination $dst -Recurse -Force
  }

  $fpv = (Get-Content (Join-Path $skillRoot 'first-principles-physical-limit-convergence\VERSION') -Raw).Trim()
  $fdv = (Get-Content (Join-Path $skillRoot 'local-ai-reality-foundation\VERSION') -Raw).Trim()
  $fpSkill = Get-Content (Join-Path $skillRoot 'first-principles-physical-limit-convergence\SKILL.md') -Raw

  $contentGate = (
    $fpSkill -match '一虚一实' -and
    $fpSkill -match '虚拟成熟' -and
    $fpSkill -match '实际验证' -and
    $fpSkill -match 'min\(T_VALID\)'
  )

  $legacyBranch = (& $git -C $Repo ls-remote --heads origin 'codex/first-principles-physical-limit-convergence-v3.1.9' | Out-String).Trim()
  $legacyPass = [bool]$legacyBranch

  Write-Host "FIRST_PRINCIPLES_LOCAL_VERSION=$fpv"
  Write-Host "FOUNDATION_LOCAL_VERSION=$fdv"
  Write-Host "CONTENT_GATE=$contentGate"
  Write-Host "BACKUP_ROOT=$backupRoot"
  Write-Host "LEGACY_V3_BRANCH_PRESERVED=$legacyPass"
  Write-Host 'PROXY_CHANGED=NO'

  if ($fpv -eq '4.0.0' -and $fdv -eq '1.0.0' -and $contentGate -and $legacyPass) {
    Write-Host 'FINAL=PASS'
  } else {
    Write-Host 'FINAL=FAIL'
    exit 1
  }
  Write-Host 'ACTION=STOP'
}
finally {
  try { & $git -C $Repo worktree remove --force $tmp | Out-Null } catch {}
}
