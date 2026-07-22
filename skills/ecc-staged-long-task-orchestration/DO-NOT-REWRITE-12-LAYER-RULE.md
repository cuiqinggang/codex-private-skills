# Do Not Rewrite 12 Layer Rule

Claude-style 12 Layer 只能复刻，不能重写。

## 禁止事项

```text
不能改成普通 12 步。
不能改名、不能压缩、不能重解释。
不能替换成“目标确认 / 现状读取 / 风险识别 / 小步实现 / 回归验证”。
不能把 Layer 6 的 claim 当成 acceptance。
不能把 Verification Plane 省略。
不能把 Repair Loop 省略。
不能把 final-report 当 final acceptance。
不能只返回文件夹路径。
```

## 必须保留的英文层名

```text
Control Plane / Orchestrator
Short Entry / Memory
Skills / Progressive Disclosure
Planning / Work Decomposition
Subagents / Context Isolation
Execution Plane
Hooks / Lifecycle Triggers
Scripts / Deterministic Checks
Verification Plane
Repair Loop
Compact / Handoff
Final Acceptance
```

## 必须保留的中文名

```text
主控调度层
短入口 / 项目记忆层
技能按需加载 / 渐进加载层
任务拆解层
子智能体 / 上下文隔离层
执行平面
生命周期钩子层
脚本确定性检查层
独立验证平面
返修循环层
压缩交接层
最终验收层
```
## 中文详细执行标准

复杂长任务、2H / 8H endurance validation、SkillOpt、Run Guard 和 T8H official run 还必须读取：

```text
CLAUDE-CODE-12-LAYER-DETAILED-CHINESE-EXECUTION-STANDARD.md
```

不得只列 12 个标题；每层必须包含中文详细操作、文件要求、内容要求、禁止项、时间门槛关联、多智能体 / 上下文隔离要求、Verification Plane 接受条件和失败返回。
