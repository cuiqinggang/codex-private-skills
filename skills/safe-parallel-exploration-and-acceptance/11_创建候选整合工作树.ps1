param([Parameter(Mandatory=$true)][string]$ProjectPath,[Parameter(Mandatory=$true)][string]$ProjectSlug,[string]$Version='v1',[switch]$ConfirmCreate)
& (Join-Path $PSScriptRoot 'scripts\integration\create-integration-worktree.ps1') -ProjectPath $ProjectPath -ProjectSlug $ProjectSlug -Version $Version -ConfirmCreate:$ConfirmCreate







