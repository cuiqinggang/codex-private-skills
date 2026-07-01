# Recommended Workflow

## Stable Mainline

1. Import the user's original image.
2. Create a precise mask for the local repair area.
3. Use inpaint/img2img only on the masked region.
4. Avoid masking the face, eyes, mouth, hands, clothing logos/patterns, and body outline unless they are the actual defect.
5. Decode and inspect the repaired image at original resolution.
6. Run Ultimate SD Upscale with 2x scale and conservative denoise.
7. Export the 4K target or nearest target size.
8. Use Topaz Photo AI/Gigapixel manually for final denoise, sharpen, face recovery, and export polish when available.

## ComfyUI Node Chain

Use a common SD/SDXL inpaint graph structure:

```text
Load Image
Mask Editor / Load Mask
Checkpoint Loader
CLIP Text Encode positive
CLIP Text Encode negative
VAE Encode For Inpaint
KSampler
VAE Decode
Preview/Save Image
UltimateSDUpscale
Save Image
Topaz final pass outside ComfyUI
```

For a portrait/person image, the prompt should describe only the intended repair and preservation target. Do not rewrite the whole person if the goal is local repair.

## Image Consistency Rules

- Preserve the original face and core body silhouette.
- Keep denoise lower for identity-critical edits.
- Use a soft mask edge; feather enough to hide seams but not so much that the face or clothing is affected.
- Repair background, hair tips, flower fields, tails, props, and edge artifacts before global upscale.
- Inspect the image after inpaint before upscaling; do not upscale a broken face or warped hands.

## 4K Upscale Strategy

- Prefer one clean 2x pass first.
- Use Ultimate SD Upscale tiles to avoid VRAM spikes.
- For a typical 1024-2048px source, 2x often reaches or approaches 4K on one side.
- If the image is small, use a preliminary non-diffusion upscale or resize step, then one Ultimate SD Upscale pass.
- Avoid direct 8K unless the source is already high quality, the subject identity is stable, and VRAM/time budget is acceptable.

## Topaz Position

Topaz is the final enhancement stage, not the repair stage. Use it after ComfyUI output for:

- mild sharpening
- denoise
- face recovery when it improves identity
- final resize/export polish

If Topaz is not licensed or not installed, do not fail the ComfyUI workflow. Record it as a manual finishing step.
