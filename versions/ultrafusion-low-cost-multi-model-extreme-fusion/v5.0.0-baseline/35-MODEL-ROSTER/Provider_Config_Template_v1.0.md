# Provider 配置模板 v1.0

## 本地配置示例

Provider 配置应存储在本地 `.env` 或 `config.yaml` 中，不打包进技能包。

```yaml
providers:
  deepseek:
    type: official_api
    model: deepseek-v4-pro
    base_url: https://api.deepseek.com
  minimax:
    type: official_api
    model: minimax-m2.7
    base_url: https://api.minimax.chat
  qwen:
    type: official_api
    model: qwen3.5-flash
    base_url: https://dashscope.aliyuncs.com/compatible-mode/v1
```

技能包只包含模板和适配器规范，不包含真实凭据。
