# Hermes / Open WebUI No-Answer Chain

Use this reference when New API is running but Hermes, Open WebUI, or the digital assistant does not answer, saves an empty assistant message, or logs connection errors for stale worker ports.

## Scope

This is the local chain:

```text
Open WebUI 3000
  -> http://host.docker.internal:8642/v1
  -> Windows native Hermes gateway 8642
  -> http://127.0.0.1:3001/v1
  -> New API local gateway
```

Preserve these ports unless the user explicitly approves a port change:

- New API UI: `http://127.0.0.1:3001`
- New API base for Hermes: `http://127.0.0.1:3001/v1`
- Hermes gateway: `http://127.0.0.1:8642`
- Open WebUI: `http://127.0.0.1:3000`
- Open WebUI API base to Hermes: `http://host.docker.internal:8642/v1`

Treat old worker bases `http://host.docker.internal:18641/v1` through `http://host.docker.internal:18644/v1` as stale unless those workers are explicitly intended to be running and are freshly verified.

## Safety

- Do not print `.env`, New API tokens, Open WebUI JWTs, upstream API keys, or passwords.
- Do not delete containers, volumes, databases, chat history, or Hermes files for this repair.
- Back up `/app/backend/data/webui.db` before editing Open WebUI configuration.
- Prefer read-only checks until the failing boundary is proven.
- If Open WebUI database edits fail, restore the `webui.db.bak-*` backup and restart `open-webui-clean`.

## Fast Recovery Pattern: 8642 Not Listening

Use this when the digital assistant stops answering after restart and G01 shows:

- `new-api`, `new-api-postgres`, `new-api-redis`, and `open-webui-clean` are running.
- `http://127.0.0.1:3001` returns `200`.
- `http://127.0.0.1:3001/v1/models` returns `401` without a token.
- `http://127.0.0.1:3000` returns `200`.
- Port `8642` is `NOT_LISTENING`, and both Hermes `/health` and `/v1/models` cannot connect.

In this case, do not edit Open WebUI or New API first. The failing boundary is
the Windows native Hermes gateway. Start it with the mature launcher:

```powershell
cmd.exe /c "H:\Hermes_Windows_Native_014\START-HERMES-WEBUI.cmd"
```

Then verify:

```powershell
$owner = Get-NetTCPConnection -LocalPort 8642 -State Listen -ErrorAction Stop | Select-Object -First 1
$proc = Get-CimInstance Win32_Process -Filter "ProcessId=$($owner.OwningProcess)"
"PORT_8642_OWNER=$($proc.CommandLine)"
(Invoke-WebRequest -Uri "http://127.0.0.1:8642/health" -UseBasicParsing -TimeoutSec 10).Content
(Invoke-WebRequest -Uri "http://127.0.0.1:8642/v1/models" -UseBasicParsing -TimeoutSec 10).Content
$page = Invoke-WebRequest -Uri "http://127.0.0.1:3000" -UseBasicParsing -TimeoutSec 20
"OPENWEBUI_CODE=$([int]$page.StatusCode)"
$latest = Get-ChildItem -LiteralPath "H:\Hermes_Windows_Native_014\reports" -Filter "daily-start-*.log" |
  Sort-Object LastWriteTime -Descending | Select-Object -First 1
"LATEST_LOG=$($latest.FullName)"
Get-Content -LiteralPath $latest.FullName -Tail 40
```

Expected evidence:

- `PORT_8642_OWNER` includes `H:\Hermes_Windows_Native_014\venv\Scripts\hermes.exe gateway run --replace`.
- `/health` returns `{"status": "ok", "platform": "hermes-agent"}`.
- `/v1/models` returns `hermes-agent`.
- Open WebUI returns `200`.
- Latest `daily-start-*.log` contains `FINAL_PASS Windows native Hermes page is ready`.

Continue with G02, G03, G04, and G06. Only run G05 if G04 proves stale Open
WebUI bases are present. If G04 shows exactly
`http://host.docker.internal:8642/v1`, no database repair is needed.

2026-05-22 incident note: this pattern restored a no-answer state where New API
and Open WebUI were healthy, `8642` was not listening, recent Open WebUI chats
had empty assistant messages, and the final checks returned `HERMES_DIRECT_OK`,
`HERMES_STREAM_OK`, and `FINAL_CHAIN_OK`.

