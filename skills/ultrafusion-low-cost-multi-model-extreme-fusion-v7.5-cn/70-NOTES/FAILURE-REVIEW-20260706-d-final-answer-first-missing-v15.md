# Failure Review: D Final-Answer-First Package Missing V15

Date: 2026-07-06

## What Happened

A D-layer rerun package was rebuilt to force `FINAL_ANSWER FIRST`, but the package omitted the full canonical V15 body and official D prompt. The user caught the issue before reuse.

## Why This Is Wrong

In UltraFusion V7.0 full ABCD runs, every layer must inject V15. The D layer also needs the official D prompt for final convergence, fact checking, scoring, Gain calculation, counter-example testing, and risk analysis.

The `FINAL_ANSWER FIRST` wrapper fixes output order only. It does not replace V15, D_PROMPT, or layer-specific evidence inputs.

## Correct D Package Assembly

```text
[COPY_START]
D execution wrapper / FINAL_ANSWER FIRST
Original question Q
Full canonical V15
Official D prompt
A_Initial / Score_0
C_Fusion
[COPY_END]
```

## Future Gate

Invalidate any D-layer package if:

- it lacks `V15+G 前置约束层`, `Auto-V15`, or `V15 瀑布式`
- it lacks `本阶段（D 层）核心定位与约束`
- it contains an unreplaced placeholder such as `<<<V15_FULL>>>` or `在这里粘贴完整 V15 文本`
- it only contains the final-answer-first wrapper without V15 and the official D prompt

Failure codes:

```text
UF_PROMPT_ASSEMBLY_FAIL: D_LAYER_V15_FULL_MISSING
UF_PROMPT_ASSEMBLY_FAIL: D_LAYER_OFFICIAL_PROMPT_MISSING
UF_PROMPT_ASSEMBLY_FAIL: V15_PLACEHOLDER_NOT_REPLACED
```
