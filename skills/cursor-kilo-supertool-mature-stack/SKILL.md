---
name: cursor-kilo-supertool-mature-stack
description: Use when Codex needs to reproduce, continue, audit, recover, verify, package, or hand off the user's mature Cursor + Kilo Code + OpenRouter AI coding super tool route without relying on Claude official login. Triggers include Cursor/Kilo super tool, Kilo First, OpenRouter DeepSeek V4 Pro, GLM-5.2 controller, Qwen3-VL vision, mature stack deployment, Stage4/Stage5, provider/model live smoke verification, recovery from reports/ZIPs, UI localization verification, Serena noise control, continuous verification logic repair, and packaging reports for another person to reproduce the same workflow.
---

# Cursor Kilo SuperTool Mature Stack

## Core Rule

Build and preserve a mature, reproducible Cursor/Kilo super tool stack. Do not chase similar tool names, cheap unstable models, or login bypasses. Prefer verified, repeatable routes with evidence.

## Master Goal

The final target is a mature AI Coding SuperTool ecosystem:

`Cursor + Kilo Code + OpenRouter proxy + OpenRouter-hosted DeepSeek V4 Pro / GLM-5.2 / Qwen3-VL-235B`.

This is not an empty new workstation. Use mature local assets, official docs,
existing skills, proven reports, Gate Review, Repair Loop, checkpoint/handoff,
and multimodal workflows. Keep the runtime entry light and store heavy
knowledge in the skill package and Knowledge Brain.

Read `references/MASTER-GOAL-20260702.md` before changing route priorities.

## Current Mature Matrix

Use this matrix unless a newer local report explicitly supersedes it:

| Layer | Model / Tool | Role |
|---|---|---|
| Main IDE | Cursor + Kilo Code | SuperTool entrypoint |
| Main executor | OpenRouter proxy / DeepSeek V4 Pro | Code execution, ordinary debug, ordinary project work |
| Strong controller | OpenRouter proxy / GLM-5.2 | Strong instruction following, complex command packs, long orchestration, Gate Review, Repair Loop, risk boundary checks |
| Vision primary | OpenRouter proxy / Qwen3-VL-235B-A22B-Instruct | Screenshot, UI, OCR, image, chart, video keyframe, multimodal understanding |
| Vision reasoning backup | OpenRouter proxy / Qwen3-VL-235B-A22B-Thinking | Hard visual reasoning backup |
| Light model | DeepSeek V4 Flash | Light tasks only if stable; otherwise use Pro |
| Disabled | Auto Model / Auto Free / Kilo Gateway defaulting | Keep disabled unless a later verified report changes this |

## Non-Negotiable Safety Boundaries

- Do not print full API keys, tokens, ID numbers, addresses, or phone numbers.
- Do not modify API keys, Hermes Gateway, Qwen direct vision config, Windows proxy/network, or unrelated user files.
- Do not reinstall Cursor, uninstall Kilo, enable CCR, or revive Claude Code mainline unless explicitly requested.
- Do not set low-cost 8B/30B vision models as default primary routes.
- Do not continue unexpected Cursor UI automation after the user reports surprise; use file/CLI evidence or ask before visible UI control.

## Start Workflow

0. **If this is the first time assessing maturity or recovering the station**, read `references/ASSET-SEARCH-PATHS.md` first to avoid search-scope misjudgments. Missing any of the 4 asset layers will cause severe underestimation.
1. Read `references/HANDOFF-SUMMARY.md` first for compact context.
2. Read `references/SOP.md` for the stage flow.
3. Read `references/CHECKLISTS.md` before changing configuration or generating reports.
4. If recovering the mature station, read `references/FULL-DEPLOY-ARTIFACTS.md`.
5. If model/provider proof is requested, read `references/LIVE-SMOKE-RECOVERY.md` and use real live-call evidence when authorized.
6. If verification/gate logic is being repaired, read `references/VERIFICATION-LOGIC.md`.
7. If model/provider/UI verification is requested, apply the existing `ui-setting-actual-open-self-verify-loop` skill unless the user explicitly forbids UI automation.
8. If long text paste or Ctrl+V paste fails in Cursor/Kilo, read `references/LONGTEXT-PASTE-RESTORE.md` and reuse the existing `cursor-kilo-terminal-paste-repair` plus `codex-pasted-text-attachment-repair` skills.
9. After every meaningful stage, run `scripts/sync_stage.py` to append the result into the skill's recent-use log.

## Evidence-First Acceptance

For deployment, model/provider, UI, or localization claims, prefer evidence:

- report path
- screenshot path
- model log path
- ZIP package path
- desktop numeric ZIP path
- exact final status string
- what was not touched

If UI evidence is incomplete because user asked to stop visible UI automation, say so plainly and do not claim full UI PASS.

For provider/model claims, distinguish:

- `active_config_confirmed`
- `local_report_confirmed`
- `user_decision_confirmed`
- `provider_catalog_confirmed`
- `live_call_verified`

Only set `live_call_verified=true` after an actual provider call returns a non-empty assistant text response.

## Desktop Numeric Package Rule

After every completed stage/task that produces a final report or evidence ZIP, also create a simple desktop handoff package:

- Use a three-digit numeric name such as `123`, `456`, `789`, or another available three-digit number.
- If the user provides a number, use that exact number.
${REDACTED_SECRET}
${REDACTED_SECRET}
- Put the final report, evidence ZIP, and the most important key files or README into the folder.
- If an existing folder or ZIP with that number exists, rename it to a timestamped backup first.
- Keep the numeric package compact. Do not copy browser profiles, node_modules, cache folders, or heavy source trees unless the user explicitly asks for a full archive.
- Mention the desktop numeric ZIP in the final answer.

## Key References

- `references/ASSET-SEARCH-PATHS.md`: **Complete 4-layer asset search path architecture. Read first when assessing maturity to avoid search-scope misjudgment.**
- `references/HANDOFF-SUMMARY.md`: compact current state and major outputs.
- `references/MASTER-GOAL-20260702.md`: top-level mature station target and route priority.
- `references/SOP.md`: reproducible step-by-step route.
- `references/CHECKLISTS.md`: preflight, stage, packaging, and safety checks.
- `references/DESKTOP-NUMERIC-PACKAGING-RULE.md`: mandatory simple desktop ZIP handoff rule.
- `references/MODEL-MATRIX.md`: model-routing rules.
- `references/LIVE-SMOKE-RECOVERY.md`: actual OpenRouter model smoke verification and recovery.
- `references/VERIFICATION-LOGIC.md`: bidirectional success/failure validation and gate repair.
- `references/KILO-UI-MODEL-STATE-FIX.md`: minimal Cursor state repair when Kilo UI falls back to DeepSeek V3.2 instead of OpenRouter DeepSeek V4 Pro.
- `references/KILO-CURSOR-MIDDLE-SCREEN-COORDINATE-VIRTUAL-INPUT.md`: middle-screen fullscreen Cursor/Kilo coordinate map and no-real-mouse/keyboard operation boundary.
- `references/LONGTEXT-PASTE-RESTORE.md`: Cursor/Kilo terminal Ctrl+V and Kilo long-text `@file` mention repair route.
- `references/FULL-DEPLOY-ARTIFACTS.md`: canonical station paths, latest packages, and compact recovery flow.
- `references/REPORT-TEMPLATE.md`: report sections for future stages.
- `references/FAILURE-MODES.md`: known traps and fixes.
- `references/recent-use-log.md`: append-only maturity log.

## Sync Rule

At the end of each completed stage, run:

```powershell
${REDACTED_SECRET}
```

Then include the updated skill path or package path in the final answer when relevant.
