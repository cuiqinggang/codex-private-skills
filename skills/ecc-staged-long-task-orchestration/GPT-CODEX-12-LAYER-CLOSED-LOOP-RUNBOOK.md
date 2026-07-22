# GPT-Codex 12 Layer Closed Loop Runbook

## 角色分工

```text
用户：发布任务，看最终结论。
GPT：制定 Claude-style 12 Layer 命令包，并做最终验收。
Codex 桌面端：操作电脑、执行命令、收集证据、回传给 GPT。
```

## 标准流程

```text
用户把任务发给 Codex 桌面端
↓
Codex 收集：
- 用户任务；
- 相关技能包；
- 当前环境信息；
- 工作区路径；
- 禁止事项；
- 验收要求。
↓
Codex 把这些内容发送给 GPT
↓
GPT 按 Claude-style 12 Layer 原顺序生成完整可执行命令包
↓
Codex 严格执行 GPT 命令包
↓
Codex 收集每层证据
↓
Codex 把执行回传包交给 GPT
↓
GPT 根据 Layer 9 Verification Plane 和 Layer 12 Final Acceptance 做最终验收
↓
Codex 根据 GPT 结论归档、修复或停止
↓
用户只看最终结论
```

## 关键规则

```text
1. Codex 不能自己重新发明流程。
2. Codex 不能把 12 Layer 改成普通 12 步。
3. Codex 不能只返回文件夹路径。
4. Codex 不能在 GPT 未验收前宣布最终完成。
5. GPT 生成命令包时必须显式写出 12 Layer。
6. GPT 验收时必须检查 Verification Plane 和 Final Acceptance。
```

## Codex 到 GPT 的回传边界

Codex 必须回传证据摘要，而不是只返回文件夹路径。

```text
只返回文件夹路径 = FAIL。
只返回“已完成” = FAIL。
没有核心证据摘要 = FAIL。
```

## GPT 最终验收边界

GPT 最终验收必须检查：

- 12 个 Layer 是否完整。
- Layer 6 是否只 claim，没有 self-accept。
- Layer 8 是否有 deterministic checks。
- Layer 9 是否有 acceptance / rejection。
- Layer 10 是否处理 rejected claims。
- Layer 12 是否有 final-acceptance.md 和 final-acceptance.json。
