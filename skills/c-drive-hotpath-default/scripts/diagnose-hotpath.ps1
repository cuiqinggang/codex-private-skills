param(
  [string]$OutputDir = "",
  [int]$Samples = 5,
  [int]$SampleIntervalSeconds = 1
)

$ErrorActionPreference = "Continue"
$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"

if ([string]::IsNullOrWhiteSpace($OutputDir)) {
  $OutputDir = Join-Path $env:USERPROFILE "Documents\Codex\hotpath-diagnostics"
}

New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null
$report = Join-Path $OutputDir "hotpath-diagnostic-$timestamp.txt"

function Add-Section {
  param([string]$Title, [scriptblock]$Body)
  Add-Content -LiteralPath $report -Value ""
  Add-Content -LiteralPath $report -Value ("===== " + $Title + " =====")
  try {
    $result = & $Body | Out-String -Width 300
    Add-Content -LiteralPath $report -Value $result
  } catch {
    Add-Content -LiteralPath $report -Value ("ERROR: " + $_.Exception.Message)
  }
}

Add-Content -LiteralPath $report -Value "C Drive Hotpath Diagnostic"
Add-Content -LiteralPath $report -Value ("Timestamp: " + (Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz"))
Add-Content -LiteralPath $report -Value "Rule: C: is default hot runtime path. D/H/K are opt-in only."

Add-Section "Disk Inventory" {
  Get-Disk | Sort-Object Number | Format-List Number,FriendlyName,SerialNumber,BusType,MediaType,OperationalStatus,HealthStatus,Size,PartitionStyle
}

Add-Section "Physical Disks" {
  Get-PhysicalDisk | Sort-Object DeviceId | Format-List DeviceId,FriendlyName,SerialNumber,MediaType,BusType,Size,HealthStatus,OperationalStatus,SpindleSpeed
}

Add-Section "Volumes" {
  Get-Volume | Sort-Object DriveLetter | Format-Table DriveLetter,FileSystemLabel,FileSystem,DriveType,HealthStatus,SizeRemaining,Size -AutoSize
}

Add-Section "Partitions" {
  Get-Partition | Sort-Object DiskNumber,PartitionNumber | Format-Table DiskNumber,PartitionNumber,DriveLetter,Type,Size,Offset -AutoSize
}

Add-Section "Disk IO Samples" {
  Get-Counter '\PhysicalDisk(*)\Disk Read Bytes/sec','\PhysicalDisk(*)\Disk Write Bytes/sec','\LogicalDisk(*)\Disk Read Bytes/sec','\LogicalDisk(*)\Disk Write Bytes/sec' -SampleInterval $SampleIntervalSeconds -MaxSamples $Samples |
    ForEach-Object { $_.CounterSamples | Where-Object { $_.CookedValue -gt 0 } | Select-Object Timestamp,Path,CookedValue } |
    Format-Table -AutoSize
}

Add-Section "Non-C Runtime Processes" {
  Get-CimInstance Win32_Process |
    Where-Object { ($_.ExecutablePath -match '^[D-HK]:\\') -or ($_.CommandLine -match '[D-HK]:\\') } |
    Select-Object ProcessId,Name,ExecutablePath,CommandLine |
    Format-List
}

Add-Section "Scheduled Tasks Referencing Non-C Drives" {
  Get-ScheduledTask |
    ForEach-Object {
      $task = $_
      foreach ($a in $task.Actions) {
        [pscustomobject]@{
          TaskPath = $task.TaskPath
          TaskName = $task.TaskName
          State = $task.State
          Execute = $a.Execute
          Arguments = $a.Arguments
        }
      }
    } |
    Where-Object { ($_.Execute -match '^[D-HK]:\\') -or ($_.Arguments -match '[D-HK]:\\') } |
    Format-List
}

Add-Section "Startup Commands Referencing Non-C Drives" {
  Get-CimInstance Win32_StartupCommand |
    Where-Object { $_.Command -match '[D-HK]:\\' } |
    Select-Object Name,Location,Command,User |
    Format-List
}

Add-Section "Services Referencing Non-C Drives" {
  Get-CimInstance Win32_Service |
    Where-Object { $_.PathName -match '^[\"'']?[D-HK]:\\' } |
    Select-Object Name,State,StartMode,PathName |
    Format-List
}

Add-Section "Pagefile" {
  Get-CimInstance Win32_PageFileSetting | Format-List Name,InitialSize,MaximumSize
  Get-CimInstance Win32_PageFileUsage | Format-List Name,AllocatedBaseSize,CurrentUsage,PeakUsage
}

Add-Section "User Temp And Profile Paths" {
  Get-ChildItem Env:TEMP,Env:TMP,Env:USERPROFILE,Env:LOCALAPPDATA,Env:APPDATA |
    Format-Table Name,Value -AutoSize
}

Add-Section "Disk Idle Power Setting" {
  powercfg /query SCHEME_CURRENT SUB_DISK DISKIDLE
}

Add-Section "Hotpath Summary Hints" {
  "Review any non-C process, task, startup item, service, temp path, pagefile, or sustained D/H/K disk IO above."
  "Do not delete, format, move, or disable protected tasks without explicit user approval."
}

Write-Output $report

