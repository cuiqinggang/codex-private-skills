param([Parameter(Mandatory=$true)][string]$ProjectPath)
& (Join-Path $PSScriptRoot 'scripts\worktree\list-project-worktrees.ps1') -ProjectPath $ProjectPath
git -C ([IO.Path]::GetFullPath($ProjectPath)) status --short
git -C ([IO.Path]::GetFullPath($ProjectPath)) branch --list







