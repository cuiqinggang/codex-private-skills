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
