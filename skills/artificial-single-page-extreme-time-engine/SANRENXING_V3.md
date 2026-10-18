# 《三人行》第3版｜正式方法冻结（2026-10-17）
VERSION=SANRENXING_V3
FREEZE_ID=SRX-V3-F001-20261017
STATUS=FROZEN_PUBLISHED
METHOD_LINEAGE=V2_C002_FREEZE_PLUS_V3_VERIFIED_DELTA
GLOBAL_FINAL_VALID=NOT_CLAIMED
TEN_PAIR_AB=10/10_PASS_20_OF_20_20261017
CAP30_BASIC=30/30_PASS
CAP30_RUNTIME_RESTART=PASS
CAP1000=DEFERRED_BY_USER
LEGACY_TASKS=KEEP_PINNED_METHOD_REF

## 一、来源及冻结范围
本版不是把V2正文直接改名。其不变原则继承真实已冻结的V2 C002：
`skills/artificial-single-page-extreme-time-engine/method-freezes/SANRENXING_V2_C002_F001_20261012/SANRENXING_V2.md`，内容固定源提交 `78ffb94c4cacd07662b83a59042bc0fe3e7f69e7`。
V3唯一已定位的增量证据：`skills/artificial-single-page-extreme-time-engine/SANRENXING_V3_ORCA_HEARTBEAT_20261016.md`，内容blob `0071d3e0f658568d616ab39b57de11a353b2b992`。
Windows执行桥规范依赖 `skills/gpt-windows-execution-bridge/SKILL.md` 与 `v9-deterministic-routing.md`。
三者原件不可变；本文件以依赖链接与以下差分构成V3可发现的正式方法版本。

## 二、运行硬原则
GPT CEO为任务唯一总控；按任务实际复杂度按需调用Codex执行、Orca编排、多Executor并行，禁止为形式引入第三方；大量任务编排可以调用Orca，但无需为每个任务强制启动。
目标为同合同质量及安全约束下的完整有效时间最小化 `T*=min(T_VALID)`，包括任务接收、规划、派发、执行、恢复、合并、验收。只计业务最终有效，启动或局部成功不得冒充。
成熟方案优先，既有GOOD→BAD→FIRST_DELTA→最小成熟修复→独立QA；虚拟成熟整体Freeze后现实验证，不逐点Reality。不放宽授权、Exactly-once、业务三态、任务状态隔离及安全边界。
Codex子任务业务面和Orca管理心跳必须隔离；管理心跳超时归类UNKNOWN_RECONCILE，不得通过异常清理正常Codex业务进程。结算使用唯一request_id和官方幂等重试，UNKNOWN先对账再决定重发。原有全局预算、资源底线4GiB、独立QA不取消。
Windows执行统一先加载V9桥正式入口。C为唯一默认首选；C实际失败并有界重试失败才允许A；A也失败才B。不得改FlClash或Windows代理。每个降级记录证据；从备份回归的新任务仍先检查C。
当前任务如已固定METHOD_REF，不自动迁移；本版仅适用于明确选择V3或默认方法正式入口完成更新后的新任务。

## 三、实证边界（不能混写）
2026-10-16 r4/pilot-B 已有本地accepted=true、Orca completed及独立离线回归21项；它只是单次新版本pilot，不计正式十组稳定性。
管理心跳注入测试2/2 PASS但不等同官方服务端真实故障注入；历史r3失败永久保留。
正式10组稳定性及配对AB已完成：同一r4版本，10/10组、20/20套真实三任务完整业务通过，结果见本文件第五节。30项轻量任务的Orca基础编排也已完成，但与真实模型执行、并发容量与完整韧性须分开认证。物理极限、全面生产FINAL_VALID仍未知；不能宣称V3对V2或原生Codex整体更快。
Windows V9已写入GitHub方法入口，但所有现场运行器是否真正加载、C失败自动转A、A失败转B及C恢复复归尚未通过端到端验收。

## 四、版本解析与停机门
加载顺序：本V3文件→V2 C002固定提交的完整继承规则→V3 Orca增量→Windows V9技能入口→任务CURRENT/合同/Freeze。
若任一必需依赖不可读取，标记VERSION_MISMATCH，不静默降级为V2、不伪造V3验收。
冻结、发布与用户指定默认版本是方法入口状态，不代表十组稳定性与完整生产业务已经认证。

