# 2026-06-17 API Server Streaming Config Cleanup

## Value Judgment

HIGH_VALUE.

This incident records a failure mode where Hermes looked healthy on
`/health`, `/v1/models`, gateway state, and Telegram polling, but real browser
or API answers were slow, stalled, or timed out after a Telegram-side automated
config edit and gateway restart. Future repairs must not stop at health checks.

## Trigger Phrases

Use this note when:

- The user says browser/Open WebUI answers are very slow, blank, or appear not
  to answer, while Telegram feels faster.
${REDACTED_SECRET}
  said "restart gateway to take effect".
- Restart appears successful, but `http://127.0.0.1:8642/v1/chat/completions`
  times out.
- `/health` and `/v1/models` pass, but real user questions do not answer.
- `config.yaml` contains duplicated blocks around `display`, `platforms`,
  `api_server`, `streaming`, or other repeated YAML sections.

## Critical Lessons

1. Do not treat `/health` as enough. It only proves the HTTP server is alive.
2. Do not treat `gateway_state.json` connected states as enough.
3. Always test a real `/v1/chat/completions` call after gateway restart.
4. For browser perceived speed, test streaming first chunk latency, not only
   total response time.
5. If a Telegram-side agent edits config, inspect the resulting YAML before
   trusting it. In this incident the file still parsed, but the raw file had
   repeated blocks and was dangerous for future edits.
6. `hermes gateway status --deep` can temporarily misreport while a real
   listener exists. Verify the actual listener process on `127.0.0.1:8642`.

## Boundaries

- Do not print `API_SERVER_KEY`, Telegram bot token, provider API keys, or other
  secrets.
- Do not change Windows proxy or FlClash settings for this symptom.
- Do not edit `config.yaml` without a timestamped backup.
- Do not allow a Telegram-side agent to keep patching security-sensitive config
  blindly after the first failure.

## Repair Ladder

### G01 - Confirm Narrow Layer

Run the standard Telegram diagnostic:

```powershell
${REDACTED_SECRET}
```

If it passes but the user still reports no answer or slow browser response,
continue. The likely failure is not Telegram polling or port startup.

### G02 - Check the Silent 8642 Lifeline

The 1-minute lifeline is:

```text
Task Scheduler: Hermes8642SilentHealthCheck
${REDACTED_SECRET}
```

Verify:

```powershell
Get-ScheduledTaskInfo -TaskName Hermes8642SilentHealthCheck |
  Select-Object LastRunTime,LastTaskResult,NextRunTime,NumberOfMissedRuns

${REDACTED_SECRET}
```

In the incident, the task correctly detected failed health at 10:15 and
recovered 8642 by 10:15:57.

### G03 - Check the Real Listener

Do not rely only on `hermes gateway status --deep`.

```powershell
Get-NetTCPConnection -LocalAddress 127.0.0.1 -LocalPort 8642 -State Listen |
  ForEach-Object {
    $p=Get-CimInstance Win32_Process -Filter "ProcessId=$($_.OwningProcess)"
    [pscustomobject]@{PID=$_.OwningProcess; CommandLine=$p.CommandLine}
  }
```

Expected listener command includes:

```text
H:\Hermes_Windows_Native_014\venv\Scripts\hermes.exe gateway run --replace
```

### G04 - Inspect Config for Duplicate or Unsafe Blocks

Raw grep may look alarming because duplicate YAML keys collapse during parsing.
Use a YAML parser to inspect the effective config, then clean the file if raw
blocks are duplicated.

```powershell
@'
from pathlib import Path
import yaml
${REDACTED_SECRET}
data=yaml.safe_load(p.read_text(encoding='utf-8'))
print(yaml.safe_dump({
  'display_platforms': data.get('display',{}).get('platforms',{}),
  'gateway': data.get('gateway',{})
}, allow_unicode=True, sort_keys=False))
'@ | python -
```

Required effective state:

```yaml
display_platforms:
  telegram:
    streaming: true
  discord:
    streaming: false
  api_server:
    streaming: true
gateway:
  port: 8642
```

