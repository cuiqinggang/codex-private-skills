# 爱马仕大模型接入调试昨日重现技能包

## 1. 用途

用于把第三方 OpenAI-compatible / Anthropic-compatible / MaaS 大模型接入 Hermes / 爱马仕 worker。

典型任务：
- 给某个 Hermes worker 更换大模型。
- 克隆一个独立 profile 做成本测试。
- 设置清晰显示名，方便判断哪个 worker 使用哪个模型。
- 验证模型是否真的被 Hermes 调用成功，而不是只看 gateway 是否启动。
- 保存完整调试过程，方便以后重装或迁移时昨日重现。

## 2. 本次成功基线

源 worker：worker-01
最终 profile：hermes-worker-01-claude-4-7-opus
显示名称：Hermes-worker-01-Claude 4.7 OPus
模型 ID：anthropic/claude-4.7-opus
七牛接口：https://openai.sufy.com/v1
Hermes provider：deepseek
成功验证语：HERMES_CLAUDE_OPUS_OK

## 3. 核心结论

本次真正成功路线：

provider: deepseek
default: anthropic/claude-4.7-opus
base_url: https://openai.sufy.com/v1
api_mode: chat_completions

对应 .env 推荐写法：

DEEPSEEK_API_KEY=<七牛云 API Key>
DEEPSEEK_BASE_URL=https://openai.sufy.com/v1
OPENAI_API_KEY=<七牛云 API Key>
OPENAI_BASE_URL=https://openai.sufy.com/v1
QINIU_API_KEY=<七牛云 API Key>
QINIU_AI_API_KEY=<七牛云 API Key>
API_SERVER_MODEL_NAME="Hermes-worker-01-Claude 4.7 OPus"

注意：真实 API Key 只写入本机 .env，不要写入技能包。

## 4. 为什么不用 provider=openai

实测 provider=openai 会失败。

典型错误：
Unknown provider openai

结论：当前 Hermes v0.13.0 不识别 openai provider，所以不能用它接七牛。

## 5. 为什么不用 provider=openrouter

实测 provider=openrouter 也不适合。

典型现象：
虽然 config.yaml 写了 base_url=https://openai.sufy.com/v1
但 Hermes 实际运行时仍然请求 https://openrouter.ai/api/v1
并出现 HTTP 500。

结论：openrouter provider 会强制走 OpenRouter 官方 endpoint，不适合接七牛自定义 base_url。

## 6. 为什么 provider=deepseek 成功

worker-03-flash 已经证明 deepseek provider 可以走自定义 base_url。
本次把七牛 Claude 4.7 Opus 也放到 deepseek provider 下，成功调用。

因此七牛 OpenAI-compatible 模型接入 Hermes 的成熟路径是：
provider=deepseek
base_url=https://openai.sufy.com/v1
model=anthropic/claude-4.7-opus

## 7. 标准调试流程

### G01 确认目标

必须先确认：
- 源 profile，例如 worker-01
- 目标 profile，例如 hermes-worker-01-claude-4-7-opus
- 显示名，例如 Hermes-worker-01-Claude 4.7 OPus
- 模型 ID，例如 anthropic/claude-4.7-opus
- 候选 endpoint，例如 https://api.qnaigc.com/v1 和 https://openai.sufy.com/v1

### G02 先做 Windows API 预检

先测 /models。
成功标准：HTTP 200，并且模型列表包含目标模型 ID。

本次结果：
https://api.qnaigc.com/v1 可访问，但没有目标模型。
https://openai.sufy.com/v1 可访问，并且包含 anthropic/claude-4.7-opus。

所以最终使用 https://openai.sufy.com/v1。

### G03 再做 WSL API 预检

WSL 中可能有坏代理。
本次发现坏代理：
HTTP_PROXY=http://192.168.128.1:17890
HTTPS_PROXY=http://192.168.128.1:17890

典型错误：
Failed to connect to 192.168.128.1 port 17890

处理方式：
unset HTTP_PROXY HTTPS_PROXY ALL_PROXY http_proxy https_proxy all_proxy NO_PROXY no_proxy

以后启动 gateway 和测试 chat 前，都建议先清掉这些代理变量。

### G04 直连七牛 chat 预检

在改 Hermes 之前，必须先直接调用 /chat/completions。

成功标记：
QINIU_CLAUDE_OK

只有七牛直连成功后，才允许进入 Hermes profile 配置。

### G05 创建 Hermes profile

不要手工复制 profile 目录。

正确方式：
hermes profile create hermes-worker-01-claude-4-7-opus --clone --clone-from worker-01

成功后应出现 wrapper：
/home/u123456/.local/bin/hermes-worker-01-claude-4-7-opus

### G06 写入 Hermes 配置

推荐命令：
hermes-worker-01-claude-4-7-opus config set model.provider deepseek
hermes-worker-01-claude-4-7-opus config set model.default anthropic/claude-4.7-opus
hermes-worker-01-claude-4-7-opus config set model.base_url https://openai.sufy.com/v1
hermes-worker-01-claude-4-7-opus config set model.api_mode chat_completions

### G07 写入 .env

.env 中至少保留：
DEEPSEEK_API_KEY=<API_KEY>
DEEPSEEK_BASE_URL=https://openai.sufy.com/v1
OPENAI_API_KEY=<API_KEY>
OPENAI_BASE_URL=https://openai.sufy.com/v1
QINIU_API_KEY=<API_KEY>
QINIU_AI_API_KEY=<API_KEY>
API_SERVER_MODEL_NAME="Hermes-worker-01-Claude 4.7 OPus"

### G08 清代理启动 gateway

启动时必须清掉代理：
unset HTTP_PROXY HTTPS_PROXY ALL_PROXY http_proxy https_proxy all_proxy NO_PROXY no_proxy

