# Hermes F011｜《三人行》V2 执行路线沉淀：虚拟成熟冻结（Reality 前）

项目 TASK_ID=HERMES-ECO-20261014；上一状态 HERMES-ECO-F010-20261015；阶段 VIRTUAL_MATURE_FROZEN；本次仅方法增量补丁，不升 Hermes 母技能 v2.0，不改变《三人行》V2 全局激活状态。
正式运行源固定：C:/Users/A/.hermes/skills/hermes-mature-supertool/SKILL.md。桥V6交通：C→A→B（与 Hermes 内部 CLI/GUI/API 业务入口无关）。

## 目标不变量与成熟证据
真正要解决：下一轮 Hermes 升级/修复/性能任务误把 F002 自编验收客户端 POST /v1/runs 的 400/401 判为 Hermes 本体失效，因此额外绕路构建 API 门，浪费时间且阻断其他合格节点。禁止把 HTTP 401 鉴权保护当服务故障。
GOOD：F010 已在 Windows C通道真实由既存 C:/Users/A/AppData/Local/hermes/bin/ltmvh-hermes-formal.ps1 驱动 Hermes 修复 F005_REPAIR/invoice.py，模型进程 exit0/52.87s；外部 Python 原生unittest 8/8 ok exit0，测试/spec/cmd哈希不变，F002原始证据不变。F006脚本级连续性通过；F008系统manifest证明2子代理完成；F007图片输出与已知fixture一致，但 vision_analyze 工具事件未认证。
BAD：F002验收脚本输入被PS对象封装含PSPath导致HTTP400，无ack；F004修复候选离线10/10，且授权API头读取的某些远程操作被平台安全拦截；这是一个独立自动化合同，不是所有Hermes任务的前置门。
FIRST_DELTA：**业务入口选择层错误**，不是网络代理/模型/CLI/WebUI全部故障。

## 候选成熟路线（对质量风险和完整时间净收益筛选）
A=现有正式CLI+Hermes原生技能/工具+外部独立验收。既有现实GOOD已证明可完成代码Repair；默认用于文件、编码、自动Agent任务；直接复用，不新造桥或后端。KEEP。
B=已有OpenWebUI网页标签页+原后端。只有当任务目标本身需要网页点击/模型选择/附件/登录态E2E时优先于CLI；网页health200只证明服务，不证明UI聊天。没有合法GUI操控能力时保持PENDING，不开第二浏览器，不拿登录态Cookie做API。
C=现有Hermes /v1/runs 正式受信API客户端。只用于确需 programmatic runs/幂等key/status/SSE的合同；需要现有已授权机制、不读/输密钥；不得作为CLI或WebUI前置依赖。旧F002 UNKNOWN不自动重派。
**通信层与业务层分离**：GPT↔Windows先C桥，若C无合法通路才A/B；Windows上Hermes任务入口才按业务选择CLI、GUI或API。GitHub持久证据可另外走B，不意味着模型任务也走B。

## 技能包最小修订
1. 固定原C盘SKILL.md SHA并同目录以外创建精确备份；不改整个技能树，不改 UNIFIED-EXECUTION-METHOD-V2.md。
2. 在现有SKILL.md的层级说明后插入一段短入口路由，指向新增 references/EXECUTION-ROUTE-CLI-FIRST-20261015.md；保留母框架上位、5轮最终标准与旧历史 PASS/FAIL。
3. 参考文件包含上面3条业务路由、Exactly-once、GOOD/BAD/FIRST_DELTA、最小Reality、按需特殊任务分流、原F010 SHA与证据链接、持续门清单、性能计时口径。
4. references/RECENT-USE-LOG.md 增加F011指针，记方法迭代不等于整站质量PASS。
5. local Test-HermesMatureSuperToolSkill.ps1 跑实际静态结构，若发现既存无关失败原样标注。原C盘形式入口仍能真实找到、按需执行。

## 现实前冻结的攻击树
- N1 METHOD_PATH_GAP：更正入口路由，备份→局部增量→回读SKILL/参考文件→hash→skill static PASS。KEEP条件：源结构、旧固定版本不变、无重复目录；FAIL回滚候选但不直接覆盖其他新变更。
- N2 SKILL_DISCOVERY_GAP：F010报告 skill_view 找不到 hermes-repair-loop-adapter；只读调查 skill registry、Hermes可用命令、真实CLI scope；只改最小可证明源；不为此重装/升级Hermes。KEEP条件：技能本身被当前Hermes工具成功识别且真正执行；否则UNKNOWN。
- N3 WEBUI_E2E_GAP：如果存在允许附着当前Chrome页的官方GUI工具，则在已开的WebUI发布合成最小任务；没有工具则NOT_TESTED，不读取Cookies/另开浏览器/不靠health200宣称PASS。
- N4 LONG_FLOW_QUALITY：在真实获准的独立新样本里做模型+文件修复+独立Gate，使用旧F010作为成熟基线；不重复运行已DONE任务。
- N5 FINAL_STATION：独立真实图片工具事件、音频/视频、真实GUI、跨Session恢复、启动恢复、冷/暖完整T_VALID，固定合同连续五轮0/5起计和7-14天实际观察。此节点不冒充已完成。
N1可立即按用户授权一次Reality部署并静态复核，其他节点按依赖串行继续；遇安全拒绝不得换工具绕过。

## 最终口径
只在同输入、同合同、同模型/成本与质量边界下比较从TASK_ACCEPTED到独立FINAL_VALID的完整墙钟。CLI退出0、健康200、单次模型响应不能等于整站100%成熟；保留 F002 独立未完API，FINAL_VALID=NO、five rounds=0/5。原FlClash、Windows代理、密钥、浏览器会话、Docker卷、其他任务不触碰。
