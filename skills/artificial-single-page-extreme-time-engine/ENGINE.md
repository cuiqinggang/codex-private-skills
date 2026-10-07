# 《人工单页面极限短时间引擎 第19版》

版本：第19版  
升级来源：第18版  
状态：CURRENT  
唯一标准：T*=min(T_VALID)

## 1. 权威来源

权威来源=网络共同工作区  
REPO=cuiqinggang/codex-private-skills  
PATH=skills/artificial-single-page-extreme-time-engine/

禁止先去 C 盘找方法；C 盘只作为执行、缓存与产物落点。

## 2. 第19版的核心校准

第18版“一个页面=一个自然任务节点”校准为：

> **一个 Executor 执行页面 = 一个完整自然执行节点。简单任务允许 CEO 与 Executor 合一；复杂任务必须分离 CEO 控制面与 Executor 执行面。**

因此：
- 小任务：一个 CEO 页面能完整成熟并验收，就不额外开 Executor；
- 大任务：一个薄 CEO 控制页 + 最少必要的 Executor 页面；
- 页面数量不是目标，最小完整 T_VALID 才是目标；
- 页面可以不断关闭和重建，冻结状态必须连续存在。

## 3. TASK_CONTRACT_GATE：任务宪法先冻结

任何新任务先在 CEO 形成任务合同，再允许执行。

合同至少冻结：
- FINAL_REALITY_GOAL：最终现实目标，只写要得到什么，不写实现偏好；
- POSITIVE_PROMPT：必须实现、必须保留的正向要求；
- NEGATIVE_PROMPT：禁止出现、出现即漂移/失败的反向要求；
- FINAL_VALID_STANDARD / DONE_WHEN：什么才算真正完成；
- EVIDENCE_REQUIRED：用什么证据证明完成；
- IN_SCOPE / OUT_OF_SCOPE / HARD_BOUNDARIES；
- USER_PATH：用户最简现实操作路径。

生成顺序：

用户原始任务
→ 提炼最终现实结果
→ 提炼正向要求
→ 提炼反向禁止项
→ 把完成条件改写为可验收 DONE_WHEN
→ 定义证据
→ 检查是否与用户真实意图、现实物理条件、成熟标准一致
→ Freeze CONTRACT_VERSION=1

任务合同是 Source of Truth。聊天、CEO、Executor、临时计划不得静默改写它。

只有当最终目标、FINAL_VALID 标准、正向约束或反向约束本身确实需要改变时，才显式：
CONTRACT_VERSION=N → N+1。

普通节点推进、执行路线变化、Reality Delta、页面换页都不得自动提升 CONTRACT_VERSION。

## 4. PAGE_TOPOLOGY_GATE：只判断两种拓扑

### A. SIMPLE_SINGLE_PAGE

适用于一个页面可稳定闭环的简单任务：

CEO=Executor
→ USER_PATH_GATE
→ VIRTUAL_LOOP
→ STOP_GATE
→ Freeze
→ Reality（需要时）
→ FINAL

### B. CEO_EXECUTOR

适用于多阶段、长流程、Reality、等待、可并行、失败恢复或单页明显过重的任务：

CEO 控制面
→ 拆最小完整可独立验收节点
→ 按依赖派发最少必要 Executor
→ Executor 各自完成节点并 Freeze
→ CEO Merge
→ 下一节点 / Reality / CEO Freeze

CEO 不承载重执行历史。

## 5. Executor 节点内部算法不变

每个 Executor 完整执行：

成熟 BASELINE
→ 算现实 NET_GAIN
→ 选当前最大净收益点
→ ≤3 个成熟候选
→ 选 1 个
→ 虚拟替换并刷新完整节点方案
→ 重算 NET_GAIN
→ 自动进入下一轮
→ STOP_GATE
→ NODE_FREEZE

进入 VIRTUAL_LOOP 后，未满足合法出口前不得停在“下一步建议”。

合法出口只有：
1. STOP_GATE；
2. AUTH_GATE；
3. EXTERNAL_BLOCK。

## 6. Reality 仍然只是验收器

禁止：
优化一点 → Reality → 再优化一点 → Reality。

正确：

