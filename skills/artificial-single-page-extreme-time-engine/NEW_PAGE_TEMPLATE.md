# 《新页面运行模板 第7版》

版本：第7版  
状态：CURRENT

## 1. 固定来源

权威来源=网络共同工作区  
REPO=cuiqinggang/codex-private-skills  
REF=<main或冻结commit>

只读 4 个文件：

ENGINE.md  
BRAIN.md  
CURRENT_TASK_CONSTRAINTS.md  
NEW_PAGE_TEMPLATE.md

禁止先去 C 盘找方法。

## 2. 三行信封

【页面名｜任务名｜序号｜虚/实】  
状态机：<版本｜状态码｜阶段>  
时间锚：TASK_ACCEPTED=<...>｜CURRENT=<...>｜ELAPSED=<...>｜T_VALID=<...>｜T*=<...>

四字段定位和时间锚保留；其余机器信息不默认进入提示词。

## 3. NEXT_PAGE_PROMPT

只传：

- 三行信封；
- 网络共同工作区来源；
- 当前任务；
- 最多 3 条冻结事实；
- 下一步；
- 真正必要的禁止项。

目标：约 10 行。

不默认携带：
CEO_FREEZE_TAG_JSON、长 SHA 清单、完整历史、HIPE/JEV 说明、DAG、长候选表、重复证据。

证据写文件，提示词只负责交接。

## 4. 页面规则

同一页内完成连续虚拟优化，直到下一轮不划算。  
不为单点优化换页，不做中途逐点 Reality。  
页面出现明显卡顿风险时，最小冻结后换页。

一句话：**共同工作区找方法，三行信封做交接，其余全部减掉。**
