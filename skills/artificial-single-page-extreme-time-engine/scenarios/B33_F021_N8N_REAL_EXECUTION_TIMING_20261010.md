# B33 F021：n8n原生MCP真实工作流计时
DATE=2026-10-10
TASK_ID=B_SINGLE_PAGE_MATURITY_20261009
PREVIOUS_FREEZE=B33-VM-F020
CONTRACT_VERSION=4
TASK_BROWSER=EXISTING_DEDICATED_CHROME_CDP_9223
REAL_CHATGPT_AUTO_SEND_COUNT=0
FULL_AUTO_CHATGPT_HANDOFF_VALID=NO

## 实测事实
- Windows专用Chrome CDP9223真实在线，HTTP200，收尾检查46ms。
- n8n正式Docker容器n8n-local现时healthy，/healthz HTTP200，收尾检查188ms。
- 原历史n8n工作流v27McpReadonly20261009已存在，内容为n8n原生Manual Trigger接MCP Client 1.1工具browser_tabs action=list，不触发ChatGPT发送，连接Windows host.docker.internal的18931 HTTP接口。
- 18931旧MCP接口本轮初始不可用。使用已安装的微软@playwright/mcp CLI短时在本机恢复HTTP接口，附着现有专用Chrome CDP9223，没有另启浏览器。Windows端原生MCP协议五次初始化与工具发现PASS，耗时ms：276.602、30.446、26.011、22.261、20.113。Docker容器通过host.docker.internal成功访问MCP端口，GET返回协议层HTTP400而非连接拒绝。
- n8n CLI首次直接执行失败，退出码1，用时13.348秒，报错：Task Broker port 5679 already in use。既有n8n正式实例正常占用5679，未重启或关闭它。根据官方已有参数，仅在这次CLI调用中将N8N_RUNNERS_BROKER_PORT设为5680。
- 随后两次按n8n工作流ID真实执行成功退出，进程状态exit0，Windows侧从命令开始到返回整段墙钟分别14014ms及14372ms，均值14193ms（约14.193秒）。输出数据里检测到chatgpt.com域名，未打印真实聊天内容。
- 限制：Windows PowerShell 5.1不兼容结果解析器所用ConvertFrom-Json的Depth参数，未取得独立的n8n节点执行耗时和节点级状态；一个针对解析脚本的远端文件编辑工具调用又被安全检查拒绝。进程exit0和输出有chatgpt.com不能冒充完整自动GPT接续PASS。
- 临时MCP服务正常清理：确认本次服务子进程拥有的18931监听后关闭，仅此监听者数量归零；原n8n容器和专用浏览器继续HTTP200。未动FlClash，未关闭登录浏览器。

## 最终口径
N8N_EXISTING_WORKFLOW_RUN_1_WALL_MS=14014
N8N_EXISTING_WORKFLOW_RUN_2_WALL_MS=14372
N8N_CLI_WALL_MEAN_MS=14193
N8N_MCP_NODE_TIME_MS=UNKNOWN
REAL_NEW_CHAT_CLICK=NOT_TESTED
REAL_CHATGPT_MESSAGE_SEND=NOT_TESTED
REAL_NEW_GPT_RESTORED=NOT_TESTED
FULL_AUTO_T_VALID=UNKNOWN
VIRTUAL_MATURE=NO
FINAL_VALID=NO
测得的是现有n8n命令行启动并执行只读专用浏览器MCP工作流的真实约14秒墙钟，不能称为自动新聊天+短码发送+GPT恢复的完整时间，更不能把此前成功的毫秒协议握手当作完整业务。之前平台对ChatGPT自动发送曾明确拒绝，因此本轮不通过改用n8n绕过该拒绝。
