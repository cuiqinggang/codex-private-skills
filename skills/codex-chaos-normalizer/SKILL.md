---
name: codex-chaos-normalizer
description: Use when Codex Desktop or a Windows coding workspace feels chaotic, idle CPU/disk stays high, tasks open blank or hang, Git scans thousands of files, plugins/runners pile up, or the user asks to make the system orderly and reduce useless background load without deleting work.
---

# Codex Chaos Normalizer

Use this skill to turn a confused Windows Codex Desktop workspace back into an orderly, low-idle-load state.

## Core policy

- First preserve active work. Do not kill the current Codex session unless the user explicitly asks to restart Codex.
- Prefer diagnosis before changes. Treat high CPU as evidence to attribute, not as proof of weak hardware.
- Reduce repeated useless work: Git untracked-file storms, large Codex log databases, plugin over-enablement, duplicate helpers, stale runner processes, and GPU/renderer spin.
- Make reversible local changes only. Back up config before edits. Do not delete user files.
- Separate current-use work from idle background load. Stop or disable only unused, repeated, or stale components.

## Quick route

Before fresh exploration, read `references\verified-findings.md`. It records the confirmed 2026-06-07 evidence chain, thresholds, and fixes so the same CPU/log/Git/plugin investigation is not repeated from scratch.

If the symptom is "the disk keeps making noise while Codex appears idle" or "CPU/disk stays busy after a task should be finished", also read `references\2026-06-10-veeam-disk-incident.md`. It records the confirmed pattern where stale all-drive search, old local preview servers, Windmill Docker containers, and Veeam Agent automatic system-image backup were the real load sources.

1. Run the bundled script in Diagnose mode:

```powershell
${REDACTED_SECRET}
```

2. If diagnosis shows a Git storm, giant Codex logs, or plugin overload, run Normalize:

```powershell
${REDACTED_SECRET}
```

3. Re-sample CPU and disk after 15-30 seconds. If current Codex processes remain high because the already-running app has stale state loaded, schedule log archive and restart Codex cleanly when the user is ready.

## What Normalize may change

- `.git/info/exclude`: if the repo has zero tracked files and hundreds/thousands of untracked files, append a local ignore rule so Codex/Git stops scanning everything. Backup is written next to the file.
${REDACTED_SECRET}
${REDACTED_SECRET}
- `scripts\compact-codex-logs-after-exit.ps1`: optional offline compaction that waits for Codex to exit, keeps recent logs, and archives the full original database.

## Stop conditions

Stop and ask before:

- deleting files or clearing caches destructively
- changing account, auth, payment, model, security, or system-wide settings
- killing the visible active Codex window or another user-visible active app
- disabling a plugin the user is actively using for the current task

## Interpreting common findings

- `git ls-files` count is 0 and untracked count is large: this is a Git/Codex scan storm. Local exclude is appropriate.
- `logs_*.sqlite` is hundreds of MB: schedule offline archive after Codex exits.
- `logs` has tens of thousands of daily rows and most are `TRACE`/`DEBUG`: treat it as excessive for idle use. Keep 1-3 days for troubleshooting and archive the original database.
- many enabled plugins but only core coding is needed: temporarily disable low-frequency plugins and restart Codex.
- `Codex.exe --type=gpu-process` or Chrome GPU/renderer consumes CPU while idle: suspect Electron/Chromium rendering spin; first restart after config/log cleanup, then consider app-specific GPU workarounds only if still reproducible.
- Docker/WSL is active but not needed: ask or use a separate Docker management skill before stopping, because it may host local services.
- `rg.exe` or another search tool is scanning `C:\` or another whole drive from an old task: confirm the command line and stop that process if it is unrelated to the current user request. This is often a direct cause of unexplained disk noise.
- `python.exe -m http.server` or project-specific scripts are still serving old preview folders: confirm the directory and port, then stop stale preview servers that are not part of the current task.
- Docker containers are running while no Docker task is active: use `docker stats --all --no-stream` and stop only clearly stale project containers. Preserve known baseline containers such as `open-webui-clean` unless the user explicitly asks to stop or remove them.
- Veeam Agent can look like unexplained disk activity: check Windows Event Log `Veeam Agent`, `VeeamEndpointBackupSvc`, and target backup folders before stopping anything. A system-image job may read `C:` and write `H:` heavily. Disable/delete it only after explicit user request, and prefer an administrator PowerShell for service changes.

## Verification

A successful normalization should show:

- `git status --porcelain --untracked-files=all` drops sharply, ideally to 0 for empty Git wrapper workspaces.
- no repeated Codex-owned `git add -A`, `git status`, or `ls-files --others` loop.
- CPU total falls from sustained 100%, or the remaining top processes are explicitly active user apps.
- physical disk activity drops after stale searches/previews are stopped, or the remaining disk writer is explicitly identified as a real task such as Veeam backup.
- Codex opens threads without multi-minute blank UI waits after restart.

## Scheduled maintenance

For ongoing cleanup, install the current-user Windows scheduled task:

```powershell
${REDACTED_SECRET}
```

${REDACTED_SECRET}
