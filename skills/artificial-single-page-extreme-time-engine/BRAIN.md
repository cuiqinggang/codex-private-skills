# 《极限短时间执行大脑 第25版》

版本：第25版
升级来源：第24版
状态：CURRENT
唯一标准：T*=min(T_VALID)


## 第25版增补：现状保存与恢复

本版连续继承第24版，服从《自动化单页面极限短时间引擎》第28版；升级版本仅保存当前状态，不宣称成熟。

浏览器供n8n、Codex与其他合法客户端共享。无冲突任务并行，只对同一会话、标签页或共享上下文中的实际冲突按最小范围协调；不能用全局独占替代正确协调。保留成熟n8n原生MCP/去重/Wait和Playwright既有技能包，禁止重造。

已确认的三态：已执行不再写、确未执行才受控重试、UNKNOWN禁止盲重试但不阻断无关任务。现有只读、原浏览器可逆写入、多客户端共存、n8n串行及去重和Wait恢复均有现实证据；跨客户端资源级仲裁、不同目标并行、异常释放、UNKNOWN端到端对账与生产入口整合未完成。FINAL_VALID=NO，REAL_SEND=PROHIBITED。用户指定新的现实验收暂缓。缺失整套时间对照，不得称虚拟成熟完成。

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

## 1.1 REUSE_GATE 执行检查（第21版）

BRAIN 在任何新写代码或改动执行路径前按顺序核对：
- USER_SUPPLIED_ENTRY：用户指定的技能包、已有进程和执行入口是否已经实际读取并尝试复用？
- MATURE_BASELINE：已有成熟框架、配置、插件或工作流是否具备对应能力？是否有可核对来源及调用接口？
- ADAPTER_ONLY：拟新增代码是否只有映射、配置、调用、业务校验？若出现新状态机/调度器/锁/恢复机制，立即 FAIL。
- TOTAL_COST：在同等有效性及安全边界下，包含部署、调用、恢复和维护的总成本是否优于已有成熟基线？

四项必须都有事实证据；不可凭“通用功能简单”“以后再换框架”“先模拟跑通”通过。未通过则保留既有成果、停止新自研，回到成熟方案选择；无法满足时标记 BLOCKED 并提出缺口，不得默默放宽禁令。

## 1.2 初始三强比较执行门（第22版）

初次大型任务先锁合同/VALID并寻找已有成熟方案，做最少必要安全与可行性轻筛，选一条可合法完成的GOOD成熟基线先现实完整运行，得到T_BASE_REAL与各环节耗时；同合同同边界的历史完整样本可复用。然后依据现实瓶颈深入比较最多三个成熟强候选，通常三个但不足不凑数，记录可核验入口、优势、短板和全链路成本。
先评估最优单体，再评估通过成熟接口实现的强点互补组合；不得新写状态机、调度器、锁或恢复组件以实现组合。以完整 T_VALID、有效性和长期净收益选择初始 BASELINE；候选筛选本身的时间成本纳入净收益。
初选结束并非任务完成：继续执行 ENGINE 第28版所规定的节点内连续虚拟成熟直到 STOP_GATE→Freeze→Reality once。遇到不适配的底座要重新比较候选，不能用沉没成本保护先前选择。

## 1.3 成熟连接件修复门（第23版）

接口缺口先查现有执行桥、标准连接器、官方插件或Worker；最多比较三个成熟连接方案。不得将“尚未发现直接接口”等同“平台不适合”，不能因此未经总成本复核直接换编排器。允许已有成熟接口组合，不默认自写胶水，更不许自写通用HTTP调度服务。需确认调用契约、资源仲裁、消息发送未知态、恢复语义各自完整；解决传输不等于实现恰好一次发送。
若原底座可通过成熟接口合法复用并且完整净收益更优，则保留底座继续虚拟成熟；只有明确证据显示当前底座不可满足硬约束或净收益不佳，才重新三强选型。禁止沉没成本锁定，也禁止未经验证的频繁切换。

