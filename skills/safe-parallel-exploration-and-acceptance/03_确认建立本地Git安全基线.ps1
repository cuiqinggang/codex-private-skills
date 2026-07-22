param([Parameter(Mandatory=$true)][string]$ProjectPath,[Parameter(Mandatory=$true)][string[]]$IncludePaths,[switch]$ConfirmBaseline,[switch]$TestIdentity)
& (Join-Path $PSScriptRoot 'scripts\baseline\create-safe-baseline.ps1') -ProjectPath $ProjectPath -IncludePaths $IncludePaths -ConfirmBaseline:$ConfirmBaseline -TestIdentity:$TestIdentity







