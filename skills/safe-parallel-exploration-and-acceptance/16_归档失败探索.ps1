param([Parameter(Mandatory=$true)][string]$WorktreePath,[Parameter(Mandatory=$true)][string]$ArchivePath)
& (Join-Path $PSScriptRoot 'scripts\worktree\archive-worktree-summary.ps1') -WorktreePath $WorktreePath -ArchivePath $ArchivePath







