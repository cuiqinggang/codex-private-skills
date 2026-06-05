# 2026-05-13 worker-01 Flash 与 worker-04 Claude4.7Opus 分层路由复盘

## 一、最终结论

本次任务已完成。

最终模型分层如下：

主 hermes-agent：
DeepSeek V4 Pro
用途：日常复杂任务、主力判断、排障规划。

worker-01：
DeepSeek V4 Flash
显示名：Hermes-worker-01-Flash
用途：极低成本任务、状态检查、轻量总结、简单并行。

worker-04：
Claude 4.7 Opus
显示名：Hermes-worker-04-Claude4.7Opus
用途：高价值备用、疑难问题、最终复核、关键判断。

最终通过标记：

worker-01：
G12C_PASS_MODELS_NAME_FLASH

worker-04：
G14U_PASS_WORKER04_CLAUDE_OK

---

## 二、当前最终路由结构

当前主线：

hermes-agent
→ DeepSeek V4 Pro
→ https://api.deepseek.com

低成本 worker：

Hermes-worker-01.Hermes-worker-01-Flash
→ DeepSeek V4 Flash
→ https://api.deepseek.com

高质量备用 worker：

Hermes-worker-04.Hermes-worker-04-Claude4.7Opus
→ 七牛 / Sufy
→ https://openai.sufy.com/v1
→ anthropic/claude-4.7-opus

---

## 三、worker-01：DeepSeek V4 Flash 配置过程

### 目标

只修改 worker-01，不动主 hermes-agent，不动 worker-02/03/04。

目标模型：

deepseek-v4-flash

目标显示名：

Hermes-worker-01-Flash

---

### G11：worker-01 模型切换成功

定位到配置文件：

/home/u123456/.hermes/profiles/worker-01/config.yaml

定位到环境文件：

/home/u123456/.hermes/profiles/worker-01/.env

备份目录：

/mnt/h/Hermes_Backups/TASK-20260513-WORKER01-DEEPSEEK-V4-FLASH/G11_20260513_141514

备份哈希：

05ddc1fda495da4bcdf73906edae52dc3c26036354f77195fa9d100259be65fe  worker01_config.before_g11
d3f5def360bff3864cbc171107ca9071bfbf98f1c1773027fa354bd2ef85e4bb  worker01_env.before_g11

修改后 worker-01 配置：

model:
  provider: deepseek
  default: deepseek-v4-flash
  base_url: https://api.deepseek.com
  api_mode: chat_completions

并添加：

display_name: Hermes-worker-01-Flash

worker-01 只重启自身，新 PID：

21281

主模型守卫检查通过，主 hermes-agent 仍是：

deepseek-v4-pro
https://api.deepseek.com

通过标记：

G11_PASS_WORKER01_FLASH_CONFIGURED

---

### G12A：显示名未变化的诊断

问题现象：

Open WebUI 刷新后，worker-01 显示名仍然没有变成 Flash。

诊断发现：

config.yaml 中存在：

API_SERVER_MODEL_NAME: Hermes-worker-01
display_name: Hermes-worker-01-Flash

同时 worker-01 的 /v1/models 因 API key 不匹配返回 invalid API key，因此当时还不能确认模型 id 来源。

关键判断：

display_name 不一定控制 Open WebUI 下拉框显示。
Open WebUI 很可能使用 /v1/models 返回的 id/root。

---

### G12B：把 API_SERVER_MODEL_NAME 写入 config.yaml 仍不够

修改：

API_SERVER_MODEL_NAME: Hermes-worker-01-Flash

重启 worker-01 后，配置文件证据正确：

provider: deepseek
default: deepseek-v4-flash
base_url: https://api.deepseek.com
api_mode: chat_completions
API_SERVER_MODEL_NAME: Hermes-worker-01-Flash
display_name: Hermes-worker-01-Flash

但 /v1/models 仍返回旧名称：

Hermes-worker-01

判断：

API_SERVER_MODEL_NAME 写在 config.yaml 里不生效。
Hermes 实际用于 /v1/models 的名称不是从 YAML 这个字段读取。

通过但带警告：

G12B_WARN_MODELS_NAME_NOT_CONFIRMED
G12B_PASS_WORKER01_MODEL_NAME_FLASH

---

### G12C：真正修正 worker-01 显示名

关键修复：

把模型显示名写入 worker-01 的 .env：

API_SERVER_MODEL_NAME=Hermes-worker-01-Flash

备份目录：

