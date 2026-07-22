---
name: stable-diffusion-image-generation
description: Use when this Windows Codex studio needs Stable Diffusion image generation planning, ComfyUI/Diffusers workflow review, local GPU versus cloud GPU route selection, model/checkpoint safety review, or image-generation pipeline troubleshooting. Prefer existing local ComfyUI skills when the task is specifically ComfyUI inpainting or 4K upscale.
---

# Stable Diffusion Image Generation Windows Studio

Use this skill for image generation route selection and troubleshooting on Windows.

## Route Priority

1. Existing local ComfyUI workflow, especially for portrait inpainting and upscale tasks.
2. Local Diffusers or Python workflow if already present and task-specific.
3. Cloud GPU only after cost, credential, and data boundaries are explicit.
4. New model/tool install only when necessary and from trusted sources.

## Safety Rules

- Do not download unknown checkpoints or run unknown nodes/scripts without review.
- Do not expose private images, keys, or account data.
- Stop before cloud spend, account login, model marketplace purchase, or broad system install.
- Keep generated outputs under an explicit project/output directory.

## Workflow

1. Define target: style, resolution, input image, inpainting/upscale/text-to-image, output format.
2. Check existing local workflow and GPU availability before adding tools.
3. Pick the smallest viable pipeline.
4. For ComfyUI, verify workflow file, models, custom nodes, and output path.
5. Run a small smoke generation before expensive upscale or batch work.
6. Report seed/settings, output path, and PASS/FAIL evidence.

## Verification

- PASS: small output renders, required models are found, and path/settings are recorded.
- FAIL: missing model, unsafe node/checkpoint, GPU/cloud ambiguity, or no output evidence.

