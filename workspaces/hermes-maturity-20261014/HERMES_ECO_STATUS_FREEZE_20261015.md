# Hermes 成熟态 AI Coding SuperTool 生态站｜阶段冻结总报告
版本：阶段接续报告 F003（不是Hermes版本，不提升专用技能包版本）
时间：2026-10-15 19:01 北京时间左右
TASK_ID=HERMES-ECO-20261014
STATE=PARTIAL_DEPLOYED_AND_OBSERVED / FINAL_VALID=NO / FIVE_REAL_ROUNDS=0_CERTIFIED
METHOD=《三人行》第2版（本任务显式使用）；运行总方法仍遵循本机 hermes-mature-supertool v2.0
AUTHORITY=网络共同工作区，本地 C 盘为当前运行现场；不新建站点
NEXT=READ_EVIDENCE→RECONCILE_F002→FREEZE_UNFINISHED_GATES→ONLY_THEN_RESUME

## 1. 唯一目标与禁止事项
目标不是安装一台新工作站，而是将已有Windows Hermes+OpenWebUI+CLI成熟为可日用的 AI Coding SuperTool 生态站：成熟规则/技能索引/工具插件资料/自动化流程/轻运行入口/重资料库/Gate Review/Repair Loop/独立多智能体/多模态/长任务/checkpoint-resume-handoff/自动启动和恢复/充分现实验收；有效商业质量内缩短完整T_VALID。
资料库允许丰富，运行时只按需加载；优先官方和本机历史成功资产、复制成熟方案、最小适配，不从零重造。保持FlClash和系统代理、已有登录浏览器、已有容器/数据/工作区，不读/打印/传输密钥，不擅自开启旧New API/Watchdog，不重启正在运行的无关任务。失败/UNKNOWN要保留，Exactly-once先对账后重试。

## 2. 现有成果（区分年代和证据）
- 本机专用母技能：`C:\Users\A\.hermes\skills\hermes-mature-supertool\SKILL.md`，**v2.0**，原样保留。唯一上位框架“目标冻结→虚拟成熟→完整攻击树冻结→Reality串行执行→完整T_VALID对照→收敛→正式认证→冻结”。旧部署、Repair、模型路由、PowerShell、连续性和验证等专项技能继续使用。
- v2.0于10月5日结构验收历史30/30 PASS：仅结构/索引一致，不是整站运行30次。R2-01P完整cold oneshot约40.002秒，warm候选4.853秒只是曾观察到单样本，不是已认证T*。
- Hermes历史V1.3.2：OpenRouter `deepseek/deepseek-v4.1-flash` 一次性CLI真实文件工具/marker及退出码已有PASS冻结；正式wrapper `C:\Users\A\AppData\Local\hermes\bin\ltmvh-hermes-formal.ps1`；旧R1记录及R2-01候选存在。该分支R2/R3/R4…完整多门认证没有统一FINAL_VALID。
- 本机早期8月注册表有22项能力条目、13类Gate旧口径，记有模型路由、delegate_task双子任务、真实PNG视觉、Profile数据源、Repair、checkpoint/handoff、Telegram等历史RUNTIME_PASS/EXISTING_PASS；四个命名角色仍有DEPLOYED_UNWIRED项，日志与全站验证仍存在DEPLOYED/UNVERIFIED。**旧注册表updated_at为2026-08-12，不等于10月15日逐项复验**。Full Verify cron登记存在于历史索引，最新next_run为8月17日，当前持续触发/真实产物待核验。
- 2026-10-14既有Windows Hermes 0.21.5 + Docker Open WebUI启动恢复：官方Docker数据盘问题按成熟步骤修复；本机启动器 `C:\Users\A\Hermes_Windows_Native_014\launcher\start-hermes-openwebui.ps1`，Startup→Open-HermesOpenWebUI.ps1；8642→Docker→3000已曾完成授权模型发现及入口限定验收，保留原容器数据和浏览器。真实关机重启与浏览器完整聊天/长稳没有因此PASS。
- 10月14对Hermes API `platform_toolsets.api_server` 做过唯一最小配置更改，保留file/terminal/vision/video/skills/code_execution，新增web/delegation/todo/session_search/cronjob；本机config.yaml SHA256为 `02DCA0E1D3DF C80F693BF9ECFE3C3E70DD3F85E4F361A670D60ADE2A5ED75983`（阅读时去掉中间展示空格；以当前实际哈希为准）。配置及原文件备份存在，新增工具配置启用不等于真实调用全通过。
- F001/F002共用原生态站任务身份；F002验收器在GitHub托管Windows完成42/42**合成证据守卫单元测试**，PowerShell5.1/7 Parser PASS；这些不是Hermes五轮现实执行。

