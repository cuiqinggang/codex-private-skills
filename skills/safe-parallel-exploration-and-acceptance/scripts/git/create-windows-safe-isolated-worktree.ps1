param(
  [Parameter(Mandatory=$true)][string]$RepositoryPath,
  [Parameter(Mandatory=$true)][string]$WorktreePath,
  [Parameter(Mandatory=$true)][string]$BranchName,
  [string]$BaseRevision='HEAD',
  [string]$ProtectionTag='',
  [switch]$ConfirmCreate
)
$ErrorActionPreference='Stop'
Import-Module (Join-Path $PSScriptRoot '..\SafeExploration.Core.psm1') -Force
$repo=Resolve-SafeFullPath $RepositoryPath
$target=Resolve-SafeFullPath $WorktreePath
if($target -notmatch '^[Cc]:\\'){throw "Windows 安全工作树必须位于 C 盘: $target"}
if($BranchName -notmatch '^(feature|explore|integration)/[A-Za-z0-9._/-]+$' -or $BranchName -match '\.\.|//'){throw "非法分支名: $BranchName"}
$context=Get-GitRuntimeContext $repo
if($context.context -notin @('WORKTREE','BARE_REPOSITORY')){throw "需要有效 Git 工作树或裸仓库，当前: $($context.context)"}
$base=(& git -C $repo rev-parse "$BaseRevision^{commit}" 2>$null|Out-String).Trim()
if($LASTEXITCODE -ne 0 -or -not $base){throw "无法解析基线提交: $BaseRevision"}
$auditScript=Join-Path $PSScriptRoot 'audit-windows-git-paths.py'
$auditText=& python $auditScript --repository $repo --revision $base
$auditCode=$LASTEXITCODE
$audit=$auditText|ConvertFrom-Json
if($auditCode -ne 2 -or $audit.status -ne 'WINDOWS_PATH_BLOCKED'){throw '当前树未被 Windows 非法路径阻断，应使用普通 worktree 流程'}
$preview=[ordered]@{schema_version='1.0';status='PREVIEW_ONLY';mode='WINDOWS_SAFE_ISOLATED_ORPHAN';repository=$repo;repository_context=$context.context;base_revision=$base;blocked_paths=$audit.blocked_paths;branch=$BranchName;worktree_path=$target;protection_tag=$ProtectionTag;main_or_base_will_change=$false;automatic_merge=$false;push=$false;requires_confirm=$true}
if(-not $ConfirmCreate){$preview|ConvertTo-Json -Depth 12;exit 0}
if(Test-Path -LiteralPath $target){throw "目标工作树已存在: $target"}
& git -C $repo show-ref --verify --quiet "refs/heads/$BranchName"
if($LASTEXITCODE -eq 0){throw "分支已存在: $BranchName"}
if($ProtectionTag){
  & git -C $repo show-ref --verify --quiet "refs/tags/$ProtectionTag"
  if($LASTEXITCODE -eq 0){throw "保护标签已存在: $ProtectionTag"}
  & git -C $repo tag -a $ProtectionTag $base -m 'Protected before Windows-safe isolated worktree recovery'
  if($LASTEXITCODE -ne 0){throw '创建本地保护标签失败'}
}
$emptyTree=(($null|& git -C $repo mktree)|Out-String).Trim()
if($LASTEXITCODE -ne 0 -or -not $emptyTree){throw '创建空树对象失败'}
$oldAuthorName=$env:GIT_AUTHOR_NAME;$oldAuthorEmail=$env:GIT_AUTHOR_EMAIL;$oldCommitterName=$env:GIT_COMMITTER_NAME;$oldCommitterEmail=$env:GIT_COMMITTER_EMAIL
try{
  $env:GIT_AUTHOR_NAME='OpenAI Codex';$env:GIT_AUTHOR_EMAIL='codex-local@localhost';$env:GIT_COMMITTER_NAME='OpenAI Codex';$env:GIT_COMMITTER_EMAIL='codex-local@localhost'
  $orphan=( & git -C $repo commit-tree $emptyTree -m 'chore: bootstrap Windows-safe isolated branch'|Out-String).Trim()
}finally{
  $env:GIT_AUTHOR_NAME=$oldAuthorName;$env:GIT_AUTHOR_EMAIL=$oldAuthorEmail;$env:GIT_COMMITTER_NAME=$oldCommitterName;$env:GIT_COMMITTER_EMAIL=$oldCommitterEmail
}
if($LASTEXITCODE -ne 0 -or -not $orphan){throw '创建孤立引导提交失败'}
& git -C $repo update-ref "refs/heads/$BranchName" $orphan
if($LASTEXITCODE -ne 0){throw '创建孤立安全分支失败'}
$parent=Split-Path -Parent $target
if($parent){New-Item -ItemType Directory -Force -Path $parent|Out-Null}
$previousErrorAction=$ErrorActionPreference
try{
  $ErrorActionPreference='Continue'
  $gitAddRaw=@(& git -C $repo worktree add $target $BranchName 2>&1)
  $gitAddCode=$LASTEXITCODE
}finally{$ErrorActionPreference=$previousErrorAction}
$gitAddOutput=@($gitAddRaw|ForEach-Object{$_.ToString()})
if($gitAddCode -ne 0){throw "创建 Windows 安全孤立工作树失败；保留分支与证据，禁止自动清理: $($gitAddOutput -join ' | ')"}
$baseAfter=(& git -C $repo rev-parse "$BaseRevision^{commit}"|Out-String).Trim()
[ordered]@{schema_version='1.0';status='ISOLATED_WORKTREE_CREATED';mode='WINDOWS_SAFE_ISOLATED_ORPHAN';repository=$repo;base_before=$base;base_after=$baseAfter;base_unchanged=($baseAfter -eq $base);branch=$BranchName;orphan_commit=$orphan;worktree_path=$target;protection_tag=$ProtectionTag;git_worktree_add_output=$gitAddOutput;automatic_merge=$false;push=$false;warning='孤立分支与 main 无祖先关系；只允许候选验证和显式文件导入，不得自动合并主线'}|ConvertTo-Json -Depth 12
