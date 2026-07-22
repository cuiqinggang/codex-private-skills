# Governance

## 人工审批规则

必须人工审批的动作：

- 真实发送：微信、飞书、Telegram、邮件、短信、广告、支付、客户触达。
- 真实生产配置修改：Hermes、OpenClaw、小龙虾、New API 3011、Open WebUI 3000、ComfyUI、ECC。
- 真实密钥、token、cookie、账号、付款、权限、安全设置。
- 批量删除、批量覆盖、系统级安装或未知安装脚本。
- 把 WATCH/REPLAY 路线升级为真实接入。

## 审批门字段

- approval_id
- action_type
- target_system
- reason
- risk_level
- rollback_path
- evidence
- approver
- decision: approve / reject / request_changes
- decision_time

## 运行历史与复盘规则

每次运行必须记录：来源、检索关键词、候选、判断、证据、吸收/暂缓/放弃理由、影响文件、残余风险、下次检查内容。

## 密钥规则

- 只记录“是否需要 API key”，不记录 key 值。
- 不打印环境变量。
- 不读取 `.env`、生产配置、浏览器 cookie、token 文件。
- 只允许读取 `.env.example`、公开文档和 mock 配置。
