# upgrade-plan.md

TASK_ID: OPENCLAW-UPGRADE-REPLAY-AUTOLOGIN-SKILL-UPDATE-20260523
Generated: 2026-05-23

## Goal

Upgrade the currently usable Windows OpenClaw npm installation from 2026.3.13 to official latest 2026.5.20, verify CLI/config/model/gateway basics, and avoid mixing OpenClaw with Hermes.

## Chosen Route

Use OpenClaw's own updater in npm package mode:

```powershell
openclaw update --tag latest --no-restart --yes --json --timeout 600
```

Reason:

- Official npm metadata shows latest is 2026.5.20 and Node requirement is >=22.19.0.
- Local Node is v24.14.0, which satisfies the current requirement.
- `openclaw update --dry-run --tag latest --no-restart --json` succeeded and identified the exact package update.
- `--no-restart` avoids silently starting/restarting services before gateway/network verification.

## Verification Commands

```powershell
openclaw --version
npm list -g openclaw --depth=0
openclaw update status --json
openclaw models status --json
openclaw gateway --help
```

Then, after upgrade only if safe:

```powershell
openclaw gateway run --allow-unconfigured --bind loopback --port 18789 --verbose
openclaw gateway health
openclaw dashboard --no-open
```

## Rollback

If the updater fails or the new CLI is unusable:

```powershell
npm install -g openclaw@2026.3.13
```

If shims/config are damaged, restore from the H-drive backup root recorded in backup-manifest.md.

## Stop Conditions

Stop before these actions unless explicitly approved in a narrow gate:

- Writing the provided OpenRouter API key into any config/auth store.
- Creating or changing Task Scheduler/system daemon/autostart entries.
- Running WSL repair commands such as wsl --shutdown, unregister/import, firewall or portproxy changes.
- Opening or automating real browser login state.
- Exposing OpenClaw beyond local loopback.

## Known Blocker

WSL Ubuntu-24.04 currently fails minimal command probes. WSL OpenClaw upgrade and WSL dashboard validation must wait until WSL command execution is healthy.
