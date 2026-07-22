# Recovery

Use this when the existing ComfyUI-aki-v3 video baseline does not behave as expected. Recovery must stay narrow: no new models, no ComfyUI core upgrade, no broad node installation.

## First Rule

Do not reinstall. Check the current baseline first:

```powershell
${REDACTED_SECRET}
```

## Service Not Reachable

Check HTTP:

```powershell
curl.exe --max-time 5 -s -o NUL -w "%{http_code} %{size_download}`n" http://127.0.0.1:8188/
```

If the service is not running, start it:

```powershell
C:\AI\ComfyUI_Aaki_v3\START_COMFYUI_C_DRIVE_OUTPUT_D.bat
```

Then open Chrome:

```powershell
Start-Process -FilePath 'C:\Program Files\Google\Chrome\Application\chrome.exe' -ArgumentList @('--new-window','http://127.0.0.1:8188')
```

## CUDA Or GPU Not Visible

Run:

```powershell
nvidia-smi
C:\AI\ComfyUI_Aaki_v3\python\python.exe -c "import torch; print(torch.__version__, torch.version.cuda, torch.cuda.is_available(), torch.cuda.get_device_name(0) if torch.cuda.is_available() else None)"
```

Expected:

- GPU: RTX 2080 Ti
- torch: `2.9.1+cu130`
- CUDA available: `True`

If CUDA is false, stop and report. Do not change torch or reinstall dependencies as a daily recovery step.

## Model Missing

Required files:

```text
C:\AI\ComfyUI_Aaki_v3\ComfyUI\models\diffusion_models\wan2.2_ti2v_5B_fp16.safetensors
C:\AI\ComfyUI_Aaki_v3\ComfyUI\models\text_encoders\umt5_xxl_fp8_e4m3fn_scaled.safetensors
C:\AI\ComfyUI_Aaki_v3\ComfyUI\models\vae\wan2.2_vae.safetensors
```

If any file is missing, stop and report the missing file. Do not install a substitute model.

## Workflow Missing

Pinned workflow:

```text
${REDACTED_SECRET}
```

Pinned API prompt:

```text
${REDACTED_SECRET}
```

If either file is missing, restore it from the second-stage output directory:

```text
${REDACTED_SECRET}
```

## Queue Stuck

Check:

```powershell
curl.exe --max-time 10 -s http://127.0.0.1:8188/queue
nvidia-smi
```

If GPU utilization and CPU usage are changing, wait. The first successful 512x512 run took `1783.136` seconds.

If there is no progress for a long period and you choose to abort, use the UI queue controls first. Restart ComfyUI only after confirming no output is being written.

## Out Of Memory

Only reduce within Wan2.2-TI2V-5B:

- lower frames
- lower resolution
- lower steps
- keep CLIP on CPU

Do not switch to 14B, S2V, LTX, FramePack, or a model bundle.

## Output Missing

Check raw output:

```powershell
Get-ChildItem 'D:\AI_ComfyUI_Outputs\ComfyUI_Aaki_v3\output\video' -File | Sort-Object LastWriteTime -Descending | Select-Object -First 10 FullName,Length,LastWriteTime
```

Then copy selected clips manually to:

```text
D:\AI_ComfyUI_Outputs\ComfyUI_Aaki_v3\output\video_selected
D:\AI_ComfyUI_Outputs\ComfyUI_Aaki_v3\output\remotion_inbox
```
