# 《新页面运行模板 第10版》

版本：第10版  
升级来源：第9版  
状态：CURRENT  
唯一标准：T*=min(T_VALID)

## 1. 新 CEO 页面固定读取顺序

权威来源=网络共同工作区  
REPO=cuiqinggang/codex-private-skills  
SKILL_PATH=skills/artificial-single-page-extreme-time-engine/  
REF=<固定commit优先；否则明确main>

固定读取：

1. BRAIN.md
2. CURRENT_TASK_CONSTRAINTS.md 或当前任务 TASK_CONTRACT
3. 当前任务最新 CEO_FREEZE / NODE_FREEZE
4. ENGINE.md
5. NEW_PAGE_TEMPLATE.md

禁止先去 C 盘找方法。

新 CEO 页不重放旧聊天，只继承冻结结论。

## 2. 启动时先做一致性检查

必须确认：

- TASK_ID
- CONTRACT_VERSION
- FREEZE_VERSION / sequence
- FINAL_REALITY_GOAL
- POSITIVE_PROMPT
- NEGATIVE_PROMPT
- FINAL_VALID_STANDARD / DONE_WHEN
- EVIDENCE_REQUIRED
- 已完成节点
- 未完成节点
- 当前 T*
- 下一唯一控制目标

若合同缺失：
先 TASK_CONTRACT_GATE。

若 Freeze 缺失但任务已执行过：
不得靠聊天记忆猜状态，先恢复权威冻结证据。

## 3. PAGE_TOPOLOGY_GATE

新 CEO 刷新状态后只选：

A. SIMPLE_SINGLE_PAGE  
简单任务，本页 CEO=Executor，直接闭环。

B. CEO_EXECUTOR  
复杂任务，CEO 保持薄，只派最少必要 Executor。

判断依据：
哪个能在同等 VALID 下得到更低完整 T_VALID。

## 4. CEO 页面边界

一个 CEO 页面只服务一个完整自然控制节点。

自然控制节点不是“一个微优化”，而是：

读取冻结状态
→ 刷新当前决策
→ 必要时派发最小节点集
→ 接收/合并 Freeze
→ 做下一次控制判断
→ 到达新的稳定决策边界
→ CEO_FREEZE

一个控制节点内可以同时接收多个真正独立的 Executor 结果，但禁止为了凑数量固定开 3 页。

固定字符数/轮数不再是主换页触发器，只做 fallback。

## 5. Executor 页面边界

一个 Executor 页面=一个完整自然执行节点。

内部执行：

VIRTUAL_LOOP
→ STOP_GATE
→ NODE_FREEZE

该节点内部允许：
- 多轮连续虚拟成熟；
- ≤3成熟候选；
- 多个兼容优化组合；
- Reality Delta 后重新刷新。

节点 Freeze 后立即失去继续执行下一个自然节点的资格。

## 6. Freeze First → Close Second

无论 CEO 还是 Executor：

完成节点
→ 写 Freeze
→ 写证据位置
→ 上层确认可恢复
→ 页面无观察/恢复价值
→ Close

页面可以关闭，Freeze 不得丢失。

## 7. Reality

只有虚拟成熟停止后才能：

Freeze
→ Reality once

Reality PASS：
保存证据/T_VALID。

Reality FAIL/Delta：
保存真实差异；
不在 Reality 页面边改边跑；
返回新 VIRTUAL_LOOP 节点。

测试器只观察。

## 8. 三种整数版本

### 方法版本
第19版 / 第14版 / 第10版等。
系统性方法改变才升级。

### CONTRACT_VERSION
每个现实任务从 1 开始。
目标、FINAL_VALID、正向或反向约束改变时：
N → N+1。

禁止小数。

### FREEZE_VERSION / sequence
每个 CEO 自然控制节点 Freeze：
N → N+1。

它表示状态推进，不表示任务目标改变。

禁止小数。

