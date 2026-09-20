# STEP-1 PHYSICAL LIMIT

## 最少概率节点

在固定动作集合和显式约束下，每个项目至少要确定一个最终动作。

第一层 01–20：20 个最终 Choice 节点。
第二层 21–24：4 个最终 Choice 节点，必须读取 17–20 的真实动作回执。

PROBABILITY_NODE_COUNT_MIN=24

额外 Noul、Score、重采样只在通过商业门槛确实必要时保留，不作为结构先验。

## 确定性部分

schema 校验、依赖图、允许动作掩码、状态转移、批量调度、receipt 记录、hash、oracle verifier、manifest 都可确定性完成。

## 最小 DAG

T0
→ READ / VALIDATE / BUILD DEPENDENCY GRAPH
→ P1: Jev Fan-out ITEM01..ITEM20，宽度 20
→ D1: apply allowed-action mask / combine
→ A1: batch action ITEM01..ITEM20
→ O1: commit receipts，尤其 ITEM17..20
→ P2: Jev Fan-out ITEM21..ITEM24，宽度 4
→ D2: mask / combine
→ A2: batch action ITEM21..ITEM24
→ V: final reality verify + manifest
→ T1

第一批其它项目的局部验证应与 P2/A2 重叠，不形成新的关键路径屏障。

## D_MIN 证明

21–24 的正确输入包含真实 receipt；receipt 在 A1 前物理上不存在，所以不能与 P1 同一轮完成最终判断。
20 个第一层判断互相独立，可同轮 Fan-out。
4 个第二层判断在 receipts 到齐后互相独立，可同轮 Fan-out。

因此：
LAYER_WIDTHS_MIN=20,4
MAX_PARALLEL_WIDTH=20
D_MIN=2
JEV_ROUNDS_MIN=2

## 动作与验证下界

每项必须到达真实终态：
ACTION_OBJECT_COUNT_MIN=24

第二层依赖第一批动作回执：
ACTION_BATCH_ROUNDS_MIN=2

全部 24 项需要现实验证：
VERIFY_OBJECT_COUNT_MIN=24
FINAL_VERIFY_BARRIERS_MIN=1

## T_PHY 结构式

T_PHY =
t_in*
+ t_J20*
+ t_A20*
+ t_J4*
+ t_A4*
+ t_Vtail*
+ t_out*

其中每个星号量是在固定协议/硬件/网络/后端下的最低物理极限。

本版本不把公开 Jev 百毫秒级案例或社区 benchmark 直接代入，从而避免制造假的当前机器物理极限。

T_PHY_FORMULA=DERIVED
T_PHY_NUMERIC=REQUIRES_REALITY_CONSTANTS

数值现实锚定以后得到 T_REAL*；真实实现运行得到 T_P0。