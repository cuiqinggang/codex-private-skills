# 路径A｜GPT原生全自动闭环协议 R1

```ini
PATH=A
CORE_BRAIN=GPT
CODEX=NO
MANUS=NO
USER_INTERVENTION_DURING_TASK=0
EXECUTION_BRIDGE=extreme-time-automation-bridge v0.1.0
```

## 定义

路径A不是“GPT + 人工操作员”。路径A是：

```text
GPT判断
→ 无决策权执行桥
→ Windows Reality
→ 自动机器验收/结果回传
→ GPT下一轮判断
→ 循环
→ FINAL_VALID
```

正式任务执行期间，只要需要用户复制命令、查看失败、转述结果、选择下一步或人工验收，路径A即判 INVALID。

## 启动前门禁

Case 001 起表前必须满足：

1. 执行桥 Reality 冒烟 PASS。
2. Windows runner 可无人领取任务。
3. 任务结果可自动保存。
4. 机器可验事实可自动判断。
5. 上层自动回调/调度已具备，或明确由同一持续运行 GPT/Work 会话自动消费结果；不得依赖用户回来继续。

## 时间

执行桥首次安装建设计入 T_PLATFORM_BOOTSTRAP，单独保存。
标准题 T_VALID 从“候选系统在桥已可用条件下收到冻结原始需求”开始。
