# 双上下文采集模型
## TARGET
真正需要复制的 Codex 执行环境；动态行为以 TARGET 或 Codex 运行时为权威。
## COLLECTOR
仅补充宿主静态事实的沙盒外非管理员只读环境；COLLECTOR 能做到不等于 TARGET 能做到。
## 首个现实案例
TARGET 三次启动相同只读 PowerShell 子进程，均在 `SetTokenInformation(TokenDefaultDacl)` 返回 `1344`；COLLECTOR 等价操作成功。已冻结为 `TARGET_PROCESS_CREATION_RESTRICTION_REPRODUCED=YES`，未继续测试、修复或调查根因。