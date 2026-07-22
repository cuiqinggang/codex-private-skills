# Web AI Basic Flow - Qwen / DeepSeek 2026-07-05

## Proven Result

The 2026-07-05 Qwen / DeepSeek copy matrix produced:

```text
Qwen no-sidebar simple copy: 10/10 PASS
Qwen no-sidebar superlong copy: 10/10 PASS
DeepSeek sidebar superlong copy: 10/10 PASS
DeepSeek no-sidebar superlong copy: 10/10 PASS
Total official counted rounds: 40/40 PASS
```

Evidence report:

```text
${REDACTED_SECRET}
```

## What This Proves

Under the tested stable conditions:

```text
Chrome visible and usable
Qwen / DeepSeek already logged in or otherwise usable
target page reachable
sidebar / no-sidebar state explicitly separated
new-chat or clean input state reachable
prompt pasted into the correct site
answer generated
copy button reachable
clipboard sentinel checked before copy
clipboard output checked after copy
```

the ordinary coordinate screenshot method can reliably:

```text
connect to the already-open usable page state
submit prompts
wait for answers
copy answers back to local clipboard
reject stale/wrong clipboard content
```

For these tested states, it is reasonable to say the answer-acquisition path is
engineering-level mature and may target 100% success.

## What This Does Not Prove Yet

Do not generalize the 40/40 result to:

```text
cold browser launch from no Chrome process
fresh navigation from blank tab
expired login
captcha
security/account prompts
network outage or slow DNS
service outage/rate limiting
browser profile mismatch
major UI redesign
different monitor/window/zoom state
file upload, payment, publish, permission, or destructive workflows
```

These are separate state branches. They should be detected, normalized, or
handed to the user, not silently counted as part of the 40/40.

## 100% Claim Boundary

Allowed claim:

```text
In the tested Qwen / DeepSeek visible states, the workflow achieved 40/40 PASS
for prompt submission, answer generation, answer copy, and local clipboard
verification.
```

Not allowed claim:

```text
All web connection conditions are universally 100% solved.
```

Better wording:

```text
网页已可用状态下，获取答案和复制回本地已经成熟；网页登录、冷启动、网络异常、验证码、服务异常属于连接前置门槛，需要单独小型预检。
```

## Recommended Additional Lightweight Tests

Do not rerun the full 40/40 just to validate connection. Add a small preflight
suite:

```text
Qwen connection preflight: 3/3
1. From an existing Qwen tab, refresh and confirm usable input state.
2. From a new tab, open https://www.qianwen.com/ and confirm usable input state.
3. Click new chat and submit one sentinel short prompt; verify copied answer.

DeepSeek connection preflight: 3/3
1. From an existing DeepSeek tab, refresh and confirm usable input state.
2. From a new tab, open https://chat.deepseek.com/ and confirm usable input state.
3. Click new chat and submit one sentinel short prompt; verify copied answer.
```

PASS criteria:

```text
correct domain visible
no login/captcha/security/network blocker
input box reachable
new-chat or clean prompt state reachable
short answer generated
copy result differs from sentinel and contains expected marker/answer
```

If any preflight fails:

```text
do not mark the answer-copy skill failed
classify the failure as connection/login/network/service/layout branch
record screenshot evidence
normalize the branch or ask the user
```

## Trigger Phrases

Use this reference when the user says:

```text
连接网页
获得答案
网页 AI 测试
Qwen 复制测试
DeepSeek 复制测试
普通人坐标截图法
网页能不能 100%
答案能不能 100%
```
