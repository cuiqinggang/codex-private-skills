---
name: codex-deepseek-model-integration
description: "将 DeepSeek V4 Pro/Flash 接入 GPT Codex Desktop App — 3种成熟工具方案，最简单的桌面端 GUI 操作"
version: 1.1.0
author: Hermes Agent
license: MIT
tags: [codex, deepseek, openai-compatible, desktop, model-integration, mimo2codex, codex-app-transfer]
---

# Codex Desktop 接入 DeepSeek 模型 — 3种工具方案

## 核心理念

> GPT Codex Desktop App 默认只能用 OpenAI 模型。通过本地代理/网关工具，把 DeepSeek 以 OpenAI-Compatible 格式接入，
> Codex 模型选择器里就能直接选 DeepSeek V4 Pro / Flash。

## 方案对比

| 工具 | Stars | 安装方式 | GUI | DeepSeek内置 | 备注 |
|------|-------|---------|-----|------------|------|
| **mimo2codex** | 544 | npm / Desktop 安装包 | ✅ Web管理界面 | ✅ 内置 | **推荐**：有Win/Mac安装包，后台运行，开机自启 |
| **codex-app-transfer** | 241 | Windows Setup.exe | ✅ 桌面GUI | ❌ 手动配 | Tauri桌面应用，功能最全（主题/用量/MCP备份） |
| **CodexSaver** | 589 | npm | ❌ CLI | ❌ 手动配 | MCP工具，侧重降本，非桌面GUI |

---

## 【推荐方案】mimo2codex

**仓库**：https://github.com/7as0nch/mimo2codex
**下载**：https://mimodoc.chengj.online/download

### 架构

```
Codex Desktop App
  → 127.0.0.1:8788 (mimo2codex 本地代理)
    → DeepSeek API / MiMo / 任意 OpenAI-Compatible 上游
```

### 安装（2步）

**第一步**：Microsoft Store 搜索 "Codex"（OpenAI 出品）→ 安装

**第二步**：从 https://mimodoc.chengj.online/download 下载 Windows 安装包 → 安装
- 支持 Windows / macOS
- 安装后自动后台运行
- 开机自动启动
- 系统托盘一键打开管理界面

### 配置（3步）

1. 安装后自动打开管理界面 `http://127.0.0.1:8788/admin/`
2. 在 Provider 配置中填入 DeepSeek API Key
3. 点"Codex Enable"一键切换模型

### 特性

- ✅ 内置 DeepSeek V4 Pro 和 MiMo V2.5
- ✅ 通用 Provider 机制：任何 OpenAI Chat Completions 兼容（Qwen/GLM/Kimi/Ollama 等）
- ✅ 管理控制台：模型目录、聊天日志、Token 统计、Provider 配置
- ✅ 一键模型切换（管理员 WebUI）
- ✅ 工具调用、网络搜索、视觉、推理全部支持
- ✅ 自动 Responses API ↔ Chat Completions 协议转换
- ✅ SQLite 持久化

### Codex 模型选择器效果

配置完成后，Codex Desktop 的模型选择器中会出现 DeepSeek 模型选项，
选择后 Codex 通过本地 mimo2codex 代理（127.0.0.1:8788）自动路由到 DeepSeek API。

---

## 【备选方案】codex-app-transfer

**仓库**：https://github.com/Cmochance/codex-app-transfer
**下载**：https://github.com/Cmochance/codex-app-transfer/releases/latest

Windows 安装包：
```
Codex-App-Transfer-v<版本>-Windows-x64-Setup.exe    (NSIS 安装版，推荐)
Codex-App-Transfer-v<版本>-Windows-x64.msi          (MSI 企业版)
```

### 特点

- Tauri 桌面应用（Rust 后端），原生 Windows GUI
- 中英文界面，浅色/深色多套主题
- 支持 8 种供应商：DeepSeek, Kimi, MiMo, GLM, 百炼, MiniMax, Gemini, Grok
- apply_patch 兼容（DeepSeek 等 chat 模型也支持 Codex diff 编辑）
- 用量统计 + 缓存命中率
- 联网工具内置（web_fetch + web_search）

### 配置步骤

1. 启动 → 仪表盘右上角 **＋** → 选自定义供应商
2. API Base URL：`https://api.deepseek.com`
3. API Key：你的 DeepSeek API Key
4. 获取模型 → 选 deepseek-v4-pro / deepseek-v4-flash
5. 模型映射：`gpt-5.5` → `deepseek-v4-pro`，`gpt-5.4-mini` → `deepseek-v4-flash`
6. 点 **应用** → 右上角 **↻ 重启 Codex**

---

## DeepSeek API 配置（通用）

### API 地址
```
https://api.deepseek.com/v1/chat/completions
```

### DeepSeek V4 Pro
- 模型名：`deepseek-v4-pro`
- 适合：复杂编程、长上下文推理
- 建议映射到 Codex 的 `gpt-5.5`

### DeepSeek V4 Flash
- 模型名：`deepseek-v4-flash`
- 适合：日常轻量任务、快速响应
- 建议映射到 Codex 的 `gpt-5.4-mini`

---

## 关于 "Codex++"

如果你看到的视频里软件确实叫 "Codex++"，可能是以下情况之一：
1. mimo2codex 或 codex-app-transfer 在视频/教程中被作者昵称为 "Codex++"
2. 某个 B站/YouTube 创作者的自定义打包版本
3. 一个尚未被 GitHub 广泛索引的新项目

无论哪种，**mimo2codex 和 codex-app-transfer 都实现了完全相同的功能**。
推荐用 mimo2codex：Windows 安装包、内置 DeepSeek、中文支持、最简单。
