# 共同工作区资产索引

更新时间：2026-10-01  
仓库：`cuiqinggang/codex-private-skills`  
默认分支：`main`

## 目录职责

- `skills/`：正式或历史技能包；通常每个技能以 `SKILL.md` 为入口。
- `workspaces/`：长期项目工作区、阶段成果与现实证据。
- `docs/`：命令包、源清单、项目文档、迁移/审核资料。
- `AGENTS.md`：仓库级读取与保存规则。
- `README.md`：仓库背景与部分长期入口。

## main 当前技能目录快照

以下枚举是 **2026-09-29 的历史快照**，不作为当前完整目录清单；实时仓库目录高于此快照。

1. `ChatGPT官网规划桥接_让Codex读取GPT方案并执行_快照_20260504_225352`
2. `ChatGPT官网规划桥接_让Codex读取GPT方案并执行_最新`
3. `Google-Gemini视觉模型接入`
4. `Hermes-Watchdog修复失败总结`
5. `absolute-time-fireworks-optimization`
6. `ai-learning-material-pack`
7. `chatgpt-web-plan-bridge-latest`
8. `chi-yu-xing-dadao-zhijian-interest-law`
9. `claude-code-deepseek-v4pro-windows`
10. `codex-deepseek-v4pro-ccx-ccswitch-replay`
11. `complete-body-building-rules`
12. `first-principles-physical-limit-convergence-v5.6`
13. `gpt-plus-superbrain-v0.2`
14. `hermes-014-minimal-baseline-restore`
15. `hermes-014-restoration-ladder`
16. `hermes-014-windows-native-8642`
17. `hermes-model-routing-qiniu-claude-replay`
18. `hermes-watchdog-failure-postmortem`
19. `jev-probability-engine-p0`
20. `karpathy-coding-principles`
21. `mature-outcome-automation`
22. `mature-replication-four-column`
23. `new-api-local-deploy`
24. `one-person-ai-company-success-routes`
25. `openclaw-upgrade-no-model`
26. `overseas-ai-region-setup`
27. `performance-benchmark-convergence`
28. `powershell-reliability-guard`
29. `reasonix-empty-session-race-repair`
30. `reasonix-fault-repair`
31. `screenshot-browser-100-percent-route`
32. `screenshot-recognize-operate-browser`
33. `telegram-hermes-codex-vision-action`
34. `ultrafusion-low-cost-multi-model-extreme-fusion`
35. `ultrafusion-v8-minimal-pressure-chain`
36. `virtual-mouse-keyboard-demo`
37. `virtual-mouse-keyboard-demo_20260504_222552`
38. `visual-art-engine-performance-ladder`
39. `windows-github-cli-auth-repair`
40. `windows-hermes-014-official-8642-route`
41. `windows-hermes-operations`
42. `xiaolongxia-3011-openclaw-connect`
43. `xiaolongxia-boot-replay-autostart`
44. `xiaolongxia-free-model-pool`
45. `xiaolongxia-free-provider-expansion`
46. `xiaolongxia-openclaw-gateway-safety-recovery`
47. `yesterday-replay-controlled-coding`
48. `家庭作业江湖_功夫式AI辅导短片技能包_v1.2`
49. `家庭作业江湖_功夫式AI辅导短片技能包_v1.3`
50. `家庭作业江湖_功夫式AI辅导短片技能包_v1.4`
51. `家庭作业江湖_功夫式AI辅导短片技能包_v1.6_Remotion执行包`
52. `家庭作业江湖_功夫式AI辅导短片技能包_v1`
53. `爱马仕大模型接入调试昨日重现技能包`
54. `虚拟鼠标键盘_演示更新复用Skill_快照_20260504_222953`
55. `虚拟鼠标键盘_演示更新复用Skill_最新`

## main 当前工作区快照

2026-09-29 历史快照：
1. `workspaces/absolute-time-fireworks-optimization/`
2. `workspaces/visual-art-engine-performance-ladder/`

实时仓库中还应按任务继续查看 `workspaces/`，不能依赖上面旧枚举。

## 当前重点已验证入口

- **极限短时间智能体宪法 v0.2（FROZEN）**：`skills/extreme-time-agent-constitution/SKILL.md`
- **极限短时间自动化闭环 v1.2（CURRENT）**：`workspaces/extreme-time-automation-loop-v1.2/README.md`
- **v1.2 Reality Contract（DRAFT）**：`workspaces/extreme-time-automation-loop-v1.2/REALITY_CONTRACT.md`
- **JARVIS v1 历史工作区（SUPERSEDED）**：`workspaces/jarvis-v1/README.md`
- **JARVIS 长期超级助手核心方法 v0.1.0（HISTORICAL）**：`skills/jarvis-long-term-super-assistant-core/SKILL.md`
- 整体闭环极限短时间引擎：按 CURRENT / 最新冻结入口读取，不只按目录名判断版本。
- JEV Probability Engine P0：`skills/jev-probability-engine-p0/SKILL.md`
- Visual Art Engine Performance Ladder：`skills/visual-art-engine-performance-ladder/SKILL.md`
- 一人公司成功路线：`skills/one-person-ai-company-success-routes/`
- MOA：`skills/mature-outcome-automation/`
- Reasonix 故障修复：`skills/reasonix-fault-repair/`
- PowerShell 防错：`skills/powershell-reliability-guard/`
- GitHub 登录修复：`skills/windows-github-cli-auth-repair/`

## 查找规则

1. 用户给出准确技能名：先查 `skills/<name>/SKILL.md`。
2. 用户只给项目中文名/旧版本名：仓库全局搜索关键词，再定位 SKILL/CURRENT/RESULT/FREEZE。
3. main 没找到：搜索相关分支，特别是 `codex/*`。
4. 找到多个版本：优先读取项目的 CURRENT/CURRENT_VERSION/最新正式冻结说明；不得只按目录名猜“最新”。
5. 只有聊天历史提到、远端未找到：标记为 `HISTORICAL_REFERENCE_ONLY`，不能写成 `REPOSITORY_VERIFIED`。
6. 任何“已发布/已保存”结论都必须远端回读确认。

## 动态维护规则

每次新增正式技能或长期工作区时：
- 新资产写入本仓库；
- 必要时更新本索引的“重点入口”，但不要求手工维护所有历史分支；
- 其他智能体应以实时仓库目录/搜索结果为准，历史枚举只是快照。
