# Open Design Codex Connectivity Repair Note

Use this note when Open Design reports Codex failure while direct Codex CLI can
continue after reconnects.

2026-05-27 evidence showed two failure layers:

- The Open Design wrapper treated `Reconnecting...` stream messages as errors.
- A 60 second wrapper timeout was too short for recoverable Codex reconnect and
  HTTP fallback windows.

Acceptance should check both:

1. Direct Codex CLI can complete a minimal run.
2. The wrapper or daemon treats reconnect text as status, not final failure.

Related output archive:

```text
${REDACTED_SECRET}
```

Read-only checker:

```powershell
${REDACTED_SECRET}
```

The checker records process, port, and recent log-shape evidence only. It does
not restart Open Design, does not patch bundles, and does not run paid or
external model calls.
