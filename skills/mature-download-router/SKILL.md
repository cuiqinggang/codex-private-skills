---
name: mature-download-router
description: 成熟下载工具最短调用路由 v1.0.0。只判断下载来源并选择 hf、gh、aria2c 或 playwright-native-ai-browser；本身不实现下载功能。
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

按顺序判断，命中后停止，不继续匹配后面的规则。

1. **必须依赖现有网页登录态、Cookie、Session、网页按钮或 JavaScript 动态下载**
   -> `playwright-native-ai-browser`

2. **Hugging Face 模型、数据集或 huggingface.co 资源**
   -> `hf`
   -> 主要命令：`hf download`
   -> 当前已知本机可用版本：`1.19.0`

3. **GitHub Release、Release Asset、仓库克隆等 GitHub 原生任务**
   -> `gh`
   -> Release：`gh release download`
   -> 仓库：`gh repo clone`
   -> 当前已知本机可用版本：`2.92.0`
   -> 例外：可直接访问的 GitHub raw 文件 URL 按第 4 条处理

4. **无需网页登录态的普通 HTTP / HTTPS / FTP 直接文件 URL**
   -> `aria2c`
   -> 软件：`aria2`
   -> 当前已知本机可用版本：`1.37.0`

如果信息不足以判断来源，不猜工具；先确定来源或取得实际下载 URL。

## 版本规则

- 使用本机当前已经安装且能工作的版本。
- 不因为发现新版本而主动升级。
- 当前工具缺失、实际失败、缺必要功能或用户明确要求时，才处理版本问题。
- `playwright-native-ai-browser` 的版本由它自己的技能管理，本技能不复制版本号。

## 失败规则

工具成功 -> 完成。

工具实际失败 -> 记录这个具体失败，再处理这个具体问题。

不得预先建设备用下载框架。

## 边界

本技能不包含下载实现、下载算法、测速、认证工程、历史测试结果或时间账本。

## 一句话

```text
需要浏览器登录态 -> playwright-native-ai-browser
否则 Hugging Face -> hf
否则 GitHub 原生任务 -> gh
否则普通直接 URL -> aria2c
```
