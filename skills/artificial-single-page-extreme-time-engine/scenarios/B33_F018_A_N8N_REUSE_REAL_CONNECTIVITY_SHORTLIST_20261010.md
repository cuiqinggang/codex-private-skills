# B33 F018｜A路线 n8n 成熟成果回查与三方案最小联通候选
DATE=2026-10-10
MASTER_TASK=B_SINGLE_PAGE_MATURITY_20261009
PREVIOUS_FREEZE=B33-VM-F017
A_ROUTE=ENGINE28/BRAIN25/TEMPLATE18
B_ROUTE=ENGINE_B33/BRAIN_B29/TEMPLATE_B23
PRIORITY=REAL_END_TO_END_CONNECTIVITY_FIRST
TIME_OPTIMIZATION=DEFER_UNTIL_REAL_CONNECTIVITY_PASS
CURRENT_AUTO_HANDOFF_VALID=NO
VIRTUAL_MATURE=NO
FINAL_VALID=NO

## 1 共用权威已证实的 A/n8n 真实通过事项
据 routes/A/ROUTE.md、freezes/V28_BROWSER_SHARED_CURRENT_FREEZE.md、freezes/N8N_BROWSER_SHARED_CURRENT_FREEZE_20261009.md、tasks/N8N_MCP_SHARED_20261009/freezes/CURRENT_TASK_FREEZE_V2.md 和 references/V27_SHARED_BROWSER_STAGE_V1_1_0.md：
- n8n 原生 MCP Client 1.1 对既有 Playwright MCP 的 browser_tabs 实测成功；
- 隔离 n8n 跨工作流三任务串行 #23–#25 真实通过；
- 原浏览器临时 DOM 可逆写入/回读/恢复 PASS，未发真实ChatGPT消息；
- 原生 Remove Duplicates 持久去重跨重启 #18–#20、#22 PASS；
- 原生 Wait 重启恢复同一执行编号 #21 PASS；
- 写入成功后故意失败 #26，去重重试 #27 没有二次写入；
- n8n 可逆写入 #28 与另一个 MCP 客户端读取同一浏览器共存成功。
这些是真实成熟的浏览器连接和n8n可靠工作流组件，不是已经验证跨ChatGPT聊天自动接管的完整有效任务。A共享浏览器任务本身仍 VIRTUAL_MATURE=NO、FINAL_VALID=NO，跨客户端同资源仲裁/无冲突实际并行/异常释放/UNKNOWN实际对账和正式业务发送尚未通过。

## 2 本机无需重造的资产与缩减边界
通过现有Desktop Commander只读目录检查，C:\AI\n8n 仍有 compose.yml、artifacts、workflows 和部署文件；C:\AI\Hatchet-Isolated-V1\mcp-probe\n8n_mcp_readonly_workflow.json 确认实际现存两节点工作流：n8n-nodes-base.manualTrigger → @n8n/n8n-nodes-langchain.mcpClient (typeVersion 1.1)，名称V27-MCP-READONLY-DISCOVERY-20261009，文件active=false。原 C:\AI\Playwright-Native-AI-Browser\scripts 目录和正式业务技能包仍可只读定位。
一次只读Docker进程列表调用未通过平台安全检查，故 Docker CURRENT_ONLINE=UNVERIFIED；不能把历史n8n-local容器/HTTP18931旧PID和端口等同当前在线，更不能因此改FlClash或重复启动浏览器。

最简可复用的连接骨架（只作为待验证业务链）：
GPT当前任务/冻结 → 已有n8n节点（仅当持久工作流必要）→ n8n现成MCP Client → 已有官方Playwright MCP/原登录浏览器的允许操作 → 已有业务查询/结果回读 → GPT核验GitHub Freeze/CURRENT并恢复任务。
去重只使用n8n原生Remove Duplicates，等待/重启只使用原生Wait；禁止新造状态机、调度器、持久HTTP代理、锁或第二个浏览器。与B33相比这可能增加工作流/容器开销，不能先认定更快。原Playwright业务入口已有query/send/wait_extract，但没有现成new_chat完整B33自动交接验证；把browser_tabs/可逆DOM成功误认为官网新ChatGPT一次发送/真实GPT恢复PASS属于合同错误。
不得用n8n或另一连接通道完成以前被平台明确拒绝的同一ChatGPT自动写入动作；只有平台明确允许的新独立测试合同才能执行此部分。

## 3 最多三个成熟候选（依真实VALID先筛，不以纸面速度排名）
候选1 MANUAL_CHROME+GITHUB：T02人工新聊天→四字段码→新GPT从GitHub恢复计算/冻结已PASS，同质量独立测试名义T_VALID=382.518s（n=1，跨源时钟误差），但不是无人值守。
候选2 B33_AHK_UIA+GITHUB：正式B33原有Windows AHK/UIA薄适配，离线本地UIA动作3/3PASS，安全门10/10PASS，真实官网自动提交被本机exit90硬停且旧平台安全拒绝仍在；END_TO_END_VALID=NO，真实全程时间UNKNOWN。
候选3 A_N8N_NATIVE_MCP+PLAYWRIGHT_MCP：上述n8n原生连接、等待、去重、同浏览器可逆写入已有大量现实PASS，现场项目和原两节点MCP工作流已定位；但此时容器在线状态未核实、自动官网短码提交到GPT恢复没有合同级PASS，END_TO_END_VALID=NO，完整时间UNKNOWN。
官方Chrome扩展虽安装，但原B33同合同可调用接口证据不充分，不纳入本次三个成熟候选以避免凑数/重复扩张。候选1目前是唯一同合同人工联通PASS，不与两条未通过自动路径比“谁更快”。

## 4 真实联通门及最简未来验收
现阶段不优化1秒级GitHub读耗、不重复已通过的browser_tabs/Wait/去重。仅检查成熟组件当前在线/合法接口状态；如有平台允许的自动官网新聊天入口，建立新的独立无业务TEST任务及Freeze，记录原Chrome/新聊天唯一归属、一次发送、服务端用户消息、真实GPT读取冻结、完成独立结果、不可重复副作用，起止同一时钟并全程计时。任何平台拒绝则停止该操作，不替换为另一传输绕开。只在端到端VALID通过后，比较三个合格候选T_VALID及适配、恢复、运行成本，并选真实最快。
本次为A证据复用与候选筛选，未对A或B进行新的ChatGPT发送/跨页自动联通，亦未宣称现有服务在线或A全局任务已FINAL_VALID。
