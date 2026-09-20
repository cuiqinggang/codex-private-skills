# Distribution Note — v3.1.4

v3.1.4 只增加一个轻量任务定位协议，不增加第四核心、不增加第四步骤。

唯一白名单仍然是：

```text
1. 极限短时间
2. 成熟方案集群
3. 高智能虚拟成熟
```

新增定位标签只回答：

```text
哪个页面
哪个中文任务
第几个命令
当前 STEP
对应 CORE
ORDER 还是 ANSWER
当前状态
```

ORDER/ANSWER 必须以 `页 + 任务 + 序 + STEP + CORE` 精确配对。

正常目标 001..003 闭环；003 后未完成先记录原因；004..006 为修复窗口；006 后仍未完成则 STOP 并重新建立任务，不继续 007。

正式分支：

`codex/first-principles-physical-limit-convergence-v3.1.4`
