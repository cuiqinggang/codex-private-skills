param(
  [string]$OutDir = "C:\Users\A\Desktop\834-c-drive-final-cleanup",
  [string]$ZipPath = "C:\Users\A\Desktop\834.zip"
)

$ErrorActionPreference = "Continue"
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

$BeforePath = Join-Path $OutDir "834-before.txt"
$AfterPath = Join-Path $OutDir "834-after.txt"
$FinalReportPath = Join-Path $OutDir "834-final-report.md"
$DeletedComfyPath = Join-Path $OutDir "834-deleted-comfyui-installers.txt"
$HibernationPath = Join-Path $OutDir "834-hibernation.txt"
$DockerBeforePath = Join-Path $OutDir "834-docker-before.txt"
$DockerVolumePrunePath = Join-Path $OutDir "834-docker-after-volume-prune.txt"
$DockerAllPrunePath = Join-Path $OutDir "834-docker-after-all-prune.txt"
$DockerValidationPath = Join-Path $OutDir "834-docker-validation.txt"
$OpenWebuiInspectPath = Join-Path $OutDir "834-open-webui-clean-inspect.json"
$OpenWebuiMountsPath = Join-Path $OutDir "834-open-webui-mounts.md"
$VolumeListPath = Join-Path $OutDir "834-volume-list.txt"
$VolumeSizePath = Join-Path $OutDir "834-volume-size-report.txt"
$DownloadsCleanupPath = Join-Path $OutDir "834-downloads-cleanup.txt"
$NextConfirmPath = Join-Path $OutDir "834-next-confirm-list.md"
$InstallersReviewCsv = Join-Path $OutDir "834-installers-archives-review-list.csv"
$CacheCleanupPath = Join-Path $OutDir "834-cache-cleanup.txt"
$RecycleCleanupPath = Join-Path $OutDir "834-recycle-cleanup.txt"
$DeletedInstallersPath = Join-Path $OutDir "834-deleted-installers.txt"
$ProtectedCheckPath = Join-Path $OutDir "834-protected-check.txt"
$CompactScriptPath = Join-Path $OutDir "compact-docker-vhdx.txt"

$DockerRoot = "C:\Users\A\AppData\Local\Docker"
$DockerVhdx = "C:\Users\A\AppData\Local\Docker\wsl\disk\docker_data.vhdx"
$ComfyRoot = "C:\Users\A\Desktop\ComfyUI-aki(3)"

function Get-FileGB {
  param([string]$Path)
  if (Test-Path -LiteralPath $Path) {
    return [math]::Round((Get-Item -LiteralPath $Path -Force).Length / 1GB, 3)
  }
  return 0
}

function Get-DirGB {
  param([string]$Path)
  if (-not (Test-Path -LiteralPath $Path)) { return 0 }
  $sum = (Get-ChildItem -LiteralPath $Path -Recurse -Force -File -ErrorAction SilentlyContinue | Measure-Object Length -Sum).Sum
  if ($null -eq $sum) { return 0 }
  return [math]::Round($sum / 1GB, 3)
}

function Get-CDrive {
  $d = Get-CimInstance Win32_LogicalDisk -Filter "DeviceID='C:'"
  [pscustomobject]@{
    SizeGB = [math]::Round($d.Size / 1GB, 3)
    FreeGB = [math]::Round($d.FreeSpace / 1GB, 3)
    UsedGB = [math]::Round(($d.Size - $d.FreeSpace) / 1GB, 3)
  }
}

function Add-Section {
  param([string]$Path, [string]$Title)
  Add-Content -LiteralPath $Path -Value ""
  Add-Content -LiteralPath $Path -Value "===== $Title ====="
}

function Run-Capture {
  param([string]$Path, [string]$Title, [scriptblock]$Block)
  Add-Section -Path $Path -Title $Title
  try {
    $r = & $Block 2>&1
    if ($null -eq $r) { Add-Content -LiteralPath $Path -Value "(no output)" }
    else { $r | Out-String -Width 260 | Add-Content -LiteralPath $Path }
  } catch {
    Add-Content -LiteralPath $Path -Value ("ERROR: " + $_.Exception.Message)
  }
}

