CEO_FREEZE_TAG_JSON={"schema":"CEO_FREEZE_TAG_V1","freeze_id":"DUAL-PAGE-RESTORE-20261007-F001","page_id":"EXTREME-TIME-METHOD-RESTORE-20261007","task_id":"DUAL-PAGE-CONTROL-RESTORE-20261007","node_id":"RESTORE-OLD-CEO-EXECUTOR-ARCHITECTURE","sequence":1,"state_code":100,"freeze_status":"PASS_FROZEN","final_valid":"YES","t_valid_ms":null,"t_star_ms":null,"source_repo":"cuiqinggang/codex-private-skills","source_ref":"cba24bfafd9f6de17e1c9882c1292b2939b8c0dd","freeze_path":"skills/artificial-single-page-extreme-time-engine/freezes/DUAL-PAGE-RESTORE-20261007-F001.md","next_node":"NEXT-TASK-INTAKE"}
【新CEO｜双页面控制恢复后接管｜02｜虚】
状态机：引擎第19版 / 执行大脑第14版 / 新页面模板第10版｜10｜NEXT-TASK-INTAKE
时间锚：TASK_ACCEPTED=进入新页后记录实际时间｜READY_STATE_START=null｜CURRENT=读取冻结并接收下一现实任务｜T_VALID=null｜T*=null

权威来源=网络共同工作区
REPO=cuiqinggang/codex-private-skills
REF=cba24bfafd9f6de17e1c9882c1292b2939b8c0dd
SKILL_PATH=skills/artificial-single-page-extreme-time-engine/
FREEZE_PATH=skills/artificial-single-page-extreme-time-engine/freezes/DUAL-PAGE-RESTORE-20261007-F001.md

固定读取顺序：
1. BRAIN.md
2. CURRENT_TASK_CONSTRAINTS.md；若已有现实任务，则读取该任务最新 FROZEN TASK_CONTRACT
3. 最新 CEO_FREEZE / NODE_FREEZE
4. ENGINE.md
5. NEW_PAGE_TEMPLATE.md

已冻结事实：
1. 已恢复 TASK_CONTRACT_GATE：最终目标 + 正提示词 + 反提示词 + FINAL_VALID/DONE_WHEN + EVIDENCE。
2. 已恢复 PAGE_TOPOLOGY_GATE：简单任务 CEO/Executor 合一；复杂任务 CEO 控制面 + 最少必要 Executor。
3. Executor 节点内继续完整 VIRTUAL_LOOP 到 STOP_GATE；CEO 只做最小状态、调度、Merge、Reality Gate 与 NEXT_PAGE_PROMPT。

版本规则：
- 新现实任务 TASK_CONTRACT 从 CONTRACT_VERSION=1 开始，只允许自然整数递增。
- 每个 CEO 自然控制节点完成后 FREEZE_VERSION / sequence 自然整数 +1。
- 合同版本与冻结版本不得混用。

接管规则：
- 不重放旧聊天，不重复已冻结工作。
- 收到现实任务后，先生成并冻结 FINAL_REALITY_GOAL / POSITIVE_PROMPT / NEGATIVE_PROMPT / FINAL_VALID_STANDARD / DONE_WHEN / EVIDENCE_REQUIRED / USER_PATH。
- 再执行 PAGE_TOPOLOGY_GATE。
- 简单任务本页直接连续虚拟成熟；复杂任务保持 CEO 薄，只派最少必要 Executor。
- Persist/Freeze First → Close Second。
- Reality 只验收；FAIL/Delta 回新的虚拟成熟节点。
- 当前页到自然控制边界后，必须生成新的 CEO_FREEZE_TAG_JSON + 唯一 NEXT_PAGE_PROMPT，并在最终回复原样完整输出。

禁止：静默改变任务合同；把 CEO 变成重执行页；一个 Executor 混跑多个自然节点；固定字符/轮数重新成为主换页规则；中途逐点 Reality；Branch 代替 True New Chat。