## Fast Recovery Pattern: Docker And New API Down

Use this when the digital assistant, New API, or Open WebUI is disconnected and
G01 shows:

- Docker API fails with `failed to connect to the docker API`.
- Port `3001` is `NOT_LISTENING`, and `http://127.0.0.1:3001` cannot connect.
- Port `3000` is `NOT_LISTENING`, and `http://127.0.0.1:3000` cannot connect.
- Hermes `8642` is already listening, and both `/health` and `/v1/models`
  return `200`.

In this case, do not restart Hermes first and do not edit Open WebUI config.
The failing boundary is Docker/New API/Open WebUI. Start Docker Desktop, wait
for the daemon, then bring back New API and Open WebUI:

```powershell
$dockerDesktop = 'C:\Program Files\Docker\Docker\Docker Desktop.exe'
if (-not (Test-Path -LiteralPath $dockerDesktop)) { throw "DOCKER_DESKTOP_MISSING=$dockerDesktop" }
if (-not (Get-Process 'Docker Desktop' -ErrorAction SilentlyContinue)) {
  Start-Process -FilePath $dockerDesktop -WindowStyle Hidden
}

$deadline = (Get-Date).AddSeconds(240)
$ready = $false
while ((Get-Date) -lt $deadline) {
  $version = docker info --format '{{.ServerVersion}}' 2>$null
  if ($LASTEXITCODE -eq 0 -and $version) {
    "DOCKER_DAEMON_READY=$version"
    $ready = $true
    break
  }
  Start-Sleep -Seconds 5
}
if (-not $ready) { throw 'DOCKER_DAEMON_NOT_READY_AFTER_240S' }

${REDACTED_SECRET}
docker compose config --quiet
docker compose up -d
docker compose ps

docker start open-webui-clean
$deadline = (Get-Date).AddSeconds(120)
while ((Get-Date) -lt $deadline) {
  $status = docker inspect open-webui-clean --format '{{if .State.Health}}{{.State.Health.Status}}{{else}}{{.State.Status}}{{end}}' 2>$null
  if ($status -eq 'healthy' -or $status -eq 'running') {
    "OPENWEBUI_STATUS=$status"
    break
  }
  Start-Sleep -Seconds 3
}
```

Then continue with G01, G02, G03, G04, and G06 verification. Expected evidence:

- Docker daemon responds to `docker info`.
- `new-api`, `new-api-postgres`, and `new-api-redis` are running and healthy or
  starting toward healthy.
- `open-webui-clean` is running and healthy.
- `http://127.0.0.1:3001` returns `200`.
- `http://127.0.0.1:3001/v1/models` returns `401` without a token.
- `http://127.0.0.1:3000` returns `200`.
- Hermes direct chat returns `HERMES_DIRECT_OK`.
- Open WebUI API chat returns `FINAL_CHAIN_OK`.
- New API logs show `/v1/chat/completions` relay `200`.
- Telegram diagnostic returns `Result: PASS`.

2026-05-22 incident note: this pattern restored a disconnected state where
Hermes `8642` was healthy, but Docker daemon was unavailable and both New API
`3001` and Open WebUI `3000` were not listening.

For recurring reboot/login failures of this class, use the login auto recovery
task documented in `references/local-layout.md`. It starts Docker Desktop,
recovers New API, starts `open-webui-clean`, checks Hermes `8642`, and verifies
Telegram state automatically at Windows login.

## G01 Runtime Check

Purpose: prove Docker, New API, Hermes, and Open WebUI are alive before changing anything.

${REDACTED_SECRET}

Command:

