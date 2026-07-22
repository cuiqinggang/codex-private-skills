# Knowledge Log

## 2026-06-28 Cache Freeze Fix

Problem: The panel kept showing the last good quota value for hours while cclimits returned repeated Authentication failed errors. This made the display look fixed even though the quota had changed.

Fix:
- Automatic refresh interval changed from 1 minute to 5 minutes.
- Last-good fallback now expires after 10 minutes.
- After cache expiry, show a short refresh warning instead of pretending the stale value is current.
- Runtime and skill script both use `$timer.Interval = 300000` and `$LastGoodMaxAgeMinutes = 10`.

Acceptance evidence:
- Runtime refreshed to `78% 18:26 | 7天88% 5天21时` after repair.
- `quota-panel-last-good.txt` contains the same new value.
- Skill validation passed.

## 2026-06-29 Hidden Launcher Regression

Problem: The runtime panel was fixed, but the skill's launcher and installer still contained hidden panel launch commands. Running repair copied the old launcher back and started the panel with `-WindowStyle Hidden`, so the process existed while the visible quota label disappeared or became unreliable.

Fix:
- Remove `-WindowStyle Hidden` and `/min` from both runtime and skill `Start-CodexQuotaPanel.cmd`.
- Remove `-WindowStyle Hidden` from the installer when starting `CodexQuotaPanel.ps1`.
- Keep hidden mode only for `QuotaPanelWatchdog.ps1`.

Acceptance:
- Runtime log refreshed to current quota data after repair.
- Future repairs copy the corrected launcher from the skill package.

## 2026-06-29 Watchdog Hidden Restart Regression

Problem: The launcher and installer were fixed, but `QuotaPanelWatchdog.ps1` still restarted `CodexQuotaPanel.ps1` with `-WindowStyle Hidden`. If the visible panel exited, the watchdog could bring back a hidden panel.

Fix:
- Remove `-WindowStyle Hidden` from the watchdog's panel restart command.
- Keep hidden launch only for the watchdog process itself.
- On this family of bugs, inspect all restart paths: startup cmd, installer, watchdog.

## 2026-06-29 Stale Data Display Policy

Problem: After the 10-minute cache expiry, the panel showed `quota refresh...`, which was technically honest but not useful because the user wants quota-shaped data at a glance.

Fix:
- Retry cclimits up to 3 times before fallback.
- If retries still fail and cached data is stale, display the quota-shaped cached value instead of non-quota text.
- Keep writing the failure reason to the log.

## 2026-07-01 Visible Stale Prefix Removal

Problem: The visible label used a leading `旧` marker for stale cached quota data. The user found the marker meaningless in the tiny bottom-right label, and it returned because the rule existed in both the runtime script and the skill package.

Fix:
- Remove the visible stale prefix from runtime and skill `CodexQuotaPanel.ps1`.
- Keep stale/cache status in `quota-panel.log` for diagnosis.
- Extend the hardening checker so future repairs fail if the panel script can reintroduce the visible old marker.

## 2026-06-29 Hardening Gate

Problem: The same family of bugs kept returning because old copies existed in multiple places: runtime folder, skill scripts, launcher, installer, and watchdog.

Fix:
- Add `scripts/assert_quota_panel_hardened.ps1`.
- The installer copies itself and the hardening checker into the runtime folder.
- The installer runs the hardening checker after deployment.
- The checker fails on hidden/minimized panel launch, missing 5-minute timer, missing 10-minute cache age, missing 3-attempt retry, non-quota visible refresh text, or startup shortcut mismatch.

Rule: No future quota-panel repair should be considered complete until the hardening gate says `PASS: quota panel hardened`.

## 2026-06-30 Hung First Refresh / Missing Display Fix

Problem: The standalone quota query could return `status: ok`, but the panel had previously logged repeated `Authentication failed` attempts and then stopped showing a current visible quota label. The likely failure mode was an unbounded or very slow cclimits subprocess during the first refresh; because startup refreshed synchronously, the user experienced this as the bottom-right display not appearing.

