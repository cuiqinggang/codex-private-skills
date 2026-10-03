# 长期记忆超级虚拟人｜独立强备份构思与建设合同 R1

更新时间：2026-10-03（北京时间）
任务：LTMVH-INDEPENDENT-BACKUP-20261003-R1
用户要求：以长期记忆超级虚拟人 v0.4.3 为能力基线，建立完全不依赖 GPT、Codex 的同功能强备份；先讨论构思，再建设。方法：极限短时间自动化闭环 v2.0；唯一优化目标 T*=min(T_VALID)。

## 当前状态

STATE=10（方案讨论与成熟路径取证）
DESIGN_STATUS=DISCUSSION_BASELINE
PROJECT_FREEZE=NO
DEPLOYED_BY_THIS_TASK=NO
STRONG_BACKUP_CERTIFIED=NO
FUNCTIONAL_PARITY_CERTIFIED=NO
T_VALID=未产生（尚未达到 FINAL_VALID）

本文件是建设工作基线，不是部署证明，也不代表用户已选择某个候选。
本任务不等候 GPT 主路线 v1.0 毕业才启动备份建设；用户本轮已明确要求先推进强备份。
主技能保持 v0.4.3；不因新建备份方案宣称主项目毕业。

## 1. 已实读的基线与证据边界

- skills/long-term-memory-super-virtual-human/SKILL.md：v0.4.3，FINAL_VALID=NO。
- workspaces/long-term-memory-super-virtual-human-v1.0/SUMMARY.md：Reasonix v1.38.6 + DeepSeek-V4.1-Flash 独立备脑基础 Reality PASS；真实业务 DONE_WHEN 仍 OPEN。
- STRONG_BACKUP_CONTRACT.md 与 BRAIN_FAILOVER_CONTRACT.md：独立强备份尚未认证。
- skills/extreme-time-automation-bridge/SKILL.md：GPT直连Windows双路执行桥 v0.2.0，Windows 双路径具备基础 Reality，整体仍 PARTIAL。
- workspaces/extreme-time-automation-loop-v2.0/REALITY_CONTRACT.md：完整 FLOW_START→FINAL_VALID 计时，失败、等待、恢复和重试不得删掉。
- skills/extreme-time-agent-constitution/SKILL.md：当前 v0.3.1 优先于根 AGENTS.md 中旧 v0.3 内容；成熟优先，允许经现实证据证明必要的最小实现。

上述 PASS 是当前远端摘要记载，本任务没有重跑其历史测试；不能把基础备脑 PASS 当成全功能备份 PASS。

## 2. 功能等价定义

等价锚是现实能力结果和同一 DONE_WHEN，不是界面相同或模型能力口头相同。
先枚举 v0.4.3 用户实际使用的能力及真实任务，形成能力矩阵。每项有任务输入、硬边界、产物、验收器与证据；未测项必须留 OPEN。
验收至少覆盖：
1. 自然语言任务理解、规划、搜索取证和判断；
2. 长期记忆读取、更新、权威状态写回；
3. Windows 文件、命令、进程和仓库工程；
4. 网页/API/MCP 交互、已授权账号功能；
5. 长任务分阶段执行、checkpoint、故障恢复、防任务漂移；
6. 调度、外部故障检测、接管和主路恢复后的安全交接；
7. 用户实际要求的图像/视频/视觉能力，采用非 GPT/Codex 的专项成熟路径；
8. 真实产物验收、错误积累和经验回流。

能力类别覆盖不证明通用智能与 GPT 相等。困难任务质量必须用共同质量合同和真实样本判断。
任何未满足 DONE_WHEN 的降级路线不进入 VALID；更慢但达标的路线可作为备份。

## 3. 最小候选结构

用户独立入口
→ 已成熟 Agent 承载器 + 非 OpenAI 模型
→ 读取同一 TASK_CONTRACT / Checkpoint / 能力索引
→ 直接调用最少必要成熟工具
→ 验证现实产物
→ 写回状态与新的 Checkpoint

恢复监督器在主脑之外；复用 Reasonix Recovery Kit / ECC 已有 checkpoint、lease、fencing、action ledger 等机制。普通任务不默认启用多智能体或叠加调度层。

### 候选 A：优先实查与实测
Reasonix + 已有 DeepSeek 可用配置 + 原有成熟能力池。
原因：已有基础 Reality 记录，预计启动建设阻力最小。这只是优先验证顺序，未证明其完整 T_VALID 最短。

