# EXP-PAYMENT-ROUTES-20261103-001｜三条成熟收款路线与E1—E4真实验收边界

版本：V1｜核查日期：2026-11-03（北京时间）｜类型：CASE + SKILL_CANDIDATE｜证据等级：官方产品资料的结构化研究，未有本人真实完整资金闭环

## 触发与环境
海外网站/AI服务已有真实站外客户，目标为合法收款并最终银行实收。把成熟服务操作流程与本人资格/真实到账分开，不对未核身份/主体/银行随意注册或试款。

## 成熟路径与适配边界
- A：Contra项目/发票→平台许可的银行渠道（跨地区银行需按官方支持路径核实）→本人香港银行；优先核身份及香港走廊，平台产品存在不代表个人获准。新客户项目托管、熟客发票是不同产品与费用。
- B：Upwork Direct Contracts→本人名下中国人民币银行终点；必须是合法站外且尚无Upwork账号的客户，提前核实实名、银行及税务，人民币不能冒充香港到账。
- C：已有真实香港独资或公司→Stripe香港对应主体商户→同名适配银行；不能以个人香港卡替代公司户名/商业登记；不存在已核实的无HKID无BRN个人直接提现捷径。

## LAST_GOOD / FIRST_DELTA / 纠正
LAST_GOOD：11月2日Stripe香港R1已有视频教程与资格冲突研究。
FIRST_DELTA：部分公开教程仅提供注册/身份画面，却被误读为E3客户付款与E4到账；R1抖音聚合页KYC失败自述作者归属不可确认，R2发现归属为相关视频区另一个作者。
纠正：按E1注册、E2身份与真实模式、E3真实付款、E4银行到账分级；公开教程和同源转载不重复算独立成功；保留R1原文字并指向R2纠错。尚无本人完整回归交易，不报业务PASS。

## 适用/不适用
适用：真实身份/实际居住/服务类型合规、平台资格和同名银行匹配；比较审核、客户付款、交付返修、清算、银行及失败恢复的完整T_VALID。
不适用：声称三条是使用人数最多、替本人开户/付费、将不同币种终点比较为同一合同、引用历史教程推翻现行官方资质。
当前VALID=RESEARCH_ONLY；本人E3/E4=NOT_VERIFIED；记忆完整T_VALID收益=NOT_MEASURED；主支付能力包V8.0及原Freeze不变。

## 直接来源
- [2026-11-03 R2完整路径与各平台官方出处](../../../research/global-payments/three-mature-routes-2026-11-03-r2.md)
- [2026-11-02 Stripe香港R1及纠错增量](../../../research/global-payments/stripe-hk-cross-platform-cases-2026-11-02.md)
- 这张卡不记录个人账号/证件/银行号码，也不自称真实收款或新规则晋升。

## 2026-11-04 R3 增量（来源仅为GitHub研究，C盘当日原日报尚未同步）
触发：目标限定为香港银行实际到账，比较Contra、Upwork、Stripe现有三路，尤其Upwork香港本地提现新候选。证据层级：2026-11-04 R3研究及Contra/Upwork官方产品说明；无本人账户页面、资格批准或到账回执。
LAST_GOOD：2026-11-03 R2已有三路资格/费用分类，Upwork原人民币终点独立备用。FIRST_DELTA：Upwork官方Direct to Local Bank地区表同时列China(CNY)和Hong Kong(HKB)；**支持地区列表并不证明某个现有账号可选香港银行**。更正：保留原CNY路线为不同终点，新增香港支线仅标CANDIDATE，优先只读已有账号Withdrawals的实际可选币种、地区及户名校验。
Contra官方说明：证件国家选签发地，跨证件与银行国家可按官方指引选择Airwallex；官方流程存在不等于本人的香港银行账户已获接入许可。Stripe香港Individual/独资/公司与银行账户主体必须匹配，不能由股东个人账户自动推断公司结算合格。熟客账单/新项目托管及客户发起/自由职业者发起Upwork Direct Contract的费用合同不能混用。
适用：合法合规资格只读核验、银行终点比较、避免重复开户与错误手续费预估；不适用：据此声称本人实名认证、香港账户绑定、E3客户付款或E4银行到账成功，或宣称T_VALID提速。结果：RESEARCH_ONLY；ACCOUNT_ELIGIBILITY=UNKNOWN；E3/E4=NOT_VERIFIED；T_VALID=NOT_MEASURED。新规则无晋升。
来源：[2026-11-04 R3研究](../../../research/global-payments/three-channels-hk-bank-endpoint-2026-11-04-r3.md)；[Upwork官方Direct to Local Bank](https://support.upwork.com/hc/en-us/articles/211063888-How-to-withdraw-earnings-with-Direct-to-Local-Bank)；[Contra官方跨国证件/银行指引](https://help.contra.com/en/articles/9322955-how-to-verify-your-identity-on-contra)。本条仅更新共享卡，原C盘11月4日日报未完成写入/回读。
