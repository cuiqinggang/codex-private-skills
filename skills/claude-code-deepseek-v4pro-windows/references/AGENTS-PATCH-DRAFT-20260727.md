# AGENTS.md 补丁草案（不自动覆盖）

当任务涉及 Cursor 中文编辑器、Claude Code 页签恢复、DeepSeek V4 Pro、Cursor 顶部菜单英文、模型看不出来或 Claude Code 两轮截图验收时：

1. 先调用 `claude-code-deepseek-v4pro-windows`；
2. 读取 `references/CURSOR-313-CLAUDE-DEEPSEEK-RECOVERY-20260727.md` 和失败复盘；
3. 只允许 Claude Code 工具外壳转接 DeepSeek，不连接 Claude/Anthropic 官方模型；
4. 先真实最小调用，再启动 Cursor；
5. 模型证明必须由安全路由记录、真实调用和 UI 实际回答构成，禁止只靠模型自报；
6. Cursor 菜单资源修复必须有版本门禁、唯一签名门禁、备份、校验和与截图回验；
7. 至少两轮实际任务和句柄级截图通过后才能报告 `ACTUAL_OPEN_VERIFY_PASS`。
