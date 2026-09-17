# REMOTE SHARED WORKSPACE（远端共同工作区）

> 本文件定义 `Shared Workspace（共同工作区）`、`Shared Fact Source（共同事实源）` 与 `Local Execution Checkout（本地执行副本）` 的唯一含义。

## 1. 共同工作区的唯一定义

`SHARED_WORKSPACE（共同工作区）` 必须是多个执行者都可以通过网络读取、版本化、同步和核验的**远端在线权威空间**。

典型形式：

- GitHub / GitLab / Gitea 等远端 Git 仓库；
- 组织级在线文档/对象存储/制品仓库；
- 其他具备远端持久化、版本或可审计历史的在线工作区。

硬规则：

```text
SHARED_WORKSPACE_IS_REMOTE=YES（共同工作区必须是远端在线空间）
LOCAL_PATH_IS_SHARED_WORKSPACE=NO（本地路径绝不等于共同工作区）
```

任何 `C:\...`、`D:\...`、`/home/...`、本机 worktree（工作树）、clone（克隆）目录，都只能叫：

```text
LOCAL_EXECUTION_CHECKOUT（本地执行副本 / 本地检出副本）
```

不得称为“共同工作区”“共同事实源”或“共享仓库真源”。

---

## 2. 共同事实源

如果本项目使用远端 Git 仓库作为事实源：

```text
SHARED_FACT_SOURCE（共同事实源）
= REMOTE_REPOSITORY（远端仓库）
+ REMOTE_BRANCH / TAG / COMMIT（远端分支 / 标签 / 提交）
+ PROJECT_PATH（项目路径）
```

只有经过远端核验的内容才成为正式共同事实。

本机文件即使已经生成、测试通过、提交到本地 Git，也仍然只是：

```text
LOCAL_RESULT（本机结果）
```

直到完成：

```text
LOCAL RESULT（本机结果）
→ FORMAL REPORT（正式报告）
→ LOCAL COMMIT（本地提交）
→ PUSH（推送到远端）
→ REMOTE VERIFY（远端核验）
```

才允许：

```text
SHARED_FACT_CONFIRMED=YES（共同事实已确认）
```

---

## 3. 项目级共同工作区，不是全局固定仓库

共同工作区是**项目级配置**，不是本技能包的全局固定路径。

每个新项目必须显式声明：

```text
PROJECT_ID（项目ID）
SHARED_WORKSPACE_TYPE（共同工作区类型）
SHARED_WORKSPACE_REMOTE（远端共同工作区标识）
SHARED_WORKSPACE_BRANCH（远端工作分支，如适用）
SHARED_WORKSPACE_PROJECT_PATH（项目路径，如适用）
LOCAL_EXECUTION_CHECKOUT（本地执行副本，可选）
REMOTE_VERIFY_REQUIRED=YES（必须远端核验）
```

例如，H3-P0 当前项目：

```text
PROJECT_ID=H3-P0
SHARED_WORKSPACE_TYPE=GITHUB
SHARED_WORKSPACE_REMOTE=cuiqinggang/codex-private-skills
SHARED_WORKSPACE_BRANCH=codex/h3-p0-mature-convergence-v2
LOCAL_EXECUTION_CHECKOUT=C:\Users\A\Documents\Codex\codex-private-skills
```

这里：

- `cuiqinggang/codex-private-skills` 才是共同工作区；
- `C:\Users\A\Documents\Codex\codex-private-skills` 只是这台电脑上的本地执行副本。

未来做其他项目时，可以声明另一套远端共同工作区；不得默认继续使用 H3-P0 的仓库。

---

## 4. 读取规则

新任务开始时：

1. 先确定本项目的 `SHARED_WORKSPACE_REMOTE（远端共同工作区）`；
2. 优先读取远端已核验的任务文件、阶段报告、经验先验和 Failure Index（失败索引）；
3. 本机需要执行代码时，再把远端内容 fetch / pull / checkout 到 `LOCAL_EXECUTION_CHECKOUT（本地执行副本）`；
4. 本地副本必须与目标远端 branch / commit 对齐；
5. 若本地副本存在其他任务的未提交修改，保护这些修改，必要时使用安全 worktree（工作树），不得覆盖。

禁止因为本地找不到文件就大范围扫描磁盘来替代远端事实源定位。

如果远端任务文件已经明确存在，正确顺序是：

```text
REMOTE LOCATE（远端定位）
→ FETCH（拉取）
→ LOCAL CHECKOUT（本地检出）
→ EXECUTE（执行）
```

而不是：

```text
RECURSIVE LOCAL SEARCH（本地递归全盘搜索）
→ 猜测哪个目录可能是共同工作区
```

---

## 5. 写回规则

所有产生新的工程事实的任务都必须：

```text
LOCAL EXECUTION（本机执行）
→ EVIDENCE（证据）
→ FORMAL REPORT（正式报告）
→ EXACT STAGE（精确暂存）
→ COMMIT（提交）
→ PUSH TO SHARED_WORKSPACE_REMOTE（推送远端共同工作区）
→ REMOTE VERIFY（远端核验）
```

只有远端核验成功后，才允许宣布：

```text
STAGE_COMPLETE=YES（阶段完成）
FREEZE=YES（冻结完成）
99=YES（99完成）
```

如果网络暂时不可用，可以保留本地结果，但状态必须是：

```text
REMOTE_SYNC_PENDING=YES（远端同步待完成）
```

不得把本地未同步状态描述为共同工作区已完成。

---

## 6. 命名纪律

必须使用：

- `SHARED_WORKSPACE（共同工作区）`：远端在线权威空间；
- `SHARED_FACT_SOURCE（共同事实源）`：远端权威事实位置；
- `REMOTE_REPOSITORY（远端仓库）`：具体在线 Git 仓库；
- `LOCAL_EXECUTION_CHECKOUT（本地执行副本）`：执行器本机 clone / worktree；
- `LOCAL_EVIDENCE_ROOT（本机证据目录）`：大文件、日志、视频等本机证据；
- `REMOTE_VERIFY（远端核验）`：确认远端 branch / commit / file 已包含新事实。

禁止使用：

```text
共同工作区 = C:\某目录
共同仓库 = 本机clone目录
共同事实源 = 本机文件夹
```

---

## 一句话

> **共同工作区永远是远端在线权威空间；本机目录永远只是执行副本。每个项目显式声明自己的远端共同工作区，H3-P0 当前使用 `cuiqinggang/codex-private-skills`，其他项目可以使用完全不同的远端仓库。所有新工程事实只有 push 并 remote verify（远端核验）后，才成为正式共同事实。**
