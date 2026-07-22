param(
 [Parameter(Mandatory=$true)][string]$ProjectPath,
 [Parameter(Mandatory=$true)][string[]]$IncludePaths,
 [switch]$ConfirmBaseline,
 [switch]$TestIdentity
)
$ErrorActionPreference='Stop'
Import-Module (Join-Path $PSScriptRoot '..\SafeExploration.Core.psm1') -Force
$full=Assert-ActivePath $ProjectPath
if(-not $ConfirmBaseline){[pscustomobject]@{status='PREVIEW_ONLY';project_path=$full;include_paths=$IncludePaths;command='git init -b main; git add -- <explicit paths>; git commit'}|ConvertTo-Json; exit 0}
if(-not (Test-Path -LiteralPath $full -PathType Container)){throw "项目不存在: $full"}
if(-not (Test-GitRepository $full)){& git -C $full init -b main; if($LASTEXITCODE -ne 0){throw 'git init 失败'}}
foreach($rel in $IncludePaths){if($rel -match '(^|[\\/])\.env($|\.)|\.(pem|key|pfx|p12|zip|7z|rar|mp4|mov|mkv|onnx|safetensors|ckpt)$'){throw "禁止纳入基线: $rel"}; if(-not (Test-Path -LiteralPath (Join-Path $full $rel))){throw "显式路径不存在: $rel"}}
${REDACTED_PERSONAL_DATA}
$name=(& git -C $full config user.name 2>$null|Out-String).Trim(); $email=(& git -C $full config user.email 2>$null|Out-String).Trim()
if(-not $name -or -not $email){throw 'Git 提交身份不可用。正式项目请用户配置身份；测试仓库可传 -TestIdentity。'}
& git -C $full add --dry-run -- @IncludePaths; if($LASTEXITCODE -ne 0){throw 'git add --dry-run 失败'}
& git -C $full add -- @IncludePaths; if($LASTEXITCODE -ne 0){throw 'git add 失败'}
$cached=@(& git -C $full diff --cached --name-only)
if($cached.Count -eq 0){throw '没有可提交文件'}
& git -C $full commit -m 'chore: establish safe local baseline'; if($LASTEXITCODE -ne 0){throw '基线提交失败'}
[pscustomobject]@{status='BASELINE_CREATED';project_path=$full;branch=(& git -C $full branch --show-current);head=(& git -C $full rev-parse HEAD);tracked=$cached}|ConvertTo-Json -Depth 8










