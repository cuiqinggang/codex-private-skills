# GPT↔Codex 最终简化方案 v1

状态：

~~~text
METHOD=first-principles-physical-limit-convergence v3.1.1
CORE_1=COMPLETE
CORE_2=COMPLETE
CORE_3=FROZEN
REAL_EXECUTION=NOT_STARTED_FOR_THIS_PLAN
~~~

## 1. 为什么重新做

前面已经获得足够现实信息：

- GPT 页面和 Browser 直接交流长期可用；
- Codex 本机执行可靠；
- GitHub 共同工作区有价值，但会偶发写入/权限/transport 问题；
- 把 GitHub 变成控制链硬依赖后，偶发故障会把简单任务拖成复杂故障处理；
- GPT 直接写 GitHub 还可能触发外部写安全检查；
- 这些故障不影响“GPT 做决定、Codex 执行”这个本质能力。

因此重新按三核心设计。

## 2. CORE 1 — 极限短时间

TASK：

~~~text
让 Codex 自动向 GPT 获取方案/判断并执行，
用户不在中间搬运文本，
尽快得到第一个正确 VALID 结果。
~~~

唯一指标：

~~~text
T_VALID
~~~

任何传输方案都只服务于缩短 T_VALID。

## 3. CORE 2 — 成熟方案集群

直接采用已有成熟能力：

~~~text
Playwright Native AI Browser
ChatGPT 页面
Codex 本机执行
现有本机去重/恢复
GitHub 共同工作区
~~~

其中 GitHub 只保留它最擅长的用途：

~~~text
记录
共享
证据
备份
跨页面参考
~~~

不让它承担“控制链必须在线”的责任。

## 4. CORE 3 — 最终路径

### 4.1 控制主链

~~~text
Codex 准备必要上下文
-> Browser 发给 GPT 页面
-> GPT 返回 GPT_COMMAND
-> Browser 原样读取
-> Codex 执行 + 验证
-> Browser 把 RESULT 发给 GPT
-> GPT 返回 GPT_DECISION
-> Browser 原样读取
-> Codex 继续下一步或 STOP
~~~

这是唯一控制主链。

### 4.2 GPT 输出

命令：

~~~text
GPT_COMMAND
<完整业务命令>
END_GPT_COMMAND
~~~

判断：

~~~text
GPT_DECISION
<完整判断；必要时包含下一命令或 STOP>
END_GPT_DECISION
~~~

Codex 不修改其中业务语义。

### 4.3 GitHub

GitHub 不在控制链中。

每一步如果方便：

~~~text
Codex -> mirror 当前 TASK / COMMAND / RESULT / DECISION 到 GitHub
~~~

同步失败：

~~~text
记录 GITHUB_SYNC_SKIPPED
-> 继续主任务
~~~

任务完成后再补同步也可以。

### 4.4 故障处理

只允许简单处理：

~~~text
正常
-> 故障
-> 简单恢复一次
-> 仍失败
-> 最简单备用方式
-> 继续
~~~

具体：

GPT 长时间没开始回答：

~~~text
simple 60s
normal 180s
large 600s
-> 超时 refresh/reconnect
-> 重发同一请求
~~~

正文一旦开始就算正常。

Browser 异常：

~~~text
refresh/reconnect
-> 必要时重新打开正式 Browser 入口
-> 继续同一请求
~~~

GitHub 异常：

~~~text
跳过同步
-> 继续
~~~

### 4.5 STOP 条件

只有：

~~~text
页面通信本身也无法恢复
VALID 会被破坏
安全/权限边界
用户 STOP
~~~

才停。

## 5. 明确删除的复杂性

当前方案不再要求：

~~~text
GPT 直接 GitHub write
四消息 GitHub Bus 作为控制主链
ACK 与 DECISION transport 协议
GitHub write safety recovery
复杂 relay state machine
L0/L1/L2/L3/L4
为了偶发 transport 故障停主任务
~~~

这些历史资料可以保留，但没有当前执行权。

## 6. 最小实现

现有工程只需要保留/实现：

~~~text
Browser send
Browser read
GPT_COMMAND parser
GPT_DECISION parser
Codex execute
result verify
minimal local state
optional GitHub mirror
simple timeout/reconnect
~~~

没有必要再增加新的基础设施。

## 7. 当前结论

方案已经完整。

下一阶段如果要现实执行，应直接按本方案实现/整理现有工程，然后做一次端到端真实运行；不再回头继续设计 transport 协议。

# 一句话

> GPT 页面负责想和说，Browser 负责传，Codex 负责做，GitHub 能记就记；偶发故障简单绕过，始终优先完成任务。
