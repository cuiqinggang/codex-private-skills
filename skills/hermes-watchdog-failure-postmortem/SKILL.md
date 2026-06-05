# Hermes Watchdog 失败复盘
用途：记录 Hermes Windows native 0.14 Watchdog 失败链路，防止以后重复陷入复杂补丁式修复。

核心结论：当 Hermes 主系统已经被多代 watchdog、Startup、计划任务、NewAPI recovery 脚本搅乱时，不应继续补丁式修 watchdog；应优先使用 H 盘完整恢复包恢复 Windows native Hermes 0.14 主系统。

已确认问题：1）多代 Watchdog mutex 名不同导致锁失效；2）Watchdog 自己崩溃退出但缺少诊断日志；3）Gateway 自动恢复失败且无完整日志；4）启动项碎片化，Startup、计划任务、NewAPI recovery 三套机制互相干扰。

推荐路线：先验证 H:\_FULL_RECOVERY_Hermes_Windows_Native_014_20260520 完整恢复包，再按 RESTORE_GUIDE.md 恢复主系统；恢复后先验证 8642 health/models/chat，再处理 Open WebUI / New API；watchdog 后置。

禁止路线：不要在坏环境里继续叠加 v1/v2/v3 watchdog；不要污染完整恢复包；不要未经确认修改 Startup 或计划任务。
