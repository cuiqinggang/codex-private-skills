$r='C:\AI\Polsia-V5-Parallel-20261012';$w=Join-Path $r 'save-status.ps1';$id='PA5-04';$ErrorActionPreference='Stop'
try{
& $w $id RUNNING '核对九类成熟业务矩阵、旧网站文件和真实截图条件' 0
$matrix='C:\AI\Polsia-Codex-20261011\CAPABILITY_MATRIX.md'
if(-not(Test-Path $matrix)){throw '已有九类能力矩阵未找到'}
$sha=(Get-FileHash $matrix -Algorithm SHA256).Hash
& $w $id RUNNING '已获取历史矩阵实际SHA，检查本地站点现物' 1 ('SHA='+$sha)
$site='C:\AI\AICompanyLab-20261011'
$files=@(Get-ChildItem $site -File -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Name)
& $w $id RUNNING '旧网站现物已核验，对标截图未取得前不作视觉通过判断' 2 '网站检查'
$report=[ordered]@{reference='https://polsia.com';matrix_sha256=$sha;historical_site_files=$files;functional_parity='NOT_VALIDATED';reference_screenshot='NOT_CAPTURED';local_screenshot='NOT_CAPTURED';reason='尚未核实已授权现有浏览器截图通道'}
[IO.File]::WriteAllText((Join-Path $r 'branches\PA5-04-comparison.json'),($report|ConvertTo-Json -Depth 6),[Text.UTF8Encoding]::new($false))
& $w $id DONE_SCOPED '对标差分基线已保存；真实截图与完整功能尚未通过' 3 'PA5-04-comparison.json' '左右截图尚未采集'
}catch{& $w $id ERROR ('独立对标异常：'+$_.Exception.Message) 0 '' $_.Exception.Message}