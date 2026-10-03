# LTMVH 旧页面连续性 / 恢复方案索引

> 状态：HISTORICAL / SUPERSEDED  
> 当前生产运行入口：`CHATGPT_SESSION_CONTINUITY_CONTROLLER.md`（v0.4.4）  
> 目的：保留旧方案、旧 Reality、旧故障经验，避免重复研究；**不得与当前 v0.4.4 同时作为生产控制面运行。**

## 1. 为什么保留

旧方案虽然已经被 v0.4.4 简化和统一，但其中包含：
- 页面异常分类经验；
- Checkpoint / handoff 设计；
- true New chat / 禁止 Branch 的验证过程；
- exactly-once、page lease、writer lease；
- 断连后先观察后台是否仍推进的保守规则；
- Cloudflare / 真人验证、CDP、DOM 兼容等失败证据；
- 旧恢复阶梯与备脑切换经验。

这些内容只作为：
```text
历史证据
+ 故障复盘
+ 回退参考
+ 未来重新设计时的对照
```

不作为当前生产时的第二套并行 supervisor。

## 2. 当前唯一生产入口

```text
SKILL.md
→ CHATGPT_SESSION_CONTINUITY_CONTROLLER.md
→ runtime/session-continuity-supervisor.js
→ runtime/chatgpt-continuity-runtime.js
→ runtime/chatgpt-existing-cdp.js
```

当前版本：**LTMVH v0.4.4**

核心策略：
- CEO/总控页：按上下文增长量提前换真正 New chat；
- 执行页：更低阈值主动轮换；
- 页面异常、UI 错误、断连、无进展、活跃 turn 卡死统一进入同一决策器；
- 若后台仍有活动或可能完成，则先只读 probe / 等待，不重复执行；
- 确认停滞后才停止旧 turn、Checkpoint、true New chat、最小 handoff、exactly-once；
- 已有专用浏览器必须复用，禁止无必要第二浏览器；
- Branch 不属于恢复目标。

## 3. 旧方案与资料位置

### A. 通用恢复阶梯
- `RECOVERY.md`
- `workspaces/long-term-memory-super-virtual-human-v1.0/RECOVERY_PROTOCOL.md`

用途：历史通用恢复逻辑，覆盖页面、Windows、执行器、备脑。  
状态：**保留参考，不再作为 ChatGPT 页面生命周期的独立生产控制器。**

### B. 旧连续性规范
- `CHATGPT_SESSION_CONTINUITY_CONTROLLER.md` 的 Git 历史版本（v0.2 / v0.3 / v0.4.0～v0.4.3）
- `CHANGELOG.md` 中 0.2.x～0.4.3 连续性演进记录

用途：查看旧判定规则、恢复门槛、设计演进。  
状态：**被 v0.4.4 supersede。**

### C. Reality / Evidence
- `evidence/CONTINUITY-POLICY-REALITY-20261002-R3.json`
- `evidence/REALITY-CLOSURE-20261002-R2.json`
- 后续 R6 / R8 / R9 / R10 / R15 等 Reality 记录，以 Git 历史与 evidence 目录为准。

用途：验证旧方案曾经真实做过什么，避免把历史失败/成功重新测试一遍。

### D. 旧运行实现 / 演化资产
- `runtime/session-continuity-supervisor.js`
- `runtime/session-continuity-supervisor.test.js`
- `runtime/chatgpt-page-lease.js`
- `runtime/chatgpt-existing-cdp.js`
- `runtime/chatgpt-continuity-runtime.js`
- 专用浏览器 watchdog 相关运行文件（本机运行副本 / Git 历史）

注意：上述文件中一部分已经被 v0.4.4 **继续复用并升级**，不是“遗留垃圾”。  
如果未来需要查看“旧实现”，应通过 Git 历史查看对应旧 commit，而不是恢复第二套常驻 runtime。

## 4. 禁止事项

```ini
RUN_TWO_CONTINUITY_SUPERVISORS=NO
RUN_OLD_AND_NEW_RECOVERY_POLICY_IN_PARALLEL=NO
BRANCH_AS_RECOVERY_TARGET=NO
REPLAY_FULL_OLD_CONVERSATION=NO
DELETE_OLD_REALITY_EVIDENCE=NO
DELETE_GIT_HISTORY=NO
```

## 5. 回退规则

只有出现以下情况之一，才允许回看旧方案：
1. v0.4.4 不能满足 DONE_WHEN；
2. 新版出现旧版没有的严重回归；
3. 需要复核历史 Reality、根因或恢复路径；
4. 需要从 Git 历史提取某个已验证旧机制。

回退时：
```text
先定位旧 commit / evidence
→ 只提取需要的成熟机制
→ 合并回当前唯一生产路径
→ 不重新启用第二套并行 supervisor
```

## 6. 一句话结论

> 旧方案全部保留为可检索历史资产；生产只运行 v0.4.4 一套连续性控制链。
