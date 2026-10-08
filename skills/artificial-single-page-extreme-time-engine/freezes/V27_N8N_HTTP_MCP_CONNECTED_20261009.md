# V27 n8n 到原 Windows Playwright HTTP MCP 实连证据
方法 ENGINE=27 / BRAIN=24 / NPT=17
状态：MCP_DISCOVERY_CONNECTED=PASS；FORMAL_BUSINESS_TOOL_DISCOVERED=PASS；N8N_NATIVE_NODE_WORKFLOW=UNVERIFIED；BROWSER_WRITER_ISOLATION=UNVERIFIED；FINAL_VALID=NO。
现实设备 DESKTOP-4A1EGTM。
## 修复过程
1 Desktop Commander 远程连接重新上线，无需修复代理。
2 原 Codex 子进程 27288 通过STDIO使用共享Profile；原已登录Chromium CDP=127.0.0.1:9223。保留原进程。
3 使用项目已经安装的 @playwright/mcp 官方 CLI，新启一个**独立HTTP服务进程连接已存在的CDP**（没有启动第二个浏览器或新Profile），端口127.0.0.1:18931；使用 --cdp-endpoint、--port、--host、--allowed-hosts host.docker.internal:18931,localhost:18931、--shared-browser-context。
4 首次从n8n容器通过 host.docker.internal:18931/mcp 普通GET得到403 Access is only allowed at localhost；将允许主机改成含端口的两个确切值后，普通GET返回400 Invalid request，证明请求进入MCP协议层。没有使用 * 开放主机。
5 用容器内隔离的只读MCP协议客户端进行 initialize、notifications/initialized、tools/list，5/5 PASS，发现24项工具，其中正式 browser_run_code_unsafe。未调用浏览器工具、未打开/关闭页面、未发送消息。
6 容器内端到端 初始化+工具发现耗时(毫秒)=303.354,40.531,37.591,39.235,34.277；后四次中位38.413ms。该值仅是握手+tools/list，并非browser_run_code_unsafe单次调用；冷启动303.354ms。
7 旧F011现实五任务115.670秒；旧条件虚拟模型零新增开销76.824秒。若每任务额外一次约38.413ms握手，算术情景77.016秒；若每任务三次同量级调用，假设性77.400秒，预计比115.670秒下降33.085%。后者非测得真实业务开销，不能冒充最终T_VIRTUAL_BEST。
## 本机可复用文件
C:\AI\Hatchet-Isolated-V1\mcp-probe\container_mcp_discovery.cjs （只读协议发现）
C:\AI\Hatchet-Isolated-V1\mcp-probe\readonly_mcp_client.mjs （Windows侧只读MCP客户端）
正式HTTP MCP运行进程当时PID=18388，127.0.0.1:18931监听；原Codex STDIO MCP PID=27288仍在。运行PID、端口只是当时状态，不等于重启后自动保持连接。未创建Windows自启动任务；需进一步做故障恢复/服务管理验证。
## 未解决的可靠性条件
- 目前两个MCP服务进程都可指向同一个已登录浏览器，必须在有证据的情况下解决唯一写入仲裁，不得因 tools/list 通过便并行执行浏览器写动作。
- 还没有在 n8n 原生 MCP Client 工作流内执行工具发现；目前从同一个n8n容器内完成协议握手（容器网络和MCP协议可用）。
- 尚未测量具体业务工具调用耗时、页面跨进程恢复、异常恢复费用；也未证明自动重启后的连接。
- 本HTTP服务暂时为本机回环端口且未验证应用层鉴权，不应开放到公网或允许不受信任的本机客户端使用。
当前不可宣布VIRTUAL_MATURE=YES或STOP_GATE=PASS。下一步使用n8n成熟MCP Client工作流做无发送发现、统一写入仲裁与持久部署，回填真实工具调用开销后重算。
