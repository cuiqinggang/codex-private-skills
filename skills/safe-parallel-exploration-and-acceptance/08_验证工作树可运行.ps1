param([Parameter(Mandatory=$true)][string]$WorktreePath)
& (Join-Path $PSScriptRoot 'scripts\environment\verify-environment.ps1') -WorktreePath $WorktreePath







