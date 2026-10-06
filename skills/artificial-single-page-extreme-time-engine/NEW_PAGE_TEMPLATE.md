# 《新页面运行模板 第4版》

版本：第4版  
状态：CURRENT  
升级来源：《新页面运行模板 第3版》  
唯一标准：`T*=min(T_VALID)`

## 1. 页面启动来源门禁

新 CEO 页必须先读取网络共同工作区的明确来源，不得先扫描本机猜文件。

最小必填：

```text
REPO=cuiqinggang/codex-private-skills
REF=固定 commit（正式冻结优先）或明确 main
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

## 2. 页面边界

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
任务可解性判定
→ 成熟方案映射
→ 依赖判断
→ 路由 CODE / JEV / GPT
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
- 需要证明某个元决策层是否真正降低 T_VALID。

其余情况优先整包成熟。

## 6. 页面结束与换页

以下情况才换页：
- 当前任务/分支已冻结；
- 需要进入 Reality；
- Reality 返回需要重新成熟且上下文已重；
- 页面出现卡顿/失效风险；
- 需要把执行权交给另一个明确分支。

禁止因为“刚完成一个微优化”就机械换页。

## 7. 强制机器可读冻结标签

**从第4版起，每一次任务节点完成、冻结、换页或 STOP，都必须产生机器可读冻结标签。**

标签必须是 NEXT_PAGE_PROMPT 的**第一条非空行**，格式固定为单行 JSON：

```text
CEO_FREEZE_TAG_JSON={"schema":"CEO_FREEZE_TAG_V1","freeze_id":"<不可变唯一ID>","page_id":"<页面ID>","task_id":"<任务ID>","node_id":"<节点ID>","sequence":1,"state_code":100,"freeze_status":"PASS_FROZEN","final_valid":"YES","t_valid_ms":12345.678,"t_star_ms":12345.678,"source_repo":"cuiqinggang/codex-private-skills","source_ref":"<固定commit>","freeze_path":"<冻结文件路径>","next_node":"<下一节点或STOP>"}
```

### 必填字段

- `schema`：固定 `CEO_FREEZE_TAG_V1`
- `freeze_id`：本次冻结的永久唯一 ID，生成后不得复用或改写
- `page_id`：当前 CEO 页机器 ID
- `task_id`：当前任务机器 ID
- `node_id`：当前自然逻辑节点 ID
- `sequence`：整数，单调递增
- `state_code`：只允许 10 / 20 / 30 / 40 / 100
- `freeze_status`：只允许 `READY_FROZEN / CHECKPOINT_FROZEN / PASS_FROZEN / FAIL_FROZEN / UNKNOWN_FROZEN`
- `final_valid`：只允许 `YES / NO / UNKNOWN`
- `t_valid_ms`：有正式 T_VALID 时填数值；未产生时填 JSON `null`
- `t_star_ms`：有当前正式 T* 时填数值；未知时填 JSON `null`
- `source_repo`：权威共同工作区
- `source_ref`：正式冻结优先使用不可变 commit；不得用模糊文本
- `freeze_path`：本次冻结记录的权威路径
- `next_node`：下一节点机器 ID；任务真正结束填 `STOP`

### 机器门禁

1. 同一条 `CEO_FREEZE_TAG_JSON` 必须同时写入当前冻结记录与 NEXT_PAGE_PROMPT。
2. 两处必须逐字段一致。
3. 缺失、JSON 无法解析、字段缺失、枚举非法、sequence 非整数、freeze_id 重复或两处不一致：
   `FREEZE_TAG_GATE=FAIL`。
4. `FREEZE_TAG_GATE=FAIL` 时不得自动进入下一 CEO 页，`CEO_PAGE_COMPLETE=NO`。
5. 禁止使用 `N/A`；数值未知用 JSON `null`，状态未知用规定枚举 `UNKNOWN`。
6. 人类可读的三行信封继续保留，但**不能替代**本机器标签。

## 8. NEXT_PAGE_PROMPT 门禁

需要换页时必须：

1. 写入当前冻结；
2. 生成唯一 NEXT_PAGE_PROMPT；
3. NEXT_PAGE_PROMPT 第一条非空行必须是合法 `CEO_FREEZE_TAG_JSON`；
4. 最终回复完整原样输出该 prompt；
5. prompt 必须带 REPO / REF / ENGINE_PATH / TASK_PATH；
6. 不要求用户再去 C 盘找方法文件。

即使当前任务结束、`next_node=STOP`，最终冻结回报仍必须带同样机器标签，供自动化收口和后续索引读取。

未满足任一项：

`CEO_PAGE_COMPLETE=NO`

## 9. 最小化人工胶水

NEXT_PAGE_PROMPT 的目标是让新页/自动化直接接管，而不是让用户重新解释：
- 已完成什么；
- 当前权威版本；
- 当前 T*；
- 当前 Freeze；
- 下一闭环目标；
- 禁止事项。

自动化优先读取 `CEO_FREEZE_TAG_JSON`，正文用于详细上下文。

## 10. HIPE v0.3.5 元决策层

冻结入口：
- `skills/hybrid-intelligence-probability-engine-v0-3-5/`
- 固定冻结 commit：`c6fe2878fd237e7a8120b3af8e75f93e3cd6a4d9`
- FREEZE_ID：`HIPE-v0.3.5-FULLY-SEALED-20261006-R1`

页面虚拟成熟阶段允许使用其：
- Reality Solvability Gate v0.2.0；
- Comfort-Zone Forward Compiler v0.2.0；
- CODE / JEV / GPT residual 路由；
- 合法并行；
- deterministic verifier。

原则：

```text
全流程可挂载 HIPE 判断
≠ 每一步都调用 JEV
```

确定性问题直接 CODE；有限 Choice 且可验才 JEV；开放生成/隐藏信息/定时重试回 GPT residual。

## 11. 页面结束硬规则

生成文件不等于交付完成。

最终回复必须说明：
- 本页是否执行 Reality；
- 是否更新 T*；
- 方法文件网络共同工作区路径；
- 当前 FREEZE_ID；
- 若需要下一页，完整输出唯一 NEXT_PAGE_PROMPT。

本版继续废止：

```text
每页一个自然逻辑节点 = 每页一个微变量
```

新的解释：

```text
每页一个任务闭环
任务闭环内部允许连续虚拟迭代直到成熟
每个冻结出口必须有机器标签
```
