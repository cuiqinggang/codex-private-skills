---
name: mature-download-router
description: 成熟下载工具最短调用路由 v0.1.2。只做最小确定性分发，并继承 Reality Foundation 已验证的本机网络出口；不自建下载器、适配器、队列、状态页或选源算法。
metadata:
  version: "0.1.2"
  display_name: "成熟下载工具最短调用路由"
  status: "VIRTUAL_MATURE_REAL_PENDING"
---

# 成熟下载工具最短调用路由 v0.1.2

## 1. 核心

```text
下载任务
-> 识别来源
-> 继承当前已验证的网络上下文
-> 直接交给成熟工具
-> 等结果
```

禁止自建 downloader / adapter / queue / status UI / source selector。

## 2. 路由

```text
HUGGING_FACE -> hf download
GITHUB_RELEASE -> gh（若已可用），否则 asset URL -> aria2c
DIRECT_URL / HTTP(S) / FTP / SFTP / METALINK / BITTORRENT -> aria2c
BROWSER_SESSION_REQUIRED -> Playwright Native AI Browser
OTHER_OFFICIAL_MATURE_CLI_OR_API -> 官方成熟工具
```

## 3. 唯一新增现实规则：网络上下文继承

现实认证 04 已证明路由匹配 2/2，但 hf 与 aria2c 都在联网阶段失败。此前现实证据又已证明目标站点在显式使用现有本机代理出口后可访问。

因此冻结：

```text
ROUTE_SELECTION != NETWORK_ROUTE
```

调用成熟下载工具时，不重新设计代理；只继承 Reality Foundation 当前已验证的网络出口。

当前本机已知有效出口候选：

```text
http://127.0.0.1:7890
```

使用方式必须是进程级或命令级，不修改 Windows / FlClash / Git 持久设置：

```text
hf:
  启动进程前继承 HTTP_PROXY / HTTPS_PROXY

aria2c:
  --all-proxy=<CURRENT_VERIFIED_PROXY>
  或继承标准 proxy 环境变量
```

若该已有 endpoint 当前不可连接：
```text
STOP
REALITY_DELTA=EXISTING_NETWORK_ENDPOINT_UNAVAILABLE
```

不得把它误判成 hf/aria2 算法失败。

## 4. 多任务

同一工具多个任务交给工具自己的批量/队列/并发；不同来源拆成最少成熟工具调用。不建立统一调度器。

## 5. 本机现实基线

现实认证 04：

```text
WORKDIR=C:\AI\Mature-Download-Router-Real-Test
PROCESS_SPAWN=PASS
aria2c=1.37.0
hf=1.19.0
gh=2.92.0
```

版本漂移不是本次 connection refused 的已证实原因。

当前上游稳定基线（2026-09-23）：

```text
aria2=1.37.0
huggingface_hub/hf=1.32.0
GitHub CLI=2.101.0 (optional)
```

## 6. Executor Entry

现实任务使用窄工作目录，不从用户 Home 启动 workspace-write。1344 属于 Codex Windows 进程创建问题，不等于下载工具缺失。

## 7. 方法

```text
METHOD=first-principles-physical-limit-convergence@4.6.0
REALITY_FOUNDATION=local-ai-reality-foundation@1.1.5
VIRTUAL_MATURE=PASS
REAL_CERTIFIED=NO
```

一句话：选对成熟工具，同时把现实中已经验证有效的网络出口原样带给它；除此之外不增加中间层。
