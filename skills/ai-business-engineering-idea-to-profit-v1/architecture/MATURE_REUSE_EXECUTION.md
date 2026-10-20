# 成熟方案全整合：AI商业工程执行架构 V1

## 1. 核心不是另造平台，而是能力路由
业务总线（逻辑，不必开发新服务）：客户问题→研究/验证→报价→产品生产→质检→分销→线索/销售→支付→交付→复购/客服→财务→反馈。**AI CEO负责计划和取舍；Codex负责有优势的编码与测试；现有官方服务负责标准业务动作；真实客户与市场负责决定能否赚钱。**

新任务默认按2026-10-20三人行V5：skills/artificial-single-page-extreme-time-engine/SANRENXING_V5.md（知识检索优先、轻量状态、按需逻辑岗位）。旧Lovable任务V1和Polsia任务旧METHOD_REF必须原样保留。默认单GPT执行，只有实际有净收益才调用Codex/并行代理。多代理数量不等于商业能力。

## 2. 优先成熟组件的功能映射
| 能力 | 先选已有/官方成熟方案 | 替代候选 | 接入门 |
|---|---|---|---|
| 任务规划、研究 | GPT与已有知识库、可信公开搜索 | 人工访谈/专业研究 | 事实来源与反例 |
| 自然语言生成产品 | 已安装Codex + 现有项目模板 | Dyad、bolt.diy、OpenHands | 许可证、系统可运行、测试 |
| 数据与身份 | 现有数据库/托管、Supabase等 | Neon/其他成熟云 | 账号、隐私、租户隔离 |
| 代码管理与交付 | GitHub、官方CI、成熟部署平台 | 托管构建服务 | 测试、回滚、审计 |
| 网站/SEO | 已有CMS、Google Search Central | 静态站、商店模板 | 站点所有权、合规内容 |
| 支付与订阅 | Stripe官方SDK与TEST MODE | Shopify支付等合法服务 | 真实商户审核、退款、税费 |
| CRM/销售 | HubSpot或已连接CRM | 授权表单+简单账本 | 同意、数据留存与去重 |
| 邮件/客服 | 已有Gmail/客服系统及批准流程 | Mailgun等 | 反垃圾邮件、敏感数据、发送审批 |
| 营销渠道 | 官方平台管理工具/合法API | n8n固定已验证工作流 | 广告账户、预算审批、平台政策 |
| 运营监控 | 现有Windows触发/日志、原生云监控 | Prometheus/Grafana按规模选 | 不造重复监控服务 |
| 长任务恢复 | 现有GitHub Freeze、原生调度、Codex resume、既有Loop/ECC | n8n已有成熟触发/等待 | Exactly-once、唯一写者、可回读 |
| 财务分析 | 真实订单/成本数据+会计表 | 现成会计服务 | 测试/真实分账、退款和税务口径 |

开源并不意味着所有托管、Pro功能、WebContainer、商用API都免费。Dyad：https://github.com/dyad-sh/dyad；bolt.diy：https://github.com/stackblitz-labs/bolt.diy；OpenHands：https://github.com/OpenHands/OpenHands。注意bolt.diy的仓库许可证与WebContainer商用许可可能分离。官方文档/许可证实施前重读，不自动安装。

## 3. 选择路径：三个以内成熟方案
A=现有GPT/Codex + 现成产品模板 + 已有GitHub + 官方托管/沙盒支付。通常在已有环境最少依赖。
B=Dyad本地生成器 + 官方服务。仅在实际减少完整有效时间且可合法部署时选择。
C=bolt.diy等浏览器型生成器 + 既有集成。需明确WebContainer商用授权和运行资源。
比较 T_VALID = 接单+调研+规划+安装/配置+开发+交接+测试+返工+部署/维护摊销+用户操作；必须同任务、同质量、同安全约束。未测T_VALID=UNKNOWN，不宣称倍率。

## 4. 任务合同与证据对象
TASK_ID；METHOD_REF；CONTRACT_VERSION；OWNER；NODE_ID/WORK_ITEM_ID/ATTEMPT_ID；INPUT_HASH；GOAL；DONE_WHEN；ALLOWED_ACTIONS；FORBIDDEN_ACTIONS；COST_CAP；CUSTOMER_DATA_POLICY；SOURCE_REFS；EXPECTED_OUTPUTS；T_START/T_END_MONOTONIC；EVIDENCE_PATH；STATE；NEXT；FINAL_VALID。
状态：PLANNED→EXECUTING→VERIFYING→FROZEN→NEXT/DONE；故障为RECOVERING；外部授权为WAIT_FOR_USER。仅唯一任务所有者更新全局CURRENT；执行者写自己的节点结果与不可变Freeze。没有持久化回执不称自动续接。

## 5. GOOD/BAD/FIRST_DELTA与Exactly-once
遇到失败先确定失败层级（模型、CLI、网络、API、权限、业务逻辑、支付、发布）。记录最后已证实GOOD、当前BAD与首差分FIRST_DELTA；从历史知识和官方成熟方法找合法候选，最多3个高价值进入验证。已成功步骤不重复执行。对有副作用的动作：
- CONFIRMED_DONE：禁止重做。
- CONFIRMED_NOT_DONE：在原授权范围内可受控重做。
- UNKNOWN：只读核查远端回执、订单、消息ID、部署版本，不盲重发。
明确被拒绝的行为不得更换执行工具规避；只恢复其他获准的独立子任务。

## 6. 真实赚钱闭环中的人类责任
AI可以研究、推荐、写产品、出报价草稿、生成营销内容、整理客户请求、诊断代码；真实市场需求与付款意愿要通过真人/真实交易验证。未经授权AI不自动向陌生人发送商业邮件、不擅自开广告、不自动扣款退款、不对外保证收入。重大合同、预算、个人信息、财税、合规和平台政策需要相应负责人批准。记录谁授权、授权了什么、额度和时限。

## 7. 数据、隔离与监控
客户数据与密钥不写公开GitHub、提示词日志或视频；生产密钥保存在官方凭证管理系统。独立业务使用独立资源/访问范围，审计记录只保留必要非敏感字段。定期校验业务事件、支付回执、客户服务结果和成本。故障恢复不仅是agent输出文字，必须完成原业务目标并通过回归测试。

## 8. V1的首个建议演示
使用已有视频内容生产能力，构建“客户输入需求→可交付视频样片/报价→客户留资沙盒→运营记录→人工审核→质量回执”最小产品。先做B2B真实交付验证，再扩展自动生成站点/营销、CRM和支付；避免先开发泛用Lovable克隆。真实客户外联、生产支付、广告投放另行授权。