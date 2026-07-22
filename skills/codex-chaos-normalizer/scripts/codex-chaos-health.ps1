param(
  [ValidateSet('Diagnose','Normalize','ScheduleLogArchive')]
  [string]$Mode = 'Diagnose',
  [string]$Workspace = (Get-Location).Path,
  [string]$CodexHome = (Join-Path $env:USERPROFILE '.codex'),
  [int]$CpuSampleSeconds = 5,
  [int]$LargeUntrackedThreshold = 500,
  [switch]$Json
)

$ErrorActionPreference = 'Continue'
$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$repairRoot = Join-Path $CodexHome 'repair-logs'
$runDir = Join-Path $repairRoot "codex-chaos-$stamp"
New-Item -ItemType Directory -Force -Path $runDir | Out-Null
$actions = New-Object System.Collections.Generic.List[object]
$findings = New-Object System.Collections.Generic.List[object]

function Add-Finding($Area, $Severity, $Message, $Data = $null) {
  $findings.Add([pscustomobject]@{ area=$Area; severity=$Severity; message=$Message; data=$Data }) | Out-Null
}
function Add-Action($Action, $Status, $Path = $null, $Rollback = $null) {
  $actions.Add([pscustomobject]@{ action=$Action; status=$Status; path=$Path; rollback=$Rollback }) | Out-Null
}
function Get-FileMB($Path) {
  if (Test-Path -LiteralPath $Path) { return [math]::Round((Get-Item -LiteralPath $Path).Length / 1MB, 2) }
  return 0
}
function Backup-File($Path, $Suffix) {
  if (-not (Test-Path -LiteralPath $Path)) { return $null }
  $backup = "$Path.bak.$Suffix.$stamp"
  Copy-Item -LiteralPath $Path -Destination $backup -Force
  return $backup
}

$Workspace = [System.IO.Path]::GetFullPath($Workspace)
Add-Finding 'run' 'info' "Run directory: $runDir" $null
Add-Finding 'workspace' 'info' "Workspace: $Workspace" $null

# System and process sampling.
try {
  $os = Get-CimInstance Win32_OperatingSystem
  $cs = Get-CimInstance Win32_ComputerSystem
  Add-Finding 'system' 'info' 'Memory and CPU baseline' ([pscustomobject]@{
    total_ram_gb = [math]::Round($cs.TotalPhysicalMemory / 1GB, 2)
    free_ram_gb = [math]::Round($os.FreePhysicalMemory / 1MB, 2)
    logical_processors = $cs.NumberOfLogicalProcessors
    last_boot = $os.LastBootUpTime
  })
} catch { Add-Finding 'system' 'warn' "Could not read OS baseline: $($_.Exception.Message)" }

try {
  $before = @{}
  Get-Process | Where-Object { $null -ne $_.CPU } | ForEach-Object { $before[$_.Id] = $_.CPU }
  Start-Sleep -Seconds $CpuSampleSeconds
  $cpuRows = @()
  Get-Process | Where-Object { $null -ne $_.CPU } | ForEach-Object {
    if ($before.ContainsKey($_.Id)) {
      $delta = $_.CPU - $before[$_.Id]
      if ($delta -gt 0.05) {
        $cpuRows += [pscustomobject]@{
          process = $_.ProcessName
          pid = $_.Id
          cpu_seconds = [math]::Round($delta, 3)
          ram_mb = [math]::Round($_.WorkingSet64 / 1MB, 1)
          title = $_.MainWindowTitle
        }
      }
    }
  }
  $topCpu = $cpuRows | Sort-Object cpu_seconds -Descending | Select-Object -First 20
  Add-Finding 'cpu' 'info' "Top CPU over $CpuSampleSeconds seconds" $topCpu
} catch { Add-Finding 'cpu' 'warn' "CPU sampling failed: $($_.Exception.Message)" }

try {
  $perf = Get-CimInstance Win32_PerfFormattedData_PerfProc_Process | Where-Object { $_.Name -match 'codex|Codex|chrome|powershell|git|node|python|MsMpEng|System|docker' } |
    Select-Object Name,IDProcess,PercentProcessorTime,IODataBytesPersec,IOReadBytesPersec,IOWriteBytesPersec |
    Sort-Object PercentProcessorTime -Descending | Select-Object -First 30
  Add-Finding 'process_perf' 'info' 'Codex-adjacent CPU and IO snapshot' $perf
} catch { Add-Finding 'process_perf' 'warn' "Process perf read failed: $($_.Exception.Message)" }

