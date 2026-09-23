---
name: mature-download-router
description: 成熟下载工具最短调用路由 v1.0.0。只识别下载来源并调用明确的现成工具；不实现下载器、不做下载验证工程、不自动升级工具。
metadata:
  version: "1.0.0"
  display_name: "成熟下载工具最短调用路由"
  status: "STABLE_MINIMAL_ROUTER"
---

# 成熟下载工具最短调用路由 v1.0.0

## 唯一职责

识别下载来源，然后直接调用对应的现成成熟工具。

```text
只选工具，不做下载器。
```

## 唯一路由表

### 1. Hugging Face

识别条件：Hugging Face 模型、数据集或 huggingface.co 资源。

调用工具：`hf`

主要命令：`hf download`

当前已知本机可用版本：`1.19.0`

### 2. GitHub

识别条件：GitHub Release、Release Asset、仓库克隆等 GitHub 原生任务。

调用工具：`gh`（GitHub CLI）

常用命令：
- Release 资源：`gh release download`
- 仓库：`gh repo clone`

当前已知本机可用版本：`2.92.0`

说明：如果目标本身是一个可直接访问的 raw HTTP/HTTPS 文件 URL，则按第 3 条处理。

### 3. 普通直接下载链接

识别条件：无需网页登录态的普通 HTTP / HTTPS / FTP 直接文件链接，且没有更合适的平台官方 CLI。

调用工具：`aria2c`

软件：`aria2`

当前已知本机可用版本：`1.37.0`

### 4. 必须依赖网页登录态

识别条件：必须使用登录态、Cookie、Session、网页按钮或 JavaScript 动态生成下载地址。

调用工具：`playwright-native-ai-browser`

版本：由该技能自身管理；本路由不复制其版本号。

## 版本规则

- 默认直接使用本机当前已安装且能工作的版本。
- 不因为存在更新版本而先升级。
- 不为一次下载任务自动安装、升级或替换工具。
- 只有当前工具缺失、明确失败、缺少任务所需功能，或用户明确要求升级时，才处理版本问题。

## 失败规则

当前选中的成熟工具正常完成任务：结束。

当前选中的成熟工具实际失败：报告具体失败，再针对这个具体问题处理。

不要因为“以后可能失败”预先建设 fallback、源竞争或下载框架。

## 禁止

本技能不得实现或引入：
- 自定义 downloader
- 自定义 retry / queue / cache / chunk / concurrency
- 多源竞争
- 下载测速或 benchmark
- Virtual-99 / REAL / Reality Certification
- T* 或时间账本
- 下载证据矩阵
- 为证明成熟下载器能工作而进行重复认证

## 一句话定义

```text
Hugging Face -> hf
GitHub -> gh
普通直接 URL -> aria2c
必须网页登录态 -> playwright-native-ai-browser
```
