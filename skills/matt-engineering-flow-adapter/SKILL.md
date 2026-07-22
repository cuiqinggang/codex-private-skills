---
name: matt-engineering-flow-adapter
description: 在现有 ECC 或 long-coding-flow 长流程内部，按需增强需求澄清、领域术语、正式规格、纵向 tickets、核心逻辑 TDD、未知 Bug 诊断、双轴代码审查和会话接续。不得接管 Git、Worktree、Hooks、Checkpoint、项目账本、最终 Gate、merge、push 或 UltraFusion。
---

# Matt Engineering Flow Adapter

这是长流程编程系统内部的轻量工程执行增强层，不是第二套项目生命周期。

## 启动前

1. 先遵守用户命令、稳定资产保护、Worktree/Hooks、ECC 或 long-coding-flow 和项目记忆规则。
2. 从仓库、规格和项目账本读取已知答案，不重复询问。
3. 只加载当前需要的 workflow，默认最多三个。
4. 写入前运行 gates/PRE_WRITE_GATE.md。

## 路由

- 需求模糊：workflows/01_requirements_grill.md，必要时加 02_domain_context.md。
- 需要正式规格：workflows/03_to_spec.md。
- 需要拆分纵向闭环：workflows/04_vertical_tickets.md。
- 核心逻辑适合测试先行：workflows/05_tdd_execution.md。
- Bug 原因未知：workflows/06_bug_diagnosis.md；确定复现后可加 05。
- 需要独立审查：workflows/07_dual_axis_review.md。
- 需要新会话接续：workflows/08_handoff.md。

## 禁止触发

简单文字、纯格式、只读检查、复制、哈希、备份、完整不可变命令包、低风险快速任务和 UltraFusion 核心提示词处理均不得自动触发。

## 权限边界

本技能不创建 Issue、不自动提交、不 merge、不 push、不注册 Hook、不管理 Worktree、不维护 Checkpoint、不替代项目记忆账本、不宣告最终 PASS。handoff 只是会话桥梁。

## 验收

规格用 SPEC_GATE，TDD 用 TEST_GATE，审查用 REVIEW_GATE。执行声明必须交回上层 Verification Plane 与 Final Acceptance。
