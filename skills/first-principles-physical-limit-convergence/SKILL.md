---
name: first-principles-physical-limit-convergence
description: 极限短时间引擎 v4.7.2。最终确定性版：一虚一实、双时间单闭环、G/A 有限循环状态、6 次现实尝试强制方案重组、时间锚强制可见、机器验证。
metadata:
  version: "4.7.2"
  display_name: "极限短时间引擎"
---

# 极限短时间引擎 v4.7.2

## 1. 永久核心

方法永远只有两个步骤：虚（VIRTUAL）和实（REAL）。
第三步骤禁止创建。

两个核心时间：
- `T_MATURE*`（成熟极限时间）：当前精确锚 `00:03:14.419`。
- `T_CLOSED_REAL`（现实闭环墙钟）：用户首次提交到 `FINAL_VALID=PASS` 的真实墙钟时间。

不允许建立第三个并列核心时间。

## 2. 唯一状态码

唯一用户可见状态码：`Gnn-Amm-虚/实`。

- `G`（方案代）：当前方案族第几代。
- `A`（本代现实尝试号）：当前方案代第几次正式现实尝试。
- `虚/实`：当前唯一方法阶段。

示例：`G01-A03-虚` 表示“第一代方案，第 3 次现实尝试之前的虚阶段”。

## 3. 有限循环，不允许无限顺延

同一方案代的 `A` 只允许 `01–06`。

正常：`G01-A01-虚 → G01-A01-实 → PASS → FINAL`。

现实失败且 A<06：
`G01-A01-实 FAIL → G01-A02-虚`。

若出现结构性 Reality Delta（现实差异），允许提前重组：
`G01-A03-实 FAIL → G02-A01-虚`。

第 6 次现实仍失败时：
`G01-A06-实 FAIL → 必须方案重组 → G02-A01-虚`。

`A07` 及以上永远非法。

当前冻结阈值：`MAX_REAL_ATTEMPTS_PER_GENERATION=6`。
以后如有现实证据可调整，但调整本身必须升版并重新验证。

## 4. 每个相关回答必须先显示横向时间状态锚

第一非空行固定为：

`【状态 Gnn-Amm-虚/实｜极限锚 03:14.419｜闭环 hh:mm:ss.mmm｜偏差 ±hh:mm:ss.mmm｜时间状态 目标内/超目标】`

含义：
- `极限锚` = 当前 `T_MATURE*`（成熟极限时间）。
- `闭环` = 当前 `T_CLOSED_REAL`（现实闭环墙钟）已用时间。
- `偏差` = `闭环 - 极限锚`。
- `时间状态`：偏差≤0 为“目标内”，偏差>0 为“超目标”。

这不是装饰。缺少状态锚行，视为 `DRIFT=YES`（已漂移），该回答对本技能无效。

## 5. 时间核心不得在讨论中消失

机器字段必须同时满足：
`T_MATURE_STAR_MS`、`T_CLOSED_REAL_START_TIMESTAMP`、`T_CLOSED_REAL_NOW_MS`、`TIME_GAP_MS`、`TIME_STATE`。

`TIME_GAP_MS = T_CLOSED_REAL_NOW_MS - T_MATURE_STAR_MS`。

如果算术不一致，机器验证器直接 BLOCK（阻断）。

## 6. 虚阶段

虚必须完成：现实底座读取、成熟方案组合、已知失败门、最终有效条件、执行链闭合、时间账本。

继承 v4.6.1：GPT 当前工具能低成本真实预跑的关键公开子路径，冻结前必须真实预跑并取得 PASS 证据。

不能由 GPT 等价现实预跑的本机/GPU/登录态/Windows 专属差异，明确标记后留给实。

冻结产生唯一 `FREEZE_ID`（冻结方案编号）。

## 7. 虚→实原子交付

继承 v4.7.1：虚完成与现实任务发布必须同一轮原子完成。

