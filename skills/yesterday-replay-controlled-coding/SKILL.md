---
name: yesterday-replay-controlled-coding
description: Use first when starting any task that should follow the user's global constraints for GPT planning, yesterday-replay reuse, logged-in GPT access through the Codex Chrome Extension, controlled Codex execution, Superpowers process discipline, Karpathy-style minimal coding, and verification before completion.
---

# Yesterday Replay Controlled Coding

This skill is mandatory for the user's controlled workflow. It defines the role boundary between GPT web and Codex.

## First-Step Rule

This is the first skill to load and follow for every workspace task. Before
using any other skill, plugin, browser path, shell workflow, planning route, or
implementation process, Codex must load this skill, classify the task, and apply
its routing rules. Other skills can be used only after this skill has set the
execution path.

One-sentence rule:

> 复杂任务必须交 GPT 网页超级大脑做昨日重现和规划，Codex 只做格式门、执行、验证、回报和闭环转发。

## Role Boundary Hard Rules

### GPT Web Super-Brain Owns Planning

GPT web is responsible for:

- yesterday replay
- mature-path search
- route judgment
- solution planning
- complex task decomposition
- code design judgment
- next-step planning after multi-round feedback

Before complex execution, GPT web must also perform skill/plugin replay search:

- ask Codex to list available skills, plugins, MCP tools, and local yesterday-replay examples
- decide which existing skill, plugin, or prior pattern should be reused
- decide whether anything should be installed or whether a new skill should be created
- allow custom implementation only after reusable paths are checked

Codex must not make this route judgment itself. Codex only lists available capabilities when asked, then executes and reports the GPT-selected route.

### Codex Owns Execution Control

Codex is responsible for:

- loading `AGENTS.md` and this skill as the first work step before any other skill or tool path
- deciding whether the task is simple, deterministic, and low risk
- generating a GPT planning request for complex, uncertain, coding, repair, installation, automation, or route-selection tasks
- saving GPT's raw answer
- validating the GPT plan with a format gate
- executing only compliant plans
- refusing non-compliant plans and reporting the missing fields
- producing execution reports
- feeding execution results back to GPT
- waiting for GPT's next plan and continuing the GPT -> Codex -> GPT loop until GPT judges the task complete

### Codex Must Not

Codex is forbidden from:

- replacing GPT for core yesterday-replay judgment
- inventing complex task routes on its own
- filling in missing GPT planning fields by itself
- executing when the plan is incomplete
- skipping the format gate
- bypassing the complex-task loop because Codex personally thinks the task is easy

## Task Routing

### A. Simple Tasks

Codex may directly execute a task only when it is low risk, single step, deterministic, and requires no route judgment.

Examples:

- read a file
- list a directory
- run an explicitly provided test command
- save a specified text block
- check whether a file exists

Simple tasks still require the narrowest meaningful verification.

### B. Complex Tasks

If a task involves any item below, Codex must enter the GPT planning loop:

- multi-step execution
- code changes
- system configuration
- installation or repair
- automation workflow design
- best-route judgment
- yesterday replay
- mature-practice search
- unclear or incomplete goals
- a failed execution that requires changing paths

Required complex-task flow:

1. User task
2. Codex loads `AGENTS.md` and this skill
3. Codex classifies the task as complex
4. Codex generates and sends a GPT planning request
5. GPT performs yesterday replay and planning
6. Codex saves GPT's raw answer
7. Codex validates the plan format
8. If compliant, Codex executes
9. If non-compliant, Codex refuses execution and reports missing fields
10. Codex generates an execution report
11. Codex sends the report back to GPT
12. GPT gives the next plan
13. Codex continues until GPT judges the task complete

### Preferred GPT Web Channel: Codex Chrome Extension

When the task needs GPT web planning or answers and a logged-in ChatGPT page is
already available in the user's Chrome profile, prefer the real Codex Chrome
Extension path over the legacy clipboard bridge.

Use this path when the `chrome` plugin and Codex Chrome Extension are installed
and enabled:

1. Load/use the `chrome` skill or Chrome plugin backend.
2. Run a lightweight connection check first, such as listing open Chrome tabs
   through the extension backend.
3. If the connection succeeds, call `browser.user.openTabs()`, select the
   existing ChatGPT tab by visible title and `chatgpt.com` URL, then claim that
   exact tab with `browser.user.claimTab(tab)`.
4. Send planning prompts through the claimed tab using DOM or Playwright
   controls. Prefer the actual ChatGPT input and send controls; do not move the
   real Windows mouse pointer.
5. Wait for the assistant response and copy/read the final answer from the
   page. Save `answer_raw.md`, validate the plan format, and continue the normal
   GPT -> Codex -> GPT loop.
6. Finalize Chrome tabs at the end of Chrome-backed work.

