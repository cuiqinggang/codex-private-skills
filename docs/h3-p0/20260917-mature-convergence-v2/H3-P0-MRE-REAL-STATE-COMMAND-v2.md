# H3-P0 MRE 真实态校准命令包 v2

状态：RELEASED（已发布）

本版只修正一个基础概念：**共同工作区永远是 GitHub 远端在线权威仓库；C盘目录只是本地执行副本或本机证据目录。**

其余 MRE（极简真实运行）任务合同、V3配置、计时、QC、恢复、3条正式样本、停止条件，继续继承：

`H3-P0-MRE-REAL-STATE-COMMAND-v1.md`

## 0. 方法版本

```text
METHOD（方法）= first-principles-physical-limit-convergence v1.6.0
```

必须同时读取母技能：

`origin/codex/first-principles-physical-limit-convergence-v1.6.0`

尤其读取：

`skills/first-principles-physical-limit-convergence/references/REMOTE-SHARED-WORKSPACE.md`

## 1. H3-P0 项目共同工作区

必须先读取：

`docs/h3-p0/20260917-mature-convergence-v2/H3-P0-REMOTE-WORKSPACE-DECLARATION.md`

当前项目声明：

```text
PROJECT_ID（项目ID）= H3-P0
SHARED_WORKSPACE_TYPE（共同工作区类型）= GitHub
SHARED_WORKSPACE_REMOTE（远端共同工作区）= cuiqinggang/codex-private-skills
SHARED_WORKSPACE_BRANCH（远端工作分支）= codex/h3-p0-mature-convergence-v2
SHARED_WORKSPACE_PROJECT_PATH（远端项目路径）= docs/h3-p0/20260917-mature-convergence-v2
REMOTE_VERIFY_REQUIRED（必须远端核验）= YES
```

硬规则：

```text
SHARED_WORKSPACE_IS_REMOTE=YES（共同工作区必须是远端在线空间）
LOCAL_PATH_IS_SHARED_WORKSPACE=NO（本地路径绝不等于共同工作区）
```

## 2. 本机路径的正确身份

如果本机存在：

`C:\Users\A\Documents\Codex\codex-private-skills`

它只能叫：

```text
LOCAL_EXECUTION_CHECKOUT（本地执行副本）
```

如果本机存在：

`C:\AI\H3-P0-Acceptance\mature-convergence-v2\20260917-mre-01`

它只能叫：

```text
LOCAL_EVIDENCE_ROOT（本机证据目录）
```

禁止把上述任一本地路径称为“共同工作区”或“共同事实源”。

## 3. 正确启动顺序

Codex 不得先扫描磁盘寻找共同工作区。

必须：

```text
REMOTE LOCATE（远端定位）
→ 确认 GitHub 仓库 cuiqinggang/codex-private-skills
→ 确认远端分支 codex/h3-p0-mature-convergence-v2
→ 从远端读取本命令、工作区声明、旧冻结档案和 Failure Index（失败索引）
→ 再定位本机已有 clone（克隆）作为 LOCAL_EXECUTION_CHECKOUT（本地执行副本）
→ fetch / checkout（拉取 / 检出）到目标远端状态
→ 执行本机 MRE
```

如果远端文件已存在而本地副本没有：

```text
FETCH FROM REMOTE（从远端拉取）
```

禁止：

```text
递归扫描 C:\AI、C:\Users\... 来猜文件在哪
```

## 4. MRE 执行主体

完整执行：

`H3-P0-MRE-REAL-STATE-COMMAND-v1.md`

但其中所有术语按本版重新解释：

```text
“共同工作区” = GitHub远端 cuiqinggang/codex-private-skills
“共同事实源” = GitHub远端目标分支中的已核验文件
“本地仓库/本地路径” = LOCAL_EXECUTION_CHECKOUT（本地执行副本）
“证据目录” = LOCAL_EVIDENCE_ROOT（本机证据目录）
```

本轮仍固定：

```text
LAST_GOOD（最近保留版）= V3_RESERVE1
--fast-disk
--reserve-vram 1.0
--disable-pinned-memory
PORT=8194
```

仍只运行：

```text
COLD（冷态）1次
→ WARMUP（预热）1次
→ FORMAL（正式）3次
→ QC（质量检查）
→ summary（汇总）
→ source restore（源码恢复）
→ real-state report（真实态报告）
→ STOP（停止）
```

禁止 Star7、禁止新优化、禁止新 profiling（性能剖析）、禁止自动进入下一阶段。

## 5. 写回远端共同工作区

本机执行完成后：

```text
LOCAL RESULT（本机结果）
→ LOCAL EVIDENCE（本机证据）
→ FORMAL REPORT / JSON（正式报告 / 机器状态）
→ LOCAL COMMIT（本地提交）
→ PUSH TO SHARED_WORKSPACE_REMOTE（推送远端共同工作区）
→ REMOTE VERIFY（远端核验）
```

只有：

```text
REMOTE_VERIFY=PASS（远端核验通过）
```

才允许：

```text
MRE_STAGE_COMPLETE=YES（MRE阶段完成）
SHARED_FACT_CONFIRMED=YES（共同事实已确认）
```

如果本机 MRE 已完成但尚未推送远端：

```text
LOCAL_MRE_COMPLETE=YES（本机MRE完成）
REMOTE_SYNC_PENDING=YES（远端同步待完成）
MRE_STAGE_COMPLETE=NO（阶段尚未正式完成）
```

## 6. 项目隔离

本命令中的 GitHub 仓库只属于 H3-P0 当前项目。

未来其他项目必须重新声明自己的：

```text
SHARED_WORKSPACE_REMOTE（远端共同工作区）
SHARED_WORKSPACE_BRANCH（远端分支）
SHARED_WORKSPACE_PROJECT_PATH（远端项目路径）
```

不得因为 H3-P0 使用 `cuiqinggang/codex-private-skills`，就把它自动当成所有未来项目的共同工作区。

## 一句话执行合同

> **先从 GitHub 远端共同工作区读取任务和事实，再把它检出到本机执行副本运行；本机只负责执行和产生证据，最终结果必须写回 GitHub 并远端核验。H3-P0 当前共同工作区是 `cuiqinggang/codex-private-skills`，C盘不是共同工作区。**
