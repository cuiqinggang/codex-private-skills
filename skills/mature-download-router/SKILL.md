---
name: mature-download-router
description: 成熟下载工具最短调用路由 v0.1.1。只做最小确定性分发：优先来源官方成熟工具，否则用 aria2；不自建下载器、适配器、队列、状态页或选源算法。
metadata:
  version: "0.1.1"
  display_name: "成熟下载工具最短调用路由"
  status: "VIRTUAL_MATURE_REAL_PENDING"
---

# 成熟下载工具最短调用路由 v0.1.1

## 1. 核心

```text
下载任务
-> 识别来源
-> 直接交给成熟工具
-> 等结果
```

禁止自建：

```text
DOWNLOADER
ADAPTER
QUEUE_ENGINE
STATUS_UI
SOURCE_SELECTOR
```

## 2. 路由

```text
HUGGING_FACE
-> hf download

GITHUB_RELEASE
-> 若本机 gh 已存在且可直接使用：gh release download
-> 否则：release asset 直链 -> aria2c

DIRECT_URL / HTTP(S) / FTP / SFTP / METALINK / BITTORRENT
-> aria2c

BROWSER_SESSION_REQUIRED
-> Playwright Native AI Browser

OTHER_SOURCE_WITH_MATURE_OFFICIAL_CLI_OR_API
-> 官方成熟 CLI/API
```

原则：

```text
专用成熟工具 > 通用成熟工具 > 浏览器
```

只有现实约束要求浏览器 Session 时才走浏览器。

## 3. 多任务

```text
同一工具多个任务
-> 交给工具自己的批量/队列/并发能力

不同来源
-> 按来源拆成最少工具调用
```

不建立统一下载调度器。

## 4. 本地现实基线

来自 Reality Foundation v1.1.4：

```text
aria2c=AVAILABLE_OBSERVED
hf=AVAILABLE_OBSERVED
curl.exe=AVAILABLE_OBSERVED
gh=UNKNOWN_NOT_CORE_REQUIRED
```

精确版本：VERIFY_ON_USE。

## 5. 工具缺失时

工具缺失不是下载算法问题。

```text
aria2c 缺失
-> 单独 bootstrap 官方 aria2 稳定版

hf 缺失
-> 单独 bootstrap 官方 hf CLI 稳定版

gh 缺失
-> 不阻塞核心下载；GitHub Release 走 aria2 直链
```

当前冻结外部版本信息（2026-09-23）：

```text
aria2 stable=1.37.0
huggingface_hub/hf stable=1.32.0
GitHub CLI stable=2.101.0 (optional)
```

Windows 获取信息：

```text
aria2:
- 官方 release: https://github.com/aria2/aria2/releases/tag/release-1.37.0
- Windows x64 portable ZIP 可直接使用 aria2c.exe
- Windows Package Manager package id: aria2.aria2

hf:
- 官方安装说明: https://huggingface.co/docs/huggingface_hub/installation
- Windows standalone CLI installer 为官方推荐路径之一

gh (optional):
- 官方安装/手册: https://cli.github.com/
```

不要求账号来使用 aria2。
Hugging Face 公开资源不要求登录；私有/受限资源按来源本身权限处理。

## 6. Executor Entry

下载任务之前只需要保证 Codex 能创建命令进程。

已知 Reality Foundation v1.1.4：

```text
SetTokenInformation(TokenDefaultDacl) failed: 1344
= CODEX_WINDOWS_PROCESS_SPAWN_CHANNEL_FAILURE
!= DOWNLOAD_TOOL_MISSING
```

现实任务必须先切到任务专属窄工作目录，例如：

```text
C:\AI\Mature-Download-Router-Real-Test
```

不得从 `~` / `C:\Users\<user>` 作为 workspace-write 工作目录启动。

若窄目录仍出现同类 1344：
- 允许仅重试一次已存在、已授权、以前现实成功的替代执行通道；
- 仍失败则 STOP；
- 不得把它误判成 aria2/hf 缺失。

## 7. 输入

尽量提供：

```text
SOURCE / REPO / URL
FILE_OR_PATTERN
REVISION_OR_VERSION（若有）
DESTINATION
EXPECTED_HASH（若有）
```

不为填表补造未知值。

## 8. 输出

只关心：

```text
ROUTE
TOOL
COMPLETED
OUTPUT
VALIDITY
ERROR_IF_ANY
T_VALID
```

工具自己的下载实现和进度展示不再包装。

## 9. 方法

```text
METHOD=first-principles-physical-limit-convergence@4.6.0
REALITY_FOUNDATION=local-ai-reality-foundation@1.1.4
VIRTUAL_MATURE=PASS
REAL_CERTIFIED=NO
```

只有最小现实测试 PASS 才提升 REAL_CERTIFIED。

一句话：识别来源后直接调用成熟工具，中间层尽量为零。
