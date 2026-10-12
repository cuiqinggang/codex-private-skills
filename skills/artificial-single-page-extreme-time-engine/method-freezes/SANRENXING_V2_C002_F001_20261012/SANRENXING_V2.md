# 《三人行》V2｜按需启动与无损极限时间（待审查）

VERSION=SANRENXING_V2
STATUS=REVIEW_PENDING_NOT_ACTIVE
CANDIDATE_ID=SRX-V2-REVIEW-C002
METHOD_REF_CANDIDATE=skills/artificial-single-page-extreme-time-engine/SANRENXING_V2.md@SRX-V2-REVIEW-C002
CURRENT_DEFAULT_METHOD=SANRENXING_V1
CURRENT_DEFAULT_FREEZE=SRX-V1-ACTIVE-F001
VERSION_POLICY=INTEGER_ONLY
V2_FINAL_VALID=NO
V2_T_VALID_REAL=UNKNOWN
V2_T_PHYSICAL_LIMIT=UNKNOWN
LOCAL_TEST_AUTHORIZATION=USER_REQUEST_20261012
GLOBAL_ACTIVATION=NOT_PERFORMED
V2_GAIN_PERCENT=UNKNOWN
LEGACY_METHOD_REF_MIGRATION=NO
COMPATIBILITY_MATRIX=method-drafts/SANRENXING_V2_REVIEW_MATRIX.md
ACCEPTANCE_CONTRACT=method-drafts/SANRENXING_V2_ACCEPTANCE.md

## 0. 不变架构、唯一标准

本文件仅是独立待审查候选，**不是新默认方法**，不改正式V1冻结、不改ENGINE28/BRAIN25/NEW_PAGE_TEMPLATE18/ENGINE29/旧A/B及历史证据。已开始的任务只按其CURRENT中锁定的METHOD_REF执行，尤其Polsia继续ENGINE.md@28，不因V2或连续运行层升级迁移。

一个GPT CEO是每个TASK_ID唯一决策与全局状态合并入口。默认GPT单页直接完成；仅在全程净节时有根据且获准时调用Codex Ultra、Executor并行、n8n或Windows原生任务。三人行不要求三个模型、三页面或固定三级结构；不得新造通用调度器、锁、状态机、数据库、恢复引擎或浏览器控制。

唯一目标T*=min(T_VALID)：在相同任务输入、质量、权限、安全、风险、商业成本边界下，最小化从接单至**有效验收**的完整墙钟时间，包含本次加载、规划、检索、工具启动、排队、执行、交接、人工等待、返工、恢复、冻结及独立验收。已发生的部署/维护摊销另列为 adjusted_total_ms，不混入 full_wall_ms。文字减少、局部加速、PID启动均不是完整提速证明。

## 1. 永久生效的硬门：按需加载不等于按需遵守

- 安全/授权/质量：DONE_WHEN与用户授权不变；付款、退款、发送、广告、生产、公网发布、凭据访问等需要相应明确授权；安全拒绝不能换通道绕过。
- REUSE_GATE：需要新工具/编码/连接件时先核对成熟技能包、官方接口、既有GOOD和完整成本；只允许最小适配，不重造成熟通用能力。
- Exactly-once：DONE不重做，NOT_DONE可在原授权内受控执行，UNKNOWN先对账真实回执与副作用，不盲重发。
- 唯一写者/版本：每TASK_ID只有一个CEO合并CURRENT；Executor仅写所属节点。方法、任务Freeze、连续运行技能、Windows live runner互不自动同步。
- 持久化：长任务、跨页、跨自然节点、有副作用或需恢复时，真实成果→不可变Freeze/Manifest/SHA→独立回读→再更新CURRENT→CEO验收；简单单页任务不强制制造空Freeze。
- 故障：普通可恢复阻塞按GOOD/BAD/FIRST_DELTA→成熟同类方案→最小修复→合法复验，继续原任务；授权/安全/资源等硬边界才暂停相应动作，其他合法独立分支可继续。
- 页面与历史：保留BRAIN25的PAGE_HEALTH_RISK、REPLAN_REQUIRED、同页最多3次Freeze上限；TEMPLATE18短码与新CEO回读、Executor归属关闭；旧A/B保护与人工接续后备。旧功能未证明等价不得删除、关闭或放宽。
- 证据防伪：无可比完整现实基线、虚拟模型、物理边界及最终Reality时，相关时间、提升率、VIRTUAL_MATURE、STOP_GATE与FINAL_VALID只能UNKNOWN/NOT_PASSED，不编造节时。

