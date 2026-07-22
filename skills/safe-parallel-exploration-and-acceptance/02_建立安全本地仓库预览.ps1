param([Parameter(Mandatory=$true)][string]$ProjectPath,[string]$OutputPath='')
& (Join-Path $PSScriptRoot 'scripts\baseline\prepare-baseline-preview.ps1') -ProjectPath $ProjectPath -OutputPath $OutputPath







