# v5.6.5 Freeze

VERSION=v5.6.5
FREEZE_ID=FPLC-v5.6.5-TIME-MODEL-SIMPLIFICATION-R1
STATUS=VIRTUAL_FROZEN
VIRTUAL_MATURE=PASS
REALITY_CERTIFIED=NO
FINAL_VALID=NO
FROZEN_AT=2026-09-30T01:40:47+08:00

## 唯一 Delta

把 v5.6.4 的时间模型简化为两条独立但关联的效率线：

1. T_FLOW：本轮从实际切入点到当前关键节点/完成的流程耗时。
2. T_VALID / T*：被优化任务本身的有效时间与最短有效时间。

## 固定规则

- 从哪里真实开始，就从哪里计时；不强制从10开始。
- 本轮实际起点冻结一次，不重置。
- 实际经历的关键状态记录 STATE_TIME。
- 没有实际经历的历史状态不补造、不重跑。
- 状态转换、交接/收件、执行审核、最终完成属于关键节点。
- 真实带时区时间即可；具体高精度 API 不是状态推进前提。
- 起止可比较则机械计算 T_FLOW；不可比较则 T_FLOW=未知，但不伪造、不因单一 API 失败停止业务流程。
- T_VALID 只代表已经满足 VALID 条件的任务实际有效时间。
- T* 只从可比的有效 T_VALID 中取最小值。
- 局部步骤耗时不得冒充整体 T_VALID/T*。
- 不同 FLOW_START_STATE 的 T_FLOW 不得假装成相同完整区间直接比较。

## 继承不变

- 10→20→30→40→100 状态机
- TRANSITIONS / judge 业务逻辑
- 实体证据 + SHA256
- DSE / 业务 Freeze
- 共同工作区事实源
- Reality 返回 GPT 最终审核规则

## 虚拟验证

TEST_RESULTS=13 PASS / 0 FAIL

覆盖：
- 可从状态30直接开始；
- 不要求补状态10/20历史时间；
- 本轮起点不被后续节点重置；
- tick/clock 字段不再是推进门槛；
- 无显式事件时间时运行时自动记录现实时间；
- 状态机保持不变；
- 状态20原派发逻辑保持；
- 三行头保持；
- 非最终状态不误确认 T_VALID；
- 状态100可同时显示 T_FLOW 与已验证 T_VALID/T*；
- 时间倒退/不可比较时 T_FLOW fail-closed 为未知；
- 无时区时间拒绝进入可比较时间链。

禁止在 Reality 阶段改写本 Freeze 来取得 PASS。
