---
name: hermes-mature-supertool-v2-1
description: "接续 Hermes 成熟态 SuperTool V2.1。用于 Hermes 稳定版升级、D 通道复验、网关恢复、模型与角色路由、复杂修复、会话接续和超级执行体差距核验。GPT 负责决策、冻结和独立验收，Hermes 负责执行。"
---

# Hermes 成熟态 SuperTool V2.1.0

这是 V2.0 冻结包的接续版本。升级、恢复或补验前先读 [当前状态](references/CURRENT.json) 和 [升级回执与验收手册](references/UPGRADE-AND-GATES-20261105.md)。Windows 本机的 V2.0 专项资产仍按需复用，原目录为 `C:/Users/A/.hermes/skills/hermes-mature-supertool`。旧冻结任务按其原合同接续。

## 分工与入口

- GPT 作为超级大脑，定义任务、比较成熟路线、冻结权限和验收合同、独立验收及决定发布。Hermes 通过既有工具和模型执行，保留产物、回执、检查点和可接续状态。
- GPT 到 Windows 使用 D 通道优先。Hermes 日常任务走现有正式 CLI。实际聊天或角色切换才使用现有网页入口。仅在合同明确要求 API 接单时使用原生 Runs API。
- 沿用 V2.0 的虚拟成熟 → Freeze（冻结）→ 一次整体 Reality（实跑）→ 独立验收。优先复用已有正式 CLI、Repair Loop（修复闭环）、原生委派、接续和验收器。运行时的首次失败、修复、重试和最终读回均计入完整有效交付时间。
- 升级后先核对实际运行版本、监听进程、依赖和 WebSocket RPC（对话连接），再执行一次带唯一标记的真实对话。端口 HTTP 200 只记健康接口通过。角色必须按各自 Profile（独立配置档）实际发起并核对模型回执。
- 优先补现有可见网页的真实操作，再关闭角色认证差距。先取得独立角色授权和回执，再验跨角色委派。整机重启、重复复杂任务和持续观察各自验收。

## 当前发布边界

技能包版本为 V2.1.0，Windows Hermes 软件版本为 v0.22.7。2026-11-05 的固定基线为 7/10，整站超级执行体认证待完成。维护时更新新回执，保留历史测量、失败与冻结快照。保持各 Profile 凭据隔离。
