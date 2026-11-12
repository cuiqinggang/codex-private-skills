---
name: gpt-windows-execution-bridge
description: 《Windows执行桥》第15版。用于 Windows 本机文件、命令、Docker、视频、Pi、DSH，以及 D 通道开机接续、断网恢复与验收。默认自动接续固定 Windows D 20261110-02，D 不通时对账后依次走 A、B、C。
---

# 《Windows执行桥》第15版

2026-11-12，北京时间。合并执行桥 V14 与《D通道开机自动接续》V1.3。执行桥后续沿用整数版本号。

## 默认入口与降级顺序

1. Windows 登录后由原任务 `GPT-DevSpace-D-AutoConnect-V13` 接续固定 D。用户发起任务时优先直接使用 **Windows D 20261110-02**，固定入口为 [MCP 地址](https://ogle-grooving-skipper.ngrok-free.dev/mcp)。首次打开工作区后复用该入口返回的 `workspace_id`。沿用已有 OAuth 与工具授权。
2. D 连接失败时，先按现有配方做有限的只读复验并核对在途操作。3 秒作为软判定。一次只读复验后仍不通，或该入口无法调用，再按 **A → B → C** 依次接续。每一级先做轻量只读验证，成功即用。业务命令报错单独处理。
3. A 为 **Remote Desktop Commander**，先识别当前在线设备。B 为 **GPT-Windows-MCP-Bridge**。C 为 **GitHub Actions → Windows 自托管 Runner**。已受理或结果未知的动作先读回对账，确认后按原任务号从未完成处继续。
4. 复用原固定网址、原计划任务和 V14 声音提醒。固定入口复用、故障诊断和授权恢复配方见[开机自动接续 V1.3 原文与配套文件](references/d-channel-boot-autoconnect-v1_3/SKILL.md)。原文作为保留副本，V15 的日常验收口径以本节下方为准。独立技能仍可单独使用，见[开机自动接续 V1.3](https://chatgpt.com/skills?skill_id=6af2d7161e2881918ee244361faebe9d)。

## 开机后的日常验收

1. 用户登录 Windows 后发来验收提示，直接用固定 D 打开 `C:/AI/DevSpace-Benchmark-20261031/fixture`，读取 `channel-probe.txt`，运行 `hostname.exe`。
2. 原入口首次调用即可完成全部探测，且无需手工重连、重新授权或启动服务，读到 `D_CHANNEL_PROBE_R6_OK`、`DESKTOP-4A1EGTM`、退出码 `0`，即登记 **自动接续验收通过**。无需另取工具调用之前已有 ChatGPT 会话的证据。
3. 用户要求将结果归于某次新发生的整机重启时，核对 Windows `LastBootUpTime` 与 Kernel-General 事件 12。只有核实新启动后才把通过登记到该次整机重启。如果用户明确要求在首次调用前保全已有会话证据，按当次要求先记录，再做探测。

2026-11-12 已实测固定入口首次探测通过，三个返回值均正确，无需人工重连。该次读到的 Windows 内核启动时间为北京时间 2026-11-02 20:05:17，最近一次原任务执行为 2026-11-12 18:20:20，返回 0。此条记录对应自动接续可用。

## 持续故障桌面声音提醒（继承 V14）

2026-11-10，原执行桥现已接入提醒；原2分钟健康检查和ngrok重连继续运行。

- 连续两份不同时间的失败回执后，触发“D通道连接异常提醒”；正常情况下约2—4分钟发现持续异常，非硬保证。区分公网不可达、本机服务、访问/授权或健康记录异常，不把所有故障说成整机网络断开。
- 弹窗立即请求一次系统提示音，此后每5秒重复；不点击则持续提醒。同一事件单窗口，最小化不确认；点击“已知晓，停止声音”或X确认本次事件，重连继续，同故障不反复打扰。恢复时窗口自动关闭并复位，新故障重新提醒。
- 新增的是交互式按需任务GPT-D-Connection-Alert，无定时触发器、IgnoreNew、PT0S；只承载窗口，不替代原2分钟检查，窗口等待不占住健康任务。
- 原ensure-connector.cjs在健康回执发布后调用connection-alert.cjs；原文件有before-alert-1794323842957备份，未重启服务或改变代理/认证。UI用Windows Forms Timer与SystemSounds，经原PowerShell guard执行。
- 原任务已实际产生HEALTHY提醒状态。桌面测试记录显示5秒声音调用、窗口确认后停声及已恢复状态自动关闭。没有切断真实网络；物理扬声器可听性不能由日志证明，受音量和系统声音设置影响。
- 如健康检查停止，提醒模块没有额外独立定时触发，不能声称一定覆盖整个Task Scheduler停止。任务调度、无用户登录、睡眠/关机及客户端OAuth错误的完整覆盖未认证。

详见[持续故障提醒部署与验收](references/connection-alert-v1_5.md)。提醒沿用 V14 已部署机制。独立开机接续包仍以 V1.3 为准。

## 网络恢复后自动重连

- 使用两层已部署机制：ngrok进程自带持续自动重连；原计划任务GPT-DevSpace-D-AutoConnect-V13每2分钟（PT2M，无结束Duration）检查一次。登录后延迟30秒。选择2分钟，不等用户再发提示，不新增另一套调度器。
- 任务保持Enabled、StartWhenAvailable、NetworkRequired=false及IgnoreNew。网络检查失败不禁用任务；下一次继续。睡眠/关机、任务延迟及ngrok退避可能延长恢复，不承诺2分钟硬上限。
- 本地服务端口ECONNREFUSED时，原ensure调用已验启动配方；本地OPEN但公网失败时，记录DEGRADED，ngrok继续自行重连，定时检查继续更新健康结果。进程存活不能替代公网通，公网200不能替代原生MCP验收。
- 原固定URL、插件和授权复用；网络故障不要求本人重新创建/登录。明确认证错误才按原OAuth流程处理，不伪称所有授权过期均可无人干预。
- 超时/断线后先保留原结果与回执，连接恢复时按原任务号只读对账，再差量继续；禁止对UNKNOWN写入或业务启动盲重发。
- 持续不通先看ngrok的EOF/心跳/CRL/3200原始证据，不因一次公网失败重启正常业务。只有已证实HTTP受阻才评估官方crl_url HTTPS配方；保持证书吊销校验。
- 当前没有新增强制公网重启器。现有ngrok重连能完成本次真实恢复；不得把“ensure只报DEGRADED”误说成“公网恢复后永远不会再尝试”。

## V14 历史实测

本轮读回原任务设置：PT2M、无重复结束日期、Enabled=true、StartWhenAvailable=true、NetworkRequired=false、IgnoreNew；实际触发原任务后22:47:23健康回执local/public均200、started=false、原PID未变。D原生read返回D_CHANNEL_PROBE_R6_OK，hostname返回DESKTOP-4A1EGTM及退出0（本轮179ms服务端）。

此前22:25:46 ngrok远端EOF→端点3200→22:26:21 CRL下载超时→22:26:32原进程自动重连，随后同插件原生验收通过。约46秒只表示该段有日志的断线。没有手工断网、改代理、重建插件或重启服务。整机重启、长断网、长期稳定和所有令牌刷新情形仍未认证。

- [完整故障与自动恢复证据](references/D-Fixed-Channel-Incident-20261110-2225.md)
- 实际运行根C:/AI/DevSpace-Benchmark-20261031；原任务动作仍为connector/autostart-hidden.vbs→ensure-connector.cjs→已激活ensure-connector-fixed.cjs。
