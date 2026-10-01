# Reality R2｜v0.1.3 静态调度隔离真实验证

```ini
VERSION=0.1.3
SOURCE_COMMIT=4ede02697a647c34e89dd91551578c0b6e910673
WORKFLOW_RUN_ID=36900593142
SCOPE=STATIC_DISPATCH_ISOLATION

CONTRACT_STATIC=PASS
POWERSHELL_PARSE=PASS
TASK_CONTRACT=PASS
TASK_DISCOVERY=PASS
WINDOWS_REALITY=SKIPPED_EXPECTED
GLOBAL_CONCURRENCY_BLOCK=FIXED

BRIDGE_REALITY_CERTIFIED=NO
WINDOWS_RUNNER_PICKUP=NO
```

## 结论

v0.1.2 的 workflow 级 concurrency 会被旧的 queued Windows Reality 占住，导致后续静态验证也 pending。

v0.1.3 将并发串行约束下沉到 `windows-reality` job。Run 36900593142 已真实证明：
- GitHub-hosted 静态门禁可以在旧 Windows job 仍排队时独立运行并成功；
- 本次提交未修改 task JSON，因此 Windows job 被正确 skip；
- 非任务更新不再进入本机 runner 队列。

这只证明调度隔离修复成立，不等于完整执行桥 Reality PASS。

## 下一 Reality 门

仍必须完成：

```text
目标 Windows self-hosted runner 在线
→ 领取 ETAL-BRIDGE-SMOKE-001
→ payload 真执行
→ result.json
→ artifact
→ PASS
```

之后再验证：

```text
Windows result
→ 自动回调/调度
→ GPT 自动继续下一轮
```

只有连续无人闭环满足 `USER_INTERVENTIONS=0`，执行桥才可升级为 Reality PASS。
