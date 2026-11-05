# EXP-EVENT-PILOT-20261105-001｜10美元活动后台单：先查可提现再投标

版本：V1｜核查日期：2026-11-05（北京时间）｜类型：CASE + ERROR + SKILL_CANDIDATE｜证据：原商业分支V1.1 R3项目报告；真实客户/资金闭环未发生

## 触发/合同
目标是给已有主办方的一场活动提供后台报名验证服务，固定报价USD10。客户负责主持、场次、实际收款退款；服务方仅在获授权系统核对报名、确认通知、时区、入场链接和提醒，提交脱敏验收记录。

## LAST_GOOD→FIRST_DELTA→最小调整→回归
LAST_GOOD：成熟Upwork固定价合同与本地报名表基础测试路线存在。
FIRST_DELTA：真实Upwork本人账号状态、地区/税务/身份审核、Connects、合同费率、提现方式与最低提现额没有原始账户资格证据；USD10的名义报价不必然可结算到银行。
最小调整：P0先只读核账户合法实名、可提交投标、同名出款渠道和最低可提现额度，计算实际费用后再决定是否报价；P1客户明确同意并资助合同后才进入P2真实平台报名测试，最终银行实收为P3。
回归：R3只有本地回环HTML合成测试8/8，2条合成报名、0封真实邮件、0笔合同/付款/银行到账；约50ms只属于本地合成测试，不包含找客户、审批、提醒真实送达、提交/付款安全期与提现。真实业务E2E=NOT_TESTED。

适用：已有一场真实排期、负责人/主持、工具权限和同意测试的客户，一次性后台QA；可把本地合成测试做先验质量门。
不适用：宣称已有人付款、稳定10美元收益、把150美元整单预算当本次小单定价、未经授权投标/花费Connects、承担活动主持/参加者账务、拿本地50ms当有效交付时间。无可靠同合同全链T_VALID对照，NOT_MEASURED。
与会员社群业务不同合同，不将前者免费到场推断为本方服务费到账；未观察到共享EXP实际采用回执。

## 来源
- [活动后台付费首单V1.1 R3](../../chi-yu-xing-dadao-zhijian-interest-law/references/event-backoffice-paid-pilot-v1.1-r3.md)（提交86e8224d、eb98dad046b9）
- [现有Upwork官方固定价合同与付款](https://support.upwork.com/hc/en-us/articles/211063718-How-payments-for-milestones-and-fixed-price-contracts-work)
- [Upwork官方本地提现](https://support.upwork.com/hc/en-us/articles/211063888-How-to-withdraw-earnings-with-Direct-to-Local-Bank)
