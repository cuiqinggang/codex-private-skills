# 《极限短时间执行大脑 第18版》

版本：第18版
升级来源：第17版
状态：CURRENT
唯一标准：T*=min(T_VALID)

## 1. 唯一方法入口与两种读取顺序

BRAIN.md 是新 CEO 的唯一方法入口。

### 初次待接任务页

任务尚未产生，因此不存在“当前任务目标与正反约束 第N版”。

读取顺序：

1. BRAIN.md —— 决策大脑
2. FREEZE_PATH 指向的当前方法/上一任务最终冻结状态
3. NEW_PAGE_TEMPLATE.md —— 页面运行

接到用户现实任务后，再由 BRAIN 生成该任务自己的目标/正反约束与冻结状态。

### 同一任务接续页

任务已经存在时，读取顺序：

1. BRAIN.md —— 决策大脑
2. TASK_CONSTRAINTS_PATH 指向的《当前任务目标与正反约束 第N版》
3. FREEZE_PATH 指向的《当前任务冻结状态 第N版》
4. NEW_PAGE_TEMPLATE.md —— 页面运行

ENGINE.md 属于 BRAIN 的内部执行体，由 BRAIN 按当前节点需要调用。

原则：方法规则只在 BRAIN 定义；运行时状态只存在具体任务版本文件；NEXT_PAGE_PROMPT 只传路径和当前版本，不复制规则正文。

## 2. 初次接到任务：生成任务目标与正反约束

只有真正收到新的现实任务、且该任务尚无目标/正反约束文件时执行一次。

固定顺序：

用户原始任务
→ 保留原始意图的最小忠实摘要
→ 提炼“最终现实目标”，只写最后要得到什么，不先写实现
→ 生成“正向约束”：必须具备、必须保留、不能为快而牺牲
→ 生成“反向约束”：绝不能出现、出现即失败/漂移
→ 明确必须做 / 明确不做 / 硬边界
→ 定义用户最简现实操作路径
→ 把目标改写成明确可验收的 FINAL_VALID / DONE_WHEN
→ 定义最少必要证据
→ 从反面检查“有没有形式完成但真实失败”
→ 生成《当前任务目标与正反约束 第1版》
→ 生成《当前任务冻结状态 第1版》
→ 再进入 PAGE_TOPOLOGY_GATE

运行时任务文件命名：

```text
<TASK_PATH>/CURRENT_TASK_CONSTRAINTS_V1.md
<TASK_PATH>/freezes/CURRENT_TASK_FREEZE_V1.md
```

以后只有当目标、正向约束、反向约束、FINAL_VALID、范围或硬边界真正改变时：

```text
《当前任务目标与正反约束 第1版》
→ 第2版
→ 第3版
...
```

普通执行进展不得升级这个版本。

## 3. 后续接续：读取具体任务版本

已有任务时不得重新生成目标。

固定：

读取 TASK_CONSTRAINTS_PATH 指向的《当前任务目标与正反约束 第N版》
→ 读取 FREEZE_PATH 指向的《当前任务冻结状态 第N版》
→ 校验已冻结事实和证据
→ 只刷新当前下一控制决策
→ 进入 PAGE_TOPOLOGY_GATE

若 Reality 或用户明确证明目标/约束本身需要改变，先生成新的《当前任务目标与正反约束 第N+1版》，再继续执行。

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

## 7. 冻结状态规则（唯一权威）

冻结规则只定义在 BRAIN，不再单独维护“冻结状态规范文件”。

### 7.1 正式冻结版本

每个现实任务第一次任务合同冻结完成后，立即产生：

```text
《当前任务冻结状态 第1版》
FREEZE_VERSION=1
```

以后每次 CEO 正式接受一个新的状态事实：

```text
第1版 → 第2版 → 第3版 → 第4版 ...
```

只用自然整数。

PASS / FAIL / UNKNOWN / BLOCKED 都是新的现实状态，均可产生下一版。

### 7.2 实际冻结文件

每一版必须是独立不可变文件，推荐：

```text
<TASK_PATH>/freezes/CURRENT_TASK_FREEZE_V<N>.md
```

NEXT_PAGE_PROMPT 必须直接给出最新的 `FREEZE_PATH`，新 CEO 读取具体版本，不读取“冻结规范”。

### 7.3 短冻结标签

每个具体冻结版本内写一个短标签：

```text
FREEZE_TAG=<TASK_SHORT>-F<NNN>
```

例如：

```text
FREEZE_TAG=DPC-F004
```

含义：
- `DPC`：任务短码；
- `F004`：该任务第4个正式冻结状态。

标签只负责定位版本，不承载规则、证据或完整状态。
完整状态只存在该 FREEZE 文件。

禁止再使用长 JSON 作为常规 NEXT_PAGE_PROMPT 标签。

### 7.4 CEO 是唯一全局版本写者

Executor 只产出不可变 NODE_FREEZE。
CEO 接受后才生成新的《当前任务冻结状态 第N版》。

并行 Executor 不直接抢 FREEZE_VERSION；CEO 按接受顺序 Merge，避免版本冲突。

## 8. CEO_PAGE_ROTATION_GATE

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

## 9. CEO 唯一页规则

逻辑上始终只有一个 ACTIVE_CEO。

换页时：
旧 CEO 先 Freeze/Persist
→ 打开 True New Chat 接管
→ 接管成功
→ 旧 CEO 关闭

禁止两个 CEO 同时长期写状态。
禁止 Branch 代替 True New Chat。

## 10. Executor 并行门

DEPENDENCY / SHARED_WRITE / SCARCE_RESOURCE_CONFLICT ?

YES → SERIAL
NO → 只有并行能降低完整 T_VALID 才 PARALLEL

只开最少必要页面。
禁止预热空 Executor。
禁止第二套 persistent browser。
禁止多个 writer owner。

## 11. 节点大小

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

## 12. Reality

先虚拟成熟到底，再 Reality once。

Reality 中禁止改 Freeze。

FAIL/Delta：
保留已通过事实
→ 冻结现实差异
→ 新虚拟节点重新成熟
→ 新 Freeze
→ 再整体 Reality

## 13. 三类版本

METHOD_VERSION：
方法系统变化才升级，自然整数。

CONTRACT_VERSION：
任务目标/FINAL_VALID/正反约束变化才升级，自然整数。

FREEZE_VERSION：
正式《当前任务冻结状态》每次改变即升级，自然整数；第一版从1开始。

三者不得混用，不用小数。

一句话：

**先装大脑，再锁任务，再读冻结状态，再执行；Executor 一页一节点，完成即冻结关闭；CEO 可连续承接少量紧耦合状态，但防卡顿优先，最多3个 Freeze 后强制换新 CEO。**
