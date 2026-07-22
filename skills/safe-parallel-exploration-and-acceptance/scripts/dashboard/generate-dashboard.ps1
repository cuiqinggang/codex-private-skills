param([Parameter(Mandatory=$true)][string]$WorkspacePath,[string]$RegistryPath='')
$ErrorActionPreference='Stop'
$w=[IO.Path]::GetFullPath($WorkspacePath)
if($w -match '^[Kk]:\\'){throw '禁止写入 K 盘'}
New-Item -ItemType Directory -Force -Path $w|Out-Null
$registry=@()
if($RegistryPath -and (Test-Path -LiteralPath $RegistryPath)){$registry=Get-Content -LiteralPath $RegistryPath -Encoding UTF8 -Raw|ConvertFrom-Json;$registry=@($registry)}
$counts=@{};foreach($l in @('L0','L1','L2','L3','MANUAL_REVIEW_REQUIRED')){$counts[$l]=@($registry|Where-Object management_level -eq $l).Count}
$testProject=Join-Path $w 'Safe_Exploration_Test_Project';$worktrees=@();$mainHead='';if(Test-Path -LiteralPath (Join-Path $testProject '.git')){$worktrees=@(& git -c core.quotepath=false -C $testProject worktree list);$mainHead=(& git -C $testProject rev-parse HEAD|Out-String).Trim()}
$p0=@($registry|Where-Object priority -eq 'P0').Count;$p1=@($registry|Where-Object priority -eq 'P1').Count
${REDACTED_SECRET}
$path=Join-Path $w '安全探索仪表盘.md';$lines|Set-Content -LiteralPath $path -Encoding UTF8;$path








