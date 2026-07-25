# Loop 跨重启适配合同

## 职责边界

Loop 负责目标、当前事实、游标、验证、预算和停止条件。重启适配器只负责：

```text
Loop 已保存状态
→ Arm 一次启动交接
→ 外部控制器重启
→ AtStartup 调用固定入口
→ Loop 只运行一轮
```

不得把 `LOOP-CONTRACT.json`、完整历史、业务命令或任意脚本路径复制进重启 checkpoint。不得让重启适配器判断业务是否完成。

## 状态映射

| Loop 结果 | 适配器动作 | 后续 |
|---|---|---|
| `REBOOT_REQUIRED` | `Arm` 为 `REBOOT_PENDING` | 验证后由调用方请求重启 |
| `PASS` / `CLOSED` | `Complete` | 注销启动 hook |
| `FAIL` / `REPAIR` | 不自动重启 | Loop 进入有界返修 |
| `BLOCKED` / `HUMAN_REQUIRED` | 保留证据并 `Disarm` | 停止自动续接 |

Loop 没有 `REBOOT_REQUIRED` 时不得 Arm。适配器没有返回 `REBOOT_PENDING` 时不得重启。

## 顺序

1. 冻结或读取 `LOOP-CONTRACT.json`。
2. 原子更新 Loop 的 `STATE.json`，把下一动作设为 `REBOOT_REQUIRED`。
3. 向 `RUN-LOG.jsonl` 追加本轮证据。
4. 调用适配器 `Arm`，只传 `RunId`、`ResumeStep` 和 allowlisted `EntryPointId`。
5. 回读适配器状态，验证 revision、代码身份、入口身份和 `REBOOT_PENDING`。
6. 由宿主或现有任务请求重启；适配器和测试夹具均不调用重启。
7. AtStartup 入口读取 Loop 状态，只执行一轮。
8. 本轮再次要求重启时，先保存新 Loop 状态，再用新 revision 重新 Arm。
9. Loop 达标后调用 `Complete`；达到预算或验证失败时进入 `BLOCKED`。

## 两次重启夹具

`scripts/Invoke-TwoRebootLoopFixture.ps1` 建立一个 `goal` Loop：

- 初始启动：写入合同、状态和日志，输出 `FIXTURE_REBOOT_REQUIRED_1`。
- 第一次 guest reboot 后：验证 boot id 已改变，推进一轮，输出 `FIXTURE_REBOOT_REQUIRED_2`。
- 第二次 guest reboot 后：再次验证 boot id 已改变，关闭 Loop，输出 `TWO_REBOOT_LOOP_FIXTURE_PASS`。

每次调用只推进一轮。重复调用同一 boot id 必须转 `BLOCKED`；超过两次重启不得继续；`CLOSED` 后重复调用只能返回已完成，不能重新执行。

建议测试流程：

```powershell
.\scripts\Invoke-TwoRebootLoopFixture.ps1 -Action Initialize
# 外部 VM 控制器执行第一次 guest reboot
.\scripts\Invoke-TwoRebootLoopFixture.ps1 -Action Continue
# 外部 VM 控制器执行第二次 guest reboot
.\scripts\Invoke-TwoRebootLoopFixture.ps1 -Action Continue
.\scripts\Invoke-TwoRebootLoopFixture.ps1 -Action Status
```

验收证据必须包含三个不同 boot id、两条 `REBOOT_REQUIRED`、最终 `CLOSED`、追加式三轮日志和检查点恢复结果。没有真实 guest reboot 时只能标记夹具已建立，不能标记集成测试通过。