## 1.4 虚拟成熟时间验收门（第24版）

在每个节点申请 `STOP_GATE=PASS` 或宣称虚拟成熟完成之前，执行大脑必须生成并核验统一任务合同下的完整时间对照：
- `T_BASE_REAL`（优化前成熟GOOD基线同合同同质量的完整现实时间或可信历史完整实测）及分段证据；
- `T_PHYSICAL_LIMIT`（由现实关键路径和不可避免物理/平台约束推导的理论下界或可信区间，附依据和误差）；
- `T_VIRTUAL_BEST`（冻结候选整套方案的可重放虚拟最短有效时间），附完整关键路径、部署/调度/恢复/验收开销、模型假设与误差边界；
- `DELTA_T=T_BASE_REAL-T_VIRTUAL_BEST`、`GAIN_PERCENT=DELTA_T/T_BASE_REAL×100%`、`SPEEDUP=T_BASE_REAL/T_VIRTUAL_BEST`；
- 逐轮虚拟优化前后时间对照、已验证 VALID/失败恢复路径与净收益停止依据。

不得将理想并行参照或单项加速数字当作真实整套方案成绩；若关键接口、时间参数或故障恢复没有可信证据，只能报告区间或 UNKNOWN，`VIRTUAL_MATURE=NO`，继续修复或明确标记 BLOCKED，不能以“架构收敛”代替完成。虚拟优化成熟的成绩属于 VIRTUAL；Reality once 后才可记录实际 `T_VALID_REAL`。

## 1.4.1 时间方法执行顺序澄清（2026-10-10；仍为第25版）

执行时先锁任务合同、VALID、授权与安全边界；复用已有成熟GOOD方案做最少必要轻筛，先取得同口径完整现实基线T_BASE_REAL与分段时间（BASELINE_REALITY），可复用可信历史完整样本，不拿局部耗时冒充全程。由真实关键路径和不可并行约束计算有来源、有不确定性说明的T_PHYSICAL_LIMIT理论极限下界/区间。
随后基于现实瓶颈深入比较最多三个成熟强候选与现成接口互补组合，锁定虚拟BASELINE；找最大预期净收益点→虚拟替换→刷新整套VALID、正常与故障恢复耗时和长期净收益→连续迭代，至边际净收益不大于零且STOP_GATE的完整时间及VALID证据满足。整套Freeze后对冻结候选仅作一次FINAL_REALITY_ONCE，并以T_VALID_REAL记录优化后现实耗时。
四种时间不得混用：T_BASE_REAL=优化前成熟基线真实完整时间；T_PHYSICAL_LIMIT=由现实物理约束推导的理论参照；T_VIRTUAL_BEST=连续虚拟优化后的整套最佳有效时间；T_VALID_REAL=最终冻结方案现实验收结果。前置BASELINE_REALITY不属于“每优化一步测一次”的Reality。无法合法测量时保留UNKNOWN/BLOCKED，不绕开既有安全审查或UNKNOWN禁止重发规则。此处为第25版解释澄清，B29按原继承关系使用，无须复制规范或升级版号。

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
成熟方案轻筛→先测现实成熟GOOD基线→物理下界参照→最多三成熟候选比较锁定虚拟BASELINE
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

## 6. CEO 是当前 TASK_ID 唯一任务状态写者

Executor 只产出不可变 NODE_FREEZE。
CEO 接受后才修改当前 TASK_ID 的任务状态。

作用域硬规则：
- 每个独立现实任务都必须有唯一 TASK_ID；
- ACTIVE_CEO、CONTRACT_VERSION、FREEZE_VERSION、SAME_CEO_FREEZE_COUNT、TASK_PATH、STATE_REF 默认全部属于当前 TASK_ID 命名空间；
- “CEO 唯一 writer”只表示：同一 TASK_ID 的任务状态只能由该 TASK 的 ACTIVE_CEO 写入；
- 不表示整套系统同时只能运行一个 CEO；
- 两个不同 TASK_ID 可以各自拥有一个 ACTIVE_CEO，并行推进各自不冲突的节点。

