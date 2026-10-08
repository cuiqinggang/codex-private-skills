# 第26版 n8n 成熟连接优先｜虚拟成熟完整实施合同
日期：2026-10-08
状态：VIRTUAL_PATH_MATURE_WITH_EXPLICIT_INTERFACE_GATE；非 Reality PASS；FINAL_VALID=NO
方法：ENGINE=26、BRAIN=23、NPT=17；版本提交4663cb81e3bb32f65d4de288a1ed697165c95414。

## 唯一目标
以现有F011五条真实ChatGPT验证115.67秒为现实GOOD基线，在不修改FlClash、不启动第二浏览器、不重造HTTP服务器/状态机/调度器/租约的前提下，通过成熟n8n及现有Windows合法执行入口构成五任务隔离、唯一发送、可恢复、可计量工作流。
现有Playwright浏览器业务函数支持query、send、wait_extract，原Node工作进程已经做过5/5 PASS，但旧编排器和JSON租约不得成为新通用基线。

## 新增权威入口核验（2026-10-08）
已实际读取 C:\AI\Playwright-Native-AI-Browser\skills\playwright-native-ai-browser\SKILL.md：官方项目内正式 Playwright MCP STDIO 通道已经存在，使用现有已授权登录身份；业务入口应通过已暴露的 `browser_run_code_unsafe` 加载 `scripts/chatgpt-business-entry.js`，执行 query/send/wait_extract；共享浏览器以一个有效写入者和 fencing token 为约束。MCP客户端、Windows桥是允许的授权入口，但不能并发打开同一Profile。
**因此此前的“缺HTTP接口→必须自建服务/换Temporal”是错误判断。接入主路径应优先证明：n8n已有标准MCP客户端节点是否能调用已授权STDIO MCP，或现有 Windows执行桥是否能以成熟插件完成该映射；对现有协议直接复用优先于引入HTTP中间层。**
需要分别验证连接器是否可在 Docker n8n/Windows 进程边界真实调用，不能把磁盘上存在的 MCP 技能包当作已连通。所有现有浏览器进程保持不变。

## 已核实的成熟资产与准确边界
Windows n8n-local Docker容器版本2.38.7，现成持久化卷，6个已有工作流。n8n的Reasonix工作流由Webhook、Code、HTTP Request、Code组成，通过host.docker.internal请求本机接口；可确认成熟HTTP客户端和宿主机桥接网络可用。
C:\AI\n8n\reasonix-n8n-adapter.ps1 是专用于Reasonix的业务HTTP Listener，调用reasonix.cmd，不是可直接调用ChatGPT Playwright函数的通用服务器；不得直接复制/新建调度HTTP服务器。
C:\AI\Playwright-Native-AI-Browser\skills\playwright-native-ai-browser\scripts\chatgpt-business-entry.js 是成熟Playwright async(page)入口，依赖sessionStorage配置，操作query/send/wait_extract。C:\AI\CEO-Auto-V1\v24_f010_task_worker.cjs 可在Windows调用它，但原worker自己管理JSON租约且在发送之后等待回复仍持锁，不能未经审计直接认定满足新方案的细粒度并发和跨进程恢复。
原Reasonix n8n HTTP节点retryOnFail=true，只可说明该工作流如此配置。ChatGPT的非幂等发送阶段必须禁用自动重试，并依赖真实回读判定外部副作用。

## 初始三强与补缺顺序
方案A：n8n + 现有Windows合法调用桥 + 原Playwright技能包，部署增量最小，列为主候选。
方案B：n8n + 官方Node/Windows进程成熟连接器（例如已授权插件、Windows本机Worker）直接调用已存在的Node业务入口；优先配置，禁止默认编写HTTP服务。连接器产品具体选用需以当前已安装能力为证据。
方案C：Temporal/Prefect官方Worker（替代底座）仅当A/B实证无法满足VALID及净收益才进入。不可仅以“目前还未找到现成HTTP接口”淘汰n8n。
原则：HTTP只处理调用，不能把它当作跨进程唯一发送、浏览器写锁和工作流恢复的证明；这些能力必须分别核对成熟接口。

## 完整虚拟执行图
TASK_ACCEPTED -> 生成唯一TASK_ID/MARKER/ACK -> n8n官方Webhook或已有接单节点 -> 原生验证与参数映射 -> 检查之前持久化执行意图 -> 通过合规连接器调用原浏览器query（只读） -> 若userCount>0则只恢复wait_extract；若userCount=0且能证明未曾发送，则single send；否则UNKNOWN不重发 -> 已确认SENT_CONFIRMED持久记录会话URL与PageID -> 仅允许已证明安全的资源阶段释放 -> wait_extract在所属会话等待 -> final query核实仅1个用户消息与正确ACK、无额外提交 -> 不可变NODE_FREEZE -> CEO按TASK_ID依次Merge -> 仅关闭所属页面 -> 五条都通过为FINAL_VALID。
业务连接层只允许现有官方成熟入口/配置映射；不另造通用HTTP调度、SQLite状态机、文件租约。若没有成熟仲裁，冲突浏览器写阶段保持串行，不能凭假设并发。
要使发送后等待与后续任务重叠，必须能在各自页面安全重新附着，并且原入口可分阶段操作；旧worker一体化且持全程租约，所以绝不能直接继承其锁粒度。

