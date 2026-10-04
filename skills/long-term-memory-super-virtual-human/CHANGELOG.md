# CHANGELOG

## 0.6.0 - 2026-10-04

- 将故障恢复正式升级为 **FIRST_PRINCIPLES_FAULT_ANALYSIS_AND_MINIMAL_REPAIR（第一性原理·故障分析与最小修复）**：默认从能力成立的最小条件出发按因果链逐层验证，不再把“从报错末端不断猜测/试错”作为默认方法；
- 明确第一性原理分析不等于重建：第一性原理决定定位逻辑，最小定点修复限制修改范围；找到首次偏差后只修该层，只有临时实例本身失效时才受控重建该实例；
- 新增 `FIRST_PRINCIPLES_RECOVERY.md`，冻结因果链模板、首次不成立点原则、禁止末端无边界试错、禁止无新证据机械重复等规则；
- 固化三类经验：Windows 本地连接桥历史恢复、专用 ChatGPT 浏览器/CDP 9223 Reality R2、爱马仕升级后登录凭据恢复；
- 9223 R2 真实根因：旧 `cmd.exe` 启动壳仍在，但真正 Chrome 主进程已经不存在，因此 9223 无监听；前置 executable、`shared-mcp` profile 保持不动，仅恢复缺失的唯一 Chrome 主进程后恢复；
- 9223 R2 Reality：端口监听 PASS、`/json/version` PASS、ChatGPT target PASS、Attach-Only runtime PASS、RAW CDP 真 New chat→提交→GPT ACK PASS，`submissionCount=1`、`branchUsed=false`、`newBrowserLaunched=false`；
- 新增证据 `evidence/V060-FIRST-PRINCIPLES-RECOVERY-20261004-R1.json`；
- 更新 `RECOVERY.md` 与主 `SKILL.md`，除明确单点初级错误外，Goal Loop 故障处理只允许进入第一性原理因果分析；
- 当前只认证“方法 + 9223 第一性原理定位与局部修复真实恢复”；**自动检测控制平面死亡并自动触发受控重建的完整故障注入 E2E 尚未认证**；
- 项目级 `FINAL_VALID=NO` 不变，v1.0 毕业门槛不降低。


## 0.5.0 - 2026-10-04

- 新增默认目标循环：授权任务持续判断、执行/调度、真实验证、定向返修、保存进度，达标关闭；
- 新增 GOAL_LOOP_CONTROLLER.md 与任务级薄适配器，复用循环工程 V2.0.0；沿用唯一连续性 runtime/global writer，不增加常驻并行调度器；
- 两种现有 runtime 传输路径均可处理 goalLoop 任务；绑定任务合同、冻结适配器哈希、稳定 actionId、恢复核对与反假完成门；
- 本地确定性测试 12/12 PASS，实际独立进程/文件简单验收 4/4 PASS，runtime 接线语法检查 PASS；真实 Windows/浏览器端到端 Reality 未执行，用户电脑未部署；
- 项目级 FINAL_VALID=NO 保持不变；v0.4.5 干净 CEO 生命周期冻结合同与证据保留。


## 0.4.5 - 2026-10-04

- 冻结专用 ChatGPT 浏览器 **Clean CEO Lifecycle（干净 CEO 生命周期）**：空闲态只保留 1 个空白 New chat 页；该页直接复用为 CEO-1；执行页只按业务最小数量临时创建；结果持久化后立即关闭；最终再次恢复 1 个空白页；
- Reality R18 / R19 完整通过：CEO-1 拆分 → A/B 独立执行 → 最小 checkpoint → 关闭 CEO-1 → 真正 New chat CEO-2 接管 → 使用原 A/B 结果 → FINAL_VALID → 执行页/CEO 清理 → 单空白页收口；
- R18 `T_VALID=51,454 ms`，R19 同构复验 `T_VALID=54,246 ms`；当前观测 `T*=min(T_VALID)=51,454 ms`，来源 R18；该值是当前合同下实测最好值，不声明为数学绝对下界；
- R18 checkpoint 仅 125 chars；冻结“页面只是运行时资源，记忆/状态必须持久化”的规则；
- 页面资源规则：`IDLE_CHAT_PAGE_TARGET=1`、`EXECUTOR_PAGE_COUNT=MIN_REQUIRED_ONLY`、`PREWARM_UNUSED_CHAT_PAGES=NO`、`CLOSE_EXECUTOR_AFTER_RESULT_PERSISTED=YES`、`FINAL_BROWSER_STATE=ONE_BLANK_NEW_CHAT_PAGE`；
- 实测淘汰为默认路径：A/B 提前预热、Instant 控制链、CEO 同物理 tab 复用、删除独立接管确认回合；这些路线没有降低完整 T_VALID，部分显著变慢；
- 不改变项目级 `FINAL_VALID=NO`；本次升级只冻结 CEO 专用浏览器控制链、页面清理合同和当前极限短时间路径。


