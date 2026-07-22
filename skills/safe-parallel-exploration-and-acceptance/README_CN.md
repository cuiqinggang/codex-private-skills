# 可回退并行探索与强制验收技能包 V1.0

本目录是唯一活动技能副本。它在现有 Codex Hooks 之上提供 Git、Worktree、Environment、路线验收、候选整合、三轮测试、技能分级和回滚方法；不会重新注册 Hooks。

本技能的完整正式名称就是：**可回退并行探索与强制验收技能包 V1.0**。

**日常中文简称：安全探索技能包。** 下次可直接说：`使用安全探索技能包，帮我对 <项目> 做 <任务>。`

精确内部调用名：`$safe-parallel-exploration-and-acceptance`。

- 主入口：`启动_完整安全探索工作台.cmd`
- 核心说明：`SKILL.md`
- 安全策略：`references/SAFETY_POLICY.md`
- 脚本默认行为：预览、无 push、无自动 merge、无危险清理。
- 真实运行加固：识别空 `.git`、审计 Windows 非法 Git 路径、保护精确字节资产、隔离只读注入测试，并执行候选/集成/安装后三层复测。
