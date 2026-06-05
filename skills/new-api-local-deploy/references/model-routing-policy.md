# Hermes Model Routing Policy

Use this reference when Hermes, Telegram, Open WebUI, or New API appears to route complex work to a cheap model, especially `deepseek-v4-flash`.

## Core Rule

Complex work must route to `deepseek-v4-pro`.

Flash is allowed only when the user explicitly asks for cheap, fast, low-cost, simple, or casual handling. Do not hide Flash usage from the user. If the user asks which model is running, answer from current runtime evidence, not from an old assumption.

## Task Classes

Route to `deepseek-v4-pro` for:

- Search, research, source comparison, or "find mature/common tools".
- Installing software, repairing failed installs, or trying alternate setup routes.
- Debugging, troubleshooting, integration, deployment, or configuration.
- Multi-step planning, code planning, architecture, automation, or long-running tasks.
- Capability gap filling, tool choice, model routing, and "continue until it works" tasks.
- Any task where a wrong choice can waste significant time or corrupt local configuration.

Allow `deepseek-v4-flash` only for:

- Explicit "use Flash", "cheap model", "low cost", or "fast mode" requests.
- Short factual checks, simple summaries, casual chat, or low-risk one-turn questions.
- Compression or other auxiliary tasks already isolated from decision-making.

## Current Local Targets

- Hermes default model should be `deepseek-v4-pro`.
- Hermes base URL should be `http://127.0.0.1:3001/v1`.
- Telegram router plugin path: `C:\Users\A\.hermes\plugins\telegram_model_router`.
- Plugin behavior: complex trigger words force `deepseek-v4-pro`; Flash requires explicit low-cost/fast/simple trigger words.
- New API logs are the source of truth for actual upstream model use.

## G01 Inspect Current Routing

Purpose: prove the configured model and router plugin before changing anything.

Execution location: `C:\Users\A\Desktop\1`

Command:

```powershell
$cfg = 'C:\Users\A\.hermes\config.yaml'
$i = 0
Get-Content -LiteralPath $cfg | ForEach-Object {
  $i++
  if ($_ -match '(?i)(api[_-]?key|token|secret|password|bearer)') {
    '{0,4}: {1}' -f $i, ($_ -replace '(:\s*).*','$1<redacted>')
  } else {
    '{0,4}: {1}' -f $i, $_
  }
}

Get-Content -LiteralPath 'C:\Users\A\.hermes\plugins\telegram_model_router\plugin.yaml'
python -m py_compile 'C:\Users\A\.hermes\plugins\telegram_model_router\__init__.py'
```

Success criteria:

- `model.default` is `deepseek-v4-pro`.
- `model.base_url` is `http://127.0.0.1:3001/v1`.
- `telegram_model_router` is enabled in `plugins.enabled`.
- Plugin compiles.

Failure recovery:

- Back up the affected file before edits.
- Do not print secrets from `.env`, `auth.json`, or `config.yaml`.

## G02 Router Unit Test

Purpose: prove policy behavior without sending a real Telegram message.

Execution location: `C:\Users\A\Desktop\1`

Command:

```powershell
@'
import importlib.util
from pathlib import Path

p=Path(r'C:\Users\A\.hermes\plugins\telegram_model_router\__init__.py')
spec=importlib.util.spec_from_file_location('telegram_model_router_test', p)
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class Platform:
    value='telegram'
class Source:
    platform=Platform()
class Event:
    source=Source()
    def __init__(self,text): self.text=text
class Gateway:
    def __init__(self):
        self._session_model_overrides={}
        self._pending_model_notes={}
        self.evicted=0
    def _session_key_for_source(self, source): return 'telegram:test'
    def _evict_cached_agent(self, session_key): self.evicted += 1

def run(text):
    g=Gateway()
    result=mod._route_telegram_model(event=Event(text), gateway=g)
    override=g._session_model_overrides.get('telegram:test')
    return result, override, g._pending_model_notes.get('telegram:test'), g.evicted

complex_text = '\u8bf7\u641c\u7d22\u5e76\u5b89\u88c5\u5408\u9002\u5de5\u5177\uff0c\u628a\u8fd9\u4e2a\u590d\u6742\u4efb\u52a1\u8865\u9f50'
flash_text = '\u7528Flash \u968f\u4fbf\u95ee\u95ee\u4eca\u5929\u72b6\u6001'
normal_text = '\u4f60\u597d'

cases = [
    (complex_text, mod.PRO_MODEL),
    (flash_text, mod.FLASH_MODEL),
    (normal_text, None),
]
for text, expected in cases:
    result, override, note, evicted = run(text)
    model = override.get('model') if isinstance(override, dict) else None
    print('MODEL=', model, 'EXPECTED=', expected, 'RESULT=', result, 'EVICTED=', evicted)
    assert model == expected, (text, expected, model)

print('ROUTER_UNIT=PASS')
'@ | python -
```