function Get-ChildTop {
  param([string]$Path, [int]$Top = 50)
  if (-not (Test-Path -LiteralPath $Path)) { return @() }
  Get-ChildItem -LiteralPath $Path -Force -ErrorAction SilentlyContinue |
    ForEach-Object {
      if ($_.PSIsContainer) {
        [pscustomobject]@{ GB = Get-DirGB $_.FullName; Type = "dir"; Path = $_.FullName; LastWriteTime = $_.LastWriteTime }
      } else {
        [pscustomobject]@{ GB = [math]::Round($_.Length / 1GB, 3); Type = "file"; Path = $_.FullName; LastWriteTime = $_.LastWriteTime }
      }
    } | Sort-Object GB -Descending | Select-Object -First $Top
}

function Clear-DirectoryContents {
  param([string]$Path)
  $before = Get-DirGB $Path
  if (Test-Path -LiteralPath $Path) {
    Get-ChildItem -LiteralPath $Path -Force -ErrorAction SilentlyContinue |
      ForEach-Object {
        Remove-Item -LiteralPath $_.FullName -Recurse -Force -ErrorAction SilentlyContinue
      }
  }
  $after = Get-DirGB $Path
  [pscustomobject]@{ Path=$Path; BeforeGB=$before; AfterGB=$after; FreedGB=[math]::Round($before-$after,3) }
}

function Wait-Docker {
  param([int]$Seconds = 180)
  $deadline = (Get-Date).AddSeconds($Seconds)
  while ((Get-Date) -lt $deadline) {
    docker ps *> $null
    if ($LASTEXITCODE -eq 0) { return $true }
    Start-Sleep -Seconds 5
  }
  return $false
}

function Start-DockerDesktop {
  $exe = "C:\Program Files\Docker\Docker\Docker Desktop.exe"
  if (Test-Path -LiteralPath $exe) {
    Start-Process -FilePath $exe -WindowStyle Hidden
  }
}

function Test-ContainerHealthy {
  param([string]$Name)
  $status = docker ps --filter "name=$Name" --format "{{.Status}}" 2>$null
  return ($status -match "healthy")
}

$beforeDrive = Get-CDrive
$beforeHiberGB = Get-FileGB "C:\hiberfil.sys"
$beforeDockerRootGB = Get-DirGB $DockerRoot
$beforeDockerVhdxGB = Get-FileGB $DockerVhdx

Set-Content -LiteralPath $BeforePath -Value "834 before state - $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
Run-Capture $BeforePath "C drive" { $beforeDrive | Format-List }
Run-Capture $BeforePath "Key sizes" {
  [pscustomobject]@{
    HiberfilGB = $beforeHiberGB
    DockerRootGB = $beforeDockerRootGB
    DockerDataVhdxGB = $beforeDockerVhdxGB
    ComfyUIAki3GB = Get-DirGB $ComfyRoot
    Desktop4GB = Get-DirGB "C:\Users\A\Desktop\4"
    UserTempGB = Get-DirGB "C:\Users\A\AppData\Local\Temp"
    WindowsTempGB = Get-DirGB "C:\Windows\Temp"
    UvGB = Get-DirGB "C:\Users\A\AppData\Local\uv"
    DownloadsGB = Get-DirGB "C:\Users\A\Downloads"
  } | Format-List
}
Run-Capture $BeforePath "Desktop direct children" { Get-ChildItem -LiteralPath "C:\Users\A\Desktop" -Force -ErrorAction SilentlyContinue | Select-Object Name,PSIsContainer,Length,LastWriteTime | Format-Table -AutoSize }
Run-Capture $BeforePath "AppData Local direct children" { Get-ChildItem -LiteralPath "C:\Users\A\AppData\Local" -Force -ErrorAction SilentlyContinue | Select-Object Name,PSIsContainer,Length,LastWriteTime | Format-Table -AutoSize }

Set-Content -LiteralPath $DeletedComfyPath -Value "834 deleted ComfyUI installer archives - $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
$deletedComfyGB = 0
if (Test-Path -LiteralPath $ComfyRoot) {
  $comfyTargets = Get-ChildItem -LiteralPath $ComfyRoot -Recurse -Force -File -Filter "ComfyUI-aki-v*.7z" -ErrorAction SilentlyContinue
  foreach ($file in $comfyTargets) {
    $gb = [math]::Round($file.Length / 1GB, 3)
    Add-Content -LiteralPath $DeletedComfyPath -Value "$gb GB`t$($file.FullName)"
    Remove-Item -LiteralPath $file.FullName -Force -ErrorAction SilentlyContinue
    $deletedComfyGB += $gb
  }
}

