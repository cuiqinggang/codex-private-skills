---
name: reuse-experience-brain
description: "读取和积累共同工作区的经验大脑。用户提到长期记忆、经验继承、越用越聪明、重复错误、旧解法，或AI化组织V4.2任务需要复用历史经验时加载。按触发词读取少量有来源的经验卡片，核对当前合同后采用或拒绝；收尾及21点复盘写回，保留反例并验证实际效果。"
---
# 经验大脑 V1
版本：V1，2026-10-27。它是V4.2的经验依赖，不替代执行大脑第25版、DSE或原专业技能，不增加调度层。

## 权威位置
共同工作区：`cuiqinggang/codex-private-skills` 的 `main`。
入口：`skills/reuse-experience-brain/SKILL.md`。
本技能随包经验是同版镜像；首次相关任务优先通过现有GitHub连接器读取线上 [经验索引](references/INDEX.md)，再取最相关1—3张卡。查询参数用 repository_full_name 与精确path。索引及卡片在同任务来源未变时复用，不每一步重新加载。Windows读取另加载当前Windows执行桥并先A。
没有线上访问时可读随包镜像，注明其版本/日期；不得把镜像当作最新项目状态。若正确行动依赖当前状态而无法核对，标记阻塞该动作，其他独立工作继续。

## 每次实际使用
1. 定义当前目标和合同；沿 [经验索引](references/INDEX.md) 按触发词读取相关卡片。只读导航与相关正文；不整库注入。
2. 核对环境、版本、正反约束、证据等级和不适用条件。项目状态以当前CURRENT/Freeze/最新原回执为准；卡片记录历史经验，不复活旧任务。
3. 把有效经验用于本次计划、检查或最小修复；过期/冲突/不适配就拒绝。没有命中正常继续成熟能力路由，不能凭空补经验。
4. 仅在经验影响行动时记一条最小回执：任务、经验ID/版本、采用或拒绝及原因、行动变化、真实结果、证据、时间。原任务回执已有这些字段时只留链接，不另写长报告。
5. 收尾把有新证据的增量留给原21点任务，按 [维护合同](references/MAINTENANCE.md) 去重、校验、保存与回读。无新事实不写；不自动晋升稳定规则。

## 旧记忆继承
读取 [继承映射](references/INHERITANCE.md) 和需要的 [来源清单](references/INHERITANCE.json)。
原方法/Freeze及原始日报保留原位；此包增加可跨页面读取的脱敏经验正文和原证据定位，不把所有旧资料复制入提示词，也不声称9份登记日报均已逐条蒸馏。

## 成熟与效果门
区分：保存、可找到、实际读取、改变行动、任务质量/时间净改善。文件存在或测试分数高不等于业务效率认证。
只读回忆/选路任务可用独立新上下文与隐藏期望答案验收；只证明这组回忆任务。全业务提速需同合同、同质量、同工具/成本边界的完整T_VALID对照，包含维护、检索、失败和返工。缺对照写NOT_MEASURED，不承诺模型权重变聪明或每轮必胜。
事实来源见 [成熟方案依据](references/SOURCES.md)；无需安装新的记忆框架。

## 经验卡片
- [Docker启动恢复边界](references/DOCKER-STARTUP.md)
- [H3历史精确复现](references/H3-REPLAY.md)
- [视频A/B编码契约](references/VIDEO-AB.md)
- [PayPal账户与收款资质](references/PAYPAL-ELIGIBILITY.md)
- [谷深强备V1.6宿主审计](references/GSB-V16.md)
- [租赁开源复用有效性门禁](references/RENTAL-REUSE.md)
- [Codex分层故障](references/CODEX.md)
- [Stripe来源叠色](references/STRIPE.md)
- [CalDAV取消缓存](references/CALDAV.md)
- [VEDA否决经验](references/VEDA.md)
- [Windows Harness兼容性](references/HARNESS.md)
- [HTTP重定向探针](references/HTTP-REDIRECT.md)
- [本机公网文件分享身份隔离与真实拖拽](references/FILE-SHARE.md)
- [交付制品与完整计时边界](references/DELIVERY-EFFICIENCY.md)

- [Pi原文件真实重启与分层就绪/单父优先](references/PI-REAL-BOOT.md)
- [正式浏览器MCP页面所有权审计](references/BROWSER-OWNED-TABS.md)
- [视频技术门与表演艺术门分开](references/VIDEO-ARTISTIC-GATE.md)
- [n8n安全升级限定回归](references/N8N-SECURITY-20261031.md)
- [DevSpace D通道3秒软期限及UNKNOWN核账](references/DEVSPACE-D-20261031.md)
- [共享CDP浏览器全页面附着卡顿](references/BROWSER-ATTACH-20261031.md)
- [Hermes原生后台调度与订单接续](references/HERMES-BACKGROUND-20261031.md)

