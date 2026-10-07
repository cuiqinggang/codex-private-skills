# NEXT_PAGE_PROMPT 极简化｜CEO Freeze 003

CEO_STATE_TAG={"schema":"CEO_STATE_V2","task_id":"DUAL-PAGE-CONTROL-RESTORE-20261007","freeze_version":3,"state_code":100,"next_node":"NEXT-TASK-INTAKE"}

FREEZE_VERSION=3
RESULT_STATUS=PASS
METHOD_FINAL_VALID=YES

## 当前方法版本

ENGINE_VERSION=20
BRAIN_VERSION=16
TASK_CONTRACT_SCHEMA_VERSION=2
CURRENT_TASK_FREEZE_SCHEMA_VERSION=2
NEW_PAGE_TEMPLATE_VERSION=12

## 本次冻结结论

1. NEXT_PAGE_PROMPT 只负责：权威地址、读取顺序、当前状态指针、任务一句话、下一步一句话。
2. BRAIN.md 升级为唯一方法入口；ENGINE.md 是其内部执行体，不再要求 handoff 重复列出或解释。
3. 新 CEO 显式四层读取顺序固定为：
   BRAIN → TASK_CONTRACT → CURRENT_TASK_FREEZE → NEW_PAGE_TEMPLATE。
4. 旧 CEO_FREEZE_TAG_JSON 长字段改为最小 CEO_STATE_TAG；详细状态只存在 Freeze 文件。
5. 版本规则、Executor 生命周期、CEO 三 Freeze 门、Reality 规则、正反约束正文、DONE_WHEN 等禁止在 NEXT_PAGE_PROMPT 重复。
6. NEXT_PAGE_PROMPT 目标长度约 10–12 行；能靠权威技能包恢复的内容，一律不复制。

## 极简原则

RULE_SINGLE_SOURCE_OF_TRUTH=YES
HANDOFF_IS_INDEX_NOT_MEMORY_DUMP=YES
DUPLICATED_RULES_IN_PROMPT=FORBIDDEN
FULL_HISTORY_REPLAY=NO

## 历史比较

旧简洁提示词方向正确：
三行信封 + 权威地址 + 读取 + 任务 + 下一步。

本次只补两个后来确有必要的新信息：
- FREEZE_PATH
- 最小 CEO_STATE_TAG

其余规则全部回归权威技能文件。
