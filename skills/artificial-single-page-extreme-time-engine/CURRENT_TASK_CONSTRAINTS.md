# 《当前任务目标与正反约束 当前版》

状态：CURRENT  
任务：新版极限短时间方法 Reality 验证（从零重开，不是 Greenfield-R11）  
方法基线：《人工单页面极限短时间引擎 第7版》+《极限短时间执行大脑 2.1》+《新页面运行模板 第4版》

## 1. 当前目标

重新从任务第1步定义一个同类现实任务，用新版方法从零推进，验证本次制度修正是否真正降低“从 TASK_ACCEPTED 到成熟 FINAL_VALID”的总闭环时间。

这不是继续 R11，不继承 R1-R10 的具体实现优化链。

R1-R10 只允许作为：
- 方法复盘证据；
- 失败模式反例；
- 禁止复发规则来源。

不得把 R9/R10 代码、阈值、等待参数、claim 或局部优化直接作为新任务实现基线。

## 2. 新验证任务的核心原则

```text
新任务定义
→ HIPE Reality Solvability Gate v0.2.0
→ 成熟方案集群
→ Comfort-Zone Forward Compiler v0.2.0
→ CODE / JEV / GPT residual 路由
→ 连续虚拟成熟
→ 最大合法并行
→ 整包 Freeze
→ Reality
→ verifier
→ FINAL_VALID
```

Reality 不是探索器。

## 3. HIPE v0.3.5 固定冻结来源

```text
REPO=cuiqinggang/codex-private-skills
PATH=skills/hybrid-intelligence-probability-engine-v0-3-5/
FREEZE_COMMIT=c6fe2878fd237e7a8120b3af8e75f93e3cd6a4d9
FREEZE_ID=HIPE-v0.3.5-FULLY-SEALED-20261006-R1
STATE=FULLY_SEALED
```

组件：
- Reality Solvability Gate v0.2.0
- Comfort-Zone Forward Compiler v0.2.0

禁止原地修改冻结 HIPE v0.3.5。若发现缺陷，返回 NEEDS_VERSIONED_UPGRADE。

## 4. Reality 轮数预算

```text
TARGET=3..4
HARD_MAX=5
```

- 能首轮成熟完成就首轮完成，不为了凑轮数继续。
- 3–4轮用于验证方法是否稳定，不用于机械微调。
- 最多5轮；第5轮仍未收敛必须 STOP + 复盘方法。
- 禁止再次形成 R1→R10 式无限串行微版本。

## 5. 权威位置

方法与冻结状态优先写网络共同工作区。

本地 C 盘：
- 可作为执行缓存、临时文件、运行时依赖；
- 只有网络共同工作区不可用时才作为 fallback；
- fallback 必须显式记录 SOURCE_FALLBACK=YES；
- 不得通过扫描整个 C 盘猜权威文件。

## 6. 正向约束

- 唯一标准保持 `T*=min(T_VALID)`；
- 先冻结任务边界，区分建设任务与生产子任务；
- GPT/HIPE 负责虚拟成熟和路由；
- 确定性代码承担能精确完成的工作；
- JEV 只承担有限 Choice / typed decision；
- 开放问题保留 GPT residual；
- Reality 只验证冻结方案；
- verifier 必须独立；
- performance instrumentation 首轮即布好；
- 所有页面冻结出口必须带 `CEO_FREEZE_TAG_JSON`。

## 7. 反向约束

禁止：
- 执行 Greenfield-R11；
- 继承 R10 threshold=2 或 R9 局部逻辑作为新任务基线；
- 每发现一个瓶颈就立即 Reality；
- 每个微优化都换 CEO 页；
- 把 Local Minimal Repair 当全局优化法；
- 把 JEV 插入纯确定性 hot path；
- 把“页面没有暴露的动作”交给 JEV 猜；
- 超过5轮 Reality 仍继续刷版本。

## 8. 成功判据

新版方法验证成功，不以“某一次程序跑通”单独判定。

至少要求：
1. 新任务产生真实 FINAL_VALID；
2. 整包虚拟成熟确实减少 Reality 循环；
3. 页面/冻结/交接没有恢复成微变量串行器；
4. CEO_FREEZE_TAG_JSON 可由状态机直接读取；
5. 总建设闭环时间与旧 10 轮方式相比出现明确结构性改善；
6. 3–5轮预算内完成或得出明确方法复盘结论。

## 9. 当前下一节点

`METHOD-VALIDATION-R0-TASK-DEFINE`

只重新定义新任务及 VALID / READY_STATE / 权威工作区，不执行 R11。
