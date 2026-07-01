---
name: firecrawl-web-api
description: "Firecrawl API — 搜索、抓取、爬取网页数据，LLM优化Markdown输出，MCP直连Agent。129K Stars行业标准。"
version: 1.0.0
author: Hermes Agent
license: MIT
tags: [firecrawl, web-scraping, search, crawl, markdown, api, mcp]
---

# Firecrawl — Web 搜索/抓取 API

## 概述

Firecrawl 是 Web 数据采集的行业标准工具（129K GitHub Stars）。
将任意网页转换为 LLM 优化的 Markdown，支持搜索、抓取、爬取、站点地图。

官网：https://firecrawl.dev
文档：https://docs.firecrawl.dev
API Base：https://api.firecrawl.dev

## API Key

```
fc-d847ac4257244225b308989b9de277b5
```

所有请求的 Header：
```
Authorization: Bearer fc-d847ac4257244225b308989b9de277b5
```

---

## 功能一：Scrape（单页抓取）

把任意 URL 转换为干净的 Markdown。

```bash
curl -X POST 'https://api.firecrawl.dev/v2/scrape' \
  -H 'Authorization: Bearer fc-d847ac4257244225b308989b9de277b5' \
  -H 'Content-Type: application/json' \
  -d '{"url": "https://example.com", "formats": ["markdown"]}'
```

**常用参数：**

| 参数 | 说明 | 默认 |
|------|------|------|
| `url` | 目标网址 | 必填 |
| `formats` | 输出格式：`["markdown"]`, `["html"]`, `["screenshot"]` | markdown |
| `onlyMainContent` | 只提取正文（去导航/广告/侧栏） | true |
| `waitFor` | 等待毫秒数（JS渲染页） | 0 |

**Python 示例：**

```python
import requests

response = requests.post(
    "https://api.firecrawl.dev/v2/scrape",
    headers={"Authorization": "Bearer fc-d847ac4257244225b308989b9de277b5"},
    json={"url": "https://example.com", "formats": ["markdown"]}
)
data = response.json()
print(data["data"]["markdown"])  # 干净的 Markdown 内容
```

---

## 功能二：Search（网页搜索）

搜索网页并返回结果+内容。

```bash
curl -X POST 'https://api.firecrawl.dev/v2/search' \
  -H 'Authorization: Bearer fc-d847ac4257244225b308989b9de277b5' \
  -H 'Content-Type: application/json' \
  -d '{"query": "DeepSeek V4 API documentation", "limit": 5}'
```

**Python 示例：**

```python
response = requests.post(
    "https://api.firecrawl.dev/v2/search",
    headers={"Authorization": "Bearer fc-d847ac4257244225b308989b9de277b5"},
    json={"query": "your search query", "limit": 5}
)
for result in response.json()["data"]:
    print(f"{result['title']}\n{result['url']}\n{result['description']}\n")
```

---

## 功能三：Crawl（批量爬取）

爬取整个网站或多个页面。

```bash
curl -X POST 'https://api.firecrawl.dev/v2/crawl' \
  -H 'Authorization: Bearer fc-d847ac4257244225b308989b9de277b5' \
  -H 'Content-Type: application/json' \
  -d '{
    "url": "https://docs.example.com",
    "maxDepth": 2,
    "limit": 50,
    "scrapeOptions": {"formats": ["markdown"]}
  }'
```

**返回 crawlId，轮询获取结果：**

```bash
curl 'https://api.firecrawl.dev/v2/crawl/{crawl_id}' \
  -H 'Authorization: Bearer fc-d847ac4257244225b308989b9de277b5'
```

---

## 功能四：Map（站点地图）

发现域名下所有 URL。

```bash
curl -X POST 'https://api.firecrawl.dev/v2/map' \
  -H 'Authorization: Bearer fc-d847ac4257244225b308989b9de277b5' \
  -H 'Content-Type: application/json' \
  -d '{"url": "https://docs.example.com"}'
```

---

## 使用场景速查

| 需求 | 用什么 | 命令 |
|------|--------|------|
| 读一个网页内容 | Scrape | `POST /v2/scrape` |
| 搜索信息 | Search | `POST /v2/search` |
| 爬取整个文档站 | Crawl | `POST /v2/crawl` |
| 列出站点所有URL | Map | `POST /v2/map` |
| JS渲染的页面 | Scrape + waitFor | `{"waitFor": 3000}` |

---

## 替代工具对比

| 工具 | 场景 |
|------|------|
| Jina AI Reader | 快速单页：URL前加 `r.jina.ai/` 即用 |
| DuckDuckGo | 已有技能，免费但可能被反爬 |
| XCrawl | 备用搜索渠道 |

Firecrawl 是主力，Jina AI 是快速备选。
