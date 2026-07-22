param([string]$SkillPath=(Split-Path -Parent $PSScriptRoot),[string]$EvidencePath='')
$ErrorActionPreference='Stop';$root=[IO.Path]::GetFullPath($SkillPath);$results=@()
$required=@('SKILL.md','agents\openai.yaml','scripts\SafeExploration.Core.psm1','scripts\classification\classify-task.ps1','scripts\baseline\check-baseline.ps1','scripts\worktree\create-exploration-worktree.ps1','scripts\git\get-git-runtime-context.ps1','scripts\git\audit-windows-git-paths.py','scripts\git\create-windows-safe-isolated-worktree.ps1','scripts\acceptance\verify-exact-byte-assets.py','scripts\acceptance\test-readonly-sandbox-injection.py','scripts\acceptance\evaluate-route.ps1','scripts\integration\create-integration-worktree.ps1','scripts\environment\verify-environment.ps1','tests\test_runtime_hardening.py','references\WINDOWS_GIT_INVALID_PATH_RECOVERY.md','references\EXACT_BYTE_READONLY_ASSET_POLICY.md','90_RUNTIME_HARDENING\RUNTIME_HARDENING_CHECKLIST.md','启动_完整安全探索工作台.cmd')
foreach($rel in $required){$results+=[pscustomobject]@{name="exists:$rel";passed=(Test-Path -LiteralPath (Join-Path $root $rel));detail=$rel}}
$parseErrors=@();Get-ChildItem -LiteralPath $root -Recurse -File|Where-Object {$_.Extension -in @('.ps1','.psm1')}|ForEach-Object {$e=$null;[System.Management.Automation.Language.Parser]::ParseFile($_.FullName,[ref]$null,[ref]$e)|Out-Null;foreach($x in @($e)){$parseErrors+="$($_.FullName):$($x.Extent.StartLineNumber):$($x.Message)"}}
$results+=[pscustomobject]@{name='powershell-syntax';passed=($parseErrors.Count -eq 0);detail=($parseErrors -join '; ')}
$pythonErrors=@();Get-ChildItem -LiteralPath $root -Recurse -Filter *.py -File|ForEach-Object {& python -m py_compile $_.FullName 2>&1|Out-Null;if($LASTEXITCODE -ne 0){$pythonErrors+=$_.FullName}}
$results+=[pscustomobject]@{name='python-syntax';passed=($pythonErrors.Count -eq 0);detail=($pythonErrors -join '; ')}
$jsonErrors=@();Get-ChildItem -LiteralPath $root -Recurse -Filter *.json -File|ForEach-Object {try{Get-Content -LiteralPath $_.FullName -Encoding UTF8 -Raw|ConvertFrom-Json|Out-Null}catch{$jsonErrors+="$($_.FullName):$($_.Exception.Message)"}}
$results+=[pscustomobject]@{name='json-valid';passed=($jsonErrors.Count -eq 0);detail=($jsonErrors -join '; ')}
${REDACTED_SECRET}
${REDACTED_SECRET}
$results+=[pscustomobject]@{name='hooks-no-duplicate-registration';passed=($duplicates.Count -eq 0);detail=($duplicates -join '; ')}
$passed=-not ($results.passed -contains $false);$out=[ordered]@{schema_version='1.0';suite='static';passed=$passed;time=(Get-Date -Format o);results=$results}
if($EvidencePath){$parent=Split-Path -Parent $EvidencePath;if($parent){New-Item -ItemType Directory -Force -Path $parent|Out-Null};$out|ConvertTo-Json -Depth 20|Set-Content -LiteralPath $EvidencePath -Encoding UTF8}
$out|ConvertTo-Json -Depth 20;if(-not $passed){exit 1}





