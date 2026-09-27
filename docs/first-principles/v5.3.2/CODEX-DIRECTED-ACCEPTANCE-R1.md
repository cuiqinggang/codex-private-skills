# v5.3.2 Codex 主导真实用户验收 R1

## 角色

- GPT：冻结候选版本并发布本验收任务；不替 Codex 预先选具体测试样例。
- Codex：独立选择最小有效真实任务，组织并执行验收。
- 浏览器执行器：必须使用现成的 playwright-native-ai-browser，即“JEV-native Playwright 极限浏览器自动化 R3 编译热态版”。
- 用户：观察，不出题，不提醒系统补步骤。

## Codex 必须使用的浏览器技能

- 技能 ID：playwright-native-ai-browser
- Codex 薄入口：C:\Users\A\.codex\skills\playwright-native-ai-browser
- 权威技能目录：C:\AI\Playwright-Native-AI-Browser\skills\playwright-native-ai-browser
- 权威 SKILL：C:\AI\Playwright-Native-AI-Browser\skills\playwright-native-ai-browser\SKILL.md
- MCP：playwright_native_ai_browser

禁止 Codex 自行编写 Playwright/浏览器脚本替代该技能包。

## Codex 自主选题原则

Codex 必须自己选一个：
- 足够简单；
- 低副作用；
- 很快可以虚拟成熟；
- 结果容易核验；
- 能真实覆盖“普通用户任务 → GPT 虚 → 自动 Freeze → 自动完整实命令 → Codex/浏览器真实执行 → 返回 GPT”的任务。

GPT 和用户不得事先给出具体任务答案。

## 验收方式

Codex 使用浏览器技能在真实界面模拟用户：
1. 向 GPT 页面输入自己选择的普通自然语言任务；
2. 观察 GPT 是否自己完成虚拟成熟；
3. 观察 GPT 是否无需用户提醒便自动 Freeze→实；
4. 检查屏幕上出现的 Reality Dispatch 是否为完整 Codex CHAT 命令，而不是 Header；
5. 执行该命令对应的真实任务；
6. 验证业务结果；
7. 将完整证据和 PASS/FAIL/BLOCKED 返回 GPT。

## PASS

只有真实界面完整链路自然通过，且业务结果正确，才 PASS。

## FAIL

任一成立即 FAIL：
- 需要用户提醒“继续/发命令”；
- GPT 停在 Freeze；
- 只有 Header；
- Codex 自己写浏览器脚本而不是调用冻结技能；
- 使用隐藏函数/测试捷径代替 UI 路径；
- 业务结果不正确；
- 中途发现产品问题后现场修复再继续算 PASS。
