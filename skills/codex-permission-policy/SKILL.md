---
name: codex-permission-policy
description: Use when configuring, repairing, updating, validating, or documenting local Codex permission policy so ordinary tasks run directly while Windows core operations and network/proxy changes require user approval.
---

# Codex Permission Policy

## Purpose

Use this skill when the user wants Codex Desktop permissions set to:

- ordinary project, document, browser, reporting, read-only, backup, and development tasks run directly;
- Windows system core operations require approval;
- network, DNS, hosts, firewall, route, port mapping, and proxy-related operations require approval;
- uncertain cases require approval with a clear Chinese explanation.

Current canonical mode is blacklist mode:

- The only default approval blockers are Windows system core changes and network/proxy-chain changes.
- Ordinary work is allowed by default: project file work, normal coding, reports, screenshots, browser reading, web/search/read-only research, Firecrawl-style search/scrape, package installs inside ordinary projects, logs, local validation, and document processing.
- Do not build a fragile allowlist where each new ordinary tool falls through to approval.
- Keep explicit prompt rules for the protected blacklist, and let everything outside that blacklist run normally.

This skill is for Codex configuration and acceptance reporting only. It must not perform the protected Windows or proxy operations itself.

## Safety Boundary

Do not execute these operations while applying this skill:

- modify system proxy, browser proxy, DNS, hosts, firewall, routes, or port mappings;
- modify registry, Windows services, startup items, scheduled tasks, system environment variables, drivers, Hyper-V, WSL, Docker base/runtime, or system directories;
- restart, shut down, format disks, repartition disks, or kill critical processes;
- delete or print `auth.json`, login state, tokens, cookies, sessions, passwords, or secrets;
- stop proxy software or core studio services.

If a requested action falls into those categories, stop before execution and ask for approval in Chinese. Explain what will be done, why it may affect Windows or network/proxy state, possible consequences, rollback, and safer alternatives.

## Standard Paths

Default Codex config paths:

```text
${REDACTED_SECRET}
${REDACTED_SECRET}
```

For acceptance workspaces, use the C-drive task workspace:

```text
${REDACTED_SECRET}
```

Do not automatically fall back to H or K. If the required C-drive source is missing, stop with `BLOCKED_C_SOURCE_MISSING`; read H only when the user explicitly requests a historical check.

## Workflow

${REDACTED_SECRET}
2. Back up existing files before modifying them:
   - `config.toml` to `config.backup.<slug>.toml`;
   - `default.rules` to `default.backup.<slug>.rules`;
   - copy any backups to the task workspace.
3. Update `config.toml` while preserving unrelated existing settings such as marketplaces, plugins, desktop settings, MCP servers, model settings, runtime paths, and trusted projects.
4. Create or update `default.rules` using Codex rules syntax.
5. Run only read-only validation checks.
6. Generate a clickable HTML acceptance report when the user asks for a full repair/configuration task.
7. Tell the user to fully quit and reopen Codex Desktop, then choose `自定义 (config.toml)` in the permission menu if it is not already selected.

## Activation And Persistence Check

After the user selects `自定义 (config.toml)` in the Codex permission menu, the check mark next to that item means the current UI session is using the custom config. Treat that screenshot as positive evidence, then verify the local files.

On every repair/update pass:

${REDACTED_SECRET}
${REDACTED_SECRET}
- confirm `[windows] sandbox = "elevated"` did not drift to `"unelevated"`;
${REDACTED_SECRET}
- if the desktop app rewrote unrelated runtime fields such as `notify`, MCP runtime paths, plugin versions, marketplace timestamps, model, or project trust entries, preserve them;
- if only the Windows sandbox value drifted, back up the config and restore `sandbox = "elevated"`.

Do not try to force persistence by editing undocumented app state, registry keys, startup items, services, or system settings. If the UI shows another mode such as `完全访问权限`, ask the user to select `自定义 (config.toml)` again and then rerun this skill for validation.

## Required Config Policy

Ensure `config.toml` contains these top-level settings and sections:

The `[auto_review].policy` text should use this current Chinese rule, even if older examples in this file show mojibake from previous console encoding:

```text
Codex/Kilo/Hermes 统一权限原则：黑名单保护，普通任务默认放行。

黑名单只有两类：一是 Windows 系统核心操作，二是网络/代理链路操作。除这两类之外，普通项目、文档、代码、搜索、浏览、截图、报告、备份、测试、安装项目依赖、读取日志、Firecrawl/search/scrape、文件整理和普通开发命令默认允许，直接执行，不要频繁打断用户。

必须申请批准的 Windows 系统核心操作：修改注册表、Windows 服务、启动项、计划任务、系统环境变量、PATH、驱动、Hyper-V、WSL、Docker 底座、系统目录、关机重启、格式化、磁盘分区、强杀关键进程、安装/卸载会改变系统运行环境的软件。

必须申请批准的网络/代理链路操作：修改系统代理、浏览器代理、Clash、v2ray、sing-box、Shadowsocks、跑步云、Telegram 代理、DNS、hosts、防火墙、路由、端口映射、代理订阅、代理配置；停止、重启、禁用代理软件或服务。
```