If the extension backend cannot communicate with Chrome, retry the lightweight
check once after 2 seconds. If it still fails, run only the Chrome plugin's
read-only diagnostics:

- `scripts/chrome-is-running.js --json`
- `scripts/installed-browsers.js --json`
- `scripts/check-extension-installed.js --json`
- `scripts/check-native-host-manifest.js --json`

Do not install or repair the native host manually. If the Codex Chrome Extension
is missing or disabled, tell the user to install/enable the Codex Chrome
Extension in Chrome and stop until they confirm.

Use the legacy clipboard bridge only when the Chrome Extension path is not
available, cannot be made ready without user action, or the user explicitly asks
for the old flow.

### Legacy GPT Web Channel Preflight

Before reporting that GPT web is unavailable, Codex must verify the local
ChatGPT clipboard bridge path. The failure mode to avoid is using only the
default `-WindowTitlePattern 'ChatGPT'` and missing a logged-in Chrome window
whose title is the current conversation.

Current desktop rule: use the already opened fresh GPT page when the user has
provided one; do not open another GPT page unless asked. Use the original simple
Windows bridge flow: copy prompt to clipboard, UI Automation focus the GPT
input, paste/send with virtual keystrokes, wait for a newly added assistant
answer copy button, and invoke that button with UI Automation. Do not move the
real mouse pointer. Coordinate mouse clicks or real pointer movement require
explicit `-AllowRealInput` for that run.

Use the `chatgpt-clipboard-bridge` skill. First enumerate visible Chrome/Edge
window titles when needed, then pass the matched conversation title into
`WindowTitlePattern`. On 2026-05-09 this desktop was verified with:

```powershell
-WindowTitlePattern '任务回显确认|ChatGPT'
```

In workspace `C:\Users\A\Desktop\1`, read
`docs/chatgpt-clipboard-bridge-current-flow.md` before re-testing this path.

Minimum readiness check before relying on the channel:

1. Run the bridge static encoding and discipline tests if the bridge behavior is in doubt.
2. Run the official bridge script with `-NoSend` to verify it activates the logged-in GPT window and finds the input box.
3. Run a short echo prompt with a unique `TASK_ID` and require GPT to copy back that same `TASK_ID`.
4. Treat the channel as ready only after `answer_raw.md` contains the matching `TASK_ID`.

When the user asks not to disturb their active GPT page, the preflight command
must not use `-OpenFreshWindow`. The readiness echo may run only after the
NoSend preflight proves the existing fresh GPT page and semantic input box are
available.

If a real task later hangs at GPT access, repeat this preflight and update only
the window title pattern before changing the planning workflow. Do not switch to
Playwright, a virtual browser, or a fresh GPT page unless the user asks.

## GPT Planning Request Requirements

For complex tasks, Codex must ask GPT web to include:

- task objective
- yesterday-replay findings or mature path
- risk level
- execution scope
- ordered steps
- validation method
- stop conditions
- completion criteria

Codex must not add, remove, translate, optimize, or reinterpret GPT's plan before execution. Structure extraction is allowed only when it preserves one-to-one meaning.

## Format Gate

Before executing a GPT plan, Codex must confirm the plan includes:

- objective
- scope
- steps
- validation
- stop conditions
- completion criteria

If any required field is missing, Codex must not execute. It must report the missing fields and ask GPT for a corrected plan.

## Risk Rules

- Level 0: only writes under `output/`, no deletes, no existing-code changes, no unknown commands. Execute automatically.
- Level 1: creates new files, writes logs, modifies temp/test output. Execute automatically and log.
- Level 2: modifies existing code, runs build/test, overwrites files. Execute automatically after backup, diff, and execution log.
- Level 3: deletes files, batch-modifies the project, runs unknown commands such as `curl | bash`, changes system config, operates accounts, secrets, payment, or network permissions. Stop and ask the user.

## Coding Constraints

For coding work, Codex must follow Superpowers process discipline and Karpathy-style minimal coding:

- define the problem before implementation
- make the smallest necessary change
- avoid unrelated refactors
- verify each meaningful step
- report the exact changes and verification evidence

## Replacement Rule

Replace any old interpretation like:

> Complex tasks enter planning. If the task involves multiple steps, path selection, design judgment, code changes, or tool installation, Codex first performs yesterday replay.

With:

> 复杂任务进入 GPT 规划闭环。如果涉及多步骤、路径选择、设计判断、代码修改、工具安装、系统修复或自动化流程设计，Codex 不得自行承担昨日重现和路线判断。Codex 必须把任务发布给 GPT 网页超级大脑，由 GPT 完成昨日重现、成熟路径搜索、路线判断和规划。Codex 只负责格式门验证、受控执行、最小验证、报告回传和多轮闭环。
