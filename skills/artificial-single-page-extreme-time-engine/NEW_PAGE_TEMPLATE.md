# 《新页面运行模板 第9版》

版本：第9版  
升级来源：第8版  
状态：CURRENT

## 1. 固定来源

每个新 CEO 页面必须先明确：

权威来源=网络共同工作区  
REPO=cuiqinggang/codex-private-skills  
SKILL_PATH=skills/artificial-single-page-extreme-time-engine/  
REF=<main或冻结commit>

固定读取：
- ENGINE.md
- BRAIN.md
- CURRENT_TASK_CONSTRAINTS.md
- NEW_PAGE_TEMPLATE.md

禁止先去 C 盘找方法。

## 2. 三行信封

【页面名｜任务名｜序号｜虚/实】  
状态机：<引擎版本/大脑版本｜状态码｜阶段>  
时间锚：TASK_ACCEPTED=<实际时间>｜USER_START=<实际/待测>｜CURRENT=<当前节点>｜T_SYSTEM_VALID=<数值或null>｜T_USER_VALID=<数值或null>｜T*=<数值或null>

## 3. 单页面边界

一个页面只服务一个明确任务/分支，但同一任务内部允许：
- 多轮连续虚拟成熟；
- ≤3 个成熟候选比较；
- 多个兼容优化组合；
- Reality Delta 后重新刷新。

禁止：
- 一个微优化就机械换页；
- 两个无关任务混页；
- 正式 Reality 中改 Freeze。

页面过长、卡顿或恢复风险开始明显上升时：
最小冻结 → 输出 NEXT_PAGE_PROMPT → 新页继续同一任务状态。

## 4. VIRTUAL_LOOP 页面结束门

若状态仍为 VIRTUAL_LOOP，且：
- STOP_GATE 未通过；
- 无 AUTH_GATE；
- 无 EXTERNAL_BLOCK；
- 页面也未触发 PAGE_HANDOFF；

则当前页面/回合不得以“下一步是……”结束。

必须直接继续下一轮虚拟优化。

若触发 PAGE_HANDOFF：
换页本身就是本轮动作，下一页必须继续 VIRTUAL_LOOP，不得把 handoff 当 STOP。

## 5. Reality 门

只有 VIRTUAL_OPTIMIZATION_STOP=YES 才允许 Freeze → Reality。

一个 Freeze 默认只允许一次 Reality。

Reality FAIL/Delta：
冻结真实差异 → 新虚拟状态 → 继续完整虚拟循环；
不得同页边改边补跑。

## 6. 用户入口门

用户型任务必须写清：
USER_START、用户操作步骤、SYSTEM_TAKEOVER、FINAL_VALID。

若只测到系统侧：
T_SYSTEM_VALID 可记录；
T_USER_VALID 必须保持 null/待测；
不得把 T_SYSTEM_VALID 冒充完整 T*。

## 7. NEXT_PAGE_PROMPT 最小格式

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
当前执行状态：<VIRTUAL_LOOP/FREEZE_READY/REALITY_ONCE/DELTA_RETURN/FINAL>  
下一步：<一句话>

目标：约 10–12 行。

## 8. 不再默认携带

不默认携带长 JSON、长 SHA 清单、完整历史、概率工具说明、DAG、长候选表、重复证据。

证据写文件，提示词只负责交接。

## 9. 页面结束门禁

生成 NEXT_PAGE_PROMPT 文件不等于完成。

需要换页时：
1. 当前最小冻结已写入；
2. 最终回复必须完整输出唯一 NEXT_PAGE_PROMPT；
3. 下一页能直接从明确状态继续；
4. 若状态是 VIRTUAL_LOOP，下一页第一动作就是继续虚拟循环。

一句话：**一个页面一个任务闭环；同页连续虚拟成熟；过重就换页接着跑，不得在停止门前停在计划层。**
