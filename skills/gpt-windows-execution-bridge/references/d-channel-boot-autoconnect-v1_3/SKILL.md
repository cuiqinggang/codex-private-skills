---
name: d-channel-boot-autoconnect
description: 管理《D通道开机自动接续》V1.3，复用Windows现有登录启动任务、官方ngrok固定网址与原DevSpace/OAuth，为GPT或Pi检查服务、接续固定插件并验证重启恢复。用户要求开机免手工重建D、自动连接、固定入口或升级此流程时使用。固定原生入口与原计划任务已启用，D服务重启自动恢复已验收；真实整机重启仍待验。
---
# D通道开机自动接续

版本：V1.3。2026-11-10，Asia/Shanghai。
当前阶段：`DEPLOYED_NATIVE_AND_SERVICE_RECOVERY_PASS`。默认Windows D 20261110-02；原计划任务已启用固定版，服务重启后同网址、同插件、原授权自动恢复并通过原生验收。旧01插件和旧Quick Tunnel进程已清理。2026-11-11 首次原生调用通过，Windows 本轮记录为电源唤醒，整机重启及初始令牌过期后的刷新仍未测。

## 简单成熟路线

沿用“Windows原登录任务 → 原ensure配方 → 官方ngrok固定HTTPS网址 → 原DevSpace/OAuth”。不需要GPT或Pi常驻推理，不新造浏览器、调度器或网络核心。固定版已成为默认入口；日常不得重新建插件或重跑安装。原Quick Tunnel只保留项目级回退配方，不继续运行。

## 正式边界

用户2026-11-10澄清：禁止改代理是为了保护整机已有联网能力。已明确允许本任务按成熟方法解决。只为ngrok子进程复制process.env并移除HTTP_PROXY/HTTPS_PROXY/ALL_PROXY/http_proxy_env；父进程、Windows全局环境、系统代理、FlClash、DNS、防火墙及其他程序全部保持原样。此范围已获授权，不重复询问。不要扩大为其他代理改动。
秘密仅在本机官方配置中使用，不进入聊天、技能或共享证据。免费账号，不购买域名、不升级套餐。

## 已验证路径

- 根：`C:/AI/DevSpace-Benchmark-20261031`；现有任务：`GPT-DevSpace-D-AutoConnect-V13`。
- 原D：`Windows D 20261110-01`，17676，connector；旧项目已退役，原任务定义未改，原ensure入口已通过有回退的薄封装路由到固定版。
- 固定版：官方ngrok 3.39.11，`https://ogle-grooving-skipper.ngrok-free.dev/mcp`，17677，connector-fixed。
- 固定配方：根目录 `start-connector-fixed.cjs`、`ensure-connector-fixed.cjs`，由本包prepare-fixed.cjs从原已验脚本作必要适配生成。沿用DevSpace和原Owner凭据，隔离配置与OAuth状态。
- 实测：本机和公网issuer一致；公网authorization-server及protected-resource/mcp均JSON 200；server/tunnel存活；重复ensure显示started=false、同一服务PID，无重复启动。完整原生插件与重启恢复仍未认证。

## 日常默认路径

1. 正常登录Windows后，原GPT-DevSpace-D-AutoConnect-V13任务调用原ensure-connector.cjs薄封装，选择已激活的ensure-connector-fixed.cjs。无需每天新建插件、复制网址或输入Owner密码。
2. GPT/Pi执行Windows任务优先复用Windows D 20261110-02。若仍有效直接工作；不要因新日期而重新编号。首次进入会话按新入口open_workspace并复用返回的workspace_id。
3. 当前固定runtime为connector-fixed，端口17677；原connector/status.json与autostart-health.json由原入口执行完后同步为当前固定状态，原config/config.jsonc及CONNECT-URL.txt已指向固定配置。旧配置有before-fixed备份。
4. 失败按当前执行桥有限只读恢复；UNKNOWN先对账。日志200不替代原生工具，但一次公网健康检查失败也不能在原生连接正常时杀服务。已观察两次调度健康检查TypeError，后续成功，保留历史，不夸大全天SLA。
5. 只在真实失效时按成熟恢复配方处理。下面首次安装步骤仅供回退/重新接入参考，不作日常开机动作。

