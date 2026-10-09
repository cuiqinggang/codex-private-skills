# 《B单层自动化成熟任务目标与正反约束 第4版：专用浏览器》
TASK_ID=B_SINGLE_PAGE_MATURITY_20261009
CONTRACT_VERSION=4
PREVIOUS_CONTRACT_VERSION=3
ROUTE=B
METHOD_ENGINE=B33
METHOD_BRAIN=B29
METHOD_TEMPLATE=B23
TASK_BROWSER_VARIANT=EXISTING_DEDICATED_CHROME_CDP_9223
GLOBAL_B_ROUTE_CHANGE=NO
STATUS=IN_PROGRESS

## 目标
用户明确把本任务的实际联通测试从普通Chrome改为已经登录的专用AI Chrome for Testing。GPT在合法自然任务节点完成并真实Freeze后，使用获准成熟浏览器能力在原专用会话自动新建ChatGPT聊天、一次提交正确四字段短码；新GPT从GitHub独立读取当前合同与Freeze，继续原业务并达到FINAL_VALID。整个交接无人手动操作，完成后才分析极限短时间。本V4仅改变本任务浏览器约束，不回溯改写原V3和B33公共路线。

## 正向约束
- 优先复用正在运行的专用AI Chrome及已安装微软Playwright MCP STDIO，已有CDP接口127.0.0.1:9223；不新建浏览器/配置文件、不关闭用户现有ChatGPT页、不改FlClash。
- 使用已有GitHub Freeze/CURRENT恢复，不增加自研调度器/锁/状态机/n8n常驻层；n8n只能在明确需要时作为成熟可选持久工作流组件。
- 先实际官网自动联通并得到同质量业务结果，后再做速度比较和虚拟极限优化；没有真人操作的自动闭环才能作为自动候选VALID。
- 必须区分普通Chrome与专用Chrome；不得将离线HTML动作计时或MCP只读工具发现换算成真实官网发送/完整有效时间。
- 平台此前拒绝的自动ChatGPT发送动作仍不得通过更换CDP、MCP、n8n或执行桥绕过；真实写入需经平台允许及任务会话所有权核验。旧AHK --commit硬停继续保留。UNKNOWN绝不盲重发。

## 反向约束
不误触未归属的当前用户聊天、不修改代理或浏览器Profile、不重复旧UNKNOWN短码、不以隔离模拟ACK、人工接续或组件连接PASS冒充全自动成熟。不因本任务切换专用浏览器而影响其他TASK和公共B路线。

## 本次现实只读连接证据
- 专用Chrome/CDP端口9223在线，浏览器Chrome 151.0.7922.34。
- 真实回环CDP /json/list 返回HTTP 200，22个目标中有2个chatgpt.com页面，HTTP只读请求约180ms。
- Microsoft Playwright MCP STDIO附着到现存CDP并实际调用browser_tabs action=list：PASS，识别真实ChatGPT页面2个；MCP端到端启动附着和读取45290ms，24个可用工具，未点击、未发送。
- REAL_AUTO_NEW_CHAT=NOT_TESTED；REAL_AUTO_SEND=NOT_TESTED；REAL_GPT_RESUME=NOT_TESTED；AUTO_END_TO_END_VALID=NO。

## FINAL_VALID
在已登录专用Chrome按原冻结任务完成自动新ChatGPT、一次短码、GPT线上读取和继续原业务结果，且全程合法、可计时、无人工操作。未得到允许的官网真实写入入口时只能BLOCKED，不能因读取PASS而宣布成熟。
