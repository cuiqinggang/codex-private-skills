---
name: mature-download-router
description: 成熟下载工具最短调用路由 v0.1.0。下载任务只做最小确定性分类，直接交给成熟专用工具；不自建下载器、适配器、状态页、队列或选源算法。
metadata:
  version: "0.1.0"
  display_name: "成熟下载工具最短调用路由"
  status: "VIRTUAL_MATURE_REAL_PENDING"
---

# 成熟下载工具最短调用路由 v0.1.0

## 1. 唯一目标

在下载任务有效完成的前提下，让“智能体识别任务 -> 调用成熟下载工具”的额外路径最短。

```text
BUILD_DOWNLOADER=NO
BUILD_ADAPTER=NO
BUILD_QUEUE_ENGINE=NO
BUILD_STATUS_UI=NO
BUILD_SOURCE_SELECTOR=NO
```

成熟下载工具自己的下载、并发、分段、断点、队列、缓存、进度、重试等能力全部复用，不重复实现。

## 2. 路由规则

规则按来源直接确定：

```text
HUGGING_FACE
-> hf download

GITHUB_RELEASE
-> gh release download

DIRECT_URL / HTTP(S) / FTP / SFTP / METALINK / BITTORRENT
-> aria2c

BROWSER_SESSION_REQUIRED
-> Playwright Native AI Browser

OTHER_SOURCE_WITH_MATURE_OFFICIAL_CLI_OR_API
-> 优先官方成熟 CLI/API
```

不存在额外“选源引擎”。专用工具内部能完成的事全部交给专用工具。

## 3. 多任务

```text
同一生态多个文件
-> 一次交给该成熟工具的批量/队列能力

不同生态混合任务
-> 按来源拆成最少的工具调用
-> 各成熟工具自行管理内部队列/并发
```

禁止自建全局下载调度器。

## 4. 最小输入合同

智能体尽量提供：

```text
SOURCE_TYPE
SOURCE / REPO / URL
FILE_OR_PATTERN
REVISION_OR_VERSION（若已知）
DESTINATION
EXPECTED_SIZE_OR_HASH（若已知）
```

未知字段不为填表而补造。

## 5. 最小结果合同

只关心：

```text
ROUTE_SELECTED
TOOL
COMMAND_OR_ACTION
DESTINATION
COMPLETED=YES|NO
OUTPUT_EXISTS=YES|NO
VALIDITY_CHECK=PASS|FAIL|NOT_PROVIDED
ERROR（若失败）
```

工具自己的进度显示不再重新包装。

## 6. 当前冻结成熟工具

冻结日：2026-09-23。

```text
aria2 stable = 1.37.0
GitHub CLI stable = 2.101.0
huggingface_hub stable = 1.32.0
Playwright Native AI Browser = 使用 Reality Foundation 中已认证资产，VERIFY_ON_USE
```

版本号仅作为当前冻结事实；未来版本升级只在实际需要时更新本技能包。

## 7. Fallback

只有首选成熟工具不可用时才降级：

```text
官方专用 CLI/API 不可用
-> 若已得到直接 URL：aria2c
-> 若必须依赖网页登录态：Playwright
-> 否则返回最小 Reality Delta
```

禁止为了统一接口而增加中间层。

## 8. 方法与现实底座

```text
METHOD=first-principles-physical-limit-convergence@4.6.0
REALITY_FOUNDATION=local-ai-reality-foundation@1.1.3
```

当前状态：

```text
VIRTUAL_MATURE=PASS
REAL_CERTIFIED=NO
```

只有 REAL-CERTIFICATION.md 的现实测试 PASS 后，才允许把状态提升为 REAL_CERTIFIED。

## 9. 版本规则

```text
PATCH = 工具版本、命令细节、已知 Reality Delta 修正
MINOR = 新增一种来源类别/成熟工具路线
MAJOR = 路由合同发生不兼容变化
```

一句话：能直接交给成熟工具，就直接交；不在下载节点重新造轮子。
