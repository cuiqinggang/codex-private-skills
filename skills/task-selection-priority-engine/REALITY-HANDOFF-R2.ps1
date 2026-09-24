# 【任务选择排序引擎 v0.2.0｜现实交接启动器 R2｜虚拟修复冻结】
# 只修复 Reality Delta：远端冻结包存在，但本地工作树未物化。
# 不修改算法、不修改冻结 ZIP、不修改准入/复审/排序规则。

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$Repo = 'C:\Users\A\Documents\Codex\codex-private-skills'
$Ref = 'codex/task-selection-priority-engine-v0.2.0-virtual-freeze'
$ZipRel = 'skills/task-selection-priority-engine/frozen/TSPE-v0.2.0.zip'
$ExpectedSha256 = 'dbf26948390bd64f723c75843593a5410e0f9fd4d9c1b526a1d9cce9c47f27b9'
$ExpectedGitBlob = 'ef599a3cee6839e062a62844389f7a5680bf642d'

Set-Location $Repo

$FetchSpec = '+refs/heads/' + $Ref + ':refs/remotes/origin/' + $Ref
git fetch origin $FetchSpec
if ($LASTEXITCODE -ne 0) { throw 'REALITY_HANDOFF_R2_FETCH_FAILED' }

$FrozenCommit = (git rev-parse ('refs/remotes/origin/' + $Ref)).Trim()
if (-not $FrozenCommit) { throw 'REALITY_HANDOFF_R2_COMMIT_UNRESOLVED' }

$BlobSpec = $FrozenCommit + ':' + $ZipRel
$ActualGitBlob = (git rev-parse $BlobSpec).Trim()
if ($LASTEXITCODE -ne 0 -or -not $ActualGitBlob) {
    throw 'REALITY_HANDOFF_R2_REMOTE_FROZEN_ARCHIVE_MISSING'
}
if ($ActualGitBlob -ne $ExpectedGitBlob) {
    throw ('REALITY_HANDOFF_R2_GIT_BLOB_MISMATCH expected=' + $ExpectedGitBlob + ' actual=' + $ActualGitBlob)
}

git checkout --detach $FrozenCommit
if ($LASTEXITCODE -ne 0) { throw 'REALITY_HANDOFF_R2_CHECKOUT_FAILED' }

$ZipAbs = Join-Path $Repo $ZipRel
$ZipDir = Split-Path -Parent $ZipAbs
New-Item -ItemType Directory -Path $ZipDir -Force | Out-Null

# 即使 sparse-checkout / skip-worktree 导致普通 checkout 没有物化文件，
# 也从冻结 commit 的 Git 对象强制恢复这个精确 blob。
git restore --source=$FrozenCommit --worktree --ignore-skip-worktree-bits -- $ZipRel
if ($LASTEXITCODE -ne 0) { throw 'REALITY_HANDOFF_R2_MATERIALIZE_FAILED' }

if (-not (Test-Path -LiteralPath $ZipAbs -PathType Leaf)) {
    throw 'REALITY_HANDOFF_R2_LOCAL_FROZEN_ARCHIVE_STILL_MISSING'
}

$ActualSha256 = (Get-FileHash -LiteralPath $ZipAbs -Algorithm SHA256).Hash.ToLowerInvariant()
if ($ActualSha256 -ne $ExpectedSha256) {
    throw ('REALITY_HANDOFF_R2_SHA256_MISMATCH expected=' + $ExpectedSha256 + ' actual=' + $ActualSha256)
}

$ExtractRoot = Join-Path $Repo '.reality\TSPE-v0.2.0-R2'
if (Test-Path -LiteralPath $ExtractRoot) {
    Remove-Item -LiteralPath $ExtractRoot -Recurse -Force
}
New-Item -ItemType Directory -Path $ExtractRoot -Force | Out-Null
Expand-Archive -LiteralPath $ZipAbs -DestinationPath $ExtractRoot -Force

$Verifier = Join-Path $ExtractRoot 'tspe_v020\frozen\v0.2.0\REAL-VERIFY-v0.2.0.py'
$Policy = Join-Path $ExtractRoot 'tspe_v020\frozen\v0.2.0\POLICY-v0.2.0.json'
$Fixtures = Join-Path $ExtractRoot 'tspe_v020\frozen\v0.2.0\GOLDEN-FIXTURES-v0.2.0.json'

foreach ($Required in @($Verifier, $Policy, $Fixtures)) {
    if (-not (Test-Path -LiteralPath $Required -PathType Leaf)) {
        throw ('REALITY_HANDOFF_R2_REQUIRED_FROZEN_FILE_MISSING=' + $Required)
    }
}

Write-Host ('REALITY_HANDOFF_R2=PASS')
Write-Host ('FROZEN_COMMIT=' + $FrozenCommit)
Write-Host ('FROZEN_ARCHIVE_GIT_BLOB=' + $ActualGitBlob)
Write-Host ('FROZEN_ARCHIVE_SHA256=' + $ActualSha256)
Write-Host ('FROZEN_ARCHIVE_SHA256_MATCH=YES')
Write-Host ('FROZEN_EXTRACT_ROOT=' + $ExtractRoot)
Write-Host ('FROZEN_REAL_VERIFIER=' + $Verifier)
Write-Host ('ACTION=PROCEED_TO_FROZEN_REAL_VERIFY')
