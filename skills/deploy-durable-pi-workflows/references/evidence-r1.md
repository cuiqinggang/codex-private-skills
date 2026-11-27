# Windows 三路线首轮证据快照

工作区为 Windows 执行通道 的 `<历史工作区>`。本轮证据目录为 `durable-three-route-reality-r1`。读取 `COMPARISON-FREEZE.json` 及该目录最新回执。原 ECC 两轮留在原目录。Camunda、Azure 和融合方案均未纳入本轮。

| 项目 | 实测事实与定位 |
|---|---|
| Temporal 调度服务重启 | 官方 CLI 1.10.0、服务端 1.32.2、Python SDK 1.36.0。使用持久 SQLite 和官方 greeting/retry 样例。停止原服务 PID 8588，同数据库启动 PID 14000，工作流 `persistent-restart-r1` 的 run ID 保持为 `<RUN_OR_SESSION_ID_10>`。独立读回样例结果正确，00:11.362。回执 `temporal-server-restart-result.json`。适用范围为组件样例。 |
| Temporal 首次真实 Pi 短任务 | 独立产物校验 7/7，原生 goal 在截断前仍 active，缺终态回执。85 秒从宿主启动起算，RPC 建立和启动已消耗约 47 秒；Pi 已写出完整产物，最后一次活动更新距离截止很近。确知测试超时触发停止，未证明 Pi 本来不能完成。保留 `temporal-pi-normal-r1-failure.json`、`temporal/native-runs/*/HOST.json` 和对应日志。该试次无 T_VALID。 |
| 移除限额的中间诊断 | 旧 R61 命令构造器将秒数转整数并强制生成 `--max-time`，直接传入 infinity 导致 `OverflowError`。错误发生于命令构造，和业务任务、脚本授权及模型无关。原日志 `temporal-pi-normal-r2-worker.log`。 |
| Temporal 无测试限额短流程 | 保留原增强 Pi 入口，试验专用适配移除 `--max-time`，本地宿主无总截止，无累计 token 限额；配置将子智能体运行上限置零。用 Temporal Signal 和等待条件接收本机控制器的 Pi 原生终态，避开 Activity 的必填时限。独立 7/7，`NATIVE_GOAL_COMPLETED`，01:18.316。回执 `temporal-pi-normal-uncapped-result.json`，原生记录 `temporal-uncapped/native-runs/*/HOST.json`。本机控制器发起 Pi，调度器持久化等待终态。本次覆盖正常接线与短任务签收，调度器接管派发仍待验证。 |
| Cadence | 官方源码固定 `18bd604dfd6932d0ed1a13a373afe9d89a3ff1c0`。Docker 官方镜像拉取遇 Docker Hub EOF，已重试，并并行使用已取得的官方源码构建。Go 工具链和依赖下载有日志；Python SDK 0.4.1 已拉取。尚无本机完整业务签收。 |
| Conductor | 官方源码固定 `63959259a4f1257b1239e3eed1c9c2152f473a22`。曾尝试不存在的镜像标签，之后使用官方 3.33.0，摘要 `sha256:<EVIDENCE_HASH_05>`，隔离容器 `pi-reality-r1-conductor` 已创建，端口绑定本机回环。须读取最新健康和 API 回执；短流程脚本 `conductor-pi-normal.py` 待实际签收。 |

## 夹具和后续进入点

- 短任务冻结 `frozen-short-input` 的 TASK.md、input.json、rules/SKILL.md 和故意错误的 report.json。统一用既有 `../pi-entry-r61-20261108/pi_r61_test.py` 作独立验收，散列见冻结清单。检查明细、整数金额、任务号、输入哈希、交付回执、检查点和中文摘要。既有短测 00:42.509、旧宿主恢复 01:26.375 均来自不同试次，不能用来排名。
- 复杂 GUI 合同为 `../omp-three-loops-20261029/BROWSER-FROZEN.json`。在本组还原实例实际创建两条业务记录，编辑一条，刷新读回、导出 CSV、验证 XLSX，审计原数据未变及 3 次业务提交和 1 次导出。旧审计脚本含固定端口，迁移前适配独立端口和回执目录，原 4391 实例保持只读。接口验账和真实界面证据分别记录。
- 接续先检查 Conductor 容器和现有派单、Cadence 构建与服务回执、Temporal 原生接续方案。完成三路线第 1 级同口径签收，再按第 2 至 5 级扩展。共用超时修正不得用于回填旧轮通过。当前缺三路线完整可比结果及故障与 GUI 全覆盖。
