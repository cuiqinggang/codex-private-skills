# UltraFusion v5.0 正式索引

**版本**: v5.0
**最后更新**: 2026-06-17 00:47:00

## 正式定位

UltraFusion 是**自动化多模型 A/B/C/D 极限融合技能包**。

不是手工流程，不是提示词合集，不是答案拼接器。
A/B/C/D 四层全部由自动化执行器完成（Hermes / Codex / Provider Adapter）。

## 正式主流程

| 层 | 描述 | 输出 |
|----|------|------|
| **A 层** | 首轮独立极限稿 | A_<model>_Extreme.md |
| **B 层** | 交叉增强极限稿 | B_<model>_Extreme.md |
| **C 层** | V15 驱动融合极限稿 | C_Fusion_Extreme.md |
| **D 层** | V15 驱动最终稳定极限稿 | D_Final_Ultra_Answer_Final.md |

**无 E 层。** D_Final 即最终报告。

## 硬规则

- 🚫 禁止用户手工粘贴 A/B/C/D
- 🔒 A/B/C/D 四层全部必须注入 V15_FULL
- 📋 D_Final_Ultra_Answer_Final.md 是唯一最终输出
- 🤖 正式执行必须由自动化执行器完成

## 正式目录

| 目录 | 内容 |
|------|------|
| `00-INDEX/` | 正式索引与变更日志 |
| `10-SPEC/` | V15 规范 (Guard / FULL / WITH_GUARD / v5 Summary) |
| `20-RUNBOOK/` | 自动化执行手册 (Hermes / Codex) |
| `30-TEMPLATES/` | A/B/C/D 极限模板 (v4/v3) |
| `35-MODEL-ROSTER/` | 模型阵容、选择、失败规则 |
| `36-PROVIDER-ADAPTERS/` | 多模型 API 适配器 (GPT/DeepSeek/MiniMax 等) |
| `37-SCORING/` | V15 评分 + 扣分规则 |
| `38-PROMPT-ASSEMBLY/` | 提示词拼装规范 + V15 注入硬门 |
| `40-WORKFLOWS/` | 完整 ABCD / D-Lite / 回退 / 消融 / 简化 |
| `45-RUNTIME/` | 运行时状态、命名、成本追踪 |
| `50-TESTS/` | 测试问题 Q1/Q2/QX + 预期输出 |
| `60-KB/` | Ultra Answer 知识库 |
| `70-NOTES/` | 模型行为笔记 |
| `80-SERVICE-ROADMAP/` | 服务化路线图 |
| `90-ARCHIVE/` | 历史归档（旧版 RUNBOOK/SPEC/旧提示词版本） |
| `reports/` | 安装 / 验证 / 修复 / Gate Review 报告 |

## 最终输出

```
D_Final_Ultra_Answer_Final.md
```

包含：最终答案、关键事实、反例测试、推理链闭合、模型贡献、扣分记录、残留不确定性。

## 已废弃

以下内容仅存在于 `90-ARCHIVE/` 中，不再作为正式规则：

- ❌ E 层 / 旧版 5 层流程
- ❌ 手工打开多个 AI 网页复制粘贴
- ❌ 手工拼接多个模型回答
- ❌ 手工评分
- ❌ 旧版 Phase 0 手工 RUNBOOK
