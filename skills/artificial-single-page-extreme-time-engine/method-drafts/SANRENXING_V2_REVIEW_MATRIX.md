# 《三人行 V2》待审查｜旧能力无损覆盖与按需触发矩阵

DOCUMENT_STATUS=REVIEW_ONLY_NOT_ACTIVE
CANDIDATE=SANRENXING_V2
CANDIDATE_ID=SRX-V2-REVIEW-C002
DEFAULT_METHOD=SANRENXING_V1_UNCHANGED
LEGACY_DELETE=NONE
LEGACY_METHOD_REF_MIGRATION=NONE
MATRIX_STATUS=DESIGN_COVERAGE_REQUIRES_REALITY_REGRESSION

## 权威原件快照（绝不删除、覆盖或改写旧冻结）

- ENGINE28：skills/artificial-single-page-extreme-time-engine/ENGINE.md，Git Blob 9dc78d259e8e3b6f8c3fbd2d252df6f92d4c1766。
- BRAIN25：skills/artificial-single-page-extreme-time-engine/BRAIN.md，Git Blob d2300549634c6903985dc58c4494c98f4174f5d2。
- TEMPLATE18：skills/artificial-single-page-extreme-time-engine/NEW_PAGE_TEMPLATE.md，Git Blob c344609d303316c51433874704007a60a74ff67b。
- ENGINE29：skills/artificial-single-page-extreme-time-engine/ENGINE_V29_DRAFT.md，Git Blob 513bc01e03361f0892b279292abeeb8a1acc7583。
- 三人行 V1：skills/artificial-single-page-extreme-time-engine/SANRENXING_V1.md，Git Blob a05fc51d661952790837dfa462bf766b16aba078；冻结 SRX-V1-ACTIVE-F001。
- 旧 A/B：skills/artificial-single-page-extreme-time-engine/routes/A/ROUTE.md 与 routes/B/ROUTE.md；适用任务依旧读取各自真实版本指针。
- 连续运行层：skills/artificial-single-page-extreme-time-engine/GPT_CODEX_ULTRA_CONTINUATION_INDEX.md；本次回读索引版本 V5，Git Blob f692db0a3a7ef7dbf8d4e260c2944d4d63ce2a5a；后续按当前索引动态定位，不能把 V5 当作永久固定版本。
- 连续运行层正式技能：skills/gpt-ceo-codex-ultra-continuation/SKILL.md；V5 当前 Git Blob 77bd211d07dc356d3e454c3c53e5101665db2620。
- Polsia 当前业务 V008、Windows live runner v3.1.0、旧方法 ENGINE.md@28 各自独立；本候选无权修改它们。

本矩阵所说“按需”仅指加载低频详细说明、调用工具、创建额外页面与执行器的时机；**从不**指关闭或跳过适用硬约束。以下是设计覆盖而非已通过的行为回归。旧规则在旧任务内按原版本原样执行；新任务候选 V2 若遇旧规则歧义或遗漏，按较严格合法约束处理并交 CEO 核验。

## 关键能力逐项无损对照

