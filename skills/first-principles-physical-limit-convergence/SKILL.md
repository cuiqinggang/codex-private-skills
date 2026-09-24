---
name: first-principles-physical-limit-convergence
description: 极限短时间引擎 v4.7.7。只有“虚/实”两步；现实入口新增自包含冻结胶囊，禁止 REAL 启动后再依赖远程读取或临时权限审批；继续执行阶段-执行器一致性、现实时间、证据一致性硬门。
metadata:
  version: "4.7.7"
  display_name: "极限短时间引擎"
---

# 极限短时间引擎 v4.7.7

## 核心
- 方法永远只有两步：虚、实。
- 虚由 GPT 完成成熟；实由 Codex 只执行冻结合同。
- 当前用户可见成熟基准：极限锚03:14.419（194419.3759 ms）。
- 该数是当前引擎既有成熟 clean run 基准；不得冒充“本次回归任务的物理下限”。
- 每个 REAL 必须记录自己的 T_VALID_REAL_MS；没有真实时间，REAL 永远不能 PASS。

## 0号门：阶段—执行器一致性
IF EXECUTOR=CODEX AND PHASE!=实 -> 第一副作用前 BLOCK。

PHASE=虚：
- 执行器=GPT；
- CODEX_DISPATCH=0；
- Codex 业务副作用=0；
- GPT 可以在控制面发布/回读冻结包。

PHASE=实：
- 执行器=Codex；
- 只执行冻结内容；
- 不现场重新设计。

## v4.7.7 新增：现实入口必须自包含
v4.7.6 的 03-01 REAL 在读取远程/外部合同和测试向量时等待权限审批，导致没有进入验证且现实墙钟已超基准。

因此从 v4.7.7 起：

1. REAL 启动所必需的规则、测试项、路径、Freeze、时间门必须直接包含在现实任务胶囊内；
2. GitHub/共同仓库是审计事实源，不再是 REAL 启动读取依赖；
3. REAL 启动后禁止“先申请权限读取冻结合同，再决定怎么做”；
4. 若本机目标源码本身不可访问，立即形成最小 Reality Delta 并 STOP，不等待长审批；
5. 远程回读在虚阶段完成；实阶段只消费已冻结、自包含的内容。

机器不变量：
REAL_START_DEPENDENCY_REMOTE_READ=FORBIDDEN
REAL_START_DEPENDENCY_PERMISSION_APPROVAL_FOR_FREEZE=FORBIDDEN
REAL_CAPSULE_SELF_CONTAINED=REQUIRED

## 虚完成门
VIRTUAL_COMPLETE=YES 只有同时满足：
- Reality Delta 已吸收；
- 方案已成熟；
- FREEZE_ID 已生成；
- 冻结分支已发布；
- 冻结文件已远程回读；
- REAL 胶囊已经生成；
- REAL 胶囊自包含；
- REAL 任务定位明确为“实”；
- 时间账规则已冻结；
- 证据一致性 PASS。

任一缺失：VIRTUAL_COMPLETE=NO。

## 虚→实原子转换
固定顺序：
虚成熟
-> Freeze
-> 远程发布
-> 远程回读
-> 自包含 REAL 胶囊
-> 标记“实”的 Codex 现实任务
-> 原子切换到同一状态号的“实”
-> VIRTUAL_COMPLETE=YES。

禁止：
- Codex任务标“虚”；
- 虚完成但没有现实任务；
- 实启动后再去取冻结合同；
- 同一 FREEZE_ID 第二次正式现实执行。

## 有限循环
状态格式：NN-NN。
- 前两位=方案代；
- 后两位=本方案代正式现实尝试号；
- 01–06 合法；
- 07 永久非法；
- 第6次失败强制下一方案代01；
- 第1–5次遇结构性错误可提前换代。

03-01 的失败属于结构性外部依赖闭合错误，因此进入：
04-01｜虚。

## REAL 时间
每次现实必须记录：
REAL_START
REAL_END
T_VALID_REAL_MS

当前用户可见比较基准仍为：
194419.3759 ms。

对本次回归现实任务，它只作为“当前成熟引擎性能基准/上限”，不是本任务物理下限的伪精确声明。

若功能 PASS 但耗时超过当前基准：
REAL_VALID=NO
-> 记录 Reality Delta
-> 回虚优化。

## 证据一致性
PASS 前必须检查：
- 阶段与物理动作一致；
- 现实时间完整；
- 路径字段无矛盾；
- 本地/远程 commit 与 branch 范围明确；
- 声称远程存在的对象可回读；
- PASS 项有证据；
- 自包含胶囊哈希与冻结源一致。

任一矛盾：FINAL_VALID=NO。

## v4.7.6 -> v4.7.7 Reality Delta
03-01 REAL：
- 20项验收=0/20；
- 集成未开始；
- 冻结合同/向量读取被权限审批阻断；
- REAL_START=2026-09-24 15:36:42 UTC（秒级）；
- REAL_END=2026-09-24 15:39:57.664 UTC；
- T_VALID_REAL 下界 >=194665 ms；
- 已超过当前成熟基准194419.3759 ms；
- 正确执行 STOP，没有重试。

结构性结论：
冻结包虽远程存在，但 REAL 仍依赖启动时读取/审批，因此 EXTERNAL_DEPENDENCIES_CLOSED 实际未通过。

## 本版本虚拟验证
- v4.7.6 已完成 20/20 状态转移逻辑验证；
- v4.7.7 对“自包含现实胶囊/远程依赖/时间缺失/阶段错配”等新增边界做 22/22 逻辑验证通过。

## 语言
用户可见全部中文优先。
机器字段、路径、哈希、版本号可以保留英文。

## 一句话
虚阶段把 REAL 需要的一切冻结并直接装进现实胶囊；实阶段不再取方案，只执行胶囊、计时、验证、返回。
