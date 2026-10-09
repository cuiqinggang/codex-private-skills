# 《第29版统一引擎升级任务目标与正反约束》第1版
TASK_ID=ENGINE29_UNIFIED_N8N_20261010
CONTRACT_VERSION=1
METHOD=ENGINE29/BRAIN25/NEW_PAGE_TEMPLATE18
STATUS=ACTIVE
UPGRADE_FROM=ENGINE28
ARCHIVED_DESIGN=routes/A（旧A28/A29）；routes/B（旧B29—B33）；tasks/AB_ROUTE_SPLIT_20261009；tasks/A29_CEO_DEDICATED_BROWSER_20261010
MATURE_EXECUTION_BASELINE=n8n原生工作流+Microsoft Playwright MCP+既有专用AI浏览器+GPT直连Windows双路执行桥v0.3.1

## 唯一目标
撤销“新任务必须先选择A或B”的分路线机制，恢复原成熟第28版的CEO/Executor分工及n8n执行底座，直接将共同《自动化单页面极限短时间引擎》第28版按整数顺序升为29版。吸收原B33的一页简单任务、更短冻结状态码索引、按需增加执行页、只读并行预取等有价值且不破坏原架构的规则，不使用B33被停止/保护的发送器。整个方案只在**一个原来已登录的专用AI浏览器**中运行CEO主控标签和必要时的0..N个Executor独立标签。今天先完成正式方法发布和任务冻结，明天开展最小差分审查/合法测试。

## 正向约束
- 简单任务默认CEO原页直接完成，零Executor、无强制跨页；复杂任务CEO分派独立自然节点，按需开Executor标签，完成Freeze→CEO合并→只清理自有已完成标签。
- 永远只有一个ACTIVE_CEO和任务状态唯一写者；不同Executor的NODE_FREEZE互不覆盖主任务FREEZE；唯一浏览器并不意味着同标签/会话/共享焦点没有冲突。
- 以成熟n8n原生工作流作为需要可靠外部触发、调度、队列、持久去重、等待恢复、冲突协调与对账的固定**执行底座**。GPT负责思考/决策/验收，n8n承担执行编排；不强制简单GPT答复空跑n8n节点，不改造为无n8n的B33方案。
- 现成 Playwright MCP 控制原专用浏览器 CDP127.0.0.1:9223，复用既有Windows双路执行桥v0.3.1与GitHub Freeze。除成熟组件配置映射/最薄适配外禁止开发调度器、状态机、锁或浏览器控制服务。
- 照原 ENGINE28 的REUSE_GATE、时间唯一标准、成熟现实基线→整套虚拟成熟→Freeze→一次最终Reality、安全授权和三态 Exactly-once约束执行。
- 保留 n8n 任务 N8N_MCP_SHARED_20261009 合同第1版与F002原样作为历史GOOD证据；不重复它已经通过的n8n MCP读写、去重、Wait恢复、跨流程串行、写后不重写测试。
- B33成果只选择性吸收：短状态码**索引思想**、两轮独立只读预取、单页简单任务路径。其代码 `B33_Handoff.ahk` 保护锁与之前平台拒绝仍保留，严禁用于ENGINE29实际发送，保留旧任务 STOP历史。旧 A29 单独路线不再是活动入口，原A/B所有版本/冻结/任务文件均保留可查。
- 不更改FlClash/浏览器Profile，不启动第二浏览器；未经批准不得自动发送ChatGPT业务消息或操作未归属标签。

## 反向约束与当前事实
- 禁止把“第29版方法已发布”写成“现实自动接续已通过”。原n8n F002虽有组件现实PASS，但跨客户端同资源仲裁、不同目标实际写并行、异常释放、UNKNOWN对账、正式GPT新页接管及完整T_VALID仍未全部验证。
- 禁止再次建立B34或重新开启A/B方案选型；禁止覆盖B33 STOP任务的历史合同、源文件与冻结。
- B33之前网页自动发送相关工具遭预派发安全拒绝；不得切换n8n/CDP/UIA绕过同一已拒绝行为。只有平台明确允许的正常执行入口才可进入此副作用测试。
- 第29版如需CEO轮换，先真Freeze，再合法新CEO接管确认，最后安全退役旧CEO；失败保留旧页并输出简短人工恢复提示词。不得关当前用户聊天。

## 成功验收
本次方法升级的完成条件：ENGINE28原文档封存、当前ENGINE29与SKILL/START单一入口一致、独立合同/Freeze/CURRENT真实可读；原有B和A历史未删，n8n F002未改；次日只做布局归属与执行底座的差分验证。该方法升级验收不替代生产业务FINAL_VALID及同边界T_VALID。