```toml
approval_policy = "on-request"
sandbox_mode = "danger-full-access"
approvals_reviewer = "auto_review"
web_search = "cached"

[windows]
sandbox = "elevated"

[shell_environment_policy]
inherit = "core"
ignore_default_excludes = false

[auto_review]
policy = """
Codex 本机权限原则：

除了 Windows 系统核心操作和网络代理相关操作必须申请用户批准以外，其他普通任务全部默认允许、直接执行，不要频繁打断用户。

默认允许：
项目目录内文件读写、文档整理、代码修改、日志读取、截图、浏览器普通操作、只读搜索、端口检测、服务状态检测、普通脚本运行、创建普通备份、生成报告、生成可点击 HTML 验收页、资料整理、普通开发任务。

必须申请批准的 Windows 系统核心操作：
修改注册表、Windows 服务、启动项、计划任务、系统环境变量、PATH、驱动、Hyper-V、WSL、Docker 底座、系统目录、关机重启、格式化、磁盘分区、强杀关键进程、安装卸载会改变系统运行环境的软件。

必须申请批准的网络代理相关操作：
修改系统代理、浏览器代理、Clash、v2ray、sing-box、Shadowsocks、跑步云、Telegram 代理、DNS、hosts、防火墙、路由、端口映射、代理订阅、代理配置；停止、重启、禁用代理软件或服务。

判断规则：
不属于 Windows 系统核心操作，也不属于网络代理相关操作，默认批准。
属于 Windows 系统核心操作，必须申请批准。
属于网络代理相关操作，必须申请批准。
不确定时必须申请批准。

申请批准时必须用中文说明：
准备执行什么、为什么可能影响 Windows 系统或网络代理、可能后果、如何回滚、是否有更安全替代方案。
"""
```

If `[windows]` already exists, keep it and ensure `sandbox = "elevated"` is present once. Avoid duplicating table headers.

## Required Rules

Use this Codex rules syntax:

```text
prefix_rule(pattern = ["netsh"], decision = "prompt")
prefix_rule(pattern = ["route"], decision = "prompt")
prefix_rule(pattern = ["ipconfig"], decision = "prompt")
prefix_rule(pattern = ["reg"], decision = "prompt")
prefix_rule(pattern = ["sc"], decision = "prompt")
prefix_rule(pattern = ["Stop-Service"], decision = "prompt")
prefix_rule(pattern = ["Set-Service"], decision = "prompt")
prefix_rule(pattern = ["Restart-Service"], decision = "prompt")
prefix_rule(pattern = ["schtasks"], decision = "prompt")
prefix_rule(pattern = ["bcdedit"], decision = "prompt")
prefix_rule(pattern = ["shutdown"], decision = "prompt")
prefix_rule(pattern = ["Restart-Computer"], decision = "prompt")
prefix_rule(pattern = ["Stop-Computer"], decision = "prompt")
prefix_rule(pattern = ["taskkill"], decision = "prompt")
prefix_rule(pattern = ["wsl"], decision = "prompt")
prefix_rule(pattern = ["docker"], decision = "prompt")
prefix_rule(pattern = ["format"], decision = "prompt")
prefix_rule(pattern = ["diskpart"], decision = "prompt")
prefix_rule(pattern = ["setx"], decision = "prompt")
```

## Read-Only Validation

Validate without running protected commands:

- `config.toml` exists;
- `default.rules` exists;
- `config.toml` contains `approval_policy`, `sandbox_mode`, `approvals_reviewer`, `[auto_review]`, and `[windows] sandbox = "elevated"`;
- `default.rules` contains at least `netsh`, `reg`, `sc`, `schtasks`, `docker`, `wsl`, `diskpart`, and `format`;
- `.codex-global-state.json` targeted search shows `agent-mode-by-host-id` has `local` set to `custom`, when that state file is present and readable.

Do not test by actually changing proxy, registry, services, scheduled tasks, Docker, WSL, DNS, hosts, firewall, routes, or environment variables.

## Acceptance Report

Generate a clickable HTML report named for the task, often:

```text
CODEX_PERMISSION_POLICY_ACCEPTANCE_REPORT.html
```

Include:

- what was done;
- modified file paths;
- backup file paths;
- current permission principle;
- what is allowed by default;
- what requires approval;
- ordinary task test method;
- Windows approval test method;
- network/proxy approval test method;
- rollback method;
- next step: fully quit Codex Desktop, reopen it, and select `自定义 (config.toml)` in the permission menu if it is not already selected.

When possible, copy the report to the task's `outputs` folder for the final user-facing link.
