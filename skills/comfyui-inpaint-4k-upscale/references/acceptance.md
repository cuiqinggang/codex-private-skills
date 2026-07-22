# Acceptance Checks

Run these before reporting the environment ready.

## G01 Server

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8188/system_stats" -TimeoutSec 10
```

PASS:

- HTTP 200
- response contains `comfyui_version`
- response lists CUDA device

FAIL:

- connection refused
- no CUDA device when GPU mode is expected
- Python traceback in server log

## G02 Manager

```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:8188/v2/manager/version" -TimeoutSec 10 -UseBasicParsing
```

PASS:

- HTTP 200
- content contains a Manager version, for example `V4.2.1`

FAIL:

- 404
- startup log says `--enable-manager` dependency is missing

## G03 Ultimate SD Upscale

```powershell
$obj = Invoke-RestMethod -Uri "http://127.0.0.1:8188/object_info" -TimeoutSec 30
$obj.PSObject.Properties.Name -contains "UltimateSDUpscale"
```

PASS:

- command returns `True`
- startup log shows `USDU batch patches applied successfully`

FAIL:

- node is absent
- import failure or missing submodule is in server logs

## G04 Report

PASS:

- `references/report.md` exists in this skill.
- final task report exists under the task output directory.
- report lists PASS/FAIL, paths, failures, and next minimum action.
