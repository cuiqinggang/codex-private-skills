# DeepSeek 官方 API 适配器 v1.0

## 接入方式
- DeepSeek Official API
- Base URL: https://api.deepseek.com
- 认证: Bearer token

## 模型
- deepseek-v4-pro (主力)
- deepseek-chat (备选)

## UltraFusion 使用
- M1 位置固定使用 DeepSeek-V4-Pro
- A/B/C/D 四层全程参与
- V15 注入方式：组装到 system/user prompt 中

## 状态码映射
- 200 → PASS 或 PARTIAL
- 400 → ERROR
- 401/403 → AUTH_FAILED
- 429 → RATE_LIMITED
- 5xx → ERROR (retry x1, then substitute)
