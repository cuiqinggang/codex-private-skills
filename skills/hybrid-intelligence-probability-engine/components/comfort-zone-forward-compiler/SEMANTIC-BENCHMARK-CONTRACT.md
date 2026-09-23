# 正向拆解器语义 benchmark 合同

## 目标

验证高智能语义编译层能否从“未预标路由的自然语言任务”正确抽取标准事实，并让确定性路由门把任务最大概率、但不越过证据边界地送入 JEV 舒适区。

## 固定 128 案例

- 32 个 CODE：存在唯一确定算法/规则；
- 32 个 JEV：满足全部已认证 Choice 舒适区条件；
- 64 个 GPT residual / JEV 边界案例。

64 个边界案例必须覆盖：
- 状态不能完整显式化；
- 动作空间不能有限化；
- 非认证动作本体；
- 缺少 deterministic verifier；
- 开放生成仍是任务本质；
- 依赖隐藏外部信息；
- timed retry / 时间条件；
- 转换会损失原任务语义。

## 输入与 oracle 分离

Compiler 只看到 public task。

Verifier 单独读取 hidden oracle：
- expected route；
- expected normalized facts；
- 对 JEV case 的 expected action ontology / verifier contract。

禁止把 hidden oracle 进入 compiler prompt。

## 成熟门

必须：

```text
SEMANTIC_CASES=128
ROUTE_PASS=128/128
UNSAFE_JEV_OVERRROUTE=0
MISSED_CERTIFIED_JEV=0
NORMALIZED_FACTS_GATE=PASS
```

其中：
- unsafe JEV over-route：本应 GPT/CODE 却进入 JEV；
- missed certified JEV：明确满足冻结舒适区却没有进入 JEV。

## 性能

Semantic compiler 的耗时必须进入 Hybrid 完整 T_VALID。

若编译器本身使 Hybrid 的完整 T_VALID 不再优于 Full-GPT，则该方案不能晋级，即使路由准确率 128/128。
