# 实验室安全合同

## 允许的宿主

- Windows Pro、Enterprise 或 Server，已启用 Hyper-V。
- 管理员会话。
- 具有足够磁盘空间的专用测试卷。
- 预先创建、明确标记 disposable 的 Windows guest。

不在容器、WSL、云端 Linux 工作区或真实业务终端上冒充 Hyper-V 实测。

## 网络

| 模式 | 行为 |
|---|---|
| `None` | 默认；断开 VM 的所有网络适配器 |
| `Private` | 只连接预先存在且类型为 Private 的 Hyper-V switch |
| `External` | 禁止 |

需要下载测试 payload 时，先在隔离执行之外取得合法文件、记录来源/版本/签名/SHA-256，再把固定文件送入 guest。不要让未知软件在联网状态运行。

计划必须绑定初始 VM network adapter ID 集合；Private 模式还绑定 switch ID。Prepare 改网后、ExecutePayload 前及每次 RestartGuest 前都重新验证：adapter 集合完全一致；None 模式全部断开；Private 模式全部且只连接固定 ID 的 Private switch。新增 adapter、External/Internal 连接或 switch 漂移立即阻断并进入自动恢复。

## Checkpoint 与回滚

执行前记录 VM ID、configuration version、磁盘路径和 adapter。建立唯一 baseline checkpoint。每个 checkpoint 名含 run id，不覆盖旧快照。

失败时：

1. 停止后续 guest 操作。
2. 导出已取得的只读证据。
3. 关闭 disposable VM。
4. 恢复本 run 的 baseline checkpoint。
5. 启动 guest，并通过 PowerShell Direct 验证 baseline 前不存在的测试 marker 已消失；验证失败不得称已恢复。

checkpoint 不是备份；测试 VM 必须可丢弃重建。

## 证据

每个事件记录：run id、UTC 时间、宿主名、VM ID、action、checkpoint id、guest boot id、VM state、退出码、payload SHA-256、evidence file SHA-256 和错误。凭据、token、个人文件和安装包内容不得写入日志。

任何必需证据缺失时不得标 PASS。
