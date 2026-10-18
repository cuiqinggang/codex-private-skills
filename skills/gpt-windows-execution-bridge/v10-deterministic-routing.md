# 《GPT直连Windows双路执行桥 V10.0》——动态发现与禁止误降级规则
版本：10.0
发布日期：2026-10-18
权威仓库：cuiqinggang/codex-private-skills
继承：V9.0 的 C→A→B、Exactly-once、安全边界；本版新增「动态设备发现硬门禁」。
适用：《三人行》第3版及所有调用 Windows 执行桥的任务。

## 核心故障与修复
2026-10-18 实测，同一台 DESKTOP-4A1EGTM 存在离线旧设备 ID（503e66bf-4f80-49fc-a90f-020ec8c71b1e、28ebd1ea-e749-466d-ad88-1b9f262d0651）及在线新设备 ID（f6990966-5870-484b-bf79-409bc6fb963e）。对新设备的 ping 返回 pong，且经 C 通道 PowerShell 实际返回主机名与桌面目录 True。故不能将旧 ID 离线误判为 C 故障。ID 是运行时发现值，以上 ID 仅为历史证据，不得硬编码。

## 强制前置门禁：每个新任务均须执行
1. **DISCOVER_C**：先调用 C（Remote Desktop Commander）的 list_devices。严禁先检查缓存的旧 ID 后直接转 A；禁止以“上一任务 A 可用”为依据。
2. **MATCH_TARGET**：按已授权目标电脑名称匹配（例如 DESKTOP-4A1EGTM）；从当前列出的 Online 设备中选取有效 deviceId，不依赖历史固定 ID。
3. **MULTIPLE_ONLINE**：若多个同名设备在线，以无副作用 ping 逐一验证；再用无副作用实际命令验证目标主机名，确定唯一正确会话；不能明确辨认时停止并报告，不得猜测或自动跳 A。
4. **VERIFY_C**：对选中的在线设备 ping，再执行一条无副作用 PowerShell 业务探针（如输出标识、hostname、Test-Path 桌面目录），记录真实回执。
5. **LOCK_C**：验证成功，即本任务锁定 C，所有 Windows 执行优先通过 C。不得因便利、历史行为、速度猜测而选择 A/B。
6. **RETRY_C**：只有发现失败、连接失败或无副作用业务探针失败，才在重新 list_devices 后进行一次有界重试；不可只重试旧 ID。
7. **FALLBACK_GATE**：两次当前发现及探测均有明确失败证据后才允许 CHECK_A→EXECUTE_A；A 失败才 CHECK_B→EXECUTE_B。枚举出可用 C 时绝不切 A。
8. **RECOVER_C**：每个新任务都重新 DISCOVER_C；先前故障降级不得持久化。执行中仅安全检查点换道，遵守 Exactly-once，不重复副作用命令。
9. **AUDIT**：至少记录 task_id、探测时间、目标电脑名、在线/离线设备列表、选中的运行时 deviceId、ping、业务探针、路由决策、降级失败证据；无审计证据不得宣称 C 不可用。
10. **FAIL_CLOSED**：工具临时不可用、无法识别目标设备、探针输出不明确时应报告当前未验证，不得擅自把“未知”改写为“失败并可用 A”。只有确认 C 连续不可用时才允许降级。

## 判定状态机
START → DISCOVER_C → MATCH_TARGET → PING_C → VERIFY_C
- PASS → LOCK_C → EXECUTE_C
- FAIL/UNKNOWN → DISCOVER_C_RETRY_ONCE → PING_C → VERIFY_C
- RETRY_PASS → LOCK_C → EXECUTE_C
- RETRY_FAIL_WITH_EVIDENCE → CHECK_A → [A_PASS → EXECUTE_A；A_FAIL → CHECK_B]
- 无法确认目标或无充分故障证据 → STOP_AND_REPORT（不可推断 A 合法）
注：C 的业务探针不意味着所有实际业务都必然成功；真实命令异常依照幂等、安全检查点和故障证据处理。

## 禁止事项
- 不得关闭用户登录的专用浏览器。
- 不得修改 FlClash、Windows 系统代理、虚拟网卡、网络设置、密钥或隧道。
- 不得使用旧设备 ID 离线、单次超时、网页状态或之前选 A 作为降级理由。
- 不得把文本规则已提交等同于外部执行器自动完成接入。

## 实证与待验收界限
已完成的实测（2026-10-18）：list_devices 发现新 Online ID；C ping 得到 pong；通过 C PowerShell 返回 C_CHANNEL_BUSINESS_PASS、DESKTOP-4A1EGTM、True。
仍需独立验证：在未来新会话/其他执行器中本规则是否实际被读取；C 故障与 A/B 接管完整状态机的真实测试（不得主动破坏网络、代理或已登录环境）。
发布验收：GitHub main 上正式入口指向 V10.0，回读一致；真实业务可走 C。只有完成执行端跨会话门禁验证后，才能称为“执行器自动强制接入”。