Fix:
- Add `$CclimitsTimeoutSeconds = 20`.
- Replace direct `& python cclimits.py --codex --json` calls with `Invoke-CclimitsJson`, which uses `WaitForExit` and kills a hung subprocess after the timeout.
- Keep the 3-attempt retry policy, but log each failed/no-output/timeout/status failure with its attempt number.
- Add `Show-StartupFallback` so the panel paints the last-good quota-shaped value before the first live refresh.
- Extend `assert_quota_panel_hardened.ps1` so future repairs fail if bounded timeout or visible startup fallback disappears from either runtime or skill copy.

Acceptance evidence:
${REDACTED_SECRET}
${REDACTED_SECRET}
- Process list showed both `CodexQuotaPanel.ps1` and `QuotaPanelWatchdog.ps1` running.
- Log showed `startup fallback visible: 55% 06:16 | 7天88% 6天10时`, then `refreshed: 94% 20:27 | 7天99% 6天23时`, then `moved bottom-right`.

## 2026-07-01 Startup Watchdog Persistence Fix

Problem: The Startup shortcut existed and correctly targeted `Start-CodexQuotaPanel.cmd`, but that launcher only started `CodexQuotaPanel.ps1`. The watchdog was started by the installer during repair, not by the login startup path. After reboot/login, the panel had no self-maintenance process; if it exited or got stuck after quota timeouts, it would not be restarted.

Fix:
- Update both runtime and skill `Start-CodexQuotaPanel.cmd` to start the visible panel and the hidden `QuotaPanelWatchdog.ps1`.
- Extend `assert_quota_panel_hardened.ps1` so future hardening fails unless the startup launcher contains both `CodexQuotaPanel.ps1` and `QuotaPanelWatchdog.ps1`.
- Keep the panel launch visible; only the watchdog launch may use `-WindowStyle Hidden`.

Acceptance evidence:
${REDACTED_SECRET}
- Manual `cclimits.py --codex --json` returned `status: ok`, with 5-hour remaining `94%` and 7-day remaining `94%`.
- Hardening check must pass after reinstall and process verification.

## 2026-07-02 Visible Blue PowerShell Host Console Fix

Problem: The quota panel was useful and still running, but its PowerShell host console appeared as a long-lived blank blue `Windows PowerShell` window. The visible console and the `Codex Quota` GUI belonged to the same `CodexQuotaPanel.ps1` process, so deleting the process or globally hiding the panel launcher would risk losing the useful bottom-right quota display.

Fix:
- Keep the panel launch path visible according to the existing regression rule; do not add `-WindowStyle Hidden` to `CodexQuotaPanel.ps1`.
- Add a `Hide-HostConsole` guard inside `CodexQuotaPanel.ps1` using `GetConsoleWindow` + `ShowWindow(..., 0)` so only the PowerShell console is hidden after the process starts.
- Extend `assert_quota_panel_hardened.ps1` so future repairs fail if the host-console hide guard disappears from either runtime or skill copy.
- Route future blank blue quota windows through `windows-background-task-noise-control` first, then this quota-panel knowledge log.

Acceptance:
- The `Windows PowerShell` host window should disappear after restart.
- The `Codex Quota` GUI should remain visible, topmost, and refreshed from cache or live quota.
- Hardening check must return `PASS: quota panel hardened`.

## 2026-07-03 Frozen Visible Quota / Self-Heal Scheduled Task

Problem: The bottom-right quota label stayed visible but appeared frozen for more than 20 minutes. Logs proved the 3-minute timer was still firing, but every internal `cclimits.py --codex --json` attempt timed out and the panel kept repainting an expired last-good value: `86% 18:40 | 7天67% 5天0时`. A manual quota query outside the panel returned live data within seconds, so the failure was in the panel's query execution path and lack of stale-data self-healing.

Fix:
- Change `Invoke-CclimitsJson` in both runtime and skill `CodexQuotaPanel.ps1` to collect stdout/stderr through temp files instead of redirected pipes.
- On timeout, call `taskkill.exe /PID <pid> /T /F` so the full query process tree is killed, not just the immediate wrapper process.
- Add `scripts/QuotaPanelSelfHeal.ps1`.
- Update the installer to deploy `QuotaPanelSelfHeal.ps1` and register the Windows scheduled task `CodexQuotaPanelSelfHeal`, repeating every 5 minutes.
- Self-heal logic: kill stale quota query trees older than 2 minutes; if the panel is missing or `quota-panel-last-good.txt` is older than 10 minutes, run a live quota query; if live quota succeeds, refresh the cache and restart the panel; if live quota fails, log `selfheal:` and avoid a restart loop.
- Extend `assert_quota_panel_hardened.ps1` so future repairs fail if robust timeout tree-kill/temp-output capture, the self-heal script, or the installer task registration disappears.

