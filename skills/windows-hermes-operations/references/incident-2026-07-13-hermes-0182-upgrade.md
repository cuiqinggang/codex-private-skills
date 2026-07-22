# 2026-07-13 Windows Native Hermes 0.18.2 Upgrade

## Trigger

Use this when the C-drive Windows native Hermes runtime should move from 0.17.x
to the latest 0.18.x release while preserving Telegram, Open WebUI, login
autostart, and the browser light-chat route.

Trigger keywords: `Hermes 0.18`, `爱马仕升级最新版`, `0.18.2`, `登录自启`,
`Open WebUI 自动打开`, `升级后浏览器测试`.

## Material Value Judgment

High value. The upgrade is repeatable, the package overwrites a local API
server patch, and 0.18 changes the hidden gateway process shape. Recording the
minimal compatibility rule prevents future healthy gateways from being killed
or rejected by the older launcher.

## Accepted Route

1. Confirm PyPI latest and installed version.
2. Back up `config.yaml`, `.env`, `state.db`, launchers, gateway-service files,
   Startup wrappers, and `gateway/platforms/api_server.py` without printing
   secrets.
3. Stop only the 8642 listener and upgrade the existing C-drive venv:
   `python -m pip install --upgrade hermes-agent==0.18.2`.
4. Require `pip check` and `hermes --version` PASS.
5. If `hermes config check` reports an old schema, run `hermes config migrate`
   and check again.
6. Reapply only the minimal streaming light-chat behavior to the new 0.18.2
   `api_server.py`; never restore the whole 0.17 file.
7. Update `Test-WindowsHermesOwner` so the exact hidden gateway script
${REDACTED_SECRET}
   Windows Hermes owner. Keep the legacy `gateway run` rule too.
8. Run the strict Telegram diagnostic, a real streaming marker test, and the
   login autostart script. Verify the already logged-in Chrome UI, not a
   temporary browser.

## 0.18.2 Compatibility Detail

The healthy listener can appear as `pythonw.exe` with command line:

```text
${REDACTED_SECRET}
```

The older launcher required the process lineage to contain `gateway run`, so it
misclassified this healthy 0.18.2 listener as unknown. Accept the exact hidden
gateway script path; do not broadly trust every `pythonw.exe` process.

## Acceptance Evidence

- Version: `Hermes Agent v0.18.2 (2026.7.7.2)`.
- `pip check`: no broken requirements.
- Config schema: 33 after migration.
- Streaming marker: reconstructed SSE content equals
  `HERMES_0182_STREAM_PASS`, HTTP 200, `[DONE]` present.
- Strict diagnostic: PASS for API server, Telegram, proxy, Open WebUI, task
  script, and Startup entry.
- Autostart log:
${REDACTED_SECRET}
  contains `FINAL_PASS Windows native Hermes Open WebUI autostart ready`.
- Screenshot:
${REDACTED_SECRET}
  the logged-in Open WebUI chat and model `Hermes-GLM-5.2-OpenRouter`.
- Rollback backup:
${REDACTED_SECRET}

## Failure Review Entry

If 8642 is healthy but the launcher reports an unknown owner, inspect only the
listener command line and `Test-WindowsHermesOwner`; do not reinstall Hermes.
If streaming returns HTTP 200 but a raw marker search fails, reconstruct the
`delta.content` chunks before declaring failure. Escalate only if the
reconstructed content is empty/error or `[DONE]` is absent.

## Next-Run Reuse

Start from this reference, then check PyPI for the exact newest patch version.
Treat local patch overwrite and process-owner recognition as explicit gates.

