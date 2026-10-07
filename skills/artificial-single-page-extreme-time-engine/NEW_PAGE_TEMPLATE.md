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
状态机：<引擎版本/大脑版本｜状态码｜当前自然节点>  
时间锚：TASK_ACCEPTED=<实际时间>｜READY_STATE_START=<实际/待定>｜CURRENT=<当前节点>｜T_VALID=<数值或null>｜T*=<数值或null>

USER_PATH_GATE 单独写：
USER_PATH=<最简用户操作>｜USER_PATH_GATE=<PASS/FAIL/UNFROZEN>

不把人工手速混入 T_VALID。

## 3. 一个页面 = 一个自然任务节点

每页只能服务一个明确自然任务节点/分支。

该节点内部允许：
- 多轮连续虚拟成熟；
- ≤3 个成熟候选比较；
- 多个兼容优化组合；
- Reality Delta 后重新刷新。

禁止：
- 一个微优化就机械换页；
- 在节点 VIRTUAL_LOOP 中停在计划层；
- 一个页面继续执行下一个自然节点；
- 正式 Reality 中修改 Freeze。

当前自然节点一旦完成并 Freeze：
当前页面立即结束/回收；
下一自然节点必须开新页面。

冻结文件/证据保留，不能因页面结束而丢失。

## 4. VIRTUAL_LOOP 页面结束门

若当前自然节点仍是 VIRTUAL_LOOP，且：
- STOP_GATE 未通过；
- 无 AUTH_GATE；
- 无 EXTERNAL_BLOCK；

则当前页面/回合不得以“下一步是……”结束。

必须直接继续下一轮虚拟优化。

只有该自然节点达到 FREEZE_READY/NODE_FINAL，才允许页面正常结束。

## 5. Reality 门

只有 VIRTUAL_OPTIMIZATION_STOP=YES 才允许 Freeze → Reality。

一个 Freeze 默认只允许一次 Reality。

Reality FAIL/Delta：
冻结真实差异 → 回到该节点的新 VIRTUAL_LOOP；
继续完整虚拟成熟；
不得边改边补跑。

复杂项目应把：
虚拟成熟节点、Reality 节点、Delta 修复节点
拆成独立自然节点/独立页面，靠 Freeze 接续。

## 6. 用户路径门

用户型任务必须在方案设计时明确最简 USER_PATH。

只要存在成熟方式能减少用户操作，就必须纳入候选比较。

USER_PATH_GATE=FAIL：
不得进入正式冠军候选。

但 T_VALID 仍只从电脑端合法 READY_STATE_START 到 FINAL_VALID 计算。

## 7. NEXT_PAGE_PROMPT 最小格式

正常只写：

【<页面>｜<任务>｜<序号>｜<虚/实>】  
状态机：<...>  
时间锚：<...>  
USER_PATH=<...>｜USER_PATH_GATE=<...>

权威来源=网络共同工作区  
REPO=cuiqinggang/codex-private-skills  
SKILL_PATH=skills/artificial-single-page-extreme-time-engine/  
REF=<main或冻结commit>  
读取：ENGINE.md / BRAIN.md / CURRENT_TASK_CONSTRAINTS.md / NEW_PAGE_TEMPLATE.md

当前节点冻结事实：<最多3条>  
下一自然节点：<一句话>

目标：约 10–12 行。

## 8. 不再默认携带

不默认携带长 JSON、长 SHA 清单、完整历史、概率工具说明、DAG、长候选表、重复证据。

证据写文件，提示词只负责交接。

## 9. 页面结束门禁

自然节点 Freeze 后必须：
1. 写入最小冻结；
2. 生成唯一 NEXT_PAGE_PROMPT；
3. 最终回复完整输出该 NEXT_PAGE_PROMPT；
4. 当前页面不再继续下一节点。

下一页：
只读取冻结事实；
不重复上一页已完成工作；
立即执行下一自然节点。

一句话：**一个页面一个自然节点；节点内部连续虚拟成熟到停止门；节点一冻结就换页，保持上下文永远短。**
