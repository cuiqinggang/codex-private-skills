---
name: docker-management
description: Diagnose Docker Desktop, containers, Compose, and quiet Windows login startup. Use for Docker Engine stuck starting, ProgramData environment failures, lingering processes, repeated startup windows, restart-policy surprises, or restoring Docker-dependent Tymeslot, CalDAV, n8n and Open WebUI services.
---

# Docker Management Windows Studio

Version: **1.1.0 (2026-10-24)**. Preserve the existing Windows installation and data.

## Diagnose before changing state

- Check Docker CLI exit code, Engine readiness, exact process lineage and recent host logs.
- Check the launcher's process environment: ProgramData, ALLUSERSPROFILE, COMPUTERNAME, SystemRoot and WINDIR. Read the verified [startup incident](references/startup-20261024.md) before WSL repair.
- A “WSL update required” page alone does not prove that the installed WSL version is obsolete.
- Use Compose commands from the directory containing the Compose file.
- Preserve logs before restarting. Never reset Docker, prune data, unregister WSL, delete VHDX, containers, images, volumes, databases or networks without explicit object-specific authorization.
- Never change FlClash, proxy, networking, credentials, Hermes model settings or service ports for a startup repair.
- Check other active tasks before stopping shared Docker. DSH's current local Node/Playwright/CDP browser route does not require Docker; Tymeslot/CalDAV container tests do.

## One quiet login entry

Use the existing Windows Startup mechanism, not another scheduler or persistent watchdog.

- Installed entry: current user's Startup/Docker-Quiet-Autostart.vbs.
- Target: C:\Users\A\.codex\skills\docker-management\scripts\Start-DockerQuiet.ps1.
- Invoke through the existing PowerShell Reliability Guard, WindowsPowerShell51 target.
- Normalize standard variables only in the launcher's process and children. Preserve global environment and network settings.
- Probe the Engine with a bounded hidden CLI call. If ready, exit without restarting.
- If Docker processes already exist, wait for readiness; do not start duplicates or kill business workloads.
- Only when no Docker process exists, invoke the installed Docker Desktop.exe with its existing -AutoStart argument.
- The VBS uses window style 0, waits and returns the child's exit code. Do not put .bak/.disabled files inside Startup.
- Keep Docker's native AutoStart setting false while using this sole managed entry. This is intentional duplicate prevention; Windows login still starts Docker through VBS.
- Retain legacy Hermes/OpenWebUI browser-opening entries disabled unless the user separately requests opening those pages.

Install or inspect using scripts/Install-DockerQuietStartup.ps1 through the Guard, first Mode Audit then Mode Apply. Backups and startup receipts live in C:\AI\Docker-Autostart-20261024.

## Container recovery policies

Inspect exact names, running state and restart policy separately. Docker startup can restore containers configured always/unless-stopped. Do not automatically enable old rollback or test containers. Preserve the active business stack; log and obtain task-scoped authorization before stopping a service with unknown consumers.

## Verification and claims

Require Engine response, startup entry readback, exact-wrapper execution and unchanged Docker backend PIDs on a healthy rerun. Verify relevant local service endpoints separately. Report native exit codes, unavailable analyzer/tests and remaining readiness failures honestly.

A healthy live-session test proves installed startup configuration and warm rerun behavior. Mark actual next login/reboot and cold-start acceptance PENDING until observed. Never restart the host or interrupt ongoing booking tests just to obtain that evidence.
