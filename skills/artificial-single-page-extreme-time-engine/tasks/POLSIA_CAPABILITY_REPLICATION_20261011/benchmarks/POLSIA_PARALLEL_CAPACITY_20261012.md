# Polsia 并行执行容量对比（实际测试，2026-10-12）

BENCHMARK_ID=POLSIA_PARALLEL_NATIVE_COMPARE_20261012
TASK_ID=POLSIA_CAPABILITY_REPLICATION_20261011
BASELINE_FREEZE=POLSIA-MOTHER-V008-F001
STATUS=ISOLATED_BENCHMARK_PASS_SCOPE_LIMIT
MOTHER_FINAL_VALID=NO

## 结论

在本机 Intel Core i5-3570（4核4逻辑）、32GB 内存、开始时约13GB可用内存的条件下，原生PowerShell 7运行空间线程方案更适合轻量独立任务；大量新PowerShell进程的启动开销较大。十个逻辑业务方向可以持续维护，但不意味着十个重型CLI进程同时常驻。

初始策略：本地文件审计/计算任务先以2个并发运行，实际提速稳定后可试4；等待型操作先4，必要时试8。不同业务负载需分别测量。Codex Ultra的1/2/3多Agent真实任务对照尚未执行，不能把本地线程测试结论外推成模型并行最优。

## 实测方法与完整性

- V008不可变清单128个文件；分配为12个不重叠的独立验证任务。
- 使用3种成熟原生实现：串行、ForEach-Object -Parallel（复用runspace）、Start-Job（独立进程）。同一负载各2次。
- 实际文件SHA256重复校验；等待型另设置每任务350ms受控睡眠，只模拟等待，不是真实API。
- 重负载每组11,520次哈希，正序和反序各1次，控制顺序偏差。
- 合计36轮、432个任务回执、134144次哈希校验；所有案例通过：true。
- 实验文件仅存放在 C:\AI\Polsia-Parallel-Benchmark-20261012，业务V008未重播。
- 实验后验证V008冻结文件SHA256 DAE228125E797E4CC2ABE3316346D37A1038148826525888AC3496B12A94676F、Manifest SHA256 2F3C40F4E80B5B7C49785335FA4AE17A9F592C5BB3603082F0C2FA212CCE7EB7 未改变。

## 短任务及等待型：两轮平均耗时（秒）

|方案|并发|轻量文件审计|含350ms等待|
|---|---:|---:|---:|
|串行|1|0.700|4.754|
|运行空间线程|2|0.461|2.801|
|运行空间线程|4|0.434|1.547|
|运行空间线程|6|0.444|未测|
|运行空间线程|8|0.438|0.951|
|独立PowerShell进程|2|8.059|未测|
|独立PowerShell进程|4|8.368|9.094|
|独立PowerShell进程|8|9.044|未测|

等待型runspace-8相对串行约5.00倍；轻任务独立进程方案由于进程初始化开销反而更慢。

## 重负载：每轮11,520次SHA256，两轮秒数与均值

|方案|并发|第一轮|第二轮|均值|
|---|---:|---:|---:|---:|
|serial|1|5.803|3.706|4.754|
|runspace|2|2.439|1.979|2.209|
|runspace|4|3.015|1.873|2.444|
|runspace|6|2.590|2.594|2.592|
|runspace|8|2.209|2.086|2.147|

8线程均值2.147秒、2线程2.209秒，差异约2.9%，在两轮噪声范围内，不足以认定8线程全面最优。数据有缓存与其他进程扰动，未测真实Codex的token/延迟、网络限额、CPU持续百分位或跨组件业务完成时间。

## 选定成熟组合（阶段性，不更改现役运行层）

1. GPT CEO 唯一决策；按研发、营销、客服、销售、财务、多Agent、监控、恢复、学习、系统集成维护十个逻辑业务方向。只对READY任务派工，不因一处BLOCKED而停止全部分支。
2. 本机本地并行使用正式PS7原生ForEach-Object -Parallel/ThrottleLimit；CPU/本地读写型默认2，可实测到4；I/O等待型默认4，可实测到8。任何扩容需比较相同任务总有效时间、失败和资源变化，有负收益则回退。
3. 智能任务优先复用Codex官方内建多Agent，初步仅做1/2/3多Agent的公平单合同真实试验；不直接启动十个互相竞争的Codex CLI。
4. 独立OS进程只在确需崩溃隔离/进程权限隔离时使用，不能因为“并行越多越好”而替代轻量runspace。
5. 每分支独立TASK_ID、工作目录、回执、Freeze；母任务GitHub CURRENT/VERSION仅CEO单写者可合并；DONE不重做、UNKNOWN先对账。
6. n8n现有管理HTTP401和Docker拒绝，当前不可当作已验证的自动工作流；不得绕过授权或读取凭据。
7. 不改动引擎第28版、方法v3.2.2、现役Windows运行脚本v3.1.0、原计划任务/FlClash/浏览器；无支付、外联、发布、生产副作用。

## 未通过的范围

这是Windows原生执行层容量评估，不是九类Polsia完整能力认证，也不是Codex Ultra真实并行最优证明。模型层、跨组件真实业务层、冷启动、72小时、全合同T_VALID、物理极限与最终优化10轮仍UNKNOWN/未验证。V008已冻结，母任务NEEDS_GPT为CEO_NEXT_SCOPE_DECISION_REQUIRED；下一项业务需单独审批。

## 原始证据与可重复入口

- C:\AI\Polsia-Parallel-Benchmark-20261012\audit_worker.ps1
- C:\AI\Polsia-Parallel-Benchmark-20261012\compare.ps1
- C:\AI\Polsia-Parallel-Benchmark-20261012\heavy.ps1
- C:\AI\Polsia-Parallel-Benchmark-20261012\results.json
- C:\AI\Polsia-Parallel-Benchmark-20261012\heavy.json

本摘要与相邻JSON独立保存，绝不代替V008 Freeze或修改项目CURRENT。