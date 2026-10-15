# Hermes F014｜Codex 与 Knowledge Brain 按需复用真实验收
日期2026-10-15；TASK=HERMES-ECO-20261014；总方法《三人行》V2；Windows连接桥V6 C→A→B；Hermes 母技能v2.0。
前置冻结 F014_CODEX_KNOWLEDGE_ON_DEMAND_FREEZE_20261015.md；本节点结果=SCOPED_RUNTIME_PASS。

## 现实输入、行为和原生证据
F013 官方外部目录接线后 Hermes skills_list=171，母技能及Repair适配器可以 skill_view。
F014首次直接Hermes CLI 一次只读任务，实际原生read_file成功读取：
1) C:/Users/A/.codex/skills/verification-before-completion/SKILL.md，提取 name=verification-before-completion / title=Verification Before Completion / 在声明完成前先获取当前任务独立验收证据、实际读运行输出和退出码。
2) C:/Users/A/.codex/knowledge-brain/ROUTING_MAP.md，确认 If task is about reusable workflows/skills 的首指向 indexes/skills-index.md，技能根 C:/Users/A/.codex/skills。
该次正式CLI exit0、进程runtime30.28s；原始文件完全未改，不把独立技能数量推断为已经完整兼容。

## 持久的最小方法部署
在旧Hermes自有 C:/Users/A/.hermes/skills/hermes-mature-supertool/ 中：
- 变更前精确备份母SKILL.md到 C:/Users/A/.hermes/backups/hermes-f014-kb-route-20261015-SKILL.md，文件哈希一致。
- 新增 references/CODEX-KB-ON-DEMAND-20261015.md，规定先Hermes原生skill_view已有技能，遇跨Codex需求则Knowledge Brain INDEX→ROUTING_MAP→indexes/skills-index→Top-K SKILL.md和必要reference，不全量读库、不自动改写Codex文件。
- 母SKILL.md仅加一段该reference的入口指针，原v2.0上位框架及F011 CLI优先入口保持不变；最近使用日志增加F012-F014真实成果索引。

## 再次真实驗收新方法
另启Hermes正常CLI独立只读任务，原生skill_view(name=hermes-mature-supertool, file_path=references/CODEX-KB-ON-DEMAND-20261015.md) success=true、无错误；正确返回Knowledge Brain前三路由文件 INDEX.md、ROUTING_MAP.md、indexes/skills-index.md 和不开放 Codex 自动写权限理由。进程 exit0、runtime77.01s。这里的时间是不同任务进程runtime，不能用来声称优化快慢。
此外通过官方已有 C:/Users/A/.codex/knowledge-brain/tools/kb_health_check.ps1 完成安全只读健康验收：HOT_KB_INDEX、HOT_ROUTING_MAP、ROUTING_POINTS_TO_C_HOT_KB、K_BACKUP_ONLY、HOT_ROUTE_RULES、COORDINATE_ENTRY、PERMISSION_REPORT、HOT_SYNC_SCRIPT、DEEP_SYNC_MANUAL_SCRIPT 均PASS；FINAL_RESULT=PASS。

## 本次实测资产数量及禁止误报
C:/Users/A/.codex/skills 209一级目录、218递归SKILL.md；C:/Users/A/.hermes/skills 85一级目录、161递归SKILL.md；C:/Users/A/.codex/knowledge-brain 632份文件。来源重复、嵌套、版本与非标准文件不能加总为总可执行技能数。
Codex目录**没有**直接添加到skills.external_dirs；官方说明agent对外部技能目录可能自动修改，所以本任务先保证按需只读获取、再按独立任务授权执行，避免破坏既有Codex项目。至此，Hermes原生171条技能可发现及特定Codex/KB跨根按需读取是有效当前证据，绝不宣称218个Codex技能全部运行认证。

## 未闭合
F011全包静态检查再次真实结果：PowerShell parser4文件零错误、JSON21文件零错误等PASS；high_confidence_secret_patterns有1个YAML模式命中，导致full checker FAILURE_COUNT=1，仍未调查或处理该含敏感风险旧备份，禁止泄露文本/为报绿盲删。
Open WebUI登录网页交互、音频视频、跨Hermes会话恢复、正式同合同五轮和长期观察仍未完成。FINAL_VALID=NO，F002旧5轮0/5，HTTP原生Runs API独立另行处理，不能阻断CLI/GUI业务。