## 0.4.4 - 2026-10-04

- 将 LTMVH 页面连续性正式收敛为**唯一生产控制链**：`CHATGPT_SESSION_CONTINUITY_CONTROLLER.md` + 单一 supervisor/runtime；旧恢复/换页方案全部转为历史参考，不再并行运行；
- 新增 `LEGACY_CONTINUITY_INDEX.md`，保留旧恢复阶梯、旧连续性规范、Reality、失败证据和 Git 历史；不删除历史成果；
- 总控/CEO 页面采用预防性增长阈值：默认可见文本 40,000 或用户轮次 10，任一先到即在安全 checkpoint 主动换真正 New chat；执行页默认 30,000 / 3 轮；
- 同页压缩/总结不再被视为释放上下文的性能机制，只可作为 handoff 状态材料；
- 统一页面异常触发器：增长、阶段结束、历史断连、UI/加载/发送异常、无进展、活跃 turn 卡死；统一进入同一决策器；
- 保留断连保守规则：若后台仍有活动或最终答案可能产生，则先只读 probe / 等待，避免重复执行；确认停滞后才停止旧 turn、checkpoint、true New chat、exactly-once；
- RAW CDP fallback 增加页面观察与卡死停止能力，避免当前真实 fallback 路径只会“收任务后换页”而不能持续监测；
- Reality `LTMVH-CEO-ROTATE-REALITY-20261004-R1` PASS：existing shared-mcp browser retained、true New chat、submissionCount=1、markerCount=1、ACK=true、Branch=false、newBrowserLaunched=false；
- `FINAL_VALID=NO` 不变；v0.4.4 是连续性策略/运行层升级，不代表整个 LTMVH v1.0 毕业。

## 0.4.3 Capability Registry Extension - 2026-10-03

- **不升级 LTMVH 核心版本**：v0.4.3 连续性 runtime 与既有 Reality 状态不变；
- 新注册独立能力包 **收费转免费·开源替代技能包 v1.0.0**：`skills/paid-to-free-open-source-replacement/`；
- 新增 `2026-10-03-R1` 目录，收录 96 项收费/商业软件 → 免费/开源/自托管候选；
- 强制 `FREE_IS_NOT_OPEN_SOURCE`：区分 OSS、开放核心、Source-available、Freeware；
- 新增 Agent 操作优先级：API/CLI/MCP/Headless 优先，生产替换必须通过任务级 DONE_WHEN Reality；
- 本扩展只增加可调取能力，不改变 `FINAL_VALID=NO` 与 v1.0 毕业门槛。

## 0.4.3 - 2026-10-03

- 修复专用 ChatGPT 浏览器重复 launch / 标签页累积死循环：Reality R15 观察到修复前 watchdog 已累计 `browser_launch_once=12`；
- Watchdog 新增 Windows boot launch latch：同一次 Windows 启动自动 launch 上限固定为 1；只要检测到任意现有 Chrome-for-Testing 专用进程，即 fail-closed，不再 launch；
- Watchdog 不再通过 `Target.createTarget` 自动补 ChatGPT 标签页，避免健康检查误判时无限造页；
- 禁用注册表 `GoogleChromeAutoLaunch_*` 的额外 Playwright Chromium 开机入口，并保存恢复备份；
- 旧 `ChatGPT-Continuity.cmd` 开机入口不再启动旧 supervisor，改为启动 v0.4.3 attach-only runtime；runtime 使用 `--never-launch true --no-auto-new-page true`；
- Reality：修复版运行 15 秒及追加 20 秒后 launch 计数均保持 12，专用顶层窗口保持 1；当前 CDP 故障时状态为 `CDP_DEGRADED_EXISTING_BROWSER_NO_RELAUNCH`；现有浏览器未关闭；
- 权威证据：`evidence/SINGLE-BROWSER-LOOP-FIX-REALITY-20261003-R15.json`；`FINAL_VALID=NO` 不变。

## 0.4.2 - 2026-10-03

- 闭合 ChatGPT 模型/Thinking 完整 E2E：复用现有 shared-mcp 浏览器，经 CDP 连接完成 High→Medium 实际切换、语义读回、exactly-once continuation、ACK、非法档位 fail-closed，并恢复原 High；Reality R14 PASS；
- 修复中文界面兼容：`中/高` 与 `Medium/High` 双向归一化，不再把中文 UI 标签误判为未认证档位；
- E2E harness 改为 `connectOverCDP` 复用现有浏览器，删除再次 `launchPersistentContext` 的错误路径；
- 当前 ChatGPT 新 DOM 不再暴露旧 `data-message-author-role` 时，R14 使用页面可见“你说/ChatGPT 说”语义完成 exactly-once 验证；
- `FINAL_VALID=NO` 不变；仍需 DCR 真正注销/重登、真实有价值长任务 FINAL_VALID、独立备脑业务级 DONE_WHEN。

