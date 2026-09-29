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
同时冻结 accepted_clock + accepted_tick_ns。
后续只允许同源 event_tick_ns 机械计算 T_VALID。
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
- 状态40：执行与审核时必须显示真实 TASK_ACCEPTED、同源当前节点时间和机械整体已用；T_VALID 未到最终有效边界前不得伪造。
- 状态100：完成时必须显示由同源 tick 机械产生的最终 T_VALID；如合法起点缺失，即使业务完成也只能显示 T_VALID=尚未产生。

因此每次核心状态输出都必须满足：

STATE_HEADER_PRESENT=YES
TIME_ANCHOR_PRESENT=YES
STATE_TIME_COUPLED=YES

任一缺失，该状态快照无效，不得作为正式状态交接或完成依据。

这不是新增第二状态机，而是把唯一目标 T*=min(T_VALID) 作为所有状态的共同锚定物。
