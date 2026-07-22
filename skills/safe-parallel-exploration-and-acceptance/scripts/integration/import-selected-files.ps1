param(
    [Parameter(Mandatory=$true)][string]$IntegrationWorktree,
    [Parameter(Mandatory=$true)][string]$SourceRevision,
    [Parameter(Mandatory=$true)][string[]]$Files,
    [switch]$ConfirmImport
)
$ErrorActionPreference='Stop'
$p=[IO.Path]::GetFullPath($IntegrationWorktree)
foreach($f in $Files){
    if([IO.Path]::IsPathRooted($f) -or $f -match '^\.\.|(^|[\\/])\.env($|\.)'){throw "非法或敏感文件路径: $f"}
}
if(-not $ConfirmImport){
    [pscustomobject]@{status='PREVIEW_ONLY';source=$SourceRevision;files=$Files} | ConvertTo-Json
    exit 0
}
& git -C $p checkout $SourceRevision -- @Files
if($LASTEXITCODE -ne 0){throw '选择性文件导入失败'}
$Files | ForEach-Object { '- `' + $_ + '` from `' + $SourceRevision + '`' } | Add-Content -LiteralPath (Join-Path $p 'SELECTED_COMPONENTS.md') -Encoding UTF8
[pscustomobject]@{status='SELECTED_FILES_IMPORTED';source=$SourceRevision;files=$Files} | ConvertTo-Json -Depth 8









