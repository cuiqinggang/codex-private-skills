---
name: long-term-memory-super-virtual-human
version: "0.5.0"
description: 长期记忆超级虚拟人（Long-Term Memory Super Virtual Human）。以高智能主脑为核心，吸收成熟 Recovery/Long-Flow/Browser 机制，以长期记忆、权威任务合同、Checkpoint、按需工具路由、低相关冗余和独立强备份推进现实任务；唯一优化目标仍是 T*=min(T_VALID)。
---

# 长期记忆超级虚拟人 v0.5.0
# Long-Term Memory Super Virtual Human

```ini
VERSION=0.5.0
STATUS=VIRTUAL_MATURE_CONTINUITY_RUNTIME_ACTIVE
VIRTUAL_MATURE=YES
FINAL_VALID=NO

OBJECTIVE=T*=min(T_VALID)
PRIMARY_BRAIN_CANDIDATE=GPT
LONG_TERM_MEMORY=REQUIRED
LIGHT_ENTRY=YES
ON_DEMAND_TOOL_ROUTING=YES
TASK_CONTRACT_REQUIRED_FOR_LONG_FLOW=YES
CHECKPOINT_RECOVERY=REQUIRED
INDEPENDENT_STRONG_BACKUP=REQUIRED
CRITICAL_CAPABILITY_REDUNDANCY_REQUIRED=YES
MIN_MATURE_PATHS_FOR_CRITICAL_CAPABILITY=2

REASONIX_RECOVERY_KIT_ABSORPTION=R1
ECC_V3_1_1=REUSE
PLAYWRIGHT_NATIVE_AI_BROWSER=REUSE
CHATGPT_MODEL_EFFORT_CONTROLLER=FULL_E2E_REALITY_PASS_R14
CHATGPT_SESSION_CONTINUITY_CONTROLLER=V0_4_5_CLEAN_LIFECYCLE_TSTAR_R18_R19
PAID_TO_FREE_OPEN_SOURCE_REPLACEMENT=V1_0_0_REGISTERED
GOAL_LOOP_DEFAULT=YES
GOAL_LOOP_CONTROLLER=V0_5_0_ADAPTER_READY
GOAL_LOOP_REALITY=PASS_WINDOWS_PROCESS_FILES_AND_RUNTIME_INBOX
GOAL_LOOP_WINDOWS_DEPLOYMENT=PASS_UNIQUE_RUNTIME
GOAL_LOOP_BROWSER_FAULT_REALITY=BLOCKED_EXISTING_BROWSER_CDP
```

## 1. 产品定位

“长期记忆超级虚拟人”是用户的长期数字化认知与执行代理：在授权范围内持续记忆、观察、判断、调用现实能力、行动、验收、恢复和积累经验。

运行形态固定为：

```text
轻入口
→ 读取最小必要长期记忆 / TASK_CONTRACT
→ 查 Capability Registry
→ 发现成熟能力
→ 只激活本轮必要能力
→ Reality 执行与验证
→ 写回权威状态
→ FINAL_VALID
```

能力池可以很大，但当前工作集必须小。

## 2. 方法与成熟能力来源

本 Skill 调用但不复制以下独立成熟资产：

- 极限短时间智能体宪法 v0.3.1；
- 极限短时间自动化闭环 v2.0；
- GPT直连Windows双路执行桥 v0.3.0；
- Reasonix Recovery Kit；
- ECC v3.1.1；
- Playwright Native AI Browser；
- 本机 Mature AI Coding SuperTool Ecosystem Station；
- 收费转免费·开源替代技能包 v1.0.0（按需调用；免费/开源/自托管 + Agent 可操作优先）。

成熟能力吸收边界见 `MATURE_CAPABILITY_ABSORPTION_R1.md`。

## 3. 默认主脑

GPT 当前为首选主脑候选，但不是不可替代真理。

```ini
GPT_IS_UNREPLACEABLE=NO
```

简单任务优先主脑直达。只有加入工程执行器、长流程模块、生态工作站或并行层能让任务进入 VALID，或降低完整 T_VALID 时才升级执行档位。

## 4. 轻入口、强后端

```text
识别任务
→ 查 TOOL_INDEX / CAPABILITY_REGISTRY
→ 优先成熟方案
→ 只加载最小必要 Skill / Tool
→ 能原生直达则直达
→ 工程化再调用 Codex / Reasonix
→ 长流程复用 ECC
→ 多工具重工程按需唤醒成熟生态站
```

