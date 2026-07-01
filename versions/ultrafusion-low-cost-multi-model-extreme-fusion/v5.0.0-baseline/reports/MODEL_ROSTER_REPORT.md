# 模型阵容报告

**默认 Core-3**:
- M0: GPT (Official Subscription) — 质量锚点
- M1: DeepSeek-V4-Pro — 主力推理
- M2: MiniMax-M2.7 — 多样性

**观察位**: M3-Q: Qwen3.5-Flash

**备用**: Kimi K2, Gemini 2.5 Pro, GLM-4.5

**规则**: 
- Qwen 默认不进 C_Fusion
- 需 6 题消融测试证明才能升级
- 模型失败不伪造
- <2 模型 PASS → 标注受限融合
