# 复现说明

## 冻结合同

Windows 10 build 19045、RTX 2080 Ti 22 GB、ComfyUI 0.9.2、本机 `127.0.0.1:8188`、固定 256×256 黑图、`LoadImage → P0CachedPNGWebsocket`、最低 PNG 完整验证。

## 需要部署的文件

1. 把 `p0_cached_png_websocket.py` 放入 ComfyUI `custom_nodes`。
2. 把 `fixtures/p0-control-black-256.png` 放入 ComfyUI input 目录。
3. 使用 `runtime/START_COMFYUI_C_DRIVE_OUTPUT_D.ps1` 对应的服务配置。
4. 确保 `run.py` 的 `REFERENCE` 指向 `fixtures/reference-output.png` 的同字节文件；原冻结 runner 保留了认证机器绝对路径以维持 SHA，不在归档时改写。
5. 固定工作流见 `workflow/fixed-workflow.json`。

## 运行边界

- `run.py` 是优化期 2 warmup + 5 measured runner。
- `certify.py` 是最终 40-run 认证器；只在 99 重新开启并形成明显更快候选后使用。
- 当前任务已冻结，本次归档不执行任何 benchmark。

复现前先校验 `MANIFEST.json` 与关键 SHA；改变路径、依赖或代码后，不得继续声称是相同冻结二进制。
