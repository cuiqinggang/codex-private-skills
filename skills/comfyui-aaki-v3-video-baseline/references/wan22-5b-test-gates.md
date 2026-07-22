# Wan2.2-TI2V-5B Test Gates

## G01 Freeze Baseline

Run:

```powershell
${REDACTED_SECRET}
```

This creates `G01_BASELINE_FROZEN` with install path, launch command, CUDA info, custom node list, model tree, and key small configs.

## G02 Source Check

Allowed sources:

- Official ComfyUI docs/example/template pages
- Hugging Face official `Comfy-Org` pages
- Hugging Face official `Wan-AI` pages
- ModelScope official pages

Required files only:

- `wan2.2_ti2v_5B_fp16.safetensors`
- `umt5_xxl_fp8_e4m3fn_scaled.safetensors`
- `wan2.2_vae.safetensors`

Stop if a file is unavailable or requires switching to third-party mirrors.

## G03 Model Placement

Target paths:

```text
C:\AI\ComfyUI_Aaki_v3\ComfyUI\models\diffusion_models\wan2.2_ti2v_5B_fp16.safetensors
C:\AI\ComfyUI_Aaki_v3\ComfyUI\models\text_encoders\umt5_xxl_fp8_e4m3fn_scaled.safetensors
C:\AI\ComfyUI_Aaki_v3\ComfyUI\models\vae\wan2.2_vae.safetensors
```

Create directories if missing. Do not place unrelated files.

## G04 Workflow Gate

Use the official ComfyUI Wan2.2 5B template/workflow.

Before queuing:

- verify missing nodes are zero
- verify model names match the three target files
- set low-risk parameters

Suggested first test:

- text-to-video or image-to-video; T2V is acceptable when no suitable input image exists
- width/height about `512x512`
- frames `36-48`
- fps `12-16`
- one generation only
- offload/low memory enabled where the official workflow exposes it

## G05 Run Gate

Queue exactly one low-risk test. Record:

- queued prompt id
- start/end time
- elapsed seconds
- nvidia-smi samples
- output video path
- saved workflow path

If OOM occurs, retry once with lower frame count/resolution/duration. If that fails, stop and report.
