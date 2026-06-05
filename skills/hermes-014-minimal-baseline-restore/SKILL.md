# Hermes 0.14 分阶段恢复技能包

## P1+P2 稳定基线体检与状态备份
状态：已通过。
范围：Hermes 0.14 最小状态 + Open WebUI 浏览器端口。
验收：8642 health/models/chat 正常；3000 可访问；Open WebUI 直连 8642；NewAPI/Postgres/Redis/Telegram/Watchdog/AutoRecover 不运行。
状态备份：H:\Hermes_Backups\HERMES-014-P1P2-HEALTH-BACKUP-20260522\stable-p1p2-20260522_185206
规则：New API 后置，Telegram 下一阶段单独接入，Watchdog 最后重新设计。
