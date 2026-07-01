# TASK-COMFYUI-UPSCALE-SKILL-REPLAY-20260521 Report

## 1. Final Locked Route

PASS. The mature route is:

1. Official ComfyUI local install.
2. Current ComfyUI Manager enabled with `manager_requirements.txt` and `--enable-manager`.
3. Ultimate SD Upscale installed as a ComfyUI custom node from GitHub with its submodule initialized.
4. Portrait/person local inpaint first, then Ultimate SD Upscale 2x/4K, then Topaz final enhancement manually if available.

The preferred official Windows portable archive was attempted first but GitHub transfer stalled/reset. The route stayed within official ComfyUI sources by switching to official source install with Python venv and official PyTorch CUDA wheel.

## 2. Actual Install Paths

- Task root: `C:\Users\A\Desktop\1\output\TASK-COMFYUI-UPSCALE-SKILL-REPLAY-20260521`
- ComfyUI: `C:\Users\A\Desktop\1\output\TASK-COMFYUI-UPSCALE-SKILL-REPLAY-20260521\ComfyUI`
- Python venv: `C:\Users\A\Desktop\1\output\TASK-COMFYUI-UPSCALE-SKILL-REPLAY-20260521\.venv-comfyui`
- Logs: `C:\Users\A\Desktop\1\output\TASK-COMFYUI-UPSCALE-SKILL-REPLAY-20260521\logs`
- Skill package: `C:\Users\A\.codex\skills\comfyui-inpaint-4k-upscale`
- URL: `http://127.0.0.1:8188`

## 3. Mature Experience Summary

- ComfyUI official README lists local Desktop, Windows Portable, and Manual Install as mature local paths.
- ComfyUI official README says NVIDIA users should install stable PyTorch from the official CUDA wheel index, then install `requirements.txt`.
- Current ComfyUI Manager path is the `comfyui-manager` package from `manager_requirements.txt`, launched with `--enable-manager`.
- The ComfyUI-Manager GitHub README still documents the legacy Git clone method under `ComfyUI/custom_nodes`; this was installed, but current ComfyUI policy blocks the legacy folder while the new v2 Manager endpoints work.
- Ultimate SD Upscale README documents Git clone under `custom_nodes`; its repository includes a submodule, so `git submodule update --init --recursive` is required.
- For portrait/person work, stable practice is local inpaint first, conservative denoise for identity, then tiled 2x Ultimate SD Upscale, then Topaz-style final sharpen/denoise.
- Opaque third-party bundles, version-mixed网盘 packages, and random model-pack installs were not used as the main route.

## 4. Installation And Verification Results

| Item | Status | Evidence |
| --- | --- | --- |
| ComfyUI source install | PASS | Git HEAD `03e511862ee783fec84ef14fe306ee30d4240e2c` |
| Python venv | PASS | Python `3.11.15` |
| PyTorch CUDA | PASS | `torch_version=2.12.0+cu130`, CUDA available, GPU `NVIDIA GeForce RTX 2080 Ti` |
| ComfyUI launch | PASS | `/system_stats` returned 200, ComfyUI `0.22.0` |
| Manager | PASS | `/v2/manager/version` returned `V4.2.1` |
| Ultimate SD Upscale | PASS | `/object_info` includes `UltimateSDUpscale`, `UltimateSDUpscaleCustomSample`, `UltimateSDUpscaleNoUpscale` |
| Topaz | MANUAL | Not installed automatically because Topaz normally requires user licensing/download; kept as final manual enhancement step |
| Base image models | NOT INSTALLED | No large checkpoint/upscale model files found under the new `ComfyUI\models`; use approved/user-supplied models |

## 5. Commands Used

```powershell
git clone --depth 1 https://github.com/Comfy-Org/ComfyUI.git "C:\Users\A\Desktop\1\output\TASK-COMFYUI-UPSCALE-SKILL-REPLAY-20260521\ComfyUI"
& "C:\Users\A\AppData\Roaming\uv\python\cpython-3.11.15-windows-x86_64-none\python.exe" -m venv "C:\Users\A\Desktop\1\output\TASK-COMFYUI-UPSCALE-SKILL-REPLAY-20260521\.venv-comfyui"
& "C:\Users\A\Desktop\1\output\TASK-COMFYUI-UPSCALE-SKILL-REPLAY-20260521\.venv-comfyui\Scripts\python.exe" -m pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu130
& "C:\Users\A\Desktop\1\output\TASK-COMFYUI-UPSCALE-SKILL-REPLAY-20260521\.venv-comfyui\Scripts\python.exe" -m pip install -r requirements.txt
& "C:\Users\A\Desktop\1\output\TASK-COMFYUI-UPSCALE-SKILL-REPLAY-20260521\.venv-comfyui\Scripts\python.exe" -m pip install -r manager_requirements.txt
git clone --depth 1 https://github.com/ltdrdata/ComfyUI-Manager.git "ComfyUI\custom_nodes\ComfyUI-Manager"
git clone --depth 1 https://github.com/ssitu/ComfyUI_UltimateSDUpscale.git "ComfyUI\custom_nodes\ComfyUI_UltimateSDUpscale"
git submodule update --init --recursive
& "C:\Users\A\Desktop\1\output\TASK-COMFYUI-UPSCALE-SKILL-REPLAY-20260521\.venv-comfyui\Scripts\python.exe" main.py --listen 127.0.0.1 --port 8188 --disable-auto-launch --enable-manager
```

## 6. Skill Package Contents

- `SKILL.md`
- `scripts/start-comfyui.ps1`
- `scripts/verify-comfyui.ps1`
- `references/install.md`
- `references/workflow.md`
- `references/parameters.md`
- `references/troubleshooting.md`
- `references/operator-guide.md`
- `references/acceptance.md`
- `references/report.md`

## 7. Current Readiness For Portrait Inpaint + 4K Upscale

PASS for infrastructure and reusable workflow:

- ComfyUI starts locally.
- Manager v2 endpoints work.
- Ultimate SD Upscale nodes are recognized.
- The skill package documents the mature workflow and parameter ranges.

LIMITATION:

- A real image-processing run still needs approved/user-supplied SD/SDXL/inpaint checkpoint and any desired upscale model files. The task deliberately did not install random model sources.
- Topaz remains a manual final enhancement step unless the user provides/installs a licensed Topaz app.

## 8. If Not Fully Complete, Minimum Next Action

For actual user-image processing, the minimum next action is:

1. Put an approved SD/SDXL/inpaint checkpoint under `ComfyUI\models\checkpoints`.
2. Put optional ESRGAN/SwinIR/upscale model under `ComfyUI\models\upscale_models`.
3. Provide the source image path and target edit instruction.
4. Run the workflow described in `references/workflow.md`.

## 9. Evidence Files

- `logs\G03-portable-download-fail.json`
- `logs\G03-comfyui-clone.json`
- `logs\G03-verify-torch-cuda.json`
- `logs\G04-clones.json`
- `logs\G04-usdu-submodule.json`
- `logs\G05-system-stats.json`
- `logs\G05-manager-endpoints.json`
- `logs\G05-object-info-node-scan.json`
- `logs\G06-model-file-scan.json`

## 10. Final Status

FINAL_PASS TASK-COMFYUI-UPSCALE-SKILL-REPLAY-20260521
