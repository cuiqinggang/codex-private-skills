param(
 [Parameter(Mandatory=$true)][string]$ProjectPath,
 [Parameter(Mandatory=$true)][ValidatePattern('^[a-z0-9][a-z0-9._-]*$')][string]$ProjectSlug,
 [Parameter(Mandatory=$true)][ValidatePattern('^[a-z0-9][a-z0-9._-]*$')][string]$Route,
 [string]$WorktreeRoot="$env:USERPROFILE\.codex\worktrees",
 [switch]$ConfirmCreate
)
$ErrorActionPreference='Stop'; Import-Module (Join-Path $PSScriptRoot '..\SafeExploration.Core.psm1') -Force
$project=Resolve-SafeFullPath $ProjectPath; $root=Assert-ActivePath $WorktreeRoot; $branch="explore/$ProjectSlug/$Route"; $target=Join-Path $root "$ProjectSlug-$Route"
if(-not $ConfirmCreate){[pscustomobject]@{status='PREVIEW_ONLY';project=$project;branch=$branch;worktree_path=$target;requires_confirm=$true}|ConvertTo-Json; exit 0}
$git=Get-GitSnapshot $project; if(-not $git.is_git_repository -or -not $git.head){throw 'Worktree 需要有效 Git 仓库和 HEAD'}; if($git.status.Count -gt 0){throw '主工作区不干净，禁止自动 stash 或清理'}
$auditScript=Join-Path $PSScriptRoot '..\git\audit-windows-git-paths.py'
$auditText=& python $auditScript --repository $project --revision $git.head
$auditCode=$LASTEXITCODE
if($auditCode -notin @(0,2)){throw "Windows Git 路径审计失败: exit=$auditCode"}
$audit=$auditText|ConvertFrom-Json
if($audit.status -eq 'WINDOWS_PATH_BLOCKED'){
  $first=@($audit.blocked_paths)[0]
  throw "Git tree 含 Windows 非法路径，禁止普通 worktree：$($first.path)。请改用 scripts/git/create-windows-safe-isolated-worktree.ps1。"
}
if(Test-Path -LiteralPath $target){throw "目标工作树路径已存在: $target"}; & git -C $project show-ref --verify --quiet "refs/heads/$branch"; if($LASTEXITCODE -eq 0){throw "分支已存在: $branch"}
New-Item -ItemType Directory -Force -Path $root|Out-Null
$previousErrorAction=$ErrorActionPreference
try{
  $ErrorActionPreference='Continue'
  $gitAddRaw=@(& git -C $project worktree add -b $branch $target $git.head 2>&1)
  $gitAddCode=$LASTEXITCODE
}finally{$ErrorActionPreference=$previousErrorAction}
$gitAddOutput=@($gitAddRaw|ForEach-Object{$_.ToString()})
if($gitAddCode -ne 0){throw "git worktree add 失败: $($gitAddOutput -join ' | ')"}
$codex=Join-Path $target '.codex'; New-Item -ItemType Directory -Force -Path $codex,(Join-Path $codex 'evidence\tests'),(Join-Path $codex 'evidence\screenshots'),(Join-Path $codex 'evidence\reports'),(Join-Path $codex 'evidence\logs'),(Join-Path $codex 'evidence\metrics')|Out-Null
$ctx=[ordered]@{schema_version='1.0';project_name=$ProjectSlug;mode='MODE-C';baseline_branch=$git.branch;baseline_commit=$git.head;worktree_branch=$branch;worktree_path=$target;route_id=$Route;route_name=$Route;hypothesis='';success_metrics=@();failure_metrics=@();stop_conditions=@();integration_eligible=$false;status='ACTIVE'}
Write-JsonFile $ctx (Join-Path $codex 'exploration-context.json'); Write-JsonFile ([ordered]@{schema_version='1.0';requires_acceptance=$true;task_type='skill';acceptance_level='LEVEL-3';tests=@();report_path='';screenshots=@();ui_required=$false;zip_required=$false;rollback_available=$true;final_status='FAIL';route_status='ACTIVE'}) (Join-Path $codex 'acceptance-state.json')
'# 路线验收策略`n`n必须先完成独立测试和证据；ROUTE_PASS 不等于 FINAL_PASS。'|Set-Content -LiteralPath (Join-Path $codex 'acceptance-policy.md') -Encoding UTF8
'# Exploration Route'|Set-Content -LiteralPath (Join-Path $target 'EXPLORATION_ROUTE.md') -Encoding UTF8; '# Experiment Changelog'|Set-Content -LiteralPath (Join-Path $target 'CHANGELOG_EXPERIMENT.md') -Encoding UTF8; '# Failure Notes'|Set-Content -LiteralPath (Join-Path $target 'FAILURE_NOTES.md') -Encoding UTF8
[pscustomobject]@{status='WORKTREE_CREATED';worktree_path=$target;branch=$branch;baseline_commit=$git.head;windows_path_audit=$audit.status;git_worktree_add_output=$gitAddOutput;main_status=@(& git -C $project status --short);worktree_status=@(& git -C $target status --short);evidence_path=(Join-Path $codex 'evidence')}|ConvertTo-Json -Depth 8










