# 双路执行策略 v0.2.0

## 目标

默认选择能达到 VALID 的最短现实路径，并保留第二条独立执行路由作为故障降级。

```text
主路：ChatGPT → Desktop Commander Remote → Windows
备路：ChatGPT/GitHub → GitHub Actions → Windows self-hosted runner
```

## 主路：Desktop Commander Remote

进入条件：
- 目标设备在 Desktop Commander 中为 Online；
- Remote 能访问目标路径或对应本机能力；
- 操作不超出安全/权限边界；
- 本轮任务不要求离线排队、跨会话持续或 GitHub Actions 证据链。

已 Reality 验证：
- 设备发现与在线状态：PASS；
- Downloads 目录读取与文件元数据读取：PASS；
- 本地文件创建/回读/清理：PASS；
- 本机进程/命令执行：PASS；
- Git 仓库只读命令：PASS。

默认规则：
- 满足进入条件时直接使用 Remote；
- 不先启动 GitHub runner；
- 不为已能直连完成的任务增加任务 JSON、workflow、artifact 或其他中转层。

## 备路：GitHub Actions + self-hosted runner

适用条件：
- Desktop Commander Remote 离线、不可达或能力不覆盖；
- 任务需要排队执行、GitHub 工作流证据链或与当前聊天解耦执行；
- Windows runner 在线。

Reality：
- ETAL-BRIDGE-SMOKE-001：PASS；
- 最新 Run ID：36917244551；
- 最新 artifact ID：11189839827；
- `windows-reality`、任务执行、artifact 上传：全部 success；
- 用户执行中介入=0。

当前持久化条件：
- 安装目录：C:\actions-runner-etal；
- runner 名：DESKTOP-4A1EGTM-etal；
- 计划任务：ETAL-GitHub-Actions-Runner；
- 模式：当前用户登录时自动启动并持续运行；
- runner GitHub 状态必须为 online；
- `windows-reality` 必须注入 `core.longpaths=true`，否则大型仓库 checkout 可能因 Filename too long 失败；
- Windows Service 是可选增强，不是备路可用的必要条件。

## 自动路由

```text
1. Remote Online + 能力覆盖 → 主路直连。
2. Remote 不满足 → 检查 GitHub runner。
3. runner online → 备路。
4. 两路都不可用 → 明确返回阻塞原因；不得伪装成功。
```

## 不变安全边界

- 不修改 FlClash。
- 不修改 Windows 网络代理。
- 不执行 Windows 系统破坏性动作。
- 失败结果原样记录。
- 不因为“有备路”而重复执行同一现实副作用任务。

## 防止下次失效的最小健康检查

主路：
- list_devices 显示目标设备 Online；
- ping 成功；
- 目标路径可访问。

备路：
- `ETAL-GitHub-Actions-Runner` 计划任务存在；
- GitHub API `runner.status=online`；
- labels 至少包含 `self-hosted,Windows,X64`；
- workflow 的 `windows-reality` job 保留 `core.longpaths=true` 注入；
- 若升级为 Windows Service，再额外要求 service=Running、StartMode=Auto。

只有健康检查通过的路由才进入正式执行。
