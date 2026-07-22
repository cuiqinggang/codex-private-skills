param([Parameter(Mandatory=$true)][string]$ProjectPath,[Parameter(Mandatory=$true)][string]$EvidenceDirectory)
& (Join-Path $PSScriptRoot 'tests\run-three-round-acceptance.ps1') -ProjectPath $ProjectPath -EvidenceDirectory $EvidenceDirectory







