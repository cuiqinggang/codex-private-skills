# 2026-05-13 主爱马仕接入七牛 Claude 复盘：Open WebUI 全链路通过

## 一、最终结论

本次任务已经完成。

最终 Open WebUI 验收返回：

OPENWEBUI_HERMES_CLAUDE_OK

这表示链路已经打通：

Open WebUI 3000
→ hermes-agent
→ 主爱马仕 8642
→ 七牛代理 https://openai.sufy.com/v1
→ anthropic/claude-4.7-opus

最终任务状态：

TASK-20260513-QINIU-CLAUDE-MAIN-HERMES_PASS

---

## 二、最终主 Hermes 配置

主配置文件：

~/.hermes/config.yaml

关键配置：

model:
  provider: deepseek
  default: anthropic/claude-4.7-opus
  base_url: https://openai.sufy.com/v1
  api_mode: chat_completions

重要解释：

provider: deepseek

这里不是表示实际使用 DeepSeek Pro，而是复用 Hermes 当前可用的 chat_completions 兼容适配路径。

真正决定模型路线的是：

default: anthropic/claude-4.7-opus
base_url: https://openai.sufy.com/v1

所以实际路线是：

七牛代理 Claude 4.7 Opus

---

## 三、本次复用的旧资料路径

本次优先复用以下旧成功资料：

H:\Hermes_Skills\爱马仕大模型接入调试昨日重现技能包\SKILL.md
H:\Hermes_Skills\爱马仕大模型接入调试昨日重现技能包\references\七牛Claude4.7Opus接入Hermes成功案例.md
H:\Hermes_Skills\爱马仕大模型接入调试昨日重现技能包\交接给爱马仕.md

旧资料确认的成功路径：

provider=deepseek
model/default=anthropic/claude-4.7-opus
base_url=https://openai.sufy.com/v1
api_mode=chat_completions

---

## 四、本次执行过程

### G01：搜索旧资料

结果：

三个高优先级路径全部存在。

判断：

以前的七牛 Claude 接入 Hermes 成功案例已经保存，应该优先复用，不应从零探索。

---

### G02：提取正确配置

确认参数：

base_url=https://openai.sufy.com/v1
model=anthropic/claude-4.7-opus
provider=deepseek
api_mode=chat_completions

七牛 API 直连预检通过：

模型列表包含 anthropic/claude-4.7-opus
chat 返回 QINIU_CLAUDE_OK

---

### G03：侦察当前主 Hermes

当时主 Hermes 状态：

主端口：8642
原模型：deepseek-v4-pro
原 base_url：api.deepseek.com

判断：

本次不是新建 worker，而是切换当前主 hermes-agent。

---

### G04：备份

备份目录：

H:\Hermes_Backups\TASK-20260513-QINIU-CLAUDE-MAIN-HERMES\

后续 G06U 又额外备份：

H:\Hermes_Backups\TASK-20260513-QINIU-CLAUDE-MAIN-HERMES\G06U_20260513_133548\

G06U 备份哈希：

3b23fc14f6b934c9438623d635d1224f1447976abbf9c1f2481b7f8f5eefa74d  config.yaml.bak
3601d9c543001998f0cc1e62c9ccb3f8e74567e64fc88f017910c2fdfe7163ac  .env.bak

---

### G05：最小修改主配置

修改文件：

~/.hermes/config.yaml
~/.hermes/.env

修改后配置证据：

provider: deepseek
default: anthropic/claude-4.7-opus
base_url: https://openai.sufy.com/v1
api_mode: chat_completions

---

### G06：首次重启失败

失败日志：

ERROR gateway.run: Another gateway instance PID 597 started during our startup. Exiting to avoid double-running.

判断：

不是 Claude 配置失败，而是 gateway 双实例竞争。

---

### G06S：清理竞争后仍失败

清理竞争进程后，配置证据已经正确：

provider: deepseek
default: anthropic/claude-4.7-opus
base_url: https://openai.sufy.com/v1
api_mode: chat_completions

但启动失败：

Telegram Primary api.telegram.org connection failed
Telegram Connect attempt failed: Timed out
G06S_FAIL_8642_NOT_LISTENING

判断：

Telegram 网络连接阻塞 gateway 启动。

---

### G06T：等待现有进程失败

等待后日志继续显示：

telegram connect timed out after 30s
Reconnect telegram error

判断：

不是单纯等待时间短，而是 Telegram 平台启动会阻塞主 gateway 可用性。

---

### G06U：临时禁用 Telegram 后主 8642 恢复

临时注释 .env 中 Telegram 相关变量：

TELEGRAM_BOT_TOKEN
TELEGRAM_ALLOWED_USERS
TELEGRAM_HOME_CHANNEL

证据：

