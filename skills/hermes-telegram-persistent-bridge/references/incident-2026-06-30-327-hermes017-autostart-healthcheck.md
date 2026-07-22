# 2026-06-30 327 Hermes 0.17 Autostart and 8642 Healthcheck Merge

## Use When

Use this when a 327.zip-style handoff mentions Hermes 0.17, OpenRouter
GLM-5.2, Telegram, Open WebUI, startup repair, or a drive-letter change from
the old `H:\Hermes_Windows_Native_014` path to `K:\Hermes_Windows_Native_014`.

Use it especially when:

- `K:\Hermes_Windows_Native_014\venv\Scripts\hermes.exe` exists, but
  `http://127.0.0.1:8642/health` fails.
- `gateway_state.json` says connected, but its timestamp is old.
- `Hermes8642SilentHealthCheck` logs `launcher missing:
  H:\Hermes_Windows_Native_014\launcher\hermes-014-runtime.ps1`.
- A scheduled task shows `Running`, but no real 8642 listener exists.

## 327.zip Review Result

${REDACTED_SECRET}
material, but it is not a complete installable Codex skill package by itself.
It contains `memory/` and `rules/` files, not a top-level `SKILL.md`, scripts,
or a ready manifest.

Do not copy the whole package into this skill. Keep this skill lightweight and
link to the useful lessons instead.

## Confirmed Current Baseline

- Hermes CLI: `K:\Hermes_Windows_Native_014\venv\Scripts\python.exe -m hermes_cli.main`
- Version confirmed: Hermes Agent `0.17.0`
- Durable gateway launcher:
${REDACTED_SECRET}
- Startup entry:
${REDACTED_SECRET}
- Open WebUI startup entries are also present under Startup.

## Important Fix Applied

The silent 8642 healthcheck script was stale:

```powershell
${REDACTED_SECRET}
```

Old broken launcher:

```powershell
H:\Hermes_Windows_Native_014\launcher\hermes-014-runtime.ps1
```

New launcher:

```powershell
${REDACTED_SECRET}
```

Backup created before editing:

```powershell
${REDACTED_SECRET}
```

## Verification From This Merge

- `127.0.0.1:8642` listener recovered.
- `/health` returned HTTP 200 with Hermes `0.17.0`.
- `/v1/models` returned HTTP 200 and included `Hermes-GLM-5.2-OpenRouter`.
- Manual healthcheck run returned `state=healthy`.
- Recovery test after stopping the foreground gateway returned
  `state=recovered` and relaunched the gateway from
  `Hermes_Gateway.cmd`.

## Remaining Caution

A local `/v1/chat/completions` test timed out, and the foreground gateway showed
a DeepSeek official request with `provider=deepseek` but an empty model, causing
HTTP 400. Treat this as a separate model-router/config issue before claiming
full model-chat PASS.

For Telegram acceptance, require a fresh real Telegram message and matching
new `inbound message` plus `response ready` lines in
${REDACTED_SECRET}
