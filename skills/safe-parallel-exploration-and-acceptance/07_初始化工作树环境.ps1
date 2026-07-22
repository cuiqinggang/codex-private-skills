param([Parameter(Mandatory=$true)][string]$WorktreePath,[switch]$InstallDependencies)
& (Join-Path $PSScriptRoot 'scripts\environment\bootstrap-worktree.ps1') -WorktreePath $WorktreePath -InstallDependencies:$InstallDependencies







