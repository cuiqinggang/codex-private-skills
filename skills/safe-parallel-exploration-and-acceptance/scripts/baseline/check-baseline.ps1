param([Parameter(Mandatory=$true)][string]$ProjectPath,[string]$OutputPath='')
$ErrorActionPreference='Stop'
Import-Module (Join-Path $PSScriptRoot '..\SafeExploration.Core.psm1') -Force
$full=Resolve-SafeFullPath $ProjectPath
if(-not (Test-Path -LiteralPath $full -PathType Container)){throw "项目不存在: $full"}
$git=Get-GitSnapshot $full
$sensitive=@(Get-SensitiveFileRisks $full)
$large=@(Get-LargeFileRisks $full 10)
$ignore=Join-Path $full '.gitignore'
$status=if(-not $git.is_git_repository){'BASELINE_CANDIDATE'}elseif(-not $git.head){'GIT_READY_AFTER_FIX'}elseif($git.status.Count -gt 0){'MANUAL_REVIEW_REQUIRED'}elseif($sensitive.Count -gt 0 -or $large.Count -gt 0){'GIT_READY_AFTER_FIX'}else{'GIT_READY'}
$result=[ordered]@{schema_version='1.0';status=$status;project_path=$full;git=$git;sensitive_risks=$sensitive;large_files=$large;gitignore_exists=(Test-Path -LiteralPath $ignore);checked_at=(Get-Date -Format o)}
if($OutputPath){Write-JsonFile $result (Resolve-SafeFullPath $OutputPath)}
$result | ConvertTo-Json -Depth 20










