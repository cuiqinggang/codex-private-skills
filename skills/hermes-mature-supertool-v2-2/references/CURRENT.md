# 双模型执行链当前状态

北京时间 2026-11-05。任务 `HERMES-DUAL-1017-20261105`。Hermes 运行版本 v0.22.7。状态为本机执行链通过、指定 GPT 网页实测待验。历史 V2.1.0 的 7/10 按旧合同保留。

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

## 剩余门禁

1. 现有 ChatGPT 标签可见，平台阻止自动控制 chatgpt.com。网页实聊、独立审核、图片识别、视频理解和绘图均待指定网页的实际证据。可由用户在原已登录标签使用非敏感图片和短视频实测，核对实际回复与生成图片。视频附件受账号、平台和上传方式影响，按实际接收情况登记。
2. 整机重启后的无人值守接单与续跑仍需独立实测。现有证据覆盖网关进程自动拉起和会话跨 CLI 进程接续。
3. 正式超级执行体认证还需同合同的重复复杂任务、长期稳定性和实际成本记录。优先复用此轮 F019 与现有验收器。

NEXT_ACTION 为用户在已打开的 GPT 网页完成一次多模态手动验收并回传结果。交接保留本机事务及验收回执，无独立 n8n 待执行工作。

参考 [旧 V2.1.0 实测回执](https://github.com/cuiqinggang/codex-private-skills/blob/main/skills/hermes-mature-supertool-v2-1/references/UPGRADE-AND-GATES-20261105.md)、[Flash 1017 模型页](https://openrouter.ai/deepseek/deepseek-v4.1-flash-20261017) 与 [ChatGPT 图像及视频附件说明](https://help.openai.com/en/articles/8400551-chatgpt-image-inputs-faq)。
