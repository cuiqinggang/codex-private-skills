param(
    [Parameter(Mandatory=$true)][string]$ProjectPath,
    [ValidateSet('MODE-A','MODE-B','MODE-C')][string]$Mode='MODE-B',
    [switch]$ConfirmEnable
)
$ErrorActionPreference='Stop'
$p=[IO.Path]::GetFullPath($ProjectPath)
if($p -match '^[Kk]:\\'){throw '禁止接入 K 盘活动项目'}
if(-not (Test-Path -LiteralPath $p -PathType Container)){throw '项目不存在'}
$dst=Join-Path $p '.codex'
$files=@('exploration-policy.json','acceptance-policy.md')
$conflicts=@($files | Where-Object { Test-Path -LiteralPath (Join-Path $dst $_) })
if(-not $ConfirmEnable){
    [pscustomobject]@{status='PREVIEW_ONLY';project=$p;mode=$Mode;existing_conflicts=$conflicts;requires_confirm=$true} | ConvertTo-Json
    exit 0
}
New-Item -ItemType Directory -Force -Path (Join-Path $dst 'evidence\tests'),(Join-Path $dst 'evidence\screenshots'),(Join-Path $dst 'evidence\reports'),(Join-Path $dst 'evidence\logs') | Out-Null
if($conflicts.Count){
    $backup=Join-Path $dst ('backup-safe-exploration-'+(Get-Date -Format yyyyMMdd-HHmmss))
    New-Item -ItemType Directory -Force -Path $backup | Out-Null
    foreach($f in $conflicts){Copy-Item -LiteralPath (Join-Path $dst $f) -Destination (Join-Path $backup $f)}
}
if(-not (Test-Path -LiteralPath (Join-Path $dst 'exploration-policy.json'))){
    [ordered]@{schema_version='1.0';enabled=$true;mode=$Mode;skill='safe-parallel-exploration-and-acceptance';enabled_at=(Get-Date -Format o)} | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $dst 'exploration-policy.json') -Encoding UTF8
}
if(-not (Test-Path -LiteralPath (Join-Path $dst 'acceptance-policy.md'))){
    "# Safe Exploration Acceptance Policy`n`n- Mode: $Mode`n- ROUTE_PASS is not FINAL_PASS.`n" | Set-Content -LiteralPath (Join-Path $dst 'acceptance-policy.md') -Encoding UTF8
}
if(-not (Test-Path -LiteralPath (Join-Path $p 'EXPLORATION_PLAN.md'))){'# Exploration Plan' | Set-Content -LiteralPath (Join-Path $p 'EXPLORATION_PLAN.md') -Encoding UTF8}
"# Safe Exploration Status`n`n- Enabled: true`n- Mode: $Mode" | Set-Content -LiteralPath (Join-Path $p 'SAFE_EXPLORATION_STATUS.md') -Encoding UTF8
[pscustomobject]@{status='SAFE_EXPLORATION_ENABLED';project=$p;mode=$Mode;conflicts_backed_up=$conflicts} | ConvertTo-Json -Depth 8