Set-Content -LiteralPath $HibernationPath -Value "834 hibernation - $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
Add-Content -LiteralPath $HibernationPath -Value "Before hiberfil.sys GB: $beforeHiberGB"
Run-Capture $HibernationPath "powercfg /h off" { powercfg /h off }
Start-Sleep -Seconds 3
$afterHiberGB = Get-FileGB "C:\hiberfil.sys"
Add-Content -LiteralPath $HibernationPath -Value "After hiberfil.sys GB: $afterHiberGB"

Set-Content -LiteralPath $DockerBeforePath -Value "834 docker before - $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
Run-Capture $DockerBeforePath "docker version" { docker version }
Run-Capture $DockerBeforePath "docker info" { docker info }
Run-Capture $DockerBeforePath "docker system df -v" { docker system df -v }
Run-Capture $DockerBeforePath "docker ps -a" { docker ps -a }
Run-Capture $DockerBeforePath "docker images -a" { docker images -a }
Run-Capture $DockerBeforePath "docker volume ls" { docker volume ls }
Run-Capture $DockerBeforePath "docker network ls" { docker network ls }
Run-Capture $DockerBeforePath "wsl -l -v" { wsl -l -v }

docker inspect open-webui-clean | Set-Content -LiteralPath $OpenWebuiInspectPath -Encoding UTF8
$openWebuiVolumes = @()
try {
  $inspect = Get-Content -LiteralPath $OpenWebuiInspectPath -Raw | ConvertFrom-Json
  $mountLines = New-Object System.Collections.Generic.List[string]
  $mountLines.Add("# Open WebUI mounts")
  $mountLines.Add("")
  $mountLines.Add("- Name: $($inspect.Name)")
  $mountLines.Add("- Image: $($inspect.Config.Image)")
  $mountLines.Add("- Status: $($inspect.State.Status)")
  $mountLines.Add("- Health: $($inspect.State.Health.Status)")
  $mountLines.Add("")
  $mountLines.Add("| Type | Name | Source | Destination |")
  $mountLines.Add("|---|---|---|---|")
  foreach ($m in @($inspect.Mounts)) {
    $mountLines.Add("| $($m.Type) | $($m.Name) | $($m.Source) | $($m.Destination) |")
    if ($m.Type -eq "volume" -and $m.Name) { $openWebuiVolumes += $m.Name }
  }
  $mountLines | Set-Content -LiteralPath $OpenWebuiMountsPath -Encoding UTF8
} catch {
  "Failed to parse open-webui inspect: $($_.Exception.Message)" | Set-Content -LiteralPath $OpenWebuiMountsPath -Encoding UTF8
}

docker volume ls -q | Set-Content -LiteralPath $VolumeListPath -Encoding UTF8
Set-Content -LiteralPath $VolumeSizePath -Value "834 volume size report - $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
Run-Capture $VolumeSizePath "docker system df -v" { docker system df -v }

Set-Content -LiteralPath $DockerVolumePrunePath -Value "834 docker volume prune - $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
Run-Capture $DockerVolumePrunePath "before docker system df -v" { docker system df -v }
Run-Capture $DockerVolumePrunePath "before docker volume ls" { docker volume ls }
$volumesBefore = @(docker volume ls -q 2>$null)
Run-Capture $DockerVolumePrunePath "docker volume prune -f" { docker volume prune -f }
$volumesAfter = @(docker volume ls -q 2>$null)
$deletedVolumes = @($volumesBefore | Where-Object { $volumesAfter -notcontains $_ })
Run-Capture $DockerVolumePrunePath "after docker system df -v" { docker system df -v }
Run-Capture $DockerVolumePrunePath "after docker volume ls" { docker volume ls }

