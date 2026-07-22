# Incident 2026-06-05 - Open WebUI Shows No Model Selected

Use this note when Telegram/Hermes can answer through DeepSeek, but the Open
WebUI page at `http://127.0.0.1:3000` or
`http://127.0.0.1:3000/admin/settings/connections` still shows that no large
model is connected or selected.

## Current Direct Chain

The direct web chain is:

```text
Open WebUI 3000
  -> http://host.docker.internal:8642/v1
  -> Windows native Hermes gateway 8642
  -> DeepSeek provider
  -> deepseek-v4-pro
```

Do not route this repair through old New API `3001`. New API was a previous
setup and is not the active boundary for this incident.

Hermes exposes `hermes-agent` to Open WebUI. Hermes itself selects the real
${REDACTED_SECRET}
`model.default: deepseek-v4-pro`.

## Symptoms

- Telegram/mobile Hermes test answers normally.
- Direct Hermes chat to `http://127.0.0.1:8642/v1/chat/completions` answers.
- Open WebUI `3000` loads, but the web chat says no model is selected, or the
  admin connection page shows no selected model.
- Open WebUI container env may have the correct base URL but an old
  `OPENAI_API_KEY`.
- Open WebUI database config may still contain the old connection key or no
  explicit `model_ids`.

## Safety

- Do not print `.env`, Open WebUI keys, DeepSeek keys, Telegram tokens, or JWTs.
- Back up `/app/backend/data/webui.db` before editing Open WebUI config.
- Preserve the Docker volume `open-webui-clean`; it contains Open WebUI data.
- Do not delete chat history or Hermes profile files.
- Only recreate the `open-webui-clean` container when the key is proven stale,
  and keep the same volume and port mapping.

## G01 Prove Hermes Direct DeepSeek Works

```powershell
${REDACTED_SECRET}
Select-String -LiteralPath $cfg -Pattern '^\s*provider:\s*deepseek\s*$|^\s*default:\s*deepseek-v4-pro\s*$'

${REDACTED_SECRET}
$key = (Get-Content -LiteralPath $envPath |
  Where-Object { $_ -match '^API_SERVER_KEY=' } |
  Select-Object -First 1) -replace '^API_SERVER_KEY=', ''
$headers = @{ Authorization = "Bearer $key"; 'Content-Type' = 'application/json' }

Invoke-WebRequest -Uri 'http://127.0.0.1:8642/v1/models' `
  -UseBasicParsing -Headers $headers -TimeoutSec 30

$marker = 'HERMES_DIRECT_DEEPSEEK_OK_' + (Get-Date -Format HHmmss)
$body = @{
  model = 'hermes-agent'
  messages = @(@{ role='user'; content="Please answer only: $marker" })
  stream = $false
} | ConvertTo-Json -Depth 8
$resp = Invoke-WebRequest -Uri 'http://127.0.0.1:8642/v1/chat/completions' `
  -Method Post -Headers $headers -Body $body -UseBasicParsing -TimeoutSec 180
$json = $resp.Content | ConvertFrom-Json
$content = [string]$json.choices[0].message.content
[PSCustomObject]@{
  Status = [int]$resp.StatusCode
  ContainsMarker = ($content -like "*$marker*")
  Preview = $content.Substring(0, [Math]::Min(120, $content.Length))
}
```

Success criteria:

- `config.yaml` includes `provider: deepseek` and `default: deepseek-v4-pro`.
- `/v1/models` returns HTTP `200` and includes `hermes-agent`.
- Direct chat returns HTTP `200` and contains the marker.

If this fails, fix Hermes first. Do not edit Open WebUI yet.

## G02 Check Open WebUI Container Key

Open WebUI must use the same local bearer token as Hermes `API_SERVER_KEY`.
This check does not print the key.