G06U_TELEGRAM_LINES_DISABLED=3
G06U_8642_LISTENING_AT_SECOND=3
health 返回 {"status": "ok", "platform": "hermes-agent"}

判断：

主 8642 API 已恢复。Telegram 是本次启动阻塞点。

---

### G06U 中文验收误判说明

当时中文测试出现模型回复：

你好！看起来你发的是一串问号...

原因：

PowerShell 到 WSL 管道中的中文内容可能发生编码转换，导致模型收到问号或乱码。

所以不能用这次中文自报判断模型身份。

另外当时出现：

G06U_FAIL_STILL_DEEPSEEK

这是检测规则误判。原因是 provider 字段仍叫 deepseek，但真实 base_url 和 default model 已经是七牛 Claude。

---

### G07V：ASCII 哨兵词验收成功

使用纯英文 ASCII 请求：

Reply with exactly this text and nothing else: QINIU_CLAUDE_MAIN_ASCII_OK

返回：

QINIU_CLAUDE_MAIN_ASCII_OK

验收通过：

G07V_PASS_MAIN_QINIU_CLAUDE_OK

判断：

主爱马仕 8642 已可正常调用七牛 Claude。

---

### G08：Open WebUI 全链路验收成功

在 Open WebUI 中选择：

profile hermes-agent

发送：

Reply exactly: OPENWEBUI_HERMES_CLAUDE_OK

返回：

OPENWEBUI_HERMES_CLAUDE_OK

判断：

Open WebUI → hermes-agent → 主爱马仕 8642 → 七牛 Claude 全链路成功。

---

## 五、根因分析

这次失败不是主要由 DeepSeek V4 Pro 能力不足导致。

DeepSeek V4 Pro 已经完成：

搜索旧资料
提取成功路径
读取配置
找到 key
直连预检
备份
修改配置

真正失败点是：

执行体重启自己依赖的 gateway
没有外部监督脚本接管
Telegram 网络超时阻塞 gateway 启动

所以本质是自我重启任务设计问题，不是单纯模型能力问题。

---

## 六、以后成熟复用流程

以后要把某个模型接入主爱马仕，优先走这个流程：

S01 搜索旧成功案例和技能包
S02 提取 base_url / model / provider / api_mode
S03 直连 API 预检
S04 侦察当前主 Hermes
S05 备份 config.yaml 和 .env
S06 最小修改主配置
S07 先禁用或绕开 Telegram 等平台入口
S08 外部 PowerShell 重启主 8642
S09 /health 验收
S10 ASCII 哨兵词 chat 验收
S11 Open WebUI 中选择 hermes-agent 验收
S12 成功后写入 H 盘技能包复盘

---

## 七、以后禁止项

不要让爱马仕自己重启自己后继续判断。
不要把 Telegram 连接作为主 8642 启动的前置条件。
不要一开始用中文问题判断模型身份。
不要因为 provider 字段叫 deepseek 就判断实际仍是 DeepSeek。
不要在 G01-G05 已完成后重新探索。
不要重建 Open WebUI。
不要删除 Docker 容器。
不要删除 Docker volume。
不要动 worker-01~04。

---

## 八、新启动规则建议

主日用启动优先级：

第一优先级：主 8642 API
第二优先级：Open WebUI 3000
第三优先级：Telegram / 语音 / 机器人入口

时间预算：

Hermes 8642 等待至少 180 秒
Open WebUI 冷启动等待 180 到 300 秒
Telegram 网络等待不得阻塞主 8642 验收

第一轮验收优先用 ASCII：

Reply exactly: QINIU_CLAUDE_MAIN_ASCII_OK

Open WebUI 验收：

Reply exactly: OPENWEBUI_HERMES_CLAUDE_OK

---

## 九、回滚信息

G06U 备份目录：

H:\Hermes_Backups\TASK-20260513-QINIU-CLAUDE-MAIN-HERMES\G06U_20260513_133548\

对应 WSL 路径：

/mnt/h/Hermes_Backups/TASK-20260513-QINIU-CLAUDE-MAIN-HERMES/G06U_20260513_133548/

回滚思路：

把 config.yaml.bak 覆盖回 ~/.hermes/config.yaml
把 .env.bak 覆盖回 ~/.hermes/.env
再重启主 hermes-agent

注意：

除非需要恢复 Telegram，否则不要急着回滚 .env。
因为当前临时禁用 Telegram 是为了保证主 8642 稳定可用。

---

## 十、本次最终状态

主 8642：已恢复
主模型路线：七牛 Claude
Open WebUI：已验证
Telegram：临时禁用，待单独修复
worker-01~04：未纳入本次日用主线

最终通过标记：

TASK-20260513-QINIU-CLAUDE-MAIN-HERMES_PASS
