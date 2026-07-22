---
name: claude-code-deepseek-v4pro-windows
description: Use when installing, repairing, verifying, or yesterday-replaying Windows-native Claude Code CLI integration with DeepSeek Anthropic-compatible API, especially deepseek-v4-pro[1m], User-level environment variables, gated PowerShell evidence, or future Claude Code GUI exploration.
---

# 2026-07-02 安全边界

本技能只作为“Claude Code 工具外壳转接 DeepSeek”的历史证明与恢复记忆，
不得理解为部署 Claude 模型、Anthropic API、Claude Sonnet、Claude Opus、
Claude Haiku，或恢复“Claude-style CLI 能力”。

当前允许目标：

- 只允许研究或恢复 Claude Code 工具外壳的 DeepSeek 转接能力。
- 最终模型证据必须指向 `deepseek/deepseek-v4-pro`，或用户明确认可的矩阵模型：
  `deepseek/deepseek-v4-flash`、`z-ai/glm-5.2`、
  `qwen/qwen3-vl-235b-a22b-instruct`。
- `ANTHROPIC_*` 只能作为 Claude Code 外壳兼容变量名出现；这不是接入
  Anthropic、Claude 官方模型或 Claude API Key 的许可。
- 默认不要运行 `scripts/set-claude-deepseek-env.ps1` 或
  `scripts/verify-claude-deepseek.ps1`。除非先阅读
  `references/BOUNDARY-20260702.md`，并确认本次只是 DeepSeek-only 兼容层复现。
- 如果旧证据不能证明 DeepSeek-only 转接路线，必须输出：
  `CLAUDE_CODE_DEEPSEEK_ROUTE_NOT_PROVEN`，并停止部署。
- 最终验收只能写：
  `Claude Code 工具外壳 DeepSeek V4 Pro 转接路线: PASS / PARTIAL / FAIL / NOT_PROVEN`。

# Windows 原生 Claude Code 接入 DeepSeek V4 Pro

## 用途

用于在 Windows PowerShell 原生环境中安装、确认、修复或复现 Claude Code CLI，并按 DeepSeek 官方 Anthropic-compatible API 方式接入 `deepseek-v4-pro[1m]`。

本技能来自一次已验证的实战链路：

`Windows PowerShell -> Claude Code CLI -> DeepSeek Anthropic-compatible API -> deepseek-v4-pro[1m]`

它不是一次性报告，而是可持续更新的技能包。图形界面安装与验证还没有完成验证，未来补充时先读 `references/未来图形界面扩展.md`。

## 使用前边界

- 只在当前任务目录保存报告、日志、备份和测试项目。
- 不关闭、不重启、不中断其他 Codex 或 Claude 任务。
- 不修改 Hermes、Open WebUI、OpenClaw、Codex 桌面版配置。
- 不使用 WSL，除非用户明确改目标。
- 不打印完整 `DEEPSEEK_API_KEY` 或 `ANTHROPIC_AUTH_TOKEN`。
- 缺少 DeepSeek API Key 时必须停止，输出 `NEED_DEEPSEEK_API_KEY`。
- 安装或配置失败时不要随机试错，先记录错误原文，再判断下一关。

## 官方成熟路线

优先复现官方路线，细节见 `references/官方依据.md`：

1. Anthropic 官方 Windows PowerShell 安装：
   `irm https://claude.ai/install.ps1 | iex`
2. DeepSeek 官方 Claude Code 集成路线：
   `npm install -g @anthropic-ai/claude-code`
3. DeepSeek Anthropic-compatible endpoint：
   `https://api.deepseek.com/anthropic`

实测中 Anthropic PowerShell 安装脚本可能超时；如果 `claude --version` 仍不可用，再使用 npm 官方包路线。不要在已有 `claude` 可用时覆盖安装。

## Gate 流程

每一步都写入 `report.md`，并包含 purpose、execution location、exact command、success criteria、failure criteria、failure recovery、continue or stop。

### G01 建立任务目录

在当前项目下创建：

`output/<TASK_ID>/report.md`

成功：目录和报告存在，输出 `G01_PASS`。

### G02 检查当前环境

记录：

