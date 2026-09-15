# EXECUTION BRIDGE（执行桥梁）

本文件只定义分布式执行基础设施，不增加方法层级，也不复制浏览器 Skill。

## 闭环角色

```text
METHOD（方法）= 第一性原理四列法 + 99 + 去重甲
REASONING_BRAIN（推理大脑）= ChatGPT_Web
EXECUTOR（执行器）= Codex
SHARED_FACT_SOURCE（共同事实源）= cuiqinggang/codex-private-skills
BRIDGE（通信桥）= playwright-native-ai-browser
```

推理大脑负责四列分析、物理因果模型和裁决；执行器负责本机检查、改动、真实验证、证据与 Git；GitHub 保存双方可重新读取的事实；浏览器只负责本机与网页推理大脑之间的通信。

## 自动循环

1. Codex 读取任务与共同仓库最新状态。
2. 专用浏览器恢复 ChatGPT 会话。
3. ChatGPT 读取共同事实并执行四列分析。
4. ChatGPT 输出一个明确的下一动作。
5. Codex 执行并做最小真实验证。
6. Codex 把 NEW BEST、NEW FAILURE、NEW FAST PATH、ROOT CAUSE、METHOD CHANGE、99 REOPEN 或 NEW 99 FREEZE 写入共同仓库。
7. ChatGPT 重新读取，给出 KEEP、ROLLBACK、NEXT 或 99 / FREEZE。
8. 循环。

禁止“GPT 一次给几十步、Codex 长时间盲跑”。高价值决策点必须重新回到推理大脑。

## 已只读核验的固定入口

- 权威项目：`C:\AI\Playwright-Native-AI-Browser`
- 权威 Skill：`C:\AI\Playwright-Native-AI-Browser\skills\playwright-native-ai-browser\SKILL.md`
- Codex 薄入口：`C:\Users\A\.codex\skills\playwright-native-ai-browser`
- Reasonix / agents 薄入口：`C:\Users\A\.agents\skills\playwright-native-ai-browser`
- MCP：`playwright_native_ai_browser`
- 真实业务入口：`C:\AI\Playwright-Native-AI-Browser\skills\playwright-native-ai-browser\scripts\chatgpt-business-entry.js`

2026-09-15 核验结果：上述项目、Skill、两个薄入口、MCP 与真实业务入口均存在。原先省略 `skills\playwright-native-ai-browser` 的项目根脚本路径不存在，已记录为 FI-13。

出现浏览器故障时，读取权威 `SKILL.md` 并按其故障路径处理；不得在本技能复制实现或建立第二套正式浏览器 Skill。
