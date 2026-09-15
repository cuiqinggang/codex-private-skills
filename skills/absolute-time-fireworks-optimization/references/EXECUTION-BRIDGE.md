# EXECUTION BRIDGE（执行桥梁）

本文件只定义分布式执行基础设施，不增加方法层级，也不复制浏览器 Skill。

## 闭环角色

```text
METHOD（方法）= 第一性原理四列法 + 99 + 去重甲
REASONING_BRAIN（推理大脑）= ChatGPT_Web
EXECUTOR（执行器）= Codex
SHARED_FACT_SOURCE（共同事实源）= cuiqinggang/codex-private-skills
SHARED_REPO_LOCAL（本地共同仓库）= C:\Users\A\Documents\Codex\codex-private-skills
BRIDGE（通信桥）= playwright-native-ai-browser
```

ChatGPT 负责 reasoning / four-column / decision；Codex 负责 local execution / test / evidence / Git publication；GitHub 是 persistent shared fact source；浏览器只负责本机与网页推理大脑之间的通信。

## 自动循环

1. Codex 读取任务与共同仓库最新状态。
2. 专用浏览器恢复 ChatGPT 会话。
3. ChatGPT 读取共同事实并执行四列分析。
4. ChatGPT 输出一个明确的下一动作。
5. Codex 执行并做最小真实验证。
6. Codex 形成正式阶段报告或结构化事实包。
7. Codex 只精确 stage 本轮文件，commit 并 push 到共同仓库。
8. Codex 验证 `LOCAL_HEAD == ORIGIN_HEAD` 与 `WORKTREE_CLEAN=YES`，记录 `SHARED_REPO_SYNC`、`COMMIT_SHA` 和 `REMOTE_VERIFY`。
9. ChatGPT 从共同仓库重新读取，给出 KEEP、ROLLBACK、NEXT 或 99 / FREEZE。
10. 循环。

```text
ChatGPT instruction
-> Codex local execution
-> Local evidence
-> Formal result package
-> GitHub shared repository
-> Remote verification
-> ChatGPT reads shared facts
-> Next decision
```

## 完成门禁

预计产生可复用新事实的 Codex / Reasonix 命令包必须自动包含正式报告、共同仓库写入、精确 stage、commit、push 和 remote verify。只有 `LOCAL_TASK_RESULT=PASS AND SHARED_REPO_SYNC=PASS` 才能声明阶段完成、FINAL PASS、99 或 FREEZE。

若同步因冲突、陌生 dirty worktree、权限、认证、网络、push、安全策略或仓库状态异常而不能安全完成，保留本机成果并报告 `SHARED_REPO_SYNC=BLOCKED`，最终只能是 PARTIAL 或 BLOCKED。

只读回答、纯解释、未执行草案、读取已有仓库信息和不改变 CURRENT 的查询不创建无意义 commit。

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
