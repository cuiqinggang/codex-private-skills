---
name: mature-download-router
description: 成熟下载工具最短调用路由 v0.1.3。只做最小来源判断并调用成熟工具；发布给 Codex 前，同一公开测试资源必须先由 GPT 外部取件成功并保存可回读证据。
metadata:
  version: "0.1.3"
  display_name: "成熟下载工具最短调用路由"
  status: "PRE_RELEASE_REAL_FETCH_PASS_LOCAL_REAL_PENDING"
---

# 成熟下载工具最短调用路由 v0.1.3

## 核心

下载任务只做一件事：

```text
识别来源 -> 交给成熟工具
```

不自建下载器、适配器、队列、状态页或下载算法。

## 路由原则

```text
来源有官方成熟工具 -> 官方成熟工具
已有直接 URL -> 成熟直接下载工具
必须依赖网页登录态 -> Playwright
```

## 发布门

任何用于 Codex 现实认证的公开测试资源，发布前必须满足：

```text
GPT_EXTERNAL_FETCH=PASS
ARTIFACT_SAVED_TO_SHARED_REPO=PASS
ARTIFACT_REREAD=PASS
```

否则：

```text
CODEX_REAL_TASK_RELEASE=BLOCK
```

## 当前发布前真实样本

```text
1. Hugging Face
   source=https://huggingface.co/openai-community/gpt2/resolve/main/config.json
   bytes=665
   blob_sha=10c66461e4c109db5a2196bff4bb59be30396ed8
   result=PASS

2. Generic HTTPS
   source=https://www.cloudflare.com/robots.txt
   bytes=1093
   saved_blob_sha=8e68773cbc7b359bd3f22570effed16019ea7706
   result=PASS

3. GitHub repository file
   source=aria2/aria2@release-1.37.0:README.rst
   bytes=22434
   source_blob_sha=75559047dabff9cc609760551d49b342de504cd6
   saved_blob_sha=75559047dabff9cc609760551d49b342de504cd6
   result=PASS
```

GitHub Release asset 正文当前 GPT 连接器不能直接拉取，因此不伪造 PASS，也不用于首个本地认证样本。

## 本地认证

本地认证只需要重复一个已经通过发布门的小文件下载。

当前首选样本：
```text
Hugging Face config.json, 665 bytes
```

本机先前已有现实证据：
```text
curl.exe + existing proxy http://127.0.0.1:7890 -> Hugging Face HTTP 200
```

因此首个本地认证使用 curl.exe，不再临时更换未经同类现实证明的工具。

## 状态

```text
PRE_RELEASE_REAL_FETCH=PASS
LOCAL_REAL_CERTIFIED=NO
```
