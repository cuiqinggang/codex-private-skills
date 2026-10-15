# Orca 子进程环境、模型参数与权限传递审查 V1
日期：2026-10-15
方法：三人行 V2 C002；桥 V6；合同 V1。
范围：固定官方源码 2bb20586ebc39d605e16d95f57420e20a16e7485 的只读审查。没有运行 Orca/Codex、没有修改本机配置、没有创建工作流或重发被拒预检。源码事实不等于本机实际生效值。

## 决定
F001 继续为未批准候选；N002 未批准。必须先解决默认权限与合同不一致，并取得实际子进程证据，才能冻结业务版本。Reality、连续十轮和 AB 配对均保持 0。本报告补充前次静态审查，不替代阶段报告 V2，不发布新技能版本。

## 1. 权限：已查明默认值，尚未证明本机有效值
关键调用链：
resolveAgentStartupPlanInputs → resolveTuiAgentLaunchArgs → DEFAULT_TUI_AGENT_ARGS → YOLO_TUI_AGENT_ARGS。
固定源码给 Codex 的缺省参数为 `--dangerously-bypass-approvals-and-sandbox`。只有配置对象实际拥有 codex 字符串键，或调用方给出本次 agentArgs 覆盖，才不回落这个缺省值；空字符串是显式覆盖，缺键不是。这个字符串在此仅作为源码证据，禁止用于本项目派发。

因此，“沿用原 Codex 登录”不能推出“沿用原沙箱/审批”。worker-start 的参数 schema 以及 GLOBAL_FLAGS 均无 sandbox、approval、tier 或 extra-agent-args 入口；不能虚构这些 worker 参数。宿主启动计划读取 agentDefaultArgs、agentDefaultEnv、agentCmdOverrides；具体隔离配置落点与实际 worker 采用值尚未核实。

准备要求：
- 在本任务隔离 Orca 配置范围内明确指定 Codex 参数，消除上述缺省 bypass；不得调整现役全局配置或所有 agent 的权限开关。
- 单纯清空参数只能证明不追加该 bypass，仍须证明 Codex 最终有效 sandbox=workspace-write、审批按原 on-request/auto-review 边界，不能只看开关名字。
- 审查 command override 前缀、agent 默认参数、项目配置、启动命令及有效配置，排除后层覆盖或权限放宽；不输出凭据。
- 在平台允许的执行条件成立前，不部署或运行上述准备；本报告不是替代原被拒请求的执行脚本。

此外 agentWorkspaceTrustEnabled 未显式为 false 时默认开启。PTY fresh launch 和 structured Codex 均存在预信任入口；markCodexProjectTrusted 会向传入的 config.toml 写 trusted。目录信任与沙箱/审批是不同机制。须约束这项写入在合同允许范围，不能用“hooks 已关闭”代替证明，也不能声称本机已经发生写入。

## 2. 模型：映射已确认，最终采用值待证
worker-start 的 --model、--effort 进入 workerStart 请求；effort 依赖 model。固定 catalog 的未知模型选项包含 ultra，因此 gpt-6.1-sol 不在种子列表不代表该路径必然拒绝。
终端 launch-option 映射：
- model → argv 两项：-m、gpt-6.1-sol
- effort → argv 两项：-c、model_reasoning_effort=ultra
resolveAgentStartupPlanInputs 在存在 sessionOptions 时设 sessionOptionsOverrideAgentArgs=true；对应去重逻辑移除模型/effort 的旧参数。单独调用 resolveAgentSessionOptionLaunch 且保留冲突 trailingAgentArgs 时也有抑制输出的分支，不能把局部函数结果等同最终 argv。

必须记录 requested 与 effective 分栏：model、effort、service tier。priority 仍是合同请求值；worker CLI 无 tier 参数，最终配置来源尚待落实；服务端实际 tier 未知时保持 UNKNOWN。生成参数不证明后端接受、没有降档或没有 fallback。本次未进行模型探测或业务调用。

纠正前次表述：worker 不一定是终端。固定 worker schema 明确跟随用户“新 agent tab”设置，也可能启动 structured 会话；mode 回执含 mode/preferred/reason/detail。不得把终端 argv 映射冒称 structured app-server 端到端证明。正式冻结必须指定并验证一个模式；模式改变按实质变化审查。

