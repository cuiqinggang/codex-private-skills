# 安装、排障与复验

## 本机入口

- 首选现有官方安装器和 CLI。先核对实际运行版本、官方发布、已有运行目录和本机备份。修复前保留会话、模型配置和回退点。
- 网关依次核对 `http://127.0.0.1:8642/health`、WebSocket RPC 和真实任务回执。修复沿用官方启动器和现有健康检查。切换前先核对在途任务。
- Dashboard 用本机回环 `http://127.0.0.1:9119/`。已有实例就复用。需要启动时用正式 CLI `hermes dashboard --host 127.0.0.1 --port 9119 --no-open`，再用真实浏览器核对页面、模型和任务回复。
- 日常使用正式 CLI 和 Flash 1017。沿用现有授权。配置变更先备份和回读，恢复后核对实际模型回执。

## 网页与角色验收

1. 使用无敏感内容的隔离任务，记录任务号、工作项、预期产物和计时口径。
2. 用正式工具集运行 `browser_exec`。v0.22.7 的工具可见性依赖 `terminal`。在受控网页验打开、填表、单次提交和读回，由服务端日志和会话工具事件对账。
3. 经平台获准的入口向指定 GPT 网页派单。等实际完成，沿原会话读回回复或生成物，核对标记和结果。提交状态不明时先只读对账。Work Browser 的站点拒绝只说明该自动化入口受限。
4. 用 [固定的 ECC 3.1.1](https://github.com/cuiqinggang/ecc-v3.1.1/tree/b9e651bc6c6751bff43db30b80d9cab983a7c412) 跑引擎及冷恢复。业务试验中控制、资料、执行、审计各有可追溯上下文。仅执行者写约定产物，独立审计读取冻结合同及证据。核对实际文件操作，包含缓存和临时目录。
5. 同一回执记录模型、角色、耗时、错误、恢复、产物哈希和独立验收。失败时先定位最小原因，再复验受影响的功能。

[官方 Windows 安装说明](https://hermes-agent.nousresearch.com/docs/user-guide/windows-native) · [Hermes 原生浏览器说明](https://hermes-agent.nousresearch.com/docs/user-guide/features/browser)