| ID | 旧来源及原功能 | V2 触发与覆盖 | 必测反例／保留边界 |
|---|---|---|---|
| 01 | ENGINE28 §2／V1 §1：唯一目标 T*=min(T_VALID) | 始终有效；以相同结果、质量、风险、授权和总耗时选路 | 不能以文本字数、首字速度或单次启动推断净节时 |
| 02 | ENGINE28 §0.1／BRAIN25 §1.1：REUSE_GATE、禁止重造成熟通用系统 | 凡需新工具、编码、连接器或架构选择，先复用现成技能与合法入口；细节按需读 ENGINE28 | 不能以临时测试名义新造调度器、锁、状态机、浏览器控制 |
| 03 | ENGINE28 §0.2：接口缺口先查成熟连接件 | 接口故障才加载对应桥、插件与官方接口说明 | 连接器可通不等于 Exactly-once／权限已验证 |
| 04 | ENGINE28 §4.1／BRAIN25 §1.2：最多三条强成熟候选 | 有真实选择空间才比较≤3条；简单任务可只有1条 | 不能强凑三个方案或因已有沉没成本不考虑更优成熟方案 |
| 05 | ENGINE28 §0.3/0.3.1／BRAIN25 §1.4：真实基线、物理界、虚拟成熟与STOP_GATE | 正式优化认证时完整测量基线、虚拟时间、风险恢复与停止门；日常直接完成任务不冒称优化成熟 | 无同合同完整时间则 VIRTUAL_MATURE/GAIN_PERCENT=UNKNOWN，不得虚构 |
| 06 | V1 §2：接单→选路→虚拟成熟→Freeze→Reality→差分 | 短任务在单页内完成必要判断；优化实验按完整链路执行 | 不能为了形式化每一步建文件／多轮 Reality |
| 07 | ENGINE28 §4／BRAIN25 §12：先成熟基线再虚拟优化、整套冻结后最终Reality | 正式声称最优需继承完整认证合同；轻任务只验交付有效性 | 不能把每个小补丁测试当 FINAL_REALITY_ONCE |
| 08 | ENGINE28 §9／V1 §1：授权、安全、结果质量是硬门 | 所有路径始终有效；高风险外部动作前检查实际授权 | 不得通过换工具、换账户、拆分请求绕过拒绝 |
| 09 | ENGINE28 §0／V1 §12：Exactly-once三态 | 任何有副作用或未知结果：DONE不重做、NOT_DONE受控执行、UNKNOWN先对账 | 断线、exit0、日志空白均不能直接重发 |
| 10 | BRAIN25 §6：每TASK_ID唯一CEO与状态写者 | 单GPT或多Executor均只有该任务唯一全局CURRENT写者；子节点隔离写入 | 并行子Agent不得竞争更新同一CURRENT／VERSION |
| 11 | BRAIN25 §6.1／ENGINE28：跨任务共享资源协调 | 实际共享冲突时才按原成熟资源仲裁，独立任务可并行 | 不能以母任务为由全局独占浏览器或阻断无关任务 |
| 12 | BRAIN25 §4/8：页面健康与重规划门 | 仅触发 PAGE_HEALTH_RISK、REPLAN_REQUIRED 或旧合同要求时换页；细节按需读BRAIN25 | 健康紧耦合小任务不得为形式强制换页 |
| 13 | BRAIN25 §8 Gate D：同页最多接受3次连续Freeze | 保留旧硬上限及提前轮换条件；旧合同继续原样执行 | 不能悄悄取消3次上限，不能误称必须做满3次 |
| 14 | TEMPLATE18 §7–10／V1 §3：Freeze→短接续码→新CEO读回→退旧页 | 仅在实际跨页时加载完整模板；保留人工复制粘贴合法回退 | 只复制不代表新CEO接管；未验自动发送不得声称自动完成 |
| 15 | ENGINE29 §2026冻结／V1 §3：Executor所有权及标签安全关闭 | 仅对自己创建且完成验收的标签执行获准关闭；不碰用户原标签 | 不能关闭CEO、别的任务标签或未完成Executor |
| 16 | ENGINE29 §2：超大型任务可选三级责任拓扑 | 有隔离与净收益证据时按需启用；日常不强制层级 | 不能为“三人行”字面含义强开三个页面或模型 |
| 17 | V1 §10：A单GPT、C Codex长执行、P并行Executor | 先单GPT；C/P须净节时预期、明确权限与独立任务边界 | 启动成本+审核+恢复超过收益时仍选A |
| 18 | ENGINE29 §3／V1 §4：n8n事件/Wait/幂等成熟复用 | 仅需持久事件/Wait/批处理时读取n8n技能；保留原工作流 | n8n health200但管理401不可绕过授权 |
| 19 | V1 §12：母任务跨节点、原生Task Scheduler、Codex原生CLI | 长时任务按已锁运行快照调用连续运行层；latest只读差分不自动迁移；不新建第二个调度器 | 方法升级不热换正在运行的runner、不重复派发旧节点 |
| 20 | 连续运行 V5 §五／历史 v3.2.2：CEO批准与Codex定位双门 | 真正启动前核对GitHub CEO授权→Windows本地NEXT合同、当前用户定位策略及权限范围 | 批准未到本地不得启动；用户暂停标签门禁时缺标签不阻断 |
| 21 | V1 §12／V5：版本与冻结SHA、真实本地路径及官方GitHub回读 | 长任务和跨页时加载CURRENT与最后Freeze，校验本地真实路径、Manifest SHA、远端指针 | 远端basename不得拼本地根目录；错误SHA/越界拒绝 |
| 22 | 历史 v3.x 故障：Freeze ID必须严格校验 | 验收合同要求唯一独立FREEZE_ID字段；现役v3.1.0仍需单独差分修复，不由V2改runner | 仅NOTE含ID或重复FREEZE_ID必须拒绝；不能冒充已部署修复 |
| 23 | V1 §12：运行进程、INFLIGHT、PAUSE/STOP/DONE/WAIT | 只有长执行才读取对应详细状态；任何UNKNOWN禁止自动再启 | 有同任务Codex PID、未知INFLIGHT或等待CEO时不能启动第二实例 |
| 24 | ENGINE29 §0A／V1 §4：GOOD/BAD/FIRST_DELTA自主恢复 | 普通可恢复技术故障触发专用诊断，修复后继续原任务；禁止反复问用户 | 明确安全拒绝/新权限/资源不可得才合法暂停受影响动作 |
| 25 | BRAIN25 §7／V1 §5：节点事实冻结、动态CURRENT、回读后更新 | 仅需跨节点/跨页/有副作用的任务创建持久状态；事实先落盘再更新指针 | 未回读成功不能宣称Freeze成功；不得用内存结论代替证据 |
| 26 | V1 §12：断电、上下文压缩与72小时观察 | 真实长程恢复场景按已落盘检查点和执行回执接续；专用详细手册按需读 | 未做冷启动/72h现实验证不得宣称永不停机 |
| 27 | ENGINE29 §3／V1 §3：B33保护、自动发送限制、浏览器归属 | 涉及旧A/B/网页自动发送才读对应ROUTE与模板；原平台拒绝始终有效 | 不能换CDP/UIA/浏览器身份绕过受保护聊天 |
| 28 | V5 §二：动态并发、十逻辑方向与PS7成熟基线 | 只对独立任务考虑PS7初始2/4或等待型4/8的历史候选；Codex Agent数仍需实测 | 不能把十方向=十Codex，不能把PS7加速推广到模型Agent |
| 29 | V5 §三/四：中文轻量监控、报警与Grafana历史归档 | 只有使用连续运行监控时才加载V5技能；日常轻量，Grafana需独立净收益与授权 | 不删除历史Grafana或事件记录；WAITING_CEO不误报警 |
| 30 | ENGINE29 §2026冻结／V1 §6：分钟秒毫秒显示、完整时间证据 | 需比较时记录真实起止、交接、等待、恢复与人工成本；无数据UNKNOWN | 不能将毫秒脚本局部耗时冒充整任务T_VALID |
| 31 | V1 §5/7：TASK_ID、METHOD_REF、TASK_STATE_REF及版本隔离 | 接续任务先按其CURRENT固定方法版本；V2只可作为新任务正式激活后的默认 | 不能自动把Polsia ENGINE28迁移到V2 |
| 32 | SKILL.md：GitHub Contents故障分流及官方读回 | 只有实际保存/更新失败才加载详细故障处理；常规写入仍必须独立回读 | 409/422/UNKNOWN不盲重试，安全拒绝不绕道 |
| 33 | V1 §11：转接码柔和提醒及减少动态效果 | 只在需要人工跨页且已有获准UI组件时按需使用；无组件默认静态提示 | 复制成功不代表新页已接管；不能声称页面自动闪动 |
| 34 | V5 §五/六：监控不派发、事故历史与未认证边界 | 仅需监控/故障时读V5事故库，DETECTED/CLEARED保存；监控无CEO权限 | 不能用监控报警替代授权，不能把本地试点当生产验收 |
| 35 | V1 §8：旧文件及冻结不可变、历史规则不得无证删除 | V2为独立候选；旧ENGINE28/BRAIN25/TEMPLATE18/ENGINE29/V1/历史日志原样保存 | 没有逐条功能等价、负例、净收益、回退证据不得删除或覆盖 |
| 36 | V1 §3/10：并行是否真正减少完整时间 | 只有独立可切分且含整合/审核/冲突净收益为正才启用并行 | 不预设3人更快，失败分支不拖住合法独立分支 |

