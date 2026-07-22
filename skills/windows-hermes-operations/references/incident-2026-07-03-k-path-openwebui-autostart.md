# 2026-07-03 C Drive Open WebUI Autostart Repair

Use this when Docker Desktop shows "Lingering processes detected" and Hermes
8642 is healthy, but Open WebUI 3000 does not open after login.

## Observed Failure

- Hermes gateway diagnostic passed: 8642 `/health`, `/v1/models`, and Telegram
  were connected.
- Open WebUI 3000 was unavailable.
- Docker API was unavailable because Docker Desktop had lingering frontend and
  backend processes.
- `Hermes_OpenWebUI_AutoStart` still pointed to the old missing path:
  `H:\Hermes_Windows_Native_014\AUTO-START-HERMES-OPENWEBUI.cmd`.
- A temporary recovery runtime existed at `K:\Hermes_Windows_Native_014`.
- The current active skill package remains on C drive:
${REDACTED_SECRET}
- The final primary startup runtime must be on C drive:
${REDACTED_SECRET}

## Root Causes

1. The K-drive autostart script still had an internal hard-coded H-drive
   install root:
   `K:\Hermes_Windows_Native_014\launcher\auto-start-hermes-openwebui.ps1`.
2. The autostart script accepted only the old model id `hermes-agent`, while
   the current 8642 `/v1/models` returns `Hermes-GLM-5.2-OpenRouter`.
3. Docker Desktop was stuck behind lingering `Docker Desktop` and
   `com.docker.backend` processes, exactly matching the Docker Desktop dialog.

## Fix Applied

Temporary K-drive recovery was proven first. Then the runtime was copied to the
C-drive primary launch root:

```text
${REDACTED_SECRET}
```

K drive remains backup/reference only and should not be the default startup
address.

${REDACTED_SECRET}

- Changed install root from hard-coded H drive to self-location:
  `$InstallRoot = Split-Path -Parent $PSScriptRoot`.
- Added accepted model ids:
  `hermes-agent` and `Hermes-GLM-5.2-OpenRouter`.
- Re-ran the script. It cleared Docker Desktop residue, terminated only the
  `docker-desktop` WSL distro, restarted Docker Desktop, started
  `open-webui-clean`, and opened `http://127.0.0.1:3000`.

Startup-folder fallback restored to C drive:

```text
${REDACTED_SECRET}
${REDACTED_SECRET}
```

Other active C-drive startup wrappers were updated away from K/H paths:

${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}

## Acceptance Evidence

```text
Hermes /health: 200
Models: Hermes-GLM-5.2-OpenRouter
open-webui-clean: Up, healthy, 0.0.0.0:3000->8080/tcp
Open WebUI 3000: HTTP 200
Autostart log: FINAL_PASS Windows native Hermes Open WebUI autostart ready
${REDACTED_SECRET}
```

## Remaining Follow-Up

The scheduled task still points to:

```text
H:\Hermes_Windows_Native_014\AUTO-START-HERMES-OPENWEBUI.cmd
```

It should eventually point to:

```text
${REDACTED_SECRET}
```

An attempted task action change failed with `Access is denied` / run-as password
prompt. Do not unregister or recreate the task without approval. The
Startup-folder VBS is enough as the current functional login fallback, but the
stale task can still report failure at login until changed from an elevated
session.
