# 《人工单页面极限短时间引擎 第21版》

版本：第21版
升级来源：第20版
状态：CURRENT
唯一标准：T*=min(T_VALID)

## 1. 权威来源

REPO=cuiqinggang/codex-private-skills
PATH=skills/artificial-single-page-extreme-time-engine/

网络共同工作区为方法权威源。
本地目录只作为执行、缓存和证据落点。

## 2. 四层结构

整个长任务固定分四层：

1. 方法脑：BRAIN.md + 本 ENGINE.md
2. 任务定义：CURRENT_TASK_CONSTRAINTS.md / 当前 TASK_CONTRACT
3. 当前冻结状态：NEXT_PAGE_PROMPT 指向的《当前任务冻结状态 第N版》
4. 页面运行：NEW_PAGE_TEMPLATE.md

任务定义负责“不漂移”。
冻结状态负责“不断线”。
页面运行负责“保持上下文干净”。
本引擎只负责“当前自然执行节点内部怎么成熟”。

## 3. 初次任务与后续任务

新任务：
INITIAL_TASK_INTAKE
→ CONTRACT_VERSION=1
→ 生成《当前任务冻结状态 第1版》
→ FREEZE_VERSION=1
→ PAGE_TOPOLOGY_GATE

已有任务：
读取合同
→ 读取最新冻结
→ 不重复已冻结工作
→ PAGE_TOPOLOGY_GATE

## 4. PAGE_TOPOLOGY_GATE

### SIMPLE_SINGLE_PAGE
简单、低风险、一个页面能稳定闭环：
CEO=Executor。

### CEO_EXECUTOR
长流程、多阶段、Reality、等待、并行、恢复、重执行：
一个活动 CEO
+
最少必要 Executor 页面。

拓扑不是目的。
同等 VALID 下完整 T_VALID 更低者胜。

## 5. Executor：一页一完整自然执行节点

一个 Executor 页面只能接受一个被明确分配的自然执行节点。

节点定义：

一个主要目标
+ 高度相关依赖
+ 明确边界
+ DONE_WHEN
+ 可独立验收和 Freeze

节点内允许很多轮：
成熟 BASELINE
→ NET_GAIN
→ 当前最大净收益点
→ ≤3成熟候选
→ 虚拟替换
→ 刷新完整节点方案
→ 重算
→ 自动继续
→ STOP_GATE

禁止完成一个微优化就退出。

## 6. Executor 生命周期

节点最终无论：

PASS
FAIL
UNKNOWN
BLOCKED

都必须：

NODE_FREEZE
→ 持久化结果/证据/Reality Delta
→ 回报 CEO
→ CEO 接受结果
→ Executor 页面立即关闭

同一 Executor 页面不得被重新利用去执行第二个自然节点。

同时运行多个 Executor 时：
完成一个、接受一个、关闭一个。

## 7. 并行

先判断：

DEPENDENCY
SHARED_WRITE
SCARCE_RESOURCE_CONFLICT

任一为 YES：
SERIAL。

全部为 NO：
只有预计并行降低完整 T_VALID 才 PARALLEL。

禁止：
- 为多智能体而多智能体；
- 预热空 Executor；
- 无限开页面；
- 第二套 persistent browser；
- 多个全局 writer。

## 8. CEO 不执行重历史

CEO 只维护：
- TASK_CONTRACT_VERSION
- FREEZE_VERSION
- 已冻结事实
- 未完成节点
- 依赖
- Executor 分配
- Merge
- Reality Gate
- T*
- NEXT_CONTROL_DECISION
- NEXT_PAGE_PROMPT

搜索日志、代码日志、几十轮虚拟尝试属于 Executor/证据文件。

## 9. CEO 换页：防卡顿优先

每次 CEO 接受 Freeze 后执行 CEO_PAGE_ROTATION_GATE。

立即换页条件优先级最高：

### PAGE_HEALTH_RISK
页面明显变重、响应变慢、卡顿、发生断连/恢复、上下文膨胀，或下一阶段本身很重。

### REPLAN_REQUIRED
下一步需要真正重新规划：
- 合同改变；
- Reality Delta 改路线；
- 架构/执行器选择改变；
- 依赖图实质变化；
- 阶段语义明显切换。

如果两者都否，且下一节点小、紧耦合、继续当前页明显减少重理解成本：
允许继续当前 CEO。

但：

MAX_CONSECUTIVE_FREEZES_PER_CEO=3

同一 CEO 页最多接受 3 个 Freeze。
第三个 Freeze 后必须换 True New Chat。
这是防卡顿硬兜底，不要求做满3个。

## 10. CEO 唯一活动页

ACTIVE_CEO_COUNT=1

换 CEO：

旧 CEO Persist/Freeze
→ True New Chat 接管
→ 接管确认
→ 旧 CEO 立即关闭

禁止 Branch。
禁止两个 CEO 长时间并存写状态。

## 11. Freeze 与版本

### METHOD_VERSION
本方法结构改变才自然整数 +1。

### CONTRACT_VERSION
目标/FINAL_VALID/正反约束改变才自然整数 +1。

### FREEZE_VERSION
正式《当前任务冻结状态》从第1版开始；CEO 每接受一个真正改变任务状态的冻结结果，自然整数 +1。

并行 Executor 自己只生成不可变 NODE_FREEZE_ID；
CEO 是唯一全局版本写者，并生成新的《当前任务冻结状态 第N版》。

失败同样是状态变化，因此 FAIL Freeze 也进入新 FREEZE_VERSION。

## 12. Reality

Reality 只验证冻结方案。

Freeze
→ Reality once
→ PASS / FAIL / UNKNOWN

Reality 中禁止改候选。

FAIL/Delta：
已通过事实冻结
→ 真实差异进入新虚拟节点
→ 再完整成熟
→ 新 Freeze
→ 再整体验证

## 13. Persist First → Close Second

所有页面统一：

先 Freeze / Persist
再 Close

页面不是资产。
冻结状态才是资产。

## 14. 页面健康与节点大小

“语义边界”是决策点，不等于每次必须换页。

小、紧耦合节点可以继续同一 CEO；
大、重、需要重规划的节点立即换。

Executor 仍严格一页一节点，不适用 CEO 的3-Freeze复用规则。

## 15. 硬规则

禁止任务静默漂移。
禁止任务合同与冻结状态合并成一个文件。
禁止 Executor 一页多节点。
禁止 Executor 完成后遗留不关。
禁止 CEO 承载重执行历史。
禁止固定字数/轮数成为主换页条件。
禁止 Reality 逐点试错。
禁止页面关闭先于 Freeze。
禁止新 CEO 重放旧聊天。

一句话：

**初次任务先锁合同；执行时一页一 Executor 节点；CEO 是唯一状态控制面，可承接少量紧耦合 Freeze，但页面健康优先且最多3个 Freeze 后强制换页。**
