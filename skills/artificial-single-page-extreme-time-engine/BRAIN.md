# 《极限短时间执行大脑 第15版》

版本：第15版
升级来源：第14版
状态：CURRENT
唯一标准：T*=min(T_VALID)

## 1. 固定读取顺序

新 CEO 页先装“脑子”，再读任务，再读状态，再读执行体，最后读页面规则：

1. BRAIN.md —— 决策大脑：怎么判断
2. CURRENT_TASK_CONSTRAINTS.md / 当前任务 TASK_CONTRACT —— 要什么、什么不能变
3. CURRENT_TASK_FREEZE.md / 最新任务冻结版本 —— 现在做到哪
4. ENGINE.md —— 当前节点具体怎么执行
5. NEW_PAGE_TEMPLATE.md —— 当前页面怎么运行、冻结、换页

这与旧第3/4版模板的成熟顺序一致。
逻辑上是四层：方法脑 / 任务定义 / 冻结状态 / 页面运行；ENGINE 是“方法脑”的执行体。

## 2. 初次接到任务：INITIAL_TASK_INTAKE

只有新现实任务、没有现成 FROZEN TASK_CONTRACT 时执行一次。

用户原始任务
→ 写一句 FINAL_REALITY_GOAL（只写最终结果，不先写实现）
→ 写 POSITIVE_PROMPT（必须有、必须保留）
→ 写 NEGATIVE_PROMPT（绝不能有、出现即失败/漂移）
→ 明确 IN_SCOPE / OUT_OF_SCOPE / HARD_BOUNDARIES
→ 定义 USER_PATH（用户最简现实操作）
→ 定义 FINAL_VALID_STANDARD / DONE_WHEN
→ 定义 EVIDENCE_REQUIRED
→ 反向检查“有没有形式完成但真实失败的漏洞”
→ 冻结 CONTRACT_VERSION=1
→ 建立 FREEZE_VERSION=0
→ 进入 PAGE_TOPOLOGY_GATE

不得先实现，再倒推什么叫完成。

## 3. 后续接续：RESUME_TASK

已有任务时不重新定义目标：

读 CONTRACT_VERSION
→ 读最新 FREEZE_VERSION
→ 校验已冻结事实和证据
→ 只刷新当前 NEXT_CONTROL_DECISION
→ 进入 PAGE_TOPOLOGY_GATE

除非目标/FINAL_VALID/正反约束本身改变，否则 CONTRACT_VERSION 不变。

## 4. PAGE_TOPOLOGY_GATE

A. SIMPLE_SINGLE_PAGE：
简单任务，一个 CEO 页可以稳定闭环，CEO=Executor。

B. CEO_EXECUTOR：
多阶段、长流程、Reality、等待、并行、恢复或重执行任务。
一个活动 CEO 控制面 + 最少必要 Executor 页面。

## 5. Executor 固定生命周期

一个 Executor 页面只接受一个完整自然执行节点。

内部：
BASELINE
→ VIRTUAL_LOOP
→ STOP_GATE
→ NODE_FREEZE

结果无论：
PASS / FAIL / UNKNOWN / BLOCKED

都必须：
持久化证据
→ 回报 CEO
→ CEO 接受
→ 页面立即关闭

禁止完成后把同一个 Executor 页改派第二个节点。
并行任务完成一个关一个。

## 6. CEO 是唯一全局状态写者

Executor 只产出不可变 NODE_FREEZE。
CEO 接受后才修改全局任务状态。

每接受一个真正改变项目状态的冻结结果：

FREEZE_VERSION=N → N+1

包括 FAIL，因为失败也是新的现实事实。

并行 Executor 不直接争抢全局版本号；CEO 按接受顺序 Merge，避免 split-brain。

## 7. CEO_PAGE_ROTATION_GATE

目标优先级：
1. 防页面变重/卡顿/失效；
2. 保持控制状态清晰；
3. 避免不必要换页成本。

每次 CEO 接受一个 Freeze 后判断：

### Gate A：PAGE_HEALTH_RISK
出现任一项，立即换新 CEO：
- 页面/回复明显变慢或卡顿；
- 上下文已明显变重；
- 本页发生过断连/卡死/恢复；
- 下一阶段明显大、复杂、高思考；
- 当前页已承载大量 Merge/重规划信息。

### Gate B：REPLAN_REQUIRED
即使页面还轻，只要下一步需要真正重新判断/重新规划，也换新 CEO：
- CONTRACT 修订；
- Reality Delta 改变后续路线；
- 架构/执行器路线需要重新选择；
- 依赖图发生实质变化；
- 当前阶段结束，下一阶段语义明显不同。

### Gate C：SMALL_TIGHTLY_COUPLED_CONTINUE
若 A/B 都否，且下一节点小、紧耦合、复用当前上下文明显更省：
允许继续当前 CEO。

历史 LTMVH v0.7 R1 已证明：小而紧耦合的下一节点，继续当前页可明显快于立即 True New Chat。

### Gate D：HARD_CLEAN_CAP
同一 CEO 页面最多接受 3 个连续 FREEZE_VERSION。

SAME_CEO_FREEZE_COUNT=3
→ 当前页必须在第三个 Freeze 后结束
→ 生成 NEXT_PAGE_PROMPT
→ True New Chat
→ 新 CEO 计数归零

这是防卡顿兜底，不是“必须做满3个”。
任何一个节点很重或触发 A/B，都提前换。

## 8. CEO 唯一页规则

逻辑上始终只有一个 ACTIVE_CEO。

换页时：
旧 CEO 先 Freeze/Persist
→ 打开 True New Chat 接管
→ 接管成功
→ 旧 CEO 关闭

禁止两个 CEO 同时长期写状态。
禁止 Branch 代替 True New Chat。

## 9. Executor 并行门

DEPENDENCY / SHARED_WRITE / SCARCE_RESOURCE_CONFLICT ?

YES → SERIAL
NO → 只有并行能降低完整 T_VALID 才 PARALLEL

只开最少必要页面。
禁止预热空 Executor。
禁止第二套 persistent browser。
禁止多个 writer owner。

## 10. 节点大小

自然执行节点必须是“最小完整可独立验收闭环”：

一个主要目标
+ 高度相关依赖
+ 明确边界
+ DONE_WHEN
+ 可独立冻结结果

过细：
调度/保存/换页成本过大。

过粗：
上下文噪声/串行时间/失败半径过大。

原则：
能独立验收且拆开更快才拆；
强依赖、共享写、必须共同验证则合并。

## 11. Reality

先虚拟成熟到底，再 Reality once。

Reality 中禁止改 Freeze。

FAIL/Delta：
保留已通过事实
→ 冻结现实差异
→ 新虚拟节点重新成熟
→ 新 Freeze
→ 再整体 Reality

## 12. 三类版本

METHOD_VERSION：
方法系统变化才升级，自然整数。

CONTRACT_VERSION：
任务目标/FINAL_VALID/正反约束变化才升级，自然整数。

FREEZE_VERSION：
任务状态每次正式改变即升级，自然整数。

三者不得混用，不用小数。

一句话：

**先装大脑，再锁任务，再读冻结状态，再执行；Executor 一页一节点，完成即冻结关闭；CEO 可连续承接少量紧耦合状态，但防卡顿优先，最多3个 Freeze 后强制换新 CEO。**
