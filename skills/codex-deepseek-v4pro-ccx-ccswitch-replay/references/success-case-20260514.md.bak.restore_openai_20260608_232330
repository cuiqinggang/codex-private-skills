# Success Case 2026-05-14

## Date

2026-05-14.

## Route

DeepSeek official API -> CCX/API Proxy -> `http://localhost:13000/v1` -> CC Switch Codex provider -> Codex API-key provider -> `deepseek-v4-pro`.

## Tool Versions

- CCX/API Proxy: `BenedictKing/ccx` v2.6.92.
- CC Switch: `farion1231/cc-switch` v3.14.1.

## Download Sources

- CCX official GitHub release asset: `https://github.com/BenedictKing/ccx/releases/download/v2.6.92/ccx-windows-amd64.exe`
- CC Switch official GitHub release assets:
  - `https://github.com/farion1231/cc-switch/releases/download/v3.14.1/CC-Switch-v3.14.1-Windows-Portable.zip`
  - `https://github.com/farion1231/cc-switch/releases/download/v3.14.1/CC-Switch-v3.14.1-Windows.msi`

## Local Paths From Success Run

- Success output root: `C:\Users\A\Desktop\1\output\TASK-20260514-CODEX-DEEPSEEK-V4PRO-VIDEO-REPLAY`
- CCX executable: `...\tools\ccx\ccx-windows-amd64.exe`
- CCX config directory: `...\tools\ccx\.config`
- CCX env file: `...\tools\ccx\.env`
- CC Switch extracted executable: `...\tools\cc-switch-msi-extracted\Programs\CC Switch\cc-switch.exe`
- CC Switch provider database: `C:\Users\A\.cc-switch\cc-switch.db`

## Ports

- Open WebUI kept port `3000`.
- CCX used port `13000`.
- API URL: `http://localhost:13000/v1`.

## Provider

- CCX channel: `DeepSeek-V4Pro-Backup-via-CCX`
- CC Switch provider: `DeepSeek-V4Pro-Backup-via-CCX`
- Model: `deepseek-v4-pro`
- Provider is backup-only and was not current/default in CC Switch.

## Verification Evidence

- CCX `/health`: healthy.
- DeepSeek upstream ping: HTTP 200.
- CCX `/v1/responses` returned `DEEPSEEK_V4PRO_CODEX_BACKUP_OK`.
- `codex exec` temporary provider override exited with code `0` and returned `DEEPSEEK_V4PRO_CODEX_BACKUP_OK`.

## Default GPT Route

`C:\Users\A\.codex\config.toml` kept:

```toml
model = "gpt-5.5"
```

Superpowers remained enabled. No DeepSeek provider was written into default `config.toml`.

## Important Failure And Fix

CC Switch portable zip was hash-valid but Windows displayed "This app cannot run on your PC". The successful path used the same official v3.14.1 MSI with administrative extraction:

```powershell
msiexec.exe /a CC-Switch-v3.14.1-Windows.msi /qn TARGETDIR=<extract-dir>
```

Then run:

```powershell
<extract-dir>\Programs\CC Switch\cc-switch.exe
```

## Rollback Paths From Success Run

- Codex config backup: `C:\Users\A\Desktop\1\output\TASK-20260514-CODEX-DEEPSEEK-V4PRO-VIDEO-REPLAY\backups\20260514-172915\config.toml`
- CC Switch backup: `C:\Users\A\Desktop\1\output\TASK-20260514-CODEX-DEEPSEEK-V4PRO-VIDEO-REPLAY\backups\20260514-175310\.cc-switch`

## Lessons

- Do not stop Open WebUI or take port `3000`.
- Do not put the DeepSeek official key into Codex `Enter API key`.
- Codex `Enter API key` uses CCX proxy access key.
- Use CCX because Codex needs Responses-compatible behavior while DeepSeek is mainly OpenAI-compatible upstream.
- Even if DeepSeek `/v1/models` lists more than one model, the backup route must configure and test only `deepseek-v4-pro`.
