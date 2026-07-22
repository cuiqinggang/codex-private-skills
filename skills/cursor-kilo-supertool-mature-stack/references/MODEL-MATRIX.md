# Model Matrix

## Default

`openrouter/deepseek/deepseek-v4-pro`

Use for:
- code execution
- ordinary debugging
- ordinary file edits
- project work

Live status: verified through OpenRouter smoke call.

## Strong Controller

`openrouter/z-ai/glm-5.2`

Use for:
- strong instruction adherence
- complex command packages
- long workflow orchestration
- Gate Review
- Repair Loop
- risk boundary review

Status: defined controller route, not default executor.

Live status: verified through OpenRouter smoke call.

## Vision Primary

`openrouter/qwen/qwen3-vl-235b-a22b-instruct`

Use for:
- screenshots
- UI understanding
- OCR
- images
- charts/tables
- video keyframes/contact sheets
- multimodal analysis

Live status: verified through OpenRouter smoke call.

## Vision Reasoning Backup

`openrouter/qwen/qwen3-vl-235b-a22b-thinking`

Use only when primary visual reasoning is not enough.

## Light Model

DeepSeek V4 Flash.

Use only for light tasks after stability is confirmed. Fall back to Pro if unstable.

Live status: verified through OpenRouter smoke call.

## Not Default

- Qwen3-VL 8B / 30B
- GLM-4.5V / GLM-4.6V
- Doubao/Kimi/InternVL inventory routes
- Auto Model
- Auto Free