Acceptance evidence:
${REDACTED_SECRET}
- Log showed restart followed by live refresh: `refreshed: 71% 21:57 | 7天48% 3天20时`.
- Manual quota query returned `status: ok`, 5-hour remaining around `70%`, and 7-day remaining `48%`.
- `Get-ScheduledTask -TaskName CodexQuotaPanelSelfHeal` returned `Ready`.

Next-run rule:
- When the user says the quota label is still visible but has not changed for 10+ minutes, do not stop at restarting the panel. First inspect `quota-panel.log`, `quota-panel-last-good.txt` age, live `cclimits.py --codex --json`, stale cclimits child processes, and `CodexQuotaPanelSelfHeal` scheduled task state. Then run the installer and hardening check.

## 2026-07-03 Automation Health Check Repair

Finding: Scheduled automation `codex-quota-panel-health-check` found the runtime present, visible panel/watchdog processes running, `CodexQuotaPanelSelfHeal` registered, and hardening already passing. However `quota-panel-last-good.txt` was about 25 minutes old while a manual `cclimits.py --codex --json` returned `status: ok`, matching the stale-cache repair condition.

Action:
- Ran `scripts/install_or_repair_quota_panel.ps1`; installer returned `PASS: quota panel hardened`.
- Rechecked live quota: `status: ok`, 5-hour remaining `57%`, 7-day remaining `46%`.
- Rechecked cache: refreshed to `57% 21:57 | 7天46% 3天18时`, age under 1 minute.
- Rechecked scheduled task: `CodexQuotaPanelSelfHeal` present and running during validation.
- Rechecked log: restart showed `watchdog: started`, `startup fallback visible`, `refreshed: 57% 21:57 | 7天46% 3天18时`, and `moved bottom-right`.

Rule: For this automation, stale cache older than 10 minutes plus live quota success is enough to run repair even when the panel is still visible and hardening initially passes.

## 2026-07-03 Automation Health Check Healthy

Finding: Scheduled automation `codex-quota-panel-health-check` found the runtime healthy. `quota-panel-last-good.txt` was fresh at about 2.15 minutes old with `98% 03:00 | 7天43% 3天17时`; live `cclimits.py --codex --json` returned `status: ok`, 5-hour remaining `97%`, 7-day remaining `43%`; `assert_quota_panel_hardened.ps1` returned `PASS: quota panel hardened`.

Validation:
- `CodexQuotaPanel.ps1` and `QuotaPanelWatchdog.ps1` processes were running.
- `CodexQuotaPanelSelfHeal` existed, state `Ready`, last result `0`, next run scheduled normally.
${REDACTED_SECRET}
- Runtime scripts still contained the 180000 ms timer, 10-minute cache threshold, robust temp-file cclimits capture, and `taskkill.exe /T /F` timeout guard.
- Recent log showed regular `refreshed:` entries and `selfheal: healthy` entries.

Action: No installer repair was needed because no stale-cache, missing-panel, missing-task, live-quota, or hardening failure condition was present.

## 2026-07-03 Automation Health Check Healthy - 23:34 CST

Finding: Scheduled automation `codex-quota-panel-health-check` found the runtime healthy. `quota-panel-last-good.txt` was fresh at about 2.74 minutes old with `91% 03:00 | 7天42% 3天16时`; live `cclimits.py --codex --json` returned `status: ok`, 5-hour remaining `91%`, 7-day remaining `42%`; `assert_quota_panel_hardened.ps1` returned `PASS: quota panel hardened`.

Validation:
- `CodexQuotaPanel.ps1` and `QuotaPanelWatchdog.ps1` processes were running.
- `CodexQuotaPanelSelfHeal` existed, state `Ready`, last result `0`, next run scheduled normally.
${REDACTED_SECRET}
- `Start-CodexQuotaPanel.cmd` starts both the visible panel and hidden watchdog.
- Runtime scripts still contained the 180000 ms timer, 10-minute cache threshold, robust temp-file cclimits capture, and `taskkill.exe /T /F` timeout guard.
- Recent log showed regular `refreshed:` entries plus `selfheal: healthy`; earlier repair evidence still includes `watchdog: started`, `startup fallback visible`, and `moved bottom-right`.

