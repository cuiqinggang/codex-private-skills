# 长期记忆超级虚拟人 v1.0

```ini
PROJECT=长期记忆超级虚拟人
VERSION=v1.0
STATE=10
VIRTUAL_MATURE=YES
PROJECT_FREEZE=NO
FINAL_VALID=NO

OBJECTIVE=T*=min(T_VALID)
PRIMARY_BRAIN=GPT
LONG_TERM_MEMORY=REQUIRED
PRIMARY_ROUTE_CERTIFIED=PARTIAL
STRONG_BACKUP_CERTIFIED=PASS_RECOVERY_LEVEL
```

## 1. 项目定义

“长期记忆超级虚拟人”不是单一助手，也不是单一执行器。

它是一个长期存在的个人智能核心：

```text
长期记忆
+
高智能综合判断
+
互联网与在线工具
+
本地电脑工具
+
按需调用 Codex / Reasonix / 浏览器 / 专用模型 / 其他成熟执行器
+
现实结果验证
+
故障恢复与换页续跑
```

GPT 当前作为首要超级大脑候选，但在 Reality 数据证明之前，不宣称它是唯一最优路线。

## 2. 三个独立基础资产

本项目调用但不合并以下资产：

1. `极限短时间智能体宪法 v0.3.1`
2. `极限短时间自动化闭环 v2.0`
3. `GPT直连Windows双路执行桥 v0.2.0`

三者分别负责：
- 判断原则；
- 极限 T_VALID 工作方法；
- Windows 现实连接与主备通道。

它们各自独立版本、独立 Reality、独立升级。

## 3. 默认主链候选

```text
用户现实目标
→ GPT 超级大脑
→ 全维度观察 / 搜索 / 组合判断
→ 选择当前最短有效工具
→ 网络 / Remote / Codex / Reasonix / Browser / 其他执行器
→ 现实执行
→ 机器可验证结果自动验收
→ FINAL_VALID
→ 经验写回
```

工具是能力，不默认与 GPT 平级。

需要并行时，GPT 可按任务拆出搜索、执行、审核、整合等子任务；只有能改善完整 T_VALID 时才保留并行层。

## 4. 当前核心连续性能力

### A. GPT 连续性与换页恢复

v0.4 已把以下能力纳入默认运行合同：
- 上下文过长；
- 页面卡顿 / 不回答；
- 网络节点暂时故障；
- 长任务中途停止；
- 新页面丢失当前项目状态。

当前目标不是无限延长单一聊天，而是：

```text
工作会话
→ Checkpoint
→ 权威项目状态
→ 新会话恢复
→ 继续原任务
```

### B. GPT 本身不可用时的强备份

正式生产不能只依赖 GPT + Codex 同时健康。

必须存在一条独立成熟备份，使 GPT 服务、登录、配额或会话故障时仍可继续关键工作。

备份可较慢，但必须能达到同等现实 VALID。

## 5. 长期记忆结构

长期记忆不等于无限上下文。

至少分三层：

```text
个人长期记忆
→ 稳定偏好、权限边界、长期目标

项目权威状态
→ README / SUMMARY / Reality / 决策 / 证据

会话 Checkpoint
→ 当前任务、已完成、未完成、下一步、禁止重复路径
```

聊天页面只是工作内存，不是唯一事实库。

## 6. 权限边界

默认可充分使用已授权成熟能力。

长期硬边界：
- 不破坏 / 删除 Windows 系统；
- 不修改 FlClash / 网络代理；
- 高危、不可逆、账号安全、支付等动作按现实权限门处理；
- 其他普通执行尽量不要求用户充当消息中继。

## 7. 当前阶段

当前技能包版本为 **v0.4.4**，已签 VIRTUAL_MATURE=YES，但 FINAL_VALID=NO。

v0.4.4 在 v0.4.3 已完成的现有浏览器复用、真正 New chat、禁止 Branch、最小 handoff、exactly-once、page lease、global writer lease、长回答停滞自动恢复、模型/Thinking R14 Reality 与单浏览器 R15 修复基础上，进一步把页面生命周期收敛为**唯一生产连续性控制链**。总控/CEO 默认在可见文本 40,000 或用户轮次 10 任一先到时预防性换真正 New chat；执行页默认 30,000 / 3 轮。页面/UI 异常、断连、无进展、活跃 turn 卡死统一进入同一决策器：若后台仍推进则等待，确认停滞后才停止旧 turn、Checkpoint、true New chat、最小 handoff、exactly-once。Reality `LTMVH-CEO-ROTATE-REALITY-20261004-R1` 已证明 shared-mcp 现有浏览器上的强制预防轮换可行。旧 `chatgpt-continuity-v1` 与旧恢复/换页策略只保留为历史索引，不再作为第二套 supervisor 并行运行。下一阶段重点仍是 DCR 真正注销/重登恢复、真实有价值长任务 FINAL_VALID 与独立备脑业务级 DONE_WHEN。

当用户明确指定“长期记忆超级虚拟人”运行当前任务时，上述连续性规则自动生效；长页面能安全提前换就提前换。
