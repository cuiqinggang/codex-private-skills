---
name: openclaw-upgrade-no-model
description: Upgrade and verify OpenClaw / 閻忓繐绻樼欢鎶芥惞?without connecting any large model provider. Use when the user asks to update OpenClaw to latest stable, check installed version, smoke-test gateway/dashboard transport, preserve old skills/history, or prepare for later model onboarding while explicitly avoiding API keys, OpenRouter/Kimi, Pangu, server model setup, default model changes, or real model calls.
---

# OpenClaw Upgrade No Model

## Core Boundary

Treat OpenClaw / 閻忓繐绻樼欢鎶芥惞?as separate from Hermes / 闁绘牠浜堕埞鍫熺? Do not reuse Hermes ports, services, watchdogs, or model routing as OpenClaw facts.

This skill is for upgrade and transport verification only. Do not connect any model provider, write API keys, change the default model, run a Q&A/model probe, configure OpenRouter/Kimi/Pangu/server models, or export browser credentials.

## Workflow

1. Load local workspace instructions and any required first-run control skill.
2. Search yesterday-replay evidence before changing anything:
   - `H:\openclaw-recovery-20260427-skill-pack.zip`
   - `H:\_KEEP_Unmatched_Hermes_Skills_20260519\OpenClaw_Skill_Backups`
   - `H:\_KEEP_Unmatched_Hermes_Skills_20260519\OpenClaw_Full_Backups`
   - `C:\Users\A\.openclaw`
   - WSL `Ubuntu-24.04:/home/u123456/.openclaw` only if WSL commands are healthy
3. Inventory current state:
   - `node --version`
   - `npm --version`
   - `openclaw --version`
   - `npm list -g openclaw --depth=0`
   - `npm view openclaw version dist-tags engines --json`
   - `openclaw update status --json`
   - listener check for `127.0.0.1:18789`
4. Back up before upgrade:
   - `C:\Users\A\.openclaw`
   - `C:\Users\A\AppData\Roaming\npm\node_modules\openclaw`
   - npm shims `openclaw.cmd` and `openclaw.ps1`
   - old OpenClaw skill package and run evidence
5. Prefer official updater when dry-run is clean:
   - dry run: `openclaw update --dry-run --tag latest --no-restart --json`
   - execute: `openclaw update --tag latest --no-restart --yes --json --timeout 600`
   - fallback: `npm install -g openclaw@latest --no-fund --no-audit`
6. Verify latest stable:
   - `openclaw --version`
   - `npm list -g openclaw --depth=0`
   - `npm view openclaw version dist-tags engines --json`
   - `openclaw update status --json`
7. Smoke-test transport only with a temporary token:
   - start a temporary loopback gateway with `--allow-unconfigured --bind loopback --port 18789 --auth token --token [REDACTED]
   - verify `openclaw gateway health --token [REDACTED] --json --timeout 20000`
   - verify HTTP root returns 200
   - stop all gateway processes started by the test
8. Run no-model check:
   - confirm `openclaw.json` and `auth-profiles.json` status
   - search config files for `openrouter`, `moonshotai`, `kimi-k2.5`, `pangu`, `pan-gu`, `闁烩晜锚瑜版竴
   - confirm no key-like secret was written
9. Report PASS/PARTIAL with exact commands, paths, and remaining gates.

## Stop Gates

Stop before any of these unless the user explicitly starts a separate model/autostart/browser task:

- Writing API keys or auth profiles.
- Setting `openrouter/moonshotai/kimi-k2.5`, Pangu, or any server model as default.
- Running model probes, chat tests, or minimal Q&A.
- Installing gateway service, Task Scheduler entries, watchdogs, or reboot autostart.
- Repairing WSL with `wsl --shutdown`, firewall, portproxy, or network changes.
- Opening or automating browser login state.

## 2026-05-23 Baseline

Read `references/20260523-upgrade-report.md` for the completed no-model upgrade evidence.

Known result:

- Windows OpenClaw upgraded from `2026.3.13` to `2026.5.20`.
- npm latest at verification time was `2026.5.20`.
- Node was `v24.14.0`.
- Gateway transport smoke test returned health `ok: true` with a temporary token.
- No large model provider was connected.
- WSL `Ubuntu-24.04` command execution was unhealthy and not used for upgrade.

## References

- `references/20260523-upgrade-report.md`: final report and status.
- `references/20260523-current-state.md`: current state before upgrade.
- `references/20260523-history-map.md`: old local evidence and reusable paths.
- `references/20260523-backup-manifest.md`: backup root and manifest summary.
- `references/20260523-upgrade-plan.md`: chosen route and rollback.
- `references/20260523-final-version-check.txt`: latest-version verification evidence.
- `references/20260523-no-model-check.txt`: no-model/no-key evidence.

