# Stage 00 Minimal DeepSeek

Use this reference to recover the clean base layer:

```text
Hermes Windows native 0.14
  -> 127.0.0.1:8642
  -> https://api.deepseek.com
  -> deepseek-v4-pro
```

This stage intentionally does not run Telegram, New API, Open WebUI, Watchdog,
AutoRecover, Startup entries, or scheduled-task recovery.

Do not print secrets.

## Gates

### G00.1 Clean Processes

Purpose: stop old Hermes, watchdog, autorecover, New API bridge, and stale 8642
processes before creating the minimal state.

Command:

```powershell
$ErrorActionPreference='Stop'
$self=$PID
Get-CimInstance Win32_Process |
  Where-Object {
    $_.ProcessId -ne $self -and
    $_.CommandLine -match 'Hermes|hermes|Watchdog|watchdog|AutoRecover|NewAPI|8642'
  } |
  ForEach-Object {
    try { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue } catch {}
  }
Start-Sleep -Seconds 3
$left=Get-CimInstance Win32_Process |
  Where-Object {
    $_.ProcessId -ne $self -and
    $_.CommandLine -match 'Hermes|hermes|Watchdog|watchdog|AutoRecover|NewAPI|8642'
  }
if($left){$left | Select ProcessId,Name,CommandLine | Format-List; 'G00_1_WARN_PROCESS_LEFT'}else{'G00_1_PASS_CLEAN_PROCESS_STATE'}
$listen=@(Get-NetTCPConnection -LocalPort 8642 -State Listen -ErrorAction SilentlyContinue)
'LISTEN_COUNT_8642='+$listen.Count
```

Success: no relevant process remains and `LISTEN_COUNT_8642=0`.

### G00.2 Disable Old Autostart Without Deleting

Purpose: isolate legacy Startup entries and disable Hermes/NewAPI/Watchdog
scheduled tasks without deleting the originals.

Command:

```powershell
$ErrorActionPreference='Stop'
$Task='HERMES-014-MINIMAL-CLEAN-STATE-20260522'
${REDACTED_SECRET}
$Disabled="$Root\disabled-startup"
New-Item -ItemType Directory -Force $Disabled | Out-Null
$Startup=[Environment]::GetFolderPath('Startup')
Get-ChildItem $Startup -ErrorAction SilentlyContinue |
  Where-Object { $_.Name -match 'Hermes|Gateway|NewAPI|Watchdog' } |
  ForEach-Object {
    Move-Item -LiteralPath $_.FullName -Destination (Join-Path $Disabled ($_.Name+'.disabled')) -Force
  }
Get-ScheduledTask -ErrorAction SilentlyContinue |
  Where-Object { $_.TaskName -match 'Hermes|Gateway|Watchdog|NewAPI|AutoRecover|014' } |
  Disable-ScheduledTask -ErrorAction SilentlyContinue | Out-Null
'G00_2_PASS_OLD_AUTOSTART_DISABLED_NOT_DELETED'
```

### G00.3 Configure DeepSeek Official Direct Mode

Purpose: configure Hermes for direct DeepSeek V4 Pro and disable Telegram /
NewAPI / proxy routing in `.env`.

Required location:

```text
${REDACTED_SECRET}
${REDACTED_SECRET}
```

Rules:

- Backup before editing with `.bak.minimal.<timestamp>`.
- Set `DEEPSEEK_BASE_URL=https://api.deepseek.com`.
- Set the default model to `deepseek-v4-pro`.
- Disable `TELEGRAM*`, `TG_*`, `NEWAPI*`, `NEW_API*`, `OPENAI_*`, `HTTP_PROXY`,
  `HTTPS_PROXY`, and other non-DeepSeek routing variables by prefixing
  `#DISABLED_MINIMAL#`.
- Do not print `DEEPSEEK_API_KEY`.

After editing, parse `config.yaml`:

```powershell
@'
import pathlib, yaml
${REDACTED_SECRET}
with p.open('r', encoding='utf-8-sig') as f:
    yaml.safe_load(f)
print('YAML_PARSE_PASS')
'@ | python -
```

### G00.4 Recover DeepSeek V4 Pro Key From Local New API If Needed

Use this only when chat returns DeepSeek `401 invalid api key` and the user says
the valid V4 Pro channel is in New API.

Read channel metadata without printing the key:

```powershell
docker exec new-api-postgres psql -U newapi -d newapi -Atc "select id, name, type, status, coalesce(base_url,''), coalesce(test_model,''), length(coalesce(key,'')), left(coalesce(models,''),160), coalesce(model_mapping,'') from channels order by id;"
```

Known good 2026-05-22 channel:

```text
id=2
name=DeepSeek-V4-Pro-CN
status=1
base_url=https://api.deepseek.com
test_model=deepseek-v4-pro
key_length=35
```

Move the key into Hermes without printing it:

