# 长期记忆超级虚拟人｜模型与思考强度路由 v0.1

## 当前现实边界

当前 ChatGPT 会话的模型/思考档主要由产品侧模型选择器控制。

```ini
SELF_CHATGPT_MODEL_SWITCH=NOT_PROGRAMMABLY_AVAILABLE
SELF_CHATGPT_THINKING_SWITCH=NOT_PROGRAMMABLY_AVAILABLE
EXTERNAL_MODEL_ROUTING=AVAILABLE_WHEN_INTERFACE_EXPOSES_MODEL
EXTERNAL_REASONING_ROUTING=AVAILABLE_WHEN_INTERFACE_EXPOSES_REASONING
```

提示词要求“更深入思考”不能等价于真实切换产品侧思考档。

## 正确路由结构

```text
用户目标
→ 当前主脑
→ 判断任务所需能力
→ 当前会话够用：直接完成
→ 外部执行更快：按接口显式选择模型/推理档
→ Reality 验证
→ FINAL_VALID
```

可被显式路由的对象包括：API Agent、Codex/Reasonix/DeepSeek 等暴露 model/reasoning 参数的执行器。

## 选择原则

不默认“越强越好”，也不默认“越便宜越好”。

唯一效率目标仍是：
```text
先进入 VALID 候选集
→ 比较完整 T_VALID
→ T*=min(T_VALID)
```

模型档位只是候选路径的一部分。简单任务优先少层直达；复杂、长流程、高返工风险任务可提升推理档或换更强模型，直到 Reality 证明哪条完整路径更短。

## 当前开放项

若未来 ChatGPT 暴露可靠的会话内可编程模型/思考档切换接口，再把 SELF_* 状态升级；在此之前不得伪装已经自动切换。
