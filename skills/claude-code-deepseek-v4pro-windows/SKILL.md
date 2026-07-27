---
name: claude-code-deepseek-v4pro-windows
description: Use when installing, repairing, recovering, or verifying Windows-native Claude Code CLI or the Claude Code Cursor extension with the DeepSeek Anthropic-compatible API, especially deepseek-v4-pro[1m], Cursor 中文编辑器, Cursor 3.13.10 classic-menu localization, a missing Claude Code/New Agent tab, DeepSeek model visibility proof, secure session launch, screenshot acceptance, or replaying a previously working Claude Code → DeepSeek V4 Pro route without enabling Claude/Anthropic official models.
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

它不是一次性报告，而是可持续更新的技能包。Cursor 3.13.10 图形界面恢复、中文菜单、模型可见证明和两轮真实回答已于 2026-07-27 完成验证；处理这类任务时必须先读 `references/CURSOR-313-CLAUDE-DEEPSEEK-RECOVERY-20260727.md`。

## 使用前边界

- 只在当前任务目录保存报告、日志、备份和测试项目。
- 不关闭、不重启、不中断其他 Codex 或 Claude 任务。
- 不修改 Hermes、Open WebUI、OpenClaw、Codex 桌面版配置。
- 不使用 WSL，除非用户明确改目标。
- 不打印完整 `DEEPSEEK_API_KEY` 或 `ANTHROPIC_AUTH_TOKEN`。
- 缺少 DeepSeek API Key 时必须停止，输出 `NEED_DEEPSEEK_API_KEY`。
- 默认使用 `scripts/launch-cursor-deepseek-session.ps1` 的进程级会话变量；不得在日志、证明文件、截图或 Git 仓库中保存 API Key。
- 只有同时满足“执行环境安全策略允许持久化”和“用户针对本次操作明确批准”时，才允许考虑 User 级凭据路线。任一条件不满足时必须使用会话级路线。
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

### G09 Cursor 图形界面恢复与两轮可见验收

仅在用户要求 Cursor/Claude Code 图形界面时执行。完整步骤、故障分支和证据结构见：

- `references/CURSOR-313-CLAUDE-DEEPSEEK-RECOVERY-20260727.md`
- `references/CHECKLIST-CURSOR-CLAUDE-DEEPSEEK-20260727.md`
- `references/FAILURE-REVIEW-20260727-CURSOR-CLAUDE-DEEPSEEK.md`

强制规则：

1. 先验证 Claude CLI 的 DeepSeek-only 最小真实调用，再启动 Cursor。
2. Cursor 3.13.10 顶部经典菜单失去中文时，只运行带版本门禁、唯一签名门禁、备份和 `product.json` 校验和更新的 `scripts/repair-cursor-313-classic-menubar-cn.ps1`。
3. 截图必须按 Cursor 主窗口句柄截取，不能只截整个桌面后主观判断。
4. Claude Code 扩展页头不显示自定义兼容端点模型名时，不得让模型“自报”作为唯一证据；必须展示本次启动链路生成的安全路由证明。
5. 至少完成两轮真实任务：
   - 第一轮：中文回答和固定验收标记；
   - 第二轮：Claude Code 实际调用 `Read` 读取路由证明，并返回端点、模型、真实烟雾测试结果和官方模型禁用状态。
6. 最终同时输出：
   - `Claude Code 工具外壳 DeepSeek V4 Pro 转接路线: PASS / PARTIAL / FAIL / NOT_PROVEN`
   - `ACTUAL_OPEN_VERIFY_PASS / PARTIAL_PASS_WITH_SCREENSHOT_EVIDENCE / FAIL_NEEDS_FURTHER_FIX`

## 可复用脚本

- `scripts/set-claude-deepseek-env.ps1`：从 User 级 `DEEPSEEK_API_KEY` 写入 Claude Code 所需 User 环境变量。
- `scripts/verify-claude-deepseek.ps1`：执行 G02、G04、G05 读回、G06、G07 验证并写报告。
- `scripts/launch-cursor-deepseek-session.ps1`：安全读取 Key，只建立本次 Cursor 进程树的 DeepSeek-only 环境，真实调用通过后生成并打开不含密钥的模型证明。
- `scripts/repair-cursor-313-classic-menubar-cn.ps1`：仅支持 Cursor 3.13.10；备份工作台资源，执行七项唯一签名替换，更新校验和并验证中文菜单。

运行脚本前先读脚本头部参数说明。脚本只应写入用户传入的任务输出目录。

## 本次实测结论

本次实测摘要见 `references/本次实测复盘.md`。关键信息：

- `claude --version` 最终为 `2.1.143 (Claude Code)`。
- Anthropic PowerShell installer 300 秒超时。
- npm fallback 安装成功。
- DeepSeek User 环境变量写入成功。
- `claude -p "只回答：DS_CLAUDE_CODE_OK"` 成功返回目标字符串。
- 测试项目只读验证通过，前后 SHA256 一致。
- 2026-07-27 Cursor 3.13.10 图形恢复、中文菜单、动态模型证明和两轮实际回答均通过，详见专项参考和 `assets/ACCEPTANCE-20260727.html`。

## 更新规则

以后如果要补充 Claude Code 图形界面、模型名变化、DeepSeek endpoint 变化、Claude Code CLI 行为变化：

1. 先复制新增实测报告到 `references/`。
2. 更新 `SKILL.md` 中对应 gate。
3. 如需确定性操作，更新 `scripts/`。
4. 运行 `quick_validate.py`。
5. 在最终回复里说明新增版本、验证命令和 PASS/FAIL 证据。
