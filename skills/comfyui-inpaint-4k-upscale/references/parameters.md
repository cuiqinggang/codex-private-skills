# Recommended Parameters

## Inpaint Denoise

- Tiny cleanup, color, small edge fixes: `0.15-0.30`
- Hair tips, minor tail/flower/background repair: `0.25-0.45`
- Medium object/background replacement away from face: `0.40-0.60`
- Large area replacement: `0.55-0.70`
- Avoid going above `0.70` for portraits unless identity change is acceptable.

## Masking

- Feather/blur mask edges enough to hide seams: usually `8-32px` depending on image size.
- Keep mask away from face, eyes, mouth, hands, and clothing identity unless those are the defect.
- For hair or translucent edges, mask slightly outside the visible defect and use lower denoise.

## Ultimate SD Upscale

- Scale: start with `2x`.
- Tile size: `512-768` for conservative VRAM use; `768-1024` when VRAM is comfortable.
- Overlap: `48-96`; use `96-128` for detailed hair, fabric, flowers, or visible tile seams.
- Denoise: `0.18-0.35` for identity preservation; `0.35-0.45` only for stronger texture redraw.
- CFG: keep moderate; avoid aggressive prompt pressure during upscale.
- Steps: use the same practical range as the base workflow; do not over-increase steps just because output is large.

## 4K Guidance

- Target 4K by matching the final long edge or exact output canvas required by the user.
- Use one 2x pass before considering a second pass.
- Do not directly push 8K when the source has face/hand errors, low resolution, compression artifacts, or weak clothing detail.
- If 8K is required, first validate face/clothing at 4K, then run a low-denoise second pass or Topaz resize.

## Keeping Faces And Clothing Stable

- Use lower denoise for face-adjacent masks.
- Avoid masking the entire head for hair-only edits.
- Use negative prompts for extra limbs, distorted eyes, melted hands, changed outfit, logo changes, and face identity drift.
- Compare before/after at 100% and fit-to-screen views.
- Reject outputs where the face shape, eye spacing, mouth, hairstyle silhouette, outfit pattern, or body contour changes unintentionally.