## 首次安装或真正失效后的接续

1. 从当前状态与[证据](references/current-state.md)接续，不重装ngrok、不重配账号、不回退已解决的9009。
2. 在ChatGPT建立 `Windows D 20261110-02`，URL为上述固定/mcp，OAuth及原固定长字符串保持原用途。三项资料各自独立代码块，一项一键复制。ngrok免费HTML页面可能首次出现服务提示页；这是官方服务提示，不是已完成OAuth。由本人在界面完成必要连接。
3. 当前浏览器工具明确拒绝操作chatgpt.com，不得转交Pi、原始CDP或其他工具绕过这个拒绝。只交付必要一次手工连接；后续固定网址正常复用，不每天重建。
4. 新编号工具出现后，仅用新入口open_workspace、read(channel-probe.txt)、hostname.exe。必须得到D_CHANNEL_PROBE_R6_OK、DESKTOP-4A1EGTM、退出码0；原工作区句柄不跨插件假定复用。
5. 验收通过后在fixture写 `d-channel-fixed-native-acceptance.json`：status=NATIVE_RECONNECTED_PASS、entry=Windows D 20261110-02、hostname=DESKTOP-4A1EGTM、exit_code=0。仅可写真实已观察结果，禁止伪造该文件跳过验收。
6. 执行本包 `scripts/activate-fixed.cjs`：备份原ensure为ensure-connector.quick-tunnel.cjs，原ensure入口仅变为固定版/原版选择薄封装；connector-fixed/active.json启用固定版。原计划任务名称、触发器、权限和动作无需变化。此步骤已执行并通过原计划任务实际调用；当前active.json已存在，不重复激活。脚本同步原位置配置与网址，并让原ensure在进程退出时发布当前状态，避免旧技能读到退役URL。
7. 设置新插件已授权full_access，成功后删除前次插件并核对。确认原Quick Tunnel项目进程身份后按需要退出旧项目进程，避免并跑两套服务；不得停止系统服务或无关程序。
8. 更新本技能及执行桥默认入口。用户真实重启后核对同URL、同插件、无手工重建，再认证开机自动化；不擅自重启Windows。OAuth刷新和断网恢复分别验收，不由metadata推定。

## 检查与回退

- 默认只读核查：PowerShell7运行 `scripts/check-readiness.ps1`；脚本自动检测active.json，固定版激活后默认检查17677，避免误读退役17676。
- 固定版核查：加 `-Fixed -ExpectedOrigin https://ogle-grooving-skipper.ngrok-free.dev`。程序化请求使用明确应用User-Agent，依ngrok官方文档读取API；不声称这证明用户浏览器或ChatGPT连接。
- ngrok账号配置已通过，不重复运行configure-ngrok.ps1。prepare-fixed.cjs只用于首次准备或明确配方更新，不每次开机重生成。
- activate脚本要求原生证据；没有就停止激活。激活后回退：恢复已备份原ensure入口，按before-fixed备份核对原配置，保留固定配置与证据；已确认副作用先对账。
- 失败原始记录保留：9009因继承代理，已按官方仅子进程直连修正。不要重新改全局代理或以付费升级解决。

## 验收账本

固定服务与配置检查=PASS；新ChatGPT原生入口=PASS；原任务调用固定版=PASS；D项目服务重启后的自动恢复与同插件授权复用=PASS；真实整机重启=NOT_MEASURED（2026-11-11 未观察到新内核启动）；初始授权过期后的刷新=NOT_MEASURED；断网恢复=NOT_MEASURED。证据见 [服务重启验收](references/accepted-20261110.json) 与 [2026-11-11 整机重启核验](references/reboot-check-20261111.json)。
核对 Windows LastBootUpTime 和 Kernel-General 事件 12，区分电源唤醒与整机启动。只有观察到本次新启动、原任务在该次启动后成功执行、固定网址一致且未经干预的首次原生验收通过，才记录首次开机自动连接成功。工具未进入会话单独记录。
程序退出0、服务200、任务Ready、技能保存或GPT网页已登录均不能替代最终原生与重启验收。只报告观察结果；时间按分:秒:毫秒，没有完整计时不编造T_VALID。