/mnt/h/Hermes_Backups/TASK-20260513-WORKER01-DEEPSEEK-V4-FLASH/G12C_20260513_143749

备份哈希：

fdb4807f61fb1c35d546c1be624a8ec61230306e8b966da2fe5351fd968cc8b3  worker01_config.before_g12c
d3f5def360bff3864cbc171107ca9071bfbf98f1c1773027fa354bd2ef85e4bb  worker01_env.before_g12c

重启 worker-01 后：

端口：

18641

/v1/models 返回：

id: Hermes-worker-01-Flash
root: Hermes-worker-01-Flash

通过标记：

G12C_PASS_MODELS_NAME_FLASH

最终判断：

Open WebUI 的 worker 模型显示名实际由 profile .env 中的 API_SERVER_MODEL_NAME 控制。
config.yaml 里的 display_name 不足以改变 /v1/models 返回值。

---

## 四、worker-04：Claude4.7Opus 配置过程

### 目标

只修改 worker-04，把它作为 Claude 备用高质量通道。

不修改：

主 hermes-agent
worker-01
worker-02
worker-03
Open WebUI 容器
Docker volume

目标模型：

anthropic/claude-4.7-opus

目标 base_url：

https://openai.sufy.com/v1

目标显示名：

Hermes-worker-04-Claude4.7Opus

---

### G14：首次配置 worker-04

修改 worker-04 配置：

/home/u123456/.hermes/profiles/worker-04/config.yaml

最终配置写入：

model:
  provider: deepseek
  default: anthropic/claude-4.7-opus
  base_url: https://openai.sufy.com/v1
  api_mode: chat_completions

API_SERVER_MODEL_NAME: Hermes-worker-04-Claude4.7Opus
display_name: Hermes-worker-04-Claude4.7Opus

环境文件：

/home/u123456/.hermes/profiles/worker-04/.env

写入：

API_SERVER_MODEL_NAME=Hermes-worker-04-Claude4.7Opus
DEEPSEEK_API_KEY=七牛 Claude key

备份目录：

/mnt/h/Hermes_Backups/TASK-20260513-WORKER04-QINIU-CLAUDE47OPUS/G14_20260513_151710

备份哈希：

76eac3b696f30c0828b0c0b15f104a1edc2fe798af6a2dc62fe6b5fa38019e23  worker04_config.before_g14
7867c40ca6eb4bc2256e354da051a1e0e5b98a9f7fee2e871866f4ccbea59f94  worker04_env.before_g14
d880c669af261cc7e6c1e17f16ef47152bc1eb7a8707946041993d69bcbe1d17  main_config.guard_copy

worker-04 端口：

18644

/health 成功：

status=ok
platform=hermes-agent

/v1/models 成功返回：

Hermes-worker-04-Claude4.7Opus

但是 /v1/chat/completions 失败：

curl timeout after 120 seconds
0 bytes received

失败标记：

G14_FAIL_CURL_CHAT

当时判断：

显示名和模型列表成功，但实际聊天链路未验证通过。

---

### Open WebUI 显示名确认

Open WebUI 下拉框已能显示：

Hermes-worker-04.Hermes-worker-04-Claude4.7Opus

说明模型名注册已成功。

但当时发送：

Reply exactly: WORKER04_CLAUDE_OK

没有得到回答。

判断：

Open WebUI 显示成功不等于后端聊天成功。
必须继续用 API 验收 /v1/chat/completions。

---

### G14S：旧进程没有真正退出

尝试重启 worker-04 清理卡住请求时失败：

Gateway already running PID 46748

日志提示：

Use hermes gateway restart to replace it
or use hermes gateway stop
or use hermes gateway run --replace

判断：

worker-04 旧 PID 46748 未退出，新进程启动被 Hermes 拦截。
需要强制停止旧进程、清理 pid 文件、再使用 --replace。

---

### G14T：区分七牛直连与 worker 转发

强制停止旧 worker-04 后重启成功。

worker-04 端口：

18644

/health 成功。

/v1/models 成功返回：

Hermes-worker-04-Claude4.7Opus

七牛直连测试成功：

QINIU_OK

直连响应模型：

anthropic/claude-4.7-opus

直连 usage：

prompt_tokens: 8
completion_tokens: 8
total_tokens: 16

但是 worker-04 转发失败，返回：

Error code: 401
Authentication Fails
Your api key: ****bacd is invalid

失败判断：