Action: No installer repair was needed because no stale-cache, missing-panel, missing-task, live-quota, or hardening failure condition was present.

## 2026-07-04 Automation Health Check Repair - 00:32 CST

Finding: Scheduled automation `codex-quota-panel-health-check` found the panel and watchdog processes running, `CodexQuotaPanelSelfHeal` present and `Ready`, and the hardening gate already passing. However `quota-panel-last-good.txt` was about 15.78 minutes old with `76% 03:00 | 7天40% 3天15时`, while manual `cclimits.py --codex --json` returned `status: ok`, 5-hour remaining `75%`, and 7-day remaining `40%`.

Action:
- Ran `scripts/install_or_repair_quota_panel.ps1`; installer returned `PASS: quota panel hardened`.
- Rechecked runtime hardening; `assert_quota_panel_hardened.ps1` returned `PASS: quota panel hardened`.
- Rechecked cache; it refreshed to `75% 03:00 | 7天40% 3天14时`, age under 1 minute.
- Rechecked processes; `CodexQuotaPanel.ps1` and `QuotaPanelWatchdog.ps1` were running after repair.
- Rechecked scheduled task; `CodexQuotaPanelSelfHeal` remained `Ready` with last result `0`.
- Recent log showed `watchdog: started`, `starting quota panel`, `startup fallback visible`, and `refreshed: 75% 03:00 | 7天40% 3天14时`.

Rule confirmed: stale last-good cache older than 10 minutes plus live quota success triggers installer repair even when the visible panel process exists and hardening initially passes.

## 2026-07-04 Self-Heal Running-State / Non-Reentry Fix - 21:00 CST

Problem: The quota label again appeared frozen. The last-good cache was about 1098 minutes old with `61% 03:00 | 7天37% 3天13时`. The panel and watchdog were running, but the panel repeatedly timed out and kept repainting the expired cache. Manual `cclimits.py --codex --json` returned `status: ok`, 5-hour remaining around `92%`, and 7-day remaining `25%`, proving the account was not actually logged out.

Root cause:
- `CodexQuotaPanelSelfHeal` had `LastTaskResult = 267009`, meaning a prior self-heal instance was still running.
- The scheduled task had no short execution limit or non-reentry policy, so the 5-minute self-heal mechanism could itself become stuck.
- The query wrapper still used a `cmd /c` redirection layer; replacing it with direct `Start-Process` plus stdout/stderr files removed one more fragile layer.

Fix:
- Updated runtime and skill `CodexQuotaPanel.ps1` to start Python directly with `Start-Process -FilePath $Python -ArgumentList @($Checker, "--codex", "--json") -RedirectStandardOutput ... -RedirectStandardError ...`.
- Updated runtime and skill `QuotaPanelSelfHeal.ps1` the same way.
- Updated installer to stop an existing `CodexQuotaPanelSelfHeal` task before re-registering it.
- Registered `CodexQuotaPanelSelfHeal` with `ExecutionTimeLimit = PT2M`, `MultipleInstances = IgnoreNew`, `-NonInteractive`, and runtime working directory.
- Extended the hardening gate so these task settings are required.
- Updated hourly automation `codex-quota-panel-health-check` to treat `LastTaskResult 267009`, missing `PT2M`, or missing `IgnoreNew` as repair triggers.

Acceptance evidence:
- Installer returned `PASS: quota panel hardened`.
- Hardening check returned `PASS: quota panel hardened`.
- Scheduled task showed `LastTaskResult: 0`, `ExecutionTimeLimit: PT2M`, `MultipleInstances: IgnoreNew`, and next run scheduled.
- Log showed live panel recovery: `refreshed: 88% 01:18 | 7天24% 2天18时`.
- After one refresh cycle, log showed `refreshed: 87% 01:18 | 7天24% 2天18时`; last-good cache age was about 1 minute.