## 3. 子进程环境：调用链已前推至 spawn，实际环境仍缺回执
PTY 路径：
启动计划 env → runtime createTerminal → prepareRuntimePtySpawn（cwd、shell、provider、Codex home 选择）→ buildPtyHostEnv → buildRuntimePtySpawnOptions（envToDelete、trust、no-daemon 等）→ provider.spawn。
本地 provider 的 buildLocalPtySpawnEnvironment 从自身 process.env 与 spawn.env 合并，再执行删除、别名和 buildSpawnEnv；最后再次执行 envToDelete。daemon 有独立持久环境，不能用 main/启动器的 process.env 代替。
host-env assembly 还会合并 Windows PATH、配置代理环境、managed account 环境及 hooks/CLI 路径；这些转换均需核对最终值，不因本报告而修改代理。

Codex home 分支：
- selected home 时注入 CODEX_HOME 和 ORCA_CODEX_HOME；
- skip 时删除相关值；
- stripInherited 路径仅当 CODEX_HOME 与旧 ORCA marker 相等时删除 CODEX_HOME，并移除 marker；自定义 CODEX_HOME 不一定被删除。
- custom-home 判定还考虑 Windows USERPROFILE、PowerShell profile 与 Bash startup 设置。
既有 Orca 父进程 HOME/USERPROFILE 为隔离目录。把“system default”理解为真实 A 用户 home 尚无依据；显式指向实际用户 home 也可能进入 custom/mirror 分支，不能作为已经验证的零复制方案。
旧登录迁移、auth 镜像与 hooks 配置副作用仍承接前次审查，禁止为打通登录而复制凭据。

## 4. 下一次允许执行时必须具备的证据合同（非执行授权）
| 证据组 | 必须记录 | 验收条件 |
| --- | --- | --- |
| 进程归属 | 运行用户、父子 PID、启动时间、provider、runtime/task/dispatch/session 关联 | 排除旧进程、复用错会话与重复协调者 |
| 可执行文件 | Codex 绝对路径、文件摘要、版本；shell/Node 路径 | 固定 Codex 0.160.0，不用父 PATH 推测 |
| 模式与工作区 | 实际 mode、cwd、worktree、repo/输入摘要 | 任务隔离且与冻结一致 |
| 环境白名单 | HOME、USERPROFILE、CODEX_HOME、ORCA_CODEX_HOME、相关隔离标记；PATH 的 Codex 解析结果 | 在实际子进程采集；不输出完整环境、token、密码、auth 文件 |
| 参数 | 脱敏最终 argv；model/effort/tier requested 与 effective | gpt-6.1-sol/ultra；priority 请求与实际 tier 分列 |
| 权限 | 有效 sandbox、审批策略及来源；信任/hooks 设置和配置变更范围 | workspace-write，不放宽原审批；无越界全局改写 |
| 登录 | 使用既有身份的非秘密状态、home 路径关系 | 不复制凭据；不能用一次目录存在判断登录可用 |
| 完整性 | 回执摘要与独立回读；失败/未知字段保留 | 缺值即未验收，不把 ready 或 exit 0 当业务完成 |

实际子进程证据当前均未新增。现有 A 用户会话退出状态仍 UNKNOWN，不能据此启动重复任务。资源、计时及双方修复政策沿用合同与前次审查。structured 端到端权限/RPC 映射仍待源码补齐和实际回执；本报告没有宣称两种模式都已验收。

