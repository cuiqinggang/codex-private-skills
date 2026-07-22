param([Parameter(Mandatory=$true)][string]$IntegrationWorktree,[Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-fA-F]{7,40}$')][string]$Commit,[switch]$ConfirmImport)
$ErrorActionPreference='Stop';$p=[IO.Path]::GetFullPath($IntegrationWorktree);if(-not$ConfirmImport){[pscustomobject]@{status='PREVIEW_ONLY';commit=$Commit}|ConvertTo-Json;exit 0};& git -C $p cherry-pick --no-commit $Commit;if($LASTEXITCODE-ne0){throw'选择性提交导入发生冲突；保持现场并人工处理'};[pscustomobject]@{status='COMMIT_IMPORTED_NO_COMMIT';commit=$Commit}|ConvertTo-Json










