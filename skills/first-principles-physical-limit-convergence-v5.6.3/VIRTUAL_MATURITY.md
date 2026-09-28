# v5.6.3 虚拟成熟记录

结论：`VIRTUAL_MATURE=PASS`。`REALITY_CERTIFIED=NO`。

## 输入
v5.6.2 现实认证：`8355 PASS / 2 FAIL`。原 v5.6.1 的 6 个 FAIL 已全部消失；剩余两项只属于时间起点实现边界：

1. 状态10没有起点，状态40后事后向可变 `context` 补 `accepted_tick_ns` 仍能被接受。
2. Python 中 `bool` 是 `int` 子类，`False/True` 被误当 tick。

## 最小修改
只改 `runtime.py` 的时间起点冻结和 tick 类型判断；`display.py` 仅机械更新版本显示为 v5.6.3。状态表、实体证据、交接、30→40、FAIL/UNKNOWN 语义不改。

实现：
- 状态10时 runtime 只登记一次 `(context对象, accepted_clock, accepted_tick_ns)`。
- 后续时间计算只读取这份内部登记，不再从后续可变 context 读取起点。
- `type(value) is int and value >= 0` 才是合法 tick；`bool` 明确排除。
- 若进程/上下文没有状态10登记，则保持 `整体已用=未知`、`T_VALID=尚未产生`。

## 虚拟结果
- 两个现实FAIL：`2/2` 定向拦截。
- 正常冻结整数 tick：PASS。
- 合法整数0：PASS。
- 四项定向测试：`4/4 PASS`。
- 状态20：`2187/2187 PASS`。
- 状态30：`2187/2187 PASS`。
- 状态40：`3888/3888 PASS`。
- 原回归总计：`8262/8262 PASS`。

没有增加新Gate，没有重构其他已通过部分。
