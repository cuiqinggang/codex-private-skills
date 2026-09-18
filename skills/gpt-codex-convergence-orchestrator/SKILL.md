---
name: gpt-codex-convergence-orchestrator
description: GPT↔Codex 简洁自动闭环。服从 first-principles-physical-limit-convergence v3.1.1 三核心。控制链只依赖现有 Playwright Native AI Browser 页面通信：GPT 决策，Codex 执行。GitHub 共同工作区只作为可选同步/证据区，任何 GitHub 写入故障都不得阻塞主任务。
metadata:
  version: "1.5.0"
  method_dependency: "first-principles-physical-limit-convergence@3.1.1"
  architecture: "PAGE_DIRECT_CONTROL_GITHUB_OPTIONAL_MIRROR"
---

# GPT↔Codex 简洁自动闭环 v1.5.0

## CORE 1 — 极限短时间

目标只有一个：

~~~text
Codex 接到任务
-> GPT 给出正确方案/命令
-> Codex 执行
-> GPT 判断结果
-> 得到第一个 VALID 结果
~~~

唯一优化：

~~~text
T_VALID = 上述完整闭环耗时
~~~

VALID：

~~~text
GPT 负责业务规划/判断
Codex 负责确定性执行
用户中间复制粘贴 = 0
结果正确
无重复业务副作用
故障不会无意义阻塞主任务
~~~

## CORE 2 — 成熟方案集群

直接复用已经成熟、已经真实使用过的能力：

~~~text
Playwright Native AI Browser
= GPT 页面自动发送 / 读取

ChatGPT 页面
= GPT 规划与判断

Codex
= 本机执行器

现有本机状态/去重能力
= 防止同一命令重复执行

GitHub 共同工作区
= 可选共享记录 / 证据 / 备份
~~~

不再把 GitHub 写入作为控制链硬依赖。

## CORE 3 — 最终冻结方案

唯一控制链：

~~~text
1. Codex 准备当前任务/结果所需的最小完整上下文

2. Browser 直接发送到 GPT 页面

3. GPT 页面返回：
   GPT_COMMAND
   <完整命令>
   END_GPT_COMMAND

4. Browser 原样读取

5. Codex 原样执行
   -> 验证现实结果

6. Browser 把执行结果直接发给 GPT

7. GPT 页面返回：
   GPT_DECISION
   <裁决；必要时给下一命令或 STOP>
   END_GPT_DECISION

8. Codex 原样消费

9. 若还需继续：
   回到第 1 步

10. 达到 VALID：
    STOP
~~~

没有 GitHub 才不能继续的条件。

## GitHub 的唯一地位

GitHub 只做：

~~~text
MIRROR
EVIDENCE
BACKUP
SHARED_REFERENCE
~~~

Codex 在方便时可以把：

~~~text
TASK
GPT_COMMAND
RESULT
GPT_DECISION
FINAL_REPORT
~~~

同步到共同工作区。

但：

~~~text
GITHUB_SYNC_FAIL != TASK_FAIL
GITHUB_WRITE_BLOCKED != TASK_FAIL
GITHUB_UNAVAILABLE != TASK_FAIL
~~~

同步失败时：

~~~text
记录一次
-> 跳过同步
-> 主任务继续
~~~

任务完成后，如果 GitHub 已恢复，再补同步即可。

## 简单故障处理

故障处理永远保持：

~~~text
正常执行
-> 小故障
-> 简单恢复一次
-> 仍不通
-> 用最简单备用方式继续
~~~

### GPT 一直“正在思考”

只判断“开始回答以前”。

固定标准：

~~~text
简单任务：60 秒
普通任务：180 秒
大型复杂任务：600 秒
~~~

一旦 GPT 开始正常正文：

~~~text
ANSWER_STARTED=YES
-> 正常
-> 不再触发 Thinking 超时
~~~

一直没有开始正文并超时：

~~~text
refresh/reconnect
-> 重发同一请求
~~~

仍不行：

~~~text
同一登录 profile 新页面/新会话
-> 重发同一请求
~~~

不要继续无限等待。

### Browser 临时异常

~~~text
刷新/重连一次
-> 仍异常则重新打开正式 Browser 入口
-> 继续同一任务
~~~

### GitHub 临时异常

~~~text
跳过
-> 主任务继续
~~~

## 只有什么时候才 STOP

只有：

~~~text
页面直传本身也无法继续
或
继续会破坏 VALID
或
遇到登录/验证码/敏感权限/安全边界
或
用户 STOP
~~~

普通 transport 故障不值得停主任务。

## 权限边界

~~~text
GPT_PLAN_AUTHORITY=YES
CODEX_PLAN_AUTHORITY=NONE
~~~

Codex 可以：

~~~text
发送上下文
读取 GPT 输出
执行
验证
记录
可选同步 GitHub
~~~

Codex 不可以：

~~~text
修改 GPT 的业务语义
自行补新方案
自己改变研究方向
因为 transport 故障重新设计业务路线
~~~

## 最小状态

只需保留：

~~~text
TASK_ID
CURRENT_STEP
LAST_GPT_COMMAND_HASH
LAST_RESULT
DONE
~~~

目的是避免重复执行，不建立复杂状态机。

# 最终一句话

> **GPT 页面是控制通道，Codex 是执行器，GitHub 只是可选共同记录区；小故障简单恢复，恢复不了就绕过，始终优先把 VALID 任务做完。**
