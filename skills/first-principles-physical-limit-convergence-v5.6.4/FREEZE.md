# v5.6.4 Freeze

VERSION=v5.6.4
FREEZE_ID=FPLC-v5.6.4-REALITY-TIME-DISPATCH-CONTRACT-R3
STATUS=VIRTUAL_FROZEN
VIRTUAL_MATURE=PASS
REALITY_CERTIFIED=NO
FINAL_VALID=NO
FROZEN_AT=2026-09-29T22:33:53+08:00

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


## R2 最小确定性补充：状态与时间不可拆分

10 / 20 / 30 / 40 / 100 每个核心状态一旦显示或确认，必须同时显示时间锚。

每个状态快照必须同时满足：
STATE_HEADER_PRESENT=YES
TIME_ANCHOR_PRESENT=YES
STATE_TIME_COUPLED=YES

状态20/30/40不得重置 TASK_ACCEPTED 或 accepted_tick_ns。
状态30的 GPT_DISPATCH_TIME 不得替代 TASK_ACCEPTED。
状态100只有在合法冻结起点与同源 event tick 存在时才允许数值 T_VALID；否则保持 T_VALID=尚未产生。

本 R2 只补充状态-时间绑定合同；不修改 TRANSITIONS、不修改 runtime 时间算法、不修改 display 结构、不修改 SHA256 证据、不修改其他已 PASS 部分。


## R3 最小修正：时间锚不绑定具体 API

每个核心状态必须记录真实 STATE_TIME。

同源单调高精度 tick：
- 可用时优先；
- 用于更精确的区间/T_VALID 计算；
- 不是状态推进的硬前提。

若单调 tick API 不可用，但当前环境仍能取得可靠、带时区、可比较的真实时间：
- 继续状态推进；
- 记录该节点 STATE_TIME；
- 在同一可比较区间内可计算时再计算 elapsed/T_VALID；
- 不得因单一 API 失败而 STOP。

若区间无法可靠比较：
- 状态本身仍可有效；
- elapsed=未知；
- T_VALID=尚未产生。

跨宿主不得拼接不可比较的 tick。
本 R3 不修改状态机、Runtime业务逻辑、display三行结构、SHA256证据及其他已PASS部分。