不因为安装了数百个 Skill 就全部加载，也不默认私有 Skill 一定优于当前外部成熟方案。

## 5. 长流程防漂移

长任务必须有单任务 Source of Truth：

```text
TASK_CONTRACT
= FINAL_REALITY_GOAL
+ SCOPE
+ HARD_BOUNDARIES
+ DONE_WHEN
+ EVIDENCE_REQUIRED
```

Checkpoint 只负责“恢复到哪里”，不替代任务合同。

长流程的 checkpoint/handoff、Gate/Repair、lease/fencing 优先复用 Reasonix/ECC 已有成熟能力，不重造第二套。

详见：
- `DRIFT_CONTROL.md`
- `DRIFT_BENCHMARK.md`
- `MATURE_CAPABILITY_ABSORPTION_R1.md`

## 6. 页面、记忆与连续性

聊天页面只是工作内存：

```text
长期记忆
+ 项目权威状态
+ TASK_CONTRACT
+ Checkpoint
+ 当前工作会话
```

页面迟缓、上下文过长、无响应或损坏时，不无限塞上下文；由外部连续性控制器探测并恢复。

v0.3.0 冻结恢复目标：
```ini
FRESH_RECOVERY_TARGET=TRUE_NEW_CHAT
BRANCH_IN_NEW_CHAT_ALLOWED_FOR_RECOVERY=NO
FULL_OLD_CONVERSATION_REPLAY=NO
MINIMAL_HANDOFF_REQUIRED=YES
```
“在新聊天中分支 / Branch”可能继承原会话树与上下文负担，因此不得作为故障恢复的“干净新页”；恢复必须进入真正的 New chat，再投递最小 handoff。

对复杂任务采用**高频预防换页 + 断连后保守判定**：在安全 checkpoint 上提前收敛上下文，以最小 handoff（任务合同 + 已确认结论 + 当前 checkpoint + 未决项 + 下一条指令）进入新会话。当前页越长、下一阶段越复杂、或本页已出现过一次瞬时断连/卡顿，越倾向在下一阶段开始前提前轮换；特别大的独立问题可以默认“一大问题一页”。

但“连接已断开/正在重新连接”不能单独证明后台任务已经停止。若断连发生在回答生成过程中，先只读探测并观察原任务是否仍产生后台进展或最终答案；只有任务专属恢复窗口或硬截止超过且仍无完成证据时，才 checkpoint + fencing + 新页 exactly-once 接续，避免重复执行。

详见 `CHATGPT_SESSION_CONTINUITY_CONTROLLER.md`。

## 7. 工具与执行器

工具是能力池，不默认平级常驻。按 `TOOL_INDEX.md` 路由，包括：
- Web / Browser；
- Desktop Commander Remote；
- GitHub Windows runner；
- Codex；
- Reasonix / DeepSeek；
- ECC；
- Playwright Native AI Browser；
- MCP / Plugin / API / CLI；
- Mature AI Coding SuperTool Ecosystem Station；
- 图像、视频和专项模型；
- OpenAI 托管云与按需外部云节点；
- 收费/订阅软件替换：调用 `../paid-to-free-open-source-replacement/SKILL.md`，先查成熟免费/开源路线，再过 DONE_WHEN Reality。

## 8. 模型与思考强度

当前 ChatGPT 页面没有官方“由当前回答中的 GPT 直接切换自身 UI 模型/Thinking 档”的程序化接口。

v0.2 采用双控制面：

```text
A. ChatGPT Page Mode
GPT/Router → MODEL_REQUEST → 外部 UI Controller
→ 切换 → 读回确认 → exactly-once continue

B. Programmable Agent Mode
Agents API / 外部执行器
→ 直接设置 model / reasoning.effort
```

Page Mode 优先复用 Playwright Native AI Browser，不重新造第二套 ChatGPT 浏览器通信。

详见：
- `MODEL_ROUTER.md`
- `CHATGPT_MODEL_EFFORT_CONTROLLER.md`

## 9. 现实权限边界