```powershell
$ErrorActionPreference='Stop'
${REDACTED_SECRET}
$Stamp=Get-Date -Format 'yyyyMMdd_HHmmss'
$key = docker exec new-api-postgres psql -U newapi -d newapi -Atc "select key from channels where id=2 and status=1 and name='DeepSeek-V4-Pro-CN' and test_model='deepseek-v4-pro' limit 1;"
$key = ($key | Select-Object -First 1).Trim()
if([string]::IsNullOrWhiteSpace($key)){ throw 'DEEPSEEK_V4_PRO_KEY_NOT_FOUND_IN_NEW_API' }
Copy-Item -LiteralPath $envPath -Destination ($envPath+'.bak.minimal.deepseekkey.'+$Stamp) -Force
$lines=Get-Content -LiteralPath $envPath
$found=$false
$out=foreach($l in $lines){
  if($l -match '^DEEPSEEK_API_KEY='){
    $found=$true
    'DEEPSEEK_API_KEY='+$key
  } else {
    $l
  }
}
${REDACTED_SECRET}
Set-Content -Encoding UTF8 -LiteralPath $envPath -Value $out
'G00_4_PASS_DEEPSEEK_V4_PRO_KEY_MOVED_TO_HERMES_ENV'
'KEY_LENGTH='+$key.Length
'BACKUP_STAMP='+$Stamp
```

After key migration, stop New API and Open WebUI containers if Stage 00 is still
the target:

```powershell
$containers=@('new-api','new-api-postgres','new-api-redis','open-webui-clean')
$existing=@()
foreach($c in $containers){
  $id=(docker ps -aq --filter "name=^/$c$")
  if($id){ $existing += $c }
}
if($existing.Count -gt 0){ docker stop $existing | Out-Null }
'DOCKER_STOPPED='+($existing -join ',')
```

### G00.5 Start Single Hermes Entry

Command:

```powershell
$ErrorActionPreference='Stop'
$Launcher='H:\Hermes_Windows_Native_014\launcher\hermes-014-runtime.ps1'
if(!(Test-Path -LiteralPath $Launcher)){throw 'HERMES_014_RUNTIME_LAUNCHER_NOT_FOUND'}
Start-Process powershell.exe -ArgumentList @('-NoProfile','-ExecutionPolicy','Bypass','-File',$Launcher) -WindowStyle Minimized
Start-Sleep -Seconds 30
$r=Invoke-WebRequest -Uri 'http://127.0.0.1:8642/health' -UseBasicParsing -TimeoutSec 10
'HEALTH_STATUS='+$r.StatusCode
if($r.StatusCode -eq 200){'G00_5_PASS_MINIMAL_HERMES_STARTED'}else{'G00_5_FAIL_HEALTH_NOT_200'}
```

### G00.6 Verify Models And Chat

Command:

```powershell
${REDACTED_SECRET}
$Art="$Root\artifacts"
New-Item -ItemType Directory -Force $Art | Out-Null
$Out="$Art\G05-api-check-after-key-migration.txt"
$m=Invoke-WebRequest -Uri 'http://127.0.0.1:8642/v1/models' -UseBasicParsing -TimeoutSec 10
'MODELS_STATUS='+$m.StatusCode | Set-Content -Encoding UTF8 $Out
$m.Content | Add-Content -Encoding UTF8 $Out
$body=@{model='hermes-agent';messages=@(@{role='user';content='Reply exactly: HERMES_MINIMAL_DEEPSEEK_OK'})} | ConvertTo-Json -Depth 8
$c=Invoke-WebRequest -Uri 'http://127.0.0.1:8642/v1/chat/completions' -Method POST -Body $body -ContentType 'application/json' -UseBasicParsing -TimeoutSec 120
'CHAT_STATUS='+$c.StatusCode | Add-Content -Encoding UTF8 $Out
$c.Content | Add-Content -Encoding UTF8 $Out
if($m.StatusCode -eq 200 -and $c.Content -match 'HERMES_MINIMAL_DEEPSEEK_OK'){ 'G00_6_PASS_MINIMAL_DEEPSEEK_CHAT_OK' } else { 'G00_6_FAIL_CHAT_MARK_NOT_FOUND' }
```

Success:

- `/health` returns 200.
- `/v1/models` returns 200 with `hermes-agent`.
- chat returns `HERMES_MINIMAL_DEEPSEEK_OK`.
- only one listener exists on `127.0.0.1:8642`.
- New API, Telegram, Watchdog, and AutoRecover are not running.

## 2026-05-22 Evidence

- DeepSeek 401 was fixed by moving the active New API V4 Pro key into
${REDACTED_SECRET}
- `G05-api-check-after-key-migration.txt` showed `MODELS_STATUS=200`,
  `CHAT_STATUS=200`, and `HERMES_MINIMAL_DEEPSEEK_OK`.
- `G06-final-process-state-retry.txt` showed one 8642 listener and no NewAPI /
  Watchdog / AutoRecover process.

