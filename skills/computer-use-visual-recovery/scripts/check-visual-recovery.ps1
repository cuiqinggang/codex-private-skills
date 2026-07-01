param(
  [switch]$Json
)

$ErrorActionPreference = 'Stop'

$homeDir = [Environment]::GetFolderPath('UserProfile')
$skillRoot = Join-Path $homeDir '.codex\skills'

$paths = @(
  'computer-use-visual-recovery\SKILL.md',
  'computer-use-visual-recovery\references\human-visible-operation.md',
  'computer-use-visual-recovery\references\recovery-map.md',
  'computer-use-visual-recovery\references\acceptance-matrix.md',
  'codex-computer-use\SKILL.md',
  'screenshot-recognize-operate-browser\SKILL.md',
  'screenshot-recognize-operate-browser\references\human-visible-coordinate-rule-20260701.md',
  'screenshot-browser-100-percent-route\SKILL.md',
  'screenshot\SKILL.md'
)

$results = foreach ($rel in $paths) {
  $full = Join-Path $skillRoot $rel
  [pscustomobject]@{
    relative = $rel
    path = $full
    exists = Test-Path -LiteralPath $full
  }
}

$allPresent = -not ($results | Where-Object { -not $_.exists })

if ($Json) {
  [pscustomobject]@{
    status = if ($allPresent) { 'PASS' } else { 'PARTIAL' }
    checkedAt = (Get-Date).ToString('s')
    skillRoot = $skillRoot
    results = $results
  } | ConvertTo-Json -Depth 5
  exit 0
}

"VISUAL_RECOVERY_CHECK: $(if ($allPresent) { 'PASS' } else { 'PARTIAL' })"
"SKILL_ROOT: $skillRoot"
foreach ($r in $results) {
  "{0} {1}" -f ($(if ($r.exists) { '[OK]' } else { '[MISSING]' })), $r.relative
}

if (-not $allPresent) {
  exit 2
}