## 0.4.1 - 2026-10-03

- 闭合会话连续性的剩余核心门：安全长回答故障注入 → 活跃 turn 静默超时 → read-only probe → 自动停止旧 turn → Checkpoint → 真正 New chat → 最小 handoff exactly-once → ACK，Reality R10 PASS；
- Session Continuity Supervisor 新增活跃生成超时分支，确定性回归由 17/17 提升为 19/19；
- 修复当前 ChatGPT UI 兼容：停止按钮现为 `aria-label="停止"` 时也可检测与终止；
- existing-browser raw CDP 发送器将 composer hydration 等待窗口由 5 秒扩展到 20 秒，保持 attach-first / launch-last；
- R8、R9、R10 首次尝试均 fail-closed，未被冒充为 PASS；最终 R10 证据记录 `submissionCount=1`、`markerCount=1`、`ACK=true`、`branch=false`、`newBrowserLaunched=false`；
- `FINAL_VALID=NO` 不变；仍需 DCR 注销/重登、模型/Thinking 完整 E2E、真实有价值长任务 FINAL_VALID、独立备脑业务级 DONE_WHEN。

## 0.4.0 - 2026-10-03

- 将 v0.3 已完成的连续性成果正式升级为默认运行合同，而不是可选恢复模块；
- Reality R6 已证明：复用既有 shared-mcp 登录浏览器、禁止第二次 launch、同一浏览器进入真正 New chat、禁止 Branch、最小 handoff、exactly-once、ACK 确认、PAGE_LEASE 保留；
- 现有浏览器控制采用 attach-first / launch-last；Playwright attach 或 DOM 确认不兼容时，自动切 existing-browser raw CDP，仍不得重开浏览器；
- 全局 writer lease 成为唯一写入权威，修复 Windows PID reuse 导致“假 owner”问题；
- 当用户明确指定“长期记忆超级虚拟人”运行当前任务时，连续性监控、Checkpoint、长页提前轮换、true New chat、浏览器复用、禁止 Branch、exactly-once 自动生效；
- 长任务默认“能安全换就提前换”，不等到页面彻底卡死后才处理；
- 断连仍采用保守判断：连接断开不等于后台停止，先观察/只读探测，确认停滞后再恢复；
- v0.4.0 仍保持 FINAL_VALID=NO；自然发生的“长回答真实卡死 → 自动识别 → 自动恢复”完整故障注入 Reality、DCR 注销/重登、模型档位完整 E2E 和真实业务长任务 FINAL_VALID 仍为后续门槛。

## 0.3.0 - 2026-10-03

- 正式做一次成果状态固化：版本由 v0.2.1 升级为 v0.3.0；VIRTUAL_MATURE=YES，FINAL_VALID 继续保持 NO；
- 保留并登记既有 Reality：Session Continuity Supervisor 15/15、ECC lease/takeover/fault 59/59、Reasonix/DeepSeek 独立备脑 PASS、K 盘仓库备份与恢复 PASS、Windows 双路径基础能力；
- 根据新的直接使用证据修正换页规则：**“Branch in new chat / 在新聊天中分支”不得作为故障恢复的新页**；
- 恢复目标固定为真正的 ChatGPT **New chat**，只投递最小 handoff，不重放整个旧会话；
- Session Continuity Supervisor 升级：新增 Branch 拒绝门，回归扩展为 17 PASS / 0 FAIL；
- 新增 `runtime/chatgpt-continuity-runtime.js`：外部监测页面健康/断连/静默窗口/上下文膨胀，在安全 checkpoint 自动生成最小恢复包并切到真正 New chat，marker 防重复发送；
- 恢复路径继续遵守 conservative post-disconnect：断连横幅不等于后台任务失败；先只读探测，超出任务专属窗口后才换页；
- v0.3.0 是成果固化与连续性实现版本，不等于 v1.0 / FINAL_VALID；真正“旧页故障 → New chat → exactly-once 继续”的 Reality 仍需本轮复验。

## 0.2.0 - 2026-10-02

