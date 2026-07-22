param(
    [Parameter(Mandatory=$true)][string]$SkillPath,
    [Parameter(Mandatory=$true)][string]$WorkspacePath,
    [Parameter(Mandatory=$true)][string]$ZipPath
)
$ErrorActionPreference='Stop'
Add-Type -AssemblyName System.IO.Compression.FileSystem
$skill=[IO.Path]::GetFullPath($SkillPath);$workspace=[IO.Path]::GetFullPath($WorkspacePath);$zip=[IO.Path]::GetFullPath($ZipPath)
if($skill -match '^[Kk]:\\' -or $workspace -match '^[Kk]:\\' -or $zip -match '^[Kk]:\\'){throw '交付禁止写入 K 盘'}
if(Test-Path -LiteralPath $zip){throw "ZIP 已存在，禁止覆盖: $zip"}
$stamp=Get-Date -Format yyyyMMdd-HHmmss
$staging=Join-Path $env:LOCALAPPDATA "Temp\safe-exploration-delivery-$stamp"
$package=Join-Path $staging '完整安全探索技能包_V1.0'
$skillDst=Join-Path $package 'skill\safe-parallel-exploration-and-acceptance'
$workDst=Join-Path $package 'deployment-workspace'
New-Item -ItemType Directory -Force -Path $skillDst,$workDst|Out-Null
& robocopy $skill $skillDst /E /R:1 /W:1 /XD '.git' '__pycache__' 'node_modules' '.venv' 'venv' 'cache' /XF '*.pyc' '*.zip' '.env' '.env.*'|Out-Null
if($LASTEXITCODE -gt 7){throw "复制技能失败，robocopy=$LASTEXITCODE"}
& robocopy $workspace $workDst /E /R:1 /W:1 /XD '.git' '__pycache__' 'node_modules' '.venv' 'venv' 'outputs' 'rollback-test' 'worktrees' 'delivery-staging' /XF '*.pyc' '*.zip' '.env' '.env.*' 'dummy-model.safetensors'|Out-Null
if($LASTEXITCODE -gt 7){throw "复制工作区失败，robocopy=$LASTEXITCODE"}
$badNames=@(Get-ChildItem -LiteralPath $package -Recurse -Force|Where-Object{$_.Name -eq '.git' -or $_.Name -like '.env*' -or $_.Name -eq '__pycache__' -or $_.Extension -eq '.pyc'})
$large=@(Get-ChildItem -LiteralPath $package -Recurse -File -Force|Where-Object{$_.Length -gt 10MB})
${REDACTED_SECRET}
$secretHits=@()
Get-ChildItem -LiteralPath $package -Recurse -File -Force|Where-Object{$_.Extension -in @('.md','.txt','.json','.yaml','.yml','.toml','.ps1','.py','.js','.ts','.cmd','.csv')}|ForEach-Object{try{$m=Select-String -LiteralPath $_.FullName -Pattern $strongSecret -AllMatches -ErrorAction Stop;if($m){$secretHits+=$_.FullName}}catch{}}
if($badNames.Count -or $large.Count -or $secretHits.Count){throw "交付安全扫描失败: badNames=$($badNames.Count), large=$($large.Count), secretHits=$($secretHits.Count)"}
$files=@(Get-ChildItem -LiteralPath $package -Recurse -File -Force)
$manifest=@('# Package Manifest','',"- Created: $(Get-Date -Format o)","- File count before manifests: $($files.Count)","- Total bytes before manifests: $(($files|Measure-Object Length -Sum).Sum)",'- Excluded: .git, .env*, outputs, caches, pyc, rollback test copy, test worktrees, large dummy model.','- Original Hooks are referenced by audit hashes; global private configuration files are not packaged.')
$manifest|Set-Content -LiteralPath (Join-Path $package 'PACKAGE_MANIFEST.md') -Encoding UTF8
$hashLines=@();Get-ChildItem -LiteralPath $package -Recurse -File -Force|Sort-Object FullName|ForEach-Object{$rel=$_.FullName.Substring($package.Length+1);$h=(Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash;$hashLines+="$h *$rel"}
$hashLines|Set-Content -LiteralPath (Join-Path $package 'SHA256.txt') -Encoding UTF8
New-Item -ItemType Directory -Force -Path (Split-Path -Parent $zip)|Out-Null
Compress-Archive -LiteralPath $package -DestinationPath $zip -CompressionLevel Optimal
if(-not(Test-Path -LiteralPath $zip) -or (Get-Item -LiteralPath $zip).Length -eq 0){throw 'ZIP 不存在或为空'}
$archive=[IO.Compression.ZipFile]::OpenRead($zip);try{$entries=@($archive.Entries);$entryCount=$entries.Count;$forbidden=@($entries|Where-Object{$_.FullName -match '(^|/)\.git(/|$)|(^|/)\.env($|\.)|__pycache__|\.pyc$|dummy-model\.safetensors$'})}finally{$archive.Dispose()}
if($entryCount -eq 0 -or $forbidden.Count){throw "ZIP 内容验证失败: entries=$entryCount forbidden=$($forbidden.Count)"}
$zipHash=(Get-FileHash -LiteralPath $zip -Algorithm SHA256).Hash
$hashPath="$zip.sha256.txt";@("SHA256=$zipHash","FILE=$zip","ENTRIES=$entryCount")|Set-Content -LiteralPath $hashPath -Encoding UTF8
[pscustomobject]@{status='ZIP_VALID';zip=$zip;sha256=$zipHash;entries=$entryCount;size_bytes=(Get-Item -LiteralPath $zip).Length;content_manifest=(Join-Path $package 'SHA256.txt');external_checksum=$hashPath;staging=$staging;forbidden_entries=$forbidden.Count}|ConvertTo-Json -Depth 8


