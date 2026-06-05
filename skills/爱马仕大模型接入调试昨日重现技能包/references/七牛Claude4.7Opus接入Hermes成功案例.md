# 七牛 Claude 4.7 Opus 接入 Hermes 成功案例

成功日期：2026-05-12

## 最终成功配置

provider: deepseek
default: anthropic/claude-4.7-opus
base_url: https://openai.sufy.com/v1
api_mode: chat_completions

## 成功验证

HERMES_CLAUDE_OPUS_OK
G11_PASS

## 失败路径记录

1. provider=openai 失败：Hermes 报 Unknown provider openai。
2. provider=openrouter 失败：实际请求跑到 https://openrouter.ai/api/v1。
3. WSL 坏代理失败：请求被导向 192.168.128.1:17890 并超时。

## 成功路径

provider=deepseek
base_url=https://openai.sufy.com/v1
model=anthropic/claude-4.7-opus

最终 Hermes chat 返回：
HERMES_CLAUDE_OPUS_OK