```powershell
$code = @'
import os, urllib.request
base = os.environ.get('OPENAI_API_BASE_URL', '')
key = os.environ.get('OPENAI_API_KEY', '')
print('BASE', base)
print('KEY_PRESENT', bool(key))
req = urllib.request.Request(
    base.rstrip('/') + '/models',
    headers={'Authorization': 'Bearer ' + key},
)
try:
    with urllib.request.urlopen(req, timeout=30) as r:
        body = r.read(300).decode('utf-8', 'replace')
        print('STATUS', r.status)
        print('HAS_HERMES_AGENT', 'hermes-agent' in body)
except Exception as e:
    print('FAIL', type(e).__name__, str(e))
'@
$code | docker exec -i open-webui-clean python -
```

Failure signal:

- `FAIL HTTPError HTTP Error 401: Unauthorized`

Recovery when the container env key is stale:

```powershell
$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
${REDACTED_SECRET}
New-Item -ItemType Directory -Force -Path $backupDir | Out-Null
docker inspect open-webui-clean > (Join-Path $backupDir 'open-webui-clean.inspect.json')
docker logs --tail 200 open-webui-clean > (Join-Path $backupDir 'open-webui-clean.logs.tail.txt') 2>&1

${REDACTED_SECRET}
  Where-Object { $_ -match '^API_SERVER_KEY=' } |
  Select-Object -First 1) -replace '^API_SERVER_KEY=', ''
if ([string]::IsNullOrWhiteSpace($key)) { throw 'API_SERVER_KEY missing' }

docker rm -f open-webui-clean | Out-Null
docker run -d --name open-webui-clean --restart always `
  -p 3000:8080 `
  -v open-webui-clean:/app/backend/data `
  -e OPENAI_API_BASE_URL='http://host.docker.internal:8642/v1' `
  -e OPENAI_API_KEY=$key `
  -e USE_OLLAMA_DOCKER=false `
  -e ANONYMIZED_TELEMETRY=false `
  -e DO_NOT_TRACK=true `
  ghcr.io/open-webui/open-webui:main | Out-Null
```

Wait for health, then rerun G02. Expected result is `STATUS 200` and
`HAS_HERMES_AGENT True`.

## G03 Fix Open WebUI Database Connection And Default Model

Even after the container env is fixed, Open WebUI may prefer saved database
connection settings. Its connection page can still show no selected model if
`openai.api_configs.0.model_ids` is empty. Set both the saved connection key and
the default model to `hermes-agent`.

```powershell
$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
docker exec open-webui-clean cp /app/backend/data/webui.db /app/backend/data/webui.db.bak-hermes-direct-$stamp

${REDACTED_SECRET}
  Where-Object { $_ -match '^API_SERVER_KEY=' } |
  Select-Object -First 1) -replace '^API_SERVER_KEY=', ''
if ([string]::IsNullOrWhiteSpace($apiKey)) { throw 'API_SERVER_KEY missing' }

$code = @'
import os, sqlite3, json, time
p = '/app/backend/data/webui.db'
key = os.environ['HERMES_API_SERVER_KEY']
con = sqlite3.connect(p)
cur = con.cursor()
row = cur.execute('select id, data from config order by id limit 1').fetchone()
if not row:
    raise SystemExit('config row missing')
id_, raw = row
data = json.loads(raw)

openai = data.setdefault('openai', {})
openai['enable'] = True
openai['api_base_urls'] = ['http://host.docker.internal:8642/v1']
openai['api_keys'] = [key]
openai['api_configs'] = {'0': {'enable': True, 'model_ids': ['hermes-agent']}}

ollama = data.setdefault('ollama', {})
ollama['enable'] = False

ui = data.setdefault('ui', {})
ui['default_models'] = 'hermes-agent'
ui['default_pinned_models'] = 'hermes-agent'

cur.execute(
    'update config set data=?, updated_at=? where id=?',
    (json.dumps(data, ensure_ascii=False), time.strftime('%Y-%m-%d %H:%M:%S'), id_),
)
con.commit()
print('OPENWEBUI_CONNECTION_FIXED')
print('OPENAI_BASES', data['openai']['api_base_urls'])
print('CONNECTION_MODEL_IDS', data['openai']['api_configs']['0']['model_ids'])
print('UI_DEFAULT_MODELS', data['ui']['default_models'])
'@

$code | docker exec -i -e HERMES_API_SERVER_KEY=$apiKey open-webui-clean python -
docker restart open-webui-clean
```

