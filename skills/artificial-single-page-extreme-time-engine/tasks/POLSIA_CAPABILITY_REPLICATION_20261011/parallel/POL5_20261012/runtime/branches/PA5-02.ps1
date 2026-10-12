$r='C:\AI\Polsia-V5-Parallel-20261012';$w=Join-Path $r 'save-status.ps1';$id='PA5-02';$ErrorActionPreference='Stop'
try{
& $w $id RUNNING '等待成熟平台源码，准备真实网站部署' 0
$p=Join-Path $r 'platform\open-polsia'
for($i=0;$i -lt 90 -and -not(Test-Path (Join-Path $p 'package.json'));$i++){Start-Sleep -Seconds 1}
if(-not(Test-Path (Join-Path $p 'package.json'))){& $w $id WAITING_DEPENDENCY '源码尚未就绪，等待平台分支' 0 'PA5-01';exit 0}
& $w $id RUNNING '实际检查成熟控制台，并安装官方依赖' 1
$j=Get-Content (Join-Path $p 'package.json') -Raw -Encoding utf8|ConvertFrom-Json
if(-not $j.scripts.dashboard){throw '官方控制台入口不存在'}
$log=Join-Path $r 'branches\PA5-02-install.log'
& pnpm.cmd --dir $p install --frozen-lockfile --ignore-scripts --prefer-offline 2>&1|Out-File -LiteralPath $log -Encoding utf8
if($LASTEXITCODE -ne 0){& $w $id BLOCKED '官方依赖安装失败，等待针对错误最小修复' 2 'PA5-02-install.log' ('退出码'+$LASTEXITCODE);exit 0}
& $w $id RUNNING '依赖已安装，核验本地网站启动先决条件' 3 'PA5-02-install.log'
$info=Get-Content (Join-Path $p 'README.md') -Raw -Encoding utf8
if($info -match 'Postgres'){& $w $id WAITING_DEPENDENCY '成熟平台需要数据库，暂不擅自配置生产账户' 3 'package.json' '需本地隔离数据库与合法模型配置'}
else{& $w $id DONE_SCOPED '官方依赖安装完成，网页HTTP实测仍待进行' 3 'PA5-02-install.log'}
}catch{& $w $id ERROR ('站点建设故障：'+$_.Exception.Message) 0 'PA5-02-install.log' $_.Exception.Message}