推荐用 tmux 后台运行 gateway。

### G09 Hermes chat 验证

最终验收命令：
hermes-worker-01-claude-4-7-opus chat -q "只回复：HERMES_CLAUDE_OPUS_OK"

成功标准：
输出中必须出现 HERMES_CLAUDE_OPUS_OK。

失败关键词：
Unknown provider
API call failed
HTTP 500
Internal Server Error
Max retries
Final error
https://openrouter.ai/api/v1

## 8. 成功验收门

一个新大模型 worker 接入 Hermes，必须全部通过：

PASS_01 /v1/models 能看到目标模型。
PASS_02 /v1/chat/completions 直连能返回指定标记。
PASS_03 Hermes profile 创建成功。
PASS_04 config.yaml 写入正确。
PASS_05 .env 写入正确。
PASS_06 gateway 启动成功。
PASS_07 Hermes chat 返回指定标记。
PASS_08 输出中没有 Unknown provider / API failed / OpenRouter endpoint / HTTP 500。

只有 PASS_07 和 PASS_08 同时满足，才算真正成功。

## 9. 已知错误排除表

错误：Unknown provider openai
原因：Hermes 当前不识别 openai provider。
处理：改用 provider=deepseek。

错误：Endpoint 变成 https://openrouter.ai/api/v1
原因：provider=openrouter 强制走 OpenRouter。
处理：不要用 openrouter 接七牛。

错误：WSL curl 超时并指向 192.168.128.1:17890
原因：WSL 有坏代理变量。
处理：unset 所有 proxy 变量。

错误：gateway running 但 chat 失败
原因：gateway 启动不代表模型调用成功。
处理：必须做 chat 标记验收。

错误：脚本显示 PASS 但输出有 API failed
原因：Hermes chat 可能错误时退出码仍为 0。
处理：必须 grep 错误关键词。

## 10. 复用模板

替换变量即可复用：
SOURCE_PROFILE=worker-01
TARGET_PROFILE=hermes-worker-01-claude-4-7-opus
DISPLAY_NAME=Hermes-worker-01-Claude 4.7 OPus
MODEL_ID=anthropic/claude-4.7-opus
BASE_URL=https://openai.sufy.com/v1
PROVIDER=deepseek

核心路径：
API 直连预检
清除 WSL 坏代理
Hermes 官方 clone profile
provider 使用 deepseek
写入 base_url 与模型 ID
启动 gateway
chat 标记验收

## 11. 当前成功基线

profile: hermes-worker-01-claude-4-7-opus
display: Hermes-worker-01-Claude 4.7 OPus
provider: deepseek
model: anthropic/claude-4.7-opus
base_url: https://openai.sufy.com/v1
verify: HERMES_CLAUDE_OPUS_OK

这个基线就是以后昨日重现的标准答案。

## 2026-05-13 更新：主爱马仕七牛 Claude 接入复盘

本次已完成主 hermes-agent 接入七牛代理 Claude 4.7 Opus，并通过 Open WebUI 全链路验证。

新增复盘文件：

references\20260513-主爱马仕七牛Claude接入复盘-OpenWebUI通过.md

本次确认的成熟路径：

model:
  provider: deepseek
  default: anthropic/claude-4.7-opus
  base_url: https://openai.sufy.com/v1
  api_mode: chat_completions

重要经验：

1. provider 字段叫 deepseek，不代表实际仍在使用 DeepSeek；需要看 default model 和 base_url。
2. 重启主 gateway 时不能依赖爱马仕自己继续执行，必须由外部 PowerShell 监督脚本接管。
3. Telegram 网络超时会阻塞主 gateway 启动；日用主线应优先保证 8642 API，再单独修 Telegram。
4. 第一轮验收应使用 ASCII 哨兵词，避免 PowerShell 到 WSL 中文编码误判。
5. Open WebUI 验收通过标记：OPENWEBUI_HERMES_CLAUDE_OK。

最终状态：

TASK-20260513-QINIU-CLAUDE-MAIN-HERMES_PASS

## 2026-05-13 更新：worker-01 Flash 与 worker-04 Claude4.7Opus 分层路由

本次完成 worker 分层路由：

main hermes-agent = DeepSeek V4 Pro
worker-01 = DeepSeek V4 Flash
worker-04 = Claude4.7Opus via Qiniu/Sufy

新增复盘文件：

references\20260513-worker01-Flash-worker04-Claude47Opus-分层路由复盘.md

关键经验：

1. worker 显示名应写入 profile .env 的 API_SERVER_MODEL_NAME，只写 display_name 不够。
2. worker-04 Claude 配置中 provider=deepseek 是复用 Hermes 兼容适配器，不代表实际使用 DeepSeek。
3. worker-04 Claude 的真实后端由 default=anthropic/claude-4.7-opus 与 base_url=https://openai.sufy.com/v1 决定。
4. 只看 config.yaml 和 .env 不够，必须检查运行进程 /proc/PID/environ 里的 DEEPSEEK_API_KEY 是否匹配目标 key。
5. 本次 worker-04 一度出现 401 invalid api key，原因是进程实际使用了错误 key；最终通过显式 env 注入 API_SERVER_KEY、API_SERVER_MODEL_NAME、DEEPSEEK_API_KEY 解决。
6. Telegram 变量可能阻塞 gateway 启动；模型 API 服务优先，Telegram 应单独修复。
7. Claude worker-04 消耗高，验收 W04_OK 也用了约 24421 tokens，只能用于疑难问题和最终复核。

最终通过：

G12C_PASS_MODELS_NAME_FLASH
G14U_PASS_WORKER04_CLAUDE_OK
TASK-20260513-WORKER01-FLASH-WORKER04-CLAUDE47OPUS-PASS
