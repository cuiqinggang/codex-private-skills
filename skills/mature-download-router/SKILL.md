---
name: mature-download-router
description: 成熟下载工具最短调用路由 v1.0.0。按资源平台选择 hf、gh、aria2c；只有没有成熟 CLI/直接 URL 且必须依赖网页会话时才使用 playwright-native-ai-browser。
metadata:
  version: "1.0.0"
  display_name: "成熟下载工具最短调用路由"
  status: "STABLE_MINIMAL_ROUTER"
---

# 成熟下载工具最短调用路由 v1.0.0

## 唯一职责

```text
识别来源 -> 选择现成工具
```

本技能只选工具，不做下载器。

## 唯一判定顺序

### 1. Hugging Face

Hugging Face 模型、数据集、私有仓库、gated 资源或 huggingface.co 资源：

```text
-> hf
```

主要命令：`hf download`

认证规则：
- 公开资源：直接使用 `hf`，不要求登录。
- 私有 / gated 资源：仍然优先使用 `hf`；先用 `hf auth whoami` 检查 CLI 认证，需要时用 `hf auth login`。
- 不因为浏览器里已经登录 Hugging Face 就改用 Playwright。

当前已知本机可用版本：`1.19.0`

### 2. GitHub

GitHub Release、Release Asset、仓库克隆等 GitHub 原生任务：

```text
-> gh
```

Release：`gh release download`
仓库：`gh repo clone`

当前已知本机可用版本：`2.92.0`

例外：目标已经是可直接访问的 raw HTTP/HTTPS 文件 URL，则按第 3 条处理。

### 3. 普通直接下载链接

无需网页登录态的普通 HTTP / HTTPS / FTP 直接文件 URL，且没有更合适的平台官方 CLI：

```text
-> aria2c
```

软件：`aria2`
当前已知本机可用版本：`1.37.0`

### 4. 只有网页会话才能取得的下载

只有在以下条件同时成立时才使用：

- 没有更合适的平台官方 CLI；
- 没有可直接交给 `aria2c` 的文件 URL；
- 必须依赖现有 Cookie / Session / 网页按钮 / JavaScript 页面流程才能取得下载。

```text
-> playwright-native-ai-browser
```

版本由该技能自身管理。

如果信息不足以判断来源，不猜工具；先确定来源或取得实际下载 URL。

## 版本规则

- 使用本机当前已经安装且能工作的版本。
- 不因为发现新版本而主动升级。
- 当前工具缺失、实际失败、缺必要功能或用户明确要求时，才处理版本问题。

## 失败规则

工具成功 -> 完成。

工具实际失败 -> 记录这个具体失败，再处理这个具体问题。

不得预先建设备用下载框架。

## 一句话

```text
Hugging Face -> hf（需要认证时用 hf auth）
GitHub 原生任务 -> gh
普通直接 URL -> aria2c
只有网页会话才能取得 -> playwright-native-ai-browser
```
