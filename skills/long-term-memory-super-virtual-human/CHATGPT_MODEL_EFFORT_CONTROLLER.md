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
MODEL_EFFORT_CONTROLLER=DESIGNED
DETERMINISTIC_UIA_PATH=REJECTED_AS_PRIMARY
PLAYWRIGHT_PATH=CANDIDATE_MATURE_BASE
E2E_CERTIFIED=NO
```
