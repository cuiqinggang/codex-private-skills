# Hermes 0.14 H-drive Restore Decision Summary

Decision: H:\_FULL_RECOVERY_Hermes_Windows_Native_014_20260520 is the strongest restore source found.

Evidence:
- Prior Codex session C:\Users\A\.codex\sessions\2026\05\19\rollout-2026-05-19T20-54-14-019e404d-15af-7a31-b738-87e7aad54e88.jsonl contains the final answer saying this full recovery backup was created.
- Backup README says this folder is the full recovery package for Windows-native Hermes 0.14.
- VerifiedTotalFileCount: 12792
- BackupSizeMB: 268.16
- ZipReadFailures: 0
- InstallZipEntries: 9878
- ActiveSkillsZipEntries: 990
- HermesUserHomeRobocopyDryRunPassed: True
- HermesUserHomeDryRunFailed: 0
- HermesUserHomeDryRunExtras: 0
- HermesRestartedDuringBackup: False

Important correction:
- The older G05 command from the supplied GPT_PLAN points first to a missing 20260518 robocopy baseline, so do not execute that exact G05 as-is.
- For restore, use the 20260520 full recovery RESTORE_GUIDE.md and its private .hermes source path.

Level 3 boundary:
- No overwrite was executed in this run.
- Any restore to C:\Users\A\.hermes or H:\Hermes_Windows_Native_014 still needs explicit user confirmation.
