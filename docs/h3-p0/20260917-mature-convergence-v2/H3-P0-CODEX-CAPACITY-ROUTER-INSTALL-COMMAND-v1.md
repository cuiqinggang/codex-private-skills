# H3-P0 Codex 容量感知动态模型选择器安装命令 v1

状态：`READY_TO_EXECUTE / NO_H3_GPU_REPLAY`

## 目标

在本机为 Codex 长任务部署一个独立容量路由器：

```text
主模型 capacity
→ 动态刷新模型列表
→ 极小 probe
→ 自动选下一个可用模型
→ 保留 checkpoint
→ 继续同一个逻辑任务
```

## 安装边界

不得：

- 修改代理/网络；
- 修改 H3/ComfyUI/Python/Torch/CUDA/模型；
- 重跑已经完成的 GPU/QC；
- 修改当前 H3 业务命令包；
- 写死长期静态模型名单；
- 无限快速重试 capacity 模型。

## 源 Skill

从当前项目分支读取：

```text
skills/codex-capacity-aware-model-router/SKILL.md
```

安装到本机正式 Skills 根下，先备份同名旧目录（若存在），再回读确认。

## 本机实现要求

建议正式目录：

```text
C:\AI\Codex-Capacity-Router
```

至少生成：

```text
router.py
router-policy.json
README.md
state\router-state.json
state\model-health.json
state\checkpoint.json
logs\route-events.jsonl
```

### router-policy.json

不得永久写死当前模型集合。

只保存策略，例如：

```json
{
  "model_source": "codex_live_then_models_cache",
  "model_cache_ttl_seconds": 300,
  "capacity_cooldown_seconds": 600,
  "all_models_recheck_seconds": 300,
  "probe_reasoning_effort": "low",
  "preferred_models": [],
  "denied_models": [],
  "quota_sensitive": true
}
```

`preferred_models=[]` 表示运行时按当前模型目录/任务策略生成顺序，而不是没有候选。

## 模型发现

优先通过当前 Codex app-server/model list 获取；不可用时读取当前 Codex Home 的 `models_cache.json`。

必须记录：

```text
MODEL_DISCOVERY_SOURCE
MODEL_DISCOVERY_TIMESTAMP
MODEL_CANDIDATE_COUNT
```

如果模型列表不可观测：不得猜，标记 `UNKNOWN` 并安全停止。

## Probe

每个候选最多做一次极小只读 probe：

```text
Reply with exactly: ROUTER_OK
```

使用同一账号/auth、read-only/ephemeral、最低可用 reasoning effort。

结果分类：

```text
PASS
CAPACITY
RATE_LIMIT
AUTH_ERROR
NETWORK_ERROR
OTHER_ERROR
```

只有 `CAPACITY/server_overloaded` 自动尝试下一个候选。

## 路由状态

每次必须输出并保存：

```text
REQUESTED_MODEL
ACTUAL_MODEL
FALLBACK_REASON
ERROR_CLASS
PROBE_RESULT
TASK_ID
THREAD_ID
CHECKPOINT_PATH
```

## 恢复

capacity 发生在进行中的 Codex 长任务时：

1. 读取/写入当前 checkpoint；
2. 不杀死已经启动且健康的本地 H3/GPU 任务；
3. 优先使用 Codex thread resume；
4. 若 resume 无法同时完成模型切换，则创建 continuation thread 并注入 handoff；
5. continuation 必须包含 `COMPLETED_STEPS` 与 `DO_NOT_REPEAT`。

## 全模型 capacity

一次路由周期中全部候选均 capacity：

```text
ROUTER_STATE=ALL_MODELS_CAPACITY
TASK_STATE=CHECKPOINTED
LOCAL_WORK_REPLAY=NO
```

等待下一健康检查周期；禁止忙循环。

## 验收

不需要真实触发服务拥塞，可用受控 mock/fault-injection 验收路由逻辑。

必须完成：

```text
T1 主模型PASS -> PRIMARY_SELECTED
T2 主模型CAPACITY + 第二模型PASS -> FALLBACK_SELECTED
T3 前两模型CAPACITY + 第三模型PASS -> THIRD_SELECTED
T4 全候选CAPACITY -> CHECKPOINTED, no busy loop
T5 capacity 后 resume -> 已完成本地步骤不重跑
T6 route-events 含 REQUESTED_MODEL/ACTUAL_MODEL/FALLBACK_REASON
T7 模型目录增加新模型 -> 无代码修改即可发现
```

## 最终产物

生成：

```text
C:\AI\Codex-Capacity-Router\reports\INSTALL-REPORT.md
C:\AI\Codex-Capacity-Router\reports\ACCEPTANCE.json
```

并把安装报告/关键配置摘要同步回：

```text
docs/h3-p0/20260917-mature-convergence-v2/
```

最终如果全部 PASS：

```text
CODEX_CAPACITY_ROUTER=ENABLED
STATIC_MODEL_LIST=NO
CAPACITY_FAILOVER=PASS
CHECKPOINT_RESUME=PASS
LOCAL_WORK_REPLAY=NO
```

然后停止返回 GPT。