# Git storm diagnosis.
$gitDir = Join-Path $Workspace '.git'
if (Test-Path -LiteralPath $gitDir) {
  $tracked = 0
  $untracked = 0
  try { $tracked = (git -C $Workspace ls-files | Measure-Object -Line).Lines } catch { Add-Finding 'git' 'warn' "git ls-files failed: $($_.Exception.Message)" }
  try { $untracked = (git -C $Workspace status --porcelain=v1 --untracked-files=all | Measure-Object -Line).Lines } catch { Add-Finding 'git' 'warn' "git status failed: $($_.Exception.Message)" }
  Add-Finding 'git' 'info' 'Git tracked/untracked counts' ([pscustomobject]@{ tracked=$tracked; untracked=$untracked })
  if ($tracked -eq 0 -and $untracked -ge $LargeUntrackedThreshold) {
    Add-Finding 'git' 'high' 'Empty Git wrapper with many untracked files; this can cause Codex/Git scan storms.' ([pscustomobject]@{ tracked=$tracked; untracked=$untracked })
    if ($Mode -eq 'Normalize') {
      $exclude = Join-Path $gitDir 'info\exclude'
      $bak = Backup-File $exclude 'git-exclude'
      $content = if (Test-Path -LiteralPath $exclude) { Get-Content -LiteralPath $exclude -Raw } else { '' }
      if ($content -notmatch '(?m)^\*$') {
        Add-Content -LiteralPath $exclude -Value @('', '# codex-chaos-normalizer: empty Git wrapper; ignore all untracked workspace files', '*')
        Add-Action 'Append * to .git/info/exclude for empty wrapper repo' 'applied' $exclude "Restore $bak"
      } else {
        Add-Action 'Git exclude already suppresses all untracked files' 'skipped' $exclude $null
      }
    }
  }
} else {
  Add-Finding 'git' 'info' 'No .git directory in workspace.' $null
}

# Codex config and logs.
$config = Join-Path $CodexHome 'config.toml'
if (Test-Path -LiteralPath $config) {
  $configText = Get-Content -LiteralPath $config -Raw
  $enabledPlugins = [regex]::Matches($configText, '(?ms)^\[plugins\."([^"]+)"\]\s*enabled\s*=\s*true') | ForEach-Object { $_.Groups[1].Value }
  Add-Finding 'codex_config' 'info' 'Enabled plugins' $enabledPlugins
  if ($enabledPlugins.Count -gt 6) {
    Add-Finding 'codex_config' 'medium' 'Many enabled plugins can slow AppServer startup and thread opening.' $enabledPlugins
  }
  if ($Mode -eq 'Normalize') {
    $keep = @('superpowers@openai-curated','browser-use@openai-bundled','chrome@openai-bundled','browser@openai-bundled','computer-use@openai-bundled')
    $disable = @('hyperframes@openai-curated','hugging-face@openai-curated','vercel@openai-curated','remotion@openai-curated','github@openai-curated','slack@openai-curated')
    $newText = $configText
    foreach ($name in $disable) {
      if ($keep -contains $name) { continue }
      $pattern = '(?s)(\[plugins\."' + [regex]::Escape($name) + '"\]\s*)enabled\s*=\s*true'
      $newText = [regex]::Replace($newText, $pattern, '$1enabled = false')
    }
    if ($newText -ne $configText) {
      $bak = Backup-File $config 'config'
      [System.IO.File]::WriteAllText($config, $newText, [System.Text.UTF8Encoding]::new($false))
      Add-Action 'Disable low-frequency plugins to reduce background/plugin load' 'applied' $config "Restore $bak"
    } else {
      Add-Action 'Plugin config already normalized' 'skipped' $config $null
    }
  }
}

$logDbs = Get-ChildItem -LiteralPath $CodexHome -File -ErrorAction SilentlyContinue | Where-Object { $_.Name -match '^logs_.*\.sqlite' }
foreach ($db in $logDbs) {
  $mb = [math]::Round($db.Length / 1MB, 2)
  Add-Finding 'codex_logs' ($(if($mb -gt 300){'medium'}else{'info'})) "Codex log DB size: $($db.Name)" ([pscustomobject]@{ mb=$mb; path=$db.FullName })
}

try {
  $watchers = Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*compact-codex-logs-after-exit.ps1*' } |
    Select-Object ProcessId,ParentProcessId,Name,CreationDate,CommandLine
  if ($watchers) {
    Add-Finding 'codex_logs' 'info' 'Offline Codex log compaction watcher is running' $watchers
  } else {
    Add-Finding 'codex_logs' 'medium' 'No offline Codex log compaction watcher is running' $null
  }
} catch {
  Add-Finding 'codex_logs' 'warn' "Could not inspect compaction watcher: $($_.Exception.Message)" $null
}

