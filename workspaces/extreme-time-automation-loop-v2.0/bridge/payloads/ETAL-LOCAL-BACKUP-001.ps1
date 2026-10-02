param(
  [string]$BridgeWorkDir,
  [string]$TaskFile
)

$ErrorActionPreference='Stop'
$backupRoot='C:\AI\backups\codex-private-skills'
$mirror=Join-Path $backupRoot 'codex-private-skills.git'
$bundleDir=Join-Path $backupRoot 'bundles'
$repoUrl='https://github.com/cuiqinggang/codex-private-skills.git'

New-Item -ItemType Directory -Path $backupRoot -Force | Out-Null
New-Item -ItemType Directory -Path $bundleDir -Force | Out-Null

$git=(Get-Command git.exe -ErrorAction Stop).Source
$gh=(Get-Command gh.exe -ErrorAction Stop).Source

& $gh auth status 1>$null 2>$null
if ($LASTEXITCODE -ne 0) { throw 'GH_AUTH_REQUIRED' }
& $gh auth setup-git 1>$null
if ($LASTEXITCODE -ne 0) { throw 'GH_AUTH_SETUP_GIT_FAILED' }

if (Test-Path -LiteralPath (Join-Path $mirror 'HEAD')) {
  & $git --git-dir=$mirror remote set-url origin $repoUrl
  if ($LASTEXITCODE -ne 0) { throw 'MIRROR_SET_URL_FAILED' }
  & $git --git-dir=$mirror remote update --prune
  if ($LASTEXITCODE -ne 0) { throw 'MIRROR_UPDATE_FAILED' }
} else {
  & $git clone --mirror $repoUrl $mirror
  if ($LASTEXITCODE -ne 0) { throw 'MIRROR_CLONE_FAILED' }
}

& $git --git-dir=$mirror fsck --full
if ($LASTEXITCODE -ne 0) { throw 'MIRROR_FSCK_FAILED' }

$stamp=(Get-Date).ToString('yyyyMMdd-HHmmss')
$bundle=Join-Path $bundleDir ("codex-private-skills-$stamp.bundle")
& $git --git-dir=$mirror bundle create $bundle --all
if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath $bundle)) { throw 'BUNDLE_CREATE_FAILED' }

& $git bundle verify $bundle 1>$null
if ($LASTEXITCODE -ne 0) { throw 'BUNDLE_VERIFY_FAILED' }

$head=(& $git --git-dir=$mirror rev-parse refs/heads/main).Trim()
$hash=(Get-FileHash -LiteralPath $bundle -Algorithm SHA256).Hash.ToLowerInvariant()
$size=(Get-Item -LiteralPath $bundle).Length
$meta=[ordered]@{
  status='LOCAL_SECOND_BACKUP_PASS'
  backup_root=$backupRoot
  mirror_path=$mirror
  bundle_path=$bundle
  bundle_sha256=$hash
  bundle_size_bytes=$size
  main_head=$head
  verified=$true
  created=(Get-Date).ToString('o')
}
$meta | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $backupRoot 'LATEST.json') -Encoding UTF8
$meta | ConvertTo-Json -Depth 5
