# R169 定点复验与三路长测

2026-11-16，北京时间。沿用 R162 冻结合同和 R110/R144/R130/R84/R159 的已验配方。R162 旧 Run 及其回执保留原生终态。

| 关口 | 已验结果 | 原始证据 |
| --- | --- | --- |
| Temporal 隔离部署 | 按原 Compose 核对容器、卷、端口与只读 `stream.conf` 的指纹。恢复原项目的 MySQL、MinIO、中继三容器，读回 MySQL 协议握手以及 MinIO 就绪 HTTP 200。 | `R162/r162-temporal-service` 对应原项目。关联核验保留历史缺失的部署回执。 |
| Temporal 心跳与恢复 | 按 R130 回放，候选 Activity 心跳超时 30 秒，SDK 心跳节流上限 2 秒。读到间隔约 2 秒的两次服务端心跳。已有安装回执后停止 Worker，替补在原 Run 继续，Activity 尝试 `[2, 1]`，终态 `COMPLETED`，安装产物唯一且 SHA-256 一致。 | `R162/r169-temporal-heartbeat/RESULT.json`，Run `<RUN_OR_SESSION_ID_16>`。 |
| Temporal 取消进程 | 按 R84 进程归属检查核对父子进程。活动取消后，隔离复验的受控 Windows 父进程和子进程均退出。 | `R162/r169-temporal-cancel-tree/RESULT.json`。 |
| Conductor 应用健康 | 按 R144 先恢复原隔离依赖和中继，再启动 R3 已构建应用。Louez 健康接口 HTTP 200，启动到健康 `00:16:790`。预约前后均为 0，八个原证据文件指纹一致，旧原生工作流维持 `TIMED_OUT`。 | `R162/r169-conductor-r3-readiness/READINESS-RESULT.json`。 |
| Conductor 提交端可达 | 按 R159 由宿主核对容器身份、当前绑定和健康，再将冻结的回环端点交给实际增强 Pi；同上下文健康读回通过，六个非法端点被拒绝。本次完成只读探测。 | `R162/r169-conductor-worker-endpoint/ACTUAL-PI-READBACK.json`，及同目录 `VIRTUAL-AND-HOST-RESULT.json`。 |

三类证据须各自使用。心跳候选和进程取消分别在隔离回放验证，真实 Louez 构建负载、部署原子回执、故障接管、可见 GUI 和独立签收仍须逐轮取证。本次 Windows 登录启动失败发生在 WSL 预热，随后以原入口手工恢复，Docker 引擎健康。再次实际登录的自启动结果另行记录。

## 原合同三路隔离对照

- 同时派发 Temporal、Conductor，以及在所选同一调度器启用 Superpowers 的对照组。第三路保持对应基线的调度器、输入、负载和验收条件一致，记录实际加载的 Superpowers 版本、宿主和证据。Windows Claude Code 已启用 5.1.0；Codex 有上游技能副本；增强 Pi 实际加载须现场读回。原版 Pi 上游支持不作为增强 Pi 验收。当前上游版本见 [Superpowers v7.0.2](https://github.com/obra/superpowers/releases/tag/v7.0.2)。
- 统一 Louez G00–G12、账本和备份还原合同。各路独立任务号、目录、数据库、卷、端口、原生队列或调度实例、浏览器会话与文件路径；同机并行记录资源争用。发现共享写入或故障范围重叠时暂停受影响的轮次，独立轮次继续。
- 每路先签收正常轮，再按冻结的同一业务边界验证 Worker 中断、调度重启和写后丢回执。用相同独立验收器核对真实 GUI、原生 Run 和账本唯一写入。从正式接单计到独立签收，等待、恢复、返工和裁决均计入 `T_VALID`。只有同质量、同场景且已签收的时间进入对照表。

原始证据索引与 R162 冻结回执（原始链接内部留存）
