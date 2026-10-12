$r='C:\AI\Polsia-V5-Parallel-20261012';$w=Join-Path $r 'save-status.ps1';$id='PA5-01';$ErrorActionPreference='Stop'
try{
& $w $id RUNNING '实际克隆成熟公司平台' 0
$dest=Join-Path $r 'platform\open-polsia'
if(-not(Test-Path $dest)){& git -c core.autocrlf=false clone --quiet --depth 1 https://github.com/AI-Builder-Club/open-polsia.git $dest 2>&1|Out-String|Out-Null;if($LASTEXITCODE -ne 0){throw '源代码克隆失败'}}
& $w $id RUNNING '源码已落地，正在核对版本及许可证' 1
$sha=(& git -C $dest rev-parse HEAD|Out-String).Trim()
if((Get-Content (Join-Path $dest 'LICENSE') -Raw) -notmatch 'MIT License'){throw '开源许可证不符'}
& $w $id RUNNING '已核对许可证，正在检查成熟平台网站入口' 2 ('Git '+$sha)
$j=Get-Content (Join-Path $dest 'package.json') -Encoding utf8 -Raw|ConvertFrom-Json
if(-not $j.scripts.dashboard){throw '现成控制台脚本缺失'}
& $w $id DONE_SCOPED '成熟平台源码与官方控制台入口已核验；实际运行转网站分支' 4 ('Git '+$sha)
}catch{& $w $id ERROR ('平台接入故障：'+$_.Exception.Message) 0 '' $_.Exception.Message}