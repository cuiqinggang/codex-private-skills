# 《新页面运行模板 第3版》

版本：第3版  
状态：CURRENT  
升级来源：《新页面运行模板 第2版》  
唯一标准：`T*=min(T_VALID)`

## 1. 页面启动来源门禁

新 CEO 页必须先读取网络共同工作区的明确来源，不得先扫描本机猜文件。

最小必填：

```text
REPO=cuiqinggang/codex-private-skills
REF=main 或固定 commit
ENGINE_PATH=明确路径
TASK_PATH=明确路径
```

当前方法目录：

`skills/artificial-single-page-extreme-time-engine/`

默认读取顺序：

1. `BRAIN.md`
2. `CURRENT_TASK_CONSTRAINTS.md`
3. 当前任务冻结状态/证据
4. `ENGINE.md`
5. `NEW_PAGE_TEMPLATE.md`

本地 `C:\...\` 只作为执行落地点/证据源，不作为方法权威源。

## 2. 页面边界的新定义

每个页面只服务一个明确任务或分支，但**不限制该任务内部只能做一个微优化**。

允许同页：

- 多轮虚拟成熟；
- 多候选并行分析；
- 多个兼容优化组合；
- 依赖图重排；
- 删除伪串行；
- 一次形成完整 Freeze。

禁止同页：

- 混跑两个无关项目；
- 混淆两个独立 Reality 身份；
- 在正式 Reality 运行中偷偷改变 Freeze。

## 3. Reality 前必须完成虚拟成熟循环

至少执行：

```text
瓶颈排序
→ 成熟方案映射
→ 依赖判断
→ 并行机会
→ 组合候选
→ VALID 风险检查
→ 收益收敛
```

不允许“发现一个点就立刻 Reality”。

## 4. 正式 Reality

默认一个 Freeze 对应一次正式 Reality。

Reality 结束后：

- PASS：冻结证据与 T_VALID；
- FAIL：冻结现实差异；
- UNKNOWN：保留证据，不冒充 FAIL/PASS。

若需要继续优化，先回虚拟成熟，不默认只改一个变量。

## 5. 单变量 A/B 门

只有满足以下任一条件才启用：

- 因果无法从现有证据区分；
- 多变化会影响 VALID 判定；
- 候选互斥；
- 需要证明某个元决策层（例如概率引擎）是否真正降低 T_VALID。

其余情况优先整包成熟。

## 6. 页面结束与换页

以下情况才换页：

- 当前任务/分支已冻结；
- 需要进入 Reality；
- Reality 返回需要重新成熟且上下文已重；
- 页面出现卡顿/失效风险；
- 需要把执行权交给另一个明确分支。

禁止因为“刚完成一个微优化”就机械换页。

## 7. NEXT_PAGE_PROMPT 门禁

需要换页时必须：

1. 写入当前冻结；
2. 生成唯一 NEXT_PAGE_PROMPT；
3. 最终回复完整原样输出该 prompt；
4. prompt 必须带 REPO / REF / ENGINE_PATH / TASK_PATH；
5. 不要求用户再去 C 盘找方法文件。

未输出正文：

`CEO_PAGE_COMPLETE=NO`

## 8. 最小化人工胶水

NEXT_PAGE_PROMPT 的目标是让新页直接接管，而不是让用户重新解释：

- 已完成什么；
- 当前权威版本；
- 当前 T*；
- 当前 Freeze；
- 下一闭环目标；
- 禁止事项。

## 9. 概率引擎

若任务适合概率元决策，可在虚拟成熟阶段调用或设计 A/B；不得默认进入 Reality hot path。

正式纳入前必须比较：

```text
无概率元决策层
vs
概率元决策层
```

在同一 VALID 下由 T_VALID 决定。

## 10. 页面结束硬规则

生成文件不等于交付完成。

最终回复必须说明：
- 本页是否执行 Reality；
- 是否更新 T*；
- 四个方法文件的网络共同工作区路径；
- 若需要下一页，完整输出唯一 NEXT_PAGE_PROMPT。

本版明确废止：

```text
每页一个自然逻辑节点 = 每页一个微变量
```

新的解释：

```text
每页一个任务闭环
任务闭环内部允许连续虚拟迭代直到成熟
```
