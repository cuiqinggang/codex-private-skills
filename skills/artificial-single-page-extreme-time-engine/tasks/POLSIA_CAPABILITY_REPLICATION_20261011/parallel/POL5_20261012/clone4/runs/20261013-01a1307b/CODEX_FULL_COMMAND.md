任务：接续已找到的 Polsia 克隆四命令，用成熟组件与真实多智能体并行，把公开站点的视觉、页面导航与现有持久业务服务完整接通。
本命令已由编写端完成质量门禁；执行端不得再次评分或调用门禁，直接按正文执行；只核对运行时新事实。

验收：以 https://polsia.com 和用户办公室截图为参考。中文可调整，原图片、字体、颜色、尺寸、四屏滚动、logo缩放、移动断点与所有已观测入口页面逐项复刻；不得用占位图或自绘替代原资产。逐页保存同尺寸桌面1440×900/移动390×844源图和本地图，组合比较，发现布局、字体、图片、导航问题就修正后重新截图。99.9%是用户目标，不能用主观评价或测试数量冒充已经达到。至少实现首页四屏及语言菜单、/new四种状态、/login及延迟创建入口、/about、/terms、/acceptable-use、/privacy、/subprocessors、/changelog及其四个实际详情。登录后私有页面没有参考则记录缺口，不凭空伪称全面对等。
现有公司创建、目标、任务、结果、原始历史证据、最多4项并行的新Codex本地交付必须真实持久；用4个新任务验证进程、JSONL、结构化结果、文件SHA与工程固定测试。独立测试公司隔离、重复启动、并发容量、异常/中断核对和重启恢复。模型未启用、失败或结果未知时如实显示，禁止假完成、自动重发未知任务或把旧文件阅读当新业务执行。公网部署、真实广告、邮件/外联、客户派单、签约与收款目前未接入，不能声称完全复制原站业务能力。已有外部监控站由原负责人接手，不重建。

模型/力度：沿用当前Codex会话设置；本命令不修改模型、账号或全局配置，不可观察值记录UNKNOWN。新本地业务使用已安装原生Codex CLI及其现有正常授权环境，不读取或复制凭据。
智能体：4个活动角色，主智能体负责PCL-03和集成；PCL-01运行与原资产，PCL-02能力/原生执行器/公共页面，PCL-04非作者独立验收。共享目录但源码单人所有权，不让多代理同时改同一文件。
时间上限：每一实施/验收批次最长60分钟，批次结束保存真实状态；用户已要求持续继续，未完成则接续下一批，不把到时当完成。

执行要求与停止条件：
1. Windows正式执行根 C:/AI/Polsia-Codex-20261011；仅C盘日常运行。隔离代码 outputs/polsia-clone4-20261012/integration/open-polsia；证据 outputs/polsia-clone4-20261012。不读H/K、不覆盖原工作副本.env或未提交更改、不原改冻结成果。默认显式PowerShell7路径 C:/Program Files/PowerShell/7/pwsh.exe；不删系统或网络配置，不改代理/DNS/VPN/Windows服务/PATH，不绕现有沙箱/审批。
2. 共同工作区是 cuiqinggang/codex-private-skills main，源前缀 skills/artificial-single-page-extreme-time-engine/tasks/POLSIA_CAPABILITY_REPLICATION_20261011/。读取 parallel/POL5_20261012/clone4/PCL-01_TASK.md至PCL-04_TASK.md；精确blob SHA见 SOURCE_RECEIPTS.json，禁止用空搜索推断不存在。接续当前运行回执，旧PID/ASSIGNED是历史事实。
3. 继承 POLSIA-MOTHER-V008-F001，V001–V008全部只读；能力正式基线 nodes/CODEX-008/CAPABILITY_MATRIX.md。禁止重跑旧财务或媒体、修改母CURRENT/VERSION_CURRENT/Freeze。新进展仅落本轮输出/共同工作区新版本run目录，不写入母终验。原平台源码 C:/AI/Polsia-V5-Parallel-20261012/platform/open-polsia 只作继承，执行使用隔离副本。
4. PCL-01：复用成熟open-polsia锁文件和依赖，隔离官方PostgreSQL17.11（127.0.0.1:55433，数据在本轮），Node站点127.0.0.1:55437。用最新live receipt核对自身PID/启动时间/路径/参数/SQL/HTTP后才允许停止自己的site；PG持续保留。官方下载图片字体/CSS保存URL、字节与SHA，公共API图片本地映射，不热链。日志读取需FileShare.ReadWrite；失败回执保留。
5. PCL-02：维护九类历史能力白名单与原manifest SHA/字节核验，不重放旧业务。原生执行器每项独立delivery/receipts，最多4执行位、未知结果占位，exactly-once启动标记、实时持久日志、退出回执、严格JSON schema和产物校验；工程固定验收文件不可改，必须实际执行。源码视觉只解析原公开JS/DOM，不执行其生产JS或第三方埋点。公共页面沿用已采集真实DOM和原CSS，安全本地静态allowlist，原Google/邮件登录未接入则保留外观并明确提示；本地创建公司保存成功后进/workspace。
6. PCL-03：复用PgStore/Postgres接本地持久任务和真实执行，新业务类别工程/营销草稿/客服草稿/销售提案/新合成财务/项目SOP。任务、日志、报告、文档严格公司隔离；claim与容量失败恢复；completed不能重放，未知只核对。POLSIA_STAGING本地、原上游worker始终关闭，阻断上游chat/onboard/cron/proxy/reset与有副作用GET/run。公开首页使用新public-page handler；保留既有/workspace真实业务入口，页面视觉不得伪称已认证未见私有源。
7. PCL-04：非作者核查最新实现，独立HTTP/DB/故障注入与截图对比。只做新改动真正相关测试；修复后重跑失败边界，不无理由循环全量。设计交付须同时查看源图与本地图，保存design-qa.md，无P0/P1/P2才passed；不可打开或有缺口则blocked并具体说明。记录是否实际调用原生模型，不用受控子进程测试冒充模型成功。
8. 用户已于2026-10-12明确允许本地Playwright采集Polsia公开页与对比。仅专用空白测试浏览器，不改现有用户profile、登录、系统或代理；现有CDP 127.0.0.1:55439是本轮临时浏览器，以活跃回执为准。先捕获再实现，不能凭记忆猜布局。
9. 文件所有权：PCL-01 owns pcl01及运行脚本/资产收据；PCL-02 owns capabilities.ts/codex-jobs.ts/public-page.ts/public/polsia及其测试；PCL-03 owns dashboard.ts/dashboard-page.ts/staging.ts/business.ts与集成；PCL-04只写审核输出。正式冻结/全局Skill不原改，ROI与标签门禁保持用户暂停。
10. CodeGraph：仅根有.codegraph时优先索引定位/impact后变更；当前隔离根无索引，使用定向阅读，记录MCP/CLI可用性和未使用原因。Knowledge Brain按INDEX→ROUTING_MAP→相关category→Top-K完成复用，不重复全库扫描；无KB改动不sync，收尾仅正式kb_health_check。
11. 出现需要新生产/外部发布、真实账户/邮件/支付、系统或网络设置变更时先完成可审查本地结果，保留具体阻塞并请求相应授权。普通已授权本地实现、修复、测试连续执行。只有实际达标才报告完成；最终给可打开本地站点、真实测试和视觉比较证据、剩余边界与共同工作区新版命令链接，不承诺零bug。
