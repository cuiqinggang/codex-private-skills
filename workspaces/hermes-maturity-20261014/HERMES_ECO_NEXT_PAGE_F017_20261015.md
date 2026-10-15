# Hermes 爱马仕 AI 生态站｜F017 可直接接续上下文
TASK_ID=HERMES-ECO-20261014｜LAST_FREEZE=HERMES-ECO-F017-20261015｜FINAL_VALID=NO｜FIVE_INTEGRATED_ROUNDS=0/5。
方法硬约束：《三人行》第2版（该Hermes项目用户显式要求，未将全局V1改成V2）、《GPT直连Windows双路执行桥 V6.0》C→A→B、Hermes现役母技能v2.0。所有成熟资产优先从在线GitHub当前状态定位，不先去K/H盘寻旧资料。唯一当前状态：cuiqinggang/codex-private-skills/workspaces/hermes-maturity-20261014/HERMES_ECO_CURRENT_20261015.json。

## 当前真实收敛的关键能力
1. F010：原正式CLI C:/Users/A/AppData/Local/hermes/bin/ltmvh-hermes-formal.ps1 (OpenRouter deepseek-v4.1-flash)在F005_REPAIR隔离目录真正修复invoice.py，GPT独立Python unittest8/8 PASS；原F002没有改写。自写F002 POST /v1/runs HTTP400是旧验收脚本input对象合同错误，独立API待修，不再阻断正常CLI。
2. F013大根因：当前正式Hermes实际HOME=C:/Users/A/AppData/Local/hermes，而既有自定义技能在 C:/Users/A/.hermes/skills；skills.external_dirs原[]使技能不存在于当前Hermes索引。按官方hermes config set只把此旧Hermes自有技能根加入active profile，改前配置只做本机SHA一致备份。一次真实新会话skills_list72→171，原生skill_view hermes-mature-supertool和hermes-repair-loop-adapter均SUCCESS，**本故障已闭环不重做**。不改变代理/密钥/Docker/浏览器。
3. F014：Codex根 C:/Users/A/.codex/skills 实数209一级目录218递归SKILL.md；旧Hermes根85目录161份SKILL.md；Knowledge Brain根 C:/Users/A/.codex/knowledge-brain 632文件，跨源重复/旧版/非技能，不加总当有效技能数。Hermes原生read_file真实读取Codex verification-before-completion与Knowledge ROUTING_MAP，原生skill_view又真实加载母技能reference CODEX-KB-ON-DEMAND-20261015.md。KB官方kb_health_check.ps1 FINAL_RESULT=PASS。由于外部skills.external_dirs可写入源，不直接批量注册Codex可写根，保护原Codex库；使用INDEX→ROUTING_MAP→skills-index→Top-K SKILL.md定点读取。
4. F016自然任务不给技能名称，Hermes通过母skill_view+知识库索引自主读取3个相关Codex技能并产出PowerShell5.1三门正确计划，退出0、process runtime202.49s（有效但偏慢）。
5. F017虚拟成熟后仅一次对照：相同意图和三质量门，跳过已冻结的全局INDEX/ROUTING，只精准搜索现有skills-index并读取最佳1份powershell-reliability-guard SKILL.md，exit0、runtime91.82s，质量门全在。认定REALITY_OBSERVED_CANDIDATE KEEP，不宣称稳定T*或固定倍率。本机母技能reference CODEX-KB-ON-DEMAND-20261015.md已经备份后增量写入F017快路，F011 CLI-first reference添加《三人行》V2真实GitHub正文和固定blob。**无需继续对这个简单场景迭代复验**。
6. F008本阶段原生delegate_task两个孩子实际completed，F006任务级checkpoint/handoff独立新进程恢复closed_PASS，F007图片内容识别正确但缺具体vision_analyze tool事件。

## 仍需处理的独立Gate，严禁误报
- F011技能包正式静态全验仍为FAIL：唯一一处历史YAML secret-like命中，4 PowerShell parser、21 JSON均PASS。没有读取/输出疑似secret。处理需安全非敏感审计及不可变证据保护；不能为凑PASS删配置。
- F015原有Chrome未提供可授权使用的127.0.0.1:9222 CDP，3000/health之前HTTP200只是服务可达，并非网页E2E。不能重启已登录浏览器或另开第二个浏览器；有真正合法GUI操控再测试。
- 真实五模型路由、音频视频、Hermes Agent Session跨重启恢复、冷启动、7-14天真实耐久、同合同综合连续5次、T_VALID分布均未本阶段认证，整站 FINAL_VALID=NO/0-5。
- 原F002旧API请求UNKNOWN无ack/run_id，不自动重投、不绕过Bearer/API安全控制。

## 下一自然工作
按《三人行》V2：项目Freeze→已跑通成熟Baseline→GOOD/BAD/FIRST_DELTA→不超过三个实质成熟候选→虚拟成熟/攻击树冻结→一次合法Reality→真实外部证据→KEEP/ABANDONED/NOT_APPLICABLE；只对净收益和本阶段真实缺口推进，DONE不重做，UNKNOWN先对账。
下一个优先 F018：独立、安全地治理遗留YAML秘密模式静态告警，保留原始备份与F002证据，不读取/输出secret、不为假PASS放宽scanner。若现有授权无法在只读边界消解则明确BLOCKED，同时推进合法独立分支；UI在合法现有窗口操控可用才做；其余多模态/Session恢复按依赖和授权按需调用既存正式CLI。
