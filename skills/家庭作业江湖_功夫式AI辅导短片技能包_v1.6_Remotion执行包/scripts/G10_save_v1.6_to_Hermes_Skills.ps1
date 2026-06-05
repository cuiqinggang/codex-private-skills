$ErrorActionPreference='Stop'
Write-Host 'G10_BEGIN'
try {
    if(-not (Test-Path 'H:\')){ throw 'G10_FAIL_H_DRIVE_NOT_FOUND：没有找到 H 盘。' }
    $searchDirs=@((Join-Path $env:USERPROFILE 'Downloads'),([Environment]::GetFolderPath('Desktop')),'H:\') | Where-Object { $_ -and (Test-Path $_) }
    $zips = foreach($d in $searchDirs){
        Get-ChildItem -LiteralPath $d -Filter '*.zip' -File -ErrorAction SilentlyContinue | Where-Object { $_.Name -like '*homework_jianghu_ai_shortfilm_skill_v1.6*.zip' }
    }
    $src=$zips | Sort-Object LastWriteTime -Descending | Select-Object -First 1
    if(-not $src){ throw 'G10_FAIL_V16_ZIP_NOT_FOUND：没有找到 v1.6 执行包 zip，请先下载到 下载文件夹、桌面或 H 盘根目录。' }
    Write-Host "G10_FOUND_ZIP=$($src.FullName)"
    $actual=(Get-FileHash -Algorithm SHA256 -LiteralPath $src.FullName).Hash.ToLower()
    Write-Host "G10_SHA256=$actual"
    $destRoot='H:\Hermes_Skills'
    New-Item -ItemType Directory -Force -Path $destRoot | Out-Null
    $dest=Join-Path $destRoot '家庭作业江湖_功夫式AI辅导短片技能包_v1.6_Remotion执行包'
    if(Test-Path $dest){
        $bak="$dest.bak_$(Get-Date -Format yyyyMMdd_HHmmss)"
        Rename-Item -LiteralPath $dest -NewName (Split-Path $bak -Leaf)
        Write-Host "G10_BACKUP_OLD=$bak"
    }
    New-Item -ItemType Directory -Force -Path $dest | Out-Null
    Expand-Archive -LiteralPath $src.FullName -DestinationPath $dest -Force
    $inner=Join-Path $dest 'homework_jianghu_ai_shortfilm_skill_v1.6'
    if(Test-Path $inner){ Get-ChildItem -LiteralPath $inner -Force | Move-Item -Destination $dest -Force; Remove-Item -LiteralPath $inner -Force }
    $need=@(
        (Join-Path $dest 'SKILL.md'),
        (Join-Path $dest 'remotion\timeline_v1.6.csv'),
        (Join-Path $dest 'remotion\keyframes_manifest_v1.6.json'),
        (Join-Path $dest 'remotion\subtitle_rules_v1.6.md'),
        (Join-Path $dest 'remotion\audio_nodes_v1.6.md'),
        (Join-Path $dest 'codex\给Codex执行单_v1.6.md')
    )
    $missing=$need | Where-Object { -not (Test-Path $_) }
    if($missing.Count -gt 0){ $missing | ForEach-Object { Write-Host "MISSING=$_" }; throw 'G10_FAIL_EXTRACT_INCOMPLETE：v1.6 关键文件缺失。' }
    $imgDir='H:\Hermes_Skills\家庭作业江湖_功夫式AI辅导短片技能包_v1.5_正确关键帧图\images_full30_backup'
    if(-not(Test-Path $imgDir)){ throw "G10_FAIL_IMAGE_DIR_NOT_FOUND：找不到 v1.5 图片目录：$imgDir" }
    $imgCount=(Get-ChildItem -LiteralPath $imgDir -Filter 'KF*.png' -File | Measure-Object).Count
    if($imgCount -ne 30){ throw "G10_FAIL_IMAGE_COUNT_NOT_30：当前图片数量=$imgCount" }
    Write-Host 'G10_PASS_V16_REMOTION_PACK_SAVED'
    Write-Host "DEST=$dest"
    Write-Host "IMAGE_DIR=$imgDir"
    Write-Host "IMAGE_COUNT=$imgCount"
    Write-Host "CODEX_TASK_PATH=$(Join-Path $dest 'codex\给Codex执行单_v1.6.md')"
}
catch { Write-Host 'G10_FAIL'; Write-Host $_.Exception.Message }
finally { Write-Host 'G10_END'; Read-Host '结果已显示。看完后按回车继续' }