```powershell
docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Ports}}\t{{.Status}}'

$rows = @()
foreach ($port in @(3001,8642,3000)) {
  $conn = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue | Select-Object -First 1
  if ($conn) {
    $proc = Get-CimInstance Win32_Process -Filter "ProcessId=$($conn.OwningProcess)" -ErrorAction SilentlyContinue
    $rows += [PSCustomObject]@{Port=$port;Pid=$conn.OwningProcess;Process=$proc.Name;CommandLine=$proc.CommandLine}
  } else {
    $rows += [PSCustomObject]@{Port=$port;Pid='';Process='';CommandLine='NOT_LISTENING'}
  }
}
$rows | Format-List

foreach ($uri in @(
  'http://127.0.0.1:3001',
  'http://127.0.0.1:3001/v1/models',
  'http://127.0.0.1:8642/health',
  'http://127.0.0.1:8642/v1/models',
  'http://127.0.0.1:3000'
)) {
  try {
    $resp = Invoke-WebRequest -Uri $uri -UseBasicParsing -TimeoutSec 15
    "$uri STATUS=$([int]$resp.StatusCode)"
  } catch {
    $status = ''
    if ($_.Exception.Response) { $status = [int]$_.Exception.Response.StatusCode }
    "$uri STATUS=$status ERROR=$($_.Exception.Message)"
  }
}
```

Success criteria:

- `new-api`, `new-api-postgres`, `new-api-redis`, and `open-webui-clean` are `Up` and preferably `healthy`.
- `3001`, `8642`, and `3000` are listening.
- New API UI returns `200`.
- `http://127.0.0.1:3001/v1/models` returns `401` without a token; this is normal and proves auth is enforced.
- Hermes `/health` returns `platform=hermes-agent`.
- Hermes `/v1/models` returns `hermes-agent`.
- Open WebUI returns `200`.

Failure recovery:

- For New API container failures, use `references/local-layout.md`.
- For Hermes startup failures, use `windows-hermes-operations`.
- Do not edit Open WebUI database until G02-G04 identify the failing boundary.

## G02 Direct Hermes Chat

Purpose: determine whether Hermes can generate an answer without Open WebUI.

${REDACTED_SECRET}

Command:

```powershell
$body = @{
  model = 'hermes-agent'
  messages = @(@{ role='user'; content='Please answer only: HERMES_DIRECT_OK' })
  stream = $false
} | ConvertTo-Json -Depth 8

$resp = Invoke-WebRequest -Uri 'http://127.0.0.1:8642/v1/chat/completions' `
  -Method Post -ContentType 'application/json' -Body $body `
  -UseBasicParsing -TimeoutSec 120

"STATUS=$([int]$resp.StatusCode)"
$resp.Content
```

Success criteria:

- HTTP `200`.
- Response contains a non-empty assistant message.

Failure recovery:

- Inspect Hermes logs and New API logs before changing configuration.
- If this fails, the problem is below Open WebUI.

## G03 Direct Hermes Streaming Chat

Purpose: verify the streaming format that Open WebUI normally consumes.

${REDACTED_SECRET}

Command:

```powershell
$body = @{
  model = 'hermes-agent'
  messages = @(@{ role='user'; content='Please answer only: HERMES_STREAM_OK' })
  stream = $true
} | ConvertTo-Json -Depth 8

$resp = Invoke-WebRequest -Uri 'http://127.0.0.1:8642/v1/chat/completions' `
  -Method Post -ContentType 'application/json' -Body $body `
  -UseBasicParsing -TimeoutSec 120

"STATUS=$([int]$resp.StatusCode)"
$resp.Content
```

Success criteria:

- HTTP `200`.
- SSE contains `data:` lines with `choices[0].delta.content`.
- SSE ends with `data: [DONE]`.

Failure recovery:

- Fix Hermes response handling before editing Open WebUI.

## G04 Inspect Open WebUI Config And Logs

Purpose: detect stale Open WebUI API bases and empty saved assistant messages.

${REDACTED_SECRET}

Command:

