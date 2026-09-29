# v5.6.4 Reality 时间锚 R2 最小认证

ENGINE_VERSION=v5.6.4
FREEZE_ID=FPLC-v5.6.4-REALITY-TIME-DISPATCH-CONTRACT-R2
ENGINE_PATH=skills/first-principles-physical-limit-convergence-v5.6.4/

目标：只认证 v5.6.4 R2 的唯一新增合同——10/20/30/40/100 每个核心状态都必须与时间锚形成不可拆分的确定性状态快照。

必须验证：
1. 正常 Reality 命令定位行、状态机行、时间锚行齐全。
2. 缺任一行时 DISPATCH_READY=NO。
3. 状态10必须显示时间锚；无合法起点时明确未知/尚未产生。
4. 状态20必须保持同一 TASK_ACCEPTED，不得重置起点。
5. 状态30必须显示时间锚，GPT_DISPATCH_TIME 不得替代 TASK_ACCEPTED。
6. 状态40必须显示真实 TASK_ACCEPTED、同源当前节点时间和机械整体已用。
7. 状态100只有合法同源计时链存在时才允许数值 T_VALID；否则 T_VALID=尚未产生。
8. 20→30→40→100 全程不得重置 accepted_tick_ns。
9. accepted_clock / accepted_tick_ns 只冻结一次。
10. 同源 event_tick_ns 机械计算最终 T_VALID。
11. 不修改 TRANSITIONS、核心时间算法、display 结构、SHA256证据、DSE/业务 Freeze。
12. Reality 阶段禁止现场修改 Freeze 来取得 PASS。

输出：
STATE10_TIME_ANCHOR=
STATE20_TIME_ANCHOR=
STATE30_TIME_ANCHOR=
STATE40_TIME_ANCHOR=
STATE100_TIME_ANCHOR=
STATE_TIME_COUPLING=
TASK_ACCEPTED_CONTINUITY=
TIME_ORIGIN_FROZEN_ONCE=
T_VALID_MECHANICALLY_DERIVED=

失败分类：
GPT_HOST_DISPATCH
RECEIPT_PROTOCOL
TIME_ORIGIN
RUNTIME_CALCULATION
TEST_HARNESS
EXTERNAL

完成后必须 RETURN_TO_GPT=YES。
不得自行宣布 FINAL_VALID 或 DONE。