## 2. 接单先判路，实质变化才重判：按需选择 A/C/P

**接续任务先读TASK_ID的CURRENT→固定METHOD_REF→最新合同/Freeze；原任务按旧方法。** 本候选仅供隔离审查；未来正式激活后才对新任务生效。

新任务识别DONE_WHEN、输出质量、权限/副作用、是否需要外部工具、是否长时/跨页、现有GOOD及预计瓶颈。正常推进复用判路；目标、权限、副作用三态、依赖或资源归属发生实质变化时重判受影响分支，保留已验GOOD，不从零重做。最多轻筛三条有实质差异的成熟候选，不凑数；没有必要不追问或创建多层任务包。

| 路线 | 按需启动条件 | 默认避免 |
|---|---|---|
| A 单GPT | 当前页与获准工具足以有效完成，额外交接净收益无证据 | 不启动Codex/n8n/Windows，不强制任务目录、Freeze或换页 |
| C GPT CEO＋Codex | 大量编码、多工具、长执行或恢复，预计含审核/启动/故障的**全程净节时为正**，且已获准 | 不盲开Ultra或第二个同任务Codex；不直接拿Polsia专用runner运行新任务 |
| P 按需并行 | 子任务独立、冲突可控、合并/审核后仍有净节时 | 不预设三Agent最快，不争写母CURRENT |
| 专用组件 | 只有事件/Wait才用n8n；长时观察才用监控；受保护网页按原合法路线 | 不因组件存在就默认常驻、重装或绕权 |

日常任务用最小必要判断即可交付；若**宣称极限优化成熟**，仍执行旧ENGINE28的同合同真实基线→物理边界→成熟候选虚拟优化→STOP_GATE→整套Freeze→最终Reality合同。没有基线可以完成任务，但不能冒称优化最优。

## 3. 按需读取索引：加载说明而非跳过检查

| 触发 | 只读必要来源 |
|---|---|
| 轻任务 | 本候选入口和始终有效的硬门；不默认读全套历史/监控 |
| 正式优化认证/复杂比较 | ENGINE.md第28版、BRAIN.md第25版相关REUSE_GATE、时间、STOP_GATE章节 |
| 页面轮换/Executor归并 | BRAIN.md及NEW_PAGE_TEMPLATE.md第18版相关章节 |
| 明确旧A/B或受保护浏览器 | routes/A/ROUTE.md或routes/B/ROUTE.md及实际当前指针 |
| Codex长执行、Windows接续或故障 | 先遵守已有METHOD_REF/NODE_RUNTIME_SNAPSHOT；新隔离节点先解析并锁定真实commit，再按该ref读取索引及其依赖；latest只用于发现差分。改变既有运行快照须有明确授权、安全节点边界且无UNKNOWN；读取该TASK_ID合同/Freeze/现场，同节点不追随移动latest |
| 监控/并行/事故 | 按当前连续运行技能的操作指南、故障库与实证选择；不默认恢复Grafana |
| n8n持久事件 | 读取已有n8n独立技能与权限；健康200不代表管理接口已授权 |
| GitHub保存故障 | 读取原SKILL.md的官方Contents故障分流；UNKNOWN先查提交和SHA |

低频历史细节不必每次全文加载，但旧规则仍完整保留于原文件及无损矩阵；遇到适用范围不明或冲突，先核对原文，不默默采用宽松解释。

## 4. Codex一次完整前置核验（只有需要时执行）

CEO优先使用任务已固定的METHOD_REF/NODE_RUNTIME_SNAPSHOT。仅新任务或明确授权的依赖变更，在安全节点边界先解析并锁定真实commit，再按该ref读取索引与全部依赖Blob/SHA；节点内按该快照读取技能和合同。现场状态在动作前重新核对。最新版本可触发差分审查，但不得自动替换本节点 METHOD_REF 或 live runner。CEO核验**同一版本快照**：TASK_ID/NODE_ID/OWNER/DONE_WHEN/权限/输出；上一Freeze/Manifest真实路径与SHA、GitHub CURRENT/VERSION；正式CEO批准是否抵达Windows真实NEXT合同；当前有效的用户定位策略；用户暂停标签门禁时，缺少【页面名｜任务名｜序号】不得阻断、不猜造标签，已有标签只作参考；计划任务/CLI与PAUSE/WAIT/STOP/DONE；同任务进程、INFLIGHT及副作用三态。

