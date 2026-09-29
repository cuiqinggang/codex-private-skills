---
name: first-principles-physical-limit-convergence
version: "5.6.4"
description: 整体闭环极限短时间引擎；固化 Reality 派发时间合同。
---

# 整体闭环极限短时间引擎 v5.6.4

唯一目标：T*=min(T_VALID)。
完整边界：TASK_ACCEPTED → FINAL_VALID。

v5.6.4 仅做一个最小升级：
把 v5.6.3 已存在的三行时间显示与真实 TASK_ACCEPTED 规则，提升为所有正式 Reality / Codex 命令的版本级硬合同。

## Reality 派发硬合同

正式 Reality 命令派发前必须同时存在：

【页面名｜任务名｜序号｜虚/实】
【状态机｜v5.6.4｜状态码｜状态名称】
【时间锚｜TASK_ACCEPTED=...｜当前节点时间=...｜整体已用=...｜T_VALID=...｜T*=...】

必须：
LOCATOR_PRESENT=YES
STATE_HEADER_PRESENT=YES
TIME_ANCHOR_PRESENT=YES

否则：
DISPATCH_READY=NO

## 时间语义

GPT_DISPATCH_TIME 不得冒充执行器 TASK_ACCEPTED。
TASK_ACCEPTED 只能在执行器真实收件时现场建立。
同时冻结 优先记录可靠时间源；可用时再冻结 accepted_clock + accepted_tick_ns 作为精度增强。
同一测量区间若有同源单调 tick，优先机械计算 T_VALID；若该 API 不可用，可使用当前环境可靠、带时区、可比较的节点时间继续推进，并如实标注精度/来源。
无合法起点时必须保持整体已用未知、T_VALID尚未产生。
局部 benchmark、墙钟字符串差值、人工 elapsed 不得冒充整体 T_VALID。

## 继承

状态机 10→20→30→40→100、时间机械计算、实体证据 SHA256、局部最小化修复与共同工作区来源规则均继承 v5.6.3，不作架构扩张。

重复时间故障必须先分层：
- 三行缺失：GPT_HOST_DISPATCH
- TASK_ACCEPTED 非现场建立：RECEIPT_PROTOCOL
- tick 未正确冻结：TIME_ORIGIN
- tick 正确但 T_VALID 错误：RUNTIME_CALCULATION

只修被现实证据命中的层。


## 每状态时间锚硬规则

状态机不是脱离唯一目标独立显示。每一个核心状态在被确认或转换后，都必须同时显示时间锚；状态行与时间锚行构成一个不可拆分的状态快照。

固定要求：

- 状态10：显示 TASK_ACCEPTED、当前节点时间、整体已用、T_VALID、T*；如 TASK_ACCEPTED 尚未合法建立，必须明确显示未知/尚未产生。
- 状态20：冻结方案时继续显示同一 TASK_ACCEPTED 与同源时间状态，不得重置起点。
- 状态30：虚实交接时必须显示时间锚；GPT_DISPATCH_TIME 只能作为当前节点时间/派发事实，不能替换 TASK_ACCEPTED。
- 状态40：执行与审核时必须显示真实节点时间；能可靠计算区间则显示整体已用，不能可靠计算则显示未知，但不得因此阻塞状态推进。
- 状态100：完成时必须显示真实节点时间；若起止时间源可可靠比较则产生 T_VALID，否则如实显示 T_VALID=尚未产生。

因此每次核心状态输出都必须满足：

STATE_HEADER_PRESENT=YES
TIME_ANCHOR_PRESENT=YES
STATE_TIME_COUPLED=YES

任一缺失，该状态快照无效，不得作为正式状态交接或完成依据。

这不是新增第二状态机，而是把唯一目标 T*=min(T_VALID) 作为所有状态的共同锚定物。


## R3 时间源灵活性

每个核心状态必须有真实 STATE_TIME，但不绑定某一种计时 API。

时间源优先级：
1. 同源单调高精度时钟：可用时优先，用于精确区间计算。
2. 当前环境可靠、带时区、可比较的系统时间：单调 tick 不可用时可继续作为节点时间与可比较区间来源。
3. 时间本身不可可靠观察：该时间字段标记未知；不得伪造。

单一 API（例如 Stopwatch.GetTimestamp）不可用，不得自动导致业务/Reality 停止。只有“时间本身不可可靠取得”或“所需区间不可可靠比较”时，相关耗时/T_VALID 才标记未知。

跨宿主不得硬拼不可比较的 tick；各宿主只记录自己真实经历的节点时间。
