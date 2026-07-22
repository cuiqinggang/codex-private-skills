param([Parameter(Mandatory=$true)][string]$ProjectPath)
$root=Join-Path $PSScriptRoot 'scripts'
& (Join-Path $root 'baseline\check-baseline.ps1') -ProjectPath $ProjectPath
& (Join-Path $root 'environment\detect-project-environment.ps1') -ProjectPath $ProjectPath