Next-run rule:
- When the label is visible but stale, check not only cache age and live quota. Also check `Get-ScheduledTaskInfo -TaskName CodexQuotaPanelSelfHeal`; if `LastTaskResult` is `267009` or the task is currently running for too long, run the installer and hardening check.

## 2026-07-04 Automation Health Check - 22:08 CST

Finding: Scheduled automation `codex-quota-panel-health-check` found the quota panel runtime healthy, with no repair trigger.

Evidence:
- `quota-panel-last-good.txt` was fresh at about 2.5 minutes old during initial inspection and refreshed to `80% 01:18 | 7天23% 2天17时` by 22:06 CST.
${REDACTED_SECRET}
- `assert_quota_panel_hardened.ps1` returned `PASS: quota panel hardened`.
- `CodexQuotaPanel.ps1` and `QuotaPanelWatchdog.ps1` were running.
- `CodexQuotaPanelSelfHeal` was present, `Ready`, `LastTaskResult = 0`, `ExecutionTimeLimit = PT2M`, and `MultipleInstances = IgnoreNew`.
- Recent log showed regular `refreshed:` entries and `selfheal: healthy`; no stale-cache, stuck self-heal, or missing-task condition was present.
- Process inspection found no stale independent `cclimits.py --codex --json` or `QuotaPanelSelfHeal.ps1` child processes.

Action: No installer repair was needed because all runtime, live quota, self-heal task, process, and hardening gates passed.

## 2026-07-06 Obsolete Hidden Launcher / Startup Shortcut Repair - 01:01 CST

Problem: The quota label was visible but frozen again. `quota-panel-last-good.txt` was about 1219 minutes old with `91% 07:59 | 7天99% 6天22时`. Runtime logs showed repeated cclimits timeouts and `Authentication failed`, while manual live quota queries returned `status: ok`, 5-hour remaining `94%`, and 7-day remaining `86%`.

Root cause:
${REDACTED_SECRET}
- The obsolete hidden VBS launcher still existed in the runtime folder and could become the Startup target, bypassing the standard `Start-CodexQuotaPanel.cmd` launcher and the expected repair path.
- The Codex hourly health-check automation had been removed, so it was recreated as `codex-quota-panel-health-check-2`.

Fix:
- Ran `scripts/install_or_repair_quota_panel.ps1`; installer returned `PASS: quota panel hardened`.
- Added installer cleanup for `Start-CodexQuotaPanel-Hidden.vbs`.
- Deleted the runtime `Start-CodexQuotaPanel-Hidden.vbs`.
- Extended hardening so future repairs fail if the obsolete hidden launcher exists or if the installer does not remove it.
- Recreated Codex hourly health check automation and added triggers for startup shortcut mismatch and obsolete hidden launcher presence.

Acceptance evidence:
${REDACTED_SECRET}
- Runtime no longer contains `Start-CodexQuotaPanel-Hidden.vbs`.
- Hardening returned `PASS: quota panel hardened`.
- Log showed recovery: `refreshed: 93% 04:42 | 7天86% 6天2时`, then `refreshed: 92% 04:42 | 7天86% 6天2时`, then `refreshed: 92% 04:42 | 7天86% 6天1时`.
- Cache age after validation was about 1.43 minutes.

Next-run rule:
- For any visible-but-stale quota label, always check the Startup shortcut target and runtime hidden launcher presence in addition to live quota, cache age, self-heal task state, and hardening.

## 2026-07-06 Automation Health Check Healthy - 02:09 CST

Finding: Scheduled automation `codex-quota-panel-health-check-2` found the quota panel runtime healthy, with no repair trigger.

Evidence:
- `quota-panel-last-good.txt` was fresh at about 2.73 minutes old during inspection with `84% 04:42 | 7天85% 6天0时`; the panel then refreshed again to `83% 04:42 | 7天85% 6天0时`.
${REDACTED_SECRET}
- `assert_quota_panel_hardened.ps1` returned `PASS: quota panel hardened`.
- `CodexQuotaPanel.ps1` and `QuotaPanelWatchdog.ps1` were running.
- `CodexQuotaPanelSelfHeal` was present, `Ready`, `LastTaskResult = 0`, `ExecutionTimeLimit = PT2M`, and `MultipleInstances = IgnoreNew`.
${REDACTED_SECRET}
- Runtime did not contain `Start-CodexQuotaPanel-Hidden.vbs`.
- Runtime scripts still contained the 180000 ms timer, 10-minute cache threshold, direct Start-Process cclimits capture through temp stdout/stderr files, and `taskkill.exe /T /F` timeout guard.
- Process inspection found no stale independent `cclimits.py --codex --json` or stuck `QuotaPanelSelfHeal.ps1` child processes.

