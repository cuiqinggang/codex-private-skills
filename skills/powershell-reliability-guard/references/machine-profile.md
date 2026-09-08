# Recorded machine profile

## Confirmed from user context

- Operating system: Windows 10 Pro 22H2.
- Primary workflow: Codex and Cursor on Windows; PowerShell command packages are preferred over repeated manual steps.
- Codex CLI observed: 0.144.5.
- Node observed: 24.14.0; npm 11.9.0; Git 2.53.0.
- C: is the primary runtime drive; K: is backup; H: is historical. Do not scan or write H:/K: unless the current task explicitly authorizes it.
- Commands must minimize prompts and manual intervention, but must not hide failures or silently fall back.

## Conservative PowerShell target

- Default target: Windows PowerShell 5.1 (`powershell.exe`) because it is built into Windows 10.
- PowerShell 7 (`pwsh.exe`) availability and exact version: **unknown until probed in the active local session**.
- Installed PSScriptAnalyzer and Pester versions: **unknown until probed**.
- Execution policy, process architecture, elevation, active code page, module paths, and working directory: **session-dependent; probe rather than assume**.

## Known local failure constraints

- Windows PowerShell 5.1 can corrupt UTF-8-without-BOM configuration text when default text cmdlets decode it through the active ANSI code page.
- Native programs may write warnings to stderr while returning exit code 0. Judge native success from exit code plus expected postcondition.
- Codex helper validation homes placed under `%TEMP%` may be rejected; use the approved task workspace when that workflow is involved.
- Configuration changes require byte-for-byte backup, candidate validation, readback, and atomic replacement.

Refresh this file only from a real machine probe or direct user evidence. Record dates and exact commands for changed facts.

## 2026-09-08 用户回传更新（优先于上方旧版本记录）

Codex 0.153.4，PowerShell 7.6.5基线通过；5.1.19041.6456显式调用通过，默认Codex Shell仍为7.6.5。工作目录C:\Users\A\Documents\Codex。兼容测试7项通过，稳定性3/3；证据及范围见ps51-codex-acceptance-20260908.md。此为用户回传，非编写端Windows实测。
