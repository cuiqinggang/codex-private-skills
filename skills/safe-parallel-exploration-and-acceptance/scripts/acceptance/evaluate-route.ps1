param(
    [Parameter(Mandatory=$true)][string]$WorktreePath,
    [ValidateSet('auto','partial','fail','manual')][string]$Disposition='auto',
    [string[]]$SelectedFiles=@(),
    [string[]]$RejectedFiles=@()
)
$ErrorActionPreference='Stop'
$p=[IO.Path]::GetFullPath($WorktreePath)
$statePath=Join-Path $p '.codex\acceptance-state.json'
if(-not (Test-Path -LiteralPath $statePath)){throw '缺少验收状态'}
$s=Get-Content -LiteralPath $statePath -Encoding UTF8 -Raw | ConvertFrom-Json
$valid=$true
$issues=@()
foreach($t in @($s.tests)){
    if($t.status -ne 'passed'){$valid=$false;$issues+="测试未通过: $($t.name)"}
    $ev=if([IO.Path]::IsPathRooted([string]$t.evidence)){$t.evidence}else{Join-Path $p $t.evidence}
    if(-not (Test-Path -LiteralPath $ev)){$valid=$false;$issues+="证据不存在: $($t.evidence)"}
}
if($Disposition -eq 'partial'){
    $status='ROUTE_PARTIAL_PASS'
    if($SelectedFiles.Count -eq 0){throw 'PARTIAL_PASS 必须明确 SelectedFiles'}
    $lines=@('# Partial Extraction Plan','','## 保留文件')
    $lines+=@($SelectedFiles | ForEach-Object { '- `' + $_ + '`' })
    $lines+=@('','## 放弃文件')
    $lines+=@($RejectedFiles | ForEach-Object { '- `' + $_ + '`' })
    $lines+=@('','- 导入方式：仅使用 import-selected-files.ps1 的显式文件清单。')
    $lines | Set-Content -LiteralPath (Join-Path $p 'PARTIAL_EXTRACTION_PLAN.md') -Encoding UTF8
} elseif($Disposition -eq 'fail'){
    $status='ROUTE_FAIL'
} elseif($Disposition -eq 'manual'){
    $status='ROUTE_NEEDS_MANUAL_REVIEW'
} elseif($valid -and @($s.tests).Count -gt 0){
    $status='ROUTE_PASS'
} else {
    $status='ROUTE_FAIL'
}
$s | Add-Member -NotePropertyName route_status -NotePropertyValue $status -Force
$s | Add-Member -NotePropertyName updated_at -NotePropertyValue (Get-Date -Format o) -Force
$s | ConvertTo-Json -Depth 20 | Set-Content -LiteralPath $statePath -Encoding UTF8
[pscustomobject]@{status=$status;issues=$issues;selected_files=$SelectedFiles;partial_plan=(Test-Path -LiteralPath (Join-Path $p 'PARTIAL_EXTRACTION_PLAN.md'))} | ConvertTo-Json -Depth 8









