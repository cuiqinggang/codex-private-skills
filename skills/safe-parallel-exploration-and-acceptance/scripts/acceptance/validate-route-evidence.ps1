param([Parameter(Mandatory=$true)][string]$WorktreePath)
$ErrorActionPreference='Stop'; $p=[IO.Path]::GetFullPath($WorktreePath); $statePath=Join-Path $p '.codex\acceptance-state.json'; if(-not(Test-Path -LiteralPath $statePath)){throw '缺少 acceptance-state.json'}
$s=Get-Content -LiteralPath $statePath -Encoding UTF8 -Raw|ConvertFrom-Json; $issues=@(); foreach($t in @($s.tests)){if($t.status-ne'passed'){$issues+="测试未通过: $($t.name)"};$ev=if([IO.Path]::IsPathRooted([string]$t.evidence)){$t.evidence}else{Join-Path $p $t.evidence};if(-not(Test-Path -LiteralPath $ev)){$issues+="证据不存在: $($t.evidence)"}}
$report=if([IO.Path]::IsPathRooted([string]$s.report_path)){$s.report_path}else{Join-Path $p $s.report_path}; if(-not $s.report_path -or -not(Test-Path -LiteralPath $report)){$issues+='路线报告不存在'}
[pscustomobject]@{status=if($issues.Count-eq0){'EVIDENCE_VALID'}else{'EVIDENCE_INVALID'};issues=$issues;test_count=@($s.tests).Count;report=$report}|ConvertTo-Json -Depth 8; if($issues.Count){exit 1}










