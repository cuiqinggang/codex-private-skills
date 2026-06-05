# DeepSeek V4 Flash OpenClaw Repair Record - 2026-05-25

Use this record when Xiaolongxia/OpenClaw needs to be restored to the single active DeepSeek V4 Flash route, or when a future run sees model confusion, stale NVIDIA/OpenRouter fallback state, `No response from OpenClaw`, or visible identity drift such as "I am GPT-4o".

Do not store or print API keys. The DeepSeek key lives only in:

`C:\Users\A\xiaolongxia-free-api-local\secrets\deepseek_api_key.txt`

## Starting Problem

The user wanted to stop using slow or unstable free/NVIDIA routes and use only the paid official DeepSeek V4 Flash route.

The operational target was:

```text
OpenClaw / Xiaolongxia gateway 18789
  -> deepseek-official
  -> deepseek-v4-flash
```

Runtime fallbacks had to be removed. NVIDIA 70B, NVIDIA 8B, OpenRouter free models, and 3011 New API were kept only as history unless the user explicitly re-enables them.

## Safety Boundary

- Do not modify Hermes / AiMaShi.
- Do not modify Open WebUI.
- Do not modify old 3001 New API.
- Do not modify 3011 New API/model pool for this route.
- Do not connect real group chats.
- Do not use `--deliver`.
- Do not print the DeepSeek key.
- Do not write the DeepSeek key into reports, skills, or `openclaw.json`.

## Configuration That Worked

OpenClaw config path:

`C:\Users\A\.openclaw\openclaw.json`

Working summary:

- `agents.defaults.model.primary`: `deepseek-official/deepseek-v4-flash`
- `agents.defaults.model.fallbacks`: empty array
- `models.mode`: `replace`
- configured provider ids: `deepseek-official` only
- configured model ids: `deepseek-v4-flash` only
- gateway bind: loopback
- gateway port: `18789`
- channel sending: disabled
- key storage: SecretRef/file path, not plaintext

The config must validate with:

```powershell
C:\Users\A\AppData\Roaming\npm\openclaw.cmd config validate
```

Expected stdout:

```text
Config valid: ~\.openclaw\openclaw.json
```

## Exact Recovery Sequence

### G01 Check Current Config

Verify the current config state without printing secrets:

```powershell
$cfg='C:\Users\A\.openclaw\openclaw.json'
$raw=Get-Content -Raw -LiteralPath $cfg
$json=$raw | ConvertFrom-Json
[pscustomobject]@{
  Primary=$json.agents.defaults.model.primary
  FallbackCount=@($json.agents.defaults.model.fallbacks).Count
  Mode=$json.models.mode
  Providers=@($json.models.providers.PSObject.Properties.Name) -join ', '
  PlainKeyInConfig=($raw -match 'sk-[A-Za-z0-9]')
}
```

Expected:

- primary is `deepseek-official/deepseek-v4-flash`
- fallback count is `0`
- mode is `replace`
- provider list is `deepseek-official`
- `PlainKeyInConfig` is false

### G02 Restart Gateway

Stop stale 18789 listeners first, then start OpenClaw gateway:

```powershell
Get-NetTCPConnection -LocalPort 18789 -ErrorAction SilentlyContinue |
  ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }

Start-Process -FilePath 'C:\Users\A\AppData\Roaming\npm\openclaw.cmd' `
  -ArgumentList @('gateway','run','--force','--allow-unconfigured','--bind','loopback','--port','18789','--verbose') `
  -WindowStyle Hidden
```

Expected gateway log evidence:

```text
[gateway] agent model: deepseek-official/deepseek-v4-flash (thinking=off, fast=off)
[gateway] ready
```

### G03 Health Check

Use:

```powershell
C:\Users\A\AppData\Roaming\npm\openclaw.cmd gateway health --json --timeout 20000
Invoke-WebRequest -UseBasicParsing 'http://127.0.0.1:18789/'
```

Expected:

- health `ok: true`
- root HTTP status `200`
- title `OpenClaw Control`

### G04 Provider Transport Test

This is the reliable model transport acceptance check:

```powershell
C:\Users\A\AppData\Roaming\npm\openclaw.cmd infer model run `
  --gateway `
  --model 'deepseek-official/deepseek-v4-flash' `
  --prompt '请只回复：XLX_DEEPSEEK_INFER_GATEWAY_OK_20260525' `
  --json
```

Expected:

- JSON `ok: true`
- provider `deepseek-official`
- model `deepseek-v4-flash`
- output contains the marker

The local transport check also passed:

```powershell
C:\Users\A\AppData\Roaming\npm\openclaw.cmd infer model run `
  --local `
  --model 'deepseek-official/deepseek-v4-flash' `
  --prompt '请只回复：XLX_DEEPSEEK_INFER_LOCAL_OK_20260525' `
  --json
```

### G05 Agent Behavior Test

This is the reliable Xiaolongxia/OpenClaw agent acceptance check:

```powershell
C:\Users\A\AppData\Roaming\npm\openclaw.cmd agent `
  --agent main `
  --message '请只回复：XLX_DEEPSEEK_AGENT_MAIN_OK_20260525' `
  --model 'deepseek-official/deepseek-v4-flash' `
  --thinking off `
  --timeout 180 `
  --json
```

Important: include `--agent main`. Without it, OpenClaw can fail with:

```text
No target session selected. Use --agent <id>, --session-id <id>, or --to <E.164>.
```

Expected:

- exit code `0`
- marker returned
- no `--deliver`
- no real message sent

## Failed or Misleading Paths

### 1. `Start-Process openclaw`

PowerShell can choose the wrong executable entry and fail with:

```text
%1 is not a valid Win32 application.
```

Use the explicit command shim:

`C:\Users\A\AppData\Roaming\npm\openclaw.cmd`

