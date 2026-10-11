# CODEX-008 九类能力证据矩阵

【Polsia执行页｜POLSIA_CAPABILITY_REPLICATION_20261011｜CODEX-008】

TASK_ID=POLSIA_CAPABILITY_REPLICATION_20261011
NODE_ID=CODEX-008_MATURE_FULL_CAPABILITY_COVERAGE
CEO_DISPOSITION_ID=POLSIA-CEO-D007-COMPLETE-COVERAGE-20261012
ENGINE=28
MATRIX_STATUS=COMPLETE_NINE_CATEGORY_FACT_COVERAGE_WITH_SCOPE_LIMIT
FUNCTIONAL_RESULT=REAL_TOOL_EXECUTED_SYNTHETIC_RECONCILIATION_AND_GIT_FILE_RECOVERY
INDEPENDENT_REVIEW=PASS_ISOLATED_FUNCTION_ONLY;evidence/INDEPENDENT_SCENARIO_REVIEW.md
MOTHER_FINAL_VALID=NO
GENERATED_AT_UTC=2026-10-11 17:04:02 UTC

本矩阵继承 V001–V007 的有限事实，并刷新 Polsia 官方公开资料。九类全部保留；公开说明、组件正式入口、合成输入上的真实工具执行和真实生产业务是不同证据层。没有一行表示全公司 PASS。V008 财务CSV功能执行、非法金额拒绝和Git单文件恢复已有真实回执。功能阶段原回执状态 PASS_FUNCTIONAL_AWAIT_INDEPENDENT_REVIEW 保留；本矩阵的独立审核状态单列文首，GitHub封存由节点持久化回执证明，不能用矩阵作者陈述替代。

## 证据与状态口径

- PUBLIC_CLAIM：Polsia 自述，或官方页面的搜索缓存；不证明可复现业务成功。
- MATURE_ENTRY：现成正式产品/内建能力的实际入口；包安装、版本、健康 HTTP 或官方文档不等于业务执行。
- LOCAL_EXECUTED_SYNTHETIC：输入明确为合成，但程序或 Agent 实际运行并产出；可验收技术子能力，不冒充真实客户/银行/收入。
- LOCAL_DELIVERY：实际生成并审查离线业务文件；未发送草稿、推荐升级角色不等于真实回复或人工处理。
- UNKNOWN/NOT_TESTED/UNAUTHORIZED：分别表示证据不足、未运行、当前缺必要授权。不得合并为失败，也不得提升为已完成。
- HISTORICAL_ONLY：冻结旧节点事实，仅继承；本节点不重跑旧媒体、旧十轮或旧文件冲突样例。

当前官网和帮助页直开都只返回 JavaScript 外壳，完整 UI UNKNOWN，不能由此判断产品离线。deck 可直接读到正文；帮助页/子处理者新增信息只来自搜索缓存，以下明确标注。来源元数据、访问差别、短摘录及官方 URL 见 [OFFICIAL_SOURCE_EVIDENCE.json](research/OFFICIAL_SOURCE_EVIDENCE.json)。过去融资/估值报道不作为功能验收依据，本矩阵不重新研究融资。

## 九类固定矩阵