## 9. 强制机器可读冻结标签

每次 CEO Freeze、换页或 STOP，NEXT_PAGE_PROMPT 第一条非空行必须是：

```text
CEO_FREEZE_TAG_JSON={"schema":"CEO_FREEZE_TAG_V1","freeze_id":"<不可变唯一ID>","page_id":"<CEO页面ID>","task_id":"<任务ID>","node_id":"<自然控制节点ID>","sequence":1,"state_code":100,"freeze_status":"PASS_FROZEN","final_valid":"YES","t_valid_ms":12345.678,"t_star_ms":12345.678,"source_repo":"cuiqinggang/codex-private-skills","source_ref":"<固定commit>","freeze_path":"<冻结文件路径>","next_node":"<下一节点或STOP>"}
```

字段规则：
- schema 固定 CEO_FREEZE_TAG_V1
- freeze_id 永久唯一
- sequence 整数单调递增
- state_code 只允许 10 / 20 / 30 / 40 / 100
- freeze_status 只允许 READY_FROZEN / CHECKPOINT_FROZEN / PASS_FROZEN / FAIL_FROZEN / UNKNOWN_FROZEN
- final_valid 只允许 YES / NO / UNKNOWN
- 数值未知用 JSON null，禁止 N/A
- source_ref 正式冻结优先不可变 commit
- next_node 真正结束填 STOP

同一条 JSON 必须同时写进 CEO Freeze 与 NEXT_PAGE_PROMPT，逐字段一致。
否则：
FREEZE_TAG_GATE=FAIL
CEO_PAGE_COMPLETE=NO。

## 10. 三行信封继续保留

机器 JSON 之后必须有：

【页面名｜任务名｜序号｜虚/实】  
状态机：<引擎版本/大脑版本/模板版本｜状态码｜当前节点>  
时间锚：TASK_ACCEPTED=<时间>｜READY_STATE_START=<时间或null>｜CURRENT=<节点>｜T_VALID=<数值或null>｜T*=<数值或null>

机器 JSON 给自动化读；
三行信封给人读。
两者不能互相替代。

## 11. NEXT_PAGE_PROMPT 必须携带的最小状态

必须包含：

- CEO_FREEZE_TAG_JSON
- 三行信封
- REPO / REF / SKILL_PATH
- TASK_ID
- CONTRACT_VERSION
- FREEZE_VERSION
- FINAL_REALITY_GOAL
- POSITIVE_PROMPT（可引用权威合同路径，不重复长正文）
- NEGATIVE_PROMPT（可引用权威合同路径）
- FINAL_VALID / DONE_WHEN（可引用合同路径）
- 当前冻结事实，最多3条
- 已完成/未完成节点的最小摘要
- 当前 T*
- 下一唯一控制节点
- 禁止重复已冻结工作

目标：
能让新 CEO 无需旧页聊天即可直接接管。

## 12. 页面结束门禁

CEO 到自然控制边界必须：

1. 写 CEO_FREEZE；
2. FREEZE_VERSION +1；
3. 生成唯一 NEXT_PAGE_PROMPT；
4. 回读核验 JSON 与 Freeze 一致；
5. 最终回复原样完整输出同一份 NEXT_PAGE_PROMPT；
6. 当前 CEO 不再继续下一控制节点。

未满足：
CEO_PAGE_COMPLETE=NO。

即使 next_node=STOP，也必须输出机器冻结标签，供自动化收口。

## 13. 新 CEO 接管

新 CEO：

读取合同
→ 读取最新 Freeze
→ 校验版本/sequence
→ 只刷新“现在该做什么”
→ 不重做已冻结工作
→ 进入下一个自然控制节点

原则：

CONCLUSION_SURVIVES_HISTORY_DOES_NOT。

一句话：

**任务合同锁目标；CEO Freeze 锁状态；NEXT_PAGE_PROMPT 只搬运最小结晶；Executor 页面负责重执行。**
