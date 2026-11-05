# V3.0.0 当前状态与实跑回执

北京时间 2026-11-05。能力包 V3.0.0 继承 V2.2.1。Windows 本机软件 Hermes v0.22.7，正式模型 `deepseek/deepseek-v4.1-flash-20261017`，活动 Profile 为 `default`。已测范围可用，完整功能与长期可靠性认证仍有缺口。

| 功能 | 状态 | 实测回执 |
|---|---|---|
| 简单任务 | 通过 | 未给答案的去重、排序、求和题正确，`00:40:671` |
| 复杂任务 | 通过 | 订单结算代码与报表，独立测试 8/8，3 笔合计 201 分，冻结需求、输入与测试哈希一致，`03:09:682` |
| Hermes 原生浏览器 | 通过 | `browser_exec` 打开测试页、填表、选择、勾选、提交并读回。服务端收到一次有效 POST，回执相符。首轮只指定 browser 工具集失败，使用正式工具集复验 `00:34:426` |
| Dashboard 网页终端接单 | 通过 | 本机 `http://127.0.0.1:9119/chat` 真实提交算题，网页显示 Flash 1017 并返回 `HQA-UI-491\|75` |
| Hermes Webapp 图形聊天 | 通过 | 官方前端构建后在 `127.0.0.1:9120` 运行。沿用专用 Chrome，完成一次性登录。在 `default` 的新会话输入、发送中文，Flash 1017 返回 `GUI-117\|121` |
| 鼠标语音输入 | 用户实机反馈 | 图形消息框可用，Dashboard 网页终端无法输入。原生 PowerShell 终端的鼠标语音未单测 |
| 同一会话续接 | 通过 | 另一 CLI 进程按原会话 ID 读回检查点，`00:07:785` |
| 网关进程级恢复 | 历史实测通过 | 健康检查自动拉起 v0.22.7，HTTP 恢复 `00:36:467`，随后 WebSocket RPC 和真实对话通过 |
| ECC 3.1.1 引擎与冷恢复 | 限定范围通过 | 固定提交的隔离副本运行 131 项，130 通过、1 跳过。测试进程仅适配 `tasklist` 的原生解码。Hermes 实际调用 `fresh_resume.py --selftest`，结果 PASS |
| ECC 严格四角色 | 未通过 | 资料和执行子代理完成，业务产物由执行子代理写入，独立会话审计复验通过。主会话和审计在约定目录外写了临时验算脚本，已归回测试目录 |
| Hermes 委派指定 ChatGPT 网页并读回 | 受限，未实测 | ChatGPT Work 的 Browser 扩展入口在站点权限检查时拒绝控制 chatgpt.com。该入口未提交网页请求。Hermes 原生工具已在受控测试网页通过 |
| 整机重启与长期稳定性 | 未测 | 整机重启后无人值守接单和续跑、长期稳定性、同合同多样本与真实账单仍待验收 |

2026-11-05 图形入口启用记录：校验配置备份，构建官方前端，启用 Webapp，确认网关空闲后平滑重启。`8642/health` 返回 200，`9120` 在本机回环监听并返回 200。在原有专用 Chrome 完成登录与实际收发。命令行和图形版的同题端到端耗时尚未对照测量。

计时采用表中各阶段或成功样本。下次严格 ECC 复验，把主控和审计的权限设为只读，执行写入限制在约定目录，再用同一订单合同核对实际写入轨迹。指定 ChatGPT 网页待平台许可的入口可用后，单独实测 Hermes 发单、等待和读回。

[ECC 3.1.1 权威入口](https://github.com/cuiqinggang/codex-private-skills/blob/main/skills/artificial-single-page-extreme-time-engine/ECC_V3_1_1_NETWORK_AUTHORITY.md) · [Hermes 历史多代理回执](https://github.com/cuiqinggang/codex-private-skills/blob/main/workspaces/hermes-maturity-20261014/F008_DELEGATION_REALITY_20261015.md)
