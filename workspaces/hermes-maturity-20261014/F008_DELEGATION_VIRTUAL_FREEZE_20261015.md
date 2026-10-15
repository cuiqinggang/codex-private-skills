# Hermes F008｜双子代理独立审核 Gate 前置虚拟成熟
TASK=HERMES-ECO-20261014 | NODE=H-ECO-02-DELEGATION-F008 | 方法《三人行》第2版仅本项目适用 | V6执行桥C>A>B | Hermes专用技能v2.0
STATE=VIRTUAL_MATURE_FROZEN；Reality前置，只在 F007 结果完成且无其它Hermes生产任务占用时执行。

不将旧8月 delegate_task 历史 PASS 当本阶段 RUNTIME_PASS，也不把四个 runAs: subagent skill 文件冒充真实spawn；复用官方 https://hermes-agent.nousresearch.com/docs/user-guide/features/delegation 的原生 delegate_task 批量模式：新建两个拥有隔离上下文的真实子代理，只汇总实际回执。

输入范围：既有只读合成 F005_REPAIR 目录中的 requirements.md、invoice.py、test_invoice.py；不运行被平台安全门拦截的 cmd/unittest；不更改任何文件/服务/配置/代理/密钥。
- Child A：实际读取 requirements.md 与 invoice.py，检查 paid-only / bool / ValueError / negative / large int 规则，返回明确独立FAIL/PASS与所见缺陷。
- Child B：实际读取 requirements.md 与 test_invoice.py，审核测试覆盖范围，不修改任何内容，返回PASS/FAIL与覆盖结论。
要求主控一次原生 delegate_task 批量调用，两个子任务分别独立上下文返回，并收集至少两份真实完成回执；若异步后台不能在CLI一次性关闭前完成，不冒称通过，不以父模型自报代替原生孩子事件。只做一次自然任务，失败进入对账，禁止为了凑数而重发。
成功必要条件：官方系统侧两个不同 child_session_id + 均实际结束 + 文件证据与外部事实一致 + 父汇总有两个独立审查条目；只有模型回答没原生spawn事件时状态最多 PARTIAL_OBSERVED_TOOL_EVIDENCE_PENDING。
计时：与CLI完整任务同起终单调时间；不能把模型答句局部时间称端到端最优。
