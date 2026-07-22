param([Parameter(Mandatory=$true)][string]$ProjectPath,[Parameter(Mandatory=$true)][string]$ProjectSlug,[Parameter(Mandatory=$true)][string[]]$Routes,[switch]$ConfirmCreate)
foreach($route in $Routes){& (Join-Path $PSScriptRoot 'scripts\worktree\create-exploration-worktree.ps1') -ProjectPath $ProjectPath -ProjectSlug $ProjectSlug -Route $route -ConfirmCreate:$ConfirmCreate}