- 吸收 Reasonix Recovery Kit 的成熟通用机制，但不复制历史 96/100 评分为本项目成熟度；
- 新增 `MATURE_CAPABILITY_ABSORPTION_R1.md`，按 DIRECT_COPY / LIGHT_ADAPT / REFERENCE_ONLY 分类；
- 新增 `CHATGPT_MODEL_EFFORT_CONTROLLER.md`；
- 新增 `CHATGPT_SESSION_CONTINUITY_CONTROLLER.md`；
- 新增 `CLOUD_RUNTIME_OPTIONS.md`；
- ChatGPT 页面模型/Thinking 自动调整改为“主脑决策 + 外部确定性控制器 + 读回确认”；优先复用 Playwright Native AI Browser；
- 页面卡顿/上下文损坏与 GPT 服务级不可用分层处理；
- 长流程优先复用 ECC v3.1.1，不重造第二套 lease/fencing/checkpoint/Gate/Repair；
- Mature AI Coding SuperTool Ecosystem Station 保持按需唤醒，不做永久中间层；
- OpenAI 托管云、Codex Cloud、Work Cloud Browser 与自有 VPS 明确分层；
- 定义 v1.0 七项 Reality 毕业门槛；
- 当前仍不宣布 VIRTUAL_MATURE。

## 0.1.1 - 2026-10-02

- 新增系统级低相关冗余合同：关键能力至少两条成熟路径；
- 明确主路优化完整 T_VALID，备路首先保证 VALID 与可恢复，允许更慢；
- 新增 Failover-Before-Repair：主路异常先切备路恢复业务，再修主路并补回冗余；
- 新增 `RESILIENCE_REDUNDANCY.md`；
- 新增 `EXECUTION_PROFILES.md`；
- ECC v3.1.1 正式作为长流程成熟档位按需调用，不重复造第二套；
- 本机“成熟态 AI Coding SuperTool 生态站”正式作为复杂任务按需执行档位，不做永久常驻中间层；
- Windows 主备控制面明确为 Desktop Commander Remote + GitHub self-hosted runner；
- 人工只保留用户本人不可替代动作，不作为普通故障兜底。

## 0.1.0 - 2026-10-02

- 建立首个技能包版本；
- 固定“轻入口、强能力池、按需激活”；
- 明确产品定位；
- GPT 作为当前首选主脑候选，但不写成不可替代真理；
- 引用极限短时间智能体宪法 v0.3.1、自动化闭环 v2.0、Windows 双路桥 v0.2.0；
- 建立 TASK_CONTRACT、Checkpoint、漂移 Benchmark、模型路由和独立强备份要求。

## 0.2.0 Reality attempt 01 - 2026-10-02
新增未认证薄控制器及失败证据；零发送 probe 已执行，独占控制未证明，保持 NOT_E2E_CERTIFIED，不升版。


## 0.2.0 Reality closure R2 - 2026-10-02
- 正式签署 `VIRTUAL_MATURE=YES`；`FINAL_VALID` 继续保持 NO，未提前升级 v1.0；
- ChatGPT Model/Effort：独占 shared-mcp Reality 建立，Medium → High + 语义读回 PASS；
- 正式 exactly-once business entrypoint 已复用；本轮 send 未在 10 秒内 DOM 确认，后续 Cloudflare challenge 阻断恢复读回，因此完整 E2E 仍 OPEN；
- E2E harness 修正为任何中途失败都在 finally 优先尝试恢复原档；
- 新增薄层 Session Continuity Supervisor，9/9 单测通过；
- ECC v3.1.1 lease/takeover/fault 直接 Reality 59/59 PASS；
- Reasonix v1.38.6 + OpenRouter/DeepSeek-V4.1-Flash 独立备脑 Reality PASS（8045ms）；
- 确认 DCR 当前在线且存在登录 Startup 入口；GitHub self-hosted runner 为 Running + Automatic；
- 新增 `evidence/REALITY-CLOSURE-20261002-R2.json` 作为本轮权威证据。


## 0.2.1 - 2026-10-02
- 修正连续性策略：高频预防换页，但“连接已断开”不再直接等同任务失败；
- 大型独立问题允许默认“一大问题一页”，以更短上下文换取更稳定的长流程；
- 断连发生在生成中时先只读探测/观察后台结果，超过任务专属窗口后才 exactly-once 换页；
- CAPTCHA/真人验证正式建模为 HUMAN_VERIFICATION_REQUIRED，自动化暂停等待用户完成，不尝试绕过；
- 新增“VALID-first failover”：最快路径本轮过不去时，从有效候选集中移除并切成熟备路完成现实结果；
- v1.0 毕业门槛由“指定实现必须成功”改为“能力结果至少有一条 Reality 可完成路径”；
- TASK_CONTRACT 增加连续性与 fallback 字段；
- Session Continuity Supervisor 回归升级为 15/15 PASS；
- 新增 `evidence/CONTINUITY-POLICY-REALITY-20261002-R3.json`。
