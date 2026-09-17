# Codex Capacity-Aware Model Router

版本：`1.0.0`

中文：**Codex 容量感知动态模型选择器**

## 目标

解决 Codex 长任务中的：

```text
Selected model is at capacity. Please try a different model.
```

核心原则：

```text
模型容量错误 != 本地任务失败
模型切换 != 重跑已经完成的本地工作
动态发现当前可用模型，不写死模型名单
```

本选择器独立于具体项目运行；H3、Playwright、Reasonix、ARO 等任务均可复用。

## 1. 模型来源

优先读取 Codex 当前模型目录 / model list；不可用时读取 Codex Home 的 `models_cache.json`。

Codex 上游 ModelsManager 使用 `models_cache.json`，默认刷新 TTL 为 300 秒。因此本选择器不得长期保存静态模型列表。

每次路由：

1. 刷新/读取当前模型列表；
2. 读取任务的 `REQUESTED_MODEL`；
3. 依据当前 policy 生成候选模型序列；
4. 用极小只读 probe 验证候选当前是否可接受请求；
5. 选择第一个 probe PASS 的候选。

## 2. 候选排序

不在 Skill 中永久写死某几个模型名。

候选排序由运行时模型列表 + policy 决定：

```text
1. REQUESTED_MODEL
2. 同能力等级的可用模型
3. policy 允许的其他 Codex 模型
```

policy 可包含：

- `preferred_models`：用户当前偏好，可动态更新；
- `denied_models`：明确禁止模型；
- `min_capability_class`：当前任务最低能力等级；
- `quota_sensitive`：是否优先低额度消耗；
- `reasoning_effort`：探针默认 low，正式任务继承任务要求。

模型名单变化时只刷新 selector，不修改业务任务。

## 3. 容量探针

probe 必须：

- 与正式任务使用同一账号/auth；
- 独立、极小、只读；
- 不访问项目业务文件；
- reasoning effort 使用最低可用值；
- 只要求返回固定 ACK；
- 记录原始错误分类。

示意：

```text
Reply with exactly: ROUTER_OK
```

探针结果：

```text
PASS
CAPACITY
RATE_LIMIT
AUTH_ERROR
NETWORK_ERROR
OTHER_ERROR
```

只有 `CAPACITY/server_overloaded` 才自动尝试下一个模型。

## 4. 容量错误处理

收到：

```text
Selected model is at capacity
server_overloaded
```

执行：

```text
保存任务 checkpoint
标记当前模型 CAPACITY
记录 cooldown
选择下一候选模型
继续同一个逻辑任务
```

禁止：

- 因模型容量错误重跑已经完成的 GPU / benchmark / 文件修改；
- 删除当前证据；
- 把 capacity 错误判为业务 FAIL；
- 无限快速重试同一个模型。

## 5. 全模型容量不足

近期 Codex 容量错误可能是账号级/服务级，多个模型可能同时 `server_overloaded`。

如果本轮所有候选均 CAPACITY：

```text
ROUTER_STATE=ALL_MODELS_CAPACITY
TASK_STATE=CHECKPOINTED
LOCAL_WORK_REPLAY=NO
```

默认下一次健康探测间隔：300 秒。

不得忙循环。连续远端不可用超过项目规定时间盒时：

```text
BLOCKED_REMOTE_CAPACITY
```

保留 checkpoint，等待下一次恢复入口。

## 6. 长任务续接

优先使用 Codex 原生 thread resume 保留上下文。

如果当前客户端不能在 resume 时完成模型切换，则建立 continuation thread，并自动注入最小 handoff：

```text
TASK_ID
WORKDIR
BRANCH
LAST_REMOTE_HEAD
COMPLETED_STEPS
DO_NOT_REPEAT
CURRENT_BLOCKER
NEXT_ACTION
ARTIFACT_PATHS
REQUESTED_MODEL
PREVIOUS_ACTUAL_MODEL
NEW_ACTUAL_MODEL
FALLBACK_REASON
```

重点：模型切换只改变“谁继续推理”，不改变已经冻结的业务命令包。

## 7. 状态与审计

固定状态目录建议：

```text
.codex-router/
  router-state.json
  model-health.json
  checkpoint.json
  route-events.jsonl
```

每次路由必须记录：

```text
REQUESTED_MODEL
ACTUAL_MODEL
FALLBACK_REASON
ERROR_CLASS
PROBE_RESULT
TIMESTAMP
THREAD_ID / CONTINUATION_THREAD_ID
TASK_CHECKPOINT
```

模型实际不可观测时写 `UNKNOWN`，禁止猜测。

## 8. 与本地长流程控制器协作

模型路由器只负责“远端推理模型可用性”。

本地执行必须继续由 resumable controller / checkpoint 保护：

```text
模型容量中断
!=
停止本地已经启动的 GPU / ComfyUI / benchmark
```

恢复时先检查本地真实状态，再决定是否继续下一步骤；禁止由于聊天/模型错误重复提交已有工作。

## 9. 验收

至少验证：

```text
A. 主模型 probe PASS -> 使用主模型
B. 主模型模拟 CAPACITY -> 自动选择下一个可用模型
C. 两个模型 CAPACITY -> 第三个 PASS，任务状态不丢失
D. 全部模型 CAPACITY -> CHECKPOINTED/BLOCKED，不忙循环
E. capacity 后恢复 -> 不重复已完成本地步骤
F. route-events 含 REQUESTED_MODEL / ACTUAL_MODEL / FALLBACK_REASON
G. 模型目录刷新后无需改代码即可识别新模型
```

## 10. 固定结论

```text
CAPACITY_AWARE_ROUTING=YES
STATIC_MODEL_LIST=NO
CAPACITY_ERROR_IS_BUSINESS_FAILURE=NO
LOCAL_WORK_REPLAY_ON_MODEL_SWITCH=NO
AUDITABLE_MODEL_ROUTE=YES
```