长期硬边界：
- 不破坏或删除 Windows 系统；
- 不修改 FlClash / Windows 网络代理；
- 支付、账号安全、不可逆高风险动作按现实权限门处理；
- 其他已授权普通操作尽量自动完成，不要求用户做人肉消息总线。

## 10. 韧性与低相关冗余

所有会阻塞 FINAL_VALID 的关键能力默认要求至少两条成熟路径，并尽量分离控制面、认证、传输、运行身份、执行引擎、供应商和存储位置。

主路优化完整 T_VALID；备路允许更慢，但必须能达到同一个 FINAL_VALID。

主路异常：
```text
先判断主路是否仍可能完成并验收
→ 若只是短暂传输异常且后台仍在推进，继续观察
→ 若主路已经阻塞、受限或长期无法验收，则切换下一条成熟可完成路径
→ 先完成现实结果
→ 再修复或优化原主路
→ 重新补齐至少双路冗余
```

`T*=min(T_VALID)` 只在真正能完成并验收的有效候选中比较速度。更快但本轮过不去的路线不属于有效候选；更慢但能够最终完成的成熟备路优先于无限等待。

详见 `RESILIENCE_REDUNDANCY.md`。

## 11. 按需执行档位

- P0 Direct Fast Path
- P1 Engineering Executor
- P2 Long-Flow ECC
- P3 Mature AI Coding SuperTool Ecosystem Station
- P4 Independent Continuity
- P5 Cloud / Network Execution Substrate

详见 `EXECUTION_PROFILES.md` 与 `CLOUD_RUNTIME_OPTIONS.md`。

## 12. GPT 故障恢复

GPT 会话故障与 GPT 服务故障分开处理：

```text
页面/会话坏
→ Playwright query/recovery
→ checkpoint/handoff
→ 新 ChatGPT 会话 exactly-once 继续

GPT 服务不可用
→ 外部 watchdog 判定
→ fencing primary writer
→ Reasonix / DeepSeek 独立备脑
→ 读取同一 TASK_CONTRACT + Checkpoint
→ 继续 FINAL_VALID
```

详见：
- `CHATGPT_SESSION_CONTINUITY_CONTROLLER.md`
- `BRAIN_FAILOVER_CONTRACT.md`

## 13. v1.0 毕业门槛

v1.0 按**能力结果**验收，不把某一个实现工具写成唯一毕业条件。指定主路失败时，只要成熟备路能达到同一个现实结果并留下证据，就可以判定该能力 PASS；失败的主路另行修复和优化。

以下能力未全部通过前不签 v1.0：

1. **Windows 连续执行能力**：登录态变化/主控制面异常后，至少一条已授权 Windows 路径可恢复任务并继续；DCR 是主路，GitHub runner/其他成熟执行面可作为适用场景的备路；
2. **推理档位适配能力**：能根据阶段需要获得合适计算强度；ChatGPT UI 自动切档是主路之一，但 CAPTCHA/UI 阻塞时允许保持当前档继续，或转 Programmable Agent / Reasonix 等成熟路径，不因“切档动作本身”阻塞最终任务；
3. **会话连续性能力**：断连后若后台仍在完成则等待原结果；确认停滞后可以 checkpoint/handoff 到新会话或备脑，并 exactly-once 继续；
4. **独立备脑能力**：GPT 服务不可用时至少一条独立模型路径可读取同一任务合同并继续到 DONE_WHEN；
5. **防脑裂能力**：lease/fencing 能确保只有当前 writer 更新权威状态；
6. **状态恢复能力**：至少一个远端状态源 + 一个独立本地/离线副本能够真实恢复项目状态；
7. **真实任务有效性**：至少一组真实有价值任务达到 FINAL_VALID，并证明成熟能力吸收没有制造阻塞性无效层级。

原则：实现路径可以降级，DONE_WHEN 不能降级。

## 14. v0.5.0 默认运行合同

当用户明确说以下任一含义时：

```text
按“长期记忆超级虚拟人”运行当前任务
使用“长期记忆超级虚拟人”技能包完成
当前页面属于“长期记忆超级虚拟人”任务
```

即自动启用以下页面运行规则，不等待用户再次提醒：

