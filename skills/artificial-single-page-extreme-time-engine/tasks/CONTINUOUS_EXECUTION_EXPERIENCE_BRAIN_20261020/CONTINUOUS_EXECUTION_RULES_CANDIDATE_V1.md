# 连续执行与经验复用方法增量 V1（候选，未激活）
STATUS=CANDIDATE_NOT_ACTIVE
PARENT_BRAIN=25
OWNER=SANRENXING_V4
## 任务入口（不可跳过）
用户现实任务→TASK_ID→当前任务目标与正反约束V1→当前任务Freeze V1→既有REUSE_GATE→执行。已有TASK_ID只读最新合同和Freeze，不重新发明目标。合同变动才升CONTRACT_VERSION，现实状态变动才升FREEZE_VERSION，方法变动且验证通过才升METHOD_VERSION。
## 成熟岗位检索
根据业务特征查知识大脑Top-K→现有成熟Skill/SOP→Agency Agents等专业岗位成熟模板→必要时公开成熟方案；仅做最小同合同比较。匹配岗位优先进入候选，通用GPT也可参与比较；以质量、可靠性、全部协调与返工时间、维护成本选择。角色不等于常驻进程；任务路由不等于新增调度器。
## 连续执行
同一任务使用已有轻量状态持久化记录唯一TASK_ID、合同路径、FREEZE_PATH、last_verified、next_node、owner、回执和副作用状态。单节点PASS自动保存并接续下一可运行节点，无需人工发继续。页面/会话需要交接时生成NEXT_PAGE_PROMPT，明确禁止声称普通聊天模型必然能在会话终止后自动自行发起下一页；跨会话继续依赖已验证触发器。需要审批/缺失权限/无法验证或UNKNOWN则持久化阻塞并只报告真实状态。
## 故障直接命中经验
先查询已证实的错误指纹：现象、触发、环境、首次异常边界、根因、最小修复、回归命令、适用与反例、证据和版本。高匹配且版本兼容则调用既有成熟技能并回归；否则LAST_GOOD→GOOD/BAD→FIRST_DELTA→成熟方案检索→最小修复→Regression。复发更新同一经验，不重复造同义Skill。
## 每日21:00
由现有单一“每日21点决策与经验大脑复盘”任务增量记录CASE/ERROR/CANDIDATE_RULE/STABLE_RULE/SKILL_CANDIDATE/PROJECT_STATE，去重保存C盘已有Vault/Knowledge Brain。一次成功只候选，证据足够才提升稳态规则。只记录已知任务合同路径与Freeze，不自动在夜间重发业务写操作。
## 停止门
FINAL_VALID有独立证据才DONE；需要审批→WAITING_APPROVAL；副作用UNKNOWN→WAITING_RECONCILIATION；工具失效→BLOCKED_TOOL；无法自动跨会话接续→PERSISTED_NEEDS_TRIGGER。任何一种都须保留冻结事实。
## 启用门
此文件仅为方法升级候选；需使用真实但安全的短任务验证：自动相邻节点推进、断点恢复、故障旧解法命中、严格遵守合同/Freeze、夜间任务可回读与去重后，才能正式升级BRAIN25及引用入口。禁止未验收就声称全系统已激活。
