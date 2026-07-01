# Codex Quota Panel Failure Review

## Failure Modes To Avoid

- Hidden PowerShell launcher plus non-taskbar GUI: if the panel fails or appears off-screen, the user has no visible recovery path.
- Dated output-folder runtime: startup shortcuts can survive while the target becomes stale or confusing.
- No log: impossible to tell whether the panel failed, refreshed, moved, or was only hidden.
- Over-wide layout: title bar, large black strip, and empty side padding obstruct other apps.
- Pure numeric layout: shortest, but the user has to mentally translate it each time.
- Chinese literals in PowerShell 5 source: can be misread as GBK and break parsing.
- Moving only once at startup: the label can disappear behind other UI; refresh should also re-pin and re-topmost it.
- Showing transient `Authentication failed` in the visible label: cclimits can fail once and recover on the next poll, so the UI should keep the last good value.
- Keeping last-good forever: the panel can look frozen and mislead the user when cclimits fails continuously.
- Showing `quota refresh...` instead of quota data is not useful to the user. Prefer retrying, then showing stale quota-shaped data without a visible stale marker.
- Hidden launch without verification: can leave a live process but no visible recovery path.
- Regressing from the skill copy: fixing only the runtime launcher is not enough. Also patch `scripts/Start-CodexQuotaPanel.cmd` and `scripts/install_or_repair_quota_panel.ps1`, or the next repair will reintroduce hidden launch.
- Watchdog hidden restart regression: fixing the launcher and installer is still not enough if `QuotaPanelWatchdog.ps1` restarts the panel with `-WindowStyle Hidden`.
- Hung first refresh: `cclimits.py --codex --json` can intermittently hang or take too long after an auth/API failure. If the panel waits synchronously without a subprocess timeout, the user experiences this as "not displaying" even when quota works from a later manual check.
- Startup without watchdog: if the Startup shortcut only starts `CodexQuotaPanel.ps1`, the panel may appear after login but there is no long-lived maintenance process after reboot. Any later exit, timeout, sleep/resume issue, or user close leaves the label gone until manual repair.

## Accepted Pattern

- Store runtime in `C:\Users\A\.codex\quota-panel`.
- Start the panel with `powershell.exe -STA -NoProfile -ExecutionPolicy Bypass`.
- Show a compact borderless topmost label near bottom-right.
- Use rounded corners, a shallow cyan/blue background, a slightly deeper border, and dark teal text for comfortable daily reading.
- Auto-size width to text.
- Keep one-line format equivalent to `95% 18:55 | 7-day 96% 6d18h`.
- Reposition and refresh topmost state on each refresh.
- Cache the last successful quota line in `quota-panel-last-good.txt`; use it for transient failures only.
- Treat cache older than 10 minutes as stale in the log, but keep the visible label quota-shaped without a `旧` prefix if all retries fail.
- Retry cclimits up to 3 times with short delays before fallback.
- Put a hard timeout around each cclimits subprocess call and log timeout/no-output/status failures per attempt.
- On form startup, paint the last-good quota-shaped value before the first live refresh so the panel has a visible recovery path during slow quota checks.
- Refresh every 3 minutes, not every minute, to reduce churn while keeping data useful.
- Run a hidden watchdog only to restart the visible panel if it exits.
- The Startup launcher must start both the visible panel and the hidden watchdog, not just the panel. The installer starting watchdog once is not enough for reboot persistence.
- Never use `-WindowStyle Hidden` or `/min` for the panel process itself.
- Check all three restart paths: launcher, installer, and watchdog.
- Write refresh, fallback, move, and watchdog events to `quota-panel.log`.
- Use startup plus desktop manual shortcut.
