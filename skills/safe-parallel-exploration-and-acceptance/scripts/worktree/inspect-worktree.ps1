param([Parameter(Mandatory=$true)][string]$WorktreePath)
$ErrorActionPreference='Stop'; Import-Module (Join-Path $PSScriptRoot '..\SafeExploration.Core.psm1') -Force
$p=Resolve-SafeFullPath $WorktreePath; $g=Get-GitSnapshot $p; $ctx=Join-Path $p '.codex\exploration-context.json'; $state=Join-Path $p '.codex\acceptance-state.json'
[pscustomobject]@{path=$p;git=$g;context_exists=(Test-Path -LiteralPath $ctx);acceptance_state_exists=(Test-Path -LiteralPath $state);dirty=($g.status.Count-gt 0)}|ConvertTo-Json -Depth 12










