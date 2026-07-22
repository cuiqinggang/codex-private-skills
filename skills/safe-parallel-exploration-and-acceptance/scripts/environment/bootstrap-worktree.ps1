param([Parameter(Mandatory=$true)][string]$WorktreePath,[switch]$InstallDependencies)
$ErrorActionPreference='Stop'; Import-Module (Join-Path $PSScriptRoot '..\SafeExploration.Core.psm1') -Force; $p=Assert-ActivePath $WorktreePath; $types=@(Get-ProjectEnvironment $p); $actions=@()
if($InstallDependencies){
 if($types -contains 'python'){throw '依赖安装需要项目明确命令；此安全引导器不猜测或升级依赖'}
 if($types -contains 'node'){if(Test-Path (Join-Path $p 'package-lock.json')){& npm --prefix $p ci; if($LASTEXITCODE-ne0){throw 'npm ci 失败'}; $actions+='npm ci'}else{throw 'Node 项目缺少受支持锁文件，停止'}}
}
$codex=Join-Path $p '.codex'; New-Item -ItemType Directory -Force -Path $codex|Out-Null; $out=[ordered]@{schema_version='1.0';project_path=$p;types=$types;installed=$actions;secrets_copied=$false;status='ENVIRONMENT_BOOTSTRAP_PASS';time=(Get-Date -Format o)}; Write-JsonFile $out (Join-Path $codex 'environment-bootstrap-result.json'); $out|ConvertTo-Json -Depth 8










