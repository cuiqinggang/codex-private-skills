---
name: hermes-014-windows-native-8642
description: Use when validating, repairing, documenting, or repeating the Windows native Hermes 0.14 official daily route on port 8642 with C:\Users\A\.hermes, OpenAI-compatible endpoints, and Open WebUI smoke tests.
---

# Windows Native Hermes 0.14 Official 8642 Route

## 当前恢复优先入口（2026-10-14）

本页0.14、H盘和模型名记录为历史快照。当前启动/开机故障先读 [爱马仕Docker启动恢复实证](../windows-hermes-operations/references/docker-startup-recovery-20261014.md)：现用启动器已迁C盘，运行版本实测0.21.5；授权模型列表发现真实ID，401不等于超时，8642健康而3000异常先查Docker。不以本次热启动替代重启验收；不得盲目覆盖当前安装。

## Core Rule

Use the official Windows native data path and port:

- Data path: `C:\Users\A\.hermes`
- Executable: `H:\Hermes_Windows_Native_014\venv\Scripts\hermes.exe`
- Daily endpoint: `http://127.0.0.1:8642`
- OpenAI-compatible model id: discover from `/v1/models`; the verified id on 2026-05-19 was `hermes-agent`.

Do not return to the old `H:\Hermes_Windows_Native_014\runtime` or `18642` route unless a future task explicitly asks for it.

## Safety Rules

- Do not print API key, token, or password values.
- Do not run `install.ps1`, `git clone`, reinstall Hermes, or run `hermes setup` unless the user explicitly approves after a diagnostic proves it is needed.
- Do not modify Open WebUI configuration during Hermes endpoint verification.
- Do not migrate memory or sessions during smoke tests.
- Do not kill a fixed PID; identify the owner of port `8642` first.

## Verification Sequence

1. Check the executable:

```powershell
H:\Hermes_Windows_Native_014\venv\Scripts\hermes.exe --version
```

2. Check official diagnostics:

```powershell
H:\Hermes_Windows_Native_014\venv\Scripts\hermes.exe config check
H:\Hermes_Windows_Native_014\venv\Scripts\hermes.exe doctor
```

3. Check health:

```powershell
Invoke-WebRequest -Uri 'http://127.0.0.1:8642/health' -UseBasicParsing
```

4. Discover the model id. Do not guess:

```powershell
Invoke-WebRequest -Uri 'http://127.0.0.1:8642/v1/models' -UseBasicParsing
```

5. Use the returned model id for Chat Completions. The verified id was `hermes-agent`:

```powershell
$body = @{
  model = 'hermes-agent'
  messages = @(@{ role = 'user'; content = '只回复：HERMES_014_WINDOWS_NATIVE_MAIN_OK' })
  stream = $false
} | ConvertTo-Json -Depth 8 -Compress

Invoke-WebRequest `
  -Uri 'http://127.0.0.1:8642/v1/chat/completions' `
  -Method Post `
  -ContentType 'application/json; charset=utf-8' `
  -Body ([System.Text.Encoding]::UTF8.GetBytes($body)) `
  -UseBasicParsing
```

## PASS Evidence

Read `references/pass-evidence-20260519.md` when exact PASS evidence is needed.

Confirmed on 2026-05-19:

- `GET /health`: HTTP 200, platform `hermes-agent`
- `GET /v1/models`: HTTP 200, returned `hermes-agent`
- `POST /v1/chat/completions`: HTTP 200, returned `HERMES_014_WINDOWS_NATIVE_MAIN_OK`
- Open WebUI at `http://127.0.0.1:3000` returned `HERMES_OPENWEBUI_014_OK` through model `hermes-agent`
- Open WebUI was not modified
- Memory and sessions were not migrated
- Secret values were not printed

## Common Failure

If `/v1/chat/completions` returns a generic Hermes greeting, first check whether the request used a guessed model name. Fix the test by calling `/v1/models` and using the returned id, currently `hermes-agent`.

## Daily Startup After Reboot

Read `references/daily-startup-after-reboot.md` for the full Chinese operator guide and bundled-file map.

Use this file for the normal next-day startup:

```text
H:\Hermes_Windows_Native_014\明天重启后打开爱马仕页面.cmd
```

ASCII fallback:

```text
H:\Hermes_Windows_Native_014\START-HERMES-WEBUI.cmd
```

It calls:

```powershell
H:\Hermes_Windows_Native_014\launcher\start-hermes-openwebui.ps1
```

The script waits in this order:

```text
Hermes 8642 health
-> Docker Desktop API
-> Open WebUI 3000 health
-> browser page
```

Run this non-opening check when verifying from Codex:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "H:\Hermes_Windows_Native_014\launcher\启动Windows原生爱马仕页面.ps1" -NoOpen
```

Expected final line:

```text
FINAL_PASS Windows native Hermes page is ready
```

Bundled copies inside this skill package:

```text
scripts/start-hermes-openwebui.ps1
scripts/明天重启后打开爱马仕页面.cmd
scripts/START-HERMES-WEBUI.cmd
references/daily-startup-after-reboot.md
references/使用说明-明天重启后打开爱马仕页面.txt
```

Use the bundled scripts as reference copies. The live daily-use files remain under `H:\Hermes_Windows_Native_014\`.
