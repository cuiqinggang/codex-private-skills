# 《当前任务冻结状态 第5版》

FREEZE_TAG=DPC-F005
TASK_ID=DUAL-PAGE-CONTROL-RESTORE-20261007
FREEZE_VERSION=5
RESULT_STATUS=PASS

## 当前冻结状态

- 冻结规范已归入《极限短时间执行大脑 第17版》，不再存在独立“冻结状态规范”技能文件。
- 实际冻结状态采用独立不可变版本文件：第1版、第2版、第3版、第4版、第5版自然数递增。
- 当前任务冻结短标签固定为 <TASK_SHORT>-F<NNN>；当前为 DPC-F005。
- NEXT_PAGE_PROMPT 与冻结版本绑定；实际提示词文件使用 NEXT_PAGE_PROMPT_V<N>.md。
- NEXT_PAGE_PROMPT.md 只保留当前版本指针，不再复制提示词正文。
- 当前方法：引擎第21版 / 执行大脑第17版 / 任务合同规范第3版 / 新页面模板第13版。

METHOD_REF=70f7d4ae84ed7dcdfb426db13a4987a2e187a143
NEXT_PAGE_PROMPT=skills/artificial-single-page-extreme-time-engine/NEXT_PAGE_PROMPT_V5.md
NEXT_NODE=NEXT-TASK-INTAKE
