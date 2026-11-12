# 现状与接续

2026-11-10，Asia/Shanghai。

## 本机已观察

- 当前D原生读文件与hostname通过；入口Windows D 20261110-01，full_access，前次20261109-01已卸载。
- `GPT-DevSpace-D-AutoConnect-V13` 当前Ready；原任务XML为用户登录后30秒及每2分钟检查，LeastPrivilege、IgnoreNew。任务存在不等于重启验收通过。
- 现有ensure复用端口17676；端口未开启时运行原start-connector.cjs；当前start配方每次创建Cloudflare Quick Tunnel并写入随机publicBaseUrl。仅把新固定URL填入插件无法解决下次启动。
- 最新健康回执本机及公网200、服务与隧道存活；其状态明确为SERVICE_READY_PLUGIN_LINK_NOT_VERIFIED。
- ngrok.exe只发现WindowsApps别名；未发现标准两处ngrok.yml，4040管理API未监听。不能据此断定用户没有云端账号。
- 浏览器在访问ChatGPT插件内容时被host安全策略拒绝，禁止通过Pi、原始CDP或其他表面绕过。
- 已打开ngrok官方Dashboard登录页；显示上次使用GitHub登录。用户选择免费ngrok路线，等待本人登录。

## 唯一下一步

本人在https://dashboard.ngrok.com/完成登录，然后核对固定dev domain和本机官方授权。无需购买域名；不在聊天粘贴authtoken。接下来按SKILL.md完成项目级最小适配、一次固定插件连接及原生/重启验收。

## 官方依据（2026-11-10核查）

- https://developers.cloudflare.com/tunnel/get-started/quick-tunnels/ ：Quick Tunnel每次创建更换hostname，临时开发用途。
- https://developers.cloudflare.com/tunnel/get-started/ ：正式Cloudflare发布入口需要账号与域名。
- https://ngrok.com/docs/pricing-limits/free-plan-limits ：免费账号分配固定dev domain，重启agent后不变；免费额度有上限；HTML浏览器请求可能有提示页，OAuth交互须实测。
- https://ngrok.com/docs/gateway/domains ：账号dev domain与自带域名区分；具体后缀以本人Dashboard实际值为准。
- https://help.openai.com/en/articles/12584461-connecting-custom-mcp-servers-in-chatgpt ：连接配置及refresh token维持授权要求。

## 回退

固定入口未通过前保留本次可用Cloudflare入口。配置切换须有原项目文件备份，沿原凭据与OAuth状态；不关认证、不扩白名单。不执行自动重启Windows来验收，等用户实际重启后核对。

## 本轮后续已确认

- 本人已完成ngrok账号登录，官方Domains页面可见专属免费固定域名：`ogle-grooving-skipper.ngrok-free.dev`。
- 官方CLI实际执行返回 `ngrok version 3.39.11-msix-stable`；config check明确返回本机配置不存在，非安装缺失。
- 已在本机启动一次性遮蔽输入配置窗口，等待本人将官方Authtoken粘贴进去。脚本经PowerShell语法解析通过；真实授权成功尚未观察，不宣称已配置。
- `scripts/check-readiness.ps1`已在目标Windows实跑：task_state=Ready、service_metadata=PASS、fixed_origin=NO_QUICK_TUNNEL、next_action=COMPLETE_NGROK_LOGIN_AND_FIXED_ENDPOINT，退出码0只表示检查运行完成。
- 下一步更新为：完成本机官方授权 → 按原启动配方最小适配固定ngrok → 一次固定入口连接 → 原生验收 → 真实重启验收。
- 新技能安装与当前检查通过不表示固定隧道已部署；当前可用D保持原Cloudflare。

## V1.1：2026-11-10 本机授权后实测

- 本人已配置；ngrok官方config check退出0，路径为本人本机ngrok.yml。未提取或输出authtoken值。
- 官方CLI的Node spawnSync version也退出0，证明现有launcher可直接调用，无需重新下载。
- 从原start-connector.cjs与ensure-connector.cjs作必要配置适配，生成根目录start-connector-fixed.cjs与ensure-connector-fixed.cjs。隔离端口17677、独立connector-fixed/config与state；原服务、脚本、任务未覆盖。沿用原Owner凭据，本地复制至新认证配置，未进入交付/日志。
- fixed ensure真实执行：本机OAuth issuer为固定域名，但公网未通过、隧道存活为false，退出2。其本机健康的瞬时结果不能证明公网服务成功。
- ngrok日志明确ERR_NGROK_9009，因继承HTTP/S代理变量而拒绝免费账号连接。只读检查：proxy_url未配置；环境存在ALL_PROXY/HTTPS_PROXY/HTTP_PROXY。不输出变量实际值。
- 当前状态BLOCKED_NGROK_PROXY_9009。尚未执行子进程直连修改；未切换默认入口/开机任务，未删除当前Windows D 20261110-01。没有原生固定连接或重启验收。
- 下一步仅需决定：是否允许ngrok子进程单独不继承代理变量。其余代理设置保持原状。官方修正依据：https://ngrok.com/docs/errors/err_ngrok_9009 。

