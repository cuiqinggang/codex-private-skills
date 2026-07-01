# Failure Points And Recovery

## Portable Download Stalls

Symptom: GitHub `.7z` download resets or stalls for a long time.

Recovery:

1. Stop only the stuck download process.
2. Keep the partial archive only as evidence; do not build on it.
3. Switch to official source install with Python venv and official PyTorch wheel.
4. Do not switch to opaque third-party bundles as the main install route.

## ComfyUI Does Not Start With Manager

Symptom:

```text
To use the --enable-manager feature, the comfyui-manager package must be installed first.
```

Recovery:

```powershell
$Root = "C:\Users\A\Desktop\1\output\TASK-COMFYUI-UPSCALE-SKILL-REPLAY-20260521"
$Python = Join-Path $Root ".venv-comfyui\Scripts\python.exe"
$Comfy = Join-Path $Root "ComfyUI"
Set-Location $Comfy
& $Python -m pip install -r manager_requirements.txt
```

## Ultimate SD Upscale Missing

Symptom: `/object_info` does not include `UltimateSDUpscale`.

Recovery:

```powershell
$Node = "C:\Users\A\Desktop\1\output\TASK-COMFYUI-UPSCALE-SKILL-REPLAY-20260521\ComfyUI\custom_nodes\ComfyUI_UltimateSDUpscale"
Set-Location $Node
git submodule update --init --recursive
```

Then restart ComfyUI and verify `/object_info` again.

## Manager Legacy Folder Blocked By Policy

Current ComfyUI Manager is provided by the `comfyui-manager` pip package and enabled with `--enable-manager`. A cloned legacy `custom_nodes\ComfyUI-Manager` folder can be reported as blocked by policy in logs while the v2 Manager endpoints still work.

Treat Manager as PASS when:

- `pip show comfyui-manager` returns a version.
- startup logs show `[START] ComfyUI-Manager`.
- `GET /v2/manager/version` returns 200.

## Missing Models

The install task does not download random checkpoints or opaque model packs. If image generation/upscale cannot run a real workflow, install or provide approved SD/SDXL/inpaint checkpoints, VAE, LoRA, and optional upscale model files in the appropriate `ComfyUI\models\...` directories.

## Topaz Not Available

Topaz requires normal user installation/licensing. If unavailable, complete ComfyUI repair/upscale and record Topaz as a manual final enhancement step.
