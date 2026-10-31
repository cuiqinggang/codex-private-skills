# EXP-DEVSPACE-001｜连接3秒软期限和UNKNOWN写入核账
版本：V1；核查：2026-10-31；分类：CASE/ERROR/CANDIDATE_RULE；证据：DevSpace原生测试与隔离SDK注入回执。

触发：拟用DevSpace Test作为Windows执行连接D通道，希望消除10秒以上慢样本并在3秒后恢复。环境：DevSpace 1.1.0、原工具平台调用，正式执行桥仍为A收费→B→C；D仅在显式选中场景作为候选。
LAST_GOOD：同一已经授权的workspace和原有MCP会话。FIRST_DELTA：用户将3秒“慢回执”误解为所有命令三秒必须完成，可能误断长任务、误重发副作用写入。
实际证据：21字节原生只读探针100/100成功，p50=0.528s、p95=1.013s、最慢1.782s，未触发自然超3s；12秒原生任务的会话持续运行时独立探针仍可响应，原会话完成12.776s；SDK受控注入四类故障各两轮，通过最多一次只读额外请求、创建一次MCP Client或写入UNKNOWN→只读核账，两轮非幂等追加均仅COMMIT一条。恢复不是平台原生强制TCP/TLS重建。旧R5 Shell重载读取100次中曾有首次10.621s，样本不可混合。
正确操作：仅小只读/初始回执3s视为疑似迟滞，不断言断网；持久running/session_id时续读原会话；只读可最多加一次请求；写入回执缺失先核账，绝不盲目重发；一次恢复仍失败则依旧路由和副作用账本处理。
适用：现有D候选、受控SDK的同类恢复语义。不适用：正式A→B→C路由自动改版、长期SLA、全业务3秒完成、原生API保证强制重连、任意业务exactly-once或完整T_VALID提速。
源：C:\AI\DevSpace-Benchmark-20261031\DevSpace-Comprehensive-R6.md、D-Connectivity-Rules-R1.json。