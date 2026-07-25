# 上游依据

- Microsoft Hyper-V checkpoints：创建、应用和删除 VM checkpoint。
- Microsoft Hyper-V PowerShell module：`Get-VM`、`Checkpoint-VM`、`Restore-VMSnapshot`、`Restart-VM` 与网络适配器命令。
- Microsoft PowerShell Direct：从 Hyper-V 宿主与 Windows guest 通信，不依赖 guest 网络。
- Microsoft Windows edition/Hyper-V requirements：确认宿主版本和虚拟化前提。

实现只包装官方 Hyper-V 管理接口，不包含虚拟机镜像、Windows ISO、360 安装包或第三方代码。
