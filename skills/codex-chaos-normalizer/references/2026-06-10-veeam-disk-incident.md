# 2026-06-10 Veeam And Stale Task Disk Incident

Use this note when the user says the computer disk keeps making noise, CPU/disk is active with no visible work, or Codex seems idle but the machine is busy.

## Confirmed Incident

Date: 2026-06-10.

Symptoms:

- User heard constant disk activity while no intended task was running.
- Initial disk sample showed `C:` activity around `1 MB/s` with queue length `1`.
- Some process queries timed out, which itself indicated the machine was under load.

Confirmed load sources:

- Stale all-drive search:
  `rg.exe -i --hidden ... obsidian:// C:\`
- Stale local preview/check processes:
  `python.exe -m http.server` on ports `4178`, `4181`, `4182`, plus `build_obsidian_app_discovery_gate.py`.
- Docker Windmill project containers:
  `ai-company-windmill-local-mvp-server`, `ai-company-windmill-local-mvp-worker-native`, `ai-company-windmill-local-mvp-db`.
- Veeam Agent automatic system-image backup:
  job name `Windows System Volume Image to H`, service `VeeamEndpointBackupSvc`, target folder `H:\SYSTEM_IMAGE_VEEAM_20260520`.

## What Worked

Use targeted process and disk checks before stopping anything:

```powershell
Get-CimInstance Win32_PerfFormattedData_PerfDisk_PhysicalDisk |
  Select-Object Name,PercentDiskTime,CurrentDiskQueueLength,
    @{n='Disk_MBps';e={[math]::Round($_.DiskBytesPersec/1MB,2)}},
    @{n='Read_MBps';e={[math]::Round($_.DiskReadBytesPersec/1MB,2)}},
    @{n='Write_MBps';e={[math]::Round($_.DiskWriteBytesPersec/1MB,2)}}
```

```powershell
wmic process get ProcessId,Name,KernelModeTime,UserModeTime,WorkingSetSize,CommandLine /format:csv |
  findstr /i "rg.exe http.server build_obsidian docker veeam wsl python.exe codex.exe"
```

```powershell
Get-CimInstance Win32_PerfFormattedData_PerfProc_Process |
  Where-Object { $_.Name -ne '_Total' -and $_.Name -ne 'Idle' -and $_.IODataBytesPersec -gt 1048576 } |
  Sort-Object IODataBytesPersec -Descending |
  Select-Object -First 20 Name,IDProcess,PercentProcessorTime,
    @{n='IO_MBps';e={[math]::Round($_.IODataBytesPersec/1MB,2)}},
    @{n='Read_MBps';e={[math]::Round($_.IOReadBytesPersec/1MB,2)}},
    @{n='Write_MBps';e={[math]::Round($_.IOWriteBytesPersec/1MB,2)}}
```

Stop stale old-task processes only after confirming command lines:

```powershell
$targets = 24428,13104,22208,8272,10208
foreach ($targetPid in $targets) {
  $p = Get-Process -Id $targetPid -ErrorAction SilentlyContinue
  if ($p) { Stop-Process -Id $targetPid -Force }
}
```

Check Docker before stopping containers:

```powershell
docker ps --format "table {{.ID}}\t{{.Names}}\t{{.Status}}\t{{.Ports}}"
docker stats --all --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.BlockIO}}"
```

In this incident, stopping the stale `rg.exe` and preview processes dropped disk activity from about `1.01 MB/s` to `0.01 MB/s`. Stopping the stale Windmill containers dropped their CPU to `0.00%`.

## Veeam Rules

Veeam Agent can be legitimate but surprising. Do not assume it is useless. Identify it first:

```powershell
Get-WinEvent -LogName 'Veeam Agent' -MaxEvents 20 |
  Select-Object TimeCreated,Id,LevelDisplayName,ProviderName,Message
```

```powershell
Get-Service -Name 'VeeamEndpointBackupSvc'
Get-ChildItem -LiteralPath 'H:\' -Force |
  Where-Object { $_.Name -like '*VEEAM*' -or $_.Name -like '*Volume Image*' }
```

In this incident, Event Log showed the job `Windows System Volume Image to H` started daily around `00:30`, created `.vbk` and `.vib` files under `H:\SYSTEM_IMAGE_VEEAM_20260520`, and consumed about `138.95 GB`.

If the user explicitly says the backup is not needed, deletion is allowed but should be scoped:

- Stop or disable `VeeamEndpointBackupSvc` from administrator PowerShell.
- Delete only the confirmed backup target folder and its README.
- Do not uninstall Veeam or delete unrelated H drive content unless separately requested.

Administrator PowerShell commands used/needed:

```powershell
Stop-Service -Name VeeamEndpointBackupSvc -Force
Set-Service -Name VeeamEndpointBackupSvc -StartupType Disabled
Get-Service -Name VeeamEndpointBackupSvc
```

Deletion target from this incident:

```powershell
Remove-Item -LiteralPath 'H:\SYSTEM_IMAGE_VEEAM_20260520' -Recurse -Force
Remove-Item -LiteralPath 'H:\SYSTEM_IMAGE_VEEAM_20260520_README_先看我.txt' -Force
```

Final verification from the incident:

- `VeeamEndpointBackupSvc`: `Stopped`, `Disabled`.
- `H:\SYSTEM_IMAGE_VEEAM_20260520`: removed.
- H drive free space after cleanup: about `660.28 GB` free of `698.62 GB`.

## Safety Notes

- Do not stop Veeam mid-write unless the user explicitly wants to cancel backup; a partial backup may result.
- Do not delete backup files before confirming the target folder and job name.
- Do not stop or remove `open-webui-clean` just because Docker is running; it is a known local baseline service.
- Prefer "stop stale processes" over broad cleanup.
