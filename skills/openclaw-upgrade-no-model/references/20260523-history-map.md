# history-map.md

TASK_ID: OPENCLAW-UPGRADE-REPLAY-AUTOLOGIN-SKILL-UPDATE-20260523
Generated: 2026-05-23

## Key Local Evidence

| Path | Type | Time/Version | Confidence | Reusable point |
|---|---|---:|---|---|
| H:\openclaw-recovery-20260427-skill-pack.zip | User-provided old skill pack | 2026-04-27 / file modified 2026-04-27 23:41 | High | Contains original OpenClaw recovery skill pack and commands. |
| H:\_KEEP_Unmatched_Hermes_Skills_20260519\OpenClaw_Skill_Backups\da53b91e9a_openclaw-recovery-20260427\SKILL.md | H-drive archived OpenClaw recovery skill | Records OpenClaw 2026.4.25 | High | Mature route: check gateway listener first, then CLI, then npm package; if package is broken, reinstall package only and keep ~/.openclaw. |
| H:\_KEEP_Unmatched_Hermes_Skills_20260519\OpenClaw_Full_Backups\7f5016ef68_openclaw-backup\SKILL.md | Old backup skill | 2026-05-19 archive | Medium | Backup/restore pattern for ~/.openclaw and workspace. |
| C:\Users\A\.openclaw | Current Windows OpenClaw state | Files from Mar-May 2026 | High | Current Windows node host config and historical node.cmd backups. |
| C:\Users\A\AppData\Roaming\npm\node_modules\openclaw | Current Windows npm install | openclaw@2026.3.13 | High | Current install source; official update can operate here. |
| C:\Users\A\Desktop\OpenClaw-Edge-Token-Start.ps1 | Expected desktop script | Missing at G02 | High | Needs creation/repair later if autostart/browser flow proceeds. |
| Ubuntu-24.04:/home/u123456/.openclaw | Expected WSL state | Not reachable in G02 | Medium | WSL command layer currently blocks; do not assume WSL config until service is healthy. |

## Historical Successful Route Extracted

- Historical good version: OpenClaw 2026.4.25 (aa36ee6).
- Historical user/path: Ubuntu-24.04, user u123456, /home/u123456/.npm-global/bin/openclaw and /usr/local/bin/openclaw.
- Historical port: 18789.
- Historical recovery principle: do not reset ~/.openclaw first; check listener, CLI, npm package integrity, then reinstall only the program package if needed.
- Historical gateway command pattern: openclaw gateway run --port 18789 --force --verbose.
- Historical bind lesson: Windows 127.0.0.1:18789 failures mean gateway or WSL networking must be verified, not assumed.

## Separation Note

OpenClaw/xiaolongxia and Hermes/aimaishi are treated as separate systems. Port 18789 and C:\Users\A\.openclaw belong to OpenClaw evidence only. Hermes ports and skills are not used as OpenClaw runtime inputs.