Success criteria:

- Backup exists in the Open WebUI volume:
  `/app/backend/data/webui.db.bak-hermes-direct-<timestamp>`.
- Output shows `CONNECTION_MODEL_IDS ['hermes-agent']`.
- Output shows `UI_DEFAULT_MODELS hermes-agent`.

Rollback:

```powershell
docker exec open-webui-clean sh -lc 'cp /app/backend/data/webui.db.bak-hermes-direct-YYYYMMDD-HHMMSS /app/backend/data/webui.db'
docker restart open-webui-clean
```

Replace the suffix with the actual backup timestamp.

## G04 Final Verification

```powershell
$deadline = (Get-Date).AddSeconds(180)
do {
  $state = docker inspect open-webui-clean --format '{{.State.Status}}|{{if .State.Health}}{{.State.Health.Status}}{{end}}' 2>$null
  if ($state) { "STATE=$state" }
  if ($state -match '^running\|(healthy|)$') { break }
  Start-Sleep -Seconds 5
} while ((Get-Date) -lt $deadline)

$code = @'
import os, urllib.request, sqlite3, json
base = os.environ['OPENAI_API_BASE_URL']
key = os.environ['OPENAI_API_KEY']
req = urllib.request.Request(base.rstrip('/') + '/models', headers={'Authorization': 'Bearer ' + key})
with urllib.request.urlopen(req, timeout=30) as r:
    body = r.read().decode('utf-8', 'replace')
    print('MODELS_STATUS', r.status)
    print('HAS_HERMES_AGENT', 'hermes-agent' in body)
con = sqlite3.connect('/app/backend/data/webui.db')
data = json.loads(con.execute('select data from config order by id limit 1').fetchone()[0])
print('CONNECTION_MODEL_IDS', data.get('openai', {}).get('api_configs', {}).get('0', {}).get('model_ids'))
print('UI_DEFAULT_MODELS', data.get('ui', {}).get('default_models'))
print('UI_DEFAULT_PINNED_MODELS', data.get('ui', {}).get('default_pinned_models'))
'@
$code | docker exec -i open-webui-clean python -

$page = Invoke-WebRequest -Uri 'http://127.0.0.1:3000/admin/settings/connections' -UseBasicParsing -TimeoutSec 60
"CONNECTIONS_PAGE_STATUS=$([int]$page.StatusCode)"

${REDACTED_SECRET}
```

Expected evidence:

- `MODELS_STATUS 200`
- `HAS_HERMES_AGENT True`
- `CONNECTION_MODEL_IDS ['hermes-agent']`
- `UI_DEFAULT_MODELS hermes-agent`
- `CONNECTIONS_PAGE_STATUS=200`
- Auto-recovery log contains:
  `FINAL_PASS Hermes DeepSeek Open WebUI auto-recovery complete`

If the current browser tab still shows no model after this passes, refresh the
page or start a new chat. The server-side default and connection are already
set; an old tab can keep a stale empty selection in client state.

## Auto-Recovery Script Requirements

${REDACTED_SECRET}
Hermes/Open WebUI direct mode for this setup:

- Do not require New API `3001`.
- Start Docker only to keep `open-webui-clean` available.
- Check Hermes `/health` and `/v1/models` with
  `Authorization: Bearer <API_SERVER_KEY>`.
- Check Open WebUI `http://127.0.0.1:3000`.
- `-FullProbe` should call Hermes chat with `hermes-agent`.
- Success line should be:
  `FINAL_PASS Hermes DeepSeek Open WebUI auto-recovery complete`.

Automatic login persistence should include:

- Startup folder entry:
${REDACTED_SECRET}
- Scheduled task:
  `HermesNewApiAutoRecover_Logon` in `Ready` state.


