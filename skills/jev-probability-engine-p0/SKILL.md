---
name: jev-probability-engine-p0
description: 在可商用门槛内只以端到端时间为唯一优化量，把现实任务编译为最小串行深度概率执行图；以 Jev 为概率核心，配合状态机、动作与现实验证。用于 Probability Engine P0 的冻结、更新、测时与复用。
---

# JEV Probability Engine P0

版本：0.1.0，Step-1 物理结构冻结版。

## 三核心

1. 时间唯一标准：先通过 COMMERCIAL_GATE；门内唯一优化目标是 min T_E2E。
2. 成熟方案集群：概率判断、贝叶斯/分类、状态机、规则/约束、DAG 调度、反馈控制、verifier 等优先复用成熟结构，不从零发明概率理论。
3. 超级智能体虚拟成熟：现实执行前做结构收敛；Virtual-99 表示已难以再删除关键路径时间，不是新的 99 分指标。

## 引擎抽象

Probability Engine = E=(C,P,S,V)

C = Compiler：现实任务到概率执行图。
P = Probabilistic Kernel：Jev 等高速概率判断核心。
S = State Runtime：状态、依赖、确定性转移、动作回执。
V = Verifier：读取现实结果验证，不用模型自评代替现实证据。

通用原语：
OBSERVE → NORMALIZE → DECOMPOSE → DECIDE → COMBINE → TRANSITION → ACT → VERIFY → UPDATE → STOP

## 当前测功任务

PE-P0-GENERAL-01：24 项通用工作队列任务。
第一层 20 项互相独立；第二层 4 项分别依赖第一批真实动作回执。

当前冻结物理量：
PROBABILITY_NODE_COUNT_MIN=24
LAYER_WIDTHS_MIN=20,4
MAX_PARALLEL_WIDTH=20
D_MIN=2
JEV_ROUNDS_MIN=2
ACTION_OBJECT_COUNT_MIN=24
ACTION_BATCH_ROUNDS_MIN=2
VERIFY_OBJECT_COUNT_MIN=24
FINAL_VERIFY_BARRIERS_MIN=1

## 计时

T0：本次任务输入被释放给已经就绪、但尚未读取本次内容的引擎。
T1：全部最终状态真实存在、Reality Verifier 完成、COMMERCIAL_GATE=PASS、最终 manifest 已提交。

本次任务现场的读取、编译/拆解、状态构造、Jev、调度、动作、重试、恢复、验证和最终提交全部计时。
通用 Runtime、认证、连接池、通用规则等历史基础设施时间不重复摊入每个任务。

## 物理优化

不要把节点总数 N 当主目标；优先最小化不可避免的串行依赖深度 D(G)。
同层无依赖节点尽可能一次 Fan-out。
Prompt 改写后的重复询问不视为独立概率证据。
额外节点只有在通过可商用门槛确实需要时才保留。

## 当前阶段

Step 1 已完成结构冻结。
Step 2：成熟方案集群 + Virtual-99，只准在不改题的前提下删除额外串行。
Step 3：现实锚定 + Real P0，实测当前机器、网络、Jev Provider、动作后端和 verifier，得到 T_REAL* 与 T_P0。

进入后续工作前依次读取：
CURRENT_STATE.md
HISTORY.md
TASK_CONTRACT.md
PHYSICAL_LIMIT.md
UPDATE_PROTOCOL.md

禁止只保留最新结论而删除形成过程。任何改变三核心、任务合同、门槛、T0/T1、依赖结构或现实环境的更新必须产生新版本并保留旧版本。