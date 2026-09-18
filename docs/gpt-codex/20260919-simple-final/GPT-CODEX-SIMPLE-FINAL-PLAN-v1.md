# GPT↔Codex 最终简洁灵活方案 v2

状态：

~~~text
METHOD=first-principles-physical-limit-convergence v3.1.1
CORE_1=COMPLETE
CORE_2=COMPLETE
CORE_3=FROZEN
REAL_EXECUTION=NOT_STARTED_FOR_V1_5_1
~~~

## 1. 这次修正什么

v1.5.0 把页面直传写成了唯一控制主链，这又走到了另一个极端。

现实上：

- GitHub 共同工作区长期很有价值；
- 大资料、跨页面、证据、长期记录放共同工作区最方便；
- 多数时候 GitHub 是正常的；
- 偶发网络、写入或安全检查故障属于可理解的小故障；
- 这些故障不应该让任务失败；
- 页面直传本身也是长期成熟的快捷路径。

因此最终方案不是“一条唯一链”，而是“几条都很简单的成熟路径，优先共同工作区，故障时快速切换”。

## 2. CORE 1 — 极限短时间

TASK：

~~~text
Codex 自动向 GPT 获取方案/判断并执行，
用户不在中间搬运，
尽快得到第一个正确 VALID 结果。
~~~

唯一指标：

~~~text
T_VALID
~~~

任何路径只按“是否更快、更稳地达到 VALID”判断。

## 3. CORE 2 — 成熟方案集群

直接采用：

~~~text
GitHub 共同工作区
Playwright Native AI Browser
ChatGPT 页面
Codex 本机执行
现有简单去重/恢复
~~~

不新建新的 transport 基础设施。

## 4. CORE 3 — 三条简单路径

### PATH A — 共同工作区完整通道（默认）

~~~text
Codex 把 TASK / RESULT / 大资料放 GitHub
-> Browser 给 GPT 指针
-> GPT 读 GitHub
-> GPT 写 COMMAND / DECISION 到 GitHub
-> Codex 读并执行
~~~

适合绝大多数正常情况。

### PATH B — 共同工作区读取 + 页面回传

如果：

~~~text
GitHub 读正常
但 GPT 写回临时失败 / 被 safety check 阻断
~~~

则：

~~~text
TASK / RESULT / 大资料仍放 GitHub
-> GPT 继续从 GitHub 读取
-> COMMAND / DECISION 直接在页面返回
-> Browser 读取
-> Codex 执行
~~~

不放弃共同工作区，只绕开出故障的“写回”一小段。

### PATH C — 纯页面直传

如果：

~~~text
GitHub 整体暂时不可用
或继续等待明显不划算
~~~

则：

~~~text
Browser 直接把当前必要上下文发 GPT
-> GPT 页面返回 COMMAND / DECISION
-> Browser 读取
-> Codex 执行
~~~

只带当前步骤需要的信息。

## 5. 路径切换

只有：

~~~text
A 正常 -> A
A 写回失败但还能读 -> B
GitHub 整体不可用 -> C
~~~

每个小故障最多简单恢复一次。

不通就切路，不反复修 transport。

下一自然步骤发现共同工作区恢复，可以自然回 A。

## 6. 故障处理

统一：

~~~text
正常
-> 已知小故障
-> 简单恢复一次
-> 仍失败
-> 下一条简单路径
-> 继续任务
~~~

GPT 首答：

~~~text
simple 60s
normal 180s
large 600s
~~~

只限制开始回答以前；正文开始即正常。

## 7. GitHub 的价值

GitHub 不是必须永远在线，但仍然是优先路径，因为它最适合：

~~~text
大资料
长上下文
跨页面
跨会话
证据
长期积累
共享报告
~~~

所以不是“能记就记”的边缘角色，而是“优先使用、故障可绕过”的共享工作区。

## 8. STOP

只有：

~~~text
A/B/C 都走不通
VALID 会被破坏
安全/权限边界
用户 STOP
~~~

才停。

## 9. 删除复杂性

当前不再需要：

~~~text
把任何单一 transport 设成唯一
为了 GitHub 偶发故障重构系统
复杂 ACK/relay 状态机
每个小故障一套协议
L0/L1/L2/L3/L4
~~~

保留成熟能力，删掉硬绑定。

## 10. 当前结论

方案已经重新冻结。

下一阶段如果现实执行，只需要实现/整理：

~~~text
PATH A
PATH B
PATH C
简单切换
首答 timeout
最小去重
~~~

不再继续设计 transport。

# 一句话

> **共同工作区优先，但不是唯一；能读写走 A，只写回坏走 B，整体暂时坏走 C。三条都简单、都成熟、都服务于最短 VALID。**
