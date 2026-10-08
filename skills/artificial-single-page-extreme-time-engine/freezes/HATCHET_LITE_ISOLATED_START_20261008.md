# Hatchet Lite 隔离启动现实证据冻结
日期：2026-10-08；方法 ENGINE=24 / BRAIN=21 / NPT=17
状态：INFRA_REALITY_START_PASS / SDK_TASK_GATE_BLOCKED / FINAL_VALID=NO

## 实际验证
- Windows: DESKTOP-4A1EGTM。未连接 CDP 9223、未触碰原 ChatGPT 页面、未修改 FlClash/Windows 网络代理；不影响已有 n8n-local 和 open-webui-clean 容器。
- Hatchet Embedded 官方 sidecar release v0.110.5 只有 linux/darwin，未提供 Windows sidecar；本机 Ubuntu-24.04-Restore WSL 因 ext4.vhdx 路径缺失无法启动。Windows 原生 Embedded 选型不适用。
- 采用官方 Hatchet Lite Linux 镜像 ghcr.io/hatchet-dev/hatchet/hatchet-lite:v0.105.3-alpha.2，镜像成功拉取并有官方 digest；原生 Docker Linux Engine 29.3.1。
- 隔离目录 C:\AI\Hatchet-Isolated-V1\compose.yaml；项目 hatchet-isolated-v1，单独 Postgres 16 Alpine 和 Hatchet Lite 容器、独立网络及持久化卷；测试端口仅绑定 127.0.0.1:18888 和 127.0.0.1:17070。
- 执行 docker compose up -d --wait：Postgres healthy、Hatchet healthy、退出码0；访问 http://127.0.0.1:18888 返回 HTTP 200。Hatchet 日志显示数据库迁移成功及本地测试租户创建。
- 创建隔离 Python venv：C:\AI\Hatchet-Isolated-V1\.venv；hatchet-sdk 安装命令已执行，但目前未记录最终可用性验收证据。
- 创建 API token 到本地文件的执行尝试被连接器安全检查拦截；未获得 SDK 任务提交的合法鉴权凭据，未尝试绕过。无空任务/并发键/幂等/跨进程故障恢复的真实通过证据。
- 完成后 docker compose stop 正常结束，Postgres 和 Hatchet 容器都已停止；独立卷与镜像保留供后续验证。

## 结论
官方成熟 Hatchet Lite 的本机部署与HTTP服务健康验证=PASS。
外部 SDK 调用、编排性能、持久化恢复、共享浏览器隔离、整体T_VALID 相比 F011 约115.67秒的净收益=UNKNOWN。
REUSE_GATE TOTAL_COST 未形成证据，未到完整 STOP_GATE / Freeze后 Reality，不能将 F011 原执行系统替换。
不得把测试版 alpha 镜像或环境启动成功等同正式生产验收。
下一步：合法取得隔离测试实例 API token，使用 Hatchet 官方SDK示例运行最少必要的无业务任务、并发/幂等与重启恢复检查；形成完整虚拟成熟Freeze后，单次整体验收；不自行重造调度或锁。
