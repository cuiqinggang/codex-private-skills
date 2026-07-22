# Replay Method

## 昨日重现验证流程

1. 找到已经做出来的项目、产品、案例或失败分享。
2. 记录来源、时间、license、star/更新状态（能获取则填）。
3. 分析它解决的真实问题。
4. 判断逻辑是否成立：用户痛点、执行链路、治理边界、复盘能力。
5. 只在 mock/read-only/demo 模式验证。
6. 抽取可复用机制，写入 route evaluation 或 case study。
7. 映射到现有体系。
8. 形成吸收补丁：技能包规则、模板、控制台字段、watchlist 更新。
9. 复盘：保留证据、失败原因、下一步。

## Mock Replay 标准

- 输入必须是公开样例或人工构造假数据。
- 不读真实 token、密钥、cookie、生产配置。
- 不连接微信、飞书、Telegram、邮件、广告、支付或真实客户系统。
- 运行时间应短；长时间构建/下载立即停止并改为文档级验证。
- 输出必须能写入报告和复盘。

## Replay 记录字段

- route_id
- source_url
- local_source_path
- replay_type: read-only / mock / demo
- input_fixture
- expected_result
- actual_result
- evidence_path
- risks
- absorb_decision
- next_action
