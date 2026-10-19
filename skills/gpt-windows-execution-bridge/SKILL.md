---
name: gpt-windows-execution-bridge
description: Windows正式执行桥入口。V10.1 C-FIRST 强制降级判定，C→A→B。
---
# 《GPT直连Windows双路执行桥》正式入口：V10.1

权威文件：`v10.1-c-first-guard.md`，继承 `v10-deterministic-routing.md`。
每个新任务先使用 Remote Desktop Commander list_devices 动态发现 C，ping 并无副作用命令验证目标主机。C PASS 锁定 C。禁止直接使用 GPT_Windows_MCP_Bridge(A)。
仅在 C 的两次真实检查明确失败且有证据，并确认安全检查点后，先调用 `guard_route.py`，ALLOW 才可执行 A；A 明确失败后才考虑 B。UNKNOWN 禁止降级。所有 A/B 执行端应接入本门禁，不能绕过。
历史离线设备ID不是C故障证据；不改变代理、FlClash、密钥及网络设置。
注意本地门禁不能拦截直接向平台 MCP 发起的调用，跨会话接入需要额外回归验证。