- [Pi＋Google强备V2原账本与ACL](references/GSB-PI-V2-20261101.md)
- [Pi原生RPC长流程、恢复与8小时边界](references/PI-NATIVE-LONGFLOW-20261101.md)
- [OpenMausBot平台订单与确定性直达对照](references/OPENMAUSBOT-20261101.md)
- [Windows D隧道HTTP与ChatGPT插件连通分层](references/WINDOWS-D-V13-20261101.md)

- [Pi V3＋OMP18.15对照、时限截断与正式入口](references/PI-CORE-UPGRADE-20261102.md)
- [抖音公开短链接503熔断与媒体完整解码回退](references/DOUYIN-FALLBACK-20261102.md)
- [Stripe香港商户资格与真实到账E1-E4证据边界](references/STRIPE-HK-BORDERS-20261102.md)

- [Tor V4已有桌面MCP与GUI连接分层及修复](references/ONION-TOR-GUI-20261103.md)
- [海外服务三条成熟收款路径与E1—E4资格边界](references/PAYMENT-ROUTES-20261103.md)

2026-10-31仅新增有来源的经验卡与导航，不改变本技能版本，不替换正式执行大脑、Windows A→B→C通道或任何原专业Freeze。原日报及项目证据仍留C盘，经验完整T_VALID净收益NOT_MEASURED。

2026-11-01新增四张来源明确的经验卡，保持V1方法版本不变；当前项目状态继续以原CURRENT/Freeze为准。GitHub正式执行桥V12.0.3与其他项目V13路由文字冲突不可由本卡擅自裁决；本次每日复盘按用户A→B→C执行。记忆完整T_VALID净收益NOT_MEASURED。

2026-11-02仅将三张有原始证据的经验卡加入原V1入口，不改变技能方法版本；Pi最新入口与Docker状态只能按原项目时间回执核对。并非新规则正式晋升，不把代码/下载局部速度或记忆读回当作完整T_VALID提速。

2026-11-03新增两张有源项目资料的经验卡，仅扩大可检索事实：Tor桌面/官方检测页局部PASS与支付方案RESEARCH_ONLY分别保留未认证边界；Docker重复预热仍故障。没有方法版本升级或业务记忆全链提速证据。


2026-11-05新增三个有来源的经验入口，方法版本仍为V1：
- [Hermes V3的Dashboard/受控网页/ChatGPT跨站委派与ECC边界](references/HERMES-V3-20261105.md)
- [Creem/Waffo数字产品MoR与定制劳务收款分流](references/PAYMENT-MOR-20261105.md)
- [10美元活动后台试单P0提现前置核验](references/EVENT-PILOT-20261105.md)

Docker历史卡仅追加11月5日最新原回执，未认证下次启动。原项目Freeze、DSE和BRAIN第25版不变；完整业务记忆T_VALID改善仍NOT_MEASURED。2026-11-05每日任务用户明确A→B→C，专业Hermes另写D优先，不由本经验技能替任一原项目改路由。

2026-11-06有来源新增两张最小经验卡，经验方法仍V1：
- [海外收款R5—R9同条件到账证据、Wise优先撤回、钱包合法适用门禁](references/PAYMENT-EVIDENCE-R9-20261106.md)
- [DSH正式宿主与PATH候选版本差异、社区扩展仅只读诊断](references/DSH-PURGE-20261106.md)

另按原卡更新[Docker 09:33原启动恢复状态](references/DOCKER-STARTUP.md)及[Hermes 9120 Webapp图形聊天与9119终端语音差异](references/HERMES-V3-20261105.md)。没有真实账户收款、完整跨平台委派、全插件激活或完整记忆T_VALID提速证据；原合同、DSE/BRAIN25及Freeze不变。


2026-11-07有证据新增：
- [Pi成熟优先、GPT分层介入与检查器冲突守卫R57](references/PI-GPT-R57-20261107.md)

同一Docker EXP-DOCKER-001只更新11月7日18:03新的WSL预热失败时点（覆盖6日历史READY作为最新原状态），不重建卡。R57共享本机有限样本、误报纠正与真实回归不能推定全行业最优/24小时无人值守/记忆净T_VALID提速。保留经验技能V1、BRAIN25、DSE及原专业Freeze。
