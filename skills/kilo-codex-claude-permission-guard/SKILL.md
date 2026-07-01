---
name: kilo-codex-claude-permission-guard
description: Use when verifying, repairing, or documenting the user's unified permission boundary for Codex Desktop, Kilo Code, Claude Code/ECC, and Hermes on Windows: ordinary work is allowed by default, while Windows core changes and network/proxy changes must ask for explicit approval.
---

# Kilo Codex Claude Permission Guard

## Purpose

Keep one reusable permission boundary across the local AI workbench:

- Codex Desktop may do ordinary project, document, browser, reporting, coding, backup, and validation work directly.
- Kilo Code/Cursor may use the mature OpenRouter route without changing API keys, gateway settings, Windows proxy, or unrelated files.
- Claude Code/ECC may be used only as a visible or logged executor, not as a hidden permission bypass.
- Hermes checks must stay layered and must not reconnect Telegram, New API, proxy, watchdog, startup, Docker, WSL, or scheduled tasks unless the user explicitly asks.
- Windows core operations and network/proxy operations must ask the user in Chinese before execution.

This skill does not replace `codex-permission-policy`; it binds that policy to Kilo, Claude Code/ECC, and Hermes.

## Trigger Phrases

Use this skill when the user says or implies:

- Kilo 权限问题
- Codex 权限设置
- Claude Code 权限
- 爱马仕 / Hermes 权限
- Windows 系统不能破坏
- 网络代理不能破坏
- 其他全部批准
- 重启后验证权限是否还生效
- 昨天的权限方案是否写成技能包

## Canonical Policy

Default allow:

- read/write inside normal project and output folders;
- create reports, backups, HTML acceptance pages, skill notes, and logs;
- run normal development commands, tests, local scripts, status checks, and read-only diagnostics;
- inspect config files with secrets redacted;
- browser and screenshot workflows when they do not change accounts, payments, security, Windows core state, or network/proxy state.

Must ask before execution:

- registry, Windows services, startup items, scheduled tasks, drivers, PATH or system environment variables;
- Hyper-V, WSL, Docker runtime/base changes;
- system directories, disk formatting, partitioning, shutdown/restart, broad process killing;
- system proxy, browser proxy, Clash/FlClash/v2ray/sing-box/Shadowsocks, Telegram proxy, DNS, hosts, firewall, routes, port mapping, proxy clients, or stopping/restarting proxy software;
- API key changes, credential migration, login bypass, or printing tokens/secrets.

Uncertain cases:

- stop before execution and ask in Chinese;
- explain what would be done, why it may affect Windows or network/proxy state, possible consequences, rollback, and safer alternatives.

## Required Read Order

1. Read this skill.
2. Read `C:\Users\A\.codex\skills\codex-permission-policy\SKILL.md`.
3. If Kilo is involved, read:
   - `C:\Users\A\.codex\skills\cursor-kilo-supertool-mature-stack\references\HANDOFF-SUMMARY.md`
   - `C:\Users\A\.codex\skills\cursor-kilo-supertool-mature-stack\references\SOP.md`
   - `C:\Users\A\.codex\skills\cursor-kilo-supertool-mature-stack\references\CHECKLISTS.md`
4. If Hermes is involved, read the relevant `hermes-014-restoration-ladder` reference for the exact stage. Do not collapse stages.
5. If this is a knowledge reuse or skill-deployment task, check:
   - `K:\AI\knowledge-brain\INDEX.md`
   - `K:\AI\knowledge-brain\ROUTING_MAP.md`
   - `K:\AI\knowledge-brain\indexes\skills-index.md`

## Read-Only Validation SOP

Do not mutate protected state during validation.

1. Confirm Codex config:
   - `C:\Users\A\.codex\config.toml` exists.
   - `approval_policy = "on-request"`.
   - `sandbox_mode = "danger-full-access"`.
   - `approvals_reviewer = "auto_review"`.
   - `[windows] sandbox = "elevated"`.
   - `[auto_review] policy` exists.
2. Confirm Codex rules:
   - `C:\Users\A\.codex\rules\default.rules` exists.
   - prompt rules include at least `netsh`, `route`, `ipconfig`, `reg`, `sc`, `schtasks`, `docker`, `wsl`, `diskpart`, `format`, and `setx`.
3. Confirm UI state carefully:
   - targeted check only for `agent-mode-by-host-id` and `custom` in `.codex-global-state.json`;
   - never dump prompt history, drafts, cookies, tokens, or secrets.
4. Confirm Kilo route without secrets:
   - `C:\Users\A\.config\kilo\kilo.jsonc` exists when Kilo is installed;
   - model is `openrouter/deepseek/deepseek-v4-pro` unless a newer verified report supersedes it;
   - `snapshot` is `false`;
   - do not print API keys.
5. Confirm Claude Code/ECC boundary:
   - Claude Code may be present under `C:\Users\A\.claude`;
   - do not print credentials or project transcript contents;
   - do not use Claude Code login bypass;
   - implementation runs must be visible or logged with changed-file/test evidence.
6. Confirm Hermes boundary:
   - stage checks are read-only unless the user explicitly requests restoration;
   - do not reconnect New API, Telegram, watchdog, startup tasks, Docker, WSL, or proxy layers as a side effect.

## Repair SOP

If Codex config drifted:

1. Back up `config.toml` and `default.rules` with timestamped names.
2. Preserve unrelated runtime, plugin, marketplace, MCP, model, desktop, and project trust settings.
3. Restore only missing permission policy fields and prompt rules.
4. Generate an acceptance report.
5. Tell the user to fully quit and reopen Codex Desktop, then select custom/config mode if the UI is not already there.

If Kilo model route drifted:

1. Use the Kilo mature-stack skill.
2. Prefer the minimal Kilo UI/model state repair reference.
3. Do not alter API keys, OpenRouter account, Hermes Gateway, or Windows proxy.

If Claude Code/ECC drifted:

1. Treat Claude Code as an optional executor, not the main route.
2. Do not repair by changing login/session/auth files unless explicitly approved.
3. Keep output visible/logged and evidence-backed.

If Hermes drifted:

1. Restore one ladder stage at a time only when requested.
2. Stop at the narrow failing layer.

## Acceptance Criteria

Mark PASS only when:

- Codex config and rules match the canonical policy;
- Kilo route check shows no model/snapshot drift or the drift has a named repair path;
- no protected Windows or network/proxy operation was executed during validation;
- a report states exactly what was checked, what was not touched, and what would require approval;
- this skill has a recent-use log entry.

Mark PARTIAL when:

- UI selection cannot be visually confirmed in the current session;
- Kilo or Claude Code files are missing but the Codex policy itself is correct;
- a live provider call is not authorized or not needed.

## Recent Use Log

Append durable usage notes to:

```text
C:\Users\A\.codex\skills\kilo-codex-claude-permission-guard\recent-use-log.md
K:\AI\skills\kilo-codex-claude-permission-guard\recent-use-log.md
```