try {
  $preview = Get-ChildItem -LiteralPath $repairRoot -Recurse -File -Filter 'logs_2.compact.preview.sqlite' -ErrorAction SilentlyContinue |
    Sort-Object LastWriteTime -Descending | Select-Object -First 1
  if ($preview) {
    $env:CODEX_PREVIEW_DB = $preview.FullName
    $previewJson = @'
import json, os, sqlite3
path = os.environ["CODEX_PREVIEW_DB"]
con = sqlite3.connect("file:" + path + "?mode=ro", uri=True, timeout=5)
cur = con.cursor()
integrity = cur.execute("pragma integrity_check").fetchone()[0]
rows = cur.execute("select count(*) from logs").fetchone()[0]
mn, mx = cur.execute("select min(ts), max(ts) from logs").fetchone()
con.close()
print(json.dumps({"path": path, "mb": round(os.path.getsize(path)/1024/1024, 2), "integrity": integrity, "rows": rows, "min_ts": mn, "max_ts": mx}, ensure_ascii=False))
'@ | python -
    $previewStats = $previewJson | ConvertFrom-Json
    $previewSeverity = if ($previewStats.integrity -eq 'ok') { 'info' } else { 'high' }
    Add-Finding 'codex_logs' $previewSeverity 'Latest compact preview database' $previewStats
  }
} catch {
  Add-Finding 'codex_logs' 'warn' "Could not inspect compact preview: $($_.Exception.Message)" $null
}

$primaryLogDb = Join-Path $CodexHome 'logs_2.sqlite'
if (Test-Path -LiteralPath $primaryLogDb) {
  try {
    $env:CODEX_LOG_DB = $primaryLogDb
    $logStatsJson = @'
import json, os, sqlite3, datetime
path = os.environ["CODEX_LOG_DB"]
con = sqlite3.connect("file:" + path + "?mode=ro", uri=True, timeout=5)
cur = con.cursor()
mn, mx, total = cur.execute("select min(ts), max(ts), count(*) from logs").fetchone()
recent = cur.execute("select count(*) from logs where ts >= ?", (mx - 86400,)).fetchone()[0] if mx else 0
levels = dict(cur.execute("select level, count(*) from logs where ts >= ? group by level", (mx - 86400,)).fetchall()) if mx else {}
trace_debug = levels.get("TRACE", 0) + levels.get("DEBUG", 0)
ratio = round(trace_debug / recent, 3) if recent else 0
print(json.dumps({
  "first": datetime.datetime.fromtimestamp(mn).isoformat(sep=" ") if mn else None,
  "last": datetime.datetime.fromtimestamp(mx).isoformat(sep=" ") if mx else None,
  "rows_total": total,
  "rows_24h": recent,
  "levels_24h": levels,
  "trace_debug_ratio_24h": ratio
}, ensure_ascii=False))
con.close()
'@ | python -
    $logStats = $logStatsJson | ConvertFrom-Json
    $severity = if ($logStats.rows_24h -gt 10000 -and $logStats.trace_debug_ratio_24h -gt 0.5) { 'medium' } else { 'info' }
    Add-Finding 'codex_logs' $severity 'Codex log volume and level mix' $logStats
  } catch {
    Add-Finding 'codex_logs' 'warn' "Could not inspect Codex log volume: $($_.Exception.Message)" $null
  }
}

if ($Mode -in @('Normalize','ScheduleLogArchive')) {
  $archiveScript = Join-Path $runDir 'archive-codex-logs-after-exit.ps1'
  @"
`$ErrorActionPreference = 'Stop'
`$home = '$CodexHome'
`$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
`$backup = Join-Path `$home "logs-archive-`$stamp"
Write-Host "Waiting for Codex.exe/codex.exe to exit..."
while (Get-Process Codex,codex -ErrorAction SilentlyContinue) { Start-Sleep -Seconds 2 }
New-Item -ItemType Directory -Force -Path `$backup | Out-Null
foreach (`$name in 'logs_2.sqlite','logs_2.sqlite-wal','logs_2.sqlite-shm') {
  `$p = Join-Path `$home `$name
  if (Test-Path -LiteralPath `$p) { Move-Item -LiteralPath `$p -Destination (Join-Path `$backup `$name) -Force }
}
Write-Host "Archived Codex log DB to `$backup"
"@ | Set-Content -LiteralPath $archiveScript -Encoding UTF8
  Add-Action 'Create wait-until-Codex-exits log archive script' 'applied' $archiveScript 'Move files back from logs-archive-* if needed'
}

$result = [pscustomobject]@{
  mode = $Mode
  workspace = $Workspace
  codex_home = $CodexHome
  run_dir = $runDir
  findings = $findings
  actions = $actions
}

$result | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $runDir 'result.json') -Encoding UTF8
if ($Json) { $result | ConvertTo-Json -Depth 8 } else {
  Write-Host "=== Codex Chaos Health: $Mode ==="
  Write-Host "Run dir: $runDir"
  Write-Host "Findings:"
  $findings | Select-Object area,severity,message | Format-Table -AutoSize
  Write-Host "Actions:"
  $actions | Format-Table -AutoSize
}
