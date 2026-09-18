---
name: gpt-codex-convergence-orchestrator
description: GPT↔Codex 简洁灵活自动闭环。服从 first-principles-physical-limit-convergence v3.1.2 三核心。共同工作区优先，但不是唯一；按当前可用性在“共同工作区完整通道 / 共同工作区读+页面回传 / 纯页面直传”三条简单成熟路径之间切换。GPT 决策，Codex 执行，偶发 transport 故障只切路，不把简单任务变成故障工程。
metadata:
  version: "1.5.2"
  method_dependency: "first-principles-physical-limit-convergence@3.1.2"
  architecture: "PREFERRED_SHARED_WORKSPACE_WITH_SIMPLE_FALLBACKS"
---

# GPT↔Codex 简洁灵活自动闭环 v1.5.2

## CORE 1 — 极限短时间

目标：

~~~text
Codex 接到任务
-> 自动获得 GPT 的正确方案/判断
-> Codex 执行
-> 得到第一个 VALID 结果
~~~

唯一优化：

~~~text
T_VALID
~~~

传输方式只服务于更快、更稳地得到 VALID，不是目标本身。

VALID：

~~~text
GPT 负责规划/判断
Codex 负责执行
用户中间复制粘贴 = 0
结果正确
无重复业务副作用
偶发 transport 故障不无意义阻塞主任务
~~~

## CORE 2 — 成熟方案集群

直接复用已经成熟、已经真实使用过的能力：

~~~text
GitHub 共同工作区
Playwright Native AI Browser
ChatGPT 页面
Codex 本机执行
现有本机简单去重/恢复
~~~

它们不是只能组成一条固定链，而是组成几条都很简单的可切换路径。

## CORE 3 — 冻结的灵活路径

### PATH A — 共同工作区完整通道（默认优先）

适合：

~~~text
资料较大
需要跨页面/跨会话共享
需要长期证据
GitHub 读写都正常
~~~

流程：

~~~text
Codex -> 把 TASK / RESULT / 大资料放入共同工作区
-> Browser 给 GPT 最小指针
-> GPT 直接读取共同工作区
-> GPT 把 COMMAND / DECISION 写回共同工作区
-> Codex 读取并执行
~~~

这是优先路径，因为共同工作区对大资料、跨页面、证据和长期积累很有价值。

### PATH B — 共同工作区读取 + 页面回传

适合：

~~~text
GitHub 读取正常
但 GPT 写回共同工作区临时失败 / 被安全检查阻断
~~~

流程：

~~~text
Codex -> TASK / RESULT / 大资料仍放共同工作区
-> Browser 给 GPT 最小指针
-> GPT 读取共同工作区
-> GPT 直接在页面返回 COMMAND / DECISION
-> Browser 原样读取
-> Codex 执行
~~~

这样共同工作区的大资料价值仍然保留，只绕过“写回”这一小段临时故障。

### PATH C — 纯页面直传

适合：

~~~text
GitHub 整体暂时不可读/不可用
或继续等待共同工作区明显不划算
~~~

流程：

~~~text
Codex / Browser -> 直接把当前必要上下文发给 GPT 页面
-> GPT 页面返回 COMMAND / DECISION
-> Browser 原样读取
-> Codex 执行
~~~

只传当前步骤真正需要的上下文，不把整个历史都塞进页面。

## 路径选择只有三条规则

~~~text
1. 能正常使用共同工作区 -> 优先 PATH A
2. 只写回有问题 -> 立即 PATH B
3. 共同工作区整体临时不可用 -> 立即 PATH C
~~~

不建立复杂路由器，不做长期故障诊断后才允许切路。

下一轮/下一自然步骤如果共同工作区已经恢复，可以自然回到 PATH A；不需要专门做恢复工程。

## 页面输出

页面回传时只需要两个简单边界：

~~~text
GPT_COMMAND
<完整业务命令>
END_GPT_COMMAND
~~~

或：

~~~text
GPT_DECISION
<完整判断；必要时下一命令或 STOP>
END_GPT_DECISION
~~~

Codex 原样读取，不修改业务语义。

## 简单故障处理

统一原则：

~~~text
正常路径
-> 出现已知小故障
-> 简单恢复一次
-> 仍不通
-> 切到下一条简单可用路径
-> 主任务继续
~~~

### GitHub

~~~text
短暂网络/TLS异常 -> 简单重试一次
GPT write safety/block -> 不反复重试，直接 PATH B
GitHub 整体不可用 -> PATH C
~~~

### Browser

~~~text
refresh/reconnect 一次
-> 仍异常则重新打开正式 Browser 入口
-> 继续同一请求
~~~

### GPT 一直“正在思考”

只限制开始回答以前：

~~~text
简单任务 60 秒
普通任务 180 秒
大型复杂任务 600 秒
~~~

正文一旦开始：

~~~text
ANSWER_STARTED=YES
-> 视为正常
~~~

一直没有开始正文且超时：

~~~text
refresh/reconnect
-> 重发同一请求
~~~

## 什么时候才真正 STOP

只有：

~~~text
PATH A / B / C 都无法把任务继续
或
继续会破坏 VALID
或
登录/验证码/敏感权限/安全边界
或
用户 STOP
~~~

普通网络抖动、GitHub 写入阻断、页面一次异常都不是停机理由。

## 权限边界

~~~text
GPT_PLAN_AUTHORITY=YES
CODEX_PLAN_AUTHORITY=NONE
~~~

Codex 只允许：

~~~text
准备/传递上下文
读取 GPT 输出
执行
验证
记录
在路径之间按客观可用性切换
~~~

Codex 不允许：

~~~text
修改 GPT 的业务语义
自行补业务方案
因为 transport 故障改变业务目标
~~~

## 最小状态

只保留：

~~~text
TASK_ID
CURRENT_STEP
ACTIVE_PATH=A|B|C
LAST_GPT_COMMAND_HASH
LAST_RESULT
DONE
~~~

不建立复杂状态机。

# 最终一句话

> **共同工作区优先但不唯一；写回坏了走页面回传，整个工作区坏了走纯页面。三条都是简单成熟路径，按可用性切换，始终优先完成 VALID 任务。**
