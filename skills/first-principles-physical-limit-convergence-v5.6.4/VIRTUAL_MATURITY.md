# v5.6.4 虚拟成熟记录

VIRTUAL_MATURE=PASS
REALITY_CERTIFIED=NO
FINAL_VALID=NO
FREEZE_ID=FPLC-v5.6.4-REALITY-TIME-DISPATCH-CONTRACT-R2

## 核心锚定

唯一目标：T*=min(T_VALID)。

10 / 20 / 30 / 40 / 100 只是流程状态编码；每个状态的现实确定性锚点是时间。
因此每一个核心状态都必须形成不可拆分的状态快照：

STATE + TIME_ANCHOR

每个状态快照必须同时具有：
- 状态机行；
- 时间锚行；
- 同一任务的 TASK_ACCEPTED 连续性；
- 当前节点真实时间；
- 可机械推导时的整体已用；
- T_VALID 当前状态；
- T* 当前状态。

任一核心状态缺时间锚，该状态快照无效。

## 根因

v5.6.3 的 advance → render → _dispatch_command 正式出口已经能生成完整三行。
现实缺陷来自 GPT/宿主 Reality 文本可能绕过该合同；R1 已固化 Reality 三行派发合同，R2 进一步明确“每个核心状态都必须与时间锚耦合”。

## R2 最小升级

只固化：
- 10/20/30/40/100 每个核心状态必须显示时间锚；
- 状态20/30/40不得重置 TASK_ACCEPTED 或 accepted_tick_ns；
- GPT_DISPATCH_TIME 与 TASK_ACCEPTED 分离；
- 状态100只有合法同源计时链存在时才允许数值 T_VALID；
- 缺任一时间要素 fail-closed；
- 重复故障按 GPT_HOST_DISPATCH / RECEIPT_PROTOCOL / TIME_ORIGIN / RUNTIME_CALCULATION 分层。

不修改：
- 10→20→30→40→100 状态机；
- T_VALID 机械计算核心；
- display 三行结构；
- 实体证据 SHA256；
- DSE / 业务 Freeze；
- 其他已 PASS 部分。

## 虚拟验证

原缺陷命令：
LOCATOR_PRESENT=YES
STATE_HEADER_PRESENT=NO
TIME_ANCHOR_PRESENT=NO
→ DISPATCH_READY=NO

02 生产同构样本：
LOCATOR_PRESENT=YES
STATE_HEADER_PRESENT=YES
TIME_ANCHOR_PRESENT=YES
TASK_ACCEPTED_CREATED_AT_RECEIPT=YES
TIME_ORIGIN_FROZEN_ONCE=YES
T_VALID_MECHANICALLY_DERIVED=YES
→ PASS

五状态合同：
STATE10_TIME_ANCHOR=REQUIRED
STATE20_TIME_ANCHOR=REQUIRED
STATE30_TIME_ANCHOR=REQUIRED
STATE40_TIME_ANCHOR=REQUIRED
STATE100_TIME_ANCHOR=REQUIRED
STATE_TIME_COUPLING=REQUIRED

结论：
R2 方案边界单一、资料闭合、无架构扩张，VIRTUAL_MATURE=PASS，允许进入 v5.6.4 Reality。
