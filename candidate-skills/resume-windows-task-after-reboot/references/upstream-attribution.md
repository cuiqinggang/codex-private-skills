# 上游依据

- Microsoft Task Scheduler BootTrigger：使用操作系统启动触发任务。
- Microsoft PowerShell 兼容性说明：现代 PowerShell 不再提供 PowerShell Workflow；跨重启应使用 Task Scheduler 并自行持久化状态。
- Ansible `win_reboot`：以 `Win32_OperatingSystem.LastBootUpTime` 作为稳定 boot identity 的成熟做法。
- Microsoft Configuration Manager task sequence：把重启视为显式步骤并从已知步骤继续。
- HashiCorp Packer `windows-restart`：等待重启、超时和重启后继续的成熟边界。

实现吸收这些公开接口与方法，不复制第三方代码。使用时以相应产品的官方文档为准。
