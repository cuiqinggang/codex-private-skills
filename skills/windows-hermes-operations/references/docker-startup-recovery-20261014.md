# 爱马仕启动故障：Docker 数据盘未识别（2026-10-14 实证）

## 适用范围与入口
处理“爱马仕打不开、8642健康但3000不可用、Docker一直正在启动、开机自动打开失败”时先读本页。复用现有安装，不重装、不新建工作站，不恢复旧 WSL Hermes。
以下为本次实证快照，操作前只核对涉及的入口、端口及进程，不能假定永远不变：
- 当前运行版本：Windows 原生 Hermes 0.21.5；数据目录：`C:\Users\A\.hermes`。
- 现用启动器：`C:\Users\A\Hermes_Windows_Native_014\launcher\start-hermes-openwebui.ps1`。
- 手动入口：桌面 `打开爱马仕.cmd`；旧 `H:\Hermes_Windows_Native_014\打开爱马仕页面-双击.cmd` 已恢复为转调入口。
- 登录入口：Startup 内 `HermesOpenWebUIAutoOpen.vbs` → `C:\Users\A\Hermes_AutoStart\openwebui-autoopen\Open-HermesOpenWebUI.ps1` → C盘现用启动器。
- 不能因历史目录仍含“014”就降级当前运行版本；旧 H盘 launcher 不存在不等于整个安装丢失。
- 旧 `HermesNewApiAutoRecover_Logon` 等任务本次发现为 Disabled；不要依据旧文档自行重新启用。

## 最短诊断顺序
1. 核对8642监听进程的实际路径/命令行、`/health` 与最近一次启动日志。健康的 Windows Hermes 不重启。
2. 模型接口401先判断认证：通过既有本机授权机制请求，不把未认证401当成超时、WSL抢占或坏进程；不关闭认证。密钥只在本机使用，不输出、上传或存入报告。
3. 从授权 `/v1/models` 发现实际模型ID。本次有 `DeepSeek-V4.1-Flash` 等五项，不再强制旧 `hermes-agent` 名称。
4. 若8642通过但3000失败，查Docker API、`docker desktop status`、原容器 `open-webui-clean` 及最新 `daily-start-*.log`，不要继续修Hermes。
5. Docker长期starting且API超时，检查 Docker host日志的首个具体错误，区分数据盘设备未识别、文件缺失、权限失败及其它原因。

## 本次故障与证据
- 18:35:59 Hermes通过；18:42:00 Docker API等候300秒后失败。
- Docker报错：`provisioning data: detecting disk: no sd* disk ... wwid ...`。
- `C:\Users\A\AppData\Local\Docker\wsl\disk\docker_data.vhdx` 文件仍在，大小34468790272字节。
- 因此已定位到Docker/WSL内数据盘设备未就绪；不能声称磁盘文件丢失、损坏，或已查明最初触发原因。
- 官方 `docker desktop restart --timeout 60` 因明确列出的Docker进程未退出而失败。延长Hermes等待或反复开Docker窗口没有解决这一层问题。

## 成熟恢复顺序
在用户已授权修复、确认影响范围后：
1. 先使用官方 `docker desktop restart --timeout 60`，给外层命令限时并检查退出码和实际就绪状态。
2. 仅当官方停止失败且进程残留已明确，现场重新核验进程可执行路径，精确结束该次Docker前后端残留。不得复用历史PID、按宽泛通配符杀进程或自动扩大清理范围；先确认其它Docker任务受影响情况。
3. 只执行 `wsl --terminate docker-desktop`。如证据需要解绑数据盘，只指定上述已核实的完整vhdx路径执行 `wsl --unmount <完整路径>`。本次该步返回未挂载/ERROR_FILE_NOT_FOUND，不可写成解绑成功或文件丢失。
4. 使用官方 `docker desktop start --timeout 90`；命令成功仅代表启动请求，要继续验证Docker API、原容器和网页。
5. 原容器已自动恢复就不重复start；只有已存在的目标容器未运行时启动它。
禁止默认执行factory reset、删除容器/镜像/卷/vhdx、unregister、磁盘修复、全局WSL shutdown或重装；不修改FlClash、系统代理，也不关闭用户已登录浏览器。
本次强制残留清理仅为现场限定恢复，未加入开机自动循环。

## 已部署的最小防复发修改
- Docker CLI探针外层限时8秒，使用进程退出码判断；不能只靠轮询总deadline，因为单次CLI可能卡住。
- 常规等候失败后最多一次官方restart；外层65秒，成功后再等API最多180秒；失败明确退出，保留数据。
- 默认入口逻辑修正为 `((Test-WindowsHermesModels) -and ...)`，避免把-and作为命令参数；全部健康时跳过固定90秒等待。
- 修改前目标文件逐字节备份，验证后保留回滚；不拿历史脚本整套覆盖较新的本机版本。
- 本次备份后缀：`.bak-20261014-docker-recovery`。
- 本次Windows修复后SHA256：`38EADDD4810CDE4D4DED62BCB54531BCB78593E89AE0702DA6CC45D709772CA0`；后续变更须重新核验，不能硬要求一直相同。
- 修改后的PowerShell通过既有 `powershell-reliability-guard/scripts/Invoke-GuardedPowerShell.ps1` 执行，目标WindowsPowerShell51。

## 验收及防误报
本次已通过：统一执行门及解析、Pester三分支3/3、8642健康、授权模型列表、DeepSeek真实回复、容器healthy、3000/health=200、Open WebUI容器使用现有连接配置访问Hermes模型列表200、默认入口FINAL_PASS、浏览器打开命令成功。
仅有HTTP200不足以代表聊天全链路；仅有打开命令成功不足以代表已目视验收。
Open WebUI连接配置验证若需要数据库，只读连接配置，先确认schema：本次config为key/value表，不能套旧id/data表结构；不得读取用户聊天或输出密钥。
未验证：整机重启/下次登录恢复、浏览器实际聊天端到端、长期稳定或连续五轮无故障；不继承为PASS。
7.52秒只是一次热启动执行门耗时，不是修复全程耗时，不证明全局最优。PSScriptAnalyzer未安装，不宣称其通过。

## 固定证据与可复用源文件
权威仓库：`cuiqinggang/codex-private-skills`。
归档提交：`4c48e249ca9c18ecde014d8b2e43f753a1f13139`。
目录：`workspaces/hermes-startup-repair-20261014/`，包含REPORT.md、start-hermes-openwebui.ps1、docker-recovery.Tests.ps1、START-HERMES-WEBUI.cmd。
[完整实证记录](https://github.com/cuiqinggang/codex-private-skills/blob/4c48e249ca9c18ecde014d8b2e43f753a1f13139/workspaces/hermes-startup-repair-20261014/REPORT.md)
[Docker官方恢复方法](https://docs.docker.com/desktop/troubleshoot-and-support/troubleshoot/)
[Docker Desktop CLI](https://docs.docker.com/desktop/features/desktop-cli/)
[WSL精确终止与解绑](https://learn.microsoft.com/windows/wsl/reference)
