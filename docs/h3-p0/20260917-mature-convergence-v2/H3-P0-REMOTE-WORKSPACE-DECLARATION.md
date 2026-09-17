# H3-P0 远端共同工作区声明

状态：ACTIVE（当前有效）

## 0. 当前母技能身份门禁

H3-P0 当前方法规则只引用独立 canonical 母技能：

```text
CANONICAL_MOTHER_SKILL_ID=first-principles-physical-limit-convergence
REQUIRED_SKILL_VERSION=1.8.0
CANONICAL_SKILL_REMOTE=cuiqinggang/codex-private-skills
CANONICAL_SKILL_BRANCH=codex/first-principles-physical-limit-convergence-v1.8.0
CANONICAL_SKILL_PATH=skills/first-principles-physical-limit-convergence/
```

H3 项目分支中历史快照 `skills/first-principles-physical-limit-convergence/VERSION=1.0.0` 不是当前运行规则源，不得覆盖 canonical v1.8.0。

旧 `absolute-time-fireworks-optimization` 是历史祖先/兼容资产，不是当前母技能，不是当前升级目标。

正式 GPU/性能执行前必须：

```text
CANONICAL_IDENTITY_GATE=PASS
SKILL_VERSION_VERIFIED=1.8.0
NO_FREE_EXPLORATION=YES
GPT_COMPLETE_VALIDATION_RAILROAD_PRESENT=YES
```

任何一项不满足：`NO GPU RUN / RETURN TO GPT`。

## 1. 项目级工作区声明

```text
PROJECT_ID（项目ID）= H3-P0
SHARED_WORKSPACE_TYPE（共同工作区类型）= GitHub
SHARED_WORKSPACE_REMOTE（远端共同工作区）= cuiqinggang/codex-private-skills
SHARED_WORKSPACE_BRANCH（远端工作分支）= codex/h3-p0-mature-convergence-v2
SHARED_WORKSPACE_PROJECT_PATH（远端项目路径）= docs/h3-p0/20260917-mature-convergence-v2
REMOTE_VERIFY_REQUIRED（必须远端核验）= YES
```

本项目的“共同工作区”“共同事实源”均指 GitHub 上的远端仓库/分支/项目路径。

## 2. 本地目录的唯一定义

当前这台 Windows 机器可能存在：

```text
LOCAL_EXECUTION_CHECKOUT（本地执行副本）
= C:\Users\A\Documents\Codex\codex-private-skills
```

以及：

```text
LOCAL_EVIDENCE_ROOT（本机证据目录）
= C:\AI\H3-P0-Acceptance\...
```

这两个位置都不是共同工作区。

硬规则：

```text
LOCAL_EXECUTION_CHECKOUT != SHARED_WORKSPACE
LOCAL_EVIDENCE_ROOT != SHARED_WORKSPACE
```

本地执行副本只用于 Codex 在本机读取、修改、运行和提交；本机证据目录用于保存大日志、视频、运行产物等。

## 3. 正确读取顺序

Codex / 执行器启动 H3-P0 任务时：

```text
1. 先确认 canonical 母技能 v1.8.0 远端身份
2. 读取 canonical SKILL.md + CANONICAL-IDENTITY-GATE + NO-FREE-EXPLORATION-GATE
3. 确认 H3-P0 远端仓库 cuiqinggang/codex-private-skills
4. 确认远端分支 codex/h3-p0-mature-convergence-v2
5. 从远端读取本文件、当前虚拟99包和 GPT 当前验证铁路
6. 再定位/使用本机已有 clone 作为 LOCAL_EXECUTION_CHECKOUT
7. fetch / pull / checkout 到目标远端状态
8. 只执行 GPT 已授权铁路
```

禁止：

```text
先递归扫描 C:\AI / C:\Users\... 来猜“共同工作区”在哪里
或读取项目分支旧 v1.0.0 skill 快照替代 canonical v1.8.0
```

如果远端文件已确认存在，本地找不到时，应从远端 fetch（拉取），而不是把本地搜索当事实源发现机制。

## 4. 正确写回顺序

```text
LOCAL EXECUTION（本机执行）
→ LOCAL EVIDENCE（本机证据）
→ FORMAL REPORT / JSON（正式报告 / 机器状态）
→ LOCAL COMMIT（本地提交）
→ PUSH TO GitHub（推送GitHub远端共同工作区）
→ REMOTE VERIFY（远端核验）
→ STOP / RETURN TO GPT
```

只有远端核验成功后，才允许：

```text
SHARED_FACT_CONFIRMED=YES（共同事实已确认）
STAGE_COMPLETE=YES（阶段完成）
```

如果只在 C 盘完成但没有推送远端：

```text
REMOTE_SYNC_PENDING=YES（远端同步待完成）
```

不能称为共同工作区已完成。

## 5. 项目边界

本声明只属于 H3-P0 项目。

未来其他项目必须单独声明自己的：

```text
SHARED_WORKSPACE_REMOTE（远端共同工作区）
SHARED_WORKSPACE_BRANCH（远端分支）
SHARED_WORKSPACE_PROJECT_PATH（远端项目路径）
```

不得默认把 `cuiqinggang/codex-private-skills` 作为所有项目的唯一共同工作区。

## 一句话

> H3-P0 当前共同工作区是 GitHub 远端 `cuiqinggang/codex-private-skills` 的 H3 项目分支；当前母技能规则来自独立 canonical `first-principles-physical-limit-convergence v1.8.0` 分支；C 盘路径只作为本机执行副本或证据目录。
