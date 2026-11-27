# 上游路线与适配边界

| 路线 | 复用入口 | 应用到本任务的边界 |
|---|---|---|
| Temporal OSS | MIT 服务端。使用官方 CLI、Python SDK、持久化工作流历史、Activity、Signal 或等待条件 | 代码定义工作流。官方开发服务与 SQLite 可用于本机小规模持久化试验。业务写入和 Pi 会话由共同执行层核账。真实 Pi 短任务已通过 Activity 直返。短试中的 Worker 与服务恢复证据见 evidence-r73.md。 |
| Uber Cadence | Apache 2.0 服务端。使用官方部署样例与 Go 或 Python SDK，Windows Python 3.13 可使用已取到的 Python SDK 0.4.1 | 代码定义工作流。按官方版本确认部署和 gRPC 兼容，使用独立域与任务队列。保留原工作流历史及持久卷。SQLite 方案和 PostgreSQL 方案的实测分别留账。 |
| Conductor OSS | Apache 2.0 项目。使用自托管服务器、声明式工作流、外部工作器任务轮询与状态回传 | 任务定义走 API 或上游 SDK。固定工作流 ID、task ID、业务键和回执对应关系。自带 SQLite 用于起步，生产级存储选择按官方部署条件冻结。 |
| Agent-Autoloop | 固定 v1.8.2，官方命令插件、隔离本机 Hub/Worker、原轮次持久状态 | 命令成功后输出明确回执。重试前核对原业务产物并沿既有轮次回传。 |

Temporal 与 Cadence 有项目渊源，Cadence 源自 Uber。Conductor 源自 Netflix，现对照用 conductor-oss 上游。各路线固定维护来源、镜像摘要或源码提交和依赖版本。自托管不要求购买托管许可，机器、存储和维护仍有成本。公开采用案例或许可只能支撑组件选型，本机原会话接续、写入唯一、GPT 回传及 GUI 必须逐项签收。

- Temporal 来源：[服务端及许可](https://github.com/temporalio/temporal) · [CLI 开发服务](https://docs.temporal.io/cli/server) · [Activity 故障检测与必填超时](https://docs.temporal.io/encyclopedia/detecting-activity-failures)
- Cadence 来源：[官方源码及许可](https://github.com/cadence-workflow/cadence) · [安装与初始化](https://cadenceworkflow.io/docs/tech-review/day-0-planning/installation/installation-initialization/) · [Python SDK](https://cadenceworkflow.io/docs/python-client/)
- Conductor 来源：[官方源码及许可](https://github.com/conductor-oss/conductor) · [部署与存储](https://conductor-oss.github.io/conductor/devguide/running/deploy.html) · [Task API](https://github.com/conductor-oss/conductor/blob/main/docs/documentation/api/task.md)

## 节点适配记录

对每个节点记录：上游样例链接和实际版本、已验证能力、调用输入输出、本机差异、适配位置、独立证据、复用条件、未覆盖项。能直接运行的样例优先。安装异常先取原日志、下载回执、已缓存版本和服务健康，再选择官方已发布版本或官方源码构建。不要把镜像下载失败归入业务执行失败。依赖、调度器数据、Pi 工作区和 GUI 实例分别隔离，端口限于本机回环；沿用原浏览器和代理配置。
