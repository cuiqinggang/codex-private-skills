# Polsia｜CODEX-008 全能力覆盖与成熟功能实测执行合同
TASK_ID=POLSIA_CAPABILITY_REPLICATION_20261011
NODE_ID=CODEX-008_MATURE_FULL_CAPABILITY_COVERAGE
PREVIOUS_FREEZE=V007;POLSIA-MOTHER-V007-F001
CEO_DISPOSITION_ID=POLSIA-CEO-D007-COMPLETE-COVERAGE-20261012
NEXT_DISPOSITION=CEO_APPROVED_CODEX008_OFFLINE_ONLY
ENGINE=ENGINE.md@28
SCOPE=COMPLETE_CAPABILITY_COVERAGE_AND_ONE_REAL_MATURE_COMPONENT_E2E
MOTHER_FINAL_VALID=NO

读取GitHub当前CURRENT、VERSION_CURRENT、Freeze_V007_CODEX007.md以及本CEO决定，读取本机MOTHER_CURRENT、真实V007冻结和Manifest，先查Exactly-once状态，确认V007 DONE，不重复旧节点，也不重制NASA媒体。

* 全部9类Polsia能力：工程开发与BUG修复；研究和营销及内容发布；客服/人工升级；销售获客；财务支付与对账；多Agent、并发及工作流；智能运营监控与审计；异常恢复、意外中断/冷恢复；经验学习和技能沉淀。逐类区分公开声称、现有成熟可用组件、实测业务成功、局限、后续合法验证。不给任何一类直接删除、忽略、记为全公司PASS。
* 使用正式已安装的成熟平台和现成官方能力，先找已有n8n固定流程、Codex官方内建Agent及GitHub回执、原生Windows任务与日志。可核验而无外部副作用的执行优先。至少完成**一个以前未完成的功能组合的真实隔离端到端场景**，含输入→系统响应→输出→独立验证→可恢复性，不能仅写计划。可采用本机现成测试实例、无副作用本地模拟输入与原生组件，但不自行造公司平台/HTTP后端/数据库/调度器/锁/重试系统。
* 一旦第一个成熟候选不可用，按GOOD/BAD/FIRST_DELTA分析和既有组件补选，最多3成熟路线，不能为了找完美方案重复消耗节点；如果全部无法合法运行，明确单项UNKNOWN和真实权限/环境证据，不冒充公司功能已成。
* 智能监控不仅是60秒刷新黑窗：必须区分运行状态、业务结果、故障告警、证据完整性、Exactly-once和恢复决策。当前Windows轮询与GitHub事实冻结可复用，但断电/72小时长稳仍不合格。对现成恢复机制只在合法隔离输入上验证。
* 现实应用层如果需要真实账户/付款/发布/外联/生产权限，记录技术接口和授权缺口，禁止动作，不为了模拟结果捏造成功。商业ROI当前暂停，可按客观时间和功能实效衡量最短T_VALID；旧媒体时间不得移作此合同数据。
* 自然节点完成：新增真实业务证据、9类矩阵、复用路线和故障/恢复对账、独立非作者审核、不可变V008事实Freeze及SHA，官方GitHub回读一致后才更新版本和当前指针，并建议接续覆盖缺口。母任务FINAL_VALID持续NO直到真实合同完整完成并批准。