### 候选 B：独立工程执行对照
OpenCode + DeepSeek + 必要 MCP/API/CLI。
用于比较工程、工具调用和长任务恢复；不能未经证据视为完整个人助理替代。

### 候选 C：常驻入口/调度对照
OpenClaw + 非 OpenAI 模型；工程需要时才调用 Reasonix 或 OpenCode。
只有当成熟常驻入口、会话管理、调度能力能填补 A 的实际缺口并改善完整 T_VALID 时保留。n8n 也是可比较的调度组件，不作为必装层。
同一真实任务比较不同组合；有现实需要才引入并行，不默认同时运行三套。

所有框架与模型版本、模型 ID、工具兼容性在实际部署时探测并记录，不沿用旧名字猜测成功。
DeepSeek 第二模型不构成第二供应商冗余；如需抵抗其服务故障，再考察独立供应商或本地候选。本地小模型不预先宣称复杂任务同品质。

## 4. 独立性的硬门

正式备份任务运行期间：
- GPT、ChatGPT、Codex、OpenAI API 不得成为必须可达的节点；
- 任务入口、任务派发、故障检测、凭据读取、模型推理、记忆检索、搜索、视觉/媒体、验收和结果通知都需审查；
- 不能借用“只有 ChatGPT 工具环境才提供”的 Connector 作为唯一接口；邮件、日历、云盘需独立授权 API/MCP 或已有浏览器路径；
- 嵌入模型、总结模型、视觉模型、自动 fallback、插件内部调用也要检查，避免隐性 OpenAI 依赖；
- “OpenAI-compatible API”仅代表协议兼容，不等于依赖 OpenAI 服务；核验实际端点、认证和流量；
- 允许复用本机的 Windows 桥底层成熟能力；桥的调用者、决策与结果消费必须能独立运行。不能只因桥名含 GPT 就认定不可复用，也不能只因底层执行成功就宣称控制面独立；
- 本地 Windows 连接/检查默认优先 GPT直连Windows双路执行桥 v0.2.0；建设过程与灾备运行的依赖分别记录；
- GitHub 是正常状态下的共同权威源；独立本地快照作为断网恢复源，记载版本、时间、哈希和未同步增量，不以旧快照覆盖更新远端；
- GPT 浏览器保持打开，禁止为了测试关闭它；以备份进程限定的拒绝访问/故障注入验证独立性，不修改全局 FlClash 或 Windows 网络代理。

由 GPT/Codex 协助建设不等于灾备运行依赖它们；独立验收时它们不能提供步骤、审核或唤醒。
依赖审计应记录实际调用端点和进程，不记录密钥/Token/Cookie。

## 5. 接管与副作用控制

外部观察器判定明确不可用或超过任务专属恢复窗口
→ 查原执行是否仍有进展/已产生结果
→ 获取写租约并隔离旧 writer
→ 读取合同、检查点和动作账本
→ 核对未决现实动作
→ 独立备脑继续任务
→ 独立验收
→ 状态写回

主路恢复后先读新状态并做交接，不并发重放旧动作。
“exactly-once”是验收要求，不能只靠锁保证跨外部系统效果恰好一次。对有副作用动作，优先用外部幂等键、动作账本和结果对账；无法确定已执行状态时先核实，不盲重试。

## 6. Reality 测试顺序

R1 能力盘点与依赖审计：
读取已有安装、版本、配置、Recovery Kit/ECC 机制；不泄露凭据。冻结代表任务及统一 DONE_WHEN。

R2 独立冷启动：
主路不给任何任务指导，从独立入口读取权威合同/快照，运行一项真实有用任务并保存验收证据。不能只测 ACK。

R3 中途接管：
同一任务在已有安全 Checkpoint 处，使备份进程访问 GPT/Codex 路线不可用，外部监督器独立发现、取得租约、继续至同一 DONE_WHEN。保留主浏览器，不停止其他业务。

R4 备份自身恢复：
终止备份任务进程/模拟工具短暂故障，验证成熟监督机制自动恢复；记录未决动作对账与重复动作检查。

R5 状态源故障与主路回归：
GitHub 暂不可达时从已确认快照读取并保留增量；恢复后安全同步；旧主路恢复时没有双 writer、漏动作或重复副作用。

R6 功能矩阵与时间对照：
在匹配起始条件、输入、质量合同、缓存/登录态的代表任务上比较 A/B/C。首次部署时间单列，任务内故障检测、排队、模型判断、工具执行、返工、验收、保存和恢复全部计入同一 FLOW_START→FINAL_VALID 时间轴。

