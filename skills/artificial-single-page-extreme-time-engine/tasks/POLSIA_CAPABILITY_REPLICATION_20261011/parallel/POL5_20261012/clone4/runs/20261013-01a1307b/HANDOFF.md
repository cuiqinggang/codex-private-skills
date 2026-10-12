# 公开页面与四路任务接续交付

当前本地地址 http://127.0.0.1:55437/，实际业务 /workspace，公开页已在用户可见Codex Browser保留。先读 ACCEPTANCE_REPORT.md、CODEX_FULL_COMMAND_V3.md、SOURCE_RECEIPTS.json；V001–V008与母CURRENT/Freeze仍只读。

本轮 source/ 是完整文本源码与锁文件，使用成熟 open-polsia 基准 c62ba0be3368815dc9011848d96875ef228f1607。原图片/字体/WAV/CSS没有放入Git；从新克隆的干净仓库覆盖本轮 source 文本后，运行 node scripts/restore-public-assets.mjs（默认只读计划）及 --apply（仅下载缺失原资产），最后 --verify-only。相邻清单固定36来源URL/SHA/字节及23公开文本SHA；已有不匹配目标会阻断，不支持覆盖。不要删除旧工作副本或复制.env/认证资料来绕过。

当前本机已经完整运行，无需再次下载、启动或执行完成任务。接手从最新live receipt核对PID/启动时间/Node路径/参数/SQL/HTTP；PG58916与Node64728仅为当前观察，不是永久ID。新位置运行需要独立loopback PostgreSQL并沿用package/pnpm锁文件，只使用C盘。启动进程局部环境 PORT=55437、DATABASE_URL=postgres://polsia_local@127.0.0.1:55433/polsia、POLSIA_STAGING=on、POLSIA_WORKER=off、POLSIA_CODEX_JOBS=on；使用Node24以上 node --experimental-transform-types src/services/dashboard.ts。不要将此局部环境设成Windows全局配置。

源码快照没有数据库、运行队列、模型日志、用户凭据或node_modules。四完成job继续保留在原本机持久目录，不能迁移成新待执行任务。新机器先验源码/资产再建立独立测试公司；需要原历史证据时按原四命令精确C源及原Git路径读取，不猜、不重放。

公开视觉门禁通过不代表整套Polsia业务完全对等、99.9%全站量化或零bug。私有页由用户留待真实参考；付款/OAuth/外联/投放/派单/公网部署仍未接入。
