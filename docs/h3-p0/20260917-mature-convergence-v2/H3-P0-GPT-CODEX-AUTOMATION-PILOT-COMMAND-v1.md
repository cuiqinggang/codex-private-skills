# H3-P0 GPT-Codex 自动闭环 Shadow Pilot 命令 v1

状态：`READY_TO_EXECUTE / SHADOW_PILOT_ONLY / NO_H3_GPU`

## 1. 目标

实现并验收第一版：

```text
GPT planner
<-> AI Browser transport
<-> GitHub shared workspace
<-> Orchestrator
<-> Codex executor
```

本轮只证明：**用户不需要手工复制粘贴，toy task 可以从 GPT 规划到 Codex 执行再回 GPT 冻结。**

禁止在本轮自动执行 H3 GPU、ComfyUI、模型修改或视觉生成。

## 2. 读取技能

必须先读：

```text
skills/gpt-codex-convergence-orchestrator/SKILL.md
skills/gpt-codex-convergence-orchestrator/schemas/STATE.schema.json
skills/chatgpt-web-plan-bridge-latest/SKILL.md
skills/codex-capacity-aware-model-router/SKILL.md
skills/first-principles-physical-limit-convergence/SKILL.md
```

本机浏览器优先复用：

```text
C:\AI\Playwright-Native-AI-Browser
```

不得重新造一个新的浏览器自动化栈；必须调用已有成熟技能/脚本。

## 3. 正式安装目录

```text
C:\AI\GPT-Codex-Convergence-Orchestrator
```

至少实现：

```text
orchestrator.py
config.json
state\
adapters\github_workspace.py
adapters\codex_executor.py
adapters\chatgpt_browser.py
adapters\capacity_router.py
schemas\STATE.schema.json
scripts\start-shadow-pilot.ps1
scripts\stop.ps1
reports\INSTALL-REPORT.md
reports\SHADOW-PILOT-RESULT.md
```

不得修改代理、系统网络、健康 Playwright-Native-AI-Browser、H3/ComfyUI/Python/Torch/CUDA。

## 4. GitHub 工作区

本轮创建：

```text
workspaces/gpt-codex-shadow-pilot-v1/
  TASK.md
  STATE.json
  GPT-PLAN.md
  CODEX-COMMAND.md
  CODEX-RESULT.md
  CODEX-RESULT.json
  GPT-DECISION.md
  ARTIFACTS.md
  EVENTS.jsonl
```

所有状态变化必须 commit/push/remote verify。

## 5. Toy Task

固定 toy task：

```text
在本地工作目录创建一个 UTF-8 文本文件 toy-result.txt，内容必须完全等于：
GPT_CODEX_AUTOMATION_OK
然后读取回来并计算 SHA256，写入 CODEX-RESULT.json。
```

这是低风险、无外部副作用的确定性任务。

## 6. Shadow Pilot 流程

### Stage A — GPT planning

通过已有 AI Browser transport，向当前 ChatGPT 会话发送一次结构化请求：

```text
TASK_ID=gpt-codex-shadow-pilot-v1
请只返回一个机器可解析控制包，要求 Codex 完成固定 toy task。
```

浏览器必须保存：

- 发送文本；
- ChatGPT 回复文本；
- 页面完成证据；
- 发送/接收时间；
- conversation ref（可观测时）。

解析后写：

```text
GPT-PLAN.md
CODEX-COMMAND.md
STATE.status=READY_FOR_CODEX
```

### Stage B — Codex execution

Orchestrator 发现远端 `READY_FOR_CODEX` 后：

1. 调用 capacity router preflight；
2. 拉取远端命令；
3. 生成 ACTION_ID；
4. 如果 ACTION_ID 未执行，启动 Codex；
5. Codex 只执行 `CODEX-COMMAND.md`；
6. 写 RESULT + JSON；
7. commit/push/remote verify；
8. 更新 `STATE.status=READY_FOR_GPT`。

### Stage C — GPT judging

Orchestrator 检测 `READY_FOR_GPT` 后：

1. 通过 AI Browser 把 `CODEX-RESULT.md`、关键 JSON 和远端 HEAD 自动发送给 GPT；
2. 要求 GPT 只返回：

```text
CONTROL_ACTION=FREEZE
```

前提是 toy 文件内容与 SHA 验证全部通过；否则 GPT 返回 BLOCKED。

3. 自动抓取 GPT 回复；
4. 写 `GPT-DECISION.md`；
5. 更新 STATE 为 `FREEZE` 或 `BLOCKED`；
6. push + remote verify。

## 7. 幂等验收

必须做受控故障注入：

```text
T1 同一 READY_FOR_CODEX 被 watcher 读取两次 -> Codex只执行一次
T2 同一 READY_FOR_GPT 被读取两次 -> GPT只收到一次
T3 模拟 browser transport 中断 -> checkpoint 保留，不重跑 Codex
T4 模拟 capacity -> router fallback/checkpoint，不重跑 toy action
T5 orchestrator 重启 -> 从 STATE 恢复
T6 用户 stop 文件存在 -> 立即停止
T7 unknown status -> BLOCKED，不自由探索
```

不得用真实 H3 GPU 做这些 fault injection。

## 8. 成功条件

全部满足：

```text
MANUAL_COPY_PASTE_REQUIRED=NO
TOY_TASK_RESULT=PASS
GPT_TO_CODEX_TRANSPORT=PASS
CODEX_TO_GPT_TRANSPORT=PASS
GITHUB_REMOTE_TRUTH=PASS
IDEMPOTENCY=PASS
CHECKPOINT_RESUME=PASS
CAPACITY_ROUTER_INTEGRATION=PASS_OR_MOCK_PASS_WITH_SCOPE_LABELED
USER_STOP=PASS
NO_H3_GPU_RUN=YES
```

最终：

```text
AUTOMATION_SHADOW_PILOT=PASS
READY_FOR_ASSISTED_REAL_TASK_PILOT=YES
```

## 9. 失败规则

任何 login/captcha/account prompt：

```text
USER_APPROVAL_REQUIRED
STOP
```

浏览器 transport 故障：

```text
CONTROL_PLANE_FAILURE
CHECKPOINT
STOP
```

不得自行换浏览器技术路线。

## 10. 交付

生成本机：

```text
C:\AI\GPT-Codex-Convergence-Orchestrator\reports\INSTALL-REPORT.md
C:\AI\GPT-Codex-Convergence-Orchestrator\reports\SHADOW-PILOT-RESULT.md
C:\AI\GPT-Codex-Convergence-Orchestrator\reports\SHADOW-PILOT-STATE.json
```

同步项目摘要：

```text
docs/h3-p0/20260917-mature-convergence-v2/H3-P0-GPT-CODEX-AUTOMATION-PILOT-RESULT-v1.md
```

commit、push、remote verify 后 STOP RETURN TO GPT。
