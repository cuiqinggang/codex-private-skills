# 长期记忆超级虚拟人 v0.5.0｜目标循环控制合同

## 默认做事逻辑

收到用户授权任务后，默认按“读取合同与状态 → 判断 → 执行或调度 → 真实验证 → 定向返修或切成熟备路 → 保存状态 → 下一轮”推进。
目标真正达到 DONE_WHEN 且满足 EVIDENCE_REQUIRED 后停止并报告完成；不要等待用户逐轮说“继续”。
GPT既可判断也可直接调用现实工具；按需调用执行器，不强制每个任务增加中间层。
普通错误先分析、定向修复和尝试现有授权范围内的新策略；错误本身不等于不可突破的阻塞。
不得降低验收标准，不得把执行器自称完成、ACK或页面回答结束作为业务完成证据。

## 成熟机制与唯一控制链

复用“循环工程”V2.0.0的合同、状态、追加日志、真实验证、有界返修、明确停止机制，并沿用现有 TASK_CONTRACT、Checkpoint、Reasonix/ECC恢复机制。
新增 `runtime/goal-loop-controller.js` 只作为薄的任务级驱动适配器，由现有 `runtime/chatgpt-continuity-runtime.js` 的唯一 writer 调用。
不新增常驻 scheduler，不并行启动第二个连续性 supervisor，不另开浏览器。
原 v0.4.5 的干净 CEO 生命周期与 true New chat / 禁止 Branch 合同继续有效；任务适配器必须复用这些既有执行面。
任务执行完成才做最终页面清理；循环中途不得清理仍在执行或待验收的页面。

## 运行接线与合同

现有 runtime inbox 的任务可包含：

```json
{
  "marker": "TASK-UNIQUE-ID",
  "goalLoop": {
    "adapterPath": "已审核任务适配器的绝对路径",
    "contract": {
      "taskId": "TASK-UNIQUE-ID",
      "goal": "用户最终现实目标",
      "doneWhen": ["不可静默修改的完成条件"],
      "boundaries": {
        "allowed": ["本任务授权范围"],
        "forbidden": ["禁止改变网络代理等硬边界"]
      },
      "adapterSha256": "执行与验收适配器文件的冻结SHA256",
      "maxRounds": 4,
      "maxRuntimeMs": 1800000
    }
  }
}
```

`maxRounds=4` 为首轮加最多三轮返修的示例，不是所有业务的固定预算；运行前根据任务冻结预算，不得静默扩大。
适配器由任务准备阶段复用成熟执行器构造，不能要求用户手动逐轮接线；尚无可用执行/验证适配器的任务必须明确报阻塞，不能声称后台已经循环。
适配器必须提供：
- `execute({contract,state,actionId,verification,shouldStop})`：仅执行本轮获授权动作，返回紧凑 checkpoint。根据上一轮真实失败结果调整策略。副作用使用稳定 actionId 去重。
- `verify({contract,state})`：运行真实验收，返回 `passed`、`evidence`；通过时还必须返回 controller 的 `digest(contract)` 为 `contractHash`。未通过时返回机器可比较的 `progressKey`，以及适用的 `failureKey/strategyKey`。
- `reconcile({contract,state,actionId})`：恢复未确定动作时，先核对现实结果。只能返回 `COMPLETED`（附 checkpoint）、有证据的 `NOT_STARTED` 或不确定。未知状态不得重放动作。

验证器必须验证整个 DONE_WHEN，独立于模型的完成宣告，并验证证据对应本合同和当前实际结果。
适配器及其工具调用必须设置阶段超时，并协作检查 shouldStop；控制器无法强制取消不响应的第三方工具。需要硬终止的执行器沿用已有进程/连续性恢复机制，不新造并行 watchdog。
缺少时间/轮数预算、真实验收器、授权边界或适配器哈希时拒绝启动。

## 持久化与恢复

每任务保存 `LOOP-CONTRACT.json`、`STATE.json`、追加的 `RUN-LOG.jsonl`，合同哈希绑定目标、边界、预算与适配器。
当前状态原子写入；日志记录每轮事实。动作前持久化 actionId，重启后先验收，再 reconcile，不凭聊天记忆重做。
同一已关闭任务再次收到时返回原已接受结果，不重复执行。
执行异常保留 pending actionId 和失败状态；恢复时重新投递同一合同和任务编号，不能换新编号逃避去重。
连续性恢复材料必须带任务编号、合同哈希、状态目录、pending actionId和下一动作。
升级后已运行的旧进程不会自动加载新文件；部署/重启须在安全 checkpoint 由现有 Windows 执行桥完成。