认证至少分两层：
- 场景 PASS：仅对已验收任务类别有效；
- 强备份 CERTIFIED：必须完成约定能力矩阵、真实任务和故障测试，不用单次成功泛化全部功能。

## 7. 时间唯一目标

T*=min(T_VALID)，质量、正确性、权限和证据决定 VALID 集合。
失败路线不产生 T_VALID，不参与“最快成功路线”排序，但失败耗时、失败次数和原因必须保留，避免筛选成功样本造成虚假速度优势。
接管不得从恢复时重新起表；原 FLOW_START 保持不变，另列恢复时长作为瓶颈解释。
冷/热启动、健康/故障场景分别比较；同场景不得只拿模型响应速度代替端到端时间。
成本与免费偏好作为候选可用性约束；不默认购买新服务，不把费用与时间并列优化。

## 8. 当前下一步

先与用户讨论以上结构及“同等功能”的现实能力矩阵，然后按授权推进成熟组件盘点与代表任务合同。
用户已要求建设，不应要求其再次批准普通只读盘点或可逆准备。
本轮仅形成远端建设基线，尚未部署、触发接管或完成独立业务 Reality。

## 官方成熟候选来源（2026-10-03 已浏览）

- DeepSeek/OpenCode：https://api-docs.deepseek.com/quick_start/agent_integrations/opencode/
- OpenClaw/DeepSeek：https://docs.openclaw.ai/providers/deepseek
- OpenClaw 记忆配置：https://docs.openclaw.ai/reference/memory-config
注意：OpenClaw 文档明确记忆检索默认嵌入 provider 为 openai，需显式选择非 OpenAI 路线。官方功能存在不等于本机组合已验收。

## 用户纠正后的正式方向（2026-10-03 R2，覆盖 R1 的路线选择及测试顺序）

用户明确：目标是一套日常即可独立运行、不使用 GPT/Codex 的完整成熟自动化流程，作为 v0.4.3 的额外强备份；不是先做 GPT/Codex 不可用模拟，再搭备脑。

判断：保留“独立强备份”的现实目标，撤销“默认新建另一套编排/恢复系统”的建设预设。先找完整成熟产品并直接采用其原生记忆、工具、调度、恢复与模型后备；仅做必要配置、现有任务合同/状态接入和真实业务验收。

候选筛选改为完整产品优先：Hermes Agent、OpenClaw 等 + 非 GPT 模型。Reasonix/OpenCode 仅在成品确有工程执行缺口时按需接入；n8n/LangGraph 作为调度/框架能力，不能仅凭组件成熟就宣称完整个人助理等价。

官方资料核验：
- Hermes 原生持续记忆、技能和定时自动化：https://hermes-agent.nousresearch.com/docs/
- Hermes 模型后备：https://hermes-agent.nousresearch.com/docs/user-guide/features/fallback-providers/
- OpenClaw 完整个人助理入口：https://docs.openclaw.ai/start/openclaw/index.html
- OpenClaw 模型后备：https://docs.openclaw.ai/concepts/model-failover
- OpenClaw Gateway 重启会话恢复：https://docs.openclaw.ai/concepts/session
- LangGraph 持久化属于应用框架能力：https://docs.langchain.com/oss/python/langgraph/persistence

成熟功能存在不等于每种故障都能不中断。模型后备需要配置；本机断电/磁盘故障/所有外部服务不可达的恢复范围取决于部署与独立资源。恢复允许短暂停顿，同一任务状态与完成标准不能丢失。

下一步：核对用户已有成品安装与可用功能 → 选一个最小完整成熟组合 → 直接完成真实任务 → 验证该产品原生恢复及其承诺范围 → 只对已证实缺口做最小配置/接入。GPT/Codex 不参与运行是部署属性，故障注入只是后续验收手段之一。

T*=min(T_VALID) 保持唯一优化目标；未有真实业务结果前不宣称同等功能已成熟。当前仍 STATE=10、未部署、未认证。

## Hermes 已选定与现存自启技能定位（2026-10-03 R3）

用户已选择 Hermes Agent，明确已有安装与能力，要求直接复用；并授权需要时恢复原有开机启动。用户随后要求先找到完整自启技能包。