## V1.2：用户澄清边界后已修正

- 用户确认“不改代理”的目的是保护原联网能力；本次仅ngrok子进程采用复制并过滤代理环境，未改父环境、全局代理或网络配置。
- prepare-fixed.cjs已同步这项薄适配。初次失败遗留的隔离服务经进程命令行身份检查后停止；端口17677关闭再重新启动，未触碰原D。
- 固定服务实跑PASS：ngrok日志client session established / started tunnel；本机与公网OAuth issuer=https://ogle-grooving-skipper.ngrok-free.dev/。
- Node程序化GET：authorization-server与protected-resource/mcp均200，resource精确匹配固定/mcp；refresh_token grant已公布，刷新行为本身尚未测。
- 再次原ensure-fixed执行退出0、started=false、server_pid=30300未变化、server/tunnel alive=true、plugin_url_can_change=false。
- PowerShell检查脚本-Fixed实跑退出0，service_metadata=PASS、fixed_origin=MATCHES_EXPECTED_ORIGIN、native/reboot均NOT_MEASURED。
- 父进程环境仍可见ALL_PROXY、HTTPS_PROXY、HTTP_PROXY（不输出实际值），说明ngrok过滤未改变调用环境。
- 普通PowerShell默认浏览器UA请求出现ngrok免费HTML提示ERR_NGROK_6024，不能当JSON服务通过。API请求正常；首次OAuth浏览器交互由本人按实际页面确认。
- 预备activate-fixed.cjs已语法检查，要求真实新原生验收文件后才允许将原ensure路由到固定版；当前未运行激活，不宣称已接入登录任务。
- 下一步：本人一次性连接Windows D 20261110-02，GPT只验新入口，再激活原任务路由，最后等真实重启验收。

## 固定插件已连接，等待原生工具暴露

- 本人完成ngrok首次Visit Site提示后报告已连接。
- 服务端诊断：2026-11-10T09:00:21.035Z GET、09:00:31.750Z POST，resource为固定origin+/mcp，expected一致、allowed=true。
- Windows D 20261110-02单独full_access设置回执成功。
- 当前会话ALL_TOOLS未找到任何描述含20261110-02的新工具；未通过该入口open_workspace/read/hostname，故标WAITING_NEW_ENTRY，而非NATIVE_RECONNECTED_PASS。
- 会话中另有显示名Windows D、命名空间windows_d_69a00918的工具，两个只读open_workspace返回Internal error；其配置网址未确认，不能把它视作指定编号02，也不能把该错误归给固定新入口。停止尝试该不明入口。
- A备用只读核对：固定服务pid30300、ngrok pid30132及固定URL仍在；固定域名OAuth请求已到达服务。未切换原开机入口，未写伪造native验收文件，未删除当前01插件。
- 唯一下一步：在当前聊天输入框通过@选择Windows D 20261110-02后发送继续，使其工具进入会话；只验新入口。不要重复创建、重新登录或更换固定网址。

## V1.3 最终启用与自动恢复验收

- 新入口工具随后进入会话；只通过Windows D 20261110-02完成open_workspace、探针及hostname，退出0（初次命令服务端83毫秒）。此前未出现工具为会话发现延迟，不是用户创建失败。
- 写入真实native验收文件后执行activate-fixed.cjs；原任务定义不变，原ensure.cjs有备份并改为固定/回退薄封装。原配置和网址发布为固定入口；原路径status/health在每次原ensure退出时同步当前固定状态，避免遗留状态误导旧恢复流程。
- Windows D 20261110-01卸载成功；仅在核对旧项目进程命令行与父子关系后退役旧Quick Tunnel项目，不修改系统服务或网络。
- 曾有调度健康检查public TypeError、任务返回2；保留失败。后续固定metadata恢复，调度返回0。只增加cause_code诊断，不猜改网络、不重启正常服务来掩盖健康检查波动。
- 准备器在原ensure成为薄封装后触发BASELINE_MISMATCH，未覆盖运行配方；已改为从已保存的原ensure-connector.quick-tunnel.cjs读取成熟基线，语法和生成复核通过。
- 受控D项目服务重启：原server30300/ngrok30132停止后，原计划任务自动启动server20052/ngrok27796；同一ngrok网址不变，local/public 200、started=true、任务LastResult=0、Ready。
- 随后同一个Windows D 20261110-02原生read返回D_CHANNEL_PROBE_R6_OK，hostname返回DESKTOP-4A1EGTM及0（服务端85毫秒），无需用户重新登录。没有重启Windows，没有改变系统代理。
- 原位置canonical status与fixed status的PID和URL一致，active marker与原ensure备份均存在。
- 最终状态DEPLOYED_NATIVE_AND_SERVICE_RECOVERY_PASS。只剩实际Windows整机重启、初始token过期刷新与断网恢复未测，不把服务重启替代整机验收。
