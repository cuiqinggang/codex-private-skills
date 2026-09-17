# Codex 容量感知动态模型选择器

正式本机目录：`C:\AI\Codex-Capacity-Router`；Skill 安装目录：当前 `CODEX_HOME\skills\codex-capacity-aware-model-router`。

`router.py` 每次先请求当前 Codex app-server 的 `model/list`，不可用时读取当前 `CODEX_HOME\models_cache.json`。策略文件只保存排序与冷却规则，不保存静态模型集合。探针使用同一 Codex CLI 账号、`--ephemeral --sandbox read-only`、中性工作目录、该模型支持的最低 reasoning effort，只要求返回 `ROUTER_OK`。

```powershell
python C:\AI\Codex-Capacity-Router\router.py discover
python C:\AI\Codex-Capacity-Router\router.py route --task-file C:\AI\Codex-Capacity-Router\state\checkpoint.json --requested-model <当前模型>
python C:\AI\Codex-Capacity-Router\router.py status
```

`continue` 会先重新路由，再使用 Codex 原生 `exec resume -m` 接续；若客户端明确拒绝在 resume 时换模型，则建立 continuation thread，并只注入 checkpoint 的 `NEXT_ACTION`、`COMPLETED_STEPS` 与 `DO_NOT_REPEAT`。`NEXT_ACTION` 缺失时安全停止。它不会直接执行或重放 GPU、QC、Git 等本地步骤。已有业务任务必须由外层可恢复控制器提供准确 checkpoint，不能仅凭聊天记录推断完成状态。

```powershell
python C:\AI\Codex-Capacity-Router\router.py continue --task-file <checkpoint.json> --requested-model <当前模型>
```

状态位于 `state/`，路由事件位于 `logs/route-events.jsonl`。全部候选 capacity 时写 `ALL_MODELS_CAPACITY / CHECKPOINTED`，至少等待策略规定的 300 秒才再次健康检查。`CAPACITY` 之外的错误不会自动切换模型。

T1–T7 故障注入：

```powershell
python -m unittest discover -s C:\AI\Codex-Capacity-Router\tests -v
```

真实 app-server 与真实 probe 的可用性需由当前 Codex Home 权限和服务状态单独核验；mock 通过不等于远端模型实际通过。