Success criteria:

- Complex task text routes to `deepseek-v4-pro`.
- Explicit Flash text routes to `deepseek-v4-flash`.
- Normal text has no plugin override and therefore uses Hermes default, which should be Pro.

## G03 Restart Hermes Gateway

Purpose: load changed router code in the running gateway.

Execution location: `C:\Users\A\Desktop\1`

Command:

```powershell
$owner = Get-NetTCPConnection -LocalPort 8642 -State Listen -ErrorAction Stop | Select-Object -First 1
$proc = Get-CimInstance Win32_Process -Filter "ProcessId=$($owner.OwningProcess)"
"CURRENT_8642_PID=$($owner.OwningProcess)"
"CURRENT_8642_CMD=$($proc.CommandLine)"
if ($proc.CommandLine -notmatch [regex]::Escape('H:\Hermes_Windows_Native_014')) {
  throw "Refusing to stop 8642 owner outside Windows Hermes: $($proc.CommandLine)"
}
Stop-Process -Id $owner.OwningProcess -Force
Start-Sleep -Seconds 3
cmd.exe /c "H:\Hermes_Windows_Native_014\START-HERMES-WEBUI.cmd"
```

Success criteria:

- Launcher exits with code 0.
- Latest daily-start log ends with `FINAL_PASS Windows native Hermes page is ready`.

Failure recovery:

- Inspect the latest log in `H:\Hermes_Windows_Native_014\reports`.
- Use `windows-hermes-operations` for startup recovery.

## G04 Verify Actual Model Use

Purpose: prove the actual upstream model from New API logs, not from assistant self-report.

Execution location: `C:\Users\A\Desktop\1`

Command:

```powershell
$body = @{
  model='hermes-agent'
  messages=@(@{role='user'; content='Please answer only: ROUTE_PRO_CHECK. This is a complex task involving search, installation, debugging, planning, and tool selection.'})
  stream=$false
} | ConvertTo-Json -Depth 8
$r = Invoke-WebRequest -Uri 'http://127.0.0.1:8642/v1/chat/completions' `
  -Method Post -ContentType 'application/json' -Body $body `
  -UseBasicParsing -TimeoutSec 180
"HERMES_CHAT_STATUS=$([int]$r.StatusCode)"
$r.Content

Start-Sleep -Seconds 2
Set-Location -LiteralPath 'C:\Users\A\new-api-local'
docker compose logs --tail 80 new-api 2>&1 |
  Select-String -Pattern 'model_name|chat/completions|deepseek-v4' -CaseSensitive:$false |
  Select-Object -Last 30
```

Success criteria:

- Hermes chat returns HTTP `200`.
- New API logs for the chat completion include `model_name":"deepseek-v4-pro"`.

Failure criteria:

- Logs show `model_name":"deepseek-v4-flash"` for a complex task.
- Logs show `client_gone`, timeout, or zero completion tokens for the final request.

Failure recovery:

- Re-check `C:\Users\A\.hermes\config.yaml` default model.
- Re-check `telegram_model_router` plugin and restart Hermes.
- Do not rely on the assistant's self-reported model without New API log evidence.