Set-Content -LiteralPath $DockerAllPrunePath -Value "834 docker after all prune - $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
Run-Capture $DockerAllPrunePath "docker container prune -f" { docker container prune -f }
Run-Capture $DockerAllPrunePath "docker image prune -a -f" { docker image prune -a -f }
Run-Capture $DockerAllPrunePath "docker builder prune -a -f" { docker builder prune -a -f }
Run-Capture $DockerAllPrunePath "docker network prune -f" { docker network prune -f }
Run-Capture $DockerAllPrunePath "docker system df -v" { docker system df -v }
Run-Capture $DockerAllPrunePath "docker ps -a" { docker ps -a }
Run-Capture $DockerAllPrunePath "docker images -a" { docker images -a }
Run-Capture $DockerAllPrunePath "docker volume ls" { docker volume ls }

$vhdxBeforeCompactGB = Get-FileGB $DockerVhdx
Run-Capture $DockerAllPrunePath "wsl --shutdown" { wsl --shutdown }
Start-Sleep -Seconds 5
@(
  "select vdisk file=""$DockerVhdx""",
  "attach vdisk readonly",
  "compact vdisk",
  "detach vdisk",
  "exit"
) | Set-Content -LiteralPath $CompactScriptPath -Encoding ASCII
if (Get-Command Optimize-VHD -ErrorAction SilentlyContinue) {
  Run-Capture $DockerAllPrunePath "Optimize-VHD" { Optimize-VHD -Path $DockerVhdx -Mode Full }
} else {
  Run-Capture $DockerAllPrunePath "diskpart compact vdisk" { diskpart /s $CompactScriptPath }
}
$vhdxAfterCompactGB = Get-FileGB $DockerVhdx

Start-DockerDesktop
$dockerReady = Wait-Docker 180
if (-not (Test-ContainerHealthy "open-webui-clean")) {
  Start-Sleep -Seconds 30
}
$openWebuiHealthy = Test-ContainerHealthy "open-webui-clean"

Set-Content -LiteralPath $DockerValidationPath -Value "834 docker validation - $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
Run-Capture $DockerValidationPath "docker ps -a" { docker ps -a }
Run-Capture $DockerValidationPath "docker inspect open-webui-clean" { docker inspect open-webui-clean }
Run-Capture $DockerValidationPath "docker logs --tail 80 open-webui-clean" { docker logs --tail 80 open-webui-clean }
Add-Content -LiteralPath $DockerValidationPath -Value "DockerReady=$dockerReady"
Add-Content -LiteralPath $DockerValidationPath -Value "OpenWebUIHealthy=$openWebuiHealthy"
Add-Content -LiteralPath $DockerValidationPath -Value "OpenWebUIVolumes=$($openWebuiVolumes -join ', ')"
Add-Content -LiteralPath $DockerValidationPath -Value "DeletedVolumes=$($deletedVolumes -join ', ')"

$cacheTargets = @(
  "C:\Users\A\AppData\Local\Temp",
  "C:\Windows\Temp",
  "C:\ProgramData\Microsoft\Windows\WER",
  "C:\Users\A\AppData\Local\pip\Cache",
  "C:\Users\A\AppData\Local\npm-cache",
  "C:\Users\A\AppData\Local\uv\cache",
  "C:\Users\A\AppData\Local\Google\Chrome\User Data\Default\Cache",
  "C:\Users\A\AppData\Local\Google\Chrome\User Data\Default\Code Cache",
  "C:\Users\A\AppData\Local\Google\Chrome\User Data\Default\GPUCache",
  "C:\Users\A\AppData\Local\Microsoft\Edge\User Data\Default\Cache",
  "C:\Users\A\AppData\Local\Microsoft\Edge\User Data\Default\Code Cache",
  "C:\Users\A\AppData\Local\Microsoft\Edge\User Data\Default\GPUCache"
)
Set-Content -LiteralPath $CacheCleanupPath -Value "834 cache cleanup - $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
$cacheFreedGB = 0
foreach ($target in $cacheTargets) {
  $r = Clear-DirectoryContents $target
  $cacheFreedGB += $r.FreedGB
  Add-Content -LiteralPath $CacheCleanupPath -Value "$($r.FreedGB) GB freed`t$($r.BeforeGB) -> $($r.AfterGB)`t$($r.Path)"
}

