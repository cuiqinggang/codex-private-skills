---
name: hermes-014-restoration-ladder
description: Use when restoring Windows native Hermes 0.14 from a minimal clean state toward Open WebUI, New API, Telegram, watchdog, or reboot persistence, especially after startup conflicts, disabled tasks, invalid DeepSeek keys, or multi-entry repair work.
---

# Hermes 0.14 Restoration Ladder

Use this skill to rebuild the local Hermes system one verified layer at a time.
Do not restore every integration at once.

## Core Rule

Work as a ladder:

1. Stage 00: Hermes 8642 only, direct DeepSeek V4 Pro.
2. Stage 01: Open the Hermes desktop panel through Open WebUI 3000.
3. Stage 02: Reconnect New API only when explicitly requested after Stage 01 passes.
4. Stage 03: Reconnect Telegram only when explicitly requested after a known-good baseline. Record whether New API is included; the 2026-05-22 P3 baseline is Telegram-only from P1/P2 and does not include New API.
5. Stage 04a: Add the silent 8642 healthcheck lifeline only.
6. Stage 04b: Add desktop/Open WebUI auto-open after 8642 lifeline is mature.

Each stage must have:

- a known previous state
- exact PowerShell gates
- artifact logs under `C:\Users\A\Desktop\1\output`
- pass/fail evidence
- no printed secrets
- no deletion of old files unless the user explicitly asks

## Required References

- Read `references/stage-00-minimal-deepseek.md` when the goal is to return
  Hermes to the minimal DeepSeek-only state or recover from DeepSeek 401.
- Read `references/stage-01-openwebui-panel.md` when the goal is to open the
  Hermes desktop panel / Open WebUI after the minimal state passes.
- Read `references/p1p2-stable-baseline-20260522.md` when the user asks whether
  the current minimal Hermes plus Open WebUI state is a stable baseline, or when
  planning the next restoration layer from the known-good P1+P2 state.
- Read `references/stage-03-telegram-restored-20260522.md` when continuing from
  the P1/P2 baseline after Telegram has been manually restored without New API,
  Watchdog, AutoRecover, or reboot persistence.
- Read `references/stage-04-8642-silent-healthcheck-20260522.md` when the user
  asks to keep Hermes 8642 alive silently every 1-2 minutes without restoring
  New API, old Watchdog, AutoRecover, or desktop browser autostart.
- Read `references/stage-04b-openwebui-autoopen-20260522.md` when the user asks
  to auto-open the Hermes desktop panel / Open WebUI after login, after the
  Stage 04a 8642 lifeline is already mature.
- Read `references/stage-04b-openwebui-autoopen-build-runbook-20260522.md` when
  the user asks how Stage 04b was built, how to reproduce it, where the scripts
  are stored, or how to verify/rollback the auto-open flow after a reboot.

Stages not named in the selected reference remain unrestored, even if another
stage has passed. Do not infer New API or reboot persistence from the
Telegram-only P3 reference.

## Stop Conditions

Stop and report the narrow failing layer if:

- `/health` on `http://127.0.0.1:8642` is not 200.
- `/v1/models` does not include `hermes-agent`.
- chat does not return the requested marker.
- a stage starts New API, Telegram, Watchdog, or AutoRecover before that stage
  is explicitly requested.
- a command would print an API key, token, password, Open WebUI JWT, or upstream
  provider secret.

## Common Mistakes

- Do not treat current service health as reboot persistence proof.
- Do not re-enable Startup entries or scheduled tasks during Stage 00 or Stage 01.
- Do not run New API or Telegram checks while restoring only the panel layer.
- Do not treat the 2026-05-22 Telegram-only P3 restore as proof that New API,
  Watchdog, AutoRecover, or login autostart are active.
- Do not mix the 8642 silent healthcheck with desktop/Open WebUI autostart; that
  is a later stage.
- Do not use broad process killing without excluding the current PowerShell
  process and verifying 8642 afterward.
- Do not preserve an invalid DeepSeek key just because `/v1/models` still works.
