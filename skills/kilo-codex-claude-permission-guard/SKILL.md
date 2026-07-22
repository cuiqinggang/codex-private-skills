---
name: kilo-codex-claude-permission-guard
description: "Use when verifying, repairing, or documenting the user's unified permission boundary for Codex Desktop, Kilo Code, Claude Code/ECC, and Hermes on Windows: ordinary work is allowed by default, while Windows core changes and network/proxy changes must ask for explicit approval."
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

Use blacklist mode, not a fragile ordinary-tool allowlist.

Default allow:

- read/write inside normal project and output folders;
- create reports, backups, HTML acceptance pages, skill notes, and logs;
- run normal development commands, dependency installs inside ordinary projects, tests, local scripts, status checks, and read-only diagnostics;
- run ordinary search/research tools such as web search, Firecrawl search/scrape/map/crawl, local rg/grep/find, browser reading, and document extraction;
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

## Blacklist Mode Implementation Matrix

Codex Desktop:

${REDACTED_SECRET}
- `[auto_review].policy` must state the blacklist rule plainly: only Windows system core and network/proxy operations require approval; ordinary work is allowed.
${REDACTED_SECRET}

Kilo Code:

${REDACTED_SECRET}
- Keep explicit `ask` or `deny` entries for Windows core and network/proxy patterns before the catch-all.
- Set the catch-all ordinary command entry to `"*": "allow"`.
- Set ordinary tool capabilities such as `external_directory`, `websearch`, `webfetch`, `doom_loop`, `agent_manager`, and `task` to `"allow"` unless a newer risk review says otherwise.
- Keep the mature model route intact: `openrouter/deepseek/deepseek-v4-pro`, `deepseek-v4-flash` for small model, and `snapshot=false`.
- Never repair Kilo permission prompts by changing OpenRouter keys, Hermes Gateway, system proxy, DNS, firewall, or browser proxy.

Hermes:

${REDACTED_SECRET}
- Do not use `approvals.mode: off` or `--yolo` as the normal fix.
- Hermes `command_allowlist` supports exact/glob patterns for single commands. Add explicit ordinary command patterns there; do not add a naked `*` unless Hermes has a verified denylist layer that still blocks Windows/proxy changes.
- Good ordinary allowlist examples: `Get-ChildItem *`, `Get-Content *`, `Set-Content *`, `New-Item *`, `Copy-Item *`, `Move-Item *`, `python *`, `node *`, `npm *`, `rg *`, `git status *`, `git diff *`, `git log *`, `git show *`, `firecrawl *`, `curl *`, `wget *`, `Invoke-WebRequest *`, `iwr *`, `irm *`.
- Do not reconnect Telegram, New API, watchdog, startup tasks, Docker, WSL, proxy, DNS, firewall, route, or gateway layers as a side effect of permission repair.

Do not use a blacklist-mode repair to approve destructive broad deletion against user data. Treat broad recursive deletion, system directory writes, and credential changes as protected unless the user explicitly asks for that exact action.

## Required Read Order

1. Read this skill.
${REDACTED_SECRET}
3. If Kilo is involved, read:
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
4. If Hermes is involved, read the relevant `hermes-014-restoration-ladder` reference for the exact stage. Do not collapse stages.
5. If this is a knowledge reuse or skill-deployment task, check:
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
   - Treat `K:\AI` copies as backup/archive/restore/delivery-only. Missing C assets must return `BLOCKED_C_SOURCE_MISSING`; only explicit user authorization may start a separate restore inspection. Never auto-fallback.

## Read-Only Validation SOP

Do not mutate protected state during validation.

1. Confirm Codex config:
${REDACTED_SECRET}
   - `approval_policy = "on-request"`.
   - `sandbox_mode = "danger-full-access"`.
   - `approvals_reviewer = "auto_review"`.
   - `[windows] sandbox = "elevated"`.
   - `[auto_review] policy` exists.
2. Confirm Codex rules:
${REDACTED_SECRET}
   - prompt rules include at least `netsh`, `route`, `ipconfig`, `reg`, `sc`, `schtasks`, `docker`, `wsl`, `diskpart`, `format`, and `setx`.
3. Confirm UI state carefully:
   - targeted check only for `agent-mode-by-host-id` and `custom` in `.codex-global-state.json`;
   - never dump prompt history, drafts, cookies, tokens, or secrets.
4. Confirm Kilo route without secrets:
${REDACTED_SECRET}
   - model is `openrouter/deepseek/deepseek-v4-pro` unless a newer verified report supersedes it;
   - `snapshot` is `false`;
   - do not print API keys.
5. Confirm Claude Code/ECC boundary:
${REDACTED_SECRET}
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
3. Restore only missing permission policy fields, the blacklist wording, `[windows] sandbox = "elevated"`, and prompt rules.
4. Generate an acceptance report.
5. Tell the user to fully quit and reopen Codex Desktop, then select custom/config mode if the UI is not already there.

If Kilo permission prompts appear for ordinary tools:

${REDACTED_SECRET}
2. Confirm the prompt is not for Windows core, network/proxy, credentials, destructive broad deletion, or account/security changes.
3. Add or preserve protected `ask`/`deny` blacklist entries before the catch-all.
4. Set ordinary command catch-all to `"*": "allow"` and set ordinary Kilo tool capabilities to `"allow"`.
5. Validate JSON parse, model route, and `snapshot=false`.

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
${REDACTED_SECRET}
4. Do not use `approvals.mode: off`, `--yolo`, or startup/gateway/proxy edits as a permission repair.

## Acceptance Criteria

Mark PASS only when:

- Codex config and rules match the canonical policy;
- Kilo uses blacklist-mode permissions for ordinary work while Windows/proxy patterns remain ask/deny;
- Hermes keeps smart approvals and explicit ordinary command allowlist entries without global approval bypass;
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
${REDACTED_SECRET}
${REDACTED_SECRET}
```
