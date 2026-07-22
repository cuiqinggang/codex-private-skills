param([Parameter(Mandatory=$true)][string]$ProjectPath,[Parameter(Mandatory=$true)][string]$ProjectSlug,[Parameter(Mandatory=$true)][string]$Route,[switch]$ConfirmCreate)
& (Join-Path $PSScriptRoot 'scripts\worktree\create-exploration-worktree.ps1') -ProjectPath $ProjectPath -ProjectSlug $ProjectSlug -Route $Route -ConfirmCreate:$ConfirmCreate







