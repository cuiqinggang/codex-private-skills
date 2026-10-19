---
name: gpt-windows-execution-bridge
description: 正式执行桥 V11.0。C-first 强制门禁，只有 C 经双重故障验证和安全检查点才可切 A，A 失败才 B。
---
# 《GPT直连Windows双路执行桥》正式入口 V11.0

**权威规则：** `v11-c-first-enforced-routing.md`；执行判定程序：`guard_route.py`。

每个 Windows 任务先 C 的 list_devices 动态发现，再 ping + 无副作用 PowerShell 探针。C PASS ⇒ LOCK_C；禁止绕过直接调用 A/B。C 明确失败且重试仍失败 ⇒ 凭审计证据和安全检查点运行 `guard_route.py`，ALLOW 才能切 A；A FAIL 后才能考虑 B。UNKNOWN 一律先对账、禁止误降级。所有外部受控入口须接入门禁。

本地门禁代码不能物理拦截平台原生工具调用；跨会话强制接入未经验证之前，不得声称全局门禁 PASS。不要改变 FlClash、代理、密钥、网络或隧道。

继承 V10.0 动态发现规则及 V10.1 判定逻辑，不覆盖历史证据。
