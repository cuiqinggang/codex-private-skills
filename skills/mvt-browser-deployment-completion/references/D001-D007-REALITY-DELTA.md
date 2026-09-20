# D001–D007 Reality Delta 与固定解决法

| ID | 现实问题 | 根因 | GPT 冻结解决法 | 通过证据 |
|---|---|---|---|---|
| D001 | FROZEN_REAL_RUN_CONFIG_INCOMPLETE | 组件存在但没有唯一现实运行入口配置 | 生成唯一 run-config，锁定 source/route/task/condition/repeat/timing/result | run-config schema + hash |
| D002 | FROZEN_HARNESS_MATRIX_BINDING_MISSING | matrix 与 route runner 没有一一绑定 | 生成 route-bindings；每个 required tuple 必须 exactly-one binding | ambiguous=0, unbound=0 |
| D003 | COLD_WARM_RECONNECT_SEMANTICS_NOT_EXECUTABLE | 只有自然语言条件定义 | 冻结为三套事件状态机 | state-machine simulation PASS |
| D004 | T_VALID_FULL_RECORD_CONTRACT_NOT_IMPLEMENTED | 统一指标没有统一 recorder | 单一 recorder schema 与 monotonic start/stop events | boundary override=0 |
| D005 | REQUIRED_RESULT_PIPELINE_MISSING | runner 输出没有统一进入统计/winner | runner->verifier->JSONL->stats->provisional winner->hash | pipeline simulation PASS |
| D006 | FROZEN_CAPABILITY_MATRIX_MISSING | 能力声明未绑定到可执行 case | capability case 必须包含 fixture/request/expected/verifier/repeats | every frozen capability bound |
| D007 | RECOVERY_EXECUTION_NOT_BOUND | recovery trigger 有定义但没有执行绑定 | fault injector->recovery runner->verifier->record | 6 fault families simulation PASS |

## 重要经验

“runner 存在”“harness 存在”“单元测试通过”均不足以证明现实竞争可运行。

必须额外证明：

```text
CONFIG
+ BINDING
+ STATE MACHINE
+ TIMING RECORDER
+ RESULT PIPELINE
+ CAPABILITY MATRIX
+ RECOVERY BINDING
= REALITY COMPETITION ASSEMBLY
```

只有总装完整性 PASS 才可交给现实执行器。