## 规则优先级与按需边界

1. 旧任务优先其已经冻结的 METHOD_REF 和真实授权，不因候选V2或连续运行层最新版本自动迁移。明确旧A/B路线继续按其ROUTE。
2. V2在任何路径上始终遵守：授权/安全、质量、Exactly-once、REUSE_GATE、唯一状态写者、版本锁、必要Freeze及真实回读；“按需”只改变低频详细资料与额外执行器的加载时机。
3. 若触发长执行，优先已有METHOD_REF/NODE_RUNTIME_SNAPSHOT；新隔离节点或明确授权变更先锁真实commit，再按该ref读取索引与依赖，不混读移动latest。最新方法版本、Windows live runner、母任务Freeze、三人行版本互不自动同步。
4. 如果旧规则适用范围不明确、引用路径不存在、校验失败或安全约束冲突，保持原有效方法并标记REVIEW_REQUIRED，不擅自降低门槛。
5. 此表仅是“设计上有覆盖”的审查矩阵；不是逐项自动化回归已PASS，也不是全量旧规则形式化证明。完整验收见 method-drafts/SANRENXING_V2_ACCEPTANCE.md。

## 目前可以合理减少的成本（不是已测提速）

- 单GPT可完成的简单任务：不启动Codex、不创建不必要TASK目录/Freeze/新页面、不加载长执行/监控/断电详细手册。
- 长任务：首轮一次核对当前合同、授权、定位、实例和冻结证据；后续无变化时复用已经验证的同一节点证据，版本或范围变化必须重新核验。
- 失败恢复：只重验受影响的合法分支，已完成且SHA相同的GOOD资产不重做；UNKNOWN必须对账。
- 多任务：只在真实独立且预计净收益为正时并行；不重复构建成熟调度和监控。

预期完整T_VALID缩短幅度=UNKNOWN；不能把正文减少量直接换算成秒数或百分比。

## C002 优先级澄清

用户已暂停标签和ROI门禁；矩阵中的旧规则按现行授权策略适用，不自动恢复。节点commit/SHA锁定与外部实时状态核验分离，实质依赖变化只重判受影响分支。full_wall_ms由输入交付至独立验收的单调时钟计算，摊销单列；36项静态覆盖不等于36项真实平台行为已通过。