Set-Content -LiteralPath $RecycleCleanupPath -Value "834 recycle cleanup - $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
$recycleBefore = Get-DirGB "C:\`$Recycle.Bin"
Clear-RecycleBin -Force -ErrorAction SilentlyContinue
$recycleAfter = Get-DirGB "C:\`$Recycle.Bin"
Add-Content -LiteralPath $RecycleCleanupPath -Value "RecycleBinGB: $recycleBefore -> $recycleAfter"

Set-Content -LiteralPath $DownloadsCleanupPath -Value "834 downloads cleanup - $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
$downloadsRepack = "C:\Users\A\Downloads\codex-msix-repack"
$downloadsDeletedGB = 0
if (Test-Path -LiteralPath $downloadsRepack) {
  $protected = Get-ChildItem -LiteralPath $downloadsRepack -Recurse -Force -File -ErrorAction SilentlyContinue |
    Where-Object { $_.Extension -match '^\.(md|txt|png|jpg|jpeg|webp|mp4|mov|avi|ps1|py|json|yaml|yml|toml)$' -or $_.FullName -match 'skill|report|image|video' }
  if (@($protected).Count -eq 0) {
    $downloadsDeletedGB = Get-DirGB $downloadsRepack
    Add-Content -LiteralPath $DownloadsCleanupPath -Value "Deleted codex-msix-repack: $downloadsDeletedGB GB"
    Remove-Item -LiteralPath $downloadsRepack -Recurse -Force -ErrorAction SilentlyContinue
  } else {
    Add-Content -LiteralPath $DownloadsCleanupPath -Value "NOT DELETED: protected-looking files found."
    $protected | Select-Object FullName,Length,LastWriteTime | Format-Table -AutoSize | Out-String -Width 240 | Add-Content -LiteralPath $DownloadsCleanupPath
  }
} else {
  Add-Content -LiteralPath $DownloadsCleanupPath -Value "MISSING: $downloadsRepack"
}

Set-Content -LiteralPath $DeletedInstallersPath -Value "834 deleted installers - $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
$feishuInstaller = "C:\Users\A\Desktop\Feishu-win32_x64-7.68.6-signed.exe"
$deletedFeishuGB = 0
if (Test-Path -LiteralPath $feishuInstaller) {
  $deletedFeishuGB = Get-FileGB $feishuInstaller
  Add-Content -LiteralPath $DeletedInstallersPath -Value "$deletedFeishuGB GB`t$feishuInstaller"
  Remove-Item -LiteralPath $feishuInstaller -Force -ErrorAction SilentlyContinue
} else {
  Add-Content -LiteralPath $DeletedInstallersPath -Value "MISSING`t$feishuInstaller"
}
Add-Content -LiteralPath $DeletedInstallersPath -Value "PROTECTED`tC:\Users\A\Desktop\FlClash-0.8.92-windows-amd64-setup.exe"

$reviewExt = @("*.exe","*.msi","*.7z","*.zip","*.rar","*.tar","*.gz","*.iso")
$reviewRows = foreach ($root in @("C:\Users\A\Desktop","C:\Users\A\Downloads")) {
  if (Test-Path -LiteralPath $root) {
    foreach ($pattern in $reviewExt) {
      Get-ChildItem -LiteralPath $root -Filter $pattern -Recurse -Force -File -ErrorAction SilentlyContinue |
        ForEach-Object {
          $judgment = "NEEDS_CONFIRM"
          $reason = "archive/installer not explicitly approved"
          if ($_.FullName -eq "C:\Users\A\Desktop\FlClash-0.8.92-windows-amd64-setup.exe") { $judgment="PROTECTED"; $reason="network proxy related" }
          [pscustomobject]@{
            Path=$_.FullName
            Name=$_.Name
            SizeGB=[math]::Round($_.Length/1GB,3)
            Extension=$_.Extension
            LastWriteTime=$_.LastWriteTime
            Judgment=$judgment
            Reason=$reason
          }
        }
    }
  }
}
$reviewRows | Export-Csv -LiteralPath $InstallersReviewCsv -NoTypeInformation -Encoding UTF8

