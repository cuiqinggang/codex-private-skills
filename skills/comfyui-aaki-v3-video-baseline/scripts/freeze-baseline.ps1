param(
  [Parameter(Mandatory=$true)]
  [string]$RunDir,
  [string]$Root = 'C:\AI\ComfyUI_Aaki_v3'
)

$ErrorActionPreference = 'Stop'
$Comfy = Join-Path $Root 'ComfyUI'
$Backup = Join-Path $RunDir 'G01_BASELINE_FROZEN'
New-Item -ItemType Directory -Force -Path $Backup | Out-Null

${REDACTED_SECRET}
$ServerPid = if (Test-Path -LiteralPath $PidPath) { [int](Get-Content -LiteralPath $PidPath -TotalCount 1) } else { $null }
$ServerProc = if ($ServerPid) { Get-Process -Id $ServerPid -ErrorAction SilentlyContinue } else { $null }

$PyCode = @'
import json, sys, torch
out = {
  "python_executable": sys.executable,
  "python_version": sys.version,
  "torch_version": torch.__version__,
  "torch_cuda_version": torch.version.cuda,
  "cuda_available": torch.cuda.is_available(),
  "cuda_device_count": torch.cuda.device_count(),
  "cuda_current_device": torch.cuda.current_device() if torch.cuda.is_available() else None,
  "cuda_device_name": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
  "cuda_capability": torch.cuda.get_device_capability(0) if torch.cuda.is_available() else None,
  "cuda_total_memory_mib": round(torch.cuda.get_device_properties(0).total_memory / 1024 / 1024) if torch.cuda.is_available() else None,
}
print(json.dumps(out, ensure_ascii=False, indent=2))
'@

$PythonProbe = & (Join-Path $Root 'python\python.exe') -c $PyCode
$Gpu = & nvidia-smi --query-gpu=name,driver_version,memory.total,memory.used,memory.free,compute_cap --format=csv,noheader,nounits

$GitExe = Join-Path $Root 'git\cmd\git.exe'
$GitInfo = [pscustomobject]@{
  ShortHash = (& $GitExe -C $Comfy rev-parse --short HEAD 2>$null)
  FullHash = (& $GitExe -C $Comfy rev-parse HEAD 2>$null)
  CommitDate = (& $GitExe -C $Comfy log -1 --format=%ci 2>$null)
  Subject = (& $GitExe -C $Comfy log -1 --format=%s 2>$null)
}

[pscustomobject]@{
  Gate = 'G01_BASELINE_FROZEN'
  CreatedAt = (Get-Date).ToString('yyyy-MM-dd HH:mm:ss K')
  InstallRoot = $Root
  ComfyUIRoot = $Comfy
  StartWorkingDirectory = $Root
  StartCommand = "$Root\python\python.exe -s ComfyUI\main.py --windows-standalone-build --port 8188 --output-directory D:\AI_ComfyUI_Outputs\ComfyUI_Aaki_v3\output --input-directory D:\AI_ComfyUI_Outputs\ComfyUI_Aaki_v3\input --temp-directory D:\AI_ComfyUI_Outputs\ComfyUI_Aaki_v3\temp"
  Url = 'http://127.0.0.1:8188/'
  ServerPid = $ServerPid
  ServerRunning = ($null -ne $ServerProc)
  ServerProcessName = if ($ServerProc) { $ServerProc.ProcessName } else { $null }
  PythonTorchCuda = ($PythonProbe | ConvertFrom-Json)
  NvidiaSmiCsv = $Gpu
  ComfyUIGit = $GitInfo
} | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $Backup 'baseline.json') -Encoding UTF8

Get-ChildItem -LiteralPath (Join-Path $Comfy 'custom_nodes') -Directory -ErrorAction SilentlyContinue |
  Sort-Object Name |
  Select-Object Name,FullName,LastWriteTime |
  ConvertTo-Json -Depth 4 |
  Set-Content -LiteralPath (Join-Path $Backup 'custom_nodes-list.json') -Encoding UTF8

if (Test-Path -LiteralPath (Join-Path $Comfy 'models')) {
  Get-ChildItem -LiteralPath (Join-Path $Comfy 'models') -Recurse -Force -ErrorAction SilentlyContinue |
    Select-Object FullName,Mode,Length,LastWriteTime |
    ConvertTo-Json -Depth 4 |
    Set-Content -LiteralPath (Join-Path $Backup 'models-tree.json') -Encoding UTF8
}

Write-Output "G01_BASELINE_FROZEN $Backup"
