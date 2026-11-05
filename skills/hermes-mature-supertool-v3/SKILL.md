---
name: hermes-mature-supertool-v3
description: "使用 Hermes SuperTool V3.0。处理 Windows 本机安装与修复、Flash 1017 执行、Hermes 网页接单和原生浏览器操作、ECC 3.1.1 验收，以及经获准入口委派 GPT 网页服务。"
---

# Hermes SuperTool V3.0.0

先读 [当前状态与实跑回执](references/CURRENT.md)，安装、排障或验收时查 [操作手册](references/OPERATIONS.md)。Windows 本机软件的实测版本为 Hermes v0.22.7。

- Windows 按执行桥 V13.0.6 的 D→A→B→C，使用当前已验证的新编号。提交结果不明确时先对账。
- GPT 定义目标、冻结合同并独立验收。Hermes 正式执行使用 DeepSeek V4.1 Flash 1017，沿用正式 CLI、Dashboard、原生委派和会话续接。
- 分开验 Hermes 在自己网页接单、Hermes 原生浏览器操作测试网站，以及 Hermes 向指定 ChatGPT 网页派单并读回。每条路径记录真实回执。
- ECC 使用固定的 3.1.1 源码。引擎测试、冷恢复、四角色产物与实际写入边界分别验收。主会话和审计的临时操作也纳入检查。
- 按《三人行》第5版和《轻量状态持久化 V3》保存必要检查点。确实需要独立宿主时才用现有 n8n，记录接收与执行 ID。
- 安装沿革、原备份和历史测试查 [V2.2.1 回执](../hermes-mature-supertool-v2-2/references/CURRENT.md)。旧等权 7/10 保留作历史。
