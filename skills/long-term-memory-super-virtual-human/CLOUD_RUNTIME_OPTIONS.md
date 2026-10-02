# 长期记忆超级虚拟人｜云运行与 MCP 定位 v0.1

## 三种不同能力

### 1. Remote MCP Server
MCP Server 是工具/数据能力服务端，不等于一台通用云电脑。

用途：
- 暴露 API、数据库、内部工具、文件系统代理等能力给 Agent；
- 作为持久工具接口；
- 可部署在公网服务器，或通过安全隧道连接私网/本机服务。

### 2. OpenAI-managed cloud execution
适合不依赖本机常开的任务：
- ChatGPT Work Cloud Browser：网页任务可在用户离开或关闭电脑后继续；
- Codex Cloud：代码任务运行在 OpenAI 管理的计算机上，电脑休眠后仍可继续；
- Scheduled / event-triggered tasks：支持的自动任务在云端执行。

这些不是用户自己的通用 VPS，但能覆盖相当一部分“电脑关机任务继续”的需求。

### 3. User-owned VPS / Cloud Worker
是真正长期在线、可自定义的网络服务器。

适合：
- 24x7 watchdog；
- 自建 MCP Server；
- webhook / callback；
- 任务队列；
- 独立备脑；
- 独立状态机；
- 与本地 Windows 低相关的灾备；
- 任意自定义 daemon/service。

## 路由原则

```text
OpenAI 托管云能直接 VALID
→ 优先托管云，少维护

需要任意服务 / 独立故障域 / 24x7 常驻
→ VPS / 云 Worker

只需要给 GPT 暴露工具
→ MCP Server
```

不要为了“有服务器”而搭服务器。

## 与本机关系

如果任务运行在：
- ChatGPT Work Cloud Browser；
- Codex Cloud；
- Scheduled cloud task；
- 自有 VPS；

则本机 Windows 可以关机，只要任务不依赖必须在线的本机文件、GUI 或设备。

如果任务需要本机：
- Desktop Commander；
- 本地 GUI；
- K盘实时文件；
- 本地 GPU；
- 本地登录态；

则本机仍必须在线，或先把所需资产同步到云端执行环境。

## 当前项目建议

P5 云层优先顺序：

```text
OpenAI managed cloud
→ 已有云资源
→ 短时按需云
→ 只有持续需求才部署常驻 VPS
```

常驻 VPS 真正有价值时，应承担低相关灾备与外部 watchdog，而不是复制本地整个巨型工作站。
