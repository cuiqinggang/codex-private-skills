# 增强 Pi 直接接单与恢复

以下命令适用于旧的隔离启动器及原任务核查。新任务如选择 Temporal，按 [原生 CLI 直投](temporal-native-submit.md)派发。

```bat
Open-Pi.cmd --durable-longflow approve "C:\path\to\job"
Open-Pi.cmd --durable-longflow run "C:\path\to\job"
Open-Pi.cmd --durable-longflow status "C:\path\to\job"
Open-Pi.cmd --durable-longflow resume "C:\path\to\job"
```

每个任务使用唯一目录和固定任务号。`request.json` 包含 `task_id`、`entrypoint`（成熟配方的参数数组）、`cwd`（本任务目录内的工作目录）、`receipt`（相对工作目录）。子执行程序完成后，用独立业务验收器原子写出 JSON，字段为 `task_id`、`status: PASS` 及 `artifacts`。每个产物包含相对工作目录的 `path` 和 `sha256`。首次在可信 Windows 宿主登记这份冻结请求，绑定请求、程序和显式脚本的 SHA-256。后续运行和接回无需重复登记，变更请求须使用独立任务身份。冻结任务后保持请求字节、配方与输入；Pi 自行声明完成不足以签收。

旧隔离配方使用 10 秒心跳失联检测、最多两次尝试和 24 小时 Activity 接口边界。R162 在真实安装、部署与构建中证实这一心跳预算会超时，正式长测按实测负载和冻结接续合同选用参数。调度端同一任务保持相同 Workflow ID 和 Run ID，接续使用原目录与 `temporal.sqlite`。保留 `DISPATCH.json`、`STATUS.json`、独立验收回执和 `ACTIVITY-COMMITTED.json`。已核验交付的接管只读原回执及产物指纹。状态查询显示最近原生读回。

未交付任务仅在业务配方本身支持恢复时设置 `resume_entrypoint` 与 `resume_preflight`，两者均为固定参数数组。独立只读预检证明旧执行器已退出、原任务原会话已定位、所有此前写入已对账后，输出带有 `status: RESUME_SAFE`、`task_id`、`request_sha256`、`checkpoint`、`checkpoint_sha256`、`session_id` 的 JSON。恢复命令接收 `DURABLE_PI_RESUME_SESSION_ID` 和 `DURABLE_PI_RESUME_CHECKPOINT`，按原配方接续。没有可信回执或核账证据时停止重放。

本机使用已验证的 Temporal CLI/Server 与 Python SDK。当前 CLI 路径与 SDK 路径在脚本中明确列出，迁移时先验证这些依赖。Worker 与服务故障、Windows 启动后接回原目录、真实用户界面签收各自独立验收。`resume` 可从用户入口接回原任务，登录恢复程序调用 `resume-pending`。实际 Windows 注册、登录触发和原 Run 接回各用本机回执确认。

2026-11-13 原预约故障：派发历史心跳超时为 0、最后一次心跳为空、尝试 1/1。预约正常封装未接入已验的心跳和接管机制。原历史回执在 Windows 工作区 `pi-comprehensive-20261113/TEMPORAL-BOOKING-ACTIVITY-AUDIT.json`。R83 双进程受控退出后重开同一数据库，同 Run 7/7，Pi 业务只运行一次，恢复 9.785 秒。该轮使用独立短任务和受控故障。
