---
name: github-issues-demand-mining
description: Use when the user wants to mine GitHub Issues for real user pain points, product opportunities, tutorial topics, bug patterns, feature requests, or unmet demand in AI tools, MCP, automation, developer tools, or open-source projects.
---

# GitHub Issues 需求挖掘

## 触发条件

- 用户要找真实需求、产品机会、教程选题、常见 bug、用户痛点。
- 用户已经有一个开源方向或仓库，想知道用户卡在哪里。
- 用户要判断某个工具是否值得做教程、服务、插件或替代方案。

## 执行流程

1. 明确主题或仓库范围。
2. 搜索未关闭且讨论热的 issue。
3. 分别查看 bug、enhancement、question、help wanted 等标签。
4. 把高评论 issue 按痛点、频率、影响范围、是否已有解决方案分类。
5. 输出可行动建议：教程选题、产品机会、避坑清单、待验证问题。

## 常用搜索式

```text
mcp is:issue is:open comments:>20
ai agent is:issue is:open comments:>20
repo:owner/name is:issue is:open comments:>10
repo:owner/name label:bug comments:>10
repo:owner/name label:enhancement comments:>10
```

## 边界条件

- 评论多不等于商业价值高，只说明讨论热。
- 老 issue 可能已被新版本解决，必须看最近回复和关闭状态。
- 不抓取私人信息，不把个人抱怨当成确定市场结论。

## 验收标准

至少列出 5 个高信号 issue 或问题簇；每个问题簇给出证据、解释和下一步验证方式。
