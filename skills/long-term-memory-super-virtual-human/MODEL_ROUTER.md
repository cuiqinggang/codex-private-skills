# 长期记忆超级虚拟人｜模型与思考强度路由 v0.1

## 当前现实边界

当前 ChatGPT 页面自身的模型/思考档主要由产品侧模型选择器与账号设置控制。

```ini
SELF_CHATGPT_MODEL_SWITCH=NOT_PROGRAMMABLY_AVAILABLE
SELF_CHATGPT_THINKING_SWITCH=NOT_PROGRAMMABLY_AVAILABLE
EXTERNAL_MODEL_ROUTING=AVAILABLE_WHEN_INTERFACE_EXPOSES_MODEL
EXTERNAL_REASONING_ROUTING=AVAILABLE_WHEN_INTERFACE_EXPOSES_REASONING
PROGRAMMABLE_OPENAI_AGENT_RUNTIME=CANDIDATE
```

提示词要求“更深入思考”不能等价于真实切换 ChatGPT 产品侧思考档。

## 两种不同控制面

### A. 当前 ChatGPT 页面

这里没有一个可由本 Skill 直接调用的“切换我自己模型/思考档”工具。

因此不能伪装：
```text
Skill 写 HIGH
= ChatGPT UI 已经切到 High
```

### B. 可编程 Agent / API / 外部执行器

当运行时暴露参数时，可由路由器显式选择：
- model；
- reasoning effort / reasoning mode；
- service tier；
- 专项执行器自身的模型参数。

OpenAI Agents API 是成熟候选之一：其 session 可配置 model 与 reasoning，并可在现有 session 上更新 model / reasoning.effort；是否作为本项目未来主运行时，仍需 Reality 比较完整 T_VALID。

Codex / Reasonix / DeepSeek 等若暴露相应参数，也按同样原则处理。

## 正确路由结构

```text
用户目标
→ 当前主脑
→ 判断最低充分能力
→ 当前会话够用：直接完成
→ 可编程外部执行更快：显式选择 model / reasoning
→ Reality 验证
→ FINAL_VALID
```

## 选择原则

不默认“越强越好”，也不默认“越便宜越好”。

唯一效率目标仍是：
```text
先满足 VALID
→ 比较完整 T_VALID
→ T*=min(T_VALID)
```

简单任务优先少层直达；复杂、长流程、高返工风险任务可提升推理档或换更强模型。最终只保留 Reality 证明完整 T_VALID 更短的路由规则。

## 下一阶段 Reality

至少比较：
```text
当前 ChatGPT 主脑（用户选档）
vs
可编程 Agent：低/中/高 reasoning
vs
专项模型 / Codex / Reasonix
```

同一类真实任务记录从 FLOW_START 到 FINAL_VALID 的完整时间，不用单次模型响应速度代替。

## 当前开放项

若未来 ChatGPT 页面本身暴露可靠的会话内可编程模型/思考档切换接口，再升级 SELF_* 状态；在此之前不得伪装已经自动切换。
