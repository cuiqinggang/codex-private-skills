---
name: hermes-mature-supertool-v2-2
description: "使用 Hermes SuperTool V2.2 双模型执行链。用于 Windows D 优先执行、DeepSeek V4.1 Flash 1017 代码与工具任务、GPT 网页审核与多模态、网关恢复、会话接续和整体验收。"
---

# Hermes SuperTool V2.2.0 双模型执行链

开工先读 [当前状态与回执](references/CURRENT.md)。Hermes v0.22.7 使用唯一正式执行模型 `deepseek/deepseek-v4.1-flash-20261017`，沿用已有 OpenRouter 配置、正式 CLI 和原生接续。GPT 负责定目标、独立审核及决策。图片、视频理解和绘图使用现有已登录的 ChatGPT 网页。

- Windows 严格按 V13.0.6 的 D→A→B→C，本次 D 为 Windows D 20261105-01。重连只验证本次新编号。保留已通过的节点，写入结果未知时先只读对账。
- 使用《三人行》第5版与《轻量状态持久化 V3》。完成当前对话能闭合的步骤；只有确实需要独立宿主时，向现有 n8n 交付一次并记录执行 ID。
- 常规辅助任务继承正式会话模型。委派走同一 1017 路线。审核以外部测试、业务产物、模型回执和会话 ID 为准。
- 网关恢复先核对进程、HTTP、WebSocket，再验证真实对话。跨 CLI 进程续跑、网关重启和整机重启分别记证据。
- 浏览器平台阻止自动控制时，记录自动化阻塞与手工验收待办。保留网页登录会话，交由用户在指定网页操作。
- V2.1.0 的 7/10 为旧合同历史。四个旧 Profile 已归档，旧模型直连、Dashboard 角色切换、额外 Open WebUI 对话和跨模型委派退出当前合同。原 V2.0、V2.1 证据按需查阅。
