CEO_FREEZE_TAG_JSON={"schema":"CEO_FREEZE_TAG_V1","freeze_id":"EXTREME-TIME-METHOD-V4-HIPE-V035-20261006-F001","page_id":"EXTREME-TIME-METHOD-REVIEW-20261006","task_id":"METHOD-REVISION-HIPE-V035-INTEGRATION","node_id":"METHOD-REVISION-COMPLETE","sequence":1,"state_code":100,"freeze_status":"PASS_FROZEN","final_valid":"YES","t_valid_ms":null,"t_star_ms":null,"source_repo":"cuiqinggang/codex-private-skills","source_ref":"bc7ca322c6a5ba4fcb5fa39d6b15c0682ad77bc6","freeze_path":"skills/artificial-single-page-extreme-time-engine/freezes/METHOD-REVISION-HIPE-V4-F001.md","next_node":"METHOD-VALIDATION-R0-TASK-DEFINE"}

执行《人工单页面极限短时间引擎 第7版》。

权威来源：
REPO=cuiqinggang/codex-private-skills
REF=bc7ca322c6a5ba4fcb5fa39d6b15c0682ad77bc6
ENGINE_PATH=skills/artificial-single-page-extreme-time-engine/ENGINE.md
BRAIN_PATH=skills/artificial-single-page-extreme-time-engine/BRAIN.md
TASK_PATH=skills/artificial-single-page-extreme-time-engine/CURRENT_TASK_CONSTRAINTS.md
TEMPLATE_PATH=skills/artificial-single-page-extreme-time-engine/NEW_PAGE_TEMPLATE.md
HIPE_INTEGRATION_PATH=skills/artificial-single-page-extreme-time-engine/HIPE_V035_INTEGRATION_FREEZE.md

HIPE 冻结来源：
HIPE_PATH=skills/hybrid-intelligence-probability-engine-v0-3-5/
HIPE_FREEZE_COMMIT=c6fe2878fd237e7a8120b3af8e75f93e3cd6a4d9
HIPE_FREEZE_ID=HIPE-v0.3.5-FULLY-SEALED-20261006-R1

依次读取：
1. BRAIN.md
2. CURRENT_TASK_CONSTRAINTS.md
3. ENGINE.md
4. NEW_PAGE_TEMPLATE.md
5. HIPE_V035_INTEGRATION_FREEZE.md

任务：进入 METHOD-VALIDATION-R0-TASK-DEFINE。

这是一个全新的方法 Reality 验证任务，不执行 Greenfield-R11，不继承 R1-R10 的具体实现、参数、阈值、claim 或优化链。R1-R10 只作为方法失败反例。

目标：重新从第1步定义一个同类现实任务，冻结新的 TASK_ACCEPTED、VALID、READY_STATE、权威工作区、生产闭环和验收方式，然后按新版流程：
Reality Solvability Gate v0.2.0
→ 成熟方案集群
→ Comfort-Zone Forward Compiler v0.2.0
→ CODE / JEV / GPT residual
→ 最大合法并行
→ 连续虚拟成熟
→ 整包 Freeze
→ Reality
→ deterministic verifier
→ FINAL_VALID。

Reality 轮数：
TARGET=3..4
HARD_MAX=5
若提前稳定成熟则提前 STOP；第5轮仍未收敛必须停止并复盘，不得继续派生 R6/R7/R8 式微版本。

本节点只完成“重新定义新任务 + 冻结 R0”，不要在同一节点直接复用旧 Greenfield 实现。

所有冻结出口必须使用《新页面运行模板 第4版》的 CEO_FREEZE_TAG_JSON；缺失或与冻结记录不一致则 CEO_PAGE_COMPLETE=NO。
