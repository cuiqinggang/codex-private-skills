# Hermes 启动修复｜2026-10-14
任务授权：使用《三人行》第2版（仅本任务）、GPT直连Windows双路执行桥 V1.0，恢复现有 Hermes/Open WebUI。
执行通道：用户自建 GPT-Windows-MCP-Bridge；未使用第三方 Remote 配额。
状态：CURRENT_RUNTIME_PASS；REBOOT_NOT_TESTED；UI_VISUAL_NOT_INSPECTED。
## 根因与范围
- 当前 8642 是 Windows 原生 Hermes 0.21.5，PID 3100，非旧 WSL relay。无认证 /v1/models 返回401属于正常认证保护；本机已有认证请求返回200及五个模型。
- 实际入口已迁至 C:/Users/A/Hermes_Windows_Native_014；旧 H:/.../launcher 路径不存在。H盘保留了转到C盘的旧自动入口。
- 2026-10-14 18:35:59 Hermes已通过，18:42:00 Docker API等候300秒失败。
- Docker日志 10:32:47Z 报 provisioning data: detecting disk: no sd* disk ... wwid ...。docker_data.vhdx存在，34468790272字节；缺少虚拟机内磁盘设备，不等于磁盘文件丢失。最初导致磁盘未识别的触发条件尚未确认。
- 官方 docker desktop restart --timeout 60 因已列出的 Docker 进程卡住失败。
## 实际恢复
- 精确核对 Docker 可执行路径后结束其残留前后端；仅 terminate docker-desktop。
- 指定 docker_data.vhdx 的 unmount 返回 ERROR_FILE_NOT_FOUND（未挂载）；未删除、迁移、修复文件系统或重装。
- 官方 docker desktop start --timeout 90 成功；原有容器恢复。
- 未改变 FlClash、系统代理、Hermes 配置、模型配置、凭据、会话或聊天数据库。
## 最小持久修复
C:/Users/A/Hermes_Windows_Native_014/launcher/start-hermes-openwebui.ps1：
1. Docker CLI探针最多8秒，使用Process超时与退出码判断。
2. 常规等待失败后仅一次官方 restart，65秒外层限时，再检查API；仍失败明确退出，不执行自动批量杀进程。
3. 修正默认入口条件表达式缺少括号；健康时实测跳过90秒等待。
原始备份：同目录 start-hermes-openwebui.ps1.bak-20261014-docker-recovery。
原始SHA256：2C4D0BD260EB926DDC536459B995F346CFC529E3C19442C4ABD5601453A9BBE7。
修复后Windows SHA256：38EADDD4810CDE4D4DED62BCB54531BCB78593E89AE0702DA6CC45D709772CA0。
桌面 C:/Users/A/Desktop/打开爱马仕.cmd 与 H:/Hermes_Windows_Native_014/打开爱马仕页面-双击.cmd 使用同一受检启动器。
原登录启动 HermesOpenWebUIAutoOpen.vbs 保留；其指向的 C盘启动器已修复。
## 验收
- PowerShell 5.1解析/统一执行门PASS；PSScriptAnalyzer未安装，未宣称分析器PASS。
- Pester 3/3：健康不重启、正常启动不重启、超时只尝试一次官方恢复。
- 8642 /health=200，version=0.21.5。
- 授权 /v1/models=200，含 DeepSeek-V4.1-Flash 等五个模型。
- 真实 /v1/chat/completions 使用 DeepSeek-V4.1-Flash 返回 HERMES_STARTUP_REPAIR_OK。
- Open WebUI容器 healthy，3000/health=200。
- 从Open WebUI容器读取仅连接配置，使用已有认证请求 host.docker.internal:8642/v1/models，返回200及五个模型。未输出密钥。
- 默认启动流程 19:32:13–19:32:19，FINAL_PASS；统一门进程总时7.52秒，仅是热启动单次记录，不是全任务耗时或提升率。
- 19:32:19 浏览器打开调用成功；未以截图核验页面、未进行网页登录聊天端到端测试。
- 独立回读确认桌面入口、自启动入口存在，网页200、容器健康、最终SHA匹配。
## 未验收边界
没有重启整台Windows；下一次实际登录/重启后的完整恢复尚待验证。
官方恢复失败后的强制清理为本次人工限定修复，未加入开机自动循环。
## 官方依据
https://docs.docker.com/desktop/troubleshoot-and-support/troubleshoot/
https://docs.docker.com/desktop/features/desktop-cli/
https://learn.microsoft.com/windows/wsl/reference
