# GPT↔Codex 简洁灵活自动闭环 v1.5.1

## 核心

~~~text
GPT 决策
Codex 执行
Browser 负责页面传递
GitHub 共同工作区优先
~~~

但共同工作区不是唯一通道。

## 三条简单路径

~~~text
A  GitHub 完整通道（优先）
B  GitHub 读资料 + 页面回 COMMAND/DECISION
C  纯页面直传
~~~

规则很简单：

~~~text
A 能用 -> A
只写回坏 -> B
GitHub 整体暂时坏 -> C
~~~

不为了偶发 transport 故障停主任务，也不为每个故障设计新协议。

旧版本中“GitHub 必须成功”或“页面是唯一控制链”的两种极端都不再采用。
