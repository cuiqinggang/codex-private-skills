param([Parameter(Mandatory=$true)][string]$ProjectPath)
$ErrorActionPreference='Stop'
Import-Module (Join-Path $PSScriptRoot '..\SafeExploration.Core.psm1') -Force
$full=Resolve-SafeFullPath $ProjectPath; $git=Get-GitSnapshot $full
$issues=@(); $pathAudit=$null
if($git.runtime_context -eq 'BROKEN_GIT_MARKER'){$issues+='存在空或损坏的 .git 标记'}
elseif($git.runtime_context -eq 'NOT_GIT'){$issues+='不是 Git 仓库'}
elseif($git.runtime_context -eq 'BARE_REPOSITORY'){$issues+='当前是裸仓库，不能直接作为普通工作区'}
if($git.is_git_repository -and -not $git.head){$issues+='缺少 HEAD'}
if($git.is_worktree -and $git.status.Count -gt 0){$issues+='主工作区不干净'}
if($git.is_git_repository -and $git.head){
  $auditScript=Join-Path $PSScriptRoot '..\git\audit-windows-git-paths.py'
  $auditText=& python $auditScript --repository $full --revision $git.head
  $auditCode=$LASTEXITCODE
  if($auditCode -notin @(0,2)){throw "Windows Git 路径审计失败: exit=$auditCode"}
  $pathAudit=$auditText|ConvertFrom-Json
  if($pathAudit.status -eq 'WINDOWS_PATH_BLOCKED'){$issues+='Git tree 含 Windows 非法路径'}
}
$sensitive=@(Get-SensitiveFileRisks $full); if($sensitive.Count -gt 0){$issues+='存在敏感文件名风险'}
$nested=@(Get-ChildItem -LiteralPath $full -Recurse -Force -Directory -Filter .git -ErrorAction SilentlyContinue | Where-Object {$_.Parent.FullName -ne $full}); if($nested.Count -gt 0){$issues+='存在嵌套仓库'}
$status=if($git.runtime_context -eq 'BROKEN_GIT_MARKER'){'BROKEN_GIT_MARKER'}elseif($git.runtime_context -eq 'NOT_GIT'){'NOT_SUITABLE_FOR_WORKTREE'}elseif($issues -contains 'Git tree 含 Windows 非法路径'){'WINDOWS_PATH_BLOCKED'}elseif($git.runtime_context -eq 'BARE_REPOSITORY'){'BARE_REPOSITORY_REQUIRES_ISOLATED_OR_CLONE_FLOW'}elseif($issues.Count -eq 0){'WORKTREE_READY'}elseif($issues -contains '主工作区不干净' -or $issues -contains '存在嵌套仓库'){'MANUAL_REVIEW_REQUIRED'}else{'WORKTREE_READY_AFTER_FIX'}
[pscustomobject]@{schema_version='1.1';status=$status;project_path=$full;runtime_context=$git.runtime_context;issues=$issues;branch=$git.branch;head=$git.head;worktrees=$git.worktrees;windows_path_audit=$pathAudit;sensitive_risks=$sensitive;nested_repositories=@($nested | ForEach-Object {$_.FullName});recovery_script=if($status -eq 'WINDOWS_PATH_BLOCKED'){'scripts/git/create-windows-safe-isolated-worktree.ps1'}else{$null}}|ConvertTo-Json -Depth 20










