# 《新页面运行模板 第16版》

版本：第16版
升级来源：第15版
状态：CURRENT
唯一标准：T*=min(T_VALID)

## 1. 新 CEO 两种固定读取顺序

### A. 初次待接现实任务

任务尚未产生，不存在《当前任务目标与正反约束 第N版》。

读取顺序：

1. BRAIN.md（《极限短时间执行大脑 当前版》）
2. FREEZE_PATH 指向的当前方法/上一任务最终冻结状态
3. NEW_PAGE_TEMPLATE.md（《新页面运行模板 当前版》）

真正收到任务以后，由 BRAIN 先生成：
- 《当前任务目标与正反约束 第1版》；
- 《当前任务冻结状态 第1版》。

然后再开始执行。

### B. 同一现实任务接续

任务已经存在时，读取顺序：

1. BRAIN.md（《极限短时间执行大脑 当前版》）
2. TASK_CONSTRAINTS_PATH 指向的《当前任务目标与正反约束 第N版》
3. FREEZE_PATH 指向的《当前任务冻结状态 第N版》
4. NEW_PAGE_TEMPLATE.md（《新页面运行模板 当前版》）

BRAIN.md 是唯一方法入口；ENGINE.md 由 BRAIN 按当前节点需要调用，不在交接提示词重复列规则。

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

### 8.1 人机双可读

人类可读内容以中文为主。

允许保留英文的仅限：
- 实际文件名；
- 仓库 / commit / 路径；
- 已冻结的短代码，如 `DPC-F006`；
- 必要的标准符号，如 `T_VALID`、`T*`。

其余显示字段优先使用中文，不得为了“机器感”堆英文缩写。

### 8.2 版本必须显式对齐

NEXT_PAGE_PROMPT 必须直接写清当前实际版本：

- 《人工单页面极限短时间引擎 第N版》；
- 《极限短时间执行大脑 第N版》；
- 已有任务时：《当前任务目标与正反约束 第N版》；
- 《当前任务冻结状态 第N版》；
- 《新页面运行模板 第N版》。

读取顺序中的每一项都必须能看出“文件名/路径 + 中文名称 + 当前版本”，禁止只写模糊的 `CURRENT` 或“最新版”。

### 8.3 最小正文

第一行使用短冻结标签：

```text
冻结标签=DPC-F006
```

其中代码串保持简短、稳定、可机器索引；中文“冻结标签”供人工审核。

随后只保留：

1. 三行信封；
2. 仓库 / 固定版本 / 技能包路径 / 冻结状态路径；
3. 带明确版本号的读取顺序；
4. 任务一句话；
5. 下一步一句话。

目标仍保持极简。

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

冻结规则由 BRAIN 唯一定义；实际当前状态由“冻结状态路径”指向的《当前任务冻结状态 第N版》提供。

## 9. NEXT_PAGE_PROMPT 母模板与平衡规则

从第16版起，NEXT_PAGE_PROMPT 固定分为两种母模板：**初次待接任务**与**同一任务接续**。

共同原则：
1. 先复制对应母模板；
2. 只替换变量；
3. 不临场新增规则段；
4. BRAIN / 任务目标文件 / Freeze / 页面模板已经存在的内容不重复；
5. 若结构确需改变，先升级《新页面运行模板》。

### 9.1 最小充分集

删除一个字段以后，如果新 CEO 仍能无歧义地：
- 找到权威来源；
- 确认当前方法/任务/冻结版本；
- 知道下一步；

则删除。

否则保留。

### 9.2 母模板A：初次待接现实任务

此时**没有任务目标与正反约束文件**，禁止伪造路径或版本。

