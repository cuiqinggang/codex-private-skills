# GPT↔Codex 简洁自动闭环 v1.5.0

这是按第一性原理重新整理后的最终简化方案。

## 核心

~~~text
GPT 决策
Browser 传递
Codex 执行
GitHub 可选同步
~~~

## 控制链

~~~text
Codex -> GPT 页面 -> GPT_COMMAND
-> Codex 执行 -> GPT 页面 -> GPT_DECISION
-> 继续或 STOP
~~~

GitHub 不再参与“任务能不能继续”的判定。

## 故障

~~~text
小故障
-> 简单恢复一次
-> 仍不通
-> 绕过/备用方式
-> 继续任务
~~~

只有页面主链本身也无法继续，才真正 STOP。

旧 v1.3/v1.4 的 GitHub Bus 强依赖、GPT 直写 GitHub、复杂 relay/ACK/Bus-write 安全处理全部降为历史证据，不再是当前方案。
