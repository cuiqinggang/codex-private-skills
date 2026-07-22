param([Parameter(Mandatory=$true)][string]$ProjectPath,[string]$OutputPath='')
$ErrorActionPreference='Stop'; Import-Module (Join-Path $PSScriptRoot '..\SafeExploration.Core.psm1') -Force; $p=Resolve-SafeFullPath $ProjectPath; $types=@(Get-ProjectEnvironment $p)
$result=[ordered]@{schema_version='1.0';project_path=$p;project_type=($types -join '+');runtime='';runtime_version='';dependency_files=@(Get-ChildItem -LiteralPath $p -File -ErrorAction SilentlyContinue|Where-Object {$_.Name-in @('pyproject.toml','requirements.txt','uv.lock','poetry.lock','package.json','package-lock.json','pnpm-lock.yaml','yarn.lock','Cargo.toml')}|ForEach-Object {$_.Name});bootstrap_command='';verify_command='';test_command='';build_command='';required_local_files=@();ignored_secret_files=@('.env','.env.*','*.key','*.pem');generated_directories=@('node_modules','.venv','dist','build','cache');worktree_ready=$false}
if($OutputPath){Write-JsonFile $result (Resolve-SafeFullPath $OutputPath)}; $result|ConvertTo-Json -Depth 8










