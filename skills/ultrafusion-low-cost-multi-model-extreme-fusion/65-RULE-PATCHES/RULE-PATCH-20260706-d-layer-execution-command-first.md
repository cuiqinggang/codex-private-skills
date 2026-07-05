# Rule Patch: D Layer Must Start With An Execution Command

Date: 2026-07-06
Route: `UF_V7_SEMI_AUTO_ABCD`
Status: active

## Problem

An external model may summarize a long D-layer copy package as a "prompt framework" or "prompt injection risk" instead of executing the D-layer task.

This happens when the package contains a large protocol but does not foreground the action command strongly enough.

## Rule

Every V7.0 D-layer copy package must begin with a short execution command before the long V15 / D_PROMPT content.

The command must explicitly say:

- this is an execution task, not a document summary;
- the model is executing UltraFusion V7.0 D layer;
- V15, D_PROMPT, Q, C_Fusion, and A_Initial/Score_0 are task inputs;
- the model must output D_Final / Ultra_Answer_Final, SCORE_FINAL, Gain, and risk analysis;
- summarizing or treating the package as prompt-injection research is invalid.

## Source

Use:

```text
30-TEMPLATES/D_LAYER_EXECUTION_COMMAND_WRAPPER_v20260706.md
```

## Failure Code

```text
UF_PROMPT_ASSEMBLY_FAIL: D_LAYER_EXECUTION_COMMAND_MISSING
```

If this command is missing, regenerate the D-layer package before external copy/paste.
