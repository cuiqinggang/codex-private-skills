---
name: codex-lite-power-upgrade
description: Use when upgrading, repairing, auditing, packaging, or smoke-testing this Windows Codex Desktop setup, especially tasks about stable Codex CLI/Desktop updates, GPT-5.5 preservation, lightweight plugin/skill curation, AGENTS.md policy, rollback, or yesterday-replay evidence.
---

# Codex Lite Power Upgrade

## Purpose

Use this skill to keep the local Codex Desktop system strong without making it bloated. It captures the 2026-05-25 upgrade result and provides the repeatable gate pattern for future upgrades.

## Required Order

1. Load `yesterday-replay-controlled-coding` first, then this skill.
2. For any real upgrade or repair, treat the task as Complex unless it is clearly read-only.
3. Do not install alpha, beta, pre-release, unknown-source plugins, broad MCP/toolbox bundles, or duplicate AI CLIs.
4. Preserve GPT-5.5 default model, Superpowers, global/project `AGENTS.md`, DeepSeek fallback routes, Hermes/OpenWebUI, and Xiaolongxia unless the user explicitly asks to change them.

## Gate Pattern

Use these gates for future upgrade work:

| Gate | Purpose | Stop If |
| --- | --- | --- |
| G01 | Read-only diagnosis: app/CLI versions, config, AGENTS, skills/plugins, model, toolchain | diagnostics incomplete or secrets would be exposed |
${REDACTED_SECRET}
| G03 | Stable upgrade from official npm/GitHub/MS Store/winget sources only | latest is prerelease only, install fails, or app needs manual Store update |
| G04 | Apply lite enhancement policy | requested dependency is low-trust or unrelated |
| G05 | Keep global `AGENTS.md` short, strong, and rollback-safe | default model or safety rules are broken |
| G06 | Curate plugin/skill inventory without destructive cleanup | deletion or broad disabling would be required |
| G07 | Run a real smoke task: write files, run script, save logs, browser-check HTML if available | marker output or browser check fails |
| G08 | Write final report with PASS/PARTIAL/STOP status and rollback path | evidence is missing |

Allowed final statuses:

- `CODEX_DESKTOP_LITE_POWER_UPGRADE_PASS`
- `CODEX_DESKTOP_LITE_POWER_UPGRADE_PARTIAL_PASS`
- `CODEX_DESKTOP_LITE_POWER_UPGRADE_STOP_FAILED`

## Reusable Checks

Run the bundled read-only check when you need a quick current-state snapshot:

```powershell
${REDACTED_SECRET}
```

It writes a timestamped JSON report under the current directory by default and never prints secrets.

For Open Design / Codex wrapper connectivity regressions, read
`references\open-design-codex-connectivity-20260527.md` and run the read-only
checker:

```powershell
${REDACTED_SECRET}
```

Use it when reconnect messages or wrapper timeouts look like Codex failures.
Do not patch or restart Open Design from this checker.

## References

- Read `references/upgrade-evidence-20260525.md` when you need the exact evidence, rollback paths, known pitfalls, and smoke-test result from the successful 2026-05-25 upgrade.
- Read `references/future-upgrade-template.md` when starting a new upgrade and you need copy-pasteable gate commands and report sections.
${REDACTED_SECRET}

## Common Pitfalls

- Do not treat "more plugins" as stronger. The target is stable official versions, clear workflow, and verified real tasks.
- Do not force Microsoft Store GUI updates from inside Codex when winget/MS Store already reports no newer stable package.
- Do not use `localhost:3000` for New API / AI Talking; that port is reserved for Hermes/Open WebUI in this workspace.
- If Playwright blocks `file:` pages, serve the smoke HTML with `python -m http.server --bind 127.0.0.1` and open `http://127.0.0.1:<port>/index.html`.
- For Playwright CLI screenshots, use `--filename`, not `--path`.