| 类别 | Polsia 官方公开声称 | 已有成熟入口与配置层级 | 历史实际成果与业务成功范围 | V008 新实测差分 | 局限与后续合法验证 |
|---|---|---|---|---|---|
| 1. 工程开发与 BUG 修复 | [deck](https://polsia.com/deck)列工程、BUG监测和代理报错/修复；[子处理者声明](https://polsia.com/subprocessors)的搜索缓存列 GitHub 集成和 Sentry 诊断。属于公开自述。 | 当前 Codex 原生任务/工具/子 Agent 与正式 GitHub 连接器可复用；本机 PowerShell/Git 是成熟 CLI。n8n [GitHub 内建节点](https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.github)是官方功能候选，其本机凭据/业务流 UNKNOWN。 | 旧节点一次性文件校验/归档脚本确实运行，事实与指针 GitHub 回执可读；V3只读回归证实特定 CRLF/错误哈希解析。但新软件需求→BUG定位→修复→回归→受控交付的业务合同未验。 | 新业务特定PowerShell校验真实运行，安全坏金额被拒绝，Git恢复隔离文件字节一致；见[功能回执](evidence/FIN008_FUNCTIONAL_RESULT.json)。这是业务适配与文件恢复，完整工程BUG闭环仍UNKNOWN。 | 不能把工具成功或文件恢复称完整研发能力。下一合法验证是已有测试仓/应用中的明确 BUG，冻结失败复现和预期，现成 Codex/Git 执行修复，独立验收；部署另需范围与权限。 |
| 2. 研究、营销及内容发布 | [deck](https://polsia.com/deck)列研究、Meta广告和社媒；[广告资金帮助](https://help.polsia.com/add-funds-to-your-ads-balance)搜索缓存描述资金不足暂停和恢复。 | 已有公开研究工具、现成媒体 CLI/技能与历史内容模板；现有 n8n 官方社媒/广告连接器仅候选，不证明本机已配置。子处理者缓存列 Late.dev 社媒接口，未连接。 | 公开研究/来源去重、NASA 内容离线生成/运营资料 V004-F002 有历史事实；V005–V007引用旧内容。实际上传、投放、排期、受众反馈及获客 UNKNOWN。 | RESEARCH_REFRESH：新增官方帮助/接口边界读回；NEW_MEDIA_EXECUTION=0。本矩阵不重制、probe、解码旧媒体，不以此次研究冒充发布成功。 | 网站/内容/广告可离线起草；发布、账户连接、广告充值、外联当前不执行。后续可先用既有官方平台的 preview/draft/test 功能验证未发送内容，真实发布需明确授权和渠道回执。 |
| 3. 客服及人工升级 | [deck](https://polsia.com/deck)列 Support；[收款帮助](https://help.polsia.com/accept-payments-on-your-site)搜索缓存明确退款需要联系支持，显示人工入口仍存在。 | V005 成熟 FAQ/回复宏、证据目录与升级清单；当前 Codex；Hermes 正式入口历史 health 可见，但实际模型/工单业务未证实。n8n既有工单/客服入口待核。 | V005 实际交付21文件、18组FAQ/宏和16组合成双语草稿，非作者 PASS_WITH_SCOPE_LIMIT；12项仅建议角色类别。send=NOT_SENT，handoff=NOT_PERFORMED，人工决定/真实关闭 UNKNOWN。 | 新[财务Agent建议](scenario/agent/FINANCE_ESCALATION.md)实际生成重复、币种、孤立流水及部分/未付/超付的人工核查建议；未发送、未派单、未退款。只证明离线升级准备，独立审核状态见文首。 | 真实客服渠道、SLA、工单关闭和人工分配没有证据。下一合法验证先采用现成工单系统已有测试空间/沙盒记录，并只验证未发送草稿和角色路由；正式升级发送须有授权。 |
| 4. 销售获客 | [deck](https://polsia.com/deck)列 Cold Outreach；[语言帮助](https://help.polsia.com/polish-interface)搜索缓存区分 outreach 的受众语言。没有公开可复播成交/客户质量验收。 | V006离线资格/提问/提案模板与当前 Codex；已有 n8n CRM/邮件官方能力是候选，当前账号/固定流程 UNKNOWN。 | V006 19文件、12条合成需求和实际资格/双语草稿已独立接受；身份、订单、价格、合同、负责人均 null，未发送、未交接。FIT_OFFLINE只代表离线范围匹配。 | NOT_TESTED_FOR_LEAD_ACQUISITION；本节点财务样例不充当真实潜客、线索导入、CRM联通或转化。 | 不删除销售能力；保留潜客来源、联系合法性、CRM测试空间、去重/导入字段和人工批准缺口。后续使用已有 CRM 沙盒/本地导入预览或只读潜客研究验证，禁止未授权实际外联。 |
| 5. 财务、支付与对账 | [deck](https://polsia.com/deck)列 Payments；[客户收款帮助](https://help.polsia.com/accept-payments-on-your-site)搜索缓存说明 Stripe身份/银行设置与人工退款；[广告资金帮助](https://help.polsia.com/add-funds-to-your-ads-balance)缓存区分资金扣入与Meta实际投放可跨日不同。 | 本机现成 PowerShell [Import-Csv](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/import-csv?view=powershell-7.5) + 当前 Codex 可做隔离对账；n8n [Stripe节点](https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.stripe)官方具balance/charge接口，但无本机已认证可用证据。 | V001–V007无付款、退款、真实订单、账务联通或对账业务测试；此类保留 UNKNOWN，不能因暂无客户而取消。 | FUNCTIONAL_REAL_EXECUTED_AWAIT_REVIEW：[账单结果](scenario/output/ledger.csv)7张合成账单、[流水去向](scenario/output/payment-routing.csv)9行；已对平2，部分/未付/超付/币种核查/重复核查各1；重复2行、币种1行、孤立1行隔离。独立Agent算术来自原输入，未读作者输出。[工具回执](evidence/FIN008_FUNCTIONAL_RESULT.json)记正常业务1次/重跑0次；只限本地功能子能力。 | 当前成果仅离线合成财务对账技术子能力；真实资金/付款/退款/银行接口继续UNKNOWN/UNAUTHORIZED。后续优先已配置支付提供商正式 sandbox/test mode 和只读报表，不读取/配置凭据，不以模拟付款捏造交易。 |
| 6. 多 Agent、并发及工作流 | [deck](https://polsia.com/deck)描述多种代理执行；公开资料没有可重播并发、隔离、Exactly-once和跨会话吞吐验收。 | 当前 Codex 官方内建委派实际可调用；现成 n8n 固定流程优先查，原生 [Executions](https://docs.n8n.io/build/understand-workflows/understand-executions.md)可提供运行历史。Windows已有任务/runner仅继承，不新建生命周期系统。 | 旧节点真实不同Agent分别编写与独立审查；V007草稿/包通过非作者审查。既有运行层有跨自然节点事实，但不能推出多公司调度/72小时稳定。 | 当前研究委派与[独立财务分析Agent](scenario/agent/AGENT_FINANCE_RECEIPT.json)已真实返回，输入SHA绑定并声明未读作者脚本/输出；最终审查须由另一非作者执行，状态见文首。n8n当前401/Docker拒绝，执行0次。并发性能和资源争抢未测。 | 子Agent数量不是公司业务成功。取消/超时/资源抢占/跨会话恢复/并发性能UNKNOWN。后续采用官方原生子Agent或已核定固定 n8n 流程，在同输入和资源边界下记录返回、超时、恢复和业务输出；不自造调度/锁/队列。 |
| 7. 智能运营监控与审计 | [deck](https://polsia.com/deck)声称BUG监控与自诊断；子处理者缓存列 Sentry技术遥测。没有当前公开不可变审计/业务一致性验证。 | 已有 Windows计划任务/日志；[Get-ScheduledTaskInfo](https://learn.microsoft.com/en-us/powershell/module/scheduledtasks/get-scheduledtaskinfo?view=windowsserver2025-ps)可读运行信息；GitHub官方Contents+SHA/Blob回执、Codex工具回执；n8n executions/错误数据为候选。 | 旧节点有运行退出、输出/manifest、非作者审查和GitHub回读；V3只读回归验证parser与LF/CRLF/错误SHA，其发布与当前live入口须分开。60秒状态窗只证明展示/轮询，不是智能经营监控。 | 新非法金额真实退出1并写[guard事件](evidence/GUARD_INCIDENTS.jsonl)，输出保留；文件损坏SHA检出/恢复回执存在。当前[只读probe](probes/MATURE_COMPONENT_PROBE.md)记录任务查询拒绝、Operational日志关闭、runtime指针3.0/live头3.1差异；GitHub结果以节点持久化回执为准。 | 必须分别记录运行状态、业务结果、故障告警、证据完整性、Exactly-once与恢复决策（下表）。断电/72小时长稳持续未通过。后续先复用现成execution/log/任务查询，只在合法测试输入上验证告警与实际业务判定，不自建监控服务。 |
| 8. 异常恢复、意外中断与冷恢复 | [deck](https://polsia.com/deck)声称基础设施自愈；[设计指南帮助](https://help.polsia.com/your-design-guide)搜索缓存描述域名读取失败降级/保留旧文档，范围仅该文档功能。 | safe-file-demo旧原CLI冲突恢复；原生 [Git restore](https://git-scm.com/docs/git-restore)可恢复指定隔离路径；n8n [Error Workflow](https://docs.n8n.io/build/flow-logic/handle-errors-gracefully.md)/[Wait](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.wait)现成机制待核入口。 | V001旧文件目录冲突与10轮只限合成文件恢复；V002源URI/读取恢复历史PASS；V003仅攻击/缺口分析，未注入新故障。V3 readonly解析回归不等于现网激活或断电恢复。 | 新[功能回执](evidence/FIN008_FUNCTIONAL_RESULT.json)记录隔离ledger副本截断后的SHA变化，已知commit原生git restore恢复到相同SHA；业务执行1次且重跑0次，坏金额拒绝保留正常输出。FUNCTIONAL_AWAIT_REVIEW；只限文件级恢复，非冷启动/重启。 | 进程崩溃、写后超时UNKNOWN、半提交、断电和72小时未认证。Wait小于65秒不转存DB，不能据短等待称重启安全。下一合法验证是已有正式产品的测试执行记录/恢复接口和安全中断；不能关机、改生产或重建恢复底座。 |
| 9. 经验学习与技能沉淀 | [deck](https://polsia.com/deck)声称跨公司记忆和运行后学习；[语言帮助](https://help.polsia.com/polish-interface)缓存说明文档版本/续跑设置，但不能推出学习效果。 | 现成Knowledge Brain、技能治理/案例、原成熟规则和版本化项目证据可复用；正式Skill冻结/manifest不得原地修改。 | 既有案例与成熟规则有定向读回，KB health历史PASS；V005–V007沉淀为项目交付/修正证据，未部署新Skill或更新长期索引。受控长期提升/跨任务隔离UNKNOWN。 | 本矩阵新增官方来源访问边界、九类差分及合法验证入口；非法金额拒绝、原生Git恢复、n8n入口权限差异成为新可复查经验。它们是项目事实，不宣称自动学习服务已运行或新Skill已部署。 | 下一合法验证可用现成版本化规则将本次实际失败入口、恢复决策和checklist交下一节点试用；遵守Skill冻结/版本升级与定向知识入库流程。只有新任务实际命中并改善质量的证据，才能称复用有效；无需新记忆平台。 |

## 智能监控的六个判定面

| 判定面 | 已有正式入口/应读取的证据 | 本矩阵能确认的事实 | 当前缺口与事实限制 |
|---|---|---|---|
| 运行状态 | Windows任务状态、最近运行时间/结果、进程、原生Codex工具回执 | V007尾部退出0；当前n8n health/readiness200，任务查询HRESULT 0x80041003拒绝；Codex原日志持续写入。运行层指针3.0与live入口3.1头不同 | 工具阶段实际起止/退出已记录；任务最近结果/当前状态UNKNOWN，未改系统查询权限 |
| 业务结果 | 冻结输入、实际输出、业务规则和非作者审阅 | 新7账单/9流水真实输出、独立Agent原输入算术已返回；实际到款仍UNKNOWN | 独立审核状态见文首；n8n业务执行0次/结果UNKNOWN |
| 故障告警 | 原生stderr/退出、SHA差异、现成Executions/Error Trigger | 非法金额退出1与guard FAILURE_OPENED事件、文件损坏SHA确实检出；未测试消息推送/事故SLA | 保留BAD/FIRST_DELTA；原生TaskScheduler/Operational当前关闭，未启用 |
| 证据完整性 | 输入SHA、输出manifest、回执、原字节和Blob校对 | 新输入SHA、功能回执、独立财务输入绑定存在；Git恢复与已知SHA相同 | 本矩阵仅绑定列举回执；manifest、Freeze和GitHub原字节结果由节点相应回执证明，不以作者陈述替代 |
| Exactly-once | 先查CURRENT/MOTHER/Freeze/执行回执；DONE不重做；UNKNOWN先对账 | V007 CONFIRMED_DONE_WITH_SCOPE_LIMIT；本次INFLIGHT属于V008；新正常业务1次、重跑0次，外部未调用 | V008提交前后先查官方状态，避免重复Freeze/指针；外部付款Exactly-once UNKNOWN |
| 恢复决策 | CONFIRMED_DONE/CONFIRMED_NOT_DONE/UNKNOWN；原生恢复入口和复核 | 隔离副本损坏而原Git commit存在，原生restore恢复SHA；正常输出未被坏金额覆盖，未重跑业务 | 文件级功能恢复有真实回执；冷恢复/断电/72h仍UNKNOWN |

n8n错误工作流的执行id/url依赖保存数据，触发节点失败时字段可能不同，故不能以空字段断言未执行；官方[错误处理说明](https://docs.n8n.io/build/flow-logic/handle-errors-gracefully.md)支持此边界。官方[Wait说明](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.wait)指出小于65秒等待不转存数据库，短等待测试不能自动证明断电/重启恢复。

## 成熟路线和冻结前约束

本节点第一候选现有 n8n 固定流程已查：health/readiness HTTP200，但/rest/workflows HTTP401，Docker管道权限拒绝，精确版本和现有流程当前节点/副作用UNKNOWN。历史active Reasonix webhook与本合同不符；没有触发任何流程。具体GOOD/BAD/FIRST_DELTA及原回执在[成熟组件probe](probes/MATURE_COMPONENT_PROBE.md)，不把执行前权限缺口判为业务失败。补选当前Codex + 原生PowerShell/Git + GitHub事实回执路线已有真实功能回执，独立审核状态见文首。最多2条成熟路线，没有新增后台、数据库、调度、锁、重试或监控服务。

新组合完整节点T_VALID=UNKNOWN_AT_MATRIX_CUTOFF；完整节点计量由根代理最终报告给出。真实[工具夹具回执](evidence/FIN008_FUNCTIONAL_RESULT.json)为5.0504秒，正常guard进程2.3792秒、非法金额guard进程2.2022秒、原生git restore进程0.0529秒；这些字段边界不同，未含全部适配、Agent分析、终审和封存，绝非完整节点T_VALID。研究耗时、旧媒体时间和局部打包时间不能替代，不能测量的字段UNKNOWN。不计算ROI或恢复用户暂停的收益门禁。

## 剩余合法验证入口

1. n8n：用已有受权只读通道核当前固定流程身份、节点和副作用，再对相符的原生测试入口执行；当前401/管道拒绝证据保留，不复制凭据或绕过拒绝。
2. 财务/客服/销售/发布：先采用现成正式产品已配置的sandbox、draft、preview或只读报表；真实账户、银行/付款、人工收件、外联和公开发布另有授权缺口。
3. 工程：已有测试仓中的明确BUG，以失败复现、现成修复入口和非作者回归验证推进；本次Git文件恢复不能替代这个合同。
4. 恢复/监控：原计划任务、native executions/log和已有恢复机制分别核运行、业务、告警、完整性、Exactly-once与决策；当前task查询拒绝、事件通道关闭、runtime描述漂移不在活动节点热改。断电、OS重启、72小时稳定持续UNKNOWN。
5. 学习：将此次真实失败入口/恢复checklist按现成版本化规则交下一任务试用；冻结Skill不原改，后续命中/质量提升须实际证据。母任务FINAL_VALID保持NO。

Knowledge Brain usage:
- INDEX checked: YES；C盘正式源定向读取。
- ROUTING_MAP checked: YES。
- Relevant indexes checked: skills-index.md定向读取；Top-K为本任务现有CAPABILITY_MATRIX/REUSE_MAP、V003/V005/V006/V007事实和V3运行层回执。
- CodeGraph used where relevant: NOT_APPLICABLE；本矩阵仅文本/公开来源证据。
- OpenHuman reference used where relevant: NOT_APPLICABLE；未设计记忆架构。
- Sync run before/after: NO_SYNC；未改KB/Skill/索引，health由根代理节点收尾统一记录。
- If not used, reason: 已使用定向路由；只C盘，无H/K读取/写入，无全库扫描。

【Polsia执行页｜POLSIA_CAPABILITY_REPLICATION_20261011｜CODEX-008】