```powershell
docker logs --tail 300 open-webui-clean 2>&1 |
  Select-String -Pattern 'ERROR','Exception','Connection error','18641','18642','18643','18644','8642','/api/models','/api/chat/completions' -CaseSensitive:$false |
  Select-Object -Last 120

$py = @'
import sqlite3, json
con=sqlite3.connect('/app/backend/data/webui.db')
cur=con.cursor()
raw=cur.execute('select data from config limit 1').fetchone()[0]
data=json.loads(raw)
openai=data.get('openai',{})
print('openai.enable=', openai.get('enable'))
print('openai.api_base_urls=', openai.get('api_base_urls'))
cfg=openai.get('api_configs')
print('openai.api_configs.keys=', list(cfg.keys()) if isinstance(cfg,dict) else type(cfg).__name__)

rows=cur.execute('select id,title,updated_at,chat from chat order by updated_at desc limit 5').fetchall()
for cid,title,updated,chat_json in rows:
    chat=json.loads(chat_json)
    msgs=chat.get('messages') or []
    print('CHAT', cid, 'TITLE=', title, 'UPDATED=', updated, 'MODELS=', chat.get('models') or chat.get('model'), 'COUNT=', len(msgs))
    for m in msgs[-2:]:
        if isinstance(m,dict):
            c=m.get('content')
            clen=len(c) if isinstance(c,str) else 0
            print('  MSG role=',m.get('role'),'model=',m.get('model'),'done=',m.get('done'),'error=',m.get('error'),'content_len=',clen)
'@
$py | docker exec -i open-webui-clean python3 -
```

Failure signals:

- `openai.api_base_urls` includes stale `18641-18644` entries.
- Logs show `Cannot connect to host host.docker.internal:18641` through `18644`.
- The latest chat shows an assistant message with `done=True`, no error, but `content_len=0`.

Recovery:

- Continue to G05 only if stale bases are present and Hermes direct chat already passed.

## G05 Remove Stale Open WebUI Bases

Purpose: remove stale worker bases from Open WebUI while preserving the working Hermes base.

${REDACTED_SECRET}

Command:

```powershell
$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$script = @'
import sqlite3, json, shutil, os
stamp = os.environ['BACKUP_STAMP']
db = '/app/backend/data/webui.db'
backup = f'/app/backend/data/webui.db.bak-{stamp}'
shutil.copy2(db, backup)

con = sqlite3.connect(db)
cur = con.cursor()
row = cur.execute('select id,data from config limit 1').fetchone()
if not row:
    raise SystemExit('CONFIG_ROW_MISSING')
config_id, raw = row
data = json.loads(raw)
openai = data.setdefault('openai', {})
base_urls = openai.get('api_base_urls') or []
api_keys = openai.get('api_keys') or []
api_configs = openai.get('api_configs') or {}
if not base_urls:
    raise SystemExit('OPENAI_BASE_URLS_EMPTY')
if base_urls[0] != 'http://host.docker.internal:8642/v1':
    raise SystemExit(f'FIRST_BASE_URL_UNEXPECTED={base_urls[0]}')

openai['api_base_urls'] = [base_urls[0]]
openai['api_keys'] = [api_keys[0] if api_keys else '']
if isinstance(api_configs, dict):
    cfg0 = api_configs.get('0') or api_configs.get(0) or {'enable': True}
    if isinstance(cfg0, dict):
        cfg0['enable'] = True
    openai['api_configs'] = {'0': cfg0}
elif isinstance(api_configs, list):
    cfg0 = api_configs[0] if api_configs else {'enable': True}
    if isinstance(cfg0, dict):
        cfg0['enable'] = True
    openai['api_configs'] = [cfg0]
else:
    openai['api_configs'] = {'0': {'enable': True}}

cur.execute('update config set data=?, updated_at=CURRENT_TIMESTAMP where id=?', (json.dumps(data, ensure_ascii=False), config_id))
con.commit()
con.close()
print('BACKUP=' + backup)
print('OPENAI_BASE_URLS_BEFORE=' + ','.join(base_urls))
print('OPENAI_BASE_URLS_AFTER=' + ','.join(openai['api_base_urls']))
'@

$script | docker exec -i -e BACKUP_STAMP=$stamp open-webui-clean python3 -
docker restart open-webui-clean
```

Success criteria:

- Command prints a `webui.db.bak-*` backup path.
- `OPENAI_BASE_URLS_AFTER=http://host.docker.internal:8642/v1`.
- `open-webui-clean` restarts.

Failure recovery:

```powershell
docker exec open-webui-clean sh -lc 'cp /app/backend/data/webui.db.bak-YYYYMMDD-HHMMSS /app/backend/data/webui.db'
docker restart open-webui-clean
```

Replace `YYYYMMDD-HHMMSS` with the printed backup suffix.

## G06 Final Verification

Purpose: prove the repaired chain works and stale bases are no longer queried.

