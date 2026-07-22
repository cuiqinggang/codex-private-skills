param([Parameter(Mandatory=$true)][string]$ProjectPath,[string]$OutputPath='')
$ErrorActionPreference='Stop'
Import-Module (Join-Path $PSScriptRoot '..\SafeExploration.Core.psm1') -Force
$full=Assert-ActivePath $ProjectPath
if(-not (Test-Path -LiteralPath $full -PathType Container)){throw "项目不存在: $full"}
$files=@(Get-ChildItem -LiteralPath $full -Recurse -File -Force -ErrorAction SilentlyContinue | Where-Object {$_.FullName -notmatch '\\(\.git|node_modules|\.venv|venv|__pycache__|dist|build|cache|outputs|backups)(\\|$)'})
$sensitive=@(Get-SensitiveFileRisks $full); $large=@(Get-LargeFileRisks $full 10)
$riskPaths=@($sensitive.path)+@($large.path)
$track=@($files | Where-Object {$riskPaths -notcontains $_.FullName -and $_.Extension -notin @('.zip','.7z','.rar','.mp4','.mov','.mkv','.avi','.wav','.mp3','.onnx','.safetensors','.ckpt')} | ForEach-Object {$_.FullName.Substring($full.Length).TrimStart('\')})
$result=[ordered]@{schema_version='1.0';status='PREVIEW_ONLY';project_path=$full;total_size_bytes=($files|Measure-Object Length -Sum).Sum;proposed_track_files=$track;excluded_risk_paths=$riskPaths;requires_confirm_baseline=$true}
if($OutputPath){Write-JsonFile $result (Resolve-SafeFullPath $OutputPath)}
$result|ConvertTo-Json -Depth 20










