param([Parameter(Mandatory=$true)][string]$ProjectPath,[Parameter(Mandatory=$true)][ValidatePattern('^[a-z0-9][a-z0-9._-]*$')][string]$ProjectSlug,[string]$Version='v1',[string]$WorktreeRoot="$env:USERPROFILE\.codex\worktrees",[switch]$ConfirmCreate)
$ErrorActionPreference='Stop'; $project=[IO.Path]::GetFullPath($ProjectPath);$root=[IO.Path]::GetFullPath($WorktreeRoot);if($root-match'^[Kk]:\\'){throw'禁止在 K 盘建立工作树'};$branch="integration/$ProjectSlug/$Version";$target=Join-Path $root "$ProjectSlug-integration-$Version"
if(-not $ConfirmCreate){[pscustomobject]@{status='PREVIEW_ONLY';branch=$branch;worktree_path=$target}|ConvertTo-Json;exit 0};$dirty=@(& git -C $project status --short);if($dirty.Count){throw '主工作区不干净'};if(Test-Path -LiteralPath $target){throw '目标路径已存在'};& git -C $project worktree add -b $branch $target HEAD;if($LASTEXITCODE -ne 0){throw '创建候选整合工作树失败'}
$codex=Join-Path $target '.codex';New-Item -ItemType Directory -Force -Path (Join-Path $codex 'evidence\tests'),(Join-Path $codex 'evidence\reports'),(Join-Path $codex 'evidence\screenshots')|Out-Null;'{"schema_version":"1.0","status":"INTEGRATION_CANDIDATE","tests":[],"final_status":"FAIL"}'|Set-Content -LiteralPath (Join-Path $codex 'acceptance-state.json') -Encoding UTF8
foreach($n in @('INTEGRATION_PLAN.md','SELECTED_COMPONENTS.md','REJECTED_COMPONENTS.md','CONFLICT_RESOLUTION.md','INTEGRATION_ACCEPTANCE.md')){"# $($n -replace '\.md$','')"|Set-Content -LiteralPath (Join-Path $target $n) -Encoding UTF8};[pscustomobject]@{status='INTEGRATION_CANDIDATE';branch=$branch;worktree_path=$target}|ConvertTo-Json