Action: No installer repair was needed because live quota, cache freshness, startup target, hidden-launcher removal, self-heal task settings, process state, and hardening gates all passed.

## 2026-07-06 03:07:33 +08:00 - Automation codex-quota-panel-health-check-2
${REDACTED_SECRET}
- Visible panel: PASS, CodexQuotaPanel.ps1 PID 5440 has visible Codex Quota window.
- Last-good cache: PASS, fresh during check (76% 04:42 | 7天84% 5天23时, age under 10 minutes).
- Live quota: PASS, cclimits.py --codex --json returned status ok, 5h remaining 76%, 7d remaining 84%.
${REDACTED_SECRET}
- Scheduled task: PASS, CodexQuotaPanelSelfHeal Ready/enabled, LastTaskResult 0, ExecutionTimeLimit PT2M, MultipleInstances IgnoreNew.
- Runtime hardening: PASS, assert_quota_panel_hardened.ps1 returned PASS: quota panel hardened.
- Obsolete hidden launcher: PASS, Start-CodexQuotaPanel-Hidden.vbs absent.
- Stale cclimits/selfheal children: PASS, none found after check.
- Repair action: not triggered; installer not run; no duplicate automation created.

## 2026-07-06 12:52:16 +08:00 - Automation codex-quota-panel-health-check-2
${REDACTED_SECRET}
- Trigger found: `quota-panel-last-good.txt` was stale by more than 10 minutes while manual `cclimits.py --codex --json` returned `status: ok`.
- Pre-repair evidence: log showed repeated internal cclimits timeouts and expired last-good fallback from 12:29 through 12:41, while manual live quota succeeded with 5h remaining 98% and 7d remaining 82%.
${REDACTED_SECRET}
${REDACTED_SECRET}
- Refresh proof: log showed `startup fallback visible`, then live `refreshed: 98% 17:41 | 7天82% 5天14时`, then `refreshed: 96% 17:41 | 7天82% 5天14时`, then `refreshed: 93% 17:41 | 7天82% 5天14时`.
- Last-good cache: refreshed at 2026-07-06 12:50:31, about 1.56 minutes old during final validation.
- Scheduled task: `CodexQuotaPanelSelfHeal` ended `Ready`, `LastTaskResult = 0`, `ExecutionTimeLimit = PT2M`, and `MultipleInstances = IgnoreNew`.
${REDACTED_SECRET}
- Obsolete hidden launcher: PASS, `Start-CodexQuotaPanel-Hidden.vbs` absent.
- Stale children: PASS, no lingering `QuotaPanelSelfHeal.ps1` or `cclimits.py` child processes after the 12:50 self-heal run completed.
- No duplicate automations were created.

## 2026-07-06 13:45:22 +08:00 - Automation codex-quota-panel-health-check-2
${REDACTED_SECRET}
- Visible panel: PASS, `CodexQuotaPanel.ps1` PID 7136 has visible window title `Codex Quota`.
- Last-good cache: PASS, refreshed during check to `83% 17:41 | 7天80% 5天13时`; final age was under 1 minute.
- Live quota: PASS, `cclimits.py --codex --json` returned `status: ok`, 5-hour remaining `83%`, and 7-day remaining `80%`.
${REDACTED_SECRET}
- Scheduled task: PASS, `CodexQuotaPanelSelfHeal` is `Ready`/enabled, `LastTaskResult = 0`, `ExecutionTimeLimit = PT2M`, and `MultipleInstances = IgnoreNew`.
- Runtime hardening: PASS, `assert_quota_panel_hardened.ps1` returned `PASS: quota panel hardened`.
- Obsolete hidden launcher: PASS, `Start-CodexQuotaPanel-Hidden.vbs` absent and no Startup shortcut targets it.
- Stale children: PASS, no independent stale `cclimits.py --codex --json` or stuck `QuotaPanelSelfHeal.ps1` process remained after inspection.
- Repair action: not triggered; installer not run; no duplicate automation created.

