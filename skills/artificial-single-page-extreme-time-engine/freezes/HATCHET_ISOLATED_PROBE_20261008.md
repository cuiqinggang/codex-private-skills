# Hatchet 独立环境验证阶段冻结（2026-10-08）
版本 ENGINE=24 / BRAIN=21 / NPT=17。
范围：只读检查本机环境、核对 Hatchet 官方发布物、在不触碰已登录浏览器的环境中获取官方容器镜像。
已证实：
1. Windows Desktop Commander 在线，Windows 设备 DESKTOP-4A1EGTM，连接标识 f6990966-5870-484b-bf79-409bc6fb963e。
2. 官方 hatchet-embedded GitHub release latest=v0.110.5，仅发布 darwin/linux amd64/arm64 sidecar，未发现 Windows sidecar。因此原生 Windows Embedded 不可作为直接已证实可用基线。
3. WSL Ubuntu-24.04-Restore 启动失败 ERROR_PATH_NOT_FOUND，相关 ext4.vhdx 映射 D:\WSL\Ubuntu-24.04-Restore\ext4.vhdx；没有改变该环境。
4. Docker Linux Engine 29.3.1 可用，已存在 n8n-local 等容器；未停止、替换或修改既有容器。
5. 官方 hatchet-lite 镜像 ghcr.io/hatchet-dev/hatchet/hatchet-lite:v0.105.3-alpha.2 已发起单独镜像下载，最后检查仍未完成，不能称为启动通过；注意当前 tag 为 alpha，仅用于隔离探索。
6. 未改变 FlClash/Windows 代理；没有连接 CDP 9223、发送 ChatGPT 消息、启动第二浏览器。
结论：原 Hatchet Embedded Windows 直接运行候选淘汰；转到官方 Linux Docker Hatchet Lite / Embedded-in-container 作为成熟候选。本轮启动/持久化/并发/幂等/恢复均未验收；不能宣称 Reality 通过、REUSE_GATE 完成或 T_VALID 优于 F011（115.67s）。
下一节点：先确认独立容器镜像拉取完整；使用隔离端口/卷与稳定镜像，在不共享已有服务的条件下官方启动及官方例程验证。随后故障恢复和业务适配虚拟成熟→Freeze→单次完整 Reality。