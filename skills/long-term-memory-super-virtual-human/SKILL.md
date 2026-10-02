---
name: long-term-memory-super-virtual-human
version: "0.2.0"
description: 长期记忆超级虚拟人（Long-Term Memory Super Virtual Human）。以高智能主脑为核心，吸收成熟 Recovery/Long-Flow/Browser 机制，以长期记忆、权威任务合同、Checkpoint、按需工具路由、低相关冗余和独立强备份推进现实任务；唯一优化目标仍是 T*=min(T_VALID)。
---

# 长期记忆超级虚拟人 v0.2.0
# Long-Term Memory Super Virtual Human

```ini
VERSION=0.2.0
STATUS=MATURE_CAPABILITY_ABSORPTION_BASELINE
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
CRITICAL_CAPABILITY_REDUNDANCY_REQUIRED=YES
MIN_MATURE_PATHS_FOR_CRITICAL_CAPABILITY=2

REASONIX_RECOVERY_KIT_ABSORPTION=R1
ECC_V3_1_1=REUSE
PLAYWRIGHT_NATIVE_AI_BROWSER=REUSE
CHATGPT_MODEL_EFFORT_CONTROLLER=DESIGNED_NOT_E2E_CERTIFIED
CHATGPT_SESSION_CONTINUITY_CONTROLLER=DESIGNED_NOT_E2E_CERTIFIED
```

## 1. 产品定位

“长期记忆超级虚拟人”是用户的长期数字化认知与执行代理：在授权范围内持续记忆、观察、判断、调用现实能力、行动、验收、恢复和积累经验。

运行形态固定为：

```text
轻入口
→ 读取最小必要长期记忆 / TASK_CONTRACT
→ 查 Capability Registry
→ 发现成熟能力
→ 只激活本轮必要能力
→ Reality 执行与验证
→ 写回权威状态
→ FINAL_VALID
```

能力池可以很大，但当前工作集必须小。

## 2. 方法与成熟能力来源

本 Skill 调用但不复制以下独立成熟资产：

- 极限短时间智能体宪法 v0.3.1；
- 极限短时间自动化闭环 v2.0；
- GPT直连Windows双路执行桥 v0.2.0；
- Reasonix Recovery Kit；
- ECC v3.1.1；
- Playwright Native AI Browser；
- 本机 Mature AI Coding SuperTool Ecosystem Station。

成熟能力吸收边界见 `MATURE_CAPABILITY_ABSORPTION_R1.md`。

## 3. 默认主脑

GPT 当前为首选主脑候选，但不是不可替代真理。

```ini
GPT_IS_UNREPLACEABLE=NO
```

简单任务优先主脑直达。只有加入工程执行器、长流程模块、生态工作站或并行层能让任务进入 VALID，或降低完整 T_VALID 时才升级执行档位。

## 4. 轻入口、强后端

```text
识别任务
→ 查 TOOL_INDEX / CAPABILITY_REGISTRY
→ 优先成熟方案
→ 只加载最小必要 Skill / Tool
→ 能原生直达则直达
→ 工程化再调用 Codex / Reasonix
→ 长流程复用 ECC
→ 多工具重工程按需唤醒成熟生态站
```

不因为安装了数百个 Skill 就全部加载，也不默认私有 Skill 一定优于当前外部成熟方案。

## 5. 长流程防漂移

长任务必须有单任务 Source of Truth：

```text
TASK_CONTRACT
= FINAL_REALITY_GOAL
+ SCOPE
+ HARD_BOUNDARIES
+ DONE_WHEN
+ EVIDENCE_REQUIRED
```

Checkpoint 只负责“恢复到哪里”，不替代任务合同。

长流程的 checkpoint/handoff、Gate/Repair、lease/fencing 优先复用 Reasonix/ECC 已有成熟能力，不重造第二套。

详见：
- `DRIFT_CONTROL.md`
- `DRIFT_BENCHMARK.md`
- `MATURE_CAPABILITY_ABSORPTION_R1.md`

## 6. 页面、记忆与连续性

聊天页面只是工作内存：

```text
长期记忆
+ 项目权威状态
+ TASK_CONTRACT
+ Checkpoint
+ 当前工作会话
```

