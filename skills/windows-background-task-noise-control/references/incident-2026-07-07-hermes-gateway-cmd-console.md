# Incident 2026-07-07: Hermes Gateway Cmd Console

## Value Judgment

High value. This prevents a repeated Windows noise failure: a background service
is started through `cmd.exe`, which keeps a console host alive and can show a
black or blue window while the useful service is still healthy.

## Symptoms

- User reported repeated blue/black windows and asked for silent operation.
- Process tree showed `cmd.exe -> python.exe -m hermes_cli.main gateway run --replace`.
- `conhost.exe` stayed attached to the Hermes gateway process chain.
- Task Scheduler entries could not be edited because Windows returned access denied.

## Accepted Fix

1. Keep the Hermes feature running.
2. Stop the long-lived `cmd.exe -> python.exe` gateway chain.
3. Start the gateway through `pythonw.exe` using a small wrapper:
${REDACTED_SECRET}
4. Preserve stdout/stderr logs by redirecting inside the Python wrapper to:
${REDACTED_SECRET}
${REDACTED_SECRET}
5. If scheduled tasks cannot be edited, quiet the target launcher instead of
   deleting or disabling the task.

## Files Changed

${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
- `H:\Hermes_Windows_Native_014\AUTO-START-HERMES-OPENWEBUI.cmd`
- `H:\AI\scripts\codegraph-sync-important-repos.ps1`

## Verification

- Hermes related `cmd.exe` and `conhost.exe` processes disappeared.
- Hermes gateway is owned by `pythonw.exe`, not `cmd.exe`.
- `http://127.0.0.1:8642/health` returned HTTP 200.
- `http://127.0.0.1:8642/v1/models` returned HTTP 200 with
  `Hermes-GLM-5.2-OpenRouter`.
- Knowledge Brain health check returned `FINAL_RESULT=PASS`.

## Next-Run Reuse

When blue/black windows involve Hermes gateway:

1. Search for `Hermes_Gateway_RunHidden.vbs`,
   `run-hermes-gateway-hidden.py`, `pythonw.exe`, and
   `hermes_cli.main gateway run`.
2. If `cmd.exe` is the long-lived parent, switch the launcher to `pythonw.exe`.
3. Preserve logs inside the Python wrapper.
4. Restart only the Hermes gateway chain and verify 8642 health/models.