### 2. `/v1/chat/completions` with `model=openclaw/main`

This path reached DeepSeek and returned HTTP 200 at the provider layer, but the OpenClaw embedded agent emitted `NO_REPLY`, causing the OpenAI-compatible wrapper to return:

```text
No response from OpenClaw.
```

This is not proof that DeepSeek is broken. The log showed:

- provider `deepseek-official`
- model `deepseek-v4-flash`
- request to `https://api.deepseek.com/chat/completions`
- provider HTTP status `200`
- then `NO_REPLY` in the embedded agent path

Do not use `/v1/chat/completions` as the primary acceptance path for this route. Use `infer model run --gateway` and `agent --agent main`.

### 3. Missing `--agent main`

`openclaw agent --message ...` without target selection fails. Add `--agent main`.

### 4. Visible Identity Drift

If the visible page says it is GPT-4o, treat that as identity/prompt drift, not routing proof. Verify actual model route from:

- `openclaw.json`
- gateway log line `agent model: deepseek-official/deepseek-v4-flash`
- `infer model run --gateway`
- `agent --agent main`

## Evidence Root

Main evidence directory:

`C:\Users\A\Desktop\1\output\XIAOLONGXIA-DEEPSEEK-V4-FLASH-OPENCLAW-CONNECT-20260525`

Key files:

- `G01-config-state.json`
- `G01-openclaw-config-validate.stdout.txt`
- `G02-gateway-start-summary.json`
- `G02-gateway-deepseek.stdout.log`
- `G03-gateway-health.json`
- `G03-infer-local-summary.json`
- `G03-infer-gateway-summary.json`
- `G03-openclaw-agent-main-summary.json`
- `G03-final-config-summary.json`
- `G04-secret-scan-and-scrub.json`
- `final-report.md`

Final status:

`XIAOLONGXIA_DEEPSEEK_V4_FLASH_OPENCLAW_CONNECT_PASS`

## Actual Use Retest After User Suspicion

After the user reported that the visible Xiaolongxia/OpenClaw page still did not answer, a second actual-use test was run. This test is important because marker success alone was not enough to prove the visible route was practical.

Evidence directory:

`C:\Users\A\Desktop\1\output\XIAOLONGXIA-DEEPSEEK-V4-FLASH-ACTUAL-USE-TEST-20260525`

Bundled evidence copy:

`references\deepseek-v4-flash-actual-use-20260525`

### What Passed

Direct DeepSeek selftest:

- Script: `C:\Users\A\xiaolongxia-free-api-local\scripts\xiaolongxia-deepseek-v4-flash-direct-selftest.ps1 -Mode quick`
- Result: 2/2 passed.
- Average API latency: about `914 ms`.
- Wall-clock runtime: about `4238 ms`.
- Conclusion: the DeepSeek official API key/model route itself was healthy and fast enough.

OpenClaw infer through gateway:

- Command family: `openclaw.cmd infer model run --gateway --model deepseek-official/deepseek-v4-flash ... --json`
- Result: passed and returned Chinese text.
- Latency: about `69429 ms`.
- Conclusion: OpenClaw gateway transport could call DeepSeek, but was too slow for practical browser use.

OpenClaw agent actual-use prompt:

- Command family: `openclaw.cmd agent --agent main --message ... --model deepseek-official/deepseek-v4-flash --thinking off --timeout 240 --json`
- Result: passed and returned useful Chinese text.
- Latency: about `178414 ms`.
- Conclusion: the OpenClaw agent route could answer, but the latency was unacceptable for normal Xiaolongxia chat operation.

### Root Cause Clarification

The failure seen by the user was not caused by a bad DeepSeek key or an unavailable DeepSeek model. The direct official DeepSeek path was fast and successful.

The practical problem was the OpenClaw browser/agent/gateway layer:

- it added large overhead;
- the visible page could appear idle or disconnected while commands still eventually finished;
- the dashboard/session path sometimes produced tool-call style output or `NO_REPLY`;
- marker-only tests were too weak to certify real use.

### Updated Acceptance Rule

Do not claim Xiaolongxia/OpenClaw browser use is ready only because a marker test passed.

Use three separate gates:

1. Direct provider gate: DeepSeek official API returns useful text quickly.
2. OpenClaw transport gate: `infer model run --gateway` returns the marker.
3. Practical-use gate: a real Chinese parent-group prompt returns useful text within an acceptable latency window.

Recommended latency thresholds:

- Direct DeepSeek quick selftest: normally under `5 s`.
- OpenClaw browser or agent practical use: should be under `15-30 s` for normal use.
- If OpenClaw agent takes around `70-180 s`, treat it as connected but not practical.

### Recommended Next Fix Route

For real Xiaolongxia use, prefer the lightweight direct DeepSeek route or a stripped-down Xiaolongxia provider wrapper. Do not route ordinary Xiaolongxia replies through a heavy OpenClaw browser/agent session unless a fresh practical-use test proves the latency is acceptable.

Preserve the OpenClaw DeepSeek config as a known working transport fallback, but do not use it as the only proof of user-visible readiness.

## What To Do Next Time

1. Do not re-explore NVIDIA/OpenRouter unless requested.
2. Check `openclaw.json` first.
3. Confirm gateway log says `deepseek-official/deepseek-v4-flash`.
4. Run `infer model run --gateway`.
5. Run `agent --agent main`.
6. Run the direct DeepSeek quick selftest.
7. Run one real Chinese actual-use prompt and record latency.
8. Do not use `/v1/chat/completions` as the main proof.
9. Do a secret scan before reporting.

Secret scan pattern:

```powershell
Select-String -Path '<report-or-skill-path>' -Pattern 'sk-[A-Za-z0-9]{20,}'
```
