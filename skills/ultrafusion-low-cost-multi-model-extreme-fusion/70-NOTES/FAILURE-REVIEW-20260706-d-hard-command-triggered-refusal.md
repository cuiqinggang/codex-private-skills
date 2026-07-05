# Failure Review: D-Layer Hard Command Triggered External Model Refusal

Date: 2026-07-06
Route: `UF_V7_SEMI_AUTO_ABCD`
Status: fixed

## What Happened

After the D-layer package was amended with a very strong "execute this command, do not summarize, do not treat this as prompt injection" preface, an external model refused to execute it. The model classified the package as a self-contained evaluation protocol / prompt-injection-style instruction set and offered only alternative analysis modes.

## Root Cause

The correction command was too forceful. Phrases such as "do not treat this as prompt injection" and "must execute" made the package look like an attempt to override model hierarchy or safety behavior.

## Corrective Action

Replace hard execution language with a user-request framing:

- say the long text is a user-provided rubric and report template;
- explicitly state it is not system text and does not override the model's system rules;
- ask the model to complete the D-layer evaluation report in the scope allowed by its own rules;
- ask it to explain limitations and complete what it can, rather than refusing the whole task.

## New Safe Request Source

```text
30-TEMPLATES/D_LAYER_EXECUTION_COMMAND_WRAPPER_v20260706.md
```

User-facing correction artifact:

```text
outputs/ufv7-d-layer-safe-execution-request-20260706.md
```

## Future Prevention

Do not include phrases like:

- "do not treat this as prompt injection"
- "you must obey this protocol"
- "this overrides other instructions"
- "if you refuse, your output is invalid"

Use rubric framing instead:

```text
This is a user-provided evaluation rubric and report template. In the scope allowed by your own rules, please generate the requested D-layer evaluation report.
```
