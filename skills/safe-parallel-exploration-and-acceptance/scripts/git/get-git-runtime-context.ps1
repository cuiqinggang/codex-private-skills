param([Parameter(Mandatory=$true)][string]$ProjectPath)
$ErrorActionPreference='Stop'
Import-Module (Join-Path $PSScriptRoot '..\SafeExploration.Core.psm1') -Force
Get-GitRuntimeContext $ProjectPath | ConvertTo-Json -Depth 8

