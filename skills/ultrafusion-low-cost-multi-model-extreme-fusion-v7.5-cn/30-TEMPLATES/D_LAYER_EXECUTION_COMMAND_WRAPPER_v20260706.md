# V7.5 中文审校说明：D 层执行包装器

D 层必须先输出最终答案，再做评估。

禁止只输出评估报告。

D 层必须包含：

- `FINAL_ANSWER`：先回答原问题；
- `SCORE_FINAL`：最终评分；
- 准确性、完备性、结构清晰度、深度洞察、风险、过度自信检查；
- 人工确认点；
- `Score_0 vs SCORE_FINAL`；
- `Gain`；
- `EFFECTIVE_CHAIN` / `INVALID_CHAIN` 判断。

推荐 `temperature = 0.20`，建议范围：`0.10 - 0.25`。

失败状态码：

- `D_META_EVALUATION_WITHOUT_FINAL_ANSWER`：D 层只评测流程，没有先回答原问题。
- `D_LAYER_V15_FULL_MISSING`：D 层缺少完整 V15。
- `FINAL_ANSWER_TOO_THIN`：最终答案过薄，缺少可执行深度。

---

# D Layer Final-Answer-First Command Wrapper

Status: active
Route: `UF_V7_SEMI_AUTO_ABCD`
Purpose: ensure D layer generates the final answer to the original question before any scoring, benchmark, or meta-evaluation appendix.

## Required Placement

Place this command immediately after `[COPY_START]` and before source materials / long D rubric.

This wrapper is only the first instruction block. It must not be used alone. A valid D-layer package must also include:

- full canonical V15 from `10-SPEC/V15_FULL_WITH_GUARD_v1.0.md`
- official D prompt from `30-TEMPLATES/40_D_Layer_Final_Extreme_Report_Template_v3.0.md`
- original question Q
- `A_Initial / Score_0`
- `C_Fusion`

If V15 or the official D prompt is missing, the D package is invalid even if this wrapper is present.

## Production-Depth Requirement

The wrapper must prevent short summary D answers. `Ultra_Answer_Final` must be a production-grade deliverable, not a simplified outline.

Required minimum content in the first section:

- system goal and boundaries
- 0/A/B/C/D flow table
- human copy-paste SOP
- 1-person and 3-person role split
- copyable 0/A/B/C/D prompt templates
- Markdown/Excel run record schema
- four-dimension scoring rubric and calibration
- privacy redaction SOP
- time and cost control
- `Gain < 2` failure attribution tree
- 30-day validation plan
- Go / Internal Tool / No-Go decision thresholds

If the output lacks these concrete artifacts, mark it:

```text
UF_D_OUTPUT_FAIL: FINAL_ANSWER_TOO_THIN
```

## Wrapper Text

```text
【D层执行命令：FINAL_ANSWER FIRST】

请基于下面的原始问题 Q、C_Fusion 候选稿、A_Initial/Score_0，生成 UltraFusion V7.0 D 层最终交付结果。

最重要：你的主任务不是评价 UltraFusion 系统本身，而是回答原始问题 Q，产出一份可以直接交付给用户使用的最终方案。

输出必须按以下顺序：

# 1. Ultra_Answer_Final（必须第一部分输出）

这一部分必须是对【原始问题 Q】的完整最终答案，而不是评测摘要。必须覆盖：

1. 系统流程
2. 角色分工
3. A/B/C/D 复制粘贴执行方式
4. 提示词/记录模板
5. 质量评分办法
6. 成本与时间控制
7. 隐私脱敏与安全规则
8. 风险清单与失败归因
9. 30 天验证计划
10. Go / Internal Tool / No-Go 决策标准

# 2. D层验收附录（第二部分输出）

在最终答案之后，再输出简短验收附录：关键事实表、四维评分、SCORE_FINAL、Gain、反例测试、推理链闭合性、风险分析、Benchmark 结论。

硬性禁止：
- 禁止只输出评估报告而没有 Ultra_Answer_Final。
- 禁止把 Ultra_Answer_Final 写成“对系统是否成立的判断”。
- 禁止只分析 Gain、统计学问题、SaaS 可行性，而不回答原始问题 Q。
- 禁止用“我可以继续帮你做 Python pipeline / SaaS 架构”作为结尾替代答案。

完整度要求：
- 不要输出“简版”“摘要”“估计版”。
- 如果篇幅需要压缩，请压缩 D 层验收附录，不要压缩 Ultra_Answer_Final。
- Ultra_Answer_Final 必须包含可复制的 0/A/B/C/D 提示词模板。
- Ultra_Answer_Final 必须包含完整运行记录 Schema，字段包括 Score_0、SCORE_FINAL、Gain、t_A、t_B、t_C、t_D、Total_Time、BreakType、Human_Error、PII_Status。
- Ultra_Answer_Final 必须包含隐私脱敏 SOP 和 Gain < 2 失败归因树。

现在开始。第一行必须是：
# 1. Ultra_Answer_Final
```
