# 通用高性能视觉作品生成引擎 — 共同办公区

英文标识：`Visual Art Engine Performance Ladder — Shared Workspace`

## 固定 GitHub 地址

私有仓库：

`https://github.com/cuiqinggang/codex-private-skills`

共同办公区：

`https://github.com/cuiqinggang/codex-private-skills/tree/main/workspaces/visual-art-engine-performance-ladder`

这是 ChatGPT 与 Codex 在 P0→P8 快速迭代期间统一使用的共享资料存放点。

任何需要 ChatGPT 审核的真实测试，Codex 都必须把关键报告和证据同步到这里；只提供 `C:\...` 本地路径不算完整交接。

P0 结果统一写入：

`workspaces/visual-art-engine-performance-ladder/stages/P0/<RUN_ID>/`

P1-P8 按同样规则进入各自阶段目录。

ChatGPT 审核文件写入：

`workspaces/visual-art-engine-performance-ladder/reviews/`

ChatGPT 规划文件写入：

`workspaces/visual-art-engine-performance-ladder/plans/`

## 固定协作方式

- ChatGPT：读取最新证据，调用 `mature-replication-four-column` V4.0（第一性原理四列法 V4.0）完成阶段审核，决定下一步并生成 Codex 执行命令。
- Codex：负责本机真实执行、测量、保存原始证据，并把需要 ChatGPT 审核的报告包同步到本目录。
- 仅提供 `C:\...` 本地路径不算完整交接；需要审核的文本、JSON、日志、脚本和摘要应同步到这里。

## 中文优先表达规则

从本目录开始，所有报告、审核和状态说明统一采用：

**中文名称在前，英文技术标识放在括号中。**

例如：

- 当前实测时间（`CURRENT`）
- 外部成熟前沿（`EXTERNAL FRONTIER`）
- 第一性原理物理时间（`FIRST-PRINCIPLES PHYSICAL TIME / T_PHY`）
- 迭代收敛（`ITERATIVE CONVERGENCE`）
- 阶段冻结（`FREEZE`）
- 重新打开冻结阶段（`REOPEN`）
- 路径/架构错误（`PATH_ARCHITECTURE_ERROR`）

英文保留用于程序、技能、变量和仓库统一识别，但不得让主要说明只剩英文。

## 四列法固定展示规则

四列法审核必须按下面的**纵向顺序**展示，不使用横向四列总表：

1. 当前实测时间（`CURRENT`）
2. 外部成熟前沿（`EXTERNAL FRONTIER`）
3. 第一性原理物理时间（`FIRST-PRINCIPLES PHYSICAL TIME / T_PHY`）
4. 迭代收敛（`ITERATIVE CONVERGENCE`）

每一项必须至少包含：

- 当前状态；
- 当前数字/区间；
- 证据来源；
- 审核判断；
- 本项与下一项之间的关系；
- 是否允许继续下一步。

## 目录结构

```text
workspaces/visual-art-engine-performance-ladder/
  README.md
  LATEST.md
  stages/
    P0/
      <run-id>/
        REPORT.md
        timing-summary.json
        output-validation.json
        raw-websocket-events.jsonl
        benchmark-contract-snapshot.md
        environment-before.json
        environment-after.json
        ...其他用于复现和审核的小型关键证据
    P1/
    ...
    P8/
  reviews/
    ...ChatGPT 四列法审核文件
  plans/
    ...ChatGPT 99分推进计划和阶段执行计划
```

## LATEST.md 规则

每次需要 ChatGPT 审核的正式运行完成后，Codex 更新 `LATEST.md`，至少包含：

- 阶段和运行 ID；
- 当前工作技能版本；
- 方法版本；
- 最终状态；
- 包含证据的 Git commit；
- 报告相对路径；
- 四项纵向状态：当前实测、外部成熟前沿、第一性原理物理时间、迭代收敛；
- 下一步请求。

## 快速迭代规则

快速迭代期间，不要求每一个本地小补丁都立刻变成正式技能发布版本；但是每一次需要 ChatGPT 深度审核的真实运行，都应该把关键报告/证据同步到本共同办公区。

正式稳定技能仍位于：

`skills/visual-art-engine-performance-ladder`

到稳定里程碑、99 分冻结点或重大关口时，再统一正式部署和 GitHub 发布。

## 证据策略

优先同步用于审核的文本、JSON、CSV、日志和脚本。避免无必要上传大型模型、缓存、重复生成媒体或整套运行环境。大型输出原则上保留 SHA-256、元数据和准确本地/外部引用，只有审核确实需要时才上传本体。

## 方法论

所有阶段统一调用：

`mature-replication-four-column` — V4.0（第一性原理四列法 V4.0）

不得在本工作区另建平行方法论。
