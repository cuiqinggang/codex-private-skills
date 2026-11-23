# UltraFusion v5.0 Official Spec Summary

**版本**: v5.0
**生成时间**: 2026-06-17 00:47:00
**定位**: 正式规范摘要，取代旧版 SPEC_KIT_v1.1 中的手工/半手工描述

---

1. UltraFusion 是**自动化多模型 A/B/C/D 极限融合系统**。

2. **A/B/C/D 四层全部必须注入 V15_FULL**。
   每层 assembled prompt = V15_Guard_Prefix + V15_FULL + Layer_Template + Layer_Inputs + Question。

3. **A 层**生成首轮独立极限稿 `A_<model>_Extreme.md`。

4. **B 层**生成交叉增强极限稿 `B_<model>_Extreme.md`。
   B 层输入包含所有有效 A 层极限稿。

5. **C 层**生成 V15 驱动融合极限稿 `C_Fusion_Extreme.md`。
   C_Fusion 是融合极限稿，不是普通合并。
   C 层必须注入 V15_FULL。

6. **D 层**生成 V15 驱动最终稳定极限稿 `D_Final_Ultra_Answer_Final.md`。
   D_Final 是最终报告，不是普通审核。
   D 层输入 prompt 必须包含 V15_FULL，但输出不得复贴 V15 原文。

7. **禁止用户手工粘贴 A/B/C/D**。
   正式执行必须由自动化执行器完成（Hermes / Codex / Provider Adapter / Runner）。

8. **不设 E 层。** D_Final 即最终报告。

9. **GPT 默认通过官网套餐自动化接入**，不默认 OpenAI API。
   GPT 是固定质量锚点，从 A 层到 D 层全程参与。

10. **默认模型阵容 (Core-3)**：
    M0: GPT-latest via official subscription automation
    M1: DeepSeek-V4-Pro (官方 API)
    M2: MiniMax-M2.7 (官方 API)

11. **Qwen3.5-Flash 为观察位 (M3-Q)**，需经 6 题消融测试证明独立贡献才可升级。

12. **缺失模型不得伪造**。
    低质量模型不得强行进入 C_Fusion。
    少于 2 个模型 PASS → D_Final 标注"受限融合"。

13. **扣分原则**是质量控制核心。
    FinalScore = V15_BaseScore − DeductionPoints + UniqueContributionBonus。

14. **最终输出**是 `D_Final_Ultra_Answer_Final.md`。
    包含：最终答案、关键事实、反例测试、推理链闭合、模型贡献、扣分记录、残留不确定性。

15. **旧版手工 RUNBOOK** 归档于 `90-ARCHIVE/`，不参与正式执行。

---

## 正式规范源

| 优先级 | 文件 |
|--------|------|
| 1 | SKILL.md |
| 2 | README.md |
| 3 | 38-PROMPT-ASSEMBLY/ (6 文件) |
| 4 | 40-WORKFLOWS/Automated_ABCD_Extreme_Workflow_v5.0.md |
| 5 | 35-MODEL-ROSTER/ (6 文件) |
| 6 | 37-SCORING/ (3 文件) |