${REDACTED_SECRET}

Command:

```powershell
$deadline = (Get-Date).AddSeconds(90)
while ((Get-Date) -lt $deadline) {
  $status = docker inspect open-webui-clean --format '{{.State.Health.Status}}' 2>$null
  if ($status -eq 'healthy') { "OPENWEBUI_HEALTH=$status"; break }
  Start-Sleep -Seconds 3
}

$py = @'
import sqlite3, json
con=sqlite3.connect('/app/backend/data/webui.db')
raw=con.execute('select data from config limit 1').fetchone()[0]
data=json.loads(raw)
openai=data.get('openai',{})
print('OPENAI_ENABLE=', openai.get('enable'))
print('OPENAI_BASE_URL_COUNT=', len(openai.get('api_base_urls') or []))
print('OPENAI_BASE_URLS=', ','.join(openai.get('api_base_urls') or []))
'@
$py | docker exec -i open-webui-clean python3 -

foreach ($uri in @('http://127.0.0.1:3001','http://127.0.0.1:8642/health','http://127.0.0.1:8642/v1/models','http://127.0.0.1:3000')) {
  try {
    $r = Invoke-WebRequest -Uri $uri -UseBasicParsing -TimeoutSec 30
    "$uri STATUS=$([int]$r.StatusCode)"
  } catch {
    "$uri ERROR=$($_.Exception.Message)"
  }
}
```

To test Open WebUI API without using the browser, create a short-lived local JWT from `/app/backend/.webui_secret_key`; keep it only in the PowerShell process and never print it:

```powershell
$pyToken = @'
import sqlite3, time, uuid, jwt, warnings
from pathlib import Path
warnings.filterwarnings('ignore')
con=sqlite3.connect('/app/backend/data/webui.db')
uid=con.execute("select id from user where role='admin' limit 1").fetchone()[0]
${REDACTED_SECRET}
payload={'id': uid, 'exp': int(time.time()) + 1800, 'jti': str(uuid.uuid4())}
print(jwt.encode(payload, secret, algorithm='HS256'))
'@
$token = ($pyToken | docker exec -i open-webui-clean python3 - | Select-Object -Last 1).Trim()
$headers = @{ Authorization = "Bearer $token" }

$modelsResp = Invoke-WebRequest -Uri 'http://127.0.0.1:3000/api/models' -Headers $headers -UseBasicParsing -TimeoutSec 45
"MODELS_STATUS=$([int]$modelsResp.StatusCode)"
($modelsResp.Content | ConvertFrom-Json).data | Select-Object id,name,owned_by | Format-Table -AutoSize

$body = @{
  model='hermes-agent'
  messages=@(@{role='user'; content='Please answer only: FINAL_CHAIN_OK'})
  stream=$true
} | ConvertTo-Json -Depth 8
$chatResp = Invoke-WebRequest -Uri 'http://127.0.0.1:3000/api/chat/completions' `
  -Method Post -Headers $headers -ContentType 'application/json' -Body $body `
  -UseBasicParsing -TimeoutSec 120
"CHAT_STREAM_STATUS=$([int]$chatResp.StatusCode)"
$chatResp.Content

Start-Sleep -Seconds 5
$matches = docker logs --since 20s open-webui-clean 2>&1 |
  Select-String -Pattern '18641','18642','18643','18644','Connection error','ERROR','/api/models' -CaseSensitive:$false
if ($matches) { $matches | Select-Object -Last 80 } else { 'NO_MATCHES' }
```

Success criteria:

- `OPENWEBUI_HEALTH=healthy`.
- `OPENAI_BASE_URL_COUNT=1`.
- `OPENAI_BASE_URLS=http://host.docker.internal:8642/v1`.
- Open WebUI `/api/models` returns `200` and includes `hermes-agent`.
- Open WebUI `/api/chat/completions` returns `200` with streaming `delta.content` and `[DONE]`.
- A fresh `/api/models` request produces no new `18641-18644` connection errors.
- New API logs show successful `/v1/chat/completions` relay activity.

Failure recovery:

- Restore the `webui.db.bak-*` backup if the config edit caused regression.
- If G02/G03 pass but G06 fails, inspect Open WebUI version-specific API behavior before making another config change.
