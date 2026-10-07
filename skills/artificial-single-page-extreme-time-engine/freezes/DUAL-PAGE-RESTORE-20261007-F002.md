# 双页面控制完整恢复与四层状态重建｜CEO Freeze 002

CEO_FREEZE_TAG_JSON={"schema":"CEO_FREEZE_TAG_V1","freeze_id":"DUAL-PAGE-RESTORE-20261007-F002","page_id":"EXTREME-TIME-METHOD-RESTORE-20261007","task_id":"DUAL-PAGE-CONTROL-RESTORE-20261007","node_id":"RESTORE-FOUR-LAYER-INTAKE-FREEZE-LIFECYCLE","sequence":2,"state_code":100,"freeze_status":"PASS_FROZEN","final_valid":"YES","t_valid_ms":null,"t_star_ms":null,"source_repo":"cuiqinggang/codex-private-skills","source_ref":"77b48728fb40eb7ec664b6b0839e08c0b8eeb927","freeze_path":"skills/artificial-single-page-extreme-time-engine/freezes/DUAL-PAGE-RESTORE-20261007-F002.md","next_node":"NEXT-TASK-INTAKE"}

## FREEZE_VERSION

FREEZE_VERSION=2

## 当前方法版本

ENGINE_VERSION=20
BRAIN_VERSION=15
TASK_CONTRACT_SCHEMA_VERSION=2
CURRENT_TASK_FREEZE_SCHEMA_VERSION=1
NEW_PAGE_TEMPLATE_VERSION=11

## 恢复的成熟结构

固定读取顺序：

1. BRAIN.md
2. CURRENT_TASK_CONSTRAINTS.md / TASK_CONTRACT
3. CURRENT_TASK_FREEZE.md / 最新冻结
4. ENGINE.md
5. NEW_PAGE_TEMPLATE.md

逻辑四层：
- 方法脑；
- 任务定义；
- 冻结状态；
- 页面运行。

ENGINE 是方法脑的执行体。

## 初次接任务

用户原始任务
→ FINAL_REALITY_GOAL
→ POSITIVE_PROMPT
→ NEGATIVE_PROMPT
→ IN/OUT_SCOPE + HARD_BOUNDARIES
→ USER_PATH
→ FINAL_VALID / DONE_WHEN
→ EVIDENCE_REQUIRED
→ 反向漏洞检查
→ CONTRACT_VERSION=1
→ FREEZE_VERSION=0
→ PAGE_TOPOLOGY_GATE

## Executor 生命周期

一个 Executor 页面=一个完整自然执行节点。

PASS / FAIL / UNKNOWN / BLOCKED
→ NODE_FREEZE
→ CEO 接受
→ 全局 FREEZE_VERSION +1
→ Executor 页面立即关闭。

并行 Executor 只产出不可变 NODE_FREEZE_ID；
CEO 是唯一全局状态 writer。

## CEO 生命周期

ACTIVE_CEO_COUNT=1

每次接受 Freeze 后执行：

1. PAGE_HEALTH_RISK=YES → 立即换；
2. REPLAN_REQUIRED=YES → 立即换；
3. 否则小而紧耦合 → 可继续当前 CEO；
4. MAX_CONSECUTIVE_FREEZES_PER_CEO=3，第三个 Freeze 后强制换 True New Chat。

防卡顿优先。
3 是硬上限，不是目标数量。

## 历史依据

- 旧 New Page Template 第3/4版已明确读取顺序：BRAIN → TASK → Freeze/Evidence → ENGINE → TEMPLATE。
- LTMVH v0.4.5 Clean CEO Lifecycle 已 Reality 验证：最少必要 Executor、结果持久化后立即关闭、CEO checkpoint 后切 True New Chat、禁止 Branch。
- LTMVH v0.7 R1 已 Reality 验证：小而紧耦合的下一节点继续当前页，比立即换 True New Chat 更快；因此“每 Freeze 必换 CEO”不成立。
- Executor 与 CEO 必须使用不同生命周期规则。

## 下一状态

当前无活动现实任务。
新任务进入时执行 INITIAL_TASK_INTAKE。
