# UltraFusion vNext Decision Log

## Version

- Version: `vNext-2026-07-01-night`
- Theme: core model route adjustment
- New core route: `GPT 官网版 + Kimi 官网会员版 + GLM-5.2 / GLM Coding Plan`

## Discussion Record

1. 最初考虑 DeepSeek，是因为它具备低成本、强推理、可作为核心推理智能体的潜力。
2. DeepSeek 后来被降级，因为快速模式能联网但深度不足，专家/深度思考模式推理强但不能联网。极限任务必须拆成“联网搜索 + 专家深思”两道流程，正式长期使用太麻烦。
3. Qwen 一度被认为可替代 DeepSeek，因为它官网可用、联网搜索整合更顺、中文能力强，适合低成本综合联网分析。
4. 最终 Kimi 比 Qwen 更适合，因为 Kimi 的关键价值不是普通综合助手，而是 Agent Swarm、多智能体分群、多角色并行审查、大规模资料探索和复杂方案分支推演。
5. Kimi 的价值不是普通长文档处理。长文档 GPT 也能做；Kimi 的差异性在复杂任务、多路线探索、多角色审查和大规模资料探索。
6. GLM-5.2 不优先接 Codex，因为用户不希望 Codex 自行摸索协议、配置和兼容性。如果没有公开成熟成功案例，不应浪费时间。
7. GLM-5.2 优先走 Kilo / Claude Code，因为这是更成熟、更符合 Coding Plan 的执行路线。
8. 本次是正式版本，因为它改变了核心模型路线、备用模型定位、测试规则和后续接入策略。

## Final Conclusion

本次版本的核心结论是：

多智能体极限低成本回答技能包的正式核心模型路线调整为：

GPT 官网版 + Kimi 官网会员版 + GLM-5.2 / GLM Coding Plan

DeepSeek 不再作为正式核心，因为它在联网与深度思考之间存在流程割裂，正式使用中需要多一道人工流程，不适合长期极限答案流程。

Qwen / 通义千问保留为低成本综合联网备用模型。如果 Kimi 测试增益不足，Qwen 可替代 Kimi 进入核心。

Kimi 的核心价值不是普通长文档处理，而是 Agent Swarm、多智能体分群、多角色并行审查、大规模资料探索和复杂任务分支推演。它更符合本技能包“极限答案、复杂任务、多样性增益”的目标。

GLM-5.2 不优先尝试 Codex 直连。除非找到公开成熟成功案例，否则不让 Codex 自行摸索。GLM-5.2 优先通过 Kilo / Claude Code 官方成熟路线调用，Codex 通过复制、剪贴板、文件交接或坐标法取回结果。

本次升级属于正式新版本，后续账号准备、Kimi 测试、GLM-5.2 接入测试都应基于本版本继续推进。
