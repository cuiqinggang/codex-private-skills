# Handling A User Image

## Minimal Operator Flow

1. Save or place the user's image under a task-specific folder.
2. Start ComfyUI with `scripts/start-comfyui.ps1`.
3. Open `http://127.0.0.1:8188`.
4. Load the image into the workflow.
5. Mask only the defect or local edit area.
6. Run a low/medium denoise inpaint pass.
7. Inspect identity and edges.
8. Run Ultimate SD Upscale at 2x with tile overlap.
9. Save the 4K output.
10. If available, open the result in Topaz for final denoise/sharpen/export.

## What To Ask The User

Ask only for the missing artifact or decision that blocks execution:

- the source image path
- the exact local edit request
- preferred final size/aspect ratio if not obvious
- whether a specific checkpoint/model must be used

Do not make the user choose between many plugin or install routes; the route is locked.

## Output Naming

Use stable names:

- `input-original.ext`
- `inpaint-v01.png`
- `upscale-2x-4k-v01.png`
- `topaz-final-v01.png`

Keep failed attempts in the task output folder with a short reason in the report.
