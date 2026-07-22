param([Parameter(Mandatory=$true)][string]$ProjectPath,[Parameter(Mandatory=$true)][string]$Revision,[Parameter(Mandatory=$true)][string]$RecoveryPath,[switch]$ConfirmCreate)
$p=[IO.Path]::GetFullPath($ProjectPath);$r=[IO.Path]::GetFullPath($RecoveryPath);if($r -match '^[Kk]:\\'){throw '禁止 K 盘工作树'};if(-not $ConfirmCreate){[pscustomobject]@{status='PREVIEW_ONLY';revision=$Revision;recovery_path=$r}|ConvertTo-Json;exit 0};if(Test-Path -LiteralPath $r){throw '恢复路径已存在'};& git -C $p worktree add --detach $r $Revision;if($LASTEXITCODE -ne 0){throw '恢复工作树创建失败'};[pscustomobject]@{status='RECOVERY_WORKTREE_CREATED';path=$r;revision=$Revision;main_untouched=$true}|ConvertTo-Json








