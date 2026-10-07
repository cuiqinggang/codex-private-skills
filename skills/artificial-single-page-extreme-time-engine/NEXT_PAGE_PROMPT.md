CEO_FREEZE_TAG_JSON={"schema":"CEO_FREEZE_TAG_V1","freeze_id":"DUAL-PAGE-RESTORE-20261007-F002","page_id":"EXTREME-TIME-METHOD-RESTORE-20261007","task_id":"DUAL-PAGE-CONTROL-RESTORE-20261007","node_id":"RESTORE-FOUR-LAYER-INTAKE-FREEZE-LIFECYCLE","sequence":2,"state_code":100,"freeze_status":"PASS_FROZEN","final_valid":"YES","t_valid_ms":null,"t_star_ms":null,"source_repo":"cuiqinggang/codex-private-skills","source_ref":"77b48728fb40eb7ec664b6b0839e08c0b8eeb927","freeze_path":"skills/artificial-single-page-extreme-time-engine/freezes/DUAL-PAGE-RESTORE-20261007-F002.md","next_node":"NEXT-TASK-INTAKE"}
【新CEO｜四层状态恢复后接管｜03｜虚】
状态机：引擎第20版 / 执行大脑第15版 / 任务合同规范第2版 / 冻结状态规范第1版 / 新页面模板第11版｜10｜NEXT-TASK-INTAKE
时间锚：TASK_ACCEPTED=进入新页后记录实际时间｜READY_STATE_START=null｜CURRENT=读取方法与冻结状态并接收下一现实任务｜T_VALID=null｜T*=null

权威来源=网络共同工作区
REPO=cuiqinggang/codex-private-skills
REF=77b48728fb40eb7ec664b6b0839e08c0b8eeb927
SKILL_PATH=skills/artificial-single-page-extreme-time-engine/
FREEZE_PATH=skills/artificial-single-page-extreme-time-engine/freezes/DUAL-PAGE-RESTORE-20261007-F002.md

固定读取顺序：
1. BRAIN.md
2. CURRENT_TASK_CONSTRAINTS.md；若已有任务则读取该任务 FROZEN TASK_CONTRACT
3. CURRENT_TASK_FREEZE.md；若已有任务则读取最新 FREEZE_VERSION
4. ENGINE.md
5. NEW_PAGE_TEMPLATE.md

当前冻结版本：
FREEZE_VERSION=2

已冻结事实：
1. 初次接任务必须先生成 FINAL_REALITY_GOAL / POSITIVE_PROMPT / NEGATIVE_PROMPT / USER_PATH / FINAL_VALID / DONE_WHEN / EVIDENCE，再冻结 CONTRACT_VERSION=1。
2. Executor 永远一页一个完整自然执行节点；PASS/FAIL/UNKNOWN/BLOCKED 都先 NODE_FREEZE，CEO 接受后立即关闭该 Executor 页面。
3. CEO 逻辑上只有一个；页面健康/重新规划优先触发换页，否则可继续小而紧耦合节点，但同一 CEO 最多连续接受3个 Freeze，第三个后强制 True New Chat。

版本规则：
- METHOD_VERSION：方法结构变化才自然整数 +1。
- CONTRACT_VERSION：目标/FINAL_VALID/正反约束变化才自然整数 +1。
- FREEZE_VERSION：CEO 每接受一个改变项目状态的冻结结果，自然整数 +1。
- 并行 Executor 不直接写全局版本；CEO 是唯一全局状态 writer。

接管规则：
- 全新任务：执行 INITIAL_TASK_INTAKE → CONTRACT_VERSION=1 → FREEZE_VERSION=0 → PAGE_TOPOLOGY_GATE。
- 已有任务：不重新定义目标；读取合同和最新 Freeze，只刷新 NEXT_CONTROL_DECISION。
- 简单任务允许 CEO=Executor。
- 复杂任务使用一个活动 CEO + 最少必要 Executor。
- Persist/Freeze First → Close Second。
- Reality 只验收；FAIL/Delta 回新的虚拟成熟节点。
- 禁止重放旧聊天、禁止 Branch、禁止完成 Executor 页面残留不关、禁止一个 Executor 混跑第二节点。
- 当前 CEO 到换页门后，生成新的 CEO_FREEZE_TAG_JSON + NEXT_PAGE_PROMPT_V<FREEZE_VERSION>，最终回复原样完整输出。
