$ErrorActionPreference='Stop'
$root='C:\AI\Polsia-V5-Parallel-20261012'
$approval=Get-Content (Join-Path $root 'contracts\CEO_APPROVED_FIVE.json') -Raw -Encoding utf8|ConvertFrom-Json
if($approval.batch_id -ne 'POL5_20261012' -or $approval.parent_freeze -ne 'POLSIA-MOTHER-V008-F001' -or @($approval.branches).Count -ne 5){throw '本地派发合同双门不通过'}
$one=@($approval.branches)|Where-Object {$_.locator -eq ('【Polsia执行页｜'+$approval.task_id+'｜'+$_.id+'｜实】') -and $_.disposition -eq 'CEO_APPROVED_LOCAL_ISOLATED'}
if($one.Count -ne 5){throw '五个页面定位标签或批准范围不一致'}
$results=@($approval.branches | ForEach-Object -Parallel {
 $b=$_;$r=$using:root;$id=[string]$b.id
 $dir=Join-Path $r ('branches\'+$id)
 New-Item -ItemType Directory -Force -Path $dir|Out-Null
 $statusFile=Join-Path $dir 'status.json'
 if(Test-Path -LiteralPath $statusFile){
  $old=Get-Content -LiteralPath $statusFile -Raw -Encoding utf8|ConvertFrom-Json
  return [pscustomobject]@{branch=$id;state='EXISTS_NO_BLIND_REPLAY';previous=$old.status}
 }
 $started=[DateTime]::UtcNow.ToString('o')
 function Save-Step([string]$state,[string]$step,[int]$count,[string]$proof,[string]$problem){
  $record=[ordered]@{id=$id;name=[string]$b.name;status=$state;step=$step;verified_steps=$count;
   planned_steps=4;checkpoint='仅有上一母任务冻结 V008；本分支尚未冻结';
   evidence=$proof;issue=$problem;started_utc=$started;updated_utc=[DateTime]::UtcNow.ToString('o');
   contract_blob=[string]$b.contract_blob;locator=[string]$b.locator}
  $temp=$statusFile+'.'+$PID+'.tmp'
  [IO.File]::WriteAllText($temp,($record|ConvertTo-Json -Depth 6),[Text.UTF8Encoding]::new($false))
  Move-Item -LiteralPath $temp -Destination $statusFile -Force
 }
 $proof='执行回执待生成';$problem='';$count=0
 Save-Step 'RUNNING' '已通过本地授权与节点定位，开始执行' 0 $proof ''
 try {
  switch($id){
   'PA5-01' {
    Save-Step 'RUNNING' '从已存在的开源项目克隆成熟公司运行平台' 0 $proof ''
    $dest=Join-Path $r 'platform\open-polsia'
    if(Test-Path $dest){throw '源代码目录已有内容；为避免重复覆盖需要先独立核对'}
    $cmdOutput=(& git -c core.autocrlf=false clone --depth 1 --quiet https://github.com/AI-Builder-Club/open-polsia.git $dest 2>&1 | Out-String)
    if($LASTEXITCODE -ne 0){throw ('成熟开源项目克隆失败：'+$cmdOutput)}
    $count=1;Save-Step 'RUNNING' '已获取源代码，核对实际版本与许可证' 1 $proof ''
    $sha=(& git -C $dest rev-parse HEAD|Out-String).Trim()
    $lic=Get-Content (Join-Path $dest 'LICENSE') -Raw -ErrorAction Stop
    if($lic -notmatch 'MIT License'){throw '许可证与预期不一致，不运行未知软件'}
    $count=2;Save-Step 'RUNNING' 'MIT许可核对通过，核对官方脚本入口' 2 ('git='+$sha) ''
    $pkg=Get-Content (Join-Path $dest 'package.json') -Raw -Encoding utf8 | ConvertFrom-Json
    if(-not $pkg.scripts.dashboard){throw '官方仪表盘命令不存在'}
    $count=3;Save-Step 'RUNNING' '保存源码SHA、官方仪表盘入口和基本功能清单' 3 ('git='+$sha) ''
    $report=[ordered]@{source='https://github.com/AI-Builder-Club/open-polsia';commit=$sha;license='MIT';dashboard_command=[string]$pkg.scripts.dashboard;
     install_result='SOURCE_CLONED_NOT_FULL_BUSINESS_RUNTIME';time=(Get-Date).ToString('o')}
    [IO.File]::WriteAllText((Join-Path $dir 'platform-evidence.json'),($report|ConvertTo-Json -Depth 6),[Text.UTF8Encoding]::new($false))
    $proof='platform-evidence.json; git '+$sha;$count=4
    Save-Step 'DONE_SCOPED' '成熟源码与执行入口实证完成；完整运行需网站分支续接' $count $proof ''
   }
   'PA5-02' {
    Save-Step 'RUNNING' '等待成熟平台源码到位，检查官方本地站点入口' 0 $proof ''
    $dest=Join-Path $r 'platform\open-polsia'
    for($n=0;$n -lt 50 -and -not(Test-Path (Join-Path $dest 'package.json'));$n++){Start-Sleep -Seconds 1}
    if(-not(Test-Path (Join-Path $dest 'package.json'))){Save-Step 'WAITING_DEPENDENCY' '等待平台源码；禁止另造空站点' 0 '依赖 PA5-01' '成熟项目尚未就绪';break}
    $count=1;Save-Step 'RUNNING' '成熟平台源码已到位，核对现成网站命令' 1 'open-polsia/package.json' ''
    $pkg=Get-Content (Join-Path $dest 'package.json') -Raw -Encoding utf8 | ConvertFrom-Json
    if(-not $pkg.scripts.dashboard){throw '未找到已有dashboard脚本'}
    $count=2;Save-Step 'RUNNING' '安装官方项目依赖（禁用第三方安装脚本）' 2 'package.json + lockfile' ''
    $p=Get-Command pnpm.cmd -ErrorAction SilentlyContinue
    if(-not $p){Save-Step 'BLOCKED' '缺少官方所需包管理器，暂不运行站点' 2 'pnpm未找到' '依赖缺失';break}
    $log=Join-Path $dir 'pnpm-install.log'
    $output=(& $p.Source --dir $dest install --frozen-lockfile --ignore-scripts --prefer-offline 2>&1 | Out-String)
    [IO.File]::WriteAllText($log,$output,[Text.UTF8Encoding]::new($false))
    if($LASTEXITCODE -ne 0){Save-Step 'BLOCKED' '成熟项目依赖安装失败，需按官方方法处理' 2 'pnpm-install.log' ('安装退出码'+$LASTEXITCODE);break}
    $count=3;Save-Step 'RUNNING' '依赖安装完成，核对本地仪表盘真实启动条件' 3 'pnpm-install.log' ''
    $readme=Get-Content (Join-Path $dest 'README.md') -Raw -Encoding utf8
    $dbNeeded=($readme -match 'Postgres')
    $details=[ordered]@{dependencies_installed=$true;needs_postgres=$dbNeeded;needs_llm_auth=($readme -match 'ANTHROPIC_API_KEY');
     site_http_verified=$false;status='READY_TO_LAUNCH_WITH_OFFICIAL_PREREQUISITES'}
    [IO.File]::WriteAllText((Join-Path $dir 'site-readiness.json'),($details|ConvertTo-Json),[Text.UTF8Encoding]::new($false))
    Save-Step 'WAITING_DEPENDENCY' '依赖已安装；等待验证官方数据库和本地站点真实运行' 3 'site-readiness.json' '尚未获取站点HTTP200，不可称网站已建成'
   }
   'PA5-03' {
    Save-Step 'RUNNING' '核对现有工作流平台、权限与本机模型桥的无副作用健康接口' 0 $proof ''
    $services=@(