# ChatGPT Model / Effort Controller v0.1

## 目标

把用户当前手工完成的：

```text
判断任务难度
→ 打开 ChatGPT 模型/Thinking 控件
→ 选择合适模型/强度
→ 继续任务
```

变成外部自动控制，同时保持低成本。

## 关键边界

当前 ChatGPT 页面没有官方“让当前回答中的 GPT 自己切换自身 UI 档位”的程序化接口。

因此控制器必须位于主脑之外。

## 架构

```text
GPT / Task Router
→ MODEL_REQUEST.json
→ Deterministic Controller
→ ChatGPT UI
→ 读回实际 model / effort
→ MODEL_ACK.json
→ 继续下一阶段
```

### 决策层
由当前主脑或便宜分类器只输出：
- desired_model_class
- desired_effort
- reason
- task_id
- expiry
- fallback

### 执行层优先级

1. **Playwright Native AI Browser**
   - 使用既有 headed persistent profile
   - DOM/Accessibility 定位模型选择器与 Thinking 控件
   - 设置后读回确认
2. Computer Use / 视觉智能体
   - 仅 DOM 失效或 UI 改版时启用
3. 人工
   - 仅账号验证、产品强制交互或两条自动路线都失效

Windows UI Automation 只暴露 ChatGPT Chromium 外壳和标题栏，本轮只读探测没有暴露网页内部控件，因此不作为主路径。

## 成本规则

不要让一个强模型每次负责“点两下”。

```text
主脑决定目标档位
→ 确定性脚本执行
→ 只有定位失败时调用低成本视觉/Browser Agent
```

## 路由建议

默认不频繁切换。一个阶段内保持会话黏性。

典型：
- 普通事务：Instant / Medium
- 复杂分析、较高返工风险：High
- 极少数最高复杂任务：Extra High / Pro
- 高档额度不足：回退 Medium/High + ECC/Gate/Repair，而不是持续烧最高档

最终阈值必须由真实 T_VALID 与额度消耗共同观测后调整；额度/成本只决定候选可用性，不替代 T_VALID。

## 自动继续

UI 切换本身不会自动产生下一轮用户消息。

因此全自动模式还需要 Sidecar Supervisor：
1. 写 checkpoint
2. 完成 model/effort 切换
3. 确认 ACK
4. 通过已验证 ChatGPT 浏览器入口发送一条唯一 marker 的 CONTINUE 消息
5. exactly-once query 防止重复发送

这必须复用 Playwright Native AI Browser 的 formal business entrypoint；不得另造第二套 ChatGPT send/query/wait_extract。

## 完成门禁

```text
SET_REQUESTED
→ UI_CHANGED
→ READBACK_MATCH
→ CONTINUE_ONCE
→ NEXT_TURN_REPORTS_EXPECTED_SETTING
```

至少测试：
- Medium → High
- High → Medium
- 不存在/额度耗尽档位的 fail-closed
- UI 改版 DOM 失败后的视觉 fallback
- 断线后 exactly-once 继续

当前：
```ini
MODEL_EFFORT_CONTROLLER=FULL_E2E_REALITY_PASS_R14
DETERMINISTIC_UIA_PATH=REJECTED_AS_PRIMARY
PLAYWRIGHT_PATH=MATURE_BASE_REUSED
E2E_CERTIFIED=YES
```

## Model/Effort Reality 2026-10-02 / 01
- Result: NOT_E2E_CERTIFIED; VERSION remains 0.2.0; no v1.0 signature.
- Formal entry source verified at canonical skill scripts/chatgpt-business-entry.js; query/send/wait_extract NOT RUN.
- Original setting: Medium, observed on authenticated shared-mcp page with composer.
- No-send: draft matched, whitespace-only empty composer verified, user turns 0 -> 0, blank handoff observed.
- Blocker: EXCLUSIVE_CONTROL_NOT_PROVEN. Without this run navigating, the current page changed to about:blank; actor unknown. Multiple same-config MCP servers exist, but only one Chromium root was observed holding shared-mcp. Do not equate idle server count with active browser ownership.
- Switch 1 High / Switch 2 Medium / exactly-once continuation / nonexistent-target test / restoration readback: NOT RUN.
- submissionCount=0; duplicate sends=0; no model/effort change performed.
- Candidate controller: runtime/chatgpt-model-effort-controller.js. It only reads/sets/reads back. Medium is observed; High remains UNAVAILABLE until its target is discovered on the real UI. No inference of High from a slider position is certified.
- Wrong-origin test returned FAIL / WRONG_ORIGIN with zero UI_CHANGED transitions.
- Evidence: evidence/MODEL-EFFORT-REALITY-20261002-01.json.
- Resume: establish exclusive control of the existing formal STDIO owner without launching another owner; discover High semantically; read original; execute both switches and exactly-once query -> send -> wait_extract; read back and restore; run nonexistent-target no-change test. Only all PASS authorizes v0.2.1 / E2E_CERTIFIED.
- T_VALID=NOT_PRODUCED.

## Model/Effort Reality 2026-10-02 / 02
- Exclusive `shared-mcp` persistent-profile control: PASS after pausing only the Playwright MCP child processes; Codex main process remained running.
- Authenticated ChatGPT page: PASS; composer present; model control semantically located as `选择 ChatGPT 模型`.
- Medium → High: PASS. Readback: `High，第 3 项，共 4 项。` with `SET_REQUESTED → UI_CHANGED → READBACK_MATCH`.
- Formal exactly-once business entrypoint was reused unchanged. Query-before returned userCount=0.
- Send step: FAIL because the user turn was not DOM-confirmed within 10 seconds; duplicate sends observed=0.
- Repeated automated relaunches then entered a Cloudflare challenge, so final Medium restoration readback could not be certified in this run.
- The E2E harness was repaired so future failures attempt restoration in `finally` before closing the context.
- Overall: switch/readback capability is Reality-proven;该次 full `CONTINUE_ONCE → answer → restore` 仍 OPEN。Evidence: `evidence/REALITY-CLOSURE-20261002-R2.json`.

## Model/Effort Reality 2026-10-03 / R14
- Existing shared-mcp browser reuse: PASS；`newBrowserLaunched=false`，通过 `connectOverCDP` 连接现有浏览器。
- 当前中文 UI 原档为 `高`，规范化为 `High`；成功切到 `中/Medium`，语义读回 PASS。
- Continuation 只提交一次；页面确认 `userCount=1`，收到 `LTMVH-MODEL-EFFORT-E2E-20261003-R14-ACK`；exactly-once PASS。
- 非法目标 `Impossible`：fail-closed，`changed=false`。
- finally 恢复原档：`中/Medium → 高/High`，读回 PASS。
- 当前 ChatGPT DOM 已不稳定暴露旧 `data-message-author-role`；R14 verifier 使用可见“你说/You said”语义兜底，不把 DOM 适配失败冒充业务失败。
- Evidence: `evidence/MODEL-EFFORT-FULL-E2E-REALITY-20261003-R14.json`。
- Result: `MODEL_EFFORT_FULL_E2E=PASS_R14`；该门已闭合，但项目 `FINAL_VALID=NO` 不变。
