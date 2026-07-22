param([Parameter(Mandatory=$true)][string]$WorktreePath)
$ErrorActionPreference='Stop'; Import-Module (Join-Path $PSScriptRoot '..\SafeExploration.Core.psm1') -Force; $p=Resolve-SafeFullPath $WorktreePath; $types=@(Get-ProjectEnvironment $p); $checks=@()
if($types-contains'python'){$checks+=[pscustomobject]@{name='python';passed=[bool](Get-Command python -ErrorAction SilentlyContinue)}}; if($types-contains'node'){$checks+=[pscustomobject]@{name='node';passed=[bool](Get-Command node -ErrorAction SilentlyContinue)}}
if($types-contains'powershell'){$errs=@(); Get-ChildItem -LiteralPath $p -Recurse -Filter *.ps1 -File -ErrorAction SilentlyContinue|ForEach-Object{[System.Management.Automation.Language.Parser]::ParseFile($_.FullName,[ref]$null,[ref]$errs)|Out-Null};$checks+=[pscustomobject]@{name='powershell-syntax';passed=($errs.Count-eq0);errors=@($errs.Message)}}
if($types-contains'skill'){$checks+=[pscustomobject]@{name='skill-frontmatter';passed=((Get-Content -LiteralPath (Join-Path $p 'SKILL.md') -Encoding UTF8 -TotalCount 1)-eq'---')}}
if($checks.Count-eq0){$checks+=[pscustomobject]@{name='path-readable';passed=$true}}
$passed=-not ($checks.passed -contains $false); [pscustomobject]@{status=if($passed){'ENVIRONMENT_READY'}else{'ENVIRONMENT_NOT_READY'};project_path=$p;types=$types;checks=$checks}|ConvertTo-Json -Depth 10; if(-not $passed){exit 1}