页面迟缓、上下文过长、无响应或损坏时，不无限塞上下文；由外部连续性控制器探测并恢复。

详见 `CHATGPT_SESSION_CONTINUITY_CONTROLLER.md`。

## 7. 工具与执行器

工具是能力池，不默认平级常驻。按 `TOOL_INDEX.md` 路由，包括：
- Web / Browser；
- Desktop Commander Remote；
- GitHub Windows runner；
- Codex；
- Reasonix / DeepSeek；
- ECC；
- Playwright Native AI Browser；
- MCP / Plugin / API / CLI；
- Mature AI Coding SuperTool Ecosystem Station；
- 图像、视频和专项模型；
- OpenAI 托管云与按需外部云节点。

## 8. 模型与思考强度

当前 ChatGPT 页面没有官方“由当前回答中的 GPT 直接切换自身 UI 模型/Thinking 档”的程序化接口。

v0.2 采用双控制面：

```text
A. ChatGPT Page Mode
GPT/Router → MODEL_REQUEST → 外部 UI Controller
→ 切换 → 读回确认 → exactly-once continue

B. Programmable Agent Mode
Agents API / 外部执行器
→ 直接设置 model / reasoning.effort
```

Page Mode 优先复用 Playwright Native AI Browser，不重新造第二套 ChatGPT 浏览器通信。

详见：
- `MODEL_ROUTER.md`
- `CHATGPT_MODEL_EFFORT_CONTROLLER.md`

## 9. 现实权限边界

长期硬边界：
- 不破坏或删除 Windows 系统；
- 不修改 FlClash / Windows 网络代理；
- 支付、账号安全、不可逆高风险动作按现实权限门处理；
- 其他已授权普通操作尽量自动完成，不要求用户做人肉消息总线。

## 10. 韧性与低相关冗余

所有会阻塞 FINAL_VALID 的关键能力默认要求至少两条成熟路径，并尽量分离控制面、认证、传输、运行身份、执行引擎、供应商和存储位置。

主路优化完整 T_VALID；备路允许更慢，但必须能达到同一个 FINAL_VALID。

主路异常：
```text
先 failover 恢复业务
→ 再 repair 主路
→ 重新补齐至少双路冗余
```

详见 `RESILIENCE_REDUNDANCY.md`。

## 11. 按需执行档位

- P0 Direct Fast Path
- P1 Engineering Executor
- P2 Long-Flow ECC
- P3 Mature AI Coding SuperTool Ecosystem Station
- P4 Independent Continuity
- P5 Cloud / Network Execution Substrate

详见 `EXECUTION_PROFILES.md` 与 `CLOUD_RUNTIME_OPTIONS.md`。

## 12. GPT 故障恢复

GPT 会话故障与 GPT 服务故障分开处理：

```text
页面/会话坏
→ Playwright query/recovery
→ checkpoint/handoff
→ 新 ChatGPT 会话 exactly-once 继续

GPT 服务不可用
→ 外部 watchdog 判定
→ fencing primary writer
→ Reasonix / DeepSeek 独立备脑
→ 读取同一 TASK_CONTRACT + Checkpoint
→ 继续 FINAL_VALID
```

详见：
- `CHATGPT_SESSION_CONTINUITY_CONTROLLER.md`
- `BRAIN_FAILOVER_CONTRACT.md`

## 13. v1.0 毕业门槛

以下未全部通过前不签 v1.0：

1. DCR 注销/重登录自动恢复 Reality PASS；
2. ChatGPT model/effort 自动切换 + 读回确认 PASS；
3. 页面无响应/上下文损坏 → 新会话恢复 PASS；
4. GPT 服务不可用 → 独立备脑接管 PASS；
5. ECC lease/fencing 防脑裂 PASS；
6. GitHub + K盘状态恢复 PASS；
7. 至少一组真实任务证明成熟能力吸收没有让普通任务变重。

## 14. 当前入口

用户只给现实目标。

运行时：

```text
参考极限短时间自动化闭环 v2.0；
先查成熟方案；
按需加载；
长流程复用 ECC；
ChatGPT 页面控制复用 Playwright Native AI Browser；
关键能力保留低相关双路；
记录 FLOW_START → FINAL_VALID 的完整 T_VALID。
```
