param([Parameter(Mandatory=$true)][string]$IntegrationWorktree,[Parameter(Mandatory=$true)][string[]]$Selected,[string[]]$Rejected=@())
$p=[IO.Path]::GetFullPath($IntegrationWorktree);@('# Integration Plan','', '## Selected')+@($Selected|ForEach-Object{"- $_"})+@('','## Rejected')+@($Rejected|ForEach-Object{"- $_"})+@('','## Gate','- 三轮测试后才可形成主线准入建议。')|Set-Content -LiteralPath (Join-Path $p 'INTEGRATION_PLAN.md') -Encoding UTF8










