# 长期记忆超级虚拟人 v1.0｜当前摘要

```ini
PROJECT=长期记忆超级虚拟人
WORKSPACE_VERSION=v1.0
SKILL_VERSION=v0.1.0
SKILL_ENGLISH_NAME=Long-Term Memory Super Virtual Human

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

LOCAL_MAIN_SNAPSHOT_BACKUP=IN_PROGRESS
LOCAL_MAIN_SNAPSHOT_RUN_ID=36997334861
FULL_GIT_HISTORY_MIRROR=NOT_YET_PASS
LOCAL_BACKUP_TARGET=C:\\actions-runner-etal\\_local-backups\\codex-private-skills

DESKTOP_COMMANDER_REMOTE=OFFLINE_AFTER_TEMPORARY_RECONNECT
DESKTOP_COMMANDER_PAIRING_RESTORE=PASS
DESKTOP_COMMANDER_TOOL_COMMAND_CHANNEL=NOT_STABLE
DESKTOP_COMMANDER_AUTOSTART_INSTALLER_PREP=QUEUED
DCR_INSTALLER_PREP_RUN_ID=36997636632

GITHUB_RUNNER_ACCOUNT=NETWORK_SERVICE
INTERACTIVE_WINDOWS_USER=A
```

## 已冻结判断

- 项目名称固定“长期记忆超级虚拟人”。
- 英文名固定 **Long-Term Memory Super Virtual Human**。
- 首个技能包版本为 `v0.1.0`，目录 `skills/long-term-memory-super-virtual-human/`。
- 长期记忆是项目核心，不省略。
- GPT 当前是主脑首选候选，但是否完整最快必须用 Reality 证明。
- 能力采用“轻入口、强后端、按需路由”，不把所有工具常驻上下文。
- Codex 是强执行器，不是唯一执行器。
- 2.0 方法作为重要工作方法和参照，不把任何实现流程写死。
- 长流程采用“稳定规则 + 权威任务合同 + Checkpoint + Reality 验证”。
- 页面不是长期事实库；必须建立 Checkpoint + 权威项目状态。
- GPT 本身必须有独立强备份。
- 旧 v5.6.5 保留为历史参照与故障经验，不再作为当前唯一方法。

## Desktop Commander 当前 Reality

本轮用户已成功恢复 persisted session：
- Session restored；
- Device 曾重新标记 Online；
- Pairing restore = PASS。

随后 GPT 对 Remote 的 `ping / list_directory / start_process` 仍发生超时，之后设备再次显示 Offline，因此不能把“Presence Online”当成完整工具链 PASS。

已确认：
- GitHub Windows runner 仍能接收任务；
- runner 身份是 `NETWORK SERVICE`；
- A 用户才持有 Desktop Commander 用户会话；
- runner 无权替 A 注册用户级计划任务，这是正常 Windows 隔离；
- 不扩大服务账户权限。

当前方案：
- runner 先在共享目录准备 A 用户级安装器；
- A 用户只需运行一次；
- 安装器注册“登录自动启动”任务；
- launcher 自循环，Remote 退出后 5 秒重连；
- 再做重登 / 重启 Reality。

安装器准备任务：Run `36997636632`，当前 Windows Reality 排队。

## 仓库第二备份

“完整 Git mirror”多次失败原因已经分离：
1. Windows→GitHub HTTPS 临时 reset；
2. runner 没有 A 用户 `gh` 登录态；
3. 改为 GitHub Actions 短期令牌后，完整 mirror 长连接在约 26 分钟处 `early EOF`。

因此先保证当前成果不丢：
- 正在下载当前 main 的完整 ZIP snapshot；
- 带 SHA256 和 archive entry 验证；
- Run `36997334861`；
- 目标 `C:\actions-runner-etal\_local-backups\codex-private-skills\snapshots`。

完整 Git 历史 mirror 保留为第二阶段增强，不能冒充已完成。

## 当前最优先

1. 完成 Desktop Commander A 用户级常驻并 Reality 复验；
2. 完成当前 main 本地快照第二备份；
3. 打造 GPT 直控主路线 v0.1 Reality；
4. 同批正式任务比较 A/B/C 三路线；
5. 主路线稳定后立即进入 GPT 不可用时的独立强备份 Reality。

## 未解决且不得消失

- GPT Checkpoint / 自动换页恢复；
- GPT 服务不可用时的独立强备份；
- ChatGPT 当前会话模型 / 思考强度的可编程切换；
- GPT 无响应时如何自动触发新会话恢复；
- 路线 C 多层 Agent + 自动化编排的 Reality 可用性；
- 完整 Git 历史 mirror 的稳定本地备份。
