---
name: extreme-time-automation-bridge
version: "0.1.0"
description: 极限短时间自动化闭环的无决策权执行桥。GPT负责判断，执行桥只负责领取、执行、记录和回传；正式任务运行期间用户人工介入必须为0。
---

# 极限短时间自动化执行桥 v0.1.0

```ini
STATUS=REALITY_CANDIDATE
VERSION=0.1.0
REALITY_CERTIFIED=NO
USER_INTERVENTION_DURING_TASK=0
CORE_BRAIN=GPT
BRIDGE_DECISION_POWER=NONE
TRANSPORT=GitHub
WINDOWS_EXECUTOR=GitHub_SELF_HOSTED_RUNNER
```

## 目标

把“GPT → 人工中继 → Windows”替换为：

```text
GPT
→ GitHub任务入口
→ Windows自托管运行器
→ Reality执行
→ 机器结果/证据
→ 自动回传
```

执行桥不是第二个智能体，不负责选方案、修改目标、判断根因或宣布最终完成。

## 最小任务入口

```text
workspaces/extreme-time-automation-loop-v2.0/bridge/tasks/<TASK_ID>.json
```

向 main 写入一个新的任务文件，就是一次机器派发事件。GitHub 工作流监听该目录，不需要额外“派发 API”。

## 有效性硬规则

1. 正式任务从启动后到 FINAL_VALID，用户人工中继次数必须为0。
2. Windows执行器只能执行任务中明确引用的 payload，不自行改任务。
3. 网络代理与 FlClash 不得修改。
4. 不得进行 Windows 系统破坏性操作。
5. 结果必须机器记录；失败原样回传，不得伪装成功。
6. GPT 仍是路径A唯一决策大脑。
7. 本桥属于实现层，不修改“极限短时间智能体宪法 v0.3”。

## 现实状态

v0.1.0 已实现仓库侧协议、任务入口、Windows执行器脚本、GitHub Actions 工作流和最小冒烟任务。
只有自托管 Windows runner 实际领取并通过冒烟任务后，才能把 REALITY_CERTIFIED 改为 YES。
