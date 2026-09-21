# Monid 统一外部工具网关索引

- Parent: `one-person-ai-company-success-routes`
- Resource type: `MATURE_TOOL_GATEWAY_CANDIDATE`
- Status: `STANDBY_NOT_DEPLOYED`
- Verified date: 2026-09-21
- Default policy: 现有已付费/已成熟能力不迁移；新增、低频、临时、长尾外部 API 需求先查 Monid。

## 一句话定位
Monid = 一人公司体系的“统一外部工具/API 候选入口”，类似“OpenRouter 管模型，Monid 管工具”。

## 当前确认
1. 官方首页：1700+ 工具、55+ providers；GitHub README 当前写 2000+ / 72+ providers，目录持续变化。
2. 不要求月订阅；按实际 endpoint 调用计费。
3. `discover` 与 `inspect` 免费；执行 `run` 才产生余额消耗。
4. 新账号官方当前提供 $1 free credit。
5. 官方钱包充值由 Stripe 处理。
6. 官方公开文档未公开承诺 Monid 充值页必然支持微信支付、支付宝或 Apple Pay；具体显示方式应在登录后的 Stripe checkout 现实核验。
7. Apple Account / 美区 Apple ID 余额不等于 Apple Pay 卡片资金，不能把“Apple 账号余额”当成外部 Stripe 网页支付方式。
8. 另有 x402 路径：可用 USDC 按次链上支付执行调用，不用预充值 Monid 余额；Base / Monad mainnet 已在官方文档列出。x402 单次最低计费 floor 为 $0.01，但这不是普通钱包 top-up 最低充值额。

## 高性价比触发条件
出现任一条件时先查 Monid：
- 需要一个现有体系没有的 API；
- 某服务要求新订阅；
- 某能力只临时使用几次；
- 要同时访问多种搜索、社交、评论、企业/人员数据源；
- Playwright 正在做纯公开网页读取，可能可由更轻的 API 替代；
- 本地 GPU 路径明显慢，而云端按次成本很低；
- n8n 新增很多外部数据源；
- 某直接供应商失效，需要第二供应商快速切换。

## 不替换
默认不替换 GPT / DeepSeek / OpenRouter / JEV / Reasonix / Codex / Playwright / n8n / GitHub，以及已经付费且稳定的 API。

## 最低部署形态
当前无需全面部署。真正需要时采用四选一：
1. Agent Skill：`set up https://monid.ai/SKILL.md`
2. MCP：`https://mcp.monid.ai/v1`
3. CLI：`npm install -g @monid-ai/cli`
4. HTTP API：`https://api.monid.ai`

账号与 Key：
- Account/Dashboard: https://app.monid.ai
- API keys: https://app.monid.ai/access/api-keys

## 免费搜索候选
TinyFish 在 Monid connector 中当前声明为 FREE，可用于 live-web search / page fetch。使用前仍应通过 `inspect` 现实确认当前价格与 contract，避免把历史/缓存价格当永久事实。

## 充值与支付待现实核验
普通余额充值的官方公开文档只确认“Payments are processed via Stripe”。
- 银行卡：Stripe 支持银行卡，但是否某张卡能在 Monid 成功，应以 Monid checkout 现实显示/支付结果为准。
- Apple Pay：Stripe Checkout 支持 Apple Pay，但 Monid 页面是否显示，受 Monid merchant 设置、浏览器/设备、币种/地区等条件影响；不得先验写成 PASS。
- 支付宝 / 微信支付：Stripe 本身支持相应支付方式，但公开资料未证明 Monid 已启用；状态 = `PENDING_LIVE_CHECKOUT_VERIFY`。
- 普通钱包最低 top-up：公开官方页面未给出固定数字；第三方 OpenAPI 镜像只给出 `minAmount example: 5`，不得把 $5 当成已验证现行最低额。登录后通过钱包配置/充值页确认。

## 决策规则
`IF existing_mature_paid_path == true THEN KEEP`
`ELSE DISCOVER -> INSPECT -> compare(T_E2E,total_cost,reliability) -> RUN only if net-positive`

## 官方来源
- https://monid.ai/
- https://monid.ai/docs/guide/pricing
- https://monid.ai/docs/guide/quickstart-skill
- https://monid.ai/docs/guide/quickstart-mcp
- https://monid.ai/docs/api/wallet
- https://monid.ai/docs/guide/pay-with-x402
- https://github.com/monid-ai/monid

## 后续
第一次真实使用时再做一次轻量验收：
`ACCOUNT -> API_KEY -> FREE_DISCOVER -> FREE_INSPECT -> FREE/TINYFISH_RUN -> BALANCE_READBACK -> OPTIONAL_TOPUP_METHOD_CHECK`
没有真实需求时，不为“部署完成”而充值或迁移现有系统。