## 3. 10月15日18:58–19:01当前只读现实快照
- 两个正式hermes.exe入口都报告 `Hermes Agent v0.21.5+6841.g8b66a51`；pip元数据另报告0.20.0，属于安装元数据口径差异，**真实CLI--version优先于旧pip显示**。
- `http://127.0.0.1:8642/health` HTTP200；`http://127.0.0.1:3000/health` HTTP200；现有`open-webui-clean` 容器 v0.11.4 healthy，另有历史命名OpenWebUI容器刚启动健康检查中（疑似其它正在执行任务，**未干预，不擅自清理**）。
- 通过既有本机授权读取`/v1/models`返回5个标识：`DeepSeek-V4.1-Flash`、`deepseek-v4-pro`、`deepseek-v4-flash`、`glm-5.2`、`qwen3-vl`；列表存在≠五模型全部完成真实业务调用。
- 同轮`/v1/toolsets`返回WebException，当前工具集实际加载状态**UNKNOWN**；不能以10月15日凌晨F002缓存的“enabled”列表直接替代现在的真实调用。
- 本轮只读核对，未发送Hermes模型任务、未重启容器/Gateway、未修改代理/配置/凭据。

## 4. 本项目尚未完成的部分
A. F002这批五轮生产同构验收**0/5已认证**。R01只有request与round-result，HTTP400/WebException，耗时112ms（不是有效T_VALID）；没有ack/run_id和独立grade；R02–R05没有有效执行回执。BATCH-RESULT=NOT_ACCEPTED，consecutive_pass=0，不能自动重派。
B. 五模型：当前五个alias可被列出，但不同模型正确路由、并行、缓存/成本/真实质量合同未全证。
C. Gate/Repair：已有组件及历史PASS；当前故障注入→自动定位→最小Repair→同项回归→独立Gate真实全流程未由本轮验收。
D. 多智能体：历史双子任务与回执成功；F002拟证明同任务2个真实子代理、独立上下文和Gate汇总尚未通过。
E. 多模态：历史真实PNG成功；当前OpenWebUI网页直接图、视频、音频与一致性验收未全面闭合。
F. 长任务：checkpoint、handoff、resume原生脚本/历史证据可复用；F002本次跨新会话resume及hash链闭合尚未完成。
G. 自动化与启动：原有Hermes+Docker OpenWebUI热态健康；冷开机/登录、浏览器实际聊天、正常恢复、多小时耐久及失败审计尚未通过本项目最终合同。
H. 性能：cold/warm分开，缺本阶段等价任务完整T_VALID和稳定分布；不得把4.853秒候选、CLI健康时间、42单元测试算正式生产T*。
项目阶段结论：**不是空站；有重大可复用历史成果；现状“可运行基础+成熟规则与部分专项能力”，尚非全能力完全闭环和最终成熟认证。**

## 5. 冻结纪律
报告到此只做取证、证据分层及下一页准备，不从零规划新系统、不清空已登录状态、不重装、不开大范围容器、没有为凑5次而重启或重派失败业务。下一页先读对应真实回执和专用v2.0，不对历史PASS机械重复测试。