### G05 - Backup and Normalize Config

Back up first:

```powershell
$stamp=Get-Date -Format 'yyyyMMdd-HHmmss'
${REDACTED_SECRET}
${REDACTED_SECRET}
```

Normalize through YAML parsing, preserving effective values but forcing the
platform streaming settings:

```powershell
@'
from pathlib import Path
import yaml
${REDACTED_SECRET}
data = yaml.safe_load(p.read_text(encoding='utf-8'))
display = data.setdefault('display', {})
platforms = display.setdefault('platforms', {})
for name, streaming in [('telegram', True), ('discord', False), ('api_server', True)]:
    node = platforms.setdefault(name, {})
    if not isinstance(node, dict):
        node = {}
        platforms[name] = node
    node['streaming'] = streaming
p.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False, default_flow_style=False), encoding='utf-8')
print('OK')
'@ | python -
```

Incident backup example:

```text
${REDACTED_SECRET}
```

### G06 - Restart Gateway Carefully

Use the normal launcher, then verify the actual listener:

```powershell
H:\Hermes_Windows_Native_014\venv\Scripts\hermes.exe gateway stop
cmd.exe /c "H:\Hermes_Windows_Native_014\START-HERMES-WEBUI.cmd"
```

If duplicate gateway processes remain, identify the real listener first and
avoid killing the current shell. Stop stale non-listening `hermes.exe gateway
run` Python processes only after confirming the listener PID.

### G07 - Acceptance Tests

Health and models:

```powershell
Invoke-RestMethod -Uri 'http://127.0.0.1:8642/health' -TimeoutSec 15
Invoke-RestMethod -Uri 'http://127.0.0.1:8642/v1/models' -Headers $headers -TimeoutSec 15
```

Real non-streaming chat:

```powershell
$body=@{
  model='hermes-agent'
  messages=@(@{role='user';content='网页端非流式速度测试：请用一句话回答状态正常。'})
} | ConvertTo-Json -Depth 6
Invoke-RestMethod -Uri 'http://127.0.0.1:8642/v1/chat/completions' `
  -Method Post -Headers $headers -ContentType 'application/json' -Body $body -TimeoutSec 180
```

Streaming first chunk:

```python
import requests, time
payload = {
  "model": "hermes-agent",
  "stream": True,
  "messages": [{"role": "user", "content": "网页端速度测试：请用三句话说明今天状态正常。"}],
}
start=time.time()
with requests.post("http://127.0.0.1:8642/v1/chat/completions", headers=headers, json=payload, stream=True, timeout=180) as r:
    r.raise_for_status()
    for line in r.iter_lines(decode_unicode=True):
        if line:
            print("first_chunk_seconds", round(time.time()-start, 3))
            break
```

Open WebUI front page:

```powershell
$sw=[Diagnostics.Stopwatch]::StartNew()
$r=Invoke-WebRequest -Uri 'http://127.0.0.1:3000' -UseBasicParsing -TimeoutSec 20
$sw.Stop()
[pscustomobject]@{status=$r.StatusCode; elapsed_ms=[math]::Round($sw.Elapsed.TotalMilliseconds)}
```

## 2026-06-17 Passing Evidence

- `http://127.0.0.1:8642/health`: `status=ok`, `platform=hermes-agent`.
- `http://127.0.0.1:8642/v1/models`: contained `hermes-agent`.
- Real non-streaming short answer returned in about 4.74 seconds.
- Streaming first chunk returned in about 0.023 seconds.
- Open WebUI `http://127.0.0.1:3000` returned HTTP 200 in about 0.8 seconds.
- Telegram diagnostic returned PASS.
- `Hermes8642SilentHealthCheck` existed and had `LastTaskResult=0`.

## Next-Run Reuse Instruction

For any future "browser is slow / Telegram is fast / restart after config edit
made Hermes stop answering" report, start here after the standard diagnostic.
Fix the config file structure and run real chat plus streaming tests before
declaring recovery.
