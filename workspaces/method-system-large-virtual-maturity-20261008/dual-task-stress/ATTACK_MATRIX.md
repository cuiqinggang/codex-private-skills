# 双大型任务并行压力攻击矩阵

METHOD=ENGINE22 / BRAIN19 / TEMPLATE17
CONTRACT=METHOD-SYSTEM-LARGE-VIRTUAL-MATURITY-20261008 V3
RESTART_FROM_BOTH_TASK_ACCEPTED=YES

TASK_A_ID=DUAL-STRESS-A-LTMVH-PAGE-CONTROL-20261008
TASK_B_ID=DUAL-STRESS-B-H3P1-VIDEO-CONVERGENCE-20261008

## 必打攻击

| 编号 | 攻击 | 预期 |
|---|---|---|
| X01 | A/B 同时 PAGE_TOPOLOGY=CEO_EXECUTOR | 各自一个 ACTIVE_CEO |
| X02 | A/B 同时派发 Executor | 独立 TASK_ID/NODE_ID |
| X03 | Executor 返回交错 | 各自 CEO 只 Merge 本任务 |
| X04 | A/B 同时申请 GitHub main writer | 单 lease owner；另一任务只等写节点 |
| X05 | A CEO 第3 Freeze 换页时 B 继续 | B 无暂停/回滚 |
| X06 | B CEO 第3 Freeze 换页时 A 继续 | A 无暂停/回滚 |
| X07 | A Reality FAIL/R15 | B 正常推进 |
| X08 | B Reality FAIL/publication race | A 正常推进 |
| X09 | A Repair/Reverify | 不触碰 B Freeze |
| X10 | B Repair/Reverify | 不触碰 A Freeze |
| X11 | A stall/True New Chat | B exactly-once 不受影响 |
| X12 | B INVALID fast candidate | 不污染 A T* / 不冒充 B T* |
| X13 | A/B 同一 persistent browser 不同页 | 禁止第二 browser；按 PAGE_ID 回收 |
| X14 | A 先完成时 B 仍运行 | A 只回收 A 页；不恢复系统单空白根页 |
| X15 | B 后完成 | 最终系统浏览器恢复 1 个空白 New chat 根页 |
| X16 | 旧 CEO / 新 CEO 接管交错 | 每 TASK_ID 内 exactly-one writer |
| X17 | STATE_REF / Freeze path 交叉注入 | 必须拒绝跨 TASK 读取/写入 |
| X18 | 同 RESOURCE_ID 双 owner 竞争 | lease 串行，无双 writer |
| X19 | 一任务回虚 | 另一任务已接受事实不可回滚 |
| X20 | 一任务关闭 Executor | 不得关闭另一任务 PAGE_ID |

最低重复门槛：
Executor parallel wave>=4；interleaved returns>=8；CEO Merge>=12；Freeze>=10/task；
True New Chat>=3/task；FAIL/Delta>=2/task；Repair/Reverify>=2/task；
shared writer contention>=6；page close>=8；second persistent browser launch=0。
