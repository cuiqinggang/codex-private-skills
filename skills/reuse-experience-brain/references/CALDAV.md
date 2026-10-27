# EXP-CALDAV-001｜取消成功但缓存残留
版本V1；证据日期2026-10-24；状态：限定Tymeslot1.30.0本地合成合同通过。
触发：Tymeslot CalDAV远端已删除，缓存仍保留事件。
故障指纹：会议UID与provider_event_id/href缓存键混用。先沿远端删除→标识映射→本地缓存找首差。
已记录最小修复：复用`CalendarEventLink.identifiers` + `ProviderCalendarEventQueries.get_by_identifiers`映射；成功删除后`CalendarEventCache.forget`；远端删除失败时保留缓存与现有重试语义，不提前清空造成“看起来成功”。
原回执实际读回：status=CONFIRMED_COMMITTED_P0_BUSINESS_PASS；3轮真实双独立浏览器同槽竞争、取消/重启/远端短暂故障/提交重放；37项业务断言通过。失败期间cache_retained_while_remote_down=true；overallMatchedTValid=NOT_VERIFIED。
边界：本地Tymeslot/Radicale/Mailpit合成合同；不代表生产公网邮件、断电恢复、永久自动一致性或另一版本已验证。更新前先读当前源码/合同；不能把3轮测试用时当完整交付时间。
证据：`C:\AI\AI-Web-Replication-V1.2-20261024\FINAL-ACCEPTANCE.json`（2026-10-27实际读回，摘录不含测试姓名/邮件）；故障定位继承`C:\Users\A\.codex\obsidian-vaults\AI-COMPANY-KNOWLEDGE-OS\01_DAILY\2026-10-24-DSE-INCREMENTAL.md`，非本次重跑故障。
