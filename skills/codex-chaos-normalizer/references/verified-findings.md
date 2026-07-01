# Verified Findings

This file records reusable findings from the 2026-06-07 Codex Desktop cleanup run. Use it to avoid repeating the same exploration when idle CPU, disk noise, blank threads, or slow task opening returns.

## Known-good evidence chain

1. Check total CPU, free memory, disk queue, and top process deltas before changing anything.
2. If memory is still abundant but CPU is saturated, treat the problem as process churn, renderer/GPU spin, logging, or repeated scanning, not weak hardware.
3. Attribute Codex load by command line:
   - `Codex.exe --type=gpu-process` indicates Electron/Chromium GPU work.
   - `Codex.exe --type=renderer` indicates one or more UI renderer processes.
   - `codex.exe app-server --analytics-default-enabled` indicates the Codex app server.
4. Do not call unfamiliar high-CPU processes malicious only because CPU is high. First verify executable path and command line.
5. Do not replace or move `logs_2.sqlite` while Codex is running. Use the wait-until-exit compaction watcher.

## Thresholds that were useful

- Empty Git wrapper plus hundreds or thousands of untracked files is a likely Git/Codex scan storm.
- `logs_2.sqlite` above 300 MB deserves inspection.
- More than 10,000 log rows in 24 hours is excessive for idle or light use.
- TRACE plus DEBUG above 50 percent of 24-hour rows means logging is too noisy for normal idle operation.
- If 3-second CPU sampling shows Codex processes consuming multiple CPU seconds on a 4-logical-processor machine, Codex itself is a primary load source.

## Confirmed local fixes

- For an empty wrapper repo, appending `*` to `.git/info/exclude` stopped the untracked-file scan storm without deleting or changing user files.
- Reducing enabled plugins to the current core set lowered startup/plugin surface. In this environment the core set was:
  - `superpowers@openai-curated`
  - `browser-use@openai-bundled`
  - `computer-use@openai-bundled`
- A compact preview database can be created read-only while Codex is running, but final replacement must wait until Codex exits.
- A watcher process with `compact-codex-logs-after-exit.ps1` and a `status.txt` file is the preferred low-risk way to compact logs after exit.

## Evidence from the 2026-06-07 run

- Git state after normalization: `tracked=0`, `untracked=0`.
- Enabled plugins after normalization: Superpowers, browser-use, computer-use.
- Large log database before offline compaction: `logs_2.sqlite` about 875 MB.
- Log volume was not reasonable for idle/light use: about 22,723 rows in 24 hours, with TRACE/DEBUG about 82.9 percent.
- Compact preview database was valid: about 207 MB, `integrity_check=ok`, about 51,539 rows retained.
- Remaining high idle CPU was mainly Codex Desktop itself: `OpenAI.Codex_26.602.4764.0` GPU process, renderers, and `codex.exe app-server`.

## Repeat route

1. Run `codex-chaos-health.ps1 -Mode Diagnose`.
2. If Git, plugin, or log findings are abnormal, run `-Mode Normalize`.
3. Confirm whether a compaction watcher is running.
4. If Codex remains high CPU and watcher is waiting, close and reopen Codex so offline compaction and config reload can happen.
5. After restart, run Diagnose again and compare CPU, Git counts, enabled plugins, log size, and log row mix.