## 连续虚拟攻击迭代
R1：最初误判连接不通等于底座失败 -> 改为成熟连接器优先。
R2：现有n8n网络桥已证实，Reasonix端点不是ChatGPT端点 -> 明确仅复用通信机制。
R3：接口签名不一致 -> 仅在成熟插件/节点能力内映射业务字段，不自建通用服务。
R4：重复提交 -> TASK_ID/MARKER预检，外部发送标记一次；UNKNOWN绝不盲目重试。
R5：执行中断 -> 先回读目标会话；页面不可重附着则UNKNOWN，不声称自动恢复。
R6：写资源冲突 -> 安全前提下仅排队冲突写动作，不能将网页等待无谓占用独占锁。
R7：另一个任务失败 -> 不回滚其他TASK_ID，不关非所属页面。
R8：n8n自动重试 -> 对非幂等发送阶段关闭，仍允许经过证明的只读恢复。
R9：完整时间 -> 原F011批次115.67秒，5任务独立阶段总和110.906秒，发送前70.370秒，回复等待39.940秒；若整段发送前串行且等待重叠，条件理想76.732秒；完全独立并行条件理想23.625秒；都不是现实物理下界。
R10：排序优化将76.732秒变成76.669秒，收益仅0.063秒，较之压缩浏览器准备/释放等待锁的机会优先级低。
R11：组合Temporal/n8n增加第二底座、状态边界和恢复面，无正净收益证据，不组合。
R12：全方案重放：无虚构API端点、不依赖未经验证的页面重附着、不在UNKNOWN情况下重发。就绪约束闭合后执行一次完整Reality，而不是逐点实测。

## 虚拟停止门与实施前缺口
设计迭代已覆盖正常5任务、失败重传、发后断线、重启、跨任务干扰、页关闭、持久化、时间边界。
但「可由n8n调用的已授权ChatGPT浏览器业务连接器」和「成熟共享浏览器排他与重启后页面重附着」尚无可核对的现成接口证据。故不能宣布REUSE_GATE=PASS或整体STOP_GATE完成。若没有接口，不得虚构实现；应继续查找并验证成熟连接件，而非直接改架构或自研。
本件为结构完整的虚拟成熟实施合同（DESIGN_FREEZE_CANDIDATE），不等于最终冻结验收。完整物理极限时间尚无法从五次任务数据唯一确定，23.625秒只是一种条件并行参照。

## 最终成熟连接件确定（新增事实）
已查官方 n8n MCP Client 文档：客户端面向外部MCP URL，不直接代表能在Docker中接入Windows STDIO进程。已查成熟Supergateway（npm项目）：支持把STDIO MCP转换为Streamable HTTP或SSE，故无需重造通用HTTP服务。
最小候选组合：现有n8n MCP Client -> 官方成熟Supergateway协议桥(Windows进程侧) -> 原授权Playwright STDIO MCP -> 已审核chatgpt-business-entry.js。前置必须确认桥仅启动/复用一个MCP进程及其Profile，不能每次请求拉起第二浏览器实例；只暴露回环或受保护的宿主机接口，禁止开放公网、无鉴权共享写接口。不得在验证前开启该桥直接访问用户浏览器。
与单体n8n HTTP +现有Reasonix桥比较：Reasonix HTTP脚本只懂Reasonix业务，不可通过简单URL替换接入ChatGPT。Supergateway是成熟可直接采用的协议转换器，但只有后续接口工具发现和单实例验收才可判PASS。
已淘汰不合规路径：自行开发通用HTTP server / 多个独立MCP进程争用共享浏览器 / 从Docker内Execute Command直接访问Windows Node / 用Temporal迁移掩盖未核实连接器。
虚拟重放最终序列：选定一个已授权STDIO MCP owner → Supergateway单实例兼容配置(待验证) → n8n MCP Client tools/list确认正式browser_run_code_unsafe存在 → 参数传递到已审核真实入口 → QUERY → SEND_ONCE(禁止retry) → WAIT_EXTRACT及只读恢复 → NODE_FREEZE → CEO Merge → 只清理属主页。未通过单实例所有权或协议发现则停止在CONFIG_BLOCKED，不能降级到自研。
完成判定：架构分层、正常路径、故障反例与成熟组件映射均已明确，设计级虚拟成熟形成冻结候选；实际MCP-HTTP握手、同Profile单实例、跨进程恢复及总净收益仍未物化，REUSE_GATE未全部PASS，不允许宣称已经过Reality门禁。
