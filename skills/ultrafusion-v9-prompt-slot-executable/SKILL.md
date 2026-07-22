---
name: ultrafusion-v9-prompt-slot-executable
description: 使用 UltraFusion 9.0 提示词外置插槽式 Manual-M1 流程处理值得付出多轮成本的复杂问题；严格封存 A_Initial，按 A/B/C/D 调用只读核心资产，锁定 D_Final 后再做价值比较。用于“UltraFusion 9.0”“提示词外置插槽”“Manual-M1”“A_Initial vs D_Final”“只读部署版”等请求。
---

# UltraFusion 9.0｜提示词外置插槽式可执行技能包

当前版本：`UF-9.0.0-beta.1`；载体：`Manual-M1`；内核：`CORE-V15.1 external`。

## 开工前

1. 运行 `python 09_AUTOMATION/scripts/run_static_acceptance.py`。
2. 读取 `00_README/QUICK_START.md`、`05_MANUAL_M1/MANUAL_M1_SOP.md`。
3. 发现历史失败时读取 `references/FAILURE_REVIEW_ENTRY.md`。
4. 只从注册表装载核心资产；不得编辑 `02_CORE_ASSETS/readonly-copies`。

## 固定流程

`A_Initial 生成并封存 → A → B → C_Fusion → D_Final 锁定 → 解封比较副本 → 价值比较`。

部署模式与提示词探索模式严格分离。没有用户明确授权，不得修改 V15.1、A/B/C/D 提示词、A/B/C/D 命令包或 A_Initial 原模板。

## 运行边界

- 简单、低风险、低价值任务直接回答，不启动本技能。
- 没有真实外部模型返回时，不得声称多模型完整运行。
- 流程模拟只能标记 `FLOW_SIMULATION_ONLY`，不能宣称质量提升已证明。
- 真实价值结论必须同时报告质量增益、模型调用、人工操作、时间与费用。

## 失败入口与证据

- 失败复盘：`references/FAILURE_REVIEW_ENTRY.md`
- 最近使用：`RECENT_USE_LOG.md`
- 验收页面：`acceptance/index.html`
- 三轮证据：`08_VALIDATION/evidence/`

