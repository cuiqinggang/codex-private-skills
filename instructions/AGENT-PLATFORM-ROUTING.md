# 平台与专项操作路由 V1.4
本文件按章节读取，不自动全量导入。与共同执行指导V1.4同目录。
状态：随V1.4接入；只按实际已验范围使用。原文是既有经验，不代表今天所有环境仍有同一故障。
历史并发2路/普通任务一律串行、固定GPT比例、自动24小时总截止等旧规则不恢复。
具体任务明确指令、现行运行配置和真实回执优先；不得重新启用撤销的授权或门禁。

## A. Windows执行桥
触发：本机文件、命令、设备、通道异常与恢复。
读当前可用的gpt-windows-execution-bridge技能，使用已验当前新编号入口。
默认D→A→B→C；D目录能力不匹配须说明，不自行扩大白名单。
3秒是轻量连接软期限；running/session_id继续原会话，不按此杀业务任务。
写入无回执先UNKNOWN核账；新旧入口、权限和主机要对应，不回退已退役入口。
PowerShell默认C:/Program Files/PowerShell/7/pwsh.exe -NoLogo -NoProfile。
复杂宿主任务先核实际版本、进程路径；仅明确兼容需要才用5.1，不改PATH。

## B. 专用浏览器、标签归属和下载
触发：Windows网页操作；纯文件任务不触发。
正式配置：C:/AI/Playwright-Native-AI-Browser/profile/shared-mcp；既有CDP9223。
GUI任务先确认正式MCP就绪；Codex按任务启用required=true、startup_timeout_sec=60，非GUI任务不设全局必需。
Codex复用已验app/mcp-existing-cdp-9223.test.json连接原9223；Pi保留现行HTTP，不因控制器退出推定传输故障。
复用已可用正式MCP与可见窗口；用户当次指定其他浏览器时按本次授权。
Pi按原xd://发现设备和工具schema，不猜名称/ref；不以shell/CDP脚本替代正式网页操作。
每次写操作前核当前页身份、目标和本任务归属；不抢其他任务页。
browser_tabs(new)既有行为会切换current；不得再把返回数字索引当稳定身份。
close前必须核归属；旧索引、当前页已变或页面消失时先对账，绝不猜关。
仅以本任务资源判断泄漏，不以全局标签数量变化判故障。
CSV原始字节下载先读pi-mature-routing/references/BROWSER-DOWNLOAD-V1.md。
正式页面只触发一次下载；事件超时先核本次限定候选，不全目录搜索或重复提交。
已有9223/8927但attach超时，不反复启动；按原V1.1-STALLED-TARGET-RECOVERY-20261018.md。
对应原文件：C:/AI/Playwright-Native-AI-Browser/skills/playwright-native-ai-browser/references/V1.1-STALLED-TARGET-RECOVERY-20261018.md。
只读审计复用C:/AI/Playwright-Native-AI-Browser/scripts/cdp-target-health-audit.cjs。
隔离故障页前先排除未保存编辑和UNKNOWN提交；未排除则记录阻塞。
认证、验证码和身份核验由本人在既有专用窗口完成，不读取凭据。

## C. Codex CLI、代码与Git
触发Codex CLI：C:/Users/A/.codex/skills/recover-windows-codex-preserving-data/SKILL.md。
新任务首次或配置变化后，用已有Python运行该技能scripts/preflight.py；相同任务配置不变复用。
PASS是本地配置检查，不是模型、MCP或业务健康；WARN/BLOCKED只核具体问题。
不默认重装、不删用户数据、不停全部MCP、不改代理。
代码库有.codegraph时按原适用规则查可用性、新鲜度、调用影响并必要刷新。
原专项完整条款：C:/Users/A/.codex/instructions/AGENTS-specialized.md的CodeGraph章节。
多执行者仅暂存自己的明确路径，不清其他改动、不强推、不以reset/clean/stash抹除他人工作。
测试命令来自目标项目自身文件，不把网上项目的bun/npm命令复制成全局命令。

## D. Pi运行兼容、Office、图片与视频
触发：Pi相应工具或本地媒体任务；普通任务不读整份。
原来源：C:/Users/A/Documents/DSH-Workspace/pi-capability-enhancement-20261028/workspace/.omp/agent/mature-first-r57.md。
该文件含历史旧规则，只读对应兼容/媒体章节；其旧串行和固定总时限不生效。
既有Python Eval内核不可用记录：保持现有关闭配置，直接用已验证本机Python，不重装。
固定Python：C:/Users/A/AppData/Local/Programs/Python/Python313/python.exe。
子进程遵守当前工具及宿主规则；不能因默认PowerShell建议就改写已验Pi内部bash机制。
OfficeCLI既有无驻留模式：OFFICECLI_NO_AUTO_RESIDENT=1、OFFICECLI_RESIDENT_FLUSH=each。
不显式启动驻留或终止其他进程；若本次版本已修复，凭实际证据更新此兼容记录。
Windows ACL下Git/MSYS unzip旧信号管道故障：优先已有Python zipfile，不重复失败路径。
图片用主模型原生read读取路径；视频先按需抽帧，不把视频容器当图片read。
已有抽帧程序：C:/Users/A/Documents/DSH-Workspace/pi-unified-upgrade-20261030/skills/pi-mature-routing/scripts/video_frames.py。
调用：固定Python、程序路径、输入视频、工作区新输出目录、--count N。
概览通常3—5张；动作或时序要求需针对相关时间加密；采样不能证明全视频合格。
按frames.path读取图片；语音、台词与音画同步按原音频/视觉专业流程。
视频能力须以合格作品验证；无素材/参数/步骤的演示不算掌握。

## E. 记忆与知识库
触发：长期记忆、技能治理、复杂工程、重复故障、项目接续。
读C:/Users/A/.codex/knowledge-brain/INDEX.md和ROUTING_MAP.md，选一个相关分类及1—3份资料。
长期入口：C:/Users/A/.codex/obsidian-vaults/AI-COMPANY-KNOWLEDGE-OS/00_INDEX/CODEX-LONGTERM-MEMORY-ENTRY.md。
Pi原目录：C:/Users/A/Documents/DSH-Workspace/pi-memory-integration-v1-20261101/MEMORY-INDEX.md。
共同权威：cuiqinggang/codex-private-skills/main的MEMORY.md及对应专业CURRENT/Freeze/最新回执。
触发固化时优先原专业包；资料转能力原入口C:/Users/A/.codex/skills/codex-video-to-usable-skill-loop。
收尾仅运行C:/Users/A/.codex/knowledge-brain/tools/kb_health_check.ps1。
明确小型hot entry变更才按原脚本显式路径hot sync；deep sync要本次明确批准。
不递归同步全Vault/Skills/Documents，不读H/K补源。
原生learn后的下一次同项目注入、共享发布和真实召回要分别记录，不宣称全页面自动注入。

## F. 授权、暂停售项与外部业务
Windows系统保护包括注册表、服务、启动项、计划任务、PATH、ACL、驱动和WSL/Docker底座。
网络保护包括代理/订阅/服务、DNS、hosts、VPN、防火墙、路由和端口映射；允许只读检测。
普通应用配置和Markdown按目标/影响判断，不因路径位于AppData/.codex自动阻断。
不可逆数据操作、付费、发布、账户和敏感外部写入按当前具体授权，不替用户批准。
ROI门禁与标签门禁继续暂停；单次明确成本分析不自动恢复全局ROI流程。
海外服务按已验证需求选路；收款核当前身份/业务资格及本人真实到账，不以别人开户成功替代。
不把权限批准、首次OAuth、令牌续期和业务授权混为一谈。
