---
name: shared-workspace-skill-index
version: "1.0.0"
description: 用户共同 GitHub 工作区、技能包、项目资料和跨智能体接手的统一定位索引。用于回答“资料在哪里”“某技能包在哪里”“换智能体后如何接续”“如何从 GitHub 找回全部已同步资产”。
---

# 共同工作区与技能包总索引 v1.0.0

## 唯一职责

让 GPT、Codex、Reasonix 或其他已获授权智能体，**用最少步骤从共同 GitHub 仓库找到用户已经同步的技能包、工作区、证据和项目资料**。

本技能不替代任何业务技能，也不复制每个项目的完整规则。

## 固定事实源

- 仓库：`cuiqinggang/codex-private-skills`
- Web：`https://github.com/cuiqinggang/codex-private-skills`
- Clone：`https://github.com/cuiqinggang/codex-private-skills.git`
- 可见性：Private
- 默认分支：`main`
- 根入口：`00_START_HERE/COMMON-ENTRY.md`
- 仓库规则：`AGENTS.md`
- 资产快照：`skills/shared-workspace-skill-index/INDEX.md`

## 必须先理解的边界

GitHub 是**已同步资产的长期共同事实源**，不是所有聊天、本机目录和历史工作的自动镜像。

因此：
- 仓库查到 = 可写 `REPOSITORY_VERIFIED`。
- 仅历史记忆/聊天提及 = 只能写 `HISTORICAL_REFERENCE_ONLY`。
- main 没有 ≠ 项目不存在；还要查相关分支。
- 分支存在但未合并 main = 明确标注分支来源。
- 本地副本仅是执行副本，不应覆盖远端事实。

## 最短读取协议

### A. 新智能体首次接手

1. 登录/连接 GitHub。
2. 打开 `cuiqinggang/codex-private-skills`。
3. 读 `00_START_HERE/COMMON-ENTRY.md`。
4. 读 `AGENTS.md`。
5. 读本技能 `SKILL.md`。
6. 根据任务搜索对应技能或项目。
7. 进入具体项目后，服从该项目自己的 `SKILL.md` / CURRENT / FREEZE / RESULT。

### B. 查一个技能

优先：
`skills/<skill-name>/SKILL.md`

找不到：
仓库关键词搜索 → 查看 main → 查看相关 `codex/*` 分支 → 确认 CURRENT/冻结文件。

### C. 查一个项目的全部资料

按顺序搜索：
1. `skills/`
2. `workspaces/`
3. `docs/`
4. 相关分支
5. 提交历史/冻结文件/RESULT

### D. 恢复访问

只恢复“访问通道”，不把任何秘密写入仓库。
- 使用用户已授权的 GitHub 连接或官方登录。
- 若用 GitHub CLI，可检查认证状态并重新登录。
- 权限恢复后重新读取远端。
- 禁止把 Token、Cookie、密码、SSH 私钥写入 SKILL、README、日志或索引。

## 其他智能体可直接使用的启动提示

“请连接我的 GitHub 私库 `cuiqinggang/codex-private-skills`，先读取 `00_START_HERE/COMMON-ENTRY.md`、`AGENTS.md` 和 `skills/shared-workspace-skill-index/SKILL.md`。然后按仓库实时内容搜索我要找的项目/技能。main 找不到时继续检查相关 `codex/*` 分支。任何资产只有在远端实际找到后才标为已保存。”

## 维护规则

- 新建长期技能：`skills/<skill-name>/`，入口为 `SKILL.md`。
- 长期项目证据：放入对应 `workspaces/` 或 `docs/`。
- 保存后远端回读确认。
- 不为同一资产随意创建多个“总索引”；本技能作为统一入口。
- 索引枚举会过期，实时仓库搜索永远高于静态清单。