## 2026-07-06 15:44:25 +08:00 - Automation codex-quota-panel-health-check-2
${REDACTED_SECRET}
- Last-good cache: PASS, `quota-panel-last-good.txt` was fresh at about 2.96 minutes old with `67% 17:41 | 7天78% 5天11时`.
- Live quota: PASS, `cclimits.py --codex --json` returned `status: ok`, 5-hour remaining `66%`, and 7-day remaining `77%`.
${REDACTED_SECRET}
- Scheduled task: PASS, `CodexQuotaPanelSelfHeal` is `Ready`, `LastTaskResult = 0`, `ExecutionTimeLimit = PT2M`, and `MultipleInstances = IgnoreNew`.
- Runtime hardening: PASS, `assert_quota_panel_hardened.ps1` returned `PASS: quota panel hardened`.
- Obsolete hidden launcher: PASS, `Start-CodexQuotaPanel-Hidden.vbs` absent and no Startup shortcut targets it.
- Runtime launcher: PASS, `Start-CodexQuotaPanel.cmd` starts both `CodexQuotaPanel.ps1` and `QuotaPanelWatchdog.ps1`, with no hidden launch for the visible panel.
- Stale children: PASS, no independent stale `cclimits.py --codex --json` or stuck `QuotaPanelSelfHeal.ps1` process remained after inspection.
- Repair action: not triggered; installer not run; no duplicate automation created.

## 2026-07-06 14:49:00 +08:00 - Automation codex-quota-panel-health-check-2
${REDACTED_SECRET}
- Visible panel: PASS, `CodexQuotaPanel.ps1` PID 7136 has visible window title `Codex Quota`.
- Last-good cache: PASS, refreshed during check to `74% 17:41 | 7天79% 5天12时`; final age was under 1 minute.
- Live quota: PASS, `cclimits.py --codex --json` returned `status: ok`, 5-hour remaining `74%`, and 7-day remaining `79%`.
${REDACTED_SECRET}
- Scheduled task: PASS, `CodexQuotaPanelSelfHeal` is `Ready`/enabled, `LastTaskResult = 0`, `ExecutionTimeLimit = PT2M`, and `MultipleInstances = IgnoreNew`.
- Runtime hardening: PASS, `assert_quota_panel_hardened.ps1` returned `PASS: quota panel hardened`.
- Obsolete hidden launcher: PASS, `Start-CodexQuotaPanel-Hidden.vbs` absent and no Startup shortcut targets it.
- Stale children: PASS, no independent stale `cclimits.py --codex --json` or stuck `QuotaPanelSelfHeal.ps1` process remained after inspection.
- Repair action: not triggered; installer not run; no duplicate automation created.

## 2026-07-06 16:49:45 +08:00 - Automation codex-quota-panel-health-check-2
${REDACTED_SECRET}
- Visible panel: PASS, `CodexQuotaPanel.ps1` PID 7136 has visible window title `Codex Quota`.
- Last-good cache: PASS, refreshed during check to `57% 17:41 | 7天76% 5天10时`; final age was about 1.69 minutes.
- Live quota: PASS, `cclimits.py --codex --json` returned `status: ok`, 5-hour remaining `57%`, and 7-day remaining `76%`.
${REDACTED_SECRET}
- Scheduled task: PASS, `CodexQuotaPanelSelfHeal` is `Ready`/enabled, `LastTaskResult = 0`, `ExecutionTimeLimit = PT2M`, and `MultipleInstances = IgnoreNew`.
- Runtime hardening: PASS, `assert_quota_panel_hardened.ps1` returned `PASS: quota panel hardened`.
- Obsolete hidden launcher: PASS, `Start-CodexQuotaPanel-Hidden.vbs` absent and no Startup shortcut targets it.
- Runtime launcher: PASS, `Start-CodexQuotaPanel.cmd` starts both `CodexQuotaPanel.ps1` and `QuotaPanelWatchdog.ps1`, with no hidden launch for the visible panel.
- Stale children: PASS, no independent stale `cclimits.py --codex --json` or stuck `QuotaPanelSelfHeal.ps1` process remained after inspection.
- Repair action: not triggered; installer not run; no duplicate automation created.