## 停止与报告

- `CLOSED（已验证完成）`：完整业务验收通过，任务级 FINAL_VALID=YES。
- `BLOCKED（阻塞）`：无授权可完成路线、验证环境失效、预算达到、两轮无可测进展、相同失败且没有新策略、动作结果不确定；任务级 FINAL_VALID=NO。
- `HUMAN_REQUIRED（需要用户决定）`：授权扩大、真人验证或不可替代的业务选择；FINAL_VALID=NO。
- `STOPPED（用户停止）`：用户 STOP 或状态目录的 STOP 信号，停止后续动作；FINAL_VALID=NO。

预算耗尽只是本轮自动化停止，不证明目标在现实中绝对不可实现。明确报告已尝试路线、失败证据、替代路线和恢复所需条件。
永久终态不自动重新激活；用户决定后应显式创建新的合同版本/任务，并链接原证据，不删除历史。
现有运行 controller 在两种传输路径均调用同一模块；只有 CLOSED 进入业务 done，其余进入非完成报告。

## 本版验证与使用边界

2026-10-04：控制器确定性测试 12/12 PASS；现有 runtime 接线语法检查 PASS。
测试覆盖返修达标、终态去重、副作用后崩溃核对恢复、未知副作用阻塞、无进展、重复失败、无证据假完成、STOP、合同漂移、writer丢失、预算。
这些是本地受控测试，不能替代用户 Windows / ChatGPT 专用浏览器完整 Reality。
`GOAL_LOOP_REALITY=NOT_RUN`；`WINDOWS_DEPLOYMENT=NOT_PERFORMED`；项目级 `FINAL_VALID=NO` 保持不变。
后续生产验收必须通过真实有价值任务，验证自动返修→断连接续→真实业务完成→自动收口，以及不可突破阻塞与用户STOP。

## 实际进程简单验收

`runtime/goal-loop-reality.js`已在 Linux/Node v24.19.0 实际启动独立进程并读写真实文件，4/4 场景 PASS：不合格结果7→返修结果18→真实文件验证→停止且重复运行不重复写；进程写入7后真实退出码73→新进程读取pending→核对原动作→只执行下一轮18；文件结果不再变化→阻塞；STOP文件→不执行。

故障次数与业务返修次数分离；`maxRecoveryAttempts`默认每动作2次，独立计数；故障恢复必须复用既有连续性/备脑链。适配器提供`recover`时，恢复后必须重新验收和reconcile，不能把恢复ACK算业务完成。真实GPT/网页故障尚未用新循环做端到端测试。


## Windows 部署与实际 runtime 验收（2026-10-04 R1）

已将 main 的 v0.5.0 部署到现有 Windows runtime 路径，并在空 inbox、无活跃任务的安全点重启唯一 writer。使用既有 Playwright 依赖路径；未启动第二 supervisor、未另启浏览器、未修改代理。

本轮 Windows 检查：循环 12/12、连续性 25/25、租约 6/6 全通过；实际独立进程/文件场景 4/4；生产唯一 runtime 的实际 inbox 场景 5/5。后者包括 7→18 自动返修与终态去重、异常后原动作核对再续接、同一投递内异常恢复再核对、无进展阻塞、STOP不执行。

修复 Windows 当前进程租约识别；恢复启动时既有 NODE_PATH 配置。所有通过均限定为本轮受控文件任务，不代表任意业务天然有适配器，也不代表真实 GPT/网页故障循环已经验收。

真实网页门：现有专用浏览器进程存在，CDP 9223 不可达；保持原浏览器，禁止另启绕过。因此 GOAL_LOOP_BROWSER_FAULT_REALITY=BLOCKED_EXISTING_BROWSER_CDP，项目 FINAL_VALID=NO。

权威证据：evidence/V050-WINDOWS-GOAL-LOOP-REALITY-20261004-R1.json。历史 NOT_RUN/NOT_PERFORMED 段落是本轮之前的记录，当前部署与验收以上述证据为准。