## 五、2026-10-17 新增正式实证成果（已验收，不修改既有冻结原则）
### A/B十组真实业务
- 固定脚本：`C:\AI\Orca-Codex-Validation-20261014\suite-ab-r4.py`，SHA256 `39CEECBEFF894BA447E86F0F24FE6E0BF0356AEB820B7C7C38736EE5DBDE5DBD`。
- 原生Codex（A）10/10 PASS，总计 **4687.004秒**，平均 **468.7004秒**。
- Orca管理Codex（B）10/10 PASS，总计 **4717.483秒**，平均 **471.7483秒**。
- 本批B总计较A多 **30.479秒（约0.65%）**；A在7组较快，B在3组较快。差异很小、样本只有10组，**不证明任一方案具有稳定速度优势**。Orca应按大批量编排能力而非单次编码加速评估。
- 20套均具备本地 `local-acceptance.json` 与 `result.json`；连续运行日志以 `ALL_REMAINING_ACCEPTED` 结束；pilot另列不抵扣正式组。计时范围为本地输入至独立QA、清理与本地结果回读，外部云端汇报不计。
- 本地总结 `C:\AI\Orca-Codex-Validation-20261014\runs\SUITE_R4_TEN_PAIR_FINAL_REPORT.md`；本地原始数据 `suite-ab-20261016-r4/p01-A` … `p10-B`。

### Orca 30项轻量任务真实编排
- Run `run_c39c0fec53ca`：Orca官方 task-create 30/30、实际dispatch 30/30、唯一worker_done结算 30/30、独立结果文件 30/30，任务权威状态全部 `completed`。
- 已检4条任务依赖关系；10次本地业务校验错误注入与恢复。**此10次不是Orca断连/崩溃注入。**
- 仅使用一个真实Orca worker终端串行执行轻量离线任务，**实际Codex模型执行为0**；不冒充30次复杂代码任务、多worker并发、公平调度或千任务容量认证。
- 隔离Orca服务正常受控重启后，原Run仍能回读30/30 completed，并可通过官方 `request-show` 查到原幂等请求完成记录。不能据此宣称活跃任务中途宕机、网络分区、磁盘写失败等均已验证。
- 30任务权威项目证据：`skills/artificial-single-page-extreme-time-engine/tasks/ORCA_CODEX_VALUE_VALIDATION_20261014/evidence/CAP30_REALITY_20261017.md`；Windows独立验收 `C:\AI\Orca-Codex-Validation-20261014\capacity-30-20261017-v2\independent-acceptance.json`、`restart-acceptance.json`。
- 30任务期间的真实失败与修正：普通shell缺Orca终端身份导致 `no_active_sender_terminal`；使用官方终端身份后创建Run；`run-use`参数须 `--id` 非 `--run`。失败样本保留，UNKNOWN先核对，不重复创建。

### 经验回流与停止条件
1. 保持管理心跳与业务执行隔离，心跳UNKNOWN不杀业务；允许合理网络波动自主恢复，结算原请求优先对账。
2. Orca适合跨任务状态、依赖、去重、派发与结算；对于少量独立任务不因已有管理层就强制使用。
3. 标记完整验收边界：10组源码业务PASS、30任务基础编排PASS、隔离服务恢复PASS；多worker并发/运行中崩溃恢复/资源竞争/400–1000容量仍未认证。
4. **用户明确决定：现阶段只做30任务；1000任务以后按实际需要再做。禁止未经新要求主动启动1000任务验证。**
5. 历史失败、修复成本和每个任务的原始JSON保留，不能把只读文件、启动、任务登记当完整业务交付。

## 六、2026-10-17 冻结增补：GPT自主闭环执行（SRX-V3-A001）

状态：FROZEN_PUBLISHED_ADDENDUM；性质：V3最小增量，原 `FREEZE_ID=SRX-V3-F001-20261017`、已验收证据和版本继承关系保持不变。用户授权本增补正式冻结发布；不将规则发布等同于运行时断线恢复已验收。