Set-Content -LiteralPath $NextConfirmPath -Value "# 834 Next Manual Confirm List"
$manualConfirmDirs = @(
  "C:\Users\A\Desktop\1",
  "C:\Users\A\Desktop\SD_Recovered",
  "C:\Users\A\Desktop\ClaudeCode_Outputs",
  "C:\Users\A\Desktop\CODEX_MAIN_NATIVE_GPT55_PROTECTION_SNAPSHOT_20260620_202852_DO_NOT_DELETE",
  "C:\Users\A\Desktop\coordinate-method-real-browser-test-v3",
  "C:\Users\A\Desktop\bridge_tests",
  "C:\Users\A\Desktop\bridge_v2_live_test"
)
foreach ($p in $manualConfirmDirs) {
  Add-Content -LiteralPath $NextConfirmPath -Value "- $(Get-DirGB $p) GB - $p"
}

$afterDrive = Get-CDrive
$afterDockerRootGB = Get-DirGB $DockerRoot
$afterDockerVhdxGB = Get-FileGB $DockerVhdx
$afterHiberGB = Get-FileGB "C:\hiberfil.sys"
$releasedGB = [math]::Round($afterDrive.FreeGB - $beforeDrive.FreeGB, 3)

Set-Content -LiteralPath $AfterPath -Value "834 after state - $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
Run-Capture $AfterPath "C drive after" { $afterDrive | Format-List }
Run-Capture $AfterPath "cleanup summary" {
  [pscustomobject]@{
    ReleasedGB=$releasedGB
    HiberfilBeforeGB=$beforeHiberGB
    HiberfilAfterGB=$afterHiberGB
    DockerRootBeforeGB=$beforeDockerRootGB
    DockerRootAfterGB=$afterDockerRootGB
    DockerDataVhdxBeforeGB=$beforeDockerVhdxGB
    DockerDataVhdxAfterGB=$afterDockerVhdxGB
    DockerVolumesDeletedCount=@($deletedVolumes).Count
    DockerVolumesDeleted=($deletedVolumes -join ", ")
    OpenWebUIHealthy=$openWebuiHealthy
    ComfyUIAki3Exists=(Test-Path -LiteralPath $ComfyRoot)
    Desktop4Exists=(Test-Path -LiteralPath "C:\Users\A\Desktop\4")
    CodexExists=(Test-Path -LiteralPath "C:\Users\A\.codex")
    CodexDocumentsExists=(Test-Path -LiteralPath "C:\Users\A\Documents\Codex")
    ProxyInstallerProtected=(Test-Path -LiteralPath "C:\Users\A\Desktop\FlClash-0.8.92-windows-amd64-setup.exe")
  } | Format-List
}

Set-Content -LiteralPath $ProtectedCheckPath -Value "834 protected check - $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
@(
  "C:\Windows",
  "C:\Program Files",
  "C:\Program Files (x86)",
  "C:\ProgramData",
  "C:\pagefile.sys",
  "C:\swapfile.sys",
  "C:\Users\A\.codex",
  "C:\Users\A\Documents\Codex",
  "C:\Users\A\Desktop\4",
  "C:\Users\A\Desktop\ComfyUI-aki(3)\controlnet",
  "C:\Users\A\Desktop\ComfyUI-aki(3)\模型",
  "C:\Users\A\Desktop\FlClash-0.8.92-windows-amd64-setup.exe"
) | ForEach-Object {
  Add-Content -LiteralPath $ProtectedCheckPath -Value "$([bool](Test-Path -LiteralPath $_))`t$_"
}

