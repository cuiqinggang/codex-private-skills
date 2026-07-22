# Phase 1 Install Gates

Use these gates only when the base install must be reproduced or audited.

## G01 Source Gate

Allowed source: 秋葉aaaki official Bilibili video `BV1Ew411776J` and the official Quark entry it points to.

Allowed archive:

`H:\ComfyUi\ComfyUI-aki(1)\ComfyUI-aki-v3.7z`

Do not use:

- `ComfyUI-aki-v2.7z`
- V9.5
- third-party repacks
- fan bundles
- unknown "full" packages

## G02 Archive Gate

Record size and SHA256. Known verified values:

- Size: `2634775597` bytes
- SHA256: `82D549D5FA0393CC064EA858397CCC7DC63803B4F32C0B484BD115E1EFD81C83`
${REDACTED_SECRET}

If password test fails, stop. Do not guess another password.

## G03 Extract Gate

Extract to:

`C:\AI\ComfyUI_Aaki_v3`

Do not overwrite an existing working install without a separate backup and explicit user instruction.

## G04 Launch Gate

Preferred no-click launch:

```powershell
C:\AI\ComfyUI_Aaki_v3\START_COMFYUI_C_DRIVE_OUTPUT_D.bat
```

Open in Google Chrome:

```powershell
Start-Process -FilePath 'C:\Program Files\Google\Chrome\Application\chrome.exe' -ArgumentList @('--new-window','http://127.0.0.1:8188')
```

Verify:

- `curl.exe --max-time 5 -s -o NUL -w "%{http_code} %{size_download}\n" http://127.0.0.1:8188/`
- `curl.exe --max-time 5 -s http://127.0.0.1:8188/system_stats`

## G05 CUDA Gate

Use embedded Python:

```powershell
C:\AI\ComfyUI_Aaki_v3\python\python.exe -c "import torch; print(torch.__version__, torch.version.cuda, torch.cuda.is_available(), torch.cuda.get_device_name(0), torch.cuda.get_device_capability(0))"
```

Expected baseline:

- Python `3.13.11`
- torch `2.9.1+cu130`
- CUDA available: `True`
- GPU: `NVIDIA GeForce RTX 2080 Ti`
- capability: `(7, 5)`
