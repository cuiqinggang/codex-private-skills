---
name: gpt-codex-convergence-orchestrator
description: GPT↔Codex 自动闭环执行技能。服从 first-principles-physical-limit-convergence v3.1.1 三核心。正常优先使用 GitHub 共同工作区；若 GitHub 写入被阻断、失败或明显异常，则立即切换为页面直传，不让偶发 transport 故障阻塞任务。GPT 始终负责业务规划/裁决，Codex 始终只负责执行。
metadata:
  version: "1.4.2"
  method_dependency: "first-principles-physical-limit-convergence@3.1.1"
  architecture: "GITHUB_PRIMARY_PAGE_FALLBACK"
---

# GPT↔Codex 自动闭环 v1.4.2

## 只保留一个简单原则

业务目标是：

~~~text
GPT 决定
Codex 执行
用户中间不搬运
尽快得到 VALID 结果
~~~

传输方式不是目标。

因此只有两条合法路径：

~~~text
A. GitHub 正常
   -> 用 GitHub 共同工作区

B. GitHub 写入失败 / 被安全检查阻断 / 明显异常
   -> 立即改用页面直传
~~~

没有第三条复杂恢复路线。

## 简单故障冗余

故障本身不是任务目标。对已理解范围内的普通故障，只允许：

~~~text
NORMAL PATH
-> 小故障
-> SIMPLE RECOVERY ONCE
-> 仍不通
-> SIMPLE FALLBACK
-> CONTINUE TASK
~~~

例如：

~~~text
GitHub 暂时写不了
-> 简单重试一次
-> 还不通
-> 页面直传
-> 任务继续
~~~

只有以下情况才真正 STOP：

~~~text
主路径不可用
AND
备用路径也不可用

或

继续会破坏 VALID / 安全 / 权限边界
~~~

禁止：

~~~text
为了修一个偶发 transport 故障无限排查
为每一种小故障新增一套协议
任务明明能走备用路却停机研究主路
把临时故障升级成系统重构
~~~

故障若以后反复成为常态，再单独解决；偶发故障只记录证据，不阻塞当前任务。

## 正常路径 A：GitHub

~~~text
Codex REQUEST -> GitHub
-> Browser wake GPT
-> GPT COMMAND -> GitHub
-> Codex execute
-> RESULT
-> GPT DECISION
-> STOP
~~~

GitHub 正常时继续把它作为共享事实源和证据区。

## fallback 路径 B：页面直传

以下任一发生，就直接切 B：

~~~text
GitHub write blocked
GitHub write safety check
GitHub write error
明显 transport 异常导致继续等待不划算
~~~

切换后：

~~~text
Codex / Browser
-> 把当前必要任务上下文直接发给 GPT 页面
-> GPT 页面直接返回 COMMAND 或 DECISION
-> Browser 原样读取
-> Codex 原样执行 / 消费
-> 继续任务
~~~

fallback 时允许 Browser 携带必要业务正文。

不要求 GPT 再写 GitHub。
不要求 Codex 为 GitHub 故障停机。
不要求先把共同工作区修好。

## 页面回复格式

COMMAND：

~~~text
GPT_COMMAND
<完整业务命令>
END_GPT_COMMAND
~~~

DECISION：

~~~text
GPT_DECISION
<完整裁决>
END_GPT_DECISION
~~~

Codex 只能原样读取和执行，不得改变业务语义。

## GitHub 恢复后的处理

任务过程中先完成任务。

如果之后 GitHub 已恢复，可以把最终结果/报告同步回共同仓库作为证据。

但：

~~~text
SYNC_BACK_FAILURE != TASK_FAILURE
~~~

偶发共同工作区故障不能阻塞主任务。

## GPT Thinking 首答超时

只看“是否开始回答”。

~~~text
简单任务 = 60 秒
普通任务 = 180 秒
大型复杂任务 = 600 秒
~~~

一旦正文开始：

~~~text
ANSWER_STARTED=YES
-> 正常
-> 不再按 Thinking timeout 刷新
~~~

始终没有开始正文并超过上限：

~~~text
refresh/reconnect
-> 重发同一请求
~~~

## 权限边界

无论走 A 还是 B：

~~~text
GPT_PLAN_AUTHORITY=YES
CODEX_PLAN_AUTHORITY=NONE
~~~

Codex 可以：

~~~text
传递
读取
执行
验证
记录
~~~

Codex 不可以：

~~~text
改 GPT 的业务方案
自己补新方案
自己决定下一研究方向
~~~

## 现实测试

新测试直接验证：

~~~text
GitHub 正常 -> A
GitHub 临时写不了 -> B
两条都能把任务完成
~~~

不再因为 transport 选择本身判整个业务失败。

# 最终一句话

> 正常路先走；小故障简单恢复一次；还不通就走备用路；能得到 VALID 结果就继续。只有主路和备用路都失效，才停下来处理故障。
