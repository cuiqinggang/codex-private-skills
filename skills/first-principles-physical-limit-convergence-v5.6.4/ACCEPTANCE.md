# v5.6.4 最小升级验收

FREEZE_ID=FPLC-v5.6.4-REALITY-TIME-DISPATCH-CONTRACT-R2

## 唯一 Delta

Reality / Codex 正式命令必须强制携带定位行、状态机行、时间锚行，并严格区分 GPT_DISPATCH_TIME 与执行器真实 TASK_ACCEPTED。

## 必须满足

1. LOCATOR_PRESENT=YES
2. STATE_HEADER_PRESENT=YES
3. TIME_ANCHOR_PRESENT=YES
4. 任一缺失时 DISPATCH_READY=NO
5. TASK_ACCEPTED 只能在执行器真实收件现场建立
6. accepted_clock / accepted_tick_ns 只冻结一次
7. 最终 T_VALID 只能由同源 tick 机械计算
8. 无合法起点时不得产生数值 T_VALID
9. 不因本升级修改状态机、SHA256证据逻辑、DSE/业务 Freeze

## 已有现实依据

v5.6.3 生产同构检测02：
DISPATCH_BEHAVIOR_TEST=PASS
TEST_RESULTS=4 PASS / 0 FAIL
LOCATOR_PRESENT=YES
STATE_HEADER_PRESENT=YES
TIME_ANCHOR_PRESENT=YES
TASK_ACCEPTED_CREATED_AT_RECEIPT=YES
TIME_ORIGIN_FROZEN_ONCE=YES
T_VALID_MECHANICALLY_DERIVED=YES
T_VALID_MS=401910.1415

该结果只证明修复方向可行，不替代 v5.6.4 自身 Reality 认证。


## 状态-时间耦合验收

10. 状态10输出必须同时存在状态行与时间锚行。
11. 状态20输出必须同时存在状态行与时间锚行，并保持原 TASK_ACCEPTED。
12. 状态30输出必须同时存在状态行与时间锚行，且 GPT_DISPATCH_TIME 不得替代 TASK_ACCEPTED。
13. 状态40输出必须同时存在状态行与时间锚行，并使用同源冻结起点计算整体已用。
14. 状态100输出必须同时存在状态行与时间锚行；只有合法同源起点存在时才允许数值 T_VALID。
15. 任一核心状态缺时间锚：STATE_TIME_COUPLED=NO，该状态快照无效。
