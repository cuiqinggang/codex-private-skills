# 《新页面运行模板 第8版》

版本：第8版  
状态：CURRENT

## 1. 固定来源

每个新 CEO 页面必须先明确：

权威来源=网络共同工作区  
REPO=cuiqinggang/codex-private-skills  
SKILL_PATH=skills/artificial-single-page-extreme-time-engine/  
REF=<main或冻结commit>

禁止先去 C 盘找方法。

固定读取：

- ENGINE.md
- BRAIN.md
- CURRENT_TASK_CONSTRAINTS.md
- NEW_PAGE_TEMPLATE.md

## 2. 三行信封

【页面名｜任务名｜序号｜虚/实】  
状态机：<引擎版本/大脑版本｜状态码｜阶段>  
时间锚：TASK_ACCEPTED=<实际时间>｜CURRENT=<当前节点>｜ELAPSED=<整体已用>｜T_VALID=<数值或null>｜T*=<数值或null>

只强制保留四字段定位、状态机、时间锚。

## 3. NEXT_PAGE_PROMPT 最小格式

正常只写：

【<页面>｜<任务>｜<序号>｜<虚/实>】  
状态机：<...>  
时间锚：<...>

权威来源=网络共同工作区  
REPO=cuiqinggang/codex-private-skills  
SKILL_PATH=skills/artificial-single-page-extreme-time-engine/  
REF=<main或冻结commit>  
读取：ENGINE.md / BRAIN.md / CURRENT_TASK_CONSTRAINTS.md / NEW_PAGE_TEMPLATE.md

任务：<一句话>  
冻结事实：<最多3条>  
下一步：<一句话>

目标：约 10–12 行。

## 4. 不再默认携带

不默认携带 CEO_FREEZE_TAG_JSON、长 SHA 清单、完整历史、HIPE/JEV 说明、DAG、长候选表、重复证据。

证据写文件，提示词只负责交接。

一句话：**技能包地址写清楚，三行信封保留，其余只传下一步。**