已找到：skills/hermes-014-restoration-ladder/SKILL.md，核心参考为 references/stage-04-8642-silent-healthcheck-20260522.md、references/stage-04b-openwebui-autoopen-build-runbook-20260522.md。该包包含静默保活、Docker/Open WebUI 网页面板自启、安装/验证/回滚和历史真实重启证据。历史 H 盘路径已过时，本机现存脚本已改用 C 盘。

通过 Windows 桥 Remote 主路实查：Hermes v0.20.0 (2026.8.3)，安装 C:\Users\A\.hermes\hermes-agent；CLI 仅显示 default，gateway stopped；3000 HTTP 200；8642 检查不可用。Hermes8642SilentHealthCheck 及旧任务均 Disabled。现存 C:\Users\A\Hermes_AutoStart\healthcheck-8642 和 openwebui-autoopen 脚本；Startup 的 HermesOpenWebUIAutoOpen.vbs 不存在。

本轮发出启用/启动 Hermes8642SilentHealthCheck 请求后 Remote 回执丢失，不能确认写操作完成，不得重复派发。GitHub 备路已提交只读状态核查：run 37120091817，任务 LTMVH-HERMES-STARTUP-AUDIT-20261003；静态门 PASS，Windows job 执行中，结果待回收。

当前主项目/强备份仍未认证。不启用旧 Watchdog/旧 NewAPI AutoRecover；不重启 Windows；不修改网络代理，不发送 Telegram 消息。下一步：先回收只读核查结果，确认启用操作实际状态，再恢复已验证的原网页自启入口、验证独立非 GPT/Codex 业务链路。


## 自启恢复 Reality（2026-10-03 R4，覆盖 R3 待确认状态）

用户授权经 GPT直连Windows双路执行桥 v0.2.0 恢复自启，并在 GPT 旁边打开网页。
Remote 主路实际恢复：Hermes8642SilentHealthCheck 已 Enabled=true；2026-10-03 20:02:02+08:00 新 healthcheck 状态 healthy，8642 health OK。
网页包装器原文件先备份为 Open-HermesOpenWebUI.ps1.before-20261003-R4，仅将旧模型断言 Hermes-GLM-5.2-OpenRouter 改为 DeepSeek-V4-Pro；实际 /v1/models 已包含该 id。未改模型/provider 配置。
调用原 Install-HermesOpenWebUIAutoOpen.ps1，返回 G_INSTALL_PASS_STAGE04B_STARTUP_VBS_READY；Startup 的 HermesOpenWebUIAutoOpen.vbs 已存在。原 VBS 手动调用成功。2026-07-06 去重文档提示存在较新主 opener，但现场其 Hermes_OpenWebUI_AutoStart_Hidden.vbs 已 disabled，本轮仅保留一个活跃网页 opener，没有同时启用两个。
本次成熟启动日志 daily-start-20261003-200718.log 于 20:07:57 FINAL_PASS：Hermes8642 healthy、Docker API ready、open-webui-clean 启动、3000 HTTP PASS、浏览器已打开。包装器状态于 20:08:08 FINAL_PASS；该结果证明启动/网页可达，不证明账号登录或强备份功能等价。
通过 Windows 本地 CDP9223，在现有 GPT 浏览器新增 3000 标签页并 bringToFront；保留原 GPT 标签页。正式 UI 读回为 /auth?redirect=%2F，显示“登录 Open WebUI / 电子邮箱 / 密码 / 登录”。未获得可用登录会话或原自动账号登录脚本，WEB_ACCOUNT_LOGIN=BLOCKED_CREDENTIALS，不重置账号、不关闭认证、不提取浏览器密码。
本轮未重启 Windows，REBOOT_TESTED=NO；未修改全局代理、未发送 Telegram 消息；Telegram 可用性未重新验收。
GitHub 备路旧审计 run37120091817 failure；无需 checkout 的 run37121562608 已在 DESKTOP-4A1EGTM-etal 执行，但用户账号不是 A，安全前置检查在写入前阻止操作。最后通过恢复后的 Remote 主路完成上述修改与读回。
STARTUP_RESTORED=YES；MANUAL_STARTUP_REALITY=PASS；WEB_OPENED_BESIDE_GPT=YES；WEB_ACCOUNT_LOGIN=OPEN；STRONG_BACKUP_CERTIFIED=NO；FUNCTIONAL_PARITY_CERTIFIED=NO。
下一步仅需现有 Open WebUI 账号登录后核验真实任务与独立运行能力；本轮不可把启动通过记作完整 FINAL_VALID。
