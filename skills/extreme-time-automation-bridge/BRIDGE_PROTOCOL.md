# 无决策权自动执行桥协议 v0.1

## 1. 角色

- GPT：唯一决策者。
- GitHub：任务总线、版本与证据载体。
- Windows自托管运行器：机械执行。
- 可选回调端：任务结束后唤醒上层调度器；不拥有方案决策权。

## 2. 任务生命周期

```text
任务JSON进入 main
→ GitHub Actions触发
→ 静态合同检查
→ 自托管Windows领取
→ Invoke-BridgeTask.ps1校验
→ 执行payload
→ 生成result.json/stdout/stderr
→ 上传Actions artifact
→ 若配置回调地址则POST结果
```

## 3. 任务格式

```json
{
  "schema_version": 1,
  "task_id": "唯一任务编号",
  "payload_path": "workspaces/extreme-time-automation-loop-v2.0/bridge/payloads/xxx.ps1",
  "timeout_seconds": 120,
  "expected_exit_code": 0
}
```

任务本身不携带自由决策文本；它只引用同一提交中的受版本控制 payload。

## 4. 最小入口

唯一最小入口是：

```text
bridge/tasks/<TASK_ID>.json
```

GPT通过 GitHub 写入任务文件即可派发。任务文件、payload、执行器和工作流都可由提交SHA追溯。

## 5. 结果

每次执行最少产生：

- result.json
- stdout.txt
- stderr.txt
- GitHub Actions run/job/step 状态
- artifact

失败也是合法现实结果；执行桥不得自行修复。

## 6. 自动继续

桥本身负责“执行并回传”。要实现跨小时/跨天的完全无人决策循环，上层需要一个常驻调度/回调端在 result 到达后重新调用 GPT。
工作流已预留仓库 Secret：ETAL_BRIDGE_CALLBACK_URL。
未配置时，桥仍可执行并保存结果，但不会自动唤醒新的 GPT 决策轮。

## 7. 计时

平台首次安装时间单独记录为 T_PLATFORM_BOOTSTRAP，不伪装成单个标准题 T_VALID。
只有当桥已 Reality 认证并作为复用基础设施存在后，Case 001 才能正式起表。
