# Codex 自动化执行手册 v1.0

## 执行方式

```bash
codex exec --skill ultrafusion-low-cost-multi-model-extreme-fusion \
  "回答以下问题: <question>"
```

## 特殊配置

Codex 需要访问：
- DeepSeek API（通过 CC Switch 配置）
- MiniMax API（通过 Provider Adapter）
- Qwen API（消融测试时）

GPT 接入通过浏览器自动化桥接（chatgpt-cdp-browser skill）。

## 输出位置

默认输出到 ~/.codex/output/ultrafusion/runs/
