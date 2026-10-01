# 共同工作区统一入口

更新时间：2026-10-01

## 1. 唯一需要记住的入口

- 共同私有 GitHub 仓库：`cuiqinggang/codex-private-skills`
- Web：`https://github.com/cuiqinggang/codex-private-skills`
- Clone：`https://github.com/cuiqinggang/codex-private-skills.git`
- 默认分支：`main`
- 技能总目录：`skills/`
- 项目工作区：`workspaces/`
- 项目/证据/命令资料：`docs/`
- 智能体读取规则：`AGENTS.md`
- 总索引技能：`skills/shared-workspace-skill-index/SKILL.md`

> 本仓库是已经同步资产的共同事实源；“过去做过”不自动等于“已同步到 main”。查找项目时必须同时检查 main、相关分支和仓库搜索结果，不得凭聊天记忆宣称文件已经存在。

## 2. 当前重点项目

当前“极限短时间自动化闭环”正式版本：

- `workspaces/extreme-time-automation-loop-v1.2/README.md`
- `workspaces/extreme-time-automation-loop-v1.2/SUMMARY.md`
- `workspaces/extreme-time-automation-loop-v1.2/REALITY_CONTRACT.md`

当前普适方法基线：

- `skills/extreme-time-agent-constitution/SKILL.md`
- `skills/extreme-time-agent-constitution/CONSTITUTION.md`
- Freeze ID: `ETAC-v0.2-FREEZE-R1`

原 `workspaces/jarvis-v1/` 为历史来源，不再代表当前项目定义。

## 3. 新智能体最短接手顺序

1. 确认已登录 GitHub，并对私库 `cuiqinggang/codex-private-skills` 有读取权限。
2. 读取本文件。
3. 读取根目录 `AGENTS.md`。
4. 读取 `skills/shared-workspace-skill-index/SKILL.md`。
5. 按任务名/技能名在 `skills/`、`workspaces/`、`docs/` 搜索。
6. main 找不到时，搜索相关 `codex/*` 分支；不要扫描用户本机替代远端事实源，除非远端不可用或用户明确要求。
7. 找到技能后，以该技能自己的 `SKILL.md`、CURRENT、FREEZE、RESULT 等文件为该项目的具体事实依据。

## 4. 认证与安全

- 私库需要用户自己的 GitHub 账号/已授权连接；仓库不保存密码、Token、Cookie、SSH 私钥。
- 可以记录“如何认证”和“认证状态”，不得把秘密凭据写入仓库。
- 登录失效时使用 GitHub 官方登录/已授权连接恢复；恢复后重新读取远端内容。
- 不擅自改变仓库可见性，不 force push。

## 5. 重要说明

`main` 是共同默认入口，但一些新项目、冻结候选或现实认证可能仍位于专用分支中。总索引负责“找到资产”，项目自身文件负责“解释资产”。