必须同时完成：
`FREEZE_ID`、四定位、`Gnn-Amm`、现实合同、发布时间、发布前时间账、PASS/FAIL 输出合同、现实命令发布/自动发送。

没有现实命令，不允许宣布虚完成。

四定位格式：`【页面名｜任务名｜Gnn-Amm｜虚/实】`。

## 8. 实阶段

Codex（现实执行器）是默认执行器；PowerShell / Playwright / 本机工具只是其内部确定性工具。

继承 v4.6.2：同一 `FREEZE_ID` 只允许一次正式 REAL（现实）发布。

现实阶段禁止现场重新设计、补方案、修方案。

REAL FAIL（现实失败）只允许：最小 Reality Delta（现实差异）→ STOP（停止）→ 回虚。

禁止：同一冻结方案直接再跑一次。

## 9. 第 6 次失败强制重组

第 6 次 REAL FAIL（现实失败）不是“再试第 7 次”的信号，而是“当前方案代存在较高结构风险”的强制审查点。

必须：旧方案代标记 superseded（被替代）→ 重新组合成熟方案 → 新 `G` → `A01` 重新开始。

这就是及时回头机制。

## 10. Reality Foundation（现实底座）

唯一真实版本：`local-ai-reality-foundation@1.1.7`。

版本链：`1.1.3 → 1.1.4 → 1.1.5 → 1.1.6 → 1.1.7`。

新增现实约束包括：Windows Codex 1344 子进程失败、窄工作目录成功路径、下载工具真实版本、curl/Schannel TLS 上下文差异、hf 1.19.0 本机真实成功下载路径。

## 11. 用户可见语言规则

用户可见说明以中文为主。

必须出现的英文术语，首次出现时必须紧跟中文解释，例如：`validator（验证器）`、`Reality Foundation（现实底座）`、`Gate Regression（门禁回归）`。

机器字段、公式、版本号、路径可以保留英文，不要求每次重复翻译。

如果一整段英文让用户无法直接理解，则该输出不合格。

## 12. 横向展示规则

用户可见状态必须横向展示，不把状态码竖着堆成大列表。

推荐格式：
`G01-A01-虚 ｜ 极限锚03:14.419 ｜ 闭环00:01:40 ｜ 偏差-01:34.419 ｜ 目标内`。

## 13. GitHub / Browser / Codex 角色

GPT：推理与最终裁决。
Codex：现实执行器。
Playwright Native AI Browser（Playwright 原生 AI 浏览器）：浏览器通信/执行桥。
GitHub：共同事实源，不是默认 REAL 启动硬依赖。

## 14. 自动闭环目标

用户只输入一次；GPT 自动虚；自动交给 Codex；Codex 自动实并回传；GPT 自动判断；失败则自动回虚并进入下一 A 或新 G；FINAL_VALID 后才通知用户。

## 15. 机器门

最终执行不是靠 AI 自觉，而是靠 `validate-cycle-state-v4.7.2.mjs`（有限循环状态验证器）。

它机械阻断：非法状态码、A>06、时间锚缺失/算错、同 Freeze 二次 REAL、REAL FAIL 直接重试、第 6 次失败不重组、FINAL 缺现实 PASS 或时间账。

## 16. 最终不变量

`METHOD_STEP_COUNT=2`。
`A<=06`。
`A06_FAIL -> NEW_G + A01`。
`TIME_CORE_VISIBLE_ALWAYS=TRUE`。
`ONE_REAL_PER_FREEZE_ID=TRUE`。
`REAL_FAIL_DOES_NOT_RESET_TASK_TIME_ID=TRUE`。
`REAL_FAIL_DOES_NOT_RESET_T_CLOSED_REAL=TRUE`。
`USER_VISIBLE_CHINESE_FIRST=TRUE`。

一句话：进入本技能后，任何有效回答都必须同时告诉你“当前是哪一代方案、第几次现实尝试、处于虚还是实、距离极限时间还有多少”；第 6 次失败必须重组，不允许无限往下试。