每接受一个真正改变项目状态的冻结结果：

FREEZE_VERSION=N → N+1

包括 FAIL，因为失败也是新的现实事实。

并行 Executor 不直接争抢当前 TASK_ID 的 FREEZE_VERSION；该 TASK 的 CEO 按接受顺序 Merge，避免 split-brain。

### 6.1 跨任务并行与系统共享资源仲裁

当两个或更多独立 TASK_ID 同时运行时，先保持任务状态完全隔离，再只对真正冲突的共享资源做局部串行。

固定规则：

1. **任务状态隔离**
   - TASK_A 的 CEO / Executor 只能写 TASK_A 的任务路径、Freeze、STATE_REF 和证据路径；
   - TASK_B 同理；
   - 任何跨 TASK 写入、Merge、回滚、版本递增都直接 Fail Fast。

2. **ACTIVE_CEO 作用域**
   - ONE_ACTIVE_CEO = PER_TASK_ID；
   - 同一 TASK_ID 禁止旧 CEO / 新 CEO split-brain；
   - 不同 TASK_ID 的 ACTIVE_CEO 可以同时存在。

3. **共享资源不是任务状态**
   - persistent browser、同一 GitHub branch writer、单实例 Windows 控制器、GPU 独占槽、同一可变文件/数据库等，属于 SYSTEM_RESOURCE；
   - 这些资源不由某个 TASK 的“唯一 CEO writer”规则直接垄断，而由独立 SYSTEM_RESOURCE_LEASE 仲裁。

4. **SYSTEM_RESOURCE_LEASE**
   - 以稳定 RESOURCE_ID 为键；
   - 同一时刻一个需要独占写/控制的 RESOURCE_ID 只能有一个 owner；
   - owner 至少绑定 TASK_ID + NODE_ID + OWNER_ID；
   - 获取与释放必须可验证，禁止口头假定“应该没人用”；
   - 若资源支持安全并发只读/独立 namespace，可按资源能力允许共享；否则串行冲突节点。

5. **只串行冲突节点**
   - 发生 SHARED_WRITE 或 SCARCE_RESOURCE_CONFLICT 时，只等待涉及该 RESOURCE_ID 的节点；
   - 不得因此把两个完整 TASK 全部串行化；
   - 另一 TASK 的无冲突节点继续推进。

6. **persistent browser**
   - 已存在合法 persistent browser 时禁止因第二 TASK 再启动第二套；
   - 可安全 attach / 独立 tab 使用时复用；
   - 若存在全局页面切换、profile mutation、关闭窗口等破坏性动作，则必须先获得对应 browser lease；
   - 任何页面关闭必须校验 TASK_ID / PAGE_ID / ownership，不得误关另一 TASK 页面。

7. **共享 writer**
   - 对同一 GitHub branch、同一可变文件、同一数据库记录等共享写目标，必须在具体写操作粒度获取 writer lease；
   - 不同 TASK 的独立任务 Freeze 仍各自由各自 CEO 生成；
   - 共享 writer lease 只保护底层共享写入，不改变各 TASK 的 FREEZE_VERSION。

8. **FAIL / rollback / cleanup 作用域**
   - 一个 TASK 的 Reality FAIL、回虚、Repair、Reverify 只回滚本 TASK 后续控制状态；
   - 不得回滚另一 TASK 已接受事实；
   - TASK FINAL_VALID 后只释放本 TASK 拥有的页面和 lease；
   - 共享资源仍被另一 TASK 使用时不得销毁。

9. **无仲裁即 Fail Fast**
   - 若节点确实需要同一共享可变/稀缺资源，而当前没有可证明的 lease / CAS / 单 owner 仲裁能力，则判 CONFIRMED_METHOD_FAULT_OR_BLOCKED_RESOURCE_CONTROL；
   - 不允许两个 writer“先一起跑再看会不会撞”。

