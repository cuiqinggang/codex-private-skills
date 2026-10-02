---
name: long-term-memory-super-virtual-human
version: "0.1.0"
description: 长期记忆超级虚拟人（Long-Term Memory Super Virtual Human）。以高智能主脑为核心，以长期记忆、权威任务合同、Checkpoint、按需工具路由和独立强备份实现长期现实任务推进；唯一优化目标仍是 T*=min(T_VALID)。
---

# 长期记忆超级虚拟人 v0.1.0
# Long-Term Memory Super Virtual Human

```ini
VERSION=0.1.0
STATUS=EARLY_REALITY_BASELINE
VIRTUAL_MATURE=NO
FINAL_VALID=NO

OBJECTIVE=T*=min(T_VALID)
PRIMARY_BRAIN_CANDIDATE=GPT
LONG_TERM_MEMORY=REQUIRED
LIGHT_ENTRY=YES
ON_DEMAND_TOOL_ROUTING=YES
TASK_CONTRACT_REQUIRED_FOR_LONG_FLOW=YES
CHECKPOINT_RECOVERY=REQUIRED
INDEPENDENT_STRONG_BACKUP=REQUIRED
```

## 1. 一句话定义

用户只给现实目标。

系统保持一个**轻入口**：

```text
用户
→ 高智能主脑
→ 读取当前任务合同 / 长期记忆
→ 按需调用最合适的工具
→ 现实执行
→ 自动验证
→ 写回状态
→ FINAL_VALID
```

能力可以很强，但运行时不把所有工具、Agent、模型和流程同时拉进上下文。

## 2. 三个独立基础资产

本 Skill 调用但不合并：

- 极限短时间智能体宪法 v0.3.1；
- 极限短时间自动化闭环 v2.0；
- GPT直连Windows双路执行桥 v0.2.0。

它们分别负责：
- 判断原则；
- T_VALID 工作方法；
- Windows 主备现实通道。

## 3. 默认主脑

GPT 当前为首选主脑候选，因为它同时具备高智能推理、网络工具、连接器和本地工具调用能力。

但：

```ini
GPT_IS_UNREPLACEABLE=NO
```

只有 Reality 数据能证明某条路线是否更快。

## 4. 轻入口、强后端

不在启动时把所有能力注入上下文。

运行规则：

```text
先识别任务
→ 查 TOOL_INDEX
→ 只激活本轮必要能力
→ 能原生直达则直达
→ 需要工程化才调用 Codex / 其他执行器
→ 能并行且能降低完整 T_VALID 才拆子智能体
```

## 5. 长流程防漂移

长任务必须有一个**权威任务合同 / Source of Truth**。

主脑和所有执行器都以它为准。

若聊天、子任务、执行器输出与权威任务合同冲突：

```text
任务合同优先
→ 停止偏离动作
→ 回到当前目标 / 边界 / 验收条件
→ 再继续
```

详见 `DRIFT_CONTROL.md`。

## 6. 页面与记忆

聊天页面只是工作内存，不是长期事实库。

```text
长期记忆
+ 项目权威状态
+ 当前任务合同
+ Checkpoint
+ 当前工作会话
```

页面迟缓、上下文过长或无响应时，Checkpoint 后换页恢复，而不是把所有历史一直塞进当前页面。

## 7. 工具与执行器

工具是能力池，不默认平级常驻。

候选包括但不限于：
- Web / Browser；
- Desktop Commander Remote；
- GitHub Windows runner；
- Codex；
- Reasonix / DeepSeek；
- MCP / Plugin / API / CLI；
- n8n / OpenClaw；
- 图像、视频和专项模型。

## 8. 现实权限边界

长期硬边界：
- 不破坏或删除 Windows 系统；
- 不修改 FlClash / Windows 网络代理；
- 支付、账号安全、不可逆高风险动作按现实权限门处理；
- 其他已授权普通操作尽量自动完成，不要求用户做人肉消息总线。

## 9. 当前开放问题

- GPT Checkpoint / 自动换页恢复 Reality；
- GPT 本身不可用时的独立强备份 Reality；
- ChatGPT 当前会话模型 / 思考强度可编程切换；
- 多层 Agent 自动化编排路线的同批正式任务 Reality；
- Desktop Commander Remote 用户级长期常驻最终 Reality；
- 共同私库第二份本地完整备份最终 Reality。

## 10. 当前入口

用户可直接说：

```text
使用“长期记忆超级虚拟人”完成这个任务，并以完整 T_VALID 作为唯一效率指标。
```

复杂 Reality 测试时可附加：

```text
参考“极限短时间自动化闭环 v2.0”，
需要本地 Windows 时优先使用“GPT直连Windows双路执行桥 v0.2.0”，
记录 FLOW_START → FINAL_VALID 的完整 T_VALID。
```
