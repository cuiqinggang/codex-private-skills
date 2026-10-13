# 《三人行》第2版｜Remote Desktop Commander 免费 10,000 次配额成熟运营方案 V1.0
状态：**运营方案已拟定，尚未部署自动分流和限额执行代码**；日期：2026-10-13。
权威项目：cuiqinggang/codex-private-skills，workspaces/gpt-windows-dual-bridge-v0.3.4。
不修改 FlClash、Windows 代理、现有自建 GPT-Windows-MCP-Bridge、自托管 GitHub Runner 或浏览器。

## 0. 事实、口径、边界
- 官方 Free 价格：$0/月、10,000 **tool calls**／月，不是 10,000 次登录或连接。官方：https://desktopcommander.app/pricing/
- 2026-10-13 当前账户 Remote Desktop Commander 的 who_am_i 返回 remote_calls_left_pct=0；之前远程文件调用明确受月度额度限制。无法凭此获取精确下次 reset_at；不可假定每月1号清零。
- 平台对跨客户端配额共享范围、失败调用计数及重置窗口细节未充分明确；https://github.com/desktop-commander/remote-desktop-commander/issues/15 仍有公开澄清请求。以平台账户面板真实统计为准。
- 自建 GPT-Windows-MCP-Bridge 当前可成功读写/执行，使用的是官方 OpenAI Secure MCP Tunnel + Windows 本地开源 Desktop Commander MCP；不等于 Remote Desktop Commander 托管服务的配额池；其 OpenAI/ChatGPT 使用权限及平台限制仍以各自规则为准。
- 使用本地 MCP 的 get_usage_stats 读到总调用 8733，start_process 2828、read_process_output 2479、read_file 1200、write_file 753。**这是本地服务累计工具统计，不应冒充 Remote 官方收费调用量**。启动+轮询约占 61%，存在减少查询的潜力。

## 1. 月度运营预算：以官方面板真实已用量为准
- 容量 10000／月；**业务常规目标 6000 次**；临时弹性 2000 次；紧急保底保留 2000 次。
- 日常软目标 <=200 次/天。按 30 天 6000；31 天 6200，需从临时弹性扣 200；不是每日官方硬额度或每日自动充值。
- 黄色提醒：已用 >=6000 次，暂停常规非必要调用，复核预算；橙色 >=7500，Remote 仅高价值任务；红色 >=8000，**自动计划停止以 Remote 执行**，保留约 2000 次人工紧急额度，常规任务转自建 A，异步转 GitHub B；>=9500 需要明确单次人工授权。
- 若面板只给剩余百分比：可用 remaining_pct 估算阈值（剩余 <=40%、<=25%、<=20%、<=5%）；由于四舍五入只做预警，不以此冒充精确额度。
- 复位：配额回归时仅按官方仪表板显示确认；如不知道 reset_at，不预设 11月1日、账户创建纪念日或任何具体恢复日期。禁止重配对/重新注册来规避限制。

## 2. 三路分工，不叠床架屋
- A（优先）：既有 GPT-Windows-MCP-Bridge + OpenAI 官方隧道 + Windows 本地 Desktop Commander MCP；频繁读写、批处理、Codex CLI 启动与验证；不消耗 Remote Desktop Commander 官方托管的 10k 池，但需注意独立的平台/权限限制。
- R（限额）：Remote Desktop Commander 官方托管免费版；只处理必要、价值高、适合交互的远程控制和 A 不可用时临时故障切换；**不作为所有命令默认路径**。
- B（备援/长任务）：GitHub Actions self-hosted Runner；适用大型异步独立节点与审计留痕，不适合小任务；极简 smoke 已 PASS，但历史生产 workflow 有下载外部 Action 超时故障，未修复前不能等同生产完成。
- 路由优先级：短/频繁→A；A 不可达但必须即刻接管→R（有额度且已经鉴权）；长期/离线/留痕→B。R=0 或超过红线自动改走 A/B，不进行无意义重试。**这是一份待部署路由策略，不是已实现的实时自动切换系统。**

## 3. 最少调用准则（节约不等于放弃验证）
1. 先明确任务自然节点、可用成熟基线、终局验收证据和 Exactly-once ID；同一节点内部虚拟成熟→Freeze→Reality，降低盲试次数。
2. 小型只读操作能用 read_multiple_files 一次读取相关少量文件，则不逐个 open；只取必要范围，不下载整个海量目录。
3. 对短命令首选一次 start_process 返回初始结果；只在工具确实返回持续运行时再 read_process_output；不固定每秒轮询、不可重复发起原副作用命令。
4. 跨多个相关动作可在**安全审核后**用一个受限本地脚本批处理，提供明确输入、目录限制、幂等标识、结构化结果和退出码。不能把不相关危险操作隐藏到一条不可审查的 shell 命令中。
5. 一次完整业务节点只允许必要的终局核验；涉及修改文件或系统配置时保留独立验证，不因省额度牺牲真实完整性。
6. 失败时先区分 QUOTA_EXHAUSTED、DEVICE_OFFLINE、AUTH、NETWORK、TOOL_ERROR；配额错误禁止反复 ping、重连、重装或循环重试；停止重复调用并切 A/B。

## 4. 观测/审核
- 可在 https://mcp.desktopcommander.app/ 读取官方面板的本月已用、剩余以及服务允许展示的复位信息，不猜测复位日。
- 每周一次低成本人工检查配额；在发生密集 Remote 任务后核对消耗，记录任务ID、工具数、成功/失败、是否替代 A 更省时、实际净收益。
- 若经过一个完整真实计费周期，Remote 工具调用 <= 8000、任务成功率/可用性满足要求→继续 $0；如持续越线，优先检查是否把大量 A 本可完成的任务误投到 R；最后才考虑购买官方 Pro 或 VPS。
- 若每天 200 次仍不够，**先切换通道而非扩容免费配额**；不要用多个身份/账号规避正式限制。

## 5. 运营验证状态与下一节点
- POLICY_DRAFT=YES；DASHBOARD_REMAINING_PCT=0；SOFT_BUDGET=200/DAY；REMOTE_STOP_AT_USED=8000/MONTH。
- AUTO_GUARD=NOT_DEPLOYED；TASK_LEDGER=NOT_DEPLOYED；RESET_DATE=UNKNOWN。
- NEXT：取得官方面板重置说明 → 在不会消耗额外 Remote 配额的管理层部署调用账本和预算决策门 → 按真实任务观察 7 天 → 再考虑是否付费。
- 未获额外授权，不对 Windows 原有服务进行关闭/重配/配额切换/代理变更。
