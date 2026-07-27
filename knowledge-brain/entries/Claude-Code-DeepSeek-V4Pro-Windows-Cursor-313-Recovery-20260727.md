---
stable_id: mem-skill-claude-code-deepseek-v4pro-windows-cursor-313
type: skill-asset
source: C:\Users\A\Documents\Codex\2026-07-27\a-claude-code-deep-seek-v
created_at: 2026-07-27T20:00:00+08:00
updated_at: 2026-07-27T20:00:00+08:00
status: confirmed
scope: workflow:claude-code-deepseek-v4pro-windows
authority: C:\Users\A\.codex\skills\claude-code-deepseek-v4pro-windows
---

# Claude Code → DeepSeek V4 Pro：Cursor 3.13.10 恢复

## 结论

- `Claude Code 工具外壳 DeepSeek V4 Pro 转接路线: PASS`
- `ACTUAL_OPEN_VERIFY_PASS`
- Cursor 顶部菜单中文化：PASS
- Claude Code 页签恢复：PASS
- 两轮中文实际任务：2/2 PASS
- Claude/Anthropic 官方模型：未启用
- Key 持久化：否，仅当前 Cursor 进程树

## 什么时候调用

出现以下需求时路由到 `claude-code-deepseek-v4pro-windows`：

- Cursor 中文编辑器找不到 Claude Code/New Agent；
- Cursor 升级后顶部菜单变回英文；
- Claude Code 能回答但页面看不出实际模型；
- 恢复 Claude Code → DeepSeek V4 Pro；
- 要求中文化、实际回答、模型证明和两轮截图验收；
- 明确禁止 Claude/Anthropic 官方模型。

## 权威配置

```text
ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic
ANTHROPIC_MODEL=deepseek-v4-pro[1m]
ANTHROPIC_DEFAULT_OPUS_MODEL=deepseek-v4-pro[1m]
ANTHROPIC_DEFAULT_SONNET_MODEL=deepseek-v4-pro[1m]
ANTHROPIC_DEFAULT_HAIKU_MODEL=deepseek-v4-flash
CLAUDE_CODE_SUBAGENT_MODEL=deepseek-v4-flash
```

`ANTHROPIC_*` 只是 Claude Code 工具外壳兼容变量名，不代表接入 Anthropic 官方服务。

## 关键经验

1. Cursor 3.13.10 更新覆盖工作台资源；旧菜单修复脚本不能盲用。
2. 顶部菜单修复必须具备版本门禁、七项唯一签名、写前备份、工作台 SHA-256 校验和更新和写后验证。
3. Windows PowerShell 5.1 下含中文的 `.ps1` 必须保存为 UTF-8 BOM。
4. Claude Code Cursor 扩展页头不显示自定义 endpoint 模型名；`Manual` 是权限模式，不是模型。
5. 模型证明必须组合：
   - 启动会话的非密钥路由记录；
   - `claude -p` 真实最小调用；
   - Cursor 内实际中文回答；
   - 第二轮 `Read` 工具读取证明。
6. UI 操作必须使用 Cursor 窗口句柄截图；粘贴后、发送前必须确认输入框真的有内容。
7. 用户授权不能覆盖执行安全策略；不能持久化 Key 时使用安全输入和进程级会话。

## 真实验收

- Cursor：`3.13.10`
- Claude Code CLI：`2.1.179`
- Claude Code 扩展：`2.1.220`
- 最小真实调用：退出码 `0`
- 返回：`DS_CLAUDE_CODE_OK`
- 第一轮标记：`DEEPSEEK_V4_PRO_中文回答_OK`
- 第二轮标记：`ROUND2_DEEPSEEK_ROUTE_FILE_READ_OK`

## 读取顺序

1. 技能 `SKILL.md`
2. `references/BOUNDARY-20260702.md`
3. `references/CURSOR-313-CLAUDE-DEEPSEEK-RECOVERY-20260727.md`
4. 检查清单
5. 失败复盘
6. 只在对应版本运行确定性脚本

## 权威位置

- 执行权威：`C:\Users\A\.codex\skills\claude-code-deepseek-v4pro-windows`
- 验收页：`assets\ACCEPTANCE-20260727.html`
- 项目报告：`C:\Users\A\Documents\Codex\2026-07-27\a-claude-code-deep-seek-v\outputs\claude-deepseek-recovery\恢复与可见验收报告.md`
- GitHub 发布分支：`https://github.com/cuiqinggang/codex-private-skills/tree/codex/claude-deepseek-cursor-313-20260727`

## ROI

- 决策：`EXECUTE`
- 原因：在现有技能上增量更新，不创建重复技能；可避免 Cursor 升级后重复排查。
- 预计投入：30–60 分钟。
- 预计单次节省：1–3 小时。
- 实际长期节省：尚无实测。
- 复核：累计 3 次真实复用后。
