# CHANGELOG

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
