# Install Notes

## Locked Mature Route

Primary route selected for this machine:

1. Prefer official ComfyUI Windows Portable when the GitHub large archive is downloadable.
2. If the portable archive stalls/resets, use the official source install path:
   - `git clone https://github.com/Comfy-Org/ComfyUI.git`
   - Python 3.11 venv
   - official PyTorch CUDA wheel
   - `pip install -r requirements.txt`
3. Enable current ComfyUI Manager with:
   - `pip install -r manager_requirements.txt`
   - launch with `--enable-manager`
4. Install Ultimate SD Upscale under `ComfyUI/custom_nodes`:
   - `git clone https://github.com/ssitu/ComfyUI_UltimateSDUpscale.git`
   - `git submodule update --init --recursive`

## Installed Paths

- Task root: `C:\Users\A\Desktop\1\output\TASK-COMFYUI-UPSCALE-SKILL-REPLAY-20260521`
- ComfyUI: `C:\Users\A\Desktop\1\output\TASK-COMFYUI-UPSCALE-SKILL-REPLAY-20260521\ComfyUI`
- Venv: `C:\Users\A\Desktop\1\output\TASK-COMFYUI-UPSCALE-SKILL-REPLAY-20260521\.venv-comfyui`
- Logs: `C:\Users\A\Desktop\1\output\TASK-COMFYUI-UPSCALE-SKILL-REPLAY-20260521\logs`
- ComfyUI-Manager package: `comfyui-manager==4.2.1`
- Ultimate SD Upscale custom node: `ComfyUI\custom_nodes\ComfyUI_UltimateSDUpscale`

## Main Commands

```powershell
$Root = "C:\Users\A\Desktop\1\output\TASK-COMFYUI-UPSCALE-SKILL-REPLAY-20260521"
$Comfy = Join-Path $Root "ComfyUI"
$Python = Join-Path $Root ".venv-comfyui\Scripts\python.exe"
Set-Location $Comfy
& $Python main.py --listen 127.0.0.1 --port 8188 --disable-auto-launch --enable-manager
```

## Mature Sources Used

- ComfyUI official GitHub/README: desktop app, Windows portable, and manual install are the official local paths.
- ComfyUI README: NVIDIA users install PyTorch with the official CUDA wheel index and then install `requirements.txt`.
- ComfyUI README: current Manager feature requires `manager_requirements.txt` and `--enable-manager`.
- ComfyUI-Manager README: mature extension method is a Git clone under `ComfyUI/custom_nodes`.
- ComfyUI_UltimateSDUpscale README: mature installation is Git clone under `custom_nodes`; the node appears under `image/upscaling`.

## Known Install Deviation

The official `ComfyUI_windows_portable_nvidia_cu126.7z` archive download was attempted first. GitHub transfer repeatedly reset/stalled after partial download, so the task switched to the official source install path instead of using a third-party package.