下游文件中的未限定 ACTIVE_CEO、global state writer、FREEZE_VERSION、SAME_CEO_FREEZE_COUNT 等表述，统一按本节解释为当前 TASK_ID 作用域；只有显式写成 SYSTEM_GLOBAL 的字段才是整套系统全局唯一。

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

对每个 TASK_ID，逻辑上始终只有一个 ACTIVE_CEO。

换页时：
旧 CEO 先 Freeze/Persist
→ 打开 True New Chat 接管
→ 接管成功
→ 旧 CEO 关闭

禁止同一 TASK_ID 的两个 CEO 同时长期写状态。
不同 TASK_ID 的 ACTIVE_CEO 可同时存在，但不得写入彼此任务状态。
禁止 Branch 代替 True New Chat。

## 10. Executor 并行门

DEPENDENCY / SHARED_WRITE / SCARCE_RESOURCE_CONFLICT ?

YES → SERIAL
NO → 只有并行能降低完整 T_VALID 才 PARALLEL

只开最少必要页面。
禁止预热空 Executor。
禁止第二套不必要 persistent browser。
同一 TASK_ID 的任务状态禁止多个 writer owner；同一 SYSTEM_RESOURCE 的独占写/控制也禁止多个 lease owner。

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

先合法运行成熟基线取得现实事实，再虚拟成熟到底、整套Freeze，然后对优化结果执行一次最终Reality（FINAL_REALITY_ONCE）。原句只禁止逐点优化Reality，不禁止前置BASELINE_REALITY。

Reality 中禁止改 Freeze。

FAIL/Delta：
保留已通过事实
→ 冻结现实差异
→ 新虚拟节点重新成熟
→ 新 Freeze
→ 再整体 Reality

## 12.1 成熟系统故障处理：第一性原理主路径

成熟系统出现故障时，不重新发明系统。

固定主路径：

```text
FAULT
→ LAST_GOOD
→ 从正确源头沿真实链路正向推进
→ 稳定重现 BAD
→ 持续缩小 GOOD / BAD 边界
→ 定位 FIRST_DELTA / 最小责任点
→ 调用成熟故障方法加速定位与修复
→ 最小 Repair
→ 从合法源头完整重跑
→ Regression
→ FINAL_VALID
```

核心不变：第一性原理负责确定“问题从哪里开始发生”，成熟方法只负责加速 GOOD→BAD 边界收敛。

成熟方法、工具、案例和同类问题解决方案能直接复用就复用，能组合就组合；它们是加速器，不替代主路径。

没有合适成熟方法时，仍回到第一性原理，从 LAST_GOOD 正向推进并重现 BAD。

仅当现有成熟实现已经选定、局部缺口有证据时，允许在其扩展接口上进行**最小适配或局部补丁**；**禁止重新开发通用组件**。未找到成熟实现不构成自行开发许可。所有候选必须先通过 ENGINE 第28版 `REUSE_GATE`；否则不得编码、虚拟重放自建实现或 Reality。

## 13. 三类版本

METHOD_VERSION：
方法系统变化才升级，自然整数。

CONTRACT_VERSION：
任务目标/FINAL_VALID/正反约束变化才升级，自然整数。

FREEZE_VERSION：
正式《当前任务冻结状态》每次改变即升级，自然整数；第一版从1开始。

三者不得混用，不用小数。

一句话：

**先装大脑，再锁任务，再读冻结状态，再执行；每个 TASK_ID 各自只有一个 ACTIVE_CEO 与任务状态 writer；跨 TASK 只对真实共享资源用 SYSTEM_RESOURCE_LEASE 仲裁；Executor 一页一节点，完成即冻结关闭；CEO 可连续承接少量紧耦合状态，但防卡顿优先，最多3个 Freeze 后强制换新 CEO。**
