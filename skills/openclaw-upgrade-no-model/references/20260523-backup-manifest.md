# backup-manifest.md

TASK_ID: OPENCLAW-UPGRADE-REPLAY-AUTOLOGIN-SKILL-UPDATE-20260523
Generated: 2026-05-23

Backup root: 

## Result

- Windows OpenClaw state backed up to H drive.
- Key-file SHA256 written to backup-sha256-keyfiles.csv.
- Full node_modules hash was intentionally not completed after the first hash sweep proved too slow; key manifests and package metadata are hashed instead.
- WSL /home/u123456/.openclaw was not copied because WSL command execution failed during G02.

## Backed Up Items

See backup-manifest.csv and backup-manifest.json in the backup root. Highlights:

- C:\Users\A\.openclaw
- C:\Users\A\AppData\Roaming\npm\node_modules\openclaw
- C:\Users\A\AppData\Roaming\npm\openclaw.cmd and openclaw.ps1
- H:\openclaw-recovery-20260427-skill-pack.zip
- H:\_KEEP_Unmatched_Hermes_Skills_20260519\OpenClaw_Skill_Backups\da53b91e9a_openclaw-recovery-20260427
- This task evidence directory

## Backup Verification

- robocopy-windows-npm-openclaw-package.log: 36,996 files total, 28,456 copied, 8,540 skipped, 0 failed, 406.72 MB copied.
- robocopy-windows-user-openclaw.log: 35 files total, 0 failed, destination already had matching copied files from the first attempt.
- source old skill and task-run evidence copied with 0 failed.
