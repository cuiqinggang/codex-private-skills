# v5.6.4 Freeze

VERSION=v5.6.4
FREEZE_ID=FPLC-v5.6.4-REALITY-TIME-DISPATCH-CONTRACT-R1
STATUS=VIRTUAL_FROZEN
VIRTUAL_MATURE=PASS
REALITY_CERTIFIED=NO
FINAL_VALID=NO
FROZEN_AT=2026-09-29T21:30:27+08:00

唯一 Delta：
正式 Reality / Codex 命令必须在派发前同时具备定位行、状态机行、时间锚行；GPT_DISPATCH_TIME 与执行器真实 TASK_ACCEPTED 必须分离。

PRE_DISPATCH_REQUIRED:
LOCATOR_PRESENT=YES
STATE_HEADER_PRESENT=YES
TIME_ANCHOR_PRESENT=YES

任意缺失：
DISPATCH_READY=NO

继承 v5.6.3：
- 10→20→30→40→100 状态机
- accepted_clock + accepted_tick_ns 一次冻结
- 同源 event_tick_ns 机械计算 T_VALID
- bool 不得作为 tick
- 无合法起点时 T_VALID=尚未产生
- 实体证据文件 + SHA256
- 局部最小化修复原则
- 网络共同工作区来源规则

重复故障分层：
1. 三行缺失 → GPT_HOST_DISPATCH
2. TASK_ACCEPTED 非现场建立 → RECEIPT_PROTOCOL
3. tick 未正确冻结 → TIME_ORIGIN
4. tick 正确但 T_VALID 错误 → RUNTIME_CALCULATION

禁止在 Reality 阶段现场修改本 Freeze 来取得 PASS。