```ini
LTMVH_RUNTIME_ACTIVE=YES
CONTINUITY_MONITORING=REQUIRED
EARLY_ROTATION_FOR_LONG_TASKS=YES
CHECKPOINT_BEFORE_ROTATION=YES
RECOVERY_TARGET=TRUE_NEW_CHAT
BRANCH_RECOVERY=FORBIDDEN
REUSE_EXISTING_CHATGPT_BROWSER=REQUIRED
SECOND_BROWSER_LAUNCH_WHEN_EXISTING=FORBIDDEN
AUTO_BROWSER_LAUNCH_MAX_PER_WINDOWS_BOOT=1
CONTINUITY_RUNTIME_BROWSER_LAUNCH=FORBIDDEN
CONTINUITY_RUNTIME_AUTO_NEW_PAGE=FORBIDDEN
CONTROL_LOSS_BEHAVIOR=FAIL_CLOSED_KEEP_EXISTING_BROWSER
EXACTLY_ONCE_CONTINUATION=REQUIRED
KEEP_BROWSER_PROCESS_OPEN=YES
IDLE_CHAT_PAGE_TARGET=1
IDLE_CHAT_PAGE_KIND=BLANK_NEW_CHAT_ROOT
CLOSE_FINISHED_EXECUTOR_PAGE=YES
CLOSE_FINISHED_CEO_PAGE_AFTER_PERSIST=YES
```

运行语义：
- 页面较长、下一阶段复杂、已出现卡顿/断连历史时，在安全 checkpoint **提前换会话**，不等页面彻底坏掉；
- 出现“连接已断开/正在重新连接”时先判断后台是否仍在推进，不立刻重复任务；
- 活跃回答超过 silence window 后先只读 probe；若仍处于生成中且无进展，则自动停止旧 turn，写入 `CONFIRMED_STALL_ABORTED` Checkpoint，再以最小 handoff 进入真正 New chat，禁止 Branch；
- 已有 `shared-mcp` 登录浏览器时必须复用；控制接口异常也不得因此启动第二个浏览器；
- 普通任务完成、主路失败、切备脑均不得关闭持久 GPT 浏览器；
- 页面只是工作内存，权威事实必须持续写回技能包/项目状态/Checkpoint。

该合同在技能包被明确调用后，对当前任务生命周期持续有效，直到任务 FINAL_VALID、用户明确 STOP，或用户明确退出该技能运行模式。


### v0.4.5 页面生命周期统一规则

同页“压缩/总结”只用于形成可接续状态，不视为真正释放上下文。页面生命周期只由一套连续性控制链管理：

```ini
SINGLE_PRODUCTION_CONTINUITY_PATH=YES
LEGACY_PARALLEL_SUPERVISOR=NO
WAIT_UNTIL_SLOW=NO
TRUE_NEW_CHAT_ONLY=YES
BRANCH_RECOVERY=FORBIDDEN

CEO_VISIBLE_TEXT_LIMIT_DEFAULT=40000
CEO_USER_TURN_LIMIT_DEFAULT=10
EXECUTOR_VISIBLE_TEXT_LIMIT_DEFAULT=30000
EXECUTOR_USER_TURN_LIMIT_DEFAULT=3
```

统一触发器：
- **增长触发**：可见文本量或轮数达到角色阈值，在安全 checkpoint 主动进入真正 New chat；
- **阶段触发**：超大独立阶段结束后可立即轮换，不等待阈值；
- **历史触发**：本页发生过断连/卡顿后，在下一个安全 checkpoint 提前轮换；
- **UI/页面异常**：composer、页面状态、发送/加载异常，经只读 probe 确认后轮换；
- **活跃 turn 卡死**：静默窗口超过且无后台进展时，先 probe，确认后停止旧 turn，再 checkpoint + true New chat；
- **断连但后台仍推进**：继续等待原结果，避免重复执行；
- **真人验证**：暂停自动化，不尝试绕过；
- **服务级不可用**：按备脑/备路合同切换，不把页面轮换误当成服务恢复。

旧页面连续性/恢复方案全部保留为历史资产，不再并行运行；索引见 `LEGACY_CONTINUITY_INDEX.md`。


### v0.4.5 专用浏览器 CEO 干净生命周期冻结合同

Reality R18 / R19 已证明专用浏览器可以在**单空白页干净基线**下完成完整 CEO 控制链，并在任务结束后恢复到单空白页。生产默认按以下最小路径运行：

