# 双模型执行链当前状态

北京时间 2026-11-05。任务 `HERMES-DUAL-1017-20261105`。技能包 V2.2.1，Hermes 运行版本 v0.22.7。本机执行链通过，Hermes 委派 GPT 网页并读回的闭环受平台限制。历史 V2.1.0 的 7/10 按旧合同保留。

## 已实施并读回

- 现有 OpenRouter 先实调 `deepseek/deepseek-v4.1-flash-20261017`，核对模型回执后，切换 Windows Hermes 默认入口和正式 CLI 包装器。
- 12 个文本辅助任务继承主会话，普通委派绑定 1017。停用 4 个 Hermes 媒体工具组和旧 Telegram 模型路由插件，清除 4 个额外 API 别名。活动 Profile 仅余 `default`。
- 原四个独立 Profile 移至本机 `C:/Users/A/.hermes/backups/hermes-dual-1017-20261105/profiles`，原配置与包装器保留校验过的同目录备份。原始 Profile 包含会话和配置，回退时沿该次事务回执复原。
- 开头按用户当时的 A→B→C 用 A 实调，用户随后指定 D→A→B→C。新 D 入口验收后，变更和复验全部通过该入口。

## 真实验收

| 门禁 | 实证 |
|---|---|
| 网关 | 官方停机后现有健康检查自动拉起 v0.22.7，新进程 HTTP 恢复 `00:36:467`，随后 WebSocket RPC 通过 |
| 正式执行 | 退款修复复用原 F019 合同。独立测试从失败修到 23/23，原需求和测试文件哈希一致。包装器实际模型回执为 Flash 1017 |
| 原生委派 | 同一个测试会话的导出记录包含一次 delegate_task 调用、两个子任务和对应工具回执 |
| 原生续接 | 另一 CLI 进程按原会话 ID 读回约定检查点，耗时 `00:09:626` |
| 单样本交付时间 | 准备隔离副本到独立判分 `02:10:536`，到同会话续跑完成 `02:20:266`。正式修复回执估算 USD 0.049925616，实际账单与同合同重复对照待测 |

## Hermes 委派 GPT 网页的验收合同

1. 由 Hermes 接单，记录 `TASK_ID`、`WORK_ITEM_ID`、验收条件及唯一标记。通过获准的智能浏览器在指定的已登录 ChatGPT 网页实际提交一份无敏感内容的测试任务。
2. 在原会话等待可核对的完成信号，由 Hermes 读回回复或生成物，独立核对任务标记和验收条件，再把结果与回执交付。回执保留脱敏会话标识、提交次数、完成状态、产物和从接单到读回校验的耗时。
3. 超时或断线后，提交状态不明时标记 `UNKNOWN`，先在获准入口对账原会话。确认原提交未发生且不会迟到时才允许有界重试。
4. 人工发单和读取用于网页能力诊断。上一轮观察到 ChatGPT 标签，但平台禁止自动控制 chatgpt.com，`HERMES_GPT_WEB_E2E=BLOCKED_BY_PLATFORM`。当前证据中 Hermes 未提交网页任务，也没有可交付的读回结果。独立审核、图片、视频和绘图按相同闭环分别验收。

## 其他剩余门禁


1. 整机重启后的无人值守接单与续跑仍需独立实测。现有证据覆盖网关进程自动拉起和会话跨 CLI 进程接续。
2. 正式超级执行体认证还需同合同的重复复杂任务、长期稳定性和实际成本记录。优先复用此轮 F019 与现有验收器。

NEXT_ACTION 为在平台允许控制指定 ChatGPT 网页的入口上，由 Hermes 执行一次带唯一标记的端到端验收。保留本机事务及验收回执，当前无可移交 n8n 的网页执行任务。

参考 [旧 V2.1.0 实测回执](https://github.com/cuiqinggang/codex-private-skills/blob/main/skills/hermes-mature-supertool-v2-1/references/UPGRADE-AND-GATES-20261105.md)、[Flash 1017 模型页](https://openrouter.ai/deepseek/deepseek-v4.1-flash-20261017) 与 [ChatGPT 图像及视频附件说明](https://help.openai.com/en/articles/8400551-chatgpt-image-inputs-faq)。
