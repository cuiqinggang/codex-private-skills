param(
    [Parameter(Mandatory=$true)][string]$ProjectPath,
    [Parameter(Mandatory=$true)][string]$WorktreePath,
    [string]$ArchiveSummaryPath='',
    [switch]$ConfirmRemove
)
$ErrorActionPreference='Stop'
$project=[IO.Path]::GetFullPath($ProjectPath);$worktree=[IO.Path]::GetFullPath($WorktreePath)
if(-not $ConfirmRemove){[pscustomobject]@{status='PREVIEW_ONLY';worktree=$worktree;requires_confirm=$true}|ConvertTo-Json;exit 0}
$status=@(& git -C $worktree status --short)
if($status.Count -gt 0){throw '工作树含未提交内容，必须停止并请求用户确认'}
$summaryExists=(Test-Path (Join-Path $worktree 'FAILURE_NOTES.md')) -or (Test-Path (Join-Path $worktree 'INTEGRATION_ACCEPTANCE.md')) -or ($ArchiveSummaryPath -and (Test-Path -LiteralPath $ArchiveSummaryPath))
if(-not $summaryExists){throw '缺少归档/验收摘要'}
& git -C $project worktree remove -- $worktree
if($LASTEXITCODE -ne 0){throw '工作树移除失败'}
[pscustomobject]@{status='WORKTREE_REMOVED';worktree=$worktree}|ConvertTo-Json




