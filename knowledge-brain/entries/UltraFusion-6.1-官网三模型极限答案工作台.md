# UltraFusion 6.1 知识库条目：官网三模型极限答案工作台

日期：2026-07-02

## 核心结论

UltraFusion 当前正式路线从 6.0 的：

```text
GPT 官网订阅版 + Kimi 官网会员版 + GLM-5.2 / GLM Coding Plan
```

修正为 6.1 的：

```text
GPT 官网版 + DeepSeek 官网版 + 千问/Qwen 官网版
```

## 角色分工

```text
GPT：主脑、总控、最终融合、最终验收、视觉/多模态入口。
DeepSeek：官网专家/深度模式，低成本深度分析、反方审稿、V15 极限答案模型。
千问/Qwen：官网 Qwen3.7-Max 优先，第三视角、中文资料补充、搜索补充、多样性审稿。
```

## 关键规则

1. 官网/官方产品质量优先，API 暂不进入当前极限答案主流程。
2. DeepSeek 只走官网，不走 API。
3. Kimi 降级为备用，只做少量高价值 Agent Swarm 标杆测试。
4. GLM-5.2 不进答案主链，仅作为工程执行候选。
5. 官网三模型组合是极限答案工作台，不是大规模自动化生产后端。
6. 公共服务路线拆成两层：官网极限质量层 + 未来工程服务层。
7. V15 必须粘贴完整 V15_FULL，不能只写“进入 V15 模式”。
8. 写入技能包/知识库后的成果必须经过三轮实际测试与截图验证。

## 路由触发词

```text
UltraFusion 6.1
官网三模型
极限答案工作台
GPT DeepSeek 千问
V15 A/B/C/D
低成本多模型融合
多智能体极限回答
DeepSeek 官网
Qwen3.7-Max
千问官网
```

## 待验证

```text
PENDING_V15_FULL_LOCATION
PENDING_QWEN_LIMIT_TEST
PENDING_DEEPSEEK_SEARCH_PREFIX_TEMPLATE
PENDING_THREE_ROUND_SCREENSHOT_VALIDATION
```

## 推荐写入本地知识库路径

```text
K:\AI\knowledge-brain\entries\UltraFusion-6.1-官网三模型极限答案工作台.md
```

如存在：

```text
K:\AI\knowledge-brain\INDEX.md
K:\AI\knowledge-brain\ROUTING_MAP.md
```

需要追加 UltraFusion 6.1 路由入口。