全部通过才由**既有获准入口**启动一个自然节点。任何一门缺失都先修正该差分，不靠启动试错。已核验的同节点未变化证据可复用，版本、授权、Freeze或外部状态变化则重验相应项；不能把“只检查一次”理解为永不复核。

完成时按实际产物→独立审查→Freeze/SHA→GitHub回读→更新CURRENT→CEO验收；下一节点须再次满足授权和Exactly-once。exit0、PID、日志增长不代表业务成功。不存在仅靠提示词跨断线常驻执行的保证。

## 5. 故障闭环、极限停止与版本升级

执行到DONE_WHEN有效即结束；有故障则回GPT做GOOD/BAD/FIRST_DELTA、最小合法修复与Codex按需复验。已完成GOOD不重做，UNKNOWN不盲重发。额外工具、并行、换页、重型监控、重复审批/核验只有预计**完整净节时大于全部附加成本**时才启用；必须保留安全和独立证据。

旧V1、ENGINE28/BRAIN25/TEMPLATE18/ENGINE29、旧A/B、所有Freeze与故障证据**全部保留**。V2只有通过36项功能覆盖审查、隔离负例、同合同真实T_VALID对照及回滚门，并经正式批准，才能冻结新正式版本并最后更新SKILL.md和START_HERE.md入口。此前CURRENT_DEFAULT_METHOD始终V1；不热改Windows runner、不改旧METHOD_REF、不重复旧业务。

详细旧能力映射见method-drafts/SANRENXING_V2_REVIEW_MATRIX.md；真实验收与计时合同见method-drafts/SANRENXING_V2_ACCEPTANCE.md。此次回读连续运行层索引为方法V5、Polsia业务V008、Windows业务runner历史记录v3.1.0；后续执行必须再次回读，不能固定此快照。

## 6. C002 修复与可复核测速口径（2026-10-12）

- 指令优先级：现行用户指令优先于方法中的一般建议。用户已暂停的精确标签门禁与 ROI 门禁保持暂停；“继续、测速、修复”不恢复它们，不运行 ROI 计算，也不因缺这些结果阻断已授权隔离测试。
- 时钟：本批 T_VALID 从测试任务输入交付时的单调时钟开始，到独立验证接受有效输出结束。received_at/accepted_at 的 UTC 记录只作定位；accepted_at 不得后移计时起点。UTC 回拨不影响持续时间。
- 墙钟与分段：full_wall_ms 由单调起止差计算；重叠并行阶段不能相加冒充墙钟。未测分段填 NULL/UNKNOWN。历史部署和维护摊销单列，不混入本次墙钟。
- 速率：valid_throughput_per_second = 本批独立验收成功任务数 / 本批完整墙钟秒。总尝试、失败数、有效率、最小值、中位数、P95、批次窗口必须一并保留。失败/慢样本不删，不取最快局部片段代替批次。
- 极限：observed_min_ms 只是本合同、本环境、本样本中最低有效实测值。物理下界、稳定容量、不同模型/任务的全局最优均需独立证据，证据不足保留 UNKNOWN。
- 证据等级：静态36项覆盖、隔离模型决策负例、本地业务执行、原生Codex子代理闭环、GPT官网CEO/Windows自动接续、断电及72h分别报告。任何一层通过不能替代其他层。
- 实验范围：只复用本次原生Codex工具、Python标准库/PowerShell7和官方GitHub文件接口；测试脚本只用于合成任务校验和计时，不承接生产任务调度、锁、生命周期或恢复。
- 本 C002 是 V2 审查修订，整数版本策略不变。保留 C001 与 V1；不更新 SKILL/START_HERE、旧任务METHOD_REF或 Windows现役配置。全局激活另按本版本的明确发布授权处理。

线上测试合同目标为 tasks/SANRENXING_V2_TEST_20261012/BENCHMARK_CONTRACT.md；本地隔离合同位于 ../BENCHMARK_CONTRACT.md，验收/矩阵的本地审查副本位于本目录同名文件；真实数据在同任务报告内逐层注明，不能把候选文档存在理解为正式启用。