1. **GPT默认自主完成：** GPT为任务主执行者和最终验收责任人。任务开始时，内部形成最短执行契约：目标、正反约束、成熟方法、必要步骤、最终完成标准和停止规则。无需为普通任务生成庞大命令包。
2. **连续执行，不逐段请示：** 在既有授权、安全、时间及资源边界内，GPT按执行契约主动连续推进，完成中间步骤不等于业务完成；除最终验收通过、确需用户授权、触及安全边界或不可恢复阻塞外，不因普通阶段性汇报而停下等待“继续”。
3. **错误正向修复：** 遇到真实失败先采集错误与证据，优先复用同类成熟方案；对照GOOD/BAD定位FIRST_DELTA，以最小修复恢复并完成必要回归。禁止盲目重复、隐藏失败或无界自循环。
4. **轻验收、终验收：** 中途仅做避免失控的必要关卡检查与状态记录；最终采用当前正式ECC验收规则和完整业务产物验证。不得把启动、局部成功或计划完成冒充FINAL_VALID。Exactly-once、UNKNOWN先核对和原有Freeze/Reality约束不变。
5. **Codex等工具按净收益委派：** GPT直接执行可行时不强制经过Codex、OpenHands、Orca或n8n；只有具体子任务需要专门能力或预期端到端净收益为正时才委派。委派不转移GPT的全局判断及验收责任；Windows V9.0仍严格C→A→B，禁止改变FlClash或网络代理。

**真实中断边界：** 上述执行契约用于避免GPT主动在中间步骤停下，不能保证GPT会话断线后自行运行。确需跨会话持续执行时采用成熟的独立进程、持久化状态与恢复方式，并另行验收；本增补不宣称该能力已验证。

**冻结核对：** 增补不变更既有V3冻结证据，不迁移旧任务METHOD_REF，不重启已运行任务，不引入默认新调度层；速度优势须以同任务、同质量、完整T_VALID实际比较确认。“GPT可完成90%任务”是用户经验判断，不作为已验证统计。


## 七、2026-10-18 执行节点终点门（SRX-V3-A002）

本节是第六节 GPT 自主闭环的执行判定补充，不新建状态机或调度器；适用于采用本次新增规范的新任务和明确授权更新的任务。保留已冻结历史证据、旧任务 METHOD_REF、Windows V9 C→A→B、权限和 Exactly-once 约束。

**默认路线：** 对 GPT 可直接完成且相同质量下完整时间具有优势的普通任务，GPT 自行调用已授权工具执行；不为形式启动 Codex、Orca、JEV 或多代理。复杂任务也先比较完整净收益，再决定是否委派；不宣称所有任务均已证明 GPT 最快。

**一个自然任务节点的合法终点仅有三种：**
1. `DONE`：达到该节点 DONE_WHEN，真实产物及必要独立 QA 回读通过；全任务 DONE_WHEN 尚未完成时，必须凭持久化状态继续下一节点，不能把节点 DONE 说成任务完成。
2. `HANDOFF`：确已到达合同定义的安全检查点或资源/页面/会话边界，持久保存 TASK_ID、当前状态、已验 GOOD、未完成事项、下一条可执行动作、版本与回执，完成独立回读；如可在本轮继续，应自动接续，不以报告等待用户说“继续”。
3. `BLOCKED`：有具体、可复查的硬阻塞证据（例如缺少必要授权、合法工具不可用且备用路径失败、安全边界、不可满足资源限额、未知副作用未对账）。注明失败步骤、原始回执、尝试过的成熟修复与为何不能继续；不将单次超时、可修复错误、模型暂时不确定或工具阶段完成当作 BLOCKED。

**节点内闭环：** `EXECUTE → CHECK → (失败则 GOOD/BAD/FIRST_DELTA → 成熟最小修复 → RECHECK) → DONE_WHEN`。普通故障优先在当前授权内自主解决，保留已通过的 GOOD；禁止无界重试、盲目重发有副作用操作，UNKNOWN 必须先对账。中途可以记录进展，但禁止以“完成了一部分”作为主动终止理由。

**停止证据门：** 每次主动停止前必须写出 `TASK_ID、NODE_ID、DONE_WHEN、STATE(DONE/HANDOFF/BLOCKED)、EVIDENCE_REF、NEXT_ACTION`。缺任一关键依据时，若仍有可执行操作则继续，不先交阶段性终结报告；若受平台调用、上下文或会话结束硬限制，必须如实说明无法保证跨会话自动持续运行，保存可恢复接续资料，不得假称后台运行。

