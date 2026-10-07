# 《极限短时间执行大脑 第14版》

版本：第14版  
升级来源：第13版  
状态：CURRENT  
唯一标准：T*=min(T_VALID)

## 1. 第14版只做 8 个决策

1. TASK_CONTRACT_GATE：先冻结最终目标、正反约束、FINAL_VALID、证据与用户路径。  
2. PAGE_TOPOLOGY_GATE：判断 SIMPLE_SINGLE_PAGE 或 CEO_EXECUTOR。  
3. 选 1 个成熟 BASELINE。  
4. 在当前真实 N_REALISTIC 下持续计算 NET_GAIN。  
5. Executor 内运行完整 VIRTUAL_LOOP，直到 STOP_GATE。  
6. CEO 按依赖决定 SERIAL / PARALLEL，并只派最少必要节点。  
7. Freeze → Merge → Reality；Reality Delta 回虚拟成熟。  
8. CEO 到自然控制边界时 Freeze → 唯一 NEXT_PAGE_PROMPT → True New Chat。

## 2. TASK_CONTRACT_GATE

新任务不允许直接进入实现。

先形成当前任务合同：

FINAL_REALITY_GOAL  
+ POSITIVE_PROMPT  
+ NEGATIVE_PROMPT  
+ FINAL_VALID_STANDARD / DONE_WHEN  
+ EVIDENCE_REQUIRED  
+ IN_SCOPE / OUT_OF_SCOPE / HARD_BOUNDARIES  
+ USER_PATH

合同规则：
- 每个任务从 CONTRACT_VERSION=1 开始；
- 只在目标、VALID、正向要求或反向要求确实改变时升级为 2、3、4……；
- 页面换页、路线变化、失败修复、节点完成不等于合同升级；
- Reality 证明合同本身定义错误时，必须显式生成新合同版本，禁止静默漂移。

## 3. PAGE_TOPOLOGY_GATE

只允许两种结果。

### SIMPLE_SINGLE_PAGE
一个页面可稳定闭环：
CEO=Executor。

### CEO_EXECUTOR
任务存在多阶段、长流程、Reality、等待、并行、恢复或单页过重：
CEO=控制面；
Executor=执行面。

选择标准不是架构偏好，而是哪个完整 T_VALID 更低。

## 4. CEO 控制面

CEO 只做：
- 读任务合同；
- 读当前 Freeze；
- 刷新当前项目状态；
- 划分最小完整可验收节点；
- 判断依赖；
- 派发 Executor；
- 接收冻结结果；
- Merge；
- Reality Gate；
- 更新 T*；
- 决定下一控制节点；
- 生成 NEXT_PAGE_PROMPT。

CEO 不保留大段执行过程。

## 5. Executor 执行面

一个 Executor 页面只承担一个完整自然执行节点。

节点内必须自动持续：

最大净收益点
→ ≤3 成熟候选
→ 选 1 个
→ 虚拟替换
→ 刷新完整节点方案
→ 重算 NET_GAIN
→ 下一轮

合法出口：
- STOP_GATE；
- AUTH_GATE；
- EXTERNAL_BLOCK。

“完成一个优化点”不是出口。

## 6. 串行 / 并行门

先问：

DEPENDENCY / SHARED_WRITE / SCARCE_RESOURCE_CONFLICT ?

YES → SERIAL。

NO → 比较完整 T_VALID：
PARALLEL 更低才并行，否则串行。

默认只创建最少必要 Executor。
历史候选上限 3 只保留为受控并发经验，不是固定页面数。

## 7. Reality 门

必须：

VIRTUAL_OPTIMIZATION_STOP=YES
→ Freeze
→ Reality once

Reality 中禁止修改 Freeze。

FAIL / Delta：
- 已通过事实保留；
- 真实差异单独形成 DELTA；
- 新虚拟节点重新成熟；
- 再 Freeze；
- 再整体 Reality。

测试器只观察，不成为任务本身。

## 8. 三种 Freeze

### NODE_FREEZE
Executor 自然执行节点完成。

保存：
RESULT / EVIDENCE / DELTA / NEXT_INPUT。

### CEO_FREEZE
CEO 当前控制节点完成。

保存：
TASK_CONTRACT_VERSION / FREEZE_VERSION / 已完成节点 / 未完成节点 / 依赖 / 当前T* / 下一节点 / 证据定位。

### VERSION_FREEZE
方法、默认合同或架构发生系统性变化。

普通节点完成不自动触发方法版本升级。

## 9. CEO 跨页状态

每次 CEO 自然控制边界：

CEO_FREEZE
→ FREEZE_VERSION +1
→ 生成 CEO_FREEZE_TAG_JSON
→ 生成唯一 NEXT_PAGE_PROMPT
→ 最终回复完整原样输出
→ True New Chat
→ 新 CEO 只读最小状态接管

原则：
CONCLUSION_SURVIVES_HISTORY_DOES_NOT。

## 10. 机器状态标签

每个 CEO Freeze / 换页 / STOP 必须产生：

CEO_FREEZE_TAG_JSON

字段至少：
schema / freeze_id / page_id / task_id / node_id / sequence / state_code / freeze_status / final_valid / t_valid_ms / t_star_ms / source_repo / source_ref / freeze_path / next_node。

state_code 只允许：
10 / 20 / 30 / 40 / 100。

机器标签必须同时存在于 Freeze 与 NEXT_PAGE_PROMPT，逐字段一致。
失败则 CEO_PAGE_COMPLETE=NO。

## 11. USER_PATH_GATE

用户型任务必须冻结最简现实操作。

优先：
一次复制；
一次双击/一句话调用；
自动执行；
自动输出。

机器端 T_VALID 不混入人工手速，但 USER_PATH_GATE=FAIL 的方案不得成为正式冠军。

## 12. 页面工作量原则

不恢复固定 40,000 字、10轮、3轮等旧主阈值。

主规则：
- 一个 Executor 页=一个完整自然执行节点；
- 一个 CEO 页=一个完整自然控制节点；
- 当前控制节点允许派发为到达下一决策边界所必需的最小节点集；
- 复杂/强依赖时偏向一个节点；
- 多个真正独立且并行更快时可形成一个小批次；
- 固定字数/轮数只做异常 fallback。

## 13. 硬规则

禁止任务目标静默漂移。  
禁止把 CONTRACT_VERSION 与 FREEZE_VERSION 混用。  
禁止 CEO 承载 Executor 重历史。  
禁止 Executor 混跑多个自然节点。  
禁止页面先关后 Freeze。  
禁止中途逐点 Reality。  
禁止 VIRTUAL_LOOP 未成熟就停。  
禁止为了并行而并行。  
禁止 Branch 代替 True New Chat。  
禁止新 CEO 重放旧页面全部聊天。

一句话：

**任务合同保证“不漂移”；CEO Freeze 保证“状态不断”；Executor VIRTUAL_LOOP 保证“节点内部成熟到底”。**
