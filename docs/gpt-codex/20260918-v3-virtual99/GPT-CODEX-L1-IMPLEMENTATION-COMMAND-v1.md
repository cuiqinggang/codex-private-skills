# GPT↔Codex L1 实施命令 v3-Virtual99

状态：AUTHORIZED_IMPLEMENTATION / NO_FREE_EXPLORATION

Codex 必须先读取：

~~~
docs/gpt-codex/20260918-v3-virtual99/GPT-CODEX-V3-MATURE-CLUSTER-VIRTUAL-99-v1.md
skills/gpt-codex-convergence-orchestrator/SKILL.md
skills/gpt-codex-convergence-orchestrator/ACCEPTANCE.md
skills/gpt-codex-convergence-orchestrator/references/CODEX-FIRST-NUMBERED-BUS-v1.md
skills/codex-capacity-aware-model-router/SKILL.md
skills/chatgpt-web-plan-bridge-latest/SKILL.md
~~~

## 1. 权限

~~~
CODEX_PLAN_AUTHORITY=NONE
NO_FREE_EXPLORATION=YES
BOUNDED_EXECUTION_FLEXIBILITY=YES
~~~

不得自行新增候选架构、替换成熟 primitive、改协议目标或扩大任务。

## 2. 安全边界

禁止：
- 改代理/网络；
- 改系统全局设置；
- force push；
- H3 GPU；
- 删除用户资料；
- 新建另一套 browser stack；
- 访问未授权 secret；
- 把 mock PASS 写成 real PASS。

所有修改先备份并回读验证。

## 3. 实施

在：

C:\AI\GPT-Codex-Convergence-Orchestrator

实现 Frozen Virtual-99 runtime：

~~~
orchestrator.py
config.json
protocol.py
storage.py
reconcile.py
adapters\github_bus.py
adapters\chatgpt_wakeup.py
adapters\codex_executor.py
adapters\capacity_router.py
tests\fault_injection.py
state\
logs\
reports\
~~~

优先 Python stdlib + sqlite3 + native git + 已有 Browser/Capacity Router。

## 4. 先做本地确定性验证

真正唤醒 GPT 前，必须真实通过：

~~~
R1 atomic message staging
R2 non-force conflict handling
R3 logical_event dedupe
R4 crash-after-effect reconciliation
R5 DONE-before-publish recovery
R6 published-before-local-ack recovery
R7 lease loss/stale runner denial
R8 version/contract mismatch BLOCKED
R9 snapshot rebuild
R10 capacity failover state preservation
N1-N5 no-free-exploration
~~~

R10 在本阶段允许 controlled mock fault injection，但必须明确标注 REAL_SERVICE_FAILOVER=UNVERIFIED，不得冒充真实服务 failover。

## 5. True L1

本地 fault injection 全通过后，创建专用 runtime bus branch：

~~~
bus/gpt-codex-shadow-pilot-v3
~~~

TASK：

~~~
TASK_ID=gpt-codex-shadow-pilot-v3
OUTPUT=toy-result.txt
CONTENT=GPT_CODEX_CODE_TO_CODE_OK
VERIFY=READBACK+SHA256
NO_H3_GPU=YES
~~~

真实运行：

~~~
000001 CODEX->GPT REQUEST
-> Browser wake current GPT conversation
-> wait for GPT direct GitHub 000002
-> execute only 000002
-> 000003 CODEX->GPT RESULT
-> Browser wake GPT
-> wait for GPT direct GitHub 000004
-> FREEZE/BLOCKED
~~~

Browser wake 只允许携带：

~~~
TASK_ID
REQUEST_OR_RESULT_SEQ
REPOSITORY
BUS_BRANCH
REQUEST_FILE
~~~

不得携带完整业务命令正文。

## 6. 证据

本机：

~~~
reports\GPT-CODEX-L1-SHADOW-PILOT-v3.md
reports\GPT-CODEX-L1-SHADOW-PILOT-v3.json
~~~

GitHub：

~~~
docs/gpt-codex/20260918-v3-virtual99/GPT-CODEX-L1-RESULT-v1.md
docs/gpt-codex/20260918-v3-virtual99/GPT-CODEX-L1-RESULT-v1.json
~~~

逐项列 A1-A15、N1-N5、R1-R10 的 PASS/FAIL/EVIDENCE。

## 7. Maturity

只有全部真实 L1 项通过才允许：

~~~
AUTOMATION_MATURITY=L1_SHADOW_PILOT_PASS
READY_FOR_ASSISTED_REAL_TASK_PILOT=YES
~~~

否则保持：

~~~
AUTOMATION_MATURITY=L0_SPEC_READY
~~~

完成或 BLOCKED 后 STOP RETURN_TO_GPT。