**效率验收：** 唯一优化指标为同质量、安全、商业成本约束下 `T*=min(T_VALID)`；连贯推进不能省略必需验证。GPT 直执行历史单次三任务：221.459 秒、独立 QA 14/14 PASS；与 Codex 10 组平均 468.7004 秒比较仅作为非盲、非配对的方向性证据，不宣称普遍加速或配额节省。此规范发布不等于节点断线自动恢复已经通过现实验收。


## 八、2026-10-19 极限短时间完整收敛流程（SRX-V3-A003）

本节将既有 ENGINE28 / V2 C002 的优化主链和 V3 GPT 自主执行约束统一成**轻量默认顺序**，不增加任何总控、引擎、调度器或强制工具层。对需要宣称“极限成熟优化”的任务执行完整流程；日常明确简单任务允许 GPT 直接完成，不能为套流程制造额外耗时。

**唯一目标：** 同业务合同、交付质量、权限、安全和商业成本约束下，最小化从接单至独立验收的有效完整墙钟时间：`T*=min(T_VALID)`；不得转而单独优化 Token、局部工具耗时、文字长度或模拟分数。

**标准六步（一次规划、连续执行）：**

1. **REAL BASELINE：** 优先使用同合同可比的现有真实 GOOD 与单调时钟日志；若不存在且允许测试，做一次最小真实运作得到 `T_BASELINE_VALID`，包含规划、工具、错误恢复和 QA；不可用则明确 `UNKNOWN`，不伪造。
2. **PHYSICAL BOUND：** 从本机实测关键路径、必要工作量、设备/网络/服务能力推导保守物理时间下界 `T_PHYSICAL_LB`。区分固定现实现法的条件界、跨成熟算法的下界与已达最佳实测，不把历史最快或某个串行流程时间误称物理极限；证据不足为 `UNKNOWN`。
3. **BROAD MATURE POOL：** 广域查找已经成功使用的成熟方案、组件、公开收益与适用条件；只保留至多三条有实质区别、可能缩短同合同完整时间的候选，不局限于现有 JEV/Codex/GPT 方案、不凑数、不从零复刻成熟基础设施。
4. **ATTACK ITERATION：** 整体虚拟推演每条候选的完成时间、启动/切换/恢复/验收成本，找最大可缩短的关键路径点；以成熟搜索→最小融合→完整刷新时间与质量约束的方式迭代。只有净收益为正的改进才保留；可融合候选，但不无证据叠加公开加速百分比或跨任务数字。
5. **VIRTUAL MATURE & STOP_GATE：** 输出预测可达 `T_VIRTUAL_VALID`、假设与可信区间、`T_PHYSICAL_LB`、两者剩余差距及最强反例；虚拟目标应不低于有效物理下界。无更优成熟改进、剩余可节时不足以覆盖新增成本、资源/质量门不满足或达到已证下界时停止攻击。若物理界未知则不宣称达到极限。
6. **FREEZE → ONE REALITY：** 整体一次冻结选中的方案、参数、合同、rollback 与唯一 `NEXT_ACTION`；随后只进行一次完整同质量现实业务验收，以 `T_REAL_VALID` 和 QA 判定是否升级。未通过则保留旧 GOOD、记录差分，不把模拟结果当生产成果，也不逐个局部改动反复 Reality。

**简洁输出合同：** `T_BASELINE_VALID | T_PHYSICAL_LB | ≤3 MATURE ROUTES | T_VIRTUAL_VALID | REMAINING_GAP | STOP_GATE | FREEZE/REALITY_STATUS`。其中实际值、推导界、外部文献结果与预测值必须分别标明；缺项记 `UNKNOWN`，不为了填表阻断合法的普通任务。

**连续执行与安全：** 沿用第六、七节：GPT 默认直接执行，普通故障自修复，节点只有 DONE/HANDOFF/BLOCKED 合法终点；V9 Windows 桥严格 C→A→B；不改变代理、不突破权限、不重复有副作用动作，Exactly-once 与独立 QA 不变。跨会话自动接续能力若未被真实认证不得宣称已经实现。
