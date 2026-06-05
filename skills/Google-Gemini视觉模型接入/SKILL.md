---
name: google-gemini-视觉模型接入
description: >
  Hermes 接入 Google Gemini 作为辅助视觉模型的完整记录。
  原始尝试 gemini-2.0-flash 失败（配额为0，返回429），最终成功切换到 gemini-2.5-flash。
  包含配置位置、API Key 设置方式、模型选型和验证方法。
category: mlops
version: 1.0
created: 2026-05-22
updated: 2026-05-22
tags:
  - google
  - gemini
  - vision
  - 视觉模型
  - config.yaml
  - auxiliary
---

# Hermes 接入 Google Gemini 视觉模型

## 背景

Hermes Agent 的 `auxiliary.vision` 用于处理图片/截图分析。默认视觉模型可能不可用或配额不足，需要接入 Google Gemini 作为替代。

## 最终配置（config.yaml）

```yaml
auxiliary:
  vision:
    provider: google
    model: gemini-2.5-flash
    base_url: 'https://generativelanguage.googleapis.com/v1beta'
    api_key: 'AIzaSyDDwIPOhypFmULy1j4DXt77dL3CA6qDW5c'          # Google Gemini API Key
    timeout: 120
    extra_body: {}
    download_timeout: 30
```

配置位置: `C:\Users\A\.hermes\config.yaml` 第116-124行

## API Key 设置

Google Gemini API Key 通过环境变量 `GOOGLE_API_KEY` 设置，或在 config.yaml 的 `api_key` 字段直接填入。

获取 API Key: https://aistudio.google.com/apikey

### Google Cloud 账户信息

| 字段 | 值 |
|------|-----|
| API Key | `AIzaSyDDwIPOhypFmULy1j4DXt77dL3CA6qDW5c` |
| 项目名称 | My Project 30133 |
| 项目 ID | protean-acrobat-497018-a3 |
| 项目编号 | 399485532359 |
| 配额剩余 | 12 个 projects |

**注意**: 中国大陆访问 Google API 需要代理。用户使用跑跑云 Clash 代理（端口 7890）。

## 模型选型过程

### ❌ gemini-2.0-flash — 失败
- **现象**: 返回 HTTP 429（配额限制）
- **原因**: API Key 的 `gemini-2.0-flash` 配额为 **0**（不是地区限制，不是代理问题，同代理下其他模型正常）
- **排查**: 在 Google AI Studio 后台确认配额为0

### ✅ gemini-2.5-flash — 成功
- **状态**: 配额充足，正常返回
- **性能**: 速度快，适合辅助视觉分析
- **说明**: `gemini-2.0-flash` 已停止免费配额，新用户只能使用 `gemini-2.5-flash` 或更高版本

## 验证方法

修改 config.yaml 后**必须重启 Gateway** 才能生效：

```bash
# 重启 Gateway
taskkill /f /im hermes.exe
H:\Hermes_Windows_Native_014\venv\Scripts\hermes.exe gateway run --replace
```

验证是否生效：发送一张图片给 Hermes，如果返回正常的图片分析结果（而非报错或 fallback），则接入成功。

也可以通过 `vision_analyze` 工具测试。

## 注意事项

1. **不要使用 gemini-2.0-flash** — 配额为0，浪费排查时间
2. **代理必须通** — Google API 在大陆需翻墙
3. **配置改动后必须重启 Gateway** — 热重载不生效
4. **API Key 不要提交到 git** — 使用环境变量或 `.hermes/config.yaml` 本地配置
5. **Google AI Studio 的免费配额有限** — 注意使用频率
