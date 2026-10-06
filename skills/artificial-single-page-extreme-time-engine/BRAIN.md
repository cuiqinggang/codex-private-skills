# 《极限短时间执行大脑 第3版》

版本：第3版  
升级来源：《极限短时间执行大脑 2.1》  
状态：CURRENT  
唯一标准：`T*=min(T_VALID)`

## 1. 第3版定位

执行大脑负责把任务不断压缩成最便宜、最快、可验证的智能形态。

核心不是“让 GPT 更努力思考”，而是：

```text
让 GPT 尽量少占串行关键路径
让 CODE 吃掉确定性
让 JEV 吃掉有限语义判断
让成熟方案吃掉已被现实解决的问题
```

## 2. 总脑循环

```text
INPUT
→ DEFINE
→ SOLVABILITY
→ DISCOVER_MATURE
→ COMPILE
→ PARALLELIZE
→ VIRTUAL_ATTACK
→ RECOMPILE
→ FREEZE
→ REALITY
→ VERIFY
→ STOP / RETURN_TO_VIRTUAL
```

## 3. Reality Solvability Gate：默认第一判断门

所有非平凡现实任务先判断：

- spec_complete
- evidence_search_complete
- physically_admissible
- mature_direct_solution
- mature_component_closure
- mature_exploration_protocol
- acceptance_verifiable
- certified_compilable_domain

输出只允许：

```text
INCOMPLETE_SPEC
SOLUTION_SEARCH_REQUIRED
INFEASIBLE_OR_CONTRADICTORY
CERTIFIED_COMPILABLE
MATURE_DIRECT
MATURE_COMPOSABLE
MATURE_EXPLORATORY
FRONTIER_UNKNOWN
```

如果 WORLD_SOLVED：
- 不允许单独开始研究；
- 直接进入成熟能力复制/组合。

## 4. Recursive Forward Compiler：全局默认编译器

对每个节点运行：

```text
if deterministic_exact && deterministic_executor_available:
    CODE
elif state_explicit
     && finite_choice
     && certified_actions
     && deterministic_verifier
     && !open_generation
     && !hidden_information
     && !timed_retry:
    JEV
else:
    GPT
```

GPT 的输出必须再次过编译器。

因此一项任务可以呈现：

```text
GPT 8%
JEV 22%
CODE 70%
```

也可以：

```text
GPT 2%
JEV 70%
CODE 28%
```

比例由任务事实决定，不预设。

## 5. “所有任务都可以用 HIPE”的正式解释

冻结：

```text
ALL_NONTRIVIAL_TASKS_CAN_BE_COMPILED=YES
ALL_TASKS_SHOULD_CALL_JEV=NO
```

几乎所有任务都可以接受：
- 可解性判断；
- 正向分解；
- 节点分类；
- 依赖分析；
- 成本/时间路径编译。

但有些节点最终会被编译为 CODE 或 GPT，而不是 JEV。

这不是“没使用概率引擎”，而是概率引擎/正向编译器成功判断出：
**该节点不应该浪费一次网络概率调用。**

## 6. Jev 最大化策略

### 6.1 Finite Choice Conversion
只要开放问题经过成熟分析后可以安全变成有限候选：
- 转 Choice；
- 用 JEV 排序/选择；
- verifier 收口。

### 6.2 Multi-question Batch
同一 state 的独立判断：
- 尽量一次请求多个 questions；
- 避免连续 model barrier。

### 6.3 Confidence Cascade
高置信 → 自动走冻结动作；
低置信/边界 → GPT residual；
最终结果 → deterministic verifier。

### 6.4 Conditional Precompute
有限前驱结果的后续路线：
- 提前算 policy；
- receipt 到达后 CODE 选分支；
- 不重新开启复杂推理。

## 7. Browser Brain

浏览器先做动作空间压缩：

```text
页面/协议
→ CODE抽取状态
→ CODE生成可执行控件/工具表
→ JEV选择有限动作
→ CODE执行
→ 增量状态
→ verifier
```

如果页面已经有唯一确定动作：
```text
CODE直接执行
```

如果页面根本未暴露所需动作：
```text
GPT / 工具发现
```

禁止 JEV 幻觉出不存在的 selector/action。

## 8. 并行规则

必须先画 DAG（依赖图）。

- 独立 evidence search：并行；
- 独立候选 probe：并行；
- 独立 typed decisions：同请求 batch 或并发；
- 独立下载：可并行；
- 独立 verifier：可并行；
- 真依赖：串行。

“代码现在写成顺序”不等于“物理上必须顺序”。

## 9. 判断一次是否值得 Reality

Reality 前必须满足：

```text
NEED_REALITY=YES
```

只有现实环境才能消除的关键未知才值一次 Reality。

若可以通过：
- 源码；
- schema；
- 已冻结成熟证据；
- deterministic test；
- 静态验证；
- 已有可靠 Reality；

消除，就不要消耗正式 Reality。

## 10. 优化候选排序

在 VALID 不变前提下，优先：
1. 删除整个模型屏障；
2. 删除整个浏览器/网络阶段；
3. 把串行变并行；
4. 直接复用成熟能力；
5. 把 GPT 降到 JEV；
6. 把 JEV 降到 CODE；
7. 条件跳过不必要阶段；
8. 最后才微调毫秒级参数。

优先优化“结构”，不是先调阈值。

## 11. 停止规则

出现以下任一即可 STOP：
- FINAL_VALID 且无高置信结构性大收益候选；
- 剩余改进低于现实抖动；
- 继续优化会增加更多状态/恢复复杂度；
- 方法验证已达 3–4轮且稳定；
- 第5轮硬上限。

## 12. HIPE v0.3.5 固定来源

```text
REPO=cuiqinggang/codex-private-skills
PATH=skills/hybrid-intelligence-probability-engine-v0-3-5/
FREEZE_COMMIT=c6fe2878fd237e7a8120b3af8e75f93e3cd6a4d9
FREEZE_ID=HIPE-v0.3.5-FULLY-SEALED-20261006-R1
```

正式组件：
- Reality Solvability Gate v0.2.0
- Comfort-Zone Forward Compiler v0.2.0
- CODE / JEV / GPT residual
- deterministic verifier

HIPE 本体 FULLY_SEALED，不原地修改。

## 13. OpenRouter / Jev Runtime Contract

固定：
```text
ENDPOINT=https://openrouter.ai/api/alpha/decisions
MODEL=typesafe/jev-1.13
KEY_ENV=OPENROUTER_API_KEY
```

生产禁止：
- 把 key 写进 Git 仓库；
- 把 key 写进日志/status/冻结文档；
- 把 key 作为命令行参数。

运行时从安全环境变量/凭据存储读取。

## 14. Integer Version Policy

执行大脑只使用整数：
```text
第3版 → 第4版 → 第5版
```

不再使用 3.1 / 3.2。

## 15. 最终原则

```text
先问：世界是否已经解决？
再问：能否变成CODE？
再问：能否变成有限Choice交给JEV？
剩下的才给GPT。
GPT做完后，再问一遍前面三个问题。
```

这就是第3版的核心执行循环。