```text
冻结标签=<方法/上一任务收口冻结短码>
【下一CEO页｜待接现实任务｜<序号>｜虚】
状态机：《人工单页面极限短时间引擎 第N版》/《极限短时间执行大脑 第N版》/《新页面运行模板 第N版》｜状态码10｜待接任务
时间锚：任务接受时间=进入新页后立即记录｜当前状态=读取方法并接单｜有效时间(T_VALID)=未产生｜当前最短(T*)=未产生

权威来源=网络共同工作区
仓库=cuiqinggang/codex-private-skills
固定版本=<固定commit>
技能包路径=skills/artificial-single-page-extreme-time-engine/
冻结状态路径=<当前方法/上一任务收口冻结路径>
读取顺序：BRAIN.md（《极限短时间执行大脑 第N版》）→ 冻结状态路径（《当前任务冻结状态 第N版》或方法收口冻结）→ NEW_PAGE_TEMPLATE.md（《新页面运行模板 第N版》）

任务：读取上述内容后接收现实任务。
下一步：接到任务后，由执行大脑生成《当前任务目标与正反约束 第1版》和《当前任务冻结状态 第1版》。
```

### 9.3 母模板B：同一现实任务接续

此时任务已经存在，必须显式携带任务目标版本路径。

```text
冻结标签=<任务短码-FNNN>
【下一CEO页｜<任务名>｜<序号>｜<虚/实>】
状态机：《人工单页面极限短时间引擎 第N版》/《极限短时间执行大脑 第N版》/《新页面运行模板 第N版》｜状态码<10/20/30/40/100>｜<当前状态>
时间锚：任务接受时间=<时间>｜当前状态=<当前节点>｜有效时间(T_VALID)=<数值/未产生>｜当前最短(T*)=<数值/未产生>

权威来源=网络共同工作区
仓库=cuiqinggang/codex-private-skills
固定版本=<固定commit>
技能包路径=skills/artificial-single-page-extreme-time-engine/
任务目标路径=<CURRENT_TASK_CONSTRAINTS_VN.md实际路径>
冻结状态路径=<CURRENT_TASK_FREEZE_VN.md实际路径>
读取顺序：BRAIN.md（《极限短时间执行大脑 第N版》）→ 任务目标路径（《当前任务目标与正反约束 第N版》）→ 冻结状态路径（《当前任务冻结状态 第N版》）→ NEW_PAGE_TEMPLATE.md（《新页面运行模板 第N版》）

任务：<一句话>
下一步：<一句话>
```

### 9.4 中文优先与禁止重复

人类可读字段默认中文。

只保留必要英文：
- 实际文件名；
- 仓库、commit、路径；
- 短代码；
- T_VALID、T* 等必要标准符号。

禁止把冻结规范、Executor 生命周期、CEO 换页门、Reality 规则、正反约束正文、DONE_WHEN 全文、长证据、JSON 状态对象复制进 NEXT_PAGE_PROMPT。

## 10. 页面结束门禁

只有同时满足：

1. Freeze 已持久化；
2. 全局 FREEZE_VERSION 已更新；
3. NEXT_PAGE_PROMPT 已生成；
4. “冻结标签”与“冻结状态路径”指向同一冻结版本；
5. 最终回复原样完整输出唯一 NEXT_PAGE_PROMPT；

当前 CEO 才允许结束。

CEO_PAGE_COMPLETE=NO 时不得自动换页。

## 11. 初次页与接续页

### 初次页
BRAIN
→ 当前方法/上一任务收口 Freeze
→ NEW_PAGE_TEMPLATE
→ 等待/接收现实任务
→ BRAIN 生成《当前任务目标与正反约束 第1版》
→ BRAIN 生成《当前任务冻结状态 第1版》
→ 执行

### 接续页
BRAIN
→ TASK_CONSTRAINTS_PATH 指向的《当前任务目标与正反约束 第N版》
→ FREEZE_PATH 指向的《当前任务冻结状态 第N版》
→ NEW_PAGE_TEMPLATE
→ 从当前下一控制决策继续

接续页禁止重新定义已冻结目标；只有目标/约束本身真正变化时才生成下一版任务目标文件。

## 12. 页面卫生

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
