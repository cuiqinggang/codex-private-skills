# 2026-05-19 PASS Evidence

Report:

```text
H:\Hermes_Backups\TASK-20260519-HERMES-014-WINDOWS-NATIVE-FIX-CHAT-COMPLETIONS-BAD-RESPONSE\reports\report.md
```

Result:

- `RESULT: PASS`
- `DATA_PATH: C:\Users\A\.hermes`
- `PORT_8642_HEALTH: PASS`
- `MODELS_ENDPOINT: PASS HTTP 200 model_ids=hermes-agent`
- `MODEL_ID_USED: hermes-agent`
- `CHAT_COMPLETIONS: PASS returned HERMES_014_WINDOWS_NATIVE_MAIN_OK`
- `OPENWEBUI_SMOKE: PASS returned HERMES_OPENWEBUI_014_OK`
- `OPENWEBUI_MODIFIED: False`
- `MEMORY_SESSIONS_MIGRATED: False`
- `SECRET_VALUES_PRINTED: False`

Key lesson:

Use `/v1/models` before `/v1/chat/completions`; the verified OpenAI-compatible model id is `hermes-agent`.

Open WebUI smoke evidence:

- URL: `http://127.0.0.1:3000`
- Model shown in UI: `hermes-agent`
- Prompt: `只回复 HERMES_OPENWEBUI_014_OK`
- Assistant response: `HERMES_OPENWEBUI_014_OK`
- Conversation URL observed: `http://127.0.0.1:3000/c/73c4bdc9-814b-42c9-9e55-59df1ee6930a`

Daily startup files:

- Script: `H:\Hermes_Windows_Native_014\launcher\start-hermes-openwebui.ps1`
- Chinese double-click wrapper: `H:\Hermes_Windows_Native_014\明天重启后打开爱马仕页面.cmd`
- ASCII double-click wrapper: `H:\Hermes_Windows_Native_014\START-HERMES-WEBUI.cmd`
- User guide: `H:\Hermes_Windows_Native_014\明天重启后打开爱马仕页面.md`
- Plain text guide: `H:\Hermes_Windows_Native_014\使用说明-明天重启后打开爱马仕页面.txt`

Bundled into this skill package:

- `scripts/start-hermes-openwebui.ps1`
- `scripts/明天重启后打开爱马仕页面.cmd`
- `scripts/START-HERMES-WEBUI.cmd`
- `references/daily-startup-after-reboot.md`
- `references/使用说明-明天重启后打开爱马仕页面.txt`

Startup verification on 2026-05-19:

- Command: `powershell.exe -NoProfile -ExecutionPolicy Bypass -File "H:\Hermes_Windows_Native_014\launcher\start-hermes-openwebui.ps1" -NoOpen`
- Result: `FINAL_PASS Windows native Hermes page is ready`
- Wrapper command: `H:\Hermes_Windows_Native_014\START-HERMES-WEBUI.cmd`
- Wrapper result: `FINAL_PASS Windows native Hermes page is ready`
