# UltraFusion 6.1B Decision Log

## 2026-07-05: V7.0 Semi-Automatic ABCD Decision

- Decision: keep UltraFusion 6.1B as the official-site multi-model route and add UltraFusion V7.0 as an optional semi-automatic route.
- Route label: `UF_V7_SEMI_AUTO_ABCD`.
- Reason: the user defined a useful human-in-the-loop workflow where Codex prepares prompts, external models answer, and Codex owns fusion/scoring. This avoids disturbing the user's active browser while preserving A/B/C/D rigor.
- Human responsibility: copy and paste only.
- Codex responsibility: baseline scoring, package generation, layer validation, fusion, convergence, final scoring, and `Gain` verdict.
- Acceptance: `Gain = SCORE_FINAL - Score_0`; if `Gain < 2.0`, the chain is `INVALID_CHAIN`.

## Version

- Version: `UltraFusion-6.1B-2026-07-03`
- Theme: current official two-tier route correction
- Current official route: `普通问题 GPT 直答；高价值 / 极限答案问题 GPT 官网 + DeepSeek 官网 + 千问/Qwen 官网`
- Deprecated route: `GPT 官网版 + Kimi 官网会员版 + GLM-5.2 / GLM Coding Plan`

## Discussion Record

1. 用户纠正：此前读到的 `GPT + Kimi + GLM` 是旧路线，不是当前正式路线。
2. 当前正式有效版本是 UltraFusion 6.1B。
3. 当前固定两档路由：普通问题由 GPT / ChatGPT 官网直接回答；高价值 / 极限答案问题才进入 GPT + DeepSeek + 千问/Qwen 官网三模型。
4. 普通问题不使用 DeepSeek、千问/Qwen、V15、A/B/C/D、多模型融合、复杂验收。
5. 高价值问题需要额外模型、V15、多模型互审能够显著提高答案质量时，才进入 UltraFusion。
6. 官网测试应优先使用普通用户可见界面、坐标定位、一步一截图的方式；不默认调试接口、DOM、网页控制或一般用户不用的方法。
7. 若用户正在使用电脑，不得使用会抢占真实鼠标、键盘或前台焦点的输入方式。要么等待用户空档，要么改用隔离环境。
8. 允许的目标是稳定、低频、尊重官网规则地使用公开界面；不得绕过网站限制、隐藏自动化或规避检测。

## Final Conclusion

本次版本的核心结论是：

UltraFusion 6.1B 的正式路线调整为：

```text
第一档：普通问题 -> GPT / ChatGPT 官网直接回答
第二档：高价值 / 极限答案问题 -> GPT 官网 + DeepSeek 官网 + 千问/Qwen 官网
```

固定入口：

```text
GPT / ChatGPT: https://chatgpt.com/
DeepSeek Chat: https://chat.deepseek.com/
千问/Qwen: https://www.qianwen.com/
Qwen backup: https://chat.qwen.ai/
```

`GPT + Kimi + GLM` 是 deprecated / old route / not current official route，不作为 6.1B 测试标准。

本次测试目标：官网连通性 + 两档路由 + 三模型骨架流程 + 坐标一步一截图证据。若本地没有找到 V15_FULL，本轮只能标记 `NON_V15_SKELETON_TEST`，不能标记 `V15_FULL_CHAIN_PASS`。