七牛 Claude 本身没问题。
worker-04 Hermes 进程实际调用 Claude 时使用了错误 API key。

这一步是本次最关键错误定位。

---

## 五、为什么 API key 会用错

### 表面现象

worker-04 的 config.yaml 正确。
worker-04 的 .env 看起来也写了正确的 DEEPSEEK_API_KEY。
七牛直连也确认 key 可以使用。

但 worker-04 通过 Hermes 调用时，返回 401：

Authentication Fails, Your api key: ****bacd is invalid

这说明：

worker-04 运行进程实际使用的 key 不是 .env 里刚写入的七牛 key，而是另一个旧 key 或外层环境变量里的 key。

---

### 根因判断

本次最合理的根因是：

Hermes worker 进程启动时，API key 来源存在优先级问题。

可能优先读取：

1. 当前 shell / systemd / nohup 继承的环境变量
2. 主进程环境变量
3. 旧 worker 进程环境变量
4. profile .env
5. config 中的 provider 相关 key

当 profile .env 与进程环境变量冲突时，进程实际可能使用旧的环境变量。

所以不能只看文件是否写对，必须验证：

/proc/PID/environ 中的 DEEPSEEK_API_KEY 是否等于目标 key。

本次就是因为只看配置文件和 .env 不够，导致最初出现：

配置正确
显示名正确
models 正确
但 chat 401

---

### 正确处理规则

以后凡是把 worker 切到不同 API 供应商，尤其是同一个 provider 名称 deepseek 但 base_url 不同的情况，必须显式注入运行环境变量。

例如 worker-04 Claude 路线：

API_SERVER_KEY=worker-04 API server key
API_SERVER_MODEL_NAME=Hermes-worker-04-Claude4.7Opus
DEEPSEEK_API_KEY=七牛 Claude key

启动时必须显式 env 注入，而不是只依赖 profile .env。

并且必须验证：

/proc/NEW_PID/environ 中 DEEPSEEK_API_KEY 与目标 key 一致。

---

### 为什么 provider 还是 deepseek

worker-04 Claude 配置中：

provider: deepseek

这不是代表实际使用 DeepSeek 模型。

它只是复用 Hermes 当前可工作的 chat_completions / OpenAI-compatible provider 适配路径。

真正决定后端的是：

default: anthropic/claude-4.7-opus
base_url: https://openai.sufy.com/v1
DEEPSEEK_API_KEY=七牛/Sufy key

所以该路线应理解为：

使用 Hermes 的 deepseek 兼容适配器
连接七牛/Sufy OpenAI-compatible 接口
调用 anthropic/claude-4.7-opus

---

### G14U：最终修复 worker-04

关键修复：

重启 worker-04 时显式注入：

API_SERVER_KEY
API_SERVER_MODEL_NAME
DEEPSEEK_API_KEY

同时禁用 worker-04 .env 里的 Telegram 变量，避免 Telegram 网络阻塞 gateway 启动。

G14U 备份目录：

/mnt/h/Hermes_Backups/TASK-20260513-WORKER04-QINIU-CLAUDE47OPUS/G14U_20260513_154141

备份哈希：

95d000c5abea03c985606332afba7d96f9f71c6b301aa95d972dcdb3e6c4a8a5  worker04_config.before_g14u
44908e0ae6c3ff299644bf47d65588ae105e48d3fc9e114d8ef04725c5829f3d  worker04_env.before_g14u

关键验证：

G14U_PROCESS_QINIU_KEY_MATCH=YES

说明新进程实际环境变量中的 DEEPSEEK_API_KEY 已与 worker-04 .env / 七牛 key 一致。

worker-04 /health 成功：

{"status": "ok", "platform": "hermes-agent"}

worker-04 /v1/models 成功：

Hermes-worker-04-Claude4.7Opus

worker-04 /v1/chat/completions 成功：

W04_OK

usage：

prompt_tokens: 24412
completion_tokens: 9
total_tokens: 24421

最终通过标记：

G14U_PASS_WORKER04_CLAUDE_OK

---

## 六、Telegram 阻塞问题

本次 worker-04 中也看到 Telegram 相关风险。

过去主 hermes-agent 切 Claude 时，Telegram 网络超时曾阻塞 gateway 启动。

本次 worker-04 中，也需要禁用 Telegram 变量：

TELEGRAM_BOT_TOKEN
TELEGRAM_ALLOWED_USERS
TELEGRAM_HOME_CHANNEL

