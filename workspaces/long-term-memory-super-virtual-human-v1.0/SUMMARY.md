# 长期记忆超级虚拟人 v1.0｜当前摘要

```ini
PROJECT=长期记忆超级虚拟人
VERSION=v1.0
STATE=10
VIRTUAL_MATURE=NO
FINAL_VALID=NO

PRIMARY_BRAIN_CANDIDATE=GPT
OBJECTIVE=T*=min(T_VALID)

CONSTITUTION=极限短时间智能体宪法 v0.3.1
METHOD_REFERENCE=极限短时间自动化闭环 v2.0
WINDOWS_BRIDGE=GPT直连Windows双路执行桥 v0.2.0

MISSING_CORE_1=GPT_CHECKPOINT_AND_SESSION_RECOVERY
MISSING_CORE_2=GPT_INDEPENDENT_STRONG_BACKUP
MODEL_THINKING_AUTOMATION=OPEN

LOCAL_REPO_SECOND_BACKUP=DEDICATED_WORKFLOW_IN_PROGRESS
LOCAL_REPO_BACKUP_RUN_ID=36992141819
LOCAL_REPO_BACKUP_TARGET=C:\\actions-runner-etal\\_local-backups\\codex-private-skills

DESKTOP_COMMANDER_REMOTE=OFFLINE
DESKTOP_COMMANDER_OFFLINE_ROOT_CAUSE=LOCAL_REMOTE_DEVICE_PROCESS_NOT_RUNNING
DESKTOP_COMMANDER_AUTOSTART=BLOCKED_UNTIL_USER_SESSION_RECONNECTED_ONCE
GITHUB_RUNNER_ACCOUNT=NETWORK_SERVICE
INTERACTIVE_WINDOWS_USER=A
```

## 已冻结判断

- 项目名称固定“长期记忆超级虚拟人”。
- 长期记忆是项目核心，不省略。
- GPT 当前是主脑首选候选，但是否完整最快必须用 Reality 证明。
- 工具按需调用；Codex 是强执行器，不是唯一执行器。
- 2.0 方法作为重要工作方法和参照，不把任何实现流程写死。
- 页面不是长期事实库；必须建立 Checkpoint + 权威项目状态。
- GPT 本身必须有独立强备份。
- 旧 v5.6.5 保留为历史参照与故障经验，不再作为当前唯一方法。

## Desktop Commander 当前 Reality

官方 Remote Device 必须在目标电脑本机运行；进程停止后设备即 Offline，持久化会话通常可在重新启动后复用。

本轮已确认：
- GitHub Windows runner 仍能接收任务；
- runner 当前执行身份是 `NETWORK SERVICE`；
- A 用户才持有原 Desktop Commander 配对会话；
- 服务账户不能写 `C:\Users\A\AppData\Local`，因此不能替 A 强行安装用户级自启动；
- 不扩大服务账户权限。

下一动作：
1. A 用户执行一次 `npx @wonderwhy-er/desktop-commander@latest remote`；
2. Remote Online 后由 GPT 直连进入 A 用户环境；
3. 再创建用户级“登录自动启动 + 异常重启”；
4. 重启/重新登录 Reality 验证。

## 仓库第二备份

目标：
- 完整 mirror；
- 独立 `.bundle`；
- SHA256；
- 本机路径 `C:\AI\backups\codex-private-skills`。

第一次因 Windows→GitHub HTTPS 临时 reset 未进入正文；第二次成功进入正文后发现 runner 服务账户没有 A 用户的 `gh` 登录态（`GH_AUTH_REQUIRED`）。

已改为专用短期令牌工作流，不保存长期 Token：Run `36992141819` 当前正在本机生成完整 mirror + `.bundle` + SHA256。

## 当前最优先

1. 恢复 Desktop Commander Remote 并完成 A 用户级常驻；
2. 完成本地完整第二备份；
3. 打造 GPT 直控主路线 v1.0 Reality；
4. 同批正式任务比较 A/B/C 三路线；
5. 主路线初步稳定后，建立 GPT 不可用时的独立强备份。

## 未解决且不得消失

- GPT Checkpoint / 换页恢复；
- GPT 服务不可用时的独立强备份；
- ChatGPT 当前会话模型 / 思考强度的可编程切换；
- GPT 无响应时如何自动触发新会话恢复；
- 路线 C 多层 Agent + 自动化编排的 Reality 可用性。