## 来源清单
全部是上述固定提交的官方源码。Git blob SHA 用于复核，不是 Windows 安装包摘要。
| 文件 | Git blob SHA |
| --- | --- |
| [src/shared/tui-agent-permissions.ts](https://github.com/stablyai/orca/blob/2bb20586ebc39d605e16d95f57420e20a16e7485/src/shared/tui-agent-permissions.ts) | db014311459ce89106e15099bb7c1a9e304d2f92 |
| [src/shared/tui-agent-launch-defaults.ts](https://github.com/stablyai/orca/blob/2bb20586ebc39d605e16d95f57420e20a16e7485/src/shared/tui-agent-launch-defaults.ts) | 5574f31bfc9d2146e31ed23d22f86a4022e43e69 |
| [src/shared/agent-startup-plan-inputs.ts](https://github.com/stablyai/orca/blob/2bb20586ebc39d605e16d95f57420e20a16e7485/src/shared/agent-startup-plan-inputs.ts) | ead55a43715b219a886a773ba8abb01bd8a26ed1 |
| [src/shared/agent-session-option-catalog-claude-codex.ts](https://github.com/stablyai/orca/blob/2bb20586ebc39d605e16d95f57420e20a16e7485/src/shared/agent-session-option-catalog-claude-codex.ts) | 6925b92a869790a8ca6149c6d421583412c0c7e9 |
| [src/shared/agent-session-option-launch.ts](https://github.com/stablyai/orca/blob/2bb20586ebc39d605e16d95f57420e20a16e7485/src/shared/agent-session-option-launch.ts) | e8c972385bdca797eb6ca107fe55c33403a17b79 |
| [src/shared/cli-argument-boundary.ts](https://github.com/stablyai/orca/blob/2bb20586ebc39d605e16d95f57420e20a16e7485/src/shared/cli-argument-boundary.ts) | 03fe4a1d2fc41c5447816e7e34f0ba1e5ffe5c3f |
| [src/main/ipc/pty/runtime/spawn-preflight.ts](https://github.com/stablyai/orca/blob/2bb20586ebc39d605e16d95f57420e20a16e7485/src/main/ipc/pty/runtime/spawn-preflight.ts) | c82b0656a377017f0cdf15bf1ea8aaf1311e41bb |
| [src/main/ipc/pty/runtime/spawn-options.ts](https://github.com/stablyai/orca/blob/2bb20586ebc39d605e16d95f57420e20a16e7485/src/main/ipc/pty/runtime/spawn-options.ts) | 26c3856b45ee0e4186e6ea7dc3d3df82d4e2b124 |
| [src/main/ipc/pty/runtime/spawn-execute.ts](https://github.com/stablyai/orca/blob/2bb20586ebc39d605e16d95f57420e20a16e7485/src/main/ipc/pty/runtime/spawn-execute.ts) | 8228175a2cf125ffc9fa18405e0865fd97a6d250 |
| [src/main/providers/local-pty-spawn-environment.ts](https://github.com/stablyai/orca/blob/2bb20586ebc39d605e16d95f57420e20a16e7485/src/main/providers/local-pty-spawn-environment.ts) | 462c7c781a9b5d23934e3b594bdaffbfa734283b |
| [src/main/ipc/pty/host-env/assembly.ts](https://github.com/stablyai/orca/blob/2bb20586ebc39d605e16d95f57420e20a16e7485/src/main/ipc/pty/host-env/assembly.ts) | 0fe3faf375e726c85e028260d8388ada429a7084 |
| [src/main/ipc/pty/host-env/codex-home.ts](https://github.com/stablyai/orca/blob/2bb20586ebc39d605e16d95f57420e20a16e7485/src/main/ipc/pty/host-env/codex-home.ts) | 3b79c0e7876e40fb946a106d91a2f26c984a56ff |
| [src/main/agent-workspace-trust-spawn.ts](https://github.com/stablyai/orca/blob/2bb20586ebc39d605e16d95f57420e20a16e7485/src/main/agent-workspace-trust-spawn.ts) | f893529b53b8dcdfc11512bf1b5bb61bbeb3315c |
| [src/main/agent-trust-presets.ts](https://github.com/stablyai/orca/blob/2bb20586ebc39d605e16d95f57420e20a16e7485/src/main/agent-trust-presets.ts) | eac0591728bb0d1d8b62458296df41e6766d09d9 |

附加已读来源：orchestration-worker-specs.ts、worker-launch-handler.ts、agent-command-plan.ts、agent-launch-surface-factories.ts、orca-runtime-create-agent-session.ts、codex-real-home-path.ts。原通用安全拒绝原因仍未知，不索取重复截图、不重发受限动作；独立静态审查与归档继续。
