# 长期记忆超级虚拟人｜权威任务合同模板 v0.1

> 作用：长流程唯一 Source of Truth。聊天、子智能体、执行器、临时计划都不得静默改写它。

```yaml
TASK_ID: <唯一任务编号>
CONTRACT_VERSION: 1

FINAL_REALITY_GOAL: >
  <最终现实目标；只写结果，不写实现偏好>

IN_SCOPE:
  - <必须完成>

OUT_OF_SCOPE:
  - <明确不做>

HARD_BOUNDARIES:
  - 不破坏/删除 Windows 系统
  - 不修改 FlClash / Windows 网络代理
  - <本任务其他硬边界>

DONE_WHEN:
  - <机器可验证完成条件 1>
  - <机器可验证完成条件 2>

EVIDENCE_REQUIRED:
  - <文件/日志/截图/测试/Run ID/Artifact 等>

FLOW_START: <带时区时间>
CURRENT_STATE: <当前阶段>
CURRENT_ROUTE: <当前工具/执行器>
NEXT_ACTION: <下一步唯一现实动作>

CONTINUITY_POLICY:
  expected_silence_window: <本阶段合理静默窗口>
  hard_deadline: <超过后才允许判定真实停滞>
  next_stage_complexity: <small|medium|large>
  proactive_rotation: <YES|NO>
  transport_disconnected: <YES|NO>
  backend_activity_observed: <YES|NO>
  human_verification_required: <YES|NO>

FALLBACK_POLICY:
  primary_route: <首选成熟路径>
  alternate_valid_routes:
    - <较慢但可达到同一 DONE_WHEN 的成熟路径>
  failover_when: <首选路径不能在门限内进入 VALID 时的切换条件>

FAILED_ROUTES:
  - route: <路径>
    root_cause: <根因>
    retry_condition: <何时才允许再试>

OPEN_UNKNOWN:
  - <会改变决策的未知>

CHECKPOINT:
  last_updated: <带时区时间>
  resume_from: <恢复点>
```

## 运行规则

1. 长流程开始时先建立任务合同；
2. 只在现实目标真正改变时提升 `CONTRACT_VERSION`；
3. 子智能体只能执行被分配的 scope，不得自行扩 FINAL_REALITY_GOAL；
4. 任何新增动作先问：是否直接服务 `DONE_WHEN`；
5. 与合同冲突时，合同优先；
6. 如果合同本身被 Reality 证明定义错误，显式修订合同，而不是让执行路线偷偷漂移；
7. 每次 Checkpoint 保存合同版本；
8. `FINAL_VALID` 只能由 `DONE_WHEN + EVIDENCE_REQUIRED` 共同判定。

## 与 Checkpoint 的区别

- 任务合同：**应该做什么，什么叫完成**；
- Checkpoint：**现在做到哪，下一步从哪里恢复**。

两者互补，不能互相替代。

## v0.5.0 目标循环补充

启用默认目标循环时冻结 GOAL_LOOP_CONTROLLER.md 中的 contract 和已审核适配器：任务编号、最终目标、DONE_WHEN、授权/禁止边界、适配器SHA256、最大轮数、总时间预算。每轮保存真实验证证据、进度、失败根因、新策略、checkpoint和稳定动作ID。恢复先验收/核对，禁止重复副作用。

CLOSED才是任务级FINAL_VALID；BLOCKED/HUMAN_REQUIRED/STOPPED均不得计为完成。任务预算或验收定义变化必须显式形成新合同，不能静默扩大。
