# 双大型任务并行压力测试 — 首个确认方法故障

任务ID：METHOD-SYSTEM-LARGE-VIRTUAL-MATURITY-20261008
合同版本：3
尝试：DUAL_TASK_ATTEMPT_0
TASK_ACCEPTED：2026-10-08T00:45:00+08:00
方法起点：ENGINE 22 / BRAIN 18 / TEMPLATE 17
METHOD_REF=e64f7593a732a99c82c8d4e36b30e25f89d00aa7

## 双母任务

TASK_A_ID=DUAL-STRESS-A-LTMVH-PAGE-CONTROL-20261008
TASK_B_ID=DUAL-STRESS-B-H3P1-VIDEO-CONVERGENCE-20261008

两者均判定：
PAGE_TOPOLOGY=CEO_EXECUTOR

因此在真实双任务并发控制流中，A/B 必须同时进入各自控制面。

## 首个分叉点

BRAIN 18 同时存在：
- “一个活动 CEO 控制面 + 最少必要 Executor 页面”；
- “逻辑上始终只有一个 ACTIVE_CEO”；
- “CEO 是唯一全局状态写者”；
- “禁止多个 writer owner”。

但没有定义这些字段的作用域是：
- SYSTEM_GLOBAL（整套系统全局），还是
- PER_TASK_ID（每个现实任务）。

也没有定义多个独立 TASK 同时竞争共享 GitHub main writer、persistent browser、Windows 执行通道等共享可变/稀缺资源时的系统级仲裁对象。

## 生产同构控制流的两个合法解释

### 路径 1：SYSTEM_GLOBAL

A 获得唯一 ACTIVE_CEO 后，B 不能拥有第二个 ACTIVE_CEO。

结果：
- B 必须等待 A 控制面释放；
- 双大型任务控制面被强制串行；
- 无法满足本合同的并发压力条件；
- 与“两个独立 TASK 各自可以拥有 ACTIVE_CEO”的目标冲突。

### 路径 2：PER_TASK_ID

A_CEO 与 B_CEO 同时存在。

结果：
- 可保持两任务控制面并发；
- 但 BRAIN 18 没有明确说明这是合法语义；
- “禁止多个 writer owner”在系统级共享资源上失去确定解释；
- 当 A/B 同时需要向同一 GitHub main 持久化 Freeze/证据，或竞争同一 persistent browser 时，没有确定的跨任务 lease/arbitration 规则。

## 判定

两个解释都可由当前文字推出，却导致不同控制流与资源归属。

这已经满足本轮 Fail Fast 定义：
- 两个合法执行路径产生不同结果；
- 可能导致双 writer 或强制全局串行；
- 共享资源无确定仲裁；
- 无法继续进行无歧义的生产同构 replay。

因此：

CONFIRMED_METHOD_FAULT=YES
FAULT_CLASS=CROSS_TASK_SCOPE_AND_RESOURCE_ARBITRATION_AMBIGUITY
FAIL_FAST=TRIGGERED
CONTINUE_COLLECTING_LATER_FAULTS=NO

## 根因

责任层为《极限短时间执行大脑》第18版。

原因：
- 故障属于具体判断、跨任务调度、共享资源仲裁；
- ENGINE 22 的“一个活动 CEO”位于“一个现实任务”的页面拓扑语境，可保持不变；
- TEMPLATE 17 是单任务页面运行模板，当前问题可由 BRAIN 对未限定字段的作用域做统一定义，无需先升级页面模板。

## 最小修复要求

只升级 BRAIN 18 → 19，至少冻结：

1. ACTIVE_CEO 唯一性作用域 = PER_TASK_ID。
2. TASK global-state writer 唯一性作用域 = PER_TASK_ID。
3. 所有未显式标记 SYSTEM_GLOBAL 的 FREEZE_VERSION / SAME_CEO_FREEZE_COUNT / STATE_REF / page lifecycle 字段均属于 TASK_ID namespace。
4. 跨任务共享资源使用独立 SYSTEM_RESOURCE_LEASE，不由任一任务 CEO 擅自覆盖。
5. 资源按 RESOURCE_ID 原子仲裁；同一可变/稀缺资源同一时刻只允许合法 owner。
6. 只串行冲突节点，不串行整个任务。
7. persistent browser 不允许因第二 TASK 再启动第二套；可安全 attach/share 时复用，否则 lease 等待。
8. GitHub main / 其他共享 writer 必须在写操作粒度获取 writer lease。
9. 页面关闭、回滚、FINAL_VALID 回收必须限定 TASK_ID + resource ownership，不得误伤另一任务。
10. 如果所需共享资源没有可证明的仲裁器，Fail Fast，不得假设并发安全。

修复后必须从 TASK_A / TASK_B 两个 TASK_ACCEPTED 全部重跑。