```text
1 个空白 ChatGPT New chat 页
→ 复用为 CEO-1
→ CEO-1 只负责理解 / 拆分 / DONE_WHEN
→ 仅按需创建最少执行页
→ 写入最小 checkpoint
→ 关闭旧 CEO
→ 真正 New chat 创建 CEO-2
→ CEO-2 基于 checkpoint 接管，禁止重做已派任务
→ 收回原执行结果并验收
→ 已完成执行页立即关闭
→ FINAL_VALID 与证据持久化
→ 关闭最终 CEO
→ 恢复恰好 1 个空白 ChatGPT New chat 页
```

冻结规则：

```ini
CLEAN_BROWSER_BASELINE_REQUIRED=YES
IDLE_CHAT_PAGE_TARGET=1
IDLE_CHAT_PAGE_KIND=BLANK_NEW_CHAT_ROOT
REUSE_BASELINE_AS_CEO1=YES
EXECUTOR_PAGE_COUNT=MIN_REQUIRED_ONLY
PREWARM_UNUSED_CHAT_PAGES=NO
CLOSE_EXECUTOR_AFTER_RESULT_PERSISTED=YES
CLOSE_OLD_CEO_AFTER_CHECKPOINT=YES
CEO_REPLACEMENT_SESSION=TRUE_NEW_CHAT_ONLY
BRANCH_RECOVERY=FORBIDDEN
FULL_CONVERSATION_REPLAY=NO
MINIMAL_CHECKPOINT=REQUIRED
FINAL_BROWSER_STATE=ONE_BLANK_NEW_CHAT_PAGE
```

当前 Reality 极限短时间记录：

```ini
CEO_CLEAN_LIFECYCLE_REALITY=PASS_R18_R19
T_VALID_R18_MS=51454
T_VALID_R19_MS=54246
T_STAR_OBSERVED_MS=51454
T_STAR_SOURCE=R18
CHECKPOINT_CHARS_R18=125
```

`T_STAR_OBSERVED_MS=51454` 表示在当前设备、当前 ChatGPT 服务状态和本冻结合同下**已观测到的最小有效值**，不是不可突破的数学下界；后续只有新的 Reality 在不降低 VALID 合同的前提下更快，才允许替换当前 T*。

已实测但不采用为默认路径的候选包括：执行页提前预热、Instant 控制链、CEO 同物理 tab 复用、删除独立接管确认回合。它们在本轮 Reality 中没有降低完整 T_VALID，部分显著变慢；不得仅凭“理论上步骤更少”替换当前冻结路径。

## 15. 当前入口

用户只给现实目标。

运行时：

```text
参考极限短时间自动化闭环 v2.0；
先查成熟方案；
按需加载；
长流程复用 ECC；
ChatGPT 页面控制复用 Playwright Native AI Browser；
关键能力保留低相关双路；
记录 FLOW_START → FINAL_VALID 的完整 T_VALID。
```

## 16. v0.5.0 目标循环默认执行合同

收到授权任务后，自动循环判断、执行或调度、真实验证、定向返修与保存状态，不等待用户每轮说“继续”。GPT可以直接执行，也可以调度成熟执行器。只有 DONE_WHEN + EVIDENCE_REQUIRED 真正通过才完成；普通错误先尝试授权内可行的新策略。无授权可完成路线、需要用户决定、预算达到、无进展或用户 STOP 时明确停止并报告。

先读取 `GOAL_LOOP_CONTROLLER.md`。任务合同、状态、日志分离；动作前保存稳定编号，中断后先核对原结果，禁止重复副作用。保持现有唯一连续性 runtime/global writer；不新建并行 supervisor 或浏览器。

本版已部署到用户 Windows 唯一连续性 runtime。2026-10-04 实测：循环控制器 12/12、连续性 25/25、租约 6/6、真实进程/文件场景 4/4、实际 runtime inbox 场景 5/5 PASS。已证明自动返修、原动作核对续接、同次投递自动恢复、终态去重、阻塞与 STOP；证据见 `evidence/V050-WINDOWS-GOAL-LOOP-REALITY-20261004-R1.json`。专用浏览器仍存在但 CDP 9223 不可达，新循环中的真实 GPT/网页故障端到端尚未通过；禁止借另启浏览器绕过。本版功能与受控 Windows 实测已通过，不等于全部生产能力通过；项目级 FINAL_VALID=NO 不变。
