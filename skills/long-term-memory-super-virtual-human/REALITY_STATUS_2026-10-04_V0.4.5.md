# 长期记忆超级虚拟人 v0.4.5｜冻结状态 2026-10-04

```ini
VERSION=0.4.5
STATUS=VIRTUAL_MATURE_CONTINUITY_RUNTIME_ACTIVE
VIRTUAL_MATURE=YES
FINAL_VALID=NO
STATE_SNAPSHOT=FROZEN

OBJECTIVE=T*=min(T_VALID)

CEO_CLEAN_LIFECYCLE=PASS_R18_R19
CLEAN_BASELINE=ONE_BLANK_NEW_CHAT_ROOT
FINAL_BROWSER_STATE=ONE_BLANK_NEW_CHAT_ROOT
TRUE_NEW_CHAT_CEO_REPLACEMENT=PASS
BRANCH_RECOVERY=FORBIDDEN
MINIMAL_CHECKPOINT=REQUIRED
EXECUTOR_CLOSE_AFTER_ACCEPTED_RESULT=YES
PREWARM_UNUSED_CHAT_PAGES=NO

T_VALID_R18_MS=51454
T_VALID_R19_MS=54246
T_STAR_OBSERVED_MS=51454
T_STAR_SOURCE=R18
CHECKPOINT_CHARS_R18=125
```

## 冻结结论

v0.4.5 在 v0.4.4 单一连续性控制链基础上，新增并冻结 **专用浏览器 CEO 干净生命周期**。

生产最小路径：

```text
1 个空白 ChatGPT New chat 页
→ 复用为 CEO-1
→ CEO-1 只负责理解 / 拆分 / DONE_WHEN
→ 仅创建业务所需的最少执行页
→ 最小 checkpoint 持久化
→ 关闭 CEO-1
→ 真正 New chat 创建 CEO-2
→ CEO-2 基于 checkpoint 接管，禁止重做已接受任务
→ 收回原执行结果
→ 已完成执行页立即关闭
→ FINAL_VALID / Evidence 持久化
→ 关闭最终 CEO
→ 恢复恰好 1 个空白 ChatGPT New chat 页
```

页面不是长期记忆，也不是资产；页面是运行时资源。长期事实必须进入 TASK_CONTRACT、Checkpoint、权威工作区或 Evidence。无业务价值的页面不得长期保留。

## R18｜当前最短有效 Reality

- Marker：`LTMVH-V044-CEO-CLEAN-E2E-20261004-R18`
- T_VALID：**51,454 ms**
- 起点：1 个空白 ChatGPT 页；
- CEO-1 复用起始空白页：PASS；
- CEO-1 关闭：PASS；
- CEO-2 真正 New chat：PASS；
- A / B 原任务结果：PASS；
- 执行页完成后关闭：PASS；
- continuity：PASS；
- FINAL_VALID（本 Reality）：YES；
- checkpoint：125 chars；
- 终点：1 个空白 ChatGPT 页；
- Overall：PASS。

## R19｜同构复验

- Marker：`LTMVH-V044-CEO-CLEAN-E2E-20261004-R19`
- T_VALID：**54,246 ms**
- 与 R18 相同合同全部 PASS；
- 终点仍为 1 个空白 ChatGPT 页。

因此当前：

```text
T* = min(T_VALID)
   = 51,454 ms
   = R18
```

这里的 T* 是当前设备、当前 ChatGPT 服务状态、当前冻结 VALID 合同下**已观测到的最小有效值**，不宣称为不可突破的数学绝对下界。

## 已实测但不冻结为默认路径

以下路线均做过 Reality，对完整 T_VALID 没有改善或显著变慢：

| 路线 | 结果 |
|---|---:|
| R8 干净完整链 | 52,542 ms PASS |
| R10 短提示 + A/B 并行 | 53,005 ms PASS |
| R13 A/B 提前预热 | 66,945 ms PASS |
| R14 Instant 控制链 | 62,540 ms PASS |
| R15 Instant + CEO 同物理 tab | 122,269 ms PASS |
| R16 High + CEO 同物理 tab | 90,623 ms PASS |
| R17 删除独立接管确认回合 | 61,827 ms PASS |
| R18 冻结候选 | **51,454 ms PASS** |
| R19 同构复验 | 54,246 ms PASS |

R9、R11、R12 因测试器/提交路径失效，不属于 VALID 候选。

## 冻结规则

1. 默认空闲态只保留 1 个空白 ChatGPT New chat 页；
2. CEO-1 直接复用该页；
3. 不提前预热没有立即业务价值的 ChatGPT 页面；
4. 执行页只创建最少必要数量；
5. 子任务结果被权威状态或 CEO 接受后立即关闭执行页；
6. CEO 换页必须是真正 New chat，禁止 Branch；
7. 不重放完整旧会话，只交接最小 checkpoint；
8. 旧 CEO 在 checkpoint 持久化后释放；
9. 最终证据持久化后关闭最终 CEO；
10. 任务结束必须回到恰好 1 个空白 ChatGPT 页；
11. 只有新的 Reality 在不降低 VALID 合同的情况下得到更小 T_VALID，才允许替换 R18 为新的 T*。

## 证据

机器可读证据：

`evidence/CEO-CLEAN-LIFECYCLE-EXTREME-TIME-20261004-R18-R19.json`

本版本升级不改变项目级 `FINAL_VALID=NO`，也不代表 LTMVH v1.0 已毕业。
