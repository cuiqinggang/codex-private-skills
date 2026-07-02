# UltraFusion 6.1B 知识库条目：两档路由 + 官网三模型极限答案工作台

日期：2026-07-02
版本：6.1B

## 核心结论

UltraFusion 当前最终路由只保留两档：

```text
第一档：普通问题 -> GPT 直接回答
第二档：高价值 / 极限答案问题 -> GPT 官网 + DeepSeek 官网 + 千问/Qwen 官网
```

普通问题不是指问题一定简单，而是指：

```text
GPT 本身已经能给出足够有价值的答案；
再调用 DeepSeek、千问/Qwen、V15、多模型融合，也不会显著增加答案质量。
```

这种问题直接由 GPT 回答，不启动多模型流程。

## 两档路由规则

### 1. 普通问题

执行：

```text
用户问题 -> GPT 直接回答 -> 结束
```

不使用：

```text
DeepSeek
千问/Qwen
V15
A/B/C/D
三模型融合
复杂验收
```

### 2. 高价值 / 极限答案问题

只有当额外模型和 V15 能显著提升回答质量时，才进入 UltraFusion。

触发条件：

```text
高价值问题；
复杂决策；
用户明确要求极限答案；
单 GPT 可能不够；
需要不同模型互审；
需要写入技能包、知识库、命令包、长期规则或工程方案。
```

使用：

```text
GPT 官网版：主脑、总控、最终融合、最终验收。
DeepSeek 官网版：深度分析、反方审稿、高价值问题补深度。
千问/Qwen 官网版：第三视角、中文资料补充、搜索补充、多样性审稿。
```

## V15 边界

```text
普通问题不用 V15。
只有高价值 / 极限答案 / 技能包 / 知识库 / 命令包 / 长期规则类任务，才使用 V15_FULL。
```

使用 V15 时必须粘贴完整 V15_FULL，不能只写“进入 V15 模式”。

## 模型状态

```text
GPT：默认入口，普通问题直接回答，高价值问题最终融合。
DeepSeek：只走官网，不走 API，只在高价值流程中使用。
千问/Qwen：进入高价值流程，优先 Qwen3.7-Max。
Kimi：降级备用，仅高价值 Agent Swarm 标杆测试。
GLM-5.2：不进答案主链，仅工程执行候选。
API：暂不进入当前极限答案主流程。
```

## 路由触发词

```text
UltraFusion 6.1B
两档路由
普通问题 GPT 直接回答
高价值问题 官网三模型
极限答案工作台
GPT DeepSeek 千问
V15 FULL
A/B/C/D
Qwen3.7-Max
DeepSeek 官网
千问官网
```

## 推荐本地写入路径

```text
K:\AI\knowledge-brain\entries\UltraFusion-6.1B-两档路由-官网三模型极限答案工作台.md
```

如存在：

```text
K:\AI\knowledge-brain\INDEX.md
K:\AI\knowledge-brain\ROUTING_MAP.md
```

需要追加 UltraFusion 6.1B 路由入口。

## 验收状态

```text
GitHub：已写入
本地知识库：等待 Codex 写入 K 盘
最终验收：PENDING_THREE_ROUND_SCREENSHOT_VALIDATION
```
