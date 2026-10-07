# 《新页面运行模板 第13版》

版本：第13版
升级来源：第12版
状态：CURRENT
唯一标准：T*=min(T_VALID)

## 1. 新 CEO 固定读取顺序

NEXT_PAGE_PROMPT 只显式要求四层，按顺序读取：

1. BRAIN.md
2. CURRENT_TASK_CONSTRAINTS.md / 当前 TASK_CONTRACT
3. FREEZE_PATH 指向的《当前任务冻结状态 第N版》
4. NEW_PAGE_TEMPLATE.md

BRAIN.md 是唯一方法入口；ENGINE.md 由 BRAIN 按当前节点需要调用，不在 handoff 重复列规则。

若是全新现实任务：
先按 BRAIN 执行 INITIAL_TASK_INTAKE，
生成 CONTRACT_VERSION=1；
随后生成《当前任务冻结状态 第1版》。

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

## 8. NEXT_PAGE_PROMPT：极简交接

NEXT_PAGE_PROMPT 的职责只有：

> 告诉新页“从哪里读、当前读哪一版冻结状态、下一步做什么”。

不得复制技能包正文。

文件/逻辑名称：

NEXT_PAGE_PROMPT_V<FREEZE_VERSION>

第一行只保留短冻结标签：

```text
FREEZE_TAG=<TASK_SHORT>-F<NNN>
```

例如：

```text
FREEZE_TAG=DPC-F004
```

随后只保留：

1. 三行信封；
2. REPO / REF / SKILL_PATH / FREEZE_PATH；
3. 四层读取顺序；
4. 任务一句话；
5. 下一步一句话。

目标：约 10–12 行。

禁止在 NEXT_PAGE_PROMPT 重复：
- 冻结规范；
- 版本升级规则；
- Executor 生命周期；
- CEO 换页门；
- Reality 规则；
- 正反约束正文；
- DONE_WHEN 全文；
- 已冻结事实长列表；
- JSON 状态对象；
- 旧聊天历史。

冻结规则由 BRAIN 唯一定义；实际当前状态由 FREEZE_PATH 指向的《当前任务冻结状态 第N版》提供。

## 9. 页面结束门禁

只有同时满足：

1. Freeze 已持久化；
2. 全局 FREEZE_VERSION 已更新；
3. NEXT_PAGE_PROMPT 已生成；
4. FREEZE_TAG 与 FREEZE_PATH 指向同一冻结版本；
5. 最终回复原样完整输出唯一 NEXT_PAGE_PROMPT；

当前 CEO 才允许结束。

CEO_PAGE_COMPLETE=NO 时不得自动换页。

## 10. 初次页与接续页

### 初次页
BRAIN
→ TASK_CONTRACT
→ 《当前任务冻结状态 第1版》
→ NEW_PAGE_TEMPLATE
→ 执行

### 接续页
BRAIN
→ TASK_CONTRACT
→ FREEZE_PATH 指向的《当前任务冻结状态 第N版》
→ NEW_PAGE_TEMPLATE
→ 从 NEXT_CONTROL_DECISION 继续

BRAIN 内部按需调用 ENGINE。
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
