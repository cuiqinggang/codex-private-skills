---
name: first-principles-physical-limit-convergence
description: 极限短时间引擎 v4.7.6。只有“虚/实”两步；新增阶段-执行器一致性总门、虚→实原子转换、现实时间必填门、证据一致性门。虚阶段由 GPT 成熟，Codex 只允许在“实”阶段执行。
metadata:
  version: "4.7.6"
  display_name: "极限短时间引擎"
---

# 极限短时间引擎 v4.7.6

## 核心不变
- 方法永远只有两步：虚、实。
- 唯一优化目标仍是：在所有有效门通过前提下最小化 T_VALID。
- 当前成熟极限时间锚：T_MATURE*=00:03:14.419（194419.3759 ms）。
- Reality Foundation（现实底座）= local-ai-reality-foundation@1.1.8。
- 用户默认只看一个时间：极限锚03:14.419；机器内部保留完整时间账。

## 0号硬门：阶段-执行器一致性
这是所有发送门之前的总门。

### 虚
- PHASE=虚 时，VIRTUAL_EXECUTOR=GPT。
- PHASE=虚 时，CODEX_DISPATCH 必须等于 0。
- PHASE=虚 时，禁止 Codex 产生业务现实副作用、修改目标业务、执行现实验证。
- GPT 在虚阶段允许做控制面动作：读取现实底座、虚拟推演、公开信息预验证、生成冻结包、把冻结包发布到共同仓库并回读。
- 控制面冻结发布不等于进入“实”。

### 实
- Codex 只允许接收 PHASE=实 的任务。
- 任何发给 Codex 且 PHASE!=实 的任务必须在第一动作前 BLOCK。
- 阻断时：CODEX_DISPATCH_COUNT=0，BUSINESS_SIDE_EFFECT=0，并返回 GPT。

机器不变量：
IF EXECUTOR=CODEX AND PHASE!=实 -> BLOCK。

## 用户可见状态
格式固定：
【页面名｜任务名｜NN-NN｜虚/实】 极限锚03:14.419

NN-NN：
- 前两位=方案代。
- 后两位=该方案代的正式现实尝试号。
- 每代只允许 01–06；07 永久非法。
- 第6次现实失败必须进入下一方案代01。
- 第1–5次若已证明结构性错误，可提前进入下一方案代01。

## 虚阶段成熟门
虚阶段由 GPT 完成，Codex 不参与成熟。

虚完成必须同时满足：
1. Reality Foundation 已读取；
2. Reality Delta 已吸收；
3. FINAL_VALID 已定义；
4. 执行链逐步闭合；
5. 外部依赖已闭合或冻结兜底；
6. 唯一 FREEZE_ID 已生成；
7. 冻结包已发布到不可变来源；
8. 冻结包已回读并校验；
9. 现实合同已完成；
10. 现实命令已完成；
11. 时间合同已完成；
12. 证据内部一致性 PASS。

任一缺失：
VIRTUAL_COMPLETE=NO。

## 虚→实原子转换
沿用 v4.7.1 原子交付，但新增一条不可绕过规则：

现实命令本身必须标记 PHASE=实。

同一轮顺序固定：
虚拟成熟 PASS
-> 生成 FREEZE_ID
-> 发布冻结包
-> 回读校验
-> 生成现实合同
-> 生成现实时间合同
-> 生成 Codex 现实任务（其定位必须为“实”）
-> 状态从 NN-NN｜虚 原子切换为 NN-NN｜实
-> 才允许 VIRTUAL_COMPLETE=YES。

以下状态永久非法：
- VIRTUAL_COMPLETE=YES 但没有现实任务；
- VIRTUAL_COMPLETE=YES 但现实任务写着“虚”；
- PHASE=虚 时 Codex 已执行；
- PHASE=实 但没有新 FREEZE_ID；
- PHASE=实 但时间合同未武装。

## 实阶段
Codex 是现实执行器，只执行冻结合同，不重新设计。

同一 FREEZE_ID 只允许一次正式 REAL。

REAL FAIL：
最小 Reality Delta
-> STOP
-> 返回 GPT
-> 回虚
-> 生成新 FREEZE_ID
-> 再进入下一次实。

不得在现实阶段现场改方案后直接重跑。

## 现实时间硬门
每一次 REAL 都必须记录：
- REAL_START
- REAL_END
- T_VALID_REAL_MS
- 当前 T_MATURE_STAR_MS

没有 T_VALID_REAL_MS：
无论功能测试多少项 PASS，REAL_VALID=NO。

当前现实认证时间门：
T_VALID_REAL_MS <= 194419.3759。

若超过：
功能可以记录为通过，但极限时间认证失败，返回虚阶段重新优化。

T_CLOSED_REAL 仍由闭环控制层内部记录，不要求每条用户回答显示。

## 证据一致性门
现实回报在判 PASS 前必须进行内部一致性检查。

至少检查：
- 路径字段是否自相矛盾；
- LOCAL / REMOTE commit、branch 是否明确区分；
- 声称已发布的远程对象是否可回读；
- PASS 字段是否有对应证据；
- 当前阶段与实际动作是否一致；
- 时间字段是否完整。

任何矛盾：
EVIDENCE_CONSISTENCY=FAIL
-> FINAL_VALID=NO。

## PRE-DISPATCH（发送前）组合顺序
合法顺序：
1. 阶段-执行器一致性门；
2. 状态/尝试号/时间锚/Freeze 门；
3. 现实合同完整性门；
4. 时间账武装门；
5. 证据一致性门；
6. ALLOW 后才进入 Codex。

状态门本身不得依赖 PowerShell/Node 本地子进程。

## 本地执行器能力仍独立
只有现实业务确实需要本机子进程时，才检查：
- EXECUTION_CHANNEL_ID；
- 当前通道真实 PROCESS_SPAWN 能力。

历史工作目录 PASS、mock PASS、别的执行通道 PASS 都不能代替当前现实证明。

## v4.7.5 -> v4.7.6 的 Reality Delta
上一轮出现：
PHASE=虚
但 Codex 实际执行了文件写入、代码修改、测试和提交。

因此该次不能计为虚拟成熟，也不能计为有效现实认证。

吸收的结构性教训：
1. “虚/实”必须是执行权限，不只是标签；
2. 虚任务进入 Codex 必须零副作用阻断；
3. REAL 没有 T_VALID_REAL 不得 PASS；
4. 证据字段自相矛盾不得 PASS；
5. commit/branch 必须明确 LOCAL/REMOTE provenance（来源范围）。

当前新方案代：03-01。

## 语言
用户可见验收结果中文优先。
机器字段、版本号、路径、哈希、公式允许保留英文；首次出现的必要英文术语附中文说明。

## 最终一句话
虚只能由 GPT 成熟并冻结；冻结包、现实合同、时间合同和“实”任务同轮齐全后才允许切实；Codex 看到任何“虚”任务必须零副作用拒绝；现实没有真实时间就没有 PASS。
