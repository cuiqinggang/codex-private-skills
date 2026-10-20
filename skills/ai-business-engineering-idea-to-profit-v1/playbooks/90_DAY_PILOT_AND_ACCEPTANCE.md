# 从想法到可验证收入：90天商业化试点与验收合同 V1

## 为什么优先选择视频B2B服务
用户已有短视频/媒体处理、Codex与自动化技能；历史Polsia节点产生过可验收的本地教育视频与内容运营包。最短验证路线不必先开发通用Lovable克隆，而是先找愿意付费的内容客户，用成熟工具实际交付，然后模板化，再按证据考虑SaaS。此为优先假设，不是已证实市场机会。

## 30天：问题与可交付价值
- 明确1个目标客户群（例如需要批量短视频规格转换/多语言字幕的机构或创作者），列3个竞品与替代方案、痛点及可量化交付。
- 通过获同意的真实客户访谈/询盘收集需求，记录拒绝与替代方案；模型虚构访谈不可计数。未经授权不自动外联。
- 用已有Codex/FFmpeg/模板做1个真正可运行的“客户输入→视频/文案/报价草案→样品交付→本地测试线索”流程，录入测试数据、质量回执和交付成本。
- 形成报价与退款政策草案、服务边界、可合法使用素材清单。未经授权不公开销售或收款。
- 验收：至少一个实际完成的样品、功能GOOD/BAD证据、真实访谈/询盘与成本记录；如没有付费证据，标PAYMENT_REAL=NOT_TESTED。
- 停损：客户明确无此痛点、交付权利不清、实际质量无法达标，则换更窄场景，不追加通用平台开发。

## 60天：最小收费验证
- 在获明确授权前提下，建立合规报价、线索记录、支付或人工开票/收款路径，生产支付与沙盒严格隔离。
- 尝试获得真实愿付费客户；保存客户同意、报价、订单、交付验收、退款和收款对账。若无真实成交，不能宣称盈利。
- 记录渠道曝光→真实线索→有效咨询→报价→付款→交付的漏斗；统计CAC/毛利，排除虚假点击、测试订单和自买单。
- 复用成熟CRM/支付/客服与现有任务Freeze，不另造通用营销平台。收集真实客户意见，比较至少两种定价假设。
- 验收：至少一次真实可归因的商业反馈（付款最好，但不保证）与质量/成本/退款记录；若没有订单，阶段结论仍为VALIDATION_INCOMPLETE，继续优化定位或转向。

## 90天：可复制与自动化经营
- 对重复需求沉淀标准输入、交付模板、质检、报价、客服FAQ、工时/算力账本。
- 只有出现重复付费与正贡献毛利的证据才评估订阅化/模板化SaaS；优先降低人工成本和交付时间，而不是盲目增加agent数量。
- 测试普通技术故障自动恢复、订单UNKNOWN不重复处理、隔离两项任务、GitHub Freeze回读、必要时人类审批。
- 验收：真实订单/客户反馈、渠道成本、重复交付质量、毛利、客户留存或复购（若观察期足够）；无足够样本不推断长期LTV。
- 失败转向：CAC长期大于可实现毛利、客户不复购、退款高、模型/人工成本失控，暂停扩量，回到市场验证。

## 最小商业合同模板
TASK_ID=NEW_UNIQUE_ID
METHOD_REF=当前正式三人行方法（旧任务保留锁定）
SKILL_REF=skills/ai-business-engineering-idea-to-profit-v1/SKILL.md@1.0.0
TARGET_CUSTOMER=...
PAIN_EVIDENCE=...
ALTERNATIVES=...
VALUE_PROPOSITION=...
PRICE_HYPOTHESIS=...
DELIVERABLE=...
DONE_WHEN=真实可运行服务/产品及经授权商业测试
FORBIDDEN=无授权广告、外联、生产支付、发布、采集个人数据
COST_CAP=...
DATA_PRIVACY=...
SUCCESS_METRICS=质量、真实线索、订单、退款、毛利、净利润
BASELINE=...
T_VALID_REAL=UNKNOWN
FINANCIAL_REALITY=NOT_TESTED
OWNER=GPT_CEO
EXECUTOR=CODEx_ON_DEMAND
STATE=PLANNED
NEXT=...

## 真实经营数据表字段
event_id, task_id, customer_ref_pseudonymous, timestamp_utc, channel, source_campaign, event_type, test_or_real, order_id, amount, currency, refund, direct_delivery_cost, acquisition_cost, model_cost, hosting_cost, other_cost, evidence_ref, approval_ref, idempotency_key, reviewer, status。
只保存合规所需的最少个人数据，隐去密钥和敏感身份信息。财务报表以真实交易/会计凭证为准；演示模拟另表，不能混算。

## 节点质量/权限验收
PASS_REAL需实际可回读业务成果+原始日志/回执+质量检查+授权证据；PARTIAL只证明部分功能；NOT_TESTED没有现实动作；UNKNOWN缺少关键回执；FAIL_REAL有失败证据。每自然节点冻结NODE_ID、版本、结果、SHA、已完成/未完成、GOOD/BAD/FIRST_DELTA、NEXT、FINAL_VALID。旧Polsia或Lovable母任务状态不可被本新试点覆盖。

## 三个反例测试
1. 产品功能完美但没人付钱：产品工程PASS、商业化FAIL/UNKNOWN，不宣称从想法到利润。
2. 有收入但CAC/履约/退款高于收入：收入PASS、净利润FAIL。
3. 广告/支付工具返回超时：核实远端真实回执后才重试，避免重复花钱、重复扣款或外发。

## 核心KPI及其使用
有效需求证据数、样品验收率、获授权发布数、独立访客、合规线索、MQL/SQL、成交率、客单价、净收入、退款率、每单履约成本、CAC、贡献毛利、净利润、留存、复购、LTV/CAC（仅在足够观察数据时）、故障恢复率、重复副作用数、完整T_VALID。
**不能用估值、注册数、生成网站数、模型响应速度或宣传“1/3赚钱”代替这些指标。**