最终 G14U 中已对 worker-04 .env 做了：

DISABLED_BY_G14U_FOR_WORKER04_ONLY

规则：

模型 API 服务优先级高于 Telegram。
不要让 Telegram 平台连接失败阻塞 worker 模型服务。

---

## 七、成本注意事项

worker-04 Claude 即使只回答 W04_OK，仍消耗：

prompt_tokens: 24412
completion_tokens: 9
total_tokens: 24421

所以 Claude worker-04 不应用作日常聊天。

用途限制：

关键判断
疑难排障
最终复核
DeepSeek Pro 和 Flash 都处理不了的问题

低成本任务应该用：

worker-01 Flash

日常复杂主力用：

main hermes-agent DeepSeek V4 Pro

---

## 八、以后复用流程

### 配置 worker-01 Flash 的成熟步骤

S01 确认主 hermes-agent 仍为 DeepSeek V4 Pro
S02 备份 worker-01 config.yaml 和 .env
S03 修改 worker-01 config.yaml：
    default=deepseek-v4-flash
    base_url=https://api.deepseek.com
S04 同步 DeepSeek 官方 key 到 worker-01 .env
S05 设置 worker-01 .env：
    API_SERVER_MODEL_NAME=Hermes-worker-01-Flash
S06 只重启 worker-01
S07 验证：
    /health
    /v1/models 返回 Hermes-worker-01-Flash
S08 Open WebUI 刷新确认显示名

关键点：

显示名要写到 .env 的 API_SERVER_MODEL_NAME。
只写 display_name 不够。

---

### 配置 worker-04 Claude 的成熟步骤

S01 确认主 hermes-agent 仍为 DeepSeek V4 Pro
S02 备份 worker-04 config.yaml 和 .env
S03 从旧成功案例或备份中找到七牛 Claude key
S04 修改 worker-04 config.yaml：
    provider=deepseek
    default=anthropic/claude-4.7-opus
    base_url=https://openai.sufy.com/v1
    api_mode=chat_completions
S05 设置 worker-04 .env：
    API_SERVER_MODEL_NAME=Hermes-worker-04-Claude4.7Opus
    DEEPSEEK_API_KEY=七牛 Claude key
S06 禁用 worker-04 Telegram 变量
S07 强制停止旧 worker-04 进程和 pid 文件
S08 使用显式环境变量注入启动：
    API_SERVER_KEY
    API_SERVER_MODEL_NAME
    DEEPSEEK_API_KEY
S09 验证进程环境：
    /proc/PID/environ 中 DEEPSEEK_API_KEY 必须匹配七牛 key
S10 验证：
    /health
    /v1/models
    /v1/chat/completions
S11 Open WebUI 中确认可选模型并做最小哨兵词测试

---

## 九、禁止重复的错误

不要只看 config.yaml 就认为完成。
不要只看 Open WebUI 出现模型名就认为聊天链路完成。
不要只看 .env 写了 key 就认为进程一定用了这个 key。
不要忽略 /proc/PID/environ 的运行时 key 验证。
不要反复用 Claude 做长对话测试。
不要让 Telegram 阻塞模型 API 服务。
不要让旧 worker 进程和 pid 文件残留。
不要同时改主模型、worker-01、worker-04。
不要在 worker-04 chat 失败时重新探索七牛配置，因为七牛直连 QINIU_OK 已证明端点和 key 有效。

---

## 十、最终稳定布局

当前推荐使用：

便宜层：
worker-01 Flash
DeepSeek V4 Flash
用于轻量任务、检查状态、简单总结、低成本并行。

主力层：
main hermes-agent
DeepSeek V4 Pro
用于日常复杂任务和主要判断。

高质量备用层：
worker-04 Claude4.7Opus
Claude 4.7 Opus via Qiniu/Sufy
用于疑难问题、关键复核、最终判断。

本地模型层：
Gemma4 / Qwen 等
暂时保留为实验/离线/备用，不纳入当前日用主线。

---

## 十一、本次最终状态

main hermes-agent：
DeepSeek V4 Pro
已通过 DEEPSEEK_V4_PRO_MAIN_OK

worker-01：
DeepSeek V4 Flash
已通过 G12C_PASS_MODELS_NAME_FLASH

worker-04：
Claude4.7Opus
已通过 G14U_PASS_WORKER04_CLAUDE_OK

最终任务状态：

TASK-20260513-WORKER01-FLASH-WORKER04-CLAUDE47OPUS-PASS
