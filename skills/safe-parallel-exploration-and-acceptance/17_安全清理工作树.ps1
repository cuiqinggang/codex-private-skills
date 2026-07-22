param([Parameter(Mandatory=$true)][string]$ProjectPath,[Parameter(Mandatory=$true)][string]$WorktreePath,[switch]$ConfirmRemove)
if(-not $ConfirmRemove){& (Join-Path $PSScriptRoot 'scripts\worktree\preview-worktree-cleanup.ps1') -ProjectPath $ProjectPath -WorktreePath $WorktreePath}else{& (Join-Path $PSScriptRoot 'scripts\worktree\remove-safe-worktree.ps1') -ProjectPath $ProjectPath -WorktreePath $WorktreePath -ConfirmRemove}







