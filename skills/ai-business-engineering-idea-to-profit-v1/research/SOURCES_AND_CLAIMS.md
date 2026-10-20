# V1来源与证据账本（2026-10-20整理）

证据等级：P1官方一手声明（只证明公司如此公开陈述）；P2采访/主流新闻；P3第三方评论/聚合；H未核实假设；E内部估算；R真实执行回执。**P1不等于独立财务审计**。所有价格、许可证、数据在实施当日重查。

## Lovable来源与主张
| 主张 | 来源链接 | 级别 | 严格口径 |
|---|---|---|---|
| AI自然语言生成App，含UI/数据库/逻辑 | https://lovable.dev/build/app-builder | P1 | 宣传/产品页面；不保证任意应用安全可用 |
| AI自然语言生成网站、设计/内容/托管 | https://lovable.dev/build/website-builder | P1 | 宣传/产品页面；SEO/访问量/转化需另测 |
| 2026-08融资约4亿美元、估值约133亿美元 | https://lovable.dev/blog/series-c | P1 | 官方融资公告，非公司当前利润或技术成本 |
| 用户调查：接近80%受访者希望商业化；其中超过1/3已有revenue | https://lovable.dev/blog/series-c | P1 | 调查自述；分母、样本偏差待核；revenue≠profit；不能说三分之一全体用户盈利 |
| 支付、SEO、Google Workspace/M365、Salesforce、Stripe、ElevenLabs、安全扫描与治理等 | https://lovable.dev/blog/series-c | P1 | 有已实现、集成、宣传或未来方向，必须逐功能检查官方文档/真实账户 |
| 免费版、Pro/Business/Enterprise及额度 | https://lovable.dev/pricing | P1 | 定价随时间变动，历史约25/50美元月费不是永久价格 |
| 公司自用AI销售团队/客户案例 | https://lovable.dev/customers/lovable-sales | P1 | 自述个案，不能外推普遍成功率 |
| GPT Engineer历史技术线索 | https://lovable.dev/gpt-engineer | P1 | 不表示Lovable现行商业平台源代码开放 |
| 项目数/访问量/ARR等历史谈话数字 | https://lovable.dev/blog/series-c | H/P1待核 | 2026-10-11谈话提及6000万项目、9亿月访问；逐项官方口径、统计期、分母需再核实 |
| “创始人演示从想法到高盈利的全自动闭环” | 用户视频与公开产品页面 | H | 访谈表达愿景不等于逐项自动执行与盈利经审计 |

## Polsia来源与主张
| 主张 | 来源链接 | 级别 | 严格口径 |
|---|---|---|---|
| AI公司自主经营产品定位 | https://polsia.com/ ; https://polsia.com/deck | P1 | 官网/投资材料自述，不是完全自治证明 |
| 创始人Ben Broca与单人公司叙述 | https://inshorts.com/en/news/polsia-offers-ai-co-founder-that-can-run-a-company-by-itself-1775154769513 ; https://www.linkedin.com/company/polsia | P2/P3 | 另有采访称Ben Cera；名称/身份关系待一手核实 |
| 市场研究、MVP、基础设施、广告、客服、日报；月费约49美元 | https://solofounders.com/blog/80-ai-20-taste-ben-cera-on-the-future-of-solo-founding/ | P2 | 采访叙述，不等于每个用户实际能自动运行 |
| 工程、增长、市场、CEO等专业agent与账号资源自动化 | https://workingagents.ai/blog/2026-03-06-07-24-polsia-review.md | P3 | 评论/评测，账号接入、合规与权限必须独立核实 |
| 自治约80%、每日自动监控/修复/退款 | https://solofounders.com/blog/80-ai-20-taste-ben-cera-on-the-future-of-solo-founding/ | P2 | 公司/创始人自述；无独立可靠性测试 |
| 报道融资3000万美元、估值2.5亿美元 | https://jawlah.co/en/57674 ; https://www.linkedin.com/posts/castagliuolo_inside-the-company-that-raised-30m-at-a-activity-7476539543857577984-2838 | P2/P3 | 报道数字，需一手融资文件/投资人交叉核验 |
| 一个月约100万美元ARR、托管1000多家公司 | https://workingagents.ai/blog/2026-03-06-07-24-polsia-review.md | P3 | 仅转述/宣传；收入定义、活跃、留存、利润未经审计 |
| 透明实时运行feed | https://workingagents.ai/blog/2026-03-06-07-24-polsia-review.md | P3 | 透明展示不等于成功率或安全认证 |
| 风险：集中凭证、权限、治理、错误营销、退款 | 同上 | P3+合理风险推断 | 是必须验证的安全议题，不是已证实事故 |

## 研究报告与二手工具参考
- 2026-10-11 Deep Research报告：研究Lovable官网、Polsia报道、完整流程、复刻成本、开源框架。研究结果存 research/DEEP_RESEARCH_20261011_REPORT_ARCHIVE.md；原始报告在Deep Research应用中。
- https://theaiinsider.tech/2026/03/24/lovable-accelerates-ai-platform-expansion-with-strategic-acquisition-push/ 曾提Lovable约6.6B估值与约400M ARR；是较早时间的报道，不能与2026-08估值并列为同期，更不能不核实ARR定义。
- https://www.splunk.com/en_us/blog/learn/agent-frameworks.html 提及LangGraph和OpenAI Agents SDK，只是技术选型线索。
- 官方或原始开源项目：https://github.com/dyad-sh/dyad ; https://github.com/stackblitz-labs/bolt.diy ; https://github.com/OpenHands/OpenHands ; https://github.com/langchain-ai/langgraph ; https://github.com/openai/openai-agents-python 。
- 其他服务：Stripe https://stripe.com/docs ; Supabase https://supabase.com/docs ; n8n https://docs.n8n.io/ ; Shopify https://shopify.dev/docs ; HubSpot https://developers.hubspot.com/ ; Google Search Central https://developers.google.com/search/docs 。

## 必须持续复核的冲突与未知
1. 133亿美元估值是资本市场估值；无法从133亿美元减去Polsia的2.5亿美元得到“获客与盈利功能价值”。
2. 受访者1/3已有收入不是“1/3所有用户有净利润”，需调查分母/样本/金额/留存/退款。
3. 深度研究旧报告声称“最小原型至少5–10人、成熟平台至少千万美元”是宽泛推测；不能拿融资额当复制成本。另有按成熟组件复用的小型原型方案，见economics文件。
4. Lovable“具备第三方接口”不等于可自动找客户、自动广告、自动成交、自动高盈利。
5. Polsia单人、80%自治、收入与融资数字的独立审计不足。
6. 2026-10-11既有Codex启动回执不是产品完成证据；截至2026-10-20应重新读取状态。
7. 原始深度研究未逐项给出全部估值和成本可审计数据，V1保留缺口，不填虚构精确值。