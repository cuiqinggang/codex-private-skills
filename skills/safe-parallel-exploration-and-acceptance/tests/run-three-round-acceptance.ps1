param([Parameter(Mandatory=$true)][string]$ProjectPath,[Parameter(Mandatory=$true)][string]$EvidenceDirectory)
$ErrorActionPreference='Stop';$p=[IO.Path]::GetFullPath($ProjectPath);$e=[IO.Path]::GetFullPath($EvidenceDirectory);if($e -match '^[Kk]:\\'){throw '禁止写入 K 盘'};New-Item -ItemType Directory -Force -Path $e|Out-Null;$rounds=@()
$r1=Join-Path $e 'round-1-static.json';& (Join-Path $PSScriptRoot 'run-static-tests.ps1') -EvidencePath $r1|Out-Null;$rounds+=[pscustomobject]@{round=1;name='结构与静态';status=if($LASTEXITCODE -eq 0){'passed'}else{'failed'};evidence=$r1}
$r2=Join-Path $e 'round-2-environment.json';$text=& (Join-Path (Split-Path -Parent $PSScriptRoot) 'scripts\environment\verify-environment.ps1') -WorktreePath $p;$text|Set-Content -LiteralPath $r2 -Encoding UTF8;$rounds+=[pscustomobject]@{round=2;name='功能与环境';status=if($LASTEXITCODE -eq 0){'passed'}else{'failed'};evidence=$r2}
$r3=Join-Path $e 'round-3-real-flow.json';$previous=$ErrorActionPreference;$ErrorActionPreference='SilentlyContinue';& git -C $p rev-parse --is-inside-work-tree 2>$null|Out-Null;$isRepo=($LASTEXITCODE -eq 0);$ErrorActionPreference=$previous;$branch=if($isRepo){(& git -C $p branch --show-current|Out-String).Trim()}else{''};$mainProtected=($branch -ne 'main');$real=[ordered]@{project=$p;is_git_repository=$isRepo;branch=$branch;main_protected=$mainProtected;git_status=@(if($isRepo){& git -C $p status --short});time=(Get-Date -Format o)};$real|ConvertTo-Json -Depth 10|Set-Content -LiteralPath $r3 -Encoding UTF8;$rounds+=[pscustomobject]@{round=3;name='真实入口与主线保护';status=if($isRepo -and $mainProtected){'passed'}else{'failed'};evidence=$r3}
$passed=-not ($rounds.status -contains 'failed');$summary=[ordered]@{schema_version='1.0';passed=$passed;rounds=$rounds;main_auto_merged=$false;push_performed=$false};$summary|ConvertTo-Json -Depth 12|Set-Content -LiteralPath (Join-Path $e 'three-round-summary.json') -Encoding UTF8;$summary|ConvertTo-Json -Depth 12;if(-not $passed){exit 1}





