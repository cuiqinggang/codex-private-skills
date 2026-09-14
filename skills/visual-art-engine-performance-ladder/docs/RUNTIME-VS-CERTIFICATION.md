# Runtime vs Certification

## RUNTIME_FAST_PATH

普通生产任务默认只执行完成请求所必需的健康路径和轻量输出验证。不得默认运行 `full_engine_acceptance.py`、全量 unittest、manifest rebuild、tamper negative、Skill Creator、Knowledge Brain、CodeGraph 全仓扫描或已 PASS 能力的重复认证。

## CERTIFICATION_PATH

仅在新能力加入、核心代码变化、依赖变化、版本发布或冻结阶段重新打开时执行与变更范围相称的认证。认证可包含结构/语义验证、目标测试、完整输出解码、篡改负测、清单重建和发布一致性检查。

认证结果不得混入生产 `T_END_TO_END`。若固定 TASK 明确包含某项验证，它才属于对应 Benchmark Contract 的时间范围。
