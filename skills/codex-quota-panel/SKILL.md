---
name: codex-quota-panel
description: Install, repair, or tune the compact Windows bottom-right Codex quota panel using cclimits. Use when the user asks about Codex usage quota, remaining 5-hour or 7-day capacity, cclimits, AI CLI Usage Monitor, right-bottom quota display, startup auto-run, or a quota panel that is missing, too large, unreadable, hidden, flickering between data and errors, or failed after reboot.
---

# Codex Quota Panel

## Goal

Keep a tiny always-visible Windows panel for Codex quota:

```text
95% 18:55 | 7-day 96% 6d18h
```

The actual GUI uses short Chinese labels for the 7-day window. The leading percentage is the 5-hour window; omit the `5-hour` label because the user already knows it.

## Stable Runtime

${REDACTED_SECRET}
- Startup shortcut: current user's Windows Startup folder, `Codex Quota Panel.lnk`
${REDACTED_SECRET}
- Self-heal scheduled task: `CodexQuotaPanelSelfHeal`, runs every 5 minutes
${REDACTED_SECRET}
${REDACTED_SECRET}

## Install Or Repair

Run:

```powershell
${REDACTED_SECRET}
```

This copies the panel files into the stable runtime folder, recreates startup and desktop shortcuts, closes old panel instances, starts the current visible panel, starts the watchdog, and registers the self-heal scheduled task.

The startup shortcut targets `Start-CodexQuotaPanel.cmd`; that launcher must start both the visible panel and `QuotaPanelWatchdog.ps1`. Do not rely on the installer-only watchdog start, because after reboot there would be no watchdog to self-maintain the panel.

Every repair must also run:

```powershell
${REDACTED_SECRET}
```

Do not claim success unless the hardening check passes.

## Display Rules

- Prefer one compact line.
- Omit the 5-hour label.
- Keep the 7-day label on the weekly portion.
- Use a readable small label, not a large title-bar window.
- Reposition and re-topmost the panel on each refresh, not only at startup.
- Refresh automatically every 3 minutes.
- On transient quota/auth/API failures, keep showing the last successful quota text only while it is fresh.
- Do not let the last-success cache become a fake fixed display; after 10 minutes, keep showing quota-shaped stale data without adding a visible `旧` prefix, and record the stale state in the log.
- Retry cclimits up to 3 times before falling back, because individual calls can fail while the next call succeeds.
- Bound every cclimits subprocess call with a 20-second timeout; collect output through temp files and kill the full query process tree on timeout, because a hung query must never prevent the panel from appearing or staying alive.
- On startup, show the last-good quota-shaped text immediately before doing the live refresh, so a slow first query cannot look like a missing panel.
- Run `QuotaPanelSelfHeal.ps1` every 5 minutes. If the last-good cache is older than 10 minutes but a fresh live quota query succeeds, the self-heal task must refresh the cache and restart the panel.
- The self-heal scheduled task must have a 2-minute execution limit and `IgnoreNew` multiple-instance policy. A stuck task result such as `267009` is a repair trigger.
- Do not start the panel itself with `-WindowStyle Hidden`, `/min`, or a hidden launcher. Only the watchdog may be hidden.
- The obsolete `Start-CodexQuotaPanel-Hidden.vbs` launcher must not exist in the runtime folder, and no shortcut may target it.
- If a repair script starts the panel, verify the repair script also avoids hidden panel launch.
- Use a stable runtime path, not dated output folders.
- Keep PowerShell source ASCII-safe where possible; PowerShell 5 can misread Chinese source encoding.

## Validation

Check quota data:

```powershell
${REDACTED_SECRET}
```

Check panel behavior:

```powershell
${REDACTED_SECRET}
```

PASS requires:

- `cclimits.py --codex --json` returns `status: ok`, or the panel keeps showing quota-shaped stale data during a transient failure.
- Hardening check returns `PASS: quota panel hardened`.
- The log shows `refreshed:` with the compact format.
- The script uses a 180000 ms timer and a 10-minute last-good cache limit.
- The script uses robust cclimits temp-output capture and `taskkill.exe /T /F` for timed-out query trees.
- The log shows `moved bottom-right`.
- The log shows `watchdog: started` after repair.
- Windows Task Scheduler has `CodexQuotaPanelSelfHeal` in Ready state, and the runtime contains `QuotaPanelSelfHeal.ps1`.
- `CodexQuotaPanelSelfHeal` has `ExecutionTimeLimit` set to `PT2M`, `MultipleInstances` set to `IgnoreNew`, and its last result is not stuck running.
- Runtime folder does not contain `Start-CodexQuotaPanel-Hidden.vbs`, and Startup shortcut targets `Start-CodexQuotaPanel.cmd`.
- The log shows `startup fallback visible` after repair, then either `refreshed:` with live quota or a bounded stale fallback.
${REDACTED_SECRET}
- `Start-CodexQuotaPanel.cmd` contains both `CodexQuotaPanel.ps1` and `QuotaPanelWatchdog.ps1`, so reboot/login starts the self-maintenance loop too.

## Failure Review

Read `references/failure-review.md` before changing launcher visibility, startup behavior, encoding, caching, or display layout.
