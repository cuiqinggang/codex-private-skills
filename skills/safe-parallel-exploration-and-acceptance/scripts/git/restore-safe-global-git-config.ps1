param(
    [bool]$DefaultBranchWasConfigured=$false,
    [string]$PreviousDefaultBranch='',
    [bool]$LongPathsWasConfigured=$false,
    [string]$PreviousLongPaths='',
    [switch]$ConfirmRestore
)
$plan=[ordered]@{status='PREVIEW_ONLY';init_defaultBranch=if($DefaultBranchWasConfigured){"restore:$PreviousDefaultBranch"}else{'unset'};core_longpaths=if($LongPathsWasConfigured){"restore:$PreviousLongPaths"}else{'unset'};other_git_config_untouched=$true}
if(-not $ConfirmRestore){$plan|ConvertTo-Json;exit 0}
if($DefaultBranchWasConfigured){git config --global init.defaultBranch $PreviousDefaultBranch}else{git config --global --unset-all init.defaultBranch 2>$null}
if($LongPathsWasConfigured){git config --global core.longpaths $PreviousLongPaths}else{git config --global --unset-all core.longpaths 2>$null}
[pscustomobject]@{status='SAFE_GLOBAL_GIT_CONFIG_RESTORED';other_git_config_untouched=$true}|ConvertTo-Json



