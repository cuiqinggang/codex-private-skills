# UltraFusion V7.0 Semi-Auto Question Package Template

Status: active template
Route label: `UF_V7_SEMI_AUTO_ABCD`

## Canonical V15 Source Rule

Before generating any A/B/C/D copy block, load and paste the full canonical V15 text from:

```text
10-SPEC/V15_FULL_WITH_GUARD_v1.0.md
```

Do not use a short summary, simplified rewrite, or placeholder. A package that still contains `<<<V15_FULL>>>`, or only says "follow V15" without the full text, is invalid.

Required manifest fields for every layer package:

```text
V15_SOURCE=10-SPEC/V15_FULL_WITH_GUARD_v1.0.md
V15_SHA256=BB836AC959885190A1BEC81ECA77454F0CD183D08BB3814070A977C39147514E
V15_STATUS=CANONICAL_FULL_TEXT_INJECTED
```

## Copy Block Wrapper

Use this wrapper for every package sent to an external model:

```text
[ULTRAFUSION_V7_LAYER=<A|B|C|D>]
[QUESTION_ID=<stable_short_id>]
[COPY_START]
<PACKAGE_BODY>
[COPY_END]
```

Only the content between `[COPY_START]` and `[COPY_END]` should be pasted into the external model.

## Layer 0 Baseline Scoring Prompt

```text
你是 UltraFusion V7.0 的基准评分器。

请评估下面的“原始问题 Q”和“普通模型答案”，输出：
1. Score_0（0-10）
2. 原始答案质量分析
3. 关键缺陷、遗漏、幻觉或风险
4. 是否值得进入 UltraFusion ABCD 流程

原始问题 Q：
<<<Q>>>

普通模型答案：
<<<BASELINE_ANSWER>>>
```

## A Layer Package Body

```text
你正在执行 UltraFusion V7.0 的 A 层：极限生成层。

核心要求：
- 严格遵守完整 V15 质量要求。
- 独立生成一个尽可能强的极限答案。
- 不要等待其他模型，不要融合他人答案。
- 输出必须包含：A层答案、核心依据、关键假设、风险与不确定性。

V15：
<<<V15_FULL>>>

A_PROMPT：
<<<A_PROMPT>>>

原始问题 Q：
<<<Q>>>

请输出：A_EXTREME_ANSWER。
```

## B Layer Package Body

```text
你正在执行 UltraFusion V7.0 的 B 层：融合增强层。

核心要求：
- 严格遵守完整 V15 质量要求。
- 阅读全部 A 层答案。
- 吸收所有强点，修复缺陷，生成一个新的更强答案。
- B 层不是审稿意见；不要只评价 A1/A2/A3。
- 输出必须是可直接使用的 B_EXTREME_ANSWER。

V15：
<<<V15_FULL>>>

B_PROMPT：
<<<B_PROMPT>>>

原始问题 Q：
<<<Q>>>

A层答案：
<<<A1>>>
<<<A2>>>
<<<A3>>>

请输出：B_EXTREME_ANSWER。
```

## C Layer Package Body

Official C prompt source:

```text
30-TEMPLATES/C_LAYER_OFFICIAL_FUSION_PROMPT_v20260706.md
```

For V7.0 full ABCD benchmark runs, paste that official C prompt verbatim after the canonical V15 text. Do not use the compact skeleton below as the live C prompt. The assembled C package must contain `复检陌生稿规则`, `四维稠密融合`, evidence/data hard rules, and output sections `【最终答案：C_Fusion】`, `【评审报告】`, and `【版本说明】`.

```text
你正在执行 UltraFusion V7.0 的 C 层：策略整合层。

核心要求：
- 严格遵守完整 V15 质量要求。
- 阅读全部有效 B 层答案。
- 生成唯一策略答案 C_FINAL。
- 必须明确最终判断、取舍、执行路径、反例、边界条件和未解风险。

V15：
<<<V15_FULL>>>

C_PROMPT：
<<<C_PROMPT>>>

原始问题 Q：
<<<Q>>>

B层答案：
<<<B1>>>
<<<B2>>>
<<<B3>>>

请输出：C_FINAL。
```

## D Layer Package Body

Execution command source:

```text
30-TEMPLATES/D_LAYER_EXECUTION_COMMAND_WRAPPER_v20260706.md
```

For V7.0 D-layer packages, paste this execution command immediately after `[COPY_START]` and before the long V15 / D_PROMPT content. The first visible instruction must tell the external model to execute D layer, not summarize or classify the package.

```text
你正在执行 UltraFusion V7.0 的 D 层：最终收敛层。

核心要求：
- 严格遵守完整 V15 质量要求。
- 以 C_FINAL 为主输入，进行最终收敛。
- 检查事实、逻辑、反例、风险、执行性和过度自信。
- 输出 FINAL_ANSWER、SCORE_FINAL、风险分析。

V15：
<<<V15_FULL>>>

D_PROMPT：
<<<D_PROMPT>>>

原始问题 Q：
<<<Q>>>

C_FINAL：
<<<C_FINAL>>>

请输出：
1. FINAL_ANSWER
2. SCORE_FINAL（0-10）
3. 风险分析
4. 仍需人工确认的点
```
