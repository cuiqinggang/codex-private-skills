# 长期记忆超级虚拟人｜能力注册表 v0.1
# Capability Registry

## 原则

```text
能力池尽量完整
≠
所有能力常驻上下文
```

主脑只常驻：
1. 能力类别；
2. 何时调用；
3. 首选/备选路由；
4. 如何即时探测健康状态。

真正的工具说明、连接状态、文件细节、执行器上下文只在任务需要时加载。

## 核心能力面

| 能力面 | 首选入口 | 备选 / 说明 |
|---|---|---|
| 公共网络检索 | Web/Search | 专用 Browser |
| 网页交互 | Browser / Computer-use 类能力（可用时） | Playwright / 已有浏览器技能 |
| Windows 文件/命令/进程 | Desktop Commander Remote | GitHub Windows self-hosted runner |
| GitHub 仓库/Actions | GitHub Connector | gh / Windows runner |
| 大型编码/仓库工程 | Codex | Reasonix / 其他工程执行器 |
| 邮件 | Gmail Connector | Browser |
| 日历 | Google Calendar Connector | Browser |
| 云文件/Docs/Sheets/Slides | Google Drive Connector | Browser |
| 图像 | 原生图像工具 | 专项视觉模型 |
| 定时/条件任务 | Automations | n8n / 外部调度 |
| 长流程状态 | TASK_CONTRACT + Checkpoint | 项目权威状态 |
| GPT 故障灾备 | 独立强备份 | 待 Reality 认证 |

## Lazy Activation｜按需激活

```text
识别任务
→ 查本表
→ 选择最少能力集合
→ 即时健康探测
→ 只加载实际要用的工具
→ 执行
→ Reality 验证
```

不执行“每个任务开始先检查全部工具”。

## GUI 与鼠标键盘

鼠标键盘不是能力定义，而只是一个执行面。

默认优先级：

```text
原生 API / Connector
→ CLI / PowerShell / App protocol
→ 浏览器自动化
→ Windows UI Automation / 交互桌面
→ 人工接管（仅真正不可替代）
```

因此某个执行器没有直接鼠标键盘接口，不等于任务不可完成；先换成熟执行面。

## 网络

“用户已授权联网”和“某个运行时具有网络出口”是两件事。

主脑可按任务路由到具备网络能力的执行面，例如：
- Web/Search；
- GitHub / Gmail / Drive 等 Connector；
- Browser；
- 在线状态下的 Desktop Commander；
- Windows runner / 已授权本机 CLI。

内部隔离 sandbox 若没有公网出口，不尝试破坏其隔离；直接换有网络能力的成熟路径。

## 健康状态

连接状态是动态 Reality，不写死在本文件。

使用前按需探测，例如：
- Desktop Commander：设备 Online + ping；
- GitHub：connector/API 或 runner job；
- Gmail/Calendar/Drive：对应 connector 调用；
- 外部模型：接口/model 参数可用性。

故障时按 `RECOVERY.md` 切换，而不是把所有备份层同时常驻运行。
