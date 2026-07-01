# Runbook

## 一次标准运行

1. 明确运行类型：initial / light / weekly / monthly / case-study。
2. 加载 `WATCHLIST.md`、`ROUTE-MATRIX.md`、`CASES.md`、`SOURCE-OF-TRUTH-MAP.md`。
3. 搜索或读取来源，只使用官方 docs、公开 repo、raw README、论文/社区公开分享。
4. 记录候选：名称、URL、开源/闭源、license、star/更新时间（能获取则填）、核心机制、风险、是否需要 mock。
5. 判断动作：ABSORB / REPLAY / WATCH / REJECT / DEPRECATED。
6. 对 REPLAY 路线只做 mock/read-only/demo。
7. 抽取机制并映射到现有体系。
8. 更新矩阵、watchlist、cases、source map、changelog。
9. 写运行报告。
10. 同步关键索引到 `H:\AI\skills\ai-company-evolving-revenue-portfolio`。

## 定期运行提醒

本技能包建议每 2 天运行一次轻量更新；每 7 天运行一次周复盘；每 30 天运行一次路线矩阵重评估。

不要自动创建 Windows 计划任务，除非用户明确要求。

## 停止条件

- 需要真实 API key、账号登录、付款、发送、广告投放或客户触达。
- 需要修改 Hermes、OpenClaw、小龙虾、New API 3011、Open WebUI 3000、ComfyUI、ECC 生产配置。
- 需要运行未知安装脚本、`curl | bash`、批量删除或系统安全设置修改。
- GitHub 限流且无法用 raw/clone/zip 继续获取公开证据。

## 成功条件

- 有来源和证据。
- 有吸收/暂缓/放弃理由。
- 有本地体系映射。
- 有更新报告。
- 没有读取或泄露密钥。
- 没有真实发送或生产配置修改。
