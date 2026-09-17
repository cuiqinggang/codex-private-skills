# H3-P0 Codex 容量路由接续记录 v1

## 背景

H3-P0 长任务再次出现：

```text
Selected model is at capacity. Please try a different model.
```

历史上已把“模型容量错误 != 本地任务失败”和“任务必须 checkpoint/resume”作为恢复原则，但此前没有把**容量感知动态模型选择器**固化为正式、可复用组件，因此当前 H3 进度链仍可能静态依赖某一 Codex 模型。

本文件补齐该缺口。

## 当前裁决

```text
CAPACITY_ERROR_CLASS=REMOTE_MODEL_CAPACITY
H3_GPU_RESULT_INVALIDATED=NO
RESEED_RECOVERY_RESULT_INVALIDATED=NO
LOCAL_WORK_REPLAY_REQUIRED=NO
```

容量错误发生在模型服务层，不得因此重复已经完成的本地 GPU、QC、Git 提交或远端核验。

## 新正式组件

全局 Skill：

```text
skills/codex-capacity-aware-model-router/SKILL.md
```

中文名：`Codex 容量感知动态模型选择器`

作用：

```text
动态模型目录
→ 极小健康 probe
→ 主模型容量不足时选下一个可用模型
→ checkpoint/resume
→ 保持业务命令包不变
```

## H3 接入要求

后续所有 H3-P0 Codex 长任务入口，在开始业务命令前先执行容量路由 preflight：

1. 读取当前 Codex 模型目录/缓存；
2. probe REQUESTED_MODEL；
3. capacity 时选择下一可用模型；
4. 写 `REQUESTED_MODEL / ACTUAL_MODEL / FALLBACK_REASON`；
5. 若全部模型 capacity，保存 checkpoint 并标为 `BLOCKED_REMOTE_CAPACITY`；
6. 不重跑已经完成的 H3 本地工作。

## 与当前质量稳定性任务关系

当前 `RESEED-UNTIL-PASS` 工作与模型路由是两层不同机制：

```text
RESEED-UNTIL-PASS
= H3 随机采样质量恢复

CAPACITY-AWARE MODEL ROUTER
= Codex 推理控制面的远端容量恢复
```

不得混为一个概率问题。

## 以后接续报告必须保留

任何新的 H3-P0 接续总结必须明确包含：

```text
CODEX_CAPACITY_ROUTER=ENABLED/NOT_INSTALLED/BLOCKED
REQUESTED_MODEL=<...>
ACTUAL_MODEL=<.../UNKNOWN>
FALLBACK_REASON=<.../NONE>
TASK_CHECKPOINT=<path>
LOCAL_WORK_REPLAY=NO
```

这样换页面/换模型/换会话后不会再次遗漏该修复。