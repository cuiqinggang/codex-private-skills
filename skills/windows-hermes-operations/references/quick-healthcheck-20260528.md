# Windows Hermes Quick Healthcheck

Use this reference when the task is to verify Windows native Hermes/Open WebUI
health without starting, stopping, or repairing production services.

Mature evidence says `/health` on 8642 is not enough. A stale WSL relay can make
that endpoint look healthy. A useful health check must separately verify:

- 8642 listener exists.
- 8642 owner command points to `H:\Hermes_Windows_Native_014` when possible.
- `http://127.0.0.1:8642/health` returns HTTP 200.
- `http://127.0.0.1:8642/v1/models` returns `hermes-agent`.
- `http://127.0.0.1:3000` returns HTTP 200 for Open WebUI.

Read-only command:

```powershell
${REDACTED_SECRET}
```

The script writes JSON evidence and prints one of:

- `WINDOWS_HERMES_HEALTHCHECK_PASS`
- `WINDOWS_HERMES_HEALTHCHECK_FAIL`

It does not print secrets, open browsers, start services, stop services, or edit
configuration.