连续虚拟成熟到底
→ Freeze
→ 一次正式 Reality
→ PASS 或 Reality Delta

若 FAIL/Delta：
- 已通过事实继续冻结；
- 只把真实差异送回新的虚拟节点；
- 从失败点刷新后续完整方案；
- 再连续成熟到 STOP_GATE；
- 新 Freeze；
- 再做整体 Reality。

## 7. CEO 的职责必须保持薄

CEO 只维护：
- 当前任务合同版本；
- 当前 FREEZE_VERSION / sequence；
- 已冻结节点；
- 未完成节点；
- 依赖关系；
- Executor 分配；
- Merge；
- Reality Gate；
- 当前 T*；
- 下一控制节点；
- NEXT_PAGE_PROMPT。

CEO 不承载：
- 长搜索过程；
- 大量代码日志；
- 几十轮虚拟尝试；
- 完整浏览器执行历史。

这些属于 Executor 或证据文件。

## 8. 串行 / 并行

先判断：

DEPENDENCY / SHARED_WRITE / SCARCE_RESOURCE_CONFLICT ?

YES → SERIAL

NO → 只有预计并行能降低完整 T_VALID 才 PARALLEL。

原则：
- 能并行不等于必须并行；
- 不为了简单而强制串行；
- 一个专用 persistent browser 内可以有受控 Executor 页面；
- 不恢复第二套专业浏览器、无限页面、多 writer owner；
- 默认只开最少必要页面，旧“3页”只作为候选上限/Reality经验，不是固定配额。

## 9. Freeze First → Close Second

Executor 或 CEO 页面结束固定顺序：

任务/控制节点完成
→ Freeze 持久化结果、证据、Delta、状态
→ 上层确认可恢复
→ 页面失去继续观察/恢复价值
→ Close

页面可以删除；冻结状态不能删除。

## 10. CEO 跨页连续性

复杂任务不要求一个 CEO 页面做完。

CEO 到达自然控制边界：
→ CEO_FREEZE
→ FREEZE_VERSION=N→N+1
→ 写最小状态
→ 生成唯一 NEXT_PAGE_PROMPT
→ 最终回复原样输出
→ True New Chat 新 CEO
→ 旧 CEO 页面结束

新 CEO 只继承：
- 任务合同；
- 当前冻结结论；
- 证据位置；
- 已完成/未完成节点；
- 当前 T*；
- 下一唯一动作。

原则：
CONCLUSION_SURVIVES_HISTORY_DOES_NOT。

## 11. 三套版本必须分离

### 方法版本
如第19版、第14版、第10版。
只有方法发生系统性变化才升级。

### CONTRACT_VERSION
每个现实任务从 1 开始。
只有目标/VALID/正反约束改变才自然数 +1。

### FREEZE_VERSION / sequence
每完成一个 CEO 自然控制节点就自然数 +1。
它表示“做到哪里”，不表示目标改变。

禁止小数版本用于上述任务合同和冻结序列。

## 12. 时间与用户路径

T_VALID 继续按电脑端合法 READY_STATE 到 FINAL_VALID：

T_VALID = FINAL_VALID - READY_STATE_START

T*=min(T_VALID)

用户人工手速不强塞进 T_VALID，但方案必须通过 USER_PATH_GATE：
- 操作现实可行；
- 尽量短、简单、可重复；
- 成熟方式能减少用户操作时应纳入候选。

## 13. 硬规则

禁止任务合同静默漂移。  
禁止 CEO 承载重执行历史。  
禁止一个 Executor 页面混跑多个自然节点。  
禁止自然节点 Freeze 后继续堆上下文。  
禁止中途逐点 Reality。  
禁止 VIRTUAL_LOOP 未到合法出口就停止。  
禁止自研优先、从零重建优先。  
禁止固定字符/轮数重新成为主触发器；它们只允许做 fallback。  
禁止为了多智能体而多智能体。  
禁止页面关闭先于 Freeze。  
禁止新 CEO 重放全部旧聊天。

一句话：

**先冻结“不漂移的任务宪法”；小任务 CEO/Executor 合一，大任务 CEO/Executor 分离；Executor 负责节点内部连续成熟，CEO 负责节点之间的最小状态、调度、合并和跨页继承。**
