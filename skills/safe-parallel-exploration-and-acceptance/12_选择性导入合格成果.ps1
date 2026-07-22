param([Parameter(Mandatory=$true)][string]$IntegrationWorktree,[Parameter(Mandatory=$true)][string]$SourceRevision,[Parameter(Mandatory=$true)][string[]]$Files,[switch]$ConfirmImport)
& (Join-Path $PSScriptRoot 'scripts\integration\import-selected-files.ps1') -IntegrationWorktree $IntegrationWorktree -SourceRevision $SourceRevision -Files $Files -ConfirmImport:$ConfirmImport