```powershell
claude --version
node --version
npm --version
git --version
```

注意：PowerShell 中 `npm.ps1 --version` 可能异常显示 usage；必要时用 `npm.cmd --version` 复核。

### G03 安装或确认 Claude Code

如果 `claude --version` 已可用，只记录版本，不重新安装。

如果不可用：

```powershell
irm https://claude.ai/install.ps1 | iex
```

若官方 PowerShell 安装超时或失败，再执行：

```powershell
npm install -g @anthropic-ai/claude-code
```

安装后必须重新验证：

```powershell
claude --version
```

### G04 检查 DeepSeek API Key

只做存在性检查：

```powershell
[Environment]::GetEnvironmentVariable('DEEPSEEK_API_KEY','User')
```

存在则同步到当前会话；不存在则停止并输出 `G04_NEED_DEEPSEEK_API_KEY`。

### G05 写入 Claude Code 到 DeepSeek 的 User 环境变量

从 User 级 `DEEPSEEK_API_KEY` 读取，不在报告中打印完整值。写入 User 级：

```text
ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic
ANTHROPIC_AUTH_TOKEN=<from DEEPSEEK_API_KEY>
ANTHROPIC_MODEL=deepseek-v4-pro[1m]
ANTHROPIC_DEFAULT_OPUS_MODEL=deepseek-v4-pro[1m]
ANTHROPIC_DEFAULT_SONNET_MODEL=deepseek-v4-pro[1m]
ANTHROPIC_DEFAULT_HAIKU_MODEL=deepseek-v4-flash
CLAUDE_CODE_SUBAGENT_MODEL=deepseek-v4-flash
CLAUDE_CODE_EFFORT_LEVEL=max
```

可使用 `scripts/set-claude-deepseek-env.ps1` 自动执行并记录非密钥值。

### G06 最小 API 验证

在临时测试目录执行：

```powershell
claude -p "只回答：DS_CLAUDE_CODE_OK"
```

成功标准：退出码为 0，输出包含 `DS_CLAUDE_CODE_OK`。

### G07 项目目录只读验证

创建最小测试目录和 `README.md`，执行：

```powershell
claude -p "请读取当前目录结构，只用一句中文说明你看到了什么，不要修改文件。"
```

执行前后记录文件列表和 SHA256，成功标准是快照完全一致。

### G08 最终报告

最终报告至少包含：

- Claude Code 是否安装、版本号。
- Node/npm/git 状态。
- DeepSeek 环境变量配置状态。
- 是否使用 `deepseek-v4-pro[1m]`。
- G06 最小验证输出。
- G07 只读验证输出和前后哈希一致证据。
- 失败项、错误原文、回滚建议。
- 最后一行：`FINAL_PASS_CLAUDE_CODE_DEEPSEEK_V4PRO_READY` 或明确失败码。

## 可复用脚本

- `scripts/set-claude-deepseek-env.ps1`：从 User 级 `DEEPSEEK_API_KEY` 写入 Claude Code 所需 User 环境变量。
- `scripts/verify-claude-deepseek.ps1`：执行 G02、G04、G05 读回、G06、G07 验证并写报告。

运行脚本前先读脚本头部参数说明。脚本只应写入用户传入的任务输出目录。

## 本次实测结论

本次实测摘要见 `references/本次实测复盘.md`。关键信息：

- `claude --version` 最终为 `2.1.143 (Claude Code)`。
- Anthropic PowerShell installer 300 秒超时。
- npm fallback 安装成功。
- DeepSeek User 环境变量写入成功。
- `claude -p "只回答：DS_CLAUDE_CODE_OK"` 成功返回目标字符串。
- 测试项目只读验证通过，前后 SHA256 一致。

## 更新规则

以后如果要补充 Claude Code 图形界面、模型名变化、DeepSeek endpoint 变化、Claude Code CLI 行为变化：

1. 先复制新增实测报告到 `references/`。
2. 更新 `SKILL.md` 中对应 gate。
3. 如需确定性操作，更新 `scripts/`。
4. 运行 `quick_validate.py`。
5. 在最终回复里说明新增版本、验证命令和 PASS/FAIL 证据。
