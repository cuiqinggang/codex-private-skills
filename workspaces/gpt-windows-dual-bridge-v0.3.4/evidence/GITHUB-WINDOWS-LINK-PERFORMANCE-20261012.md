# GPT 直连 Windows 双路执行桥 v0.3.4｜GitHub → Windows 实测记录

日期：2026-10-12（北京时间）。性质：真实 GitHub Actions / Windows 自托管 Runner 验证，不是模拟测试。

## 目标与边界

验证现有 GitHub → Windows 本机路径的连通性、完成能力、耗时及故障点。
保持 FlClash、Windows 网络代理、浏览器及业务任务不变。
不修改既有 `extreme-time-windows-bridge.yml` 生产工作流。

## 证据 A：原工作流业务连通测试 FAIL

- 工作流：`Extreme Time Windows Autonomous Bridge`
- Run：38264768349
- 地址：https://github.com/cuiqinggang/codex-private-skills/actions/runs/38264768349
- Windows job：114864140204（`windows-reality`）
- 自托管 Runner：`DESKTOP-4A1EGTM-etal`，版本 2.337.0，主机 `DESKTOP-4A1EGTM`
- 云端 `contract-static`：PASS。
- `windows-reality`：FAIL，于 Set up job 阶段，未执行 payload。
- 日志：尝试下载 `https://codeload.github.com/actions/upload-artifact/zip/ea165f8d65b6e75b540449e92b4886f43607fa02`；连续三次因 HttpClient.Timeout 100 秒到期而失败。工作流 2026-10-12 14:41:35 UTC 创建，14:48:34 UTC 完结，约 419 秒。
- 结论：Runner 确已接单，但启动前外部 Action 下载阻断了本地任务执行。

## 证据 B：零外部 Action、本机及网络诊断 PASS

- Run：38266156278
- 地址：https://github.com/cuiqinggang/codex-private-skills/actions/runs/38266156278
- Commit：01f31d7794179bd0aa29751b571d9e4616b7aa63
- `windows-direct`：PASS，真实运行本机 PowerShell，`BRIDGE_V034_SMOKE_COMPLETED_PASS`。
- 2026-10-12 14:53:06 UTC 创建，14:56:35 UTC 完结；总计 209 秒。
- 本地代码 Stopwatch：`LOCAL_PROBE_MS=107457`（107.457 秒，包括日志/环境检查/网络探测）。
- `api.github.com`：HTTP 200，3511 ms（HEAD）。
- `github.com`：HTTP 200，4450 ms（HEAD）。
- `codeload.github.com/.../upload-artifact/zip/...`：HTTP 200，1151 ms（HEAD）。
- 本地 Polsia V5 目录存在：True。
- Runner 的 PATH 中 `codex` 命令未检出：False。不能据此断言 Codex 未安装。
- 说明：HEAD 成功不等于大 ZIP 下载成功。此结果说明网络具有可达性，但表现可能波动；单次样本不可得出稳定性结论。

## 证据 C：最小本地计算基准 PASS

- Run：38266827018
- 地址：https://github.com/cuiqinggang/codex-private-skills/actions/runs/38266827018
- Commit：fa39778225844989af22ea6b765176f59435e228
- 本机 `pwsh` 真实执行：`BRIDGE_V034_MINIMAL_PASS`。
- 对 100000 次循环进行带校验求和（期望 4999950000）：计算 PASS。
- `COMPUTE_MS=776.216`（0.776 秒）。
- 14:58:40 UTC 创建，14:59:07 UTC 完结；整个 GitHub 工作流约 27 秒。
- 流程不包含 checkout / upload-artifact，也不主动请求 GitHub 网络地址。

## 结论

1. GitHub → Windows 自托管 Runner 的基本接单和执行链路真实可用（两次独立 PASS）。
2. 原业务工作流当前未通过端到端执行：外部 `actions/upload-artifact@v4` 下载三次超时导致失败。
3. 本机短计算速度不是此次瓶颈。GitHub 调度、日志、网络请求与外部 Action 下载导致明显变动：最小 27 秒；网络诊断 209 秒；业务故障 419 秒。
4. 这套链路适合异步批量、备援或中长任务，不宜在修复前当成稳定的低延迟逐条交互路径。稳定性仍需复验，禁止承诺固定时延。
5. `GPT_Windows_MCP_Bridge` 本次调用报内部错误 / session terminated。另一条 Desktop Commander 设备在线但账号提示月度使用额度到限；这是两种独立连接的状态，不能用 GitHub PASS 代替它们。
6. 建议先隔离原工作流的 Action 下载依赖，将轻量任务分流到无第三方 Action 的执行模板。对于需要文件工件的任务，保留现有工作流或另行设计经过现实验证的取证上传方式，禁止未测试就删除功能。

## 本次新增的仓库文件

- `.github/workflows/windows-github-bridge-v034-smoke.yml`：轻量测试工作流（最终为单次计算版本）。
- 本报告：`workspaces/gpt-windows-dual-bridge-v0.3.4/evidence/GITHUB-WINDOWS-LINK-PERFORMANCE-20261012.md`。

没有修改代理、FlClash、现有生产工作流，也没有启动或关闭浏览器。
