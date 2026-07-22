param([Parameter(Mandatory=$true)][string]$CandidateDirectory)
$ErrorActionPreference='Stop'
if(Test-Path -LiteralPath $CandidateDirectory){ throw 'CandidateDirectory must not already exist.' }
Write-Output 'UPDATE_PREVIEW_ONLY: fetch upstream into the supplied new candidate directory, audit license/scripts/links, compare hashes, and run three test rounds. This script never replaces the stable skill.'

