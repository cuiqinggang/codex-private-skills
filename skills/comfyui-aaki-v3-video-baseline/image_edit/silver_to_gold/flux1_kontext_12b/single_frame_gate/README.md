# FLUX.1 Kontext 12B Silver To Gold Single Frame Gate

This module is an extension of the existing ComfyUI Aaki v3 video baseline.

Use it only for a one-frame local image-edit gate before multi-frame or video production.

Current verified test:

- Frame: `177`
- Model: `flux1-dev-kontext_fp8_scaled.safetensors`
- Text encoders: `t5xxl_fp8_e4m3fn_scaled.safetensors`, `clip_l.safetensors`
- VAE: `ae.safetensors`
- Final output method: model raw output inside mask, original image outside mask.

Rule:

Do not use the raw model full-image output as final. The accepted candidate must be composited:

`final_candidate = original_outside_mask + model_edited_inside_mask`

Next gate requires GPT/user approval of the single-frame comparison.
