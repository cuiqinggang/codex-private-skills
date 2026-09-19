# 执行架构：你 + 核心大脑 + 自动化 AI 工厂

## Human Owner
负责 Why / What / Accept：商业目标、用户价值、边界、成本上限、最终验收。不要求直接阅读代码。

## Core Brain
使用最高推理档模型或经验证等价强模型，负责 External Frontier 综合、Virtual Mature State、架构/能力契约、重大 trade-off、疑难故障和最终决策。

## AI Factory
大量低成本模型/Agent 并行负责 coding、integration glue、tests、docs、log classification、candidate fixes、browser flows。

## Deterministic Verification
能程序判定的绝不让 LLM 猜：exact readback、hash、schema、build/test、latency/throughput、rollback、permission boundary、regression counts。

## 控制闭环
Human Goal
→ Core Brain creates Virtual Mature State
→ capability graph + mature command package
→ AI Factory executes
→ deterministic tools produce evidence
→ Core Brain accepts/rejects
→ repair loop
→ real maturity freeze

## 不会写代码的创始人能否总控
可以，但必须满足：
1. 代码可信度不依赖本人肉眼审查。
2. 每个关键能力都有机器可判定证据。
3. 高风险动作有权限边界、preview/diff/rollback 或审批门。
4. 最终成熟由真实运行证据决定，而不是模型自评。

不会代码不是硬阻断；缺少可靠验证与责任边界才是硬阻断。
