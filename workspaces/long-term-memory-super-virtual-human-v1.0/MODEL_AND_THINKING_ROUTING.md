# 长期记忆超级虚拟人｜模型与思考强度路由 v1.0

## 当前现实

截至 2026-10-02，ChatGPT 的模型 / 思考强度主要由产品侧模型选择器和设置控制。

不能假定：
- 在提示词里写“切到高思考”就等于真实切换 UI 档位；
- 当前聊天中的 GPT 可以任意编程控制自身模型选择器；
- 所有账号 / 计划具有相同自动切换行为。

```ini
CHATGPT_SELF_MODEL_SWITCH=NOT_PROGRAMMABLY_CERTIFIED
CHATGPT_SELF_THINKING_SWITCH=NOT_PROGRAMMABLY_CERTIFIED
EXTERNAL_MODEL_ROUTING=AVAILABLE_WHEN_TOOL_OR_API_EXPOSES_MODEL_SELECTION
```

## 当前策略

1. ChatGPT 主脑使用用户当前选定的最低充分档位；
2. 复杂度明显升级时，可建议/要求切换更高思考档，但不伪装已经自动切换；
3. 如果专项工具、API、Codex、Reasonix 或其他执行器允许显式选模型，则由主脑按任务路由；
4. 同一现实任务如果需要比较模型档位，必须记录完整 T_VALID，而不是只看单次回答速度；
5. 未来若 ChatGPT 提供可靠的可编程模型/思考档切换接口，再升级此能力状态。

## 不消失项

这是长期项目的明确开放问题，直到得到 Reality 证明前保持：

`MODEL_AND_THINKING_AUTOMATION=OPEN`
