# V5.0 附件三｜失败反例和跨版本防回归门禁

本清单每条均来自已有真实日志、工具回执、用户截图或明确失败候选；不能当作“所有环境都会如此”的定理。执行前优先复用`powershell-reliability-guard`、原V2 A路SOP及V3 B路成熟合同。

| 错误编号 | 历史失败 / 风险 | 已确定的纠偏 |
|---|---|---|
| E01 | 临时 `Validate-OneTunnel-Recovery-20261015.ps1` 对正常PID17876执行Stop-Process，造成断线，100秒无恢复 | 禁止再运行此临时脚本；不以破坏正常连接来“刷稳定次数” |
| E02 | 旧PID仍在线却真实MCP请求报409 | 健康与MCP握手分离，真正调用工具才验证ChatGPT到Windows |
| E03 | HTTP/health健康或插件管理页显示正常，当作全程成功 | 必须检查read_file正文/真实Windows操作回执，不能仅看注册和进程 |
| E04 | 源文件已补丁但常驻旧Supervisor未加载 | 区分文件SHA、Supervisor新旧PID、Tunnel父子关系；合法原任务重载后复核 |
| E05 | PS5.1误将官方Tunnel native stderr作为致命异常 | 用现成PS-002规则，以`$LASTEXITCODE`和实际业务状态判断 |
| E06 | 试图`1>$null 2>$null`消除PS5.1 RemoteException仍失败 | 保留该失败候选，不能在生产重复 |
| E07 | 参考GitHub整文件与Windows本机实际内容存在差异 | 原SHA冻结、局部唯一代码差分、原子备份、重新回读，禁止覆盖无关资产 |
| E08 | MCP工具回执内部是嵌套JSON，观察器字符串子串匹配误记FAIL | 结构化解析原始回执、退出码和后置条件，不凭嵌套包装字符串 |
| E09 | 桌面脚本2秒关闭健康窗口被理解为Tunnel停止 | 窗口与后台PID分开，交互按Enter退出状态窗 |
| E10 | 刚启动出现MCP_NOT_INITIALIZED就再次双击快捷方式 | 唯一PID最多180秒等初始化；拒绝启动第二实例；超时明确显示 |
| E11 | 为409机械刷新页面、多次输密钥或另开Tunnel | 先记录进程、子进程代次、initialize/initialized与真实错误；只按成熟SOP采取最小恢复 |
| E12 | 低权限GitHub Runner访问用户A资料被拒绝后准备改ACL | 保留拒绝，不能提权绕过；优先合法A路读写 |
| E13 | V3旧章节的“最新”旧PID、旧状态覆盖V4/V5正式入口 | 新页一律先V5 `SKILL.md`，旧章按日期视为历史证据 |
| E14 | 用B小型工件5/5、Hermes合成42/42或A短时8/8宣布整桥长期0故障 | A/B与各合同独立计数，真实开机与无人恢复另验 |
| E15 | 把开发插件管理权限配置与运行可用混同 | 插件设置只是配置；远端read_file或执行端到端才算可用 |
| E16 | 无人登录系统时要求现有Interactive账户任务自动连接 | 当前只有用户A登录触发，不宣称Windows未登录即可通 |
| E17 | 为确认开机自启主动重启电脑，影响并行生产 | 等待用户主动下次自然启动，再取证；未经授权不主动重启 |
| E18 | 用测试所需伪造MCP `initialize`消息填协议缺口 | 官方通知shim不会替代缺失的initialize；调用方会话需官方流程诊断 |
| E19 | 运行中发生`Session terminated`一律归咎代理不稳定 | 先查Tunnel是否进程退出，若同PID仍在则单独调查初始化、会话层、控制平面 |
| E20 | 某次脚本/命令调用返回HTTP400直接怪Tunnel | 业务API参数/请求合同先自查；Hermes F002单独记录不能混入桥接验收 |

## 停止规则与防泄漏
- 每个副作用任务Exactly-once，未知是否派发/执行成功则先对账，不自动重试。
- 未批准时不修改FlClash、代理、Runner配置、插件权限、Windows ACL、凭据或已登录浏览器。
- Runtime Key只由用户在本机合法界面填写/由受限DPAPI使用；不索取、读取、记录、发送。
- 不读取私人会话，不把包含凭据和商业私密信息的结果放入GitHub Job Outputs/Base64工件。
- 进程存在不等于健康；`HEALTHY_PATH_ONLY`不等于PID身份完全确认；一次短测不是长期可用率。
- 故障消失且合同PASS后停止无净收益的反复修改；新失败按GOOD/BAD/FIRST_DELTA重开。