$finalLines = New-Object System.Collections.Generic.List[string]
$finalLines.Add("# 834 C Drive Final Cleanup Report")
$finalLines.Add("")
$finalLines.Add("Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')")
$finalLines.Add("")
$finalLines.Add("## Purpose")
$finalLines.Add("Clean explicit installers, old archives, caches, Docker unused volumes, and hibernation storage while preserving Windows, proxy tools, Codex, skills, ComfyUI models/workflows, Desktop\4 models, and Open WebUI.")
$finalLines.Add("")
$finalLines.Add("## C Drive State")
$finalLines.Add("- Before: used $($beforeDrive.UsedGB) GB, free $($beforeDrive.FreeGB) GB, total $($beforeDrive.SizeGB) GB.")
$finalLines.Add("- After: used $($afterDrive.UsedGB) GB, free $($afterDrive.FreeGB) GB, total $($afterDrive.SizeGB) GB.")
$finalLines.Add("- Released: $releasedGB GB.")
$finalLines.Add("")
$finalLines.Add("## Deleted Or Cleaned")
$finalLines.Add("- Explicit ComfyUI old installer archives: $([math]::Round($deletedComfyGB,3)) GB.")
$finalLines.Add("- Feishu installer: $deletedFeishuGB GB.")
$finalLines.Add("- Downloads codex-msix-repack: $downloadsDeletedGB GB.")
$finalLines.Add("- Cache directories: $([math]::Round($cacheFreedGB,3)) GB.")
$finalLines.Add("- Recycle Bin: $([math]::Round($recycleBefore-$recycleAfter,3)) GB.")
$finalLines.Add("- Docker unused volumes deleted: $(@($deletedVolumes).Count); names: $($deletedVolumes -join ', ').")
$finalLines.Add("")
$finalLines.Add("## Docker")
$finalLines.Add("- Docker root: $beforeDockerRootGB GB -> $afterDockerRootGB GB.")
$finalLines.Add("- docker_data.vhdx: $beforeDockerVhdxGB GB -> $afterDockerVhdxGB GB.")
$finalLines.Add("- VHDX compact: $vhdxBeforeCompactGB GB -> $vhdxAfterCompactGB GB.")
$finalLines.Add("- Open WebUI healthy: $openWebuiHealthy.")
$finalLines.Add("")
$finalLines.Add("## Protected Items")
$finalLines.Add("- ComfyUI-aki(3) exists: $(Test-Path -LiteralPath $ComfyRoot).")
$finalLines.Add("- Desktop\4 exists: $(Test-Path -LiteralPath 'C:\Users\A\Desktop\4').")
$finalLines.Add("- ComfyUI controlnet exists: $(Test-Path -LiteralPath 'C:\Users\A\Desktop\ComfyUI-aki(3)\controlnet').")
$finalLines.Add("- Codex home exists: $(Test-Path -LiteralPath 'C:\Users\A\.codex').")
$finalLines.Add("- Codex documents exist: $(Test-Path -LiteralPath 'C:\Users\A\Documents\Codex').")
$finalLines.Add("- FlClash installer protected: $(Test-Path -LiteralPath 'C:\Users\A\Desktop\FlClash-0.8.92-windows-amd64-setup.exe').")
$finalLines.Add("- Browser profile directories were not deleted; only Cache/Code Cache/GPUCache children were cleaned.")
$finalLines.Add("")
$finalLines.Add("## Hibernation")
$finalLines.Add("- hiberfil.sys: $beforeHiberGB GB -> $afterHiberGB GB.")
$finalLines.Add("")
$finalLines.Add("## Next Manual Confirmation")
$finalLines.Add("- Desktop historical projects and protection snapshots were only listed, not deleted.")
$finalLines.Add("- Non-explicit zip/exe/msi/iso files were written to 834-installers-archives-review-list.csv.")
$finalLines.Add("- For more slimming, manually review Desktop historical projects, ComfyUI old-version folder, and remaining Downloads archives.")
$finalLines | Set-Content -LiteralPath $FinalReportPath -Encoding UTF8

if (Test-Path -LiteralPath $ZipPath) { Remove-Item -LiteralPath $ZipPath -Force }
$files = Get-ChildItem -LiteralPath $OutDir -File | Select-Object -ExpandProperty FullName
Compress-Archive -LiteralPath $files -DestinationPath $ZipPath -Force

[pscustomobject]@{
  Zip = $ZipPath
  BeforeUsedGB = $beforeDrive.UsedGB
  BeforeFreeGB = $beforeDrive.FreeGB
  AfterUsedGB = $afterDrive.UsedGB
  AfterFreeGB = $afterDrive.FreeGB
  ReleasedGB = $releasedGB
  HiberfilBeforeGB = $beforeHiberGB
  HiberfilAfterGB = $afterHiberGB
  DockerRootBeforeGB = $beforeDockerRootGB
  DockerRootAfterGB = $afterDockerRootGB
  DockerVhdxBeforeGB = $beforeDockerVhdxGB
  DockerVhdxAfterGB = $afterDockerVhdxGB
  DeletedDockerVolumes = @($deletedVolumes).Count
  OpenWebUIHealthy = $openWebuiHealthy
}
