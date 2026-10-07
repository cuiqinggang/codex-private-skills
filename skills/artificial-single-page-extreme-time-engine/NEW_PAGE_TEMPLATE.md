# 《新页面运行模板 第11版》

版本：第11版
升级来源：第10版
状态：CURRENT
唯一标准：T*=min(T_VALID)

## 1. 新 CEO 固定读取顺序

必须按顺序读取，不允许跳层：

1. BRAIN.md
2. CURRENT_TASK_CONSTRAINTS.md / 当前任务 TASK_CONTRACT
3. CURRENT_TASK_FREEZE.md / 最新冻结状态
4. ENGINE.md
5. NEW_PAGE_TEMPLATE.md

含义：
先装决策脑
→ 再确认任务是什么
→ 再确认做到哪里
→ 再读取当前节点执行方法
→ 最后按页面模板运行。

若是全新现实任务：
第2步先执行 INITIAL_TASK_INTAKE，
生成 CONTRACT_VERSION=1；
第3步建立 FREEZE_VERSION=0。

## 2. 页面角色

### CEO 页面
只允许一个 ACTIVE_CEO。
负责：
任务状态、节点拆分、依赖、派发、Merge、Reality Gate、版本、NEXT_PAGE_PROMPT。

### Executor 页面
一个页面只负责一个自然执行节点。
不得混用、不得改派第二节点。

## 3. Executor 页面模板

Executor 接单必须明确：
- TASK_ID
- CONTRACT_VERSION
- PARENT_FREEZE_VERSION
- NODE_ID
- NODE_GOAL
- DONE_WHEN
- HARD_BOUNDARIES
- INPUT/EVIDENCE
- OUTPUT_REQUIRED

页面内部：
VIRTUAL_LOOP
→ STOP_GATE
→ NODE_FREEZE

无论 PASS/FAIL/UNKNOWN/BLOCKED：
结果持久化
→ CEO 接受
→ 立即关闭页面。

禁止把已完成 Executor 留在专用浏览器里占资源。

## 4. CEO 控制节点

CEO 不按“每个执行节点必换页”。

每次收到并接受 Freeze 后：
更新 FREEZE_VERSION
→ 刷新当前状态
→ 判断是否需要新的控制决策
→ 执行 CEO_PAGE_ROTATION_GATE。

## 5. CEO_PAGE_ROTATION_GATE

优先顺序固定：

### A. PAGE_HEALTH_RISK
任一出现立即换页：
- 明显变慢、卡顿；
- 上下文明显变重；
- 出现过断连/卡死/恢复；
- 下一阶段是大任务/高思考；
- 当前页已经承担较多 Merge/规划。

### B. REPLAN_REQUIRED
任一出现立即换页：
- CONTRACT 修订；
- Reality Delta 改变路线；
- 需要重新选择架构/执行器；
- 依赖图实质变化；
- 进入语义明显不同的新阶段。

### C. CONTINUE_CURRENT_CEO
A/B 都否，且下一节点小、紧耦合、共享上下文高：
允许继续当前 CEO。

### D. HARD_CAP
同一 CEO 页：
MAX_CONSECUTIVE_FREEZES_PER_CEO=3

第三个 Freeze 完成后：
必须 CEO_FREEZE
→ 唯一 NEXT_PAGE_PROMPT
→ True New Chat
→ 新 CEO。

不需要做满3个。
任何时候 A/B 先触发就提前换。

## 6. CEO 唯一活动页

换页：

旧 CEO 先 Persist/Freeze
→ 生成唯一 NEXT_PAGE_PROMPT
→ True New Chat
→ 新 CEO 接管确认
→ 旧 CEO 关闭

逻辑上始终只有一个全局状态 writer。

BRANCH=FORBIDDEN。

## 7. Freeze 版本

全局任务状态：
FREEZE_VERSION 使用自然整数。

CEO 每正式接受一个改变项目状态的 Node Freeze：
N → N+1。

并行 Executor：
各自只生成不可变 NODE_FREEZE_ID；
不得自己抢全局版本号。

FAIL 也是状态变化，也必须进入新的 FREEZE_VERSION。

## 8. NEXT_PAGE_PROMPT 命名与正文

文件/逻辑名称：

NEXT_PAGE_PROMPT_V<FREEZE_VERSION>

第一条非空行必须是 CEO_FREEZE_TAG_JSON。

随后必须包含三行信封：

【页面名｜任务名｜序号｜虚/实】
状态机：<引擎/大脑/模板版本｜状态码｜节点>
时间锚：TASK_ACCEPTED=<时间>｜READY_STATE_START=<时间或null>｜CURRENT=<节点>｜T_VALID=<数值或null>｜T*=<数值或null>

然后只携带最小接管状态：
- REPO / REF / SKILL_PATH
- TASK_ID
- CONTRACT_VERSION
- FREEZE_VERSION
- FINAL_REALITY_GOAL
- 正反约束/FINAL_VALID 的权威路径
- 已冻结事实 ≤3 条
- OPEN_ITEMS
- NEXT_CONTROL_DECISION
- NEXT_NODE

禁止携带完整旧聊天。

## 9. 页面结束门禁

只有同时满足：

1. Freeze 已持久化；
2. 全局 FREEZE_VERSION 已更新；
3. NEXT_PAGE_PROMPT 已生成；
4. JSON 与 Freeze 一致；
5. 最终回复原样完整输出唯一 NEXT_PAGE_PROMPT；

当前 CEO 才允许结束。

CEO_PAGE_COMPLETE=NO 时不得自动换页。

## 10. 初次页与接续页

### 初次页
BRAIN
→ INITIAL_TASK_INTAKE
→ CONTRACT v1
→ FREEZE v0
→ ENGINE
→ PAGE_TOPOLOGY_GATE
→ 执行

### 接续页
BRAIN
→ TASK_CONTRACT
→ CURRENT_TASK_FREEZE
→ ENGINE
→ 刷新 NEXT_CONTROL_DECISION
→ 执行

接续页禁止重新解释已冻结目标和已接受成果。

## 11. 页面卫生

CEO：
最多3个连续 Freeze，且健康风险优先提前换。

Executor：
永远一页一节点，完成即关。

专用浏览器：
只开最少必要 Executor 页；
不预热空页；
完成一个关一个；
任务全部结束后不留无价值执行页。

一句话：

**页面运行模板只做三件事：按固定顺序恢复脑子/任务/状态；严格区分 CEO 和 Executor；在 Freeze 后用最小提示词无损